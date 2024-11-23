# from reportlab.lib.pagesizes import A4
# from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.utils.translation import gettext as _

from basket.utils import BasketMixin, BasketOperationTypes
# from apps.payment.services import paypal_create_order
from order.models import OrderItems, Order
from address.models import ShippingAddress, BillingAddress
from catalogue.models import Product
from rest_framework.response import Response
from django.db.models import Sum
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
# from .services import draw_pdf_invoice
from catalogue.services import get_discount
# from .tasks import order_send_email_with_invoice

# email_sender = settings.EMAIL_HOST_USER


class OrderMixin(BasketMixin):
    """
    Mixin which creates order with items
    from user's basket. Creates order and
    returns response with order data or
    with error message. Also, mixin have method
    which gets or creates user's shipping
    info and returns it. And to all this, there is
    a method for sending an invoice to the mail.
    """
    items_serializer = None
    operation_type = BasketOperationTypes.basket_clear
    __request = None
    # invoice_html_template = 'orders/invoice_msg.html'
    send_invoice_with_celery = False

    @property
    def request(self):
        return self.__request

    @request.setter
    def request(self, request):
        self.__request = request

    @staticmethod
    def get_not_available_basket_products(basket_data: dict) -> list:
        """
        Returns list with products from user's basket
        which are not available at the moment.

        Args:
            basket_data(dict): data with basket information.

        Returns:
            not_available_basket_products(list): list with not available
                                                 products from the basket.
        """
        basket_products_ids = []
        for item in basket_data['items']:
            basket_products_ids.append(item['product'])
        not_available_basket_products = Product.objects.filter(
            id__in=basket_products_ids,
            is_public=False,
            quantity=int(0),
            # availability_status=AvailabilityStatuses.out_of_stock[0]
        ).values_list('id')
        return not_available_basket_products

    @staticmethod
    def get_order_total_values(order: Order) -> dict:
        """
        This method returns dict with order
        total amount and total bonuses amount.
        """
        total_values_order = order.items.aggregate(total_amount=Sum('total_price'),)
        return total_values_order

    def process_order_payment_with_bonuses(self, order: Order):
        """
        Processes the payment for the given order
        using user bonuses balance and updates the
        payment status and order total amount accordingly.
        """
        order_total_values = self.get_order_total_values(order)

        order_total_amount = order_total_values['total_amount']
        order_total_bonuses_amount = order_total_values['total_bonuses_amount']

        if order.user and order.activate_bonuses and order.user.bonuses_balance:
            # bonuses will be withdrawn from the user's bonuses balance
            # only if he has selected this option
            user_bonuses = order.user.bonuses_balance.balance

            if user_bonuses >= order_total_amount:
                # if the user's balance is greater than the
                # total amount of the order, the total amount
                # of order will be deducted from user's bonuses
                # balance and order will be marked as paid.
                order.user.bonuses_balance.balance = user_bonuses - order_total_amount
                order.user.bonuses_balance.save()

                payment_info = order.payment_info
                payment_info.is_paid = True
                payment_info.save()

                if order_total_bonuses_amount > 0:
                    # add order bonuses to the user's balance
                    # we have the same operation in payment/signals.py in
                    # pre save signal, but in this case it won't be working
                    # because initially order not is_paid what is needed to call
                    # pre save method
                    order.user.bonuses_balance.balance += order_total_bonuses_amount
                    order.user.bonuses_balance.save()
                    payment_info.bonus_taken = True

                payment_info.payment_amount = order_total_amount
                payment_info.save()

            elif order_total_amount > user_bonuses > 0:
                order.user.bonuses_balance.balance = 0
                order.user.bonuses_balance.save()
                order_total_amount -= user_bonuses

        order.total_bonuses_amount = order_total_bonuses_amount
        order.total_amount = order_total_amount
        order.save()

    def order_total_amount_with_coupon(self, order: Order) -> bool:
        """
        This method counts order total amount
        if order have coupon.

        Args:
            order(Order): order instance.

        Returns:
            bool: True or false depending on whether the total
                  amount of the order has been changed.
        """
        order_total_values = self.get_order_total_values(order)
        order_total_amount = order_total_values['total_amount']

        if order.user and order.coupon and order.coupon.is_active:
            order_total_amount = get_discount(order_total_amount, order.coupon.coupon.discount)
            order.total_amount = order_total_amount
            order.coupon.is_active = False
            order.coupon.save()
            order.save()
            return True
        return False

    # def send_email_with_invoice(self, order: Order):
    #     html = render_to_string(self.invoice_html_template, {'order': order})
    #     invoice = draw_pdf_invoice(order)

    #     subject = 'DRF ECOMMERCE'
    #     message = f'Invoice for order# {order.id}'
    #     if self.send_invoice_with_celery:
    #         order_send_email_with_invoice.delay(message=message,
    #                                             subject=subject,
    #                                             email=order.shipping_info.email,
    #                                             order_id=order.id,
    #                                             html=html)
    #     else:
    #         email = EmailMultiAlternatives(message, subject, email_sender, [order.shipping_info.email])
    #         email.attach('invoice.pdf', invoice, 'application/pdf')
    #         email.attach_alternative(html, 'text/html')
    #         email.send(fail_silently=True)

    def create_order(self, response) -> Response:
        """
        Creates order and returns response with order data
        or with problems creating an order.

        Args:
            response: response from create method of ListCreateAPIView.

        Returns:
            Response: response with order data or with its problems.
        """
        basket_data = self.get_basket_data(self.request)

        if self.request.user.is_authenticated:
            # we need it in this case because in this
            # way we avoid unnecessary access to the cart table.
            self.clear_exist_basket(self.request)
        # else:
        #     self.basket_operation(self.request)

        not_available_basket_products = self.get_not_available_basket_products(basket_data)

        if not len(not_available_basket_products) > 0:
            # order will be created, if in user's basket
            # don't have products that are not available.

            if len(basket_data['items']) > 0:
                # if user's basket is not empty
                order_id = response.data['id']

                try:
                    order = Order.objects.select_related('user').prefetch_related('items').get(id=order_id)
                except Order.DoesNotExist:
                    return Response({'error': 'Order does not exist!'})

                for item in basket_data['items']:
                    # items['product'] - id of product
                    OrderItems.objects.create(order=order,
                                              product_id=item['product'],
                                              quantity=item['quantity'],
                                              total_price=item['total_price'])

                order_items = order.items.all().select_related('order',
                                                               'product')

                if order.coupon and self.order_total_amount_with_coupon(order):
                    # here order total amount with discount from coupon
                    response.data['total_amount'] = order.total_amount
                else:
                    response.data['total_amount'] = order_items.aggregate(
                        total_amount=Sum('total_price'))['total_amount']
                
                order.total_amount = response.data['total_amount']
                order.order_id = response.data['id']
                order.save()
                
                # if response.data['payment_method'] == Order.PAYMENT_METHODS[1][0] and not order.payment_info.is_paid:
                #     # if payment method is by card, to the response
                #     # will be added PayPal payment link
                #     value = response.data['total_amount']
                #     response.data['payment_link'] = paypal_create_order(value, order_id)
                # else:
                #     self.process_order_payment_with_bonuses(order)
                #     # we are  processing order payment with bonuses here only if
                #     # payment method is by cash, to avoid withdrawal
                #     # of bonuses without payment(in case if payment method is by card).
                #     self.send_email_with_invoice(order)

                # # هووووووووووننننننن بس زبط السيليري  لازم شغلا
                # if response.data['payment_method'] == Order.PAYMENT_METHODS[0][0] and not order.payment_info.is_paid:
                #     self.send_email_with_invoice(order)
                response.data['order_items'] = self.items_serializer(instance=order_items,
                                                                     many=True).data
                return response
            else:
                return Response({'basket': 'You dont have items in your basket!'})
        else:
            return Response({'not available': 'Some items in your basket are not available'})

    def get_user_shipping_info(self, shipping_info_data: dict) -> ShippingAddress:
        """
        This method gets or creates user's
        shipping info and returns it.

        Args:
            shipping_info_data(dict): dictionary with order shipping info data.
            session_id(str): session id of user.

        Returns:
            shipping_info(ShippingAddress): returns user's shipping info.
        """
        if self.request.user.is_authenticated:
            shipping_info, _ = ShippingAddress.objects.get_or_create(user=self.request.user,
                                                                      defaults=shipping_info_data)
        #     if not shipping_info.session_id:
        #         shipping_info.session_id = session_id
        #         shipping_info.save()
        # else:
        #     shipping_info, _ = ShippingAddress.objects.get_or_create(session_id=session_id,
        #                                                               defaults=shipping_info_data)
        shipping_info.phone_number = shipping_info_data['phone_number']
        shipping_info.notes = shipping_info_data['notes']
        shipping_info.city = shipping_info_data['city']
        shipping_info.street_address = shipping_info_data['street_address']
        shipping_info.apartment_address = shipping_info_data['apartment_address']
        shipping_info.apartment_address = shipping_info_data['apartment_address']
        shipping_info.is_default_for_shipping = True
        # shipping_info.is_default_for_billing = False
        shipping_info.save()
        return shipping_info

    def get_user_billing_info(self, billing_info_data: dict) -> BillingAddress:
        """
        This method gets or creates user's
        shipping info and returns it.

        Args:
            shipping_info_data(dict): dictionary with order shipping info data.
            session_id(str): session id of user.

        Returns:
            shipping_info(ShippingAddress): returns user's shipping info.
        """
        if self.request.user.is_authenticated:
            billing_info, _ = BillingAddress.objects.get_or_create(user=self.request.user,
                                                                      defaults=billing_info_data)
        #     if not billing_info.session_id:
        #         billing_info.session_id = session_id
        #         billing_info.save()
        # else:
        #     billing_info, _ = BillingAddress.objects.get_or_create(session_id=session_id,
        #                                                               defaults=billing_info_data)
        billing_info.phone_number = billing_info_data['phone_number']
        billing_info.notes = billing_info_data['notes']
        billing_info.city = billing_info_data['city']
        billing_info.street_address = billing_info_data['street_address']
        billing_info.apartment_address = billing_info_data['apartment_address']
        billing_info.apartment_address = billing_info_data['apartment_address']
        # billing_info.is_default_for_shipping = False
        billing_info.is_default_for_billing = True
        billing_info.save()
        return billing_info





# from reportlab.lib.pagesizes import A4
# from reportlab.pdfgen import canvas
# from reportlab.pdfbase.ttfonts import TTFont
# from reportlab.pdfbase import pdfmetrics
# import arabic_reshaper
# from bidi.algorithm import get_display
# from io import BytesIO
# from django.http import HttpResponse

# arabic_font_path = 'static/fonts/Amiri-1.000/Amiri-Regular.ttf'

# def generate_invoice_pdf(order):

    # pdfmetrics.registerFont(TTFont('Amiri', arabic_font_path))
    
    # buffer = BytesIO()
    # pdf = canvas.Canvas(buffer, pagesize=A4)
    # width, height = A4

    # pdf.setFont("Amiri", 16)

    # arabic_title = "فاتورة"
    # reshaped_title = arabic_reshaper.reshape(arabic_title)
    # bidi_title = get_display(reshaped_title)
    # pdf.drawRightString(width - 50, height - 50, bidi_title)

    # y_position = height - 100

    # pdf.setFont("Amiri", 12)
    # order_id_text = f"رقم الطلب: {order.order_id}"
    # reshaped_order_id = arabic_reshaper.reshape(order_id_text)
    # bidi_order_id = get_display(reshaped_order_id)
    # pdf.drawRightString(width - 50, y_position, bidi_order_id)
    # y_position -= 20

    # user_text = f"المستخدم: {order.user.email if order.user else 'ضيف'}"
    # reshaped_user = arabic_reshaper.reshape(user_text)
    # bidi_user = get_display(reshaped_user)
    # pdf.drawRightString(width - 50, y_position, bidi_user)
    # y_position -= 20

    # status_text = f"حالة الطلب: {dict(Order.ORDER_STATUSES).get(order.order_status, 'غير معروفة')}"
    # reshaped_status = arabic_reshaper.reshape(status_text)
    # bidi_status = get_display(reshaped_status)
    # pdf.drawRightString(width - 50, y_position, bidi_status)
    # y_position -= 20

    # total_amount_text = f"إجمالي المبلغ: {order.total_amount} عملة"
    # reshaped_total_amount = arabic_reshaper.reshape(total_amount_text)
    # bidi_total_amount = get_display(reshaped_total_amount)
    # pdf.drawRightString(width - 50, y_position, bidi_total_amount)
    # y_position -= 40

    # shipping_title = "معلومات الشحن:"
    # reshaped_shipping_title = arabic_reshaper.reshape(shipping_title)
    # bidi_shipping_title = get_display(reshaped_shipping_title)
    # pdf.drawRightString(width - 50, y_position, bidi_shipping_title)
    # y_position -= 20

    # if order.shipping_info:
    #     city_text = f"المدينة: {order.shipping_info.city}"
    #     reshaped_city = arabic_reshaper.reshape(city_text)
    #     bidi_city = get_display(reshaped_city)
    #     pdf.drawRightString(width - 50, y_position, bidi_city)
    #     y_position -= 20

    #     address_text = f"العنوان: {order.shipping_info.street_address}"
    #     reshaped_address = arabic_reshaper.reshape(address_text)
    #     bidi_address = get_display(reshaped_address)
    #     pdf.drawRightString(width - 50, y_position, bidi_address)
    #     y_position -= 20

    #     postal_code_text = f"الرمز البريدي: {order.shipping_info.postal_code}"
    #     reshaped_postal_code = arabic_reshaper.reshape(postal_code_text)
    #     bidi_postal_code = get_display(reshaped_postal_code)
    #     pdf.drawRightString(width - 50, y_position, bidi_postal_code)
    #     y_position -= 40

    # billing_title = "معلومات الفاتورة:"
    # reshaped_billing_title = arabic_reshaper.reshape(billing_title)
    # bidi_billing_title = get_display(reshaped_billing_title)
    # pdf.drawRightString(width - 50, y_position, bidi_billing_title)
    # y_position -= 20

    # if order.billing_info:
    #     billing_city_text = f"المدينة: {order.billing_info.city}"
    #     reshaped_billing_city = arabic_reshaper.reshape(billing_city_text)
    #     bidi_billing_city = get_display(reshaped_billing_city)
    #     pdf.drawRightString(width - 50, y_position, bidi_billing_city)
    #     y_position -= 20

    #     billing_address_text = f"العنوان: {order.billing_info.street_address}"
    #     reshaped_billing_address = arabic_reshaper.reshape(billing_address_text)
    #     bidi_billing_address = get_display(reshaped_billing_address)
    #     pdf.drawRightString(width - 50, y_position, bidi_billing_address)
    #     y_position -= 20

    #     billing_postal_code_text = f"الرمز البريدي: {order.billing_info.postal_code}"
    #     reshaped_billing_postal_code = arabic_reshaper.reshape(billing_postal_code_text)
    #     bidi_billing_postal_code = get_display(reshaped_billing_postal_code)
    #     pdf.drawRightString(width - 50, y_position, bidi_billing_postal_code)
    #     y_position -= 40

    # items_title = "عناصر الطلب:"
    # reshaped_items_title = arabic_reshaper.reshape(items_title)
    # bidi_items_title = get_display(reshaped_items_title)
    # pdf.drawRightString(width - 50, y_position, bidi_items_title)
    # y_position -= 20

    # for item in order.items.all():
    #     item_text = f"- {item.product.title} x {item.quantity} = {item.total_price}"
    #     reshaped_item = arabic_reshaper.reshape(item_text)
    #     bidi_item = get_display(reshaped_item)
    #     pdf.drawRightString(width - 50, y_position, bidi_item)
    #     y_position -= 20

    #     if y_position < 50:
    #         pdf.showPage()
    #         y_position = height - 100

    # pdf.save()
    # buffer.seek(0)

    # response = HttpResponse(buffer, content_type='application/pdf')
    # response['Content-Disposition'] = f'inline; filename="فاتورة_{order.order_id}.pdf"'
    # return response
