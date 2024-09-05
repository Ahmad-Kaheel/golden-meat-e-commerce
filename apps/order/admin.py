from django.contrib import admin
from order.models import Order, OrderItems

class OrderItemsInline(admin.TabularInline):
    model = OrderItems
    extra = 1
    readonly_fields = ('total_price',)

class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_id',
        'user',
        'order_status',
        'total_amount',
        'shipping_info',
        'billing_info',
        'payment_method',
        'delivery_method',
    )
    list_filter = (
        'order_status',
        'payment_method',
        'delivery_method',
        'created_at',
    )
    search_fields = (
        'order_id',
        'user__email',
        'comment',
        'shipping_info__city',
        'billing_info__city',
    )
    inlines = [OrderItemsInline]
    readonly_fields = ('created_at',)

    def save_model(self, request, obj, form, change):
        if not obj.order_id:
            obj.order_id = f"ORD-{obj.id}"
        super().save_model(request, obj, form, change)

class OrderItemsAdmin(admin.ModelAdmin):
    list_display = (
        'order',
        'product',
        'quantity',
        'total_price'
    )
    list_filter = (
        'product',
        'order',
    )
    search_fields = (
        'product__title',
        'order__order_id',
    )
    readonly_fields = ('total_price',)

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItems, OrderItemsAdmin)
