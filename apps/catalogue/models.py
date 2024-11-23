from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext_lazy
from django.utils.timezone import localtime

from catalogue.managers import CategoryQuerySet, ProductQuerySet
from catalogue.services import get_discount

User = get_user_model()


def category_image_path(instance, filename):
    return f"product/category/icons/{instance.name}/{filename}"


def product_image_path(instance, filename):
    try:
        instance._meta.get_field('title')
        return f"product/images/{instance.title}/{filename}"
    except:
        return f"product/subimages/{instance.product.title}/{filename}"


from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    name = models.CharField(_("Category Name"), max_length=100, unique=True)
    description = models.TextField(_("Description"), blank=True, null=True)
    parent = TreeForeignKey('self',
                            on_delete=models.CASCADE,
                            verbose_name='Parent',
                            blank=True,
                            null=True,
                            related_name='children')
    icon = models.ImageField(upload_to=category_image_path, blank=True)
    is_public = models.BooleanField(
        _("Is public"),
        default=True,
        db_index=True,
        help_text=_("only puplic category can seen."),
    )

    is_wholesale = models.BooleanField(
        _("Is wholesale"),
        default=False,
        help_text=_("Indicates if this category is available for wholesale.")
    )

    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    objects = CategoryQuerySet.as_manager()

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


def get_default_product_category():
    return Category.objects.get_or_create(name="Others")[0]


class Product(models.Model):
    title = models.CharField(
        pgettext_lazy("Product title", "Title"), max_length=255, blank=True
    )
    description = models.TextField(_("Description"), blank=True, null=True)
    price = models.DecimalField(
        decimal_places=2, 
        max_digits=10, 
        validators=[MinValueValidator(0.01)],
    )
    
    quantity = models.IntegerField(
        default=1, 
        validators=[MinValueValidator(1)],
    )

    weight = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        default=1,
        validators=[MinValueValidator(1.00)],
        help_text=_("Total weight of the product in kilograms.")
    )
    
    discount = models.IntegerField(
        default=0,
        verbose_name=_("Discount (Optional)"),
        validators=[MinValueValidator(0), MaxValueValidator(60)],
    )
    
    is_public = models.BooleanField(
        _("Is public"),
        default=True,
        db_index=True,
        help_text=_("Show this product in search results and catalogue listings."),
    )
    is_wholesale = models.BooleanField(
        _("Is wholesale"),
        default=False,
        help_text=_("Indicates if this product is available for wholesale.")
    )
    categories = models.ManyToManyField(
        Category, verbose_name=_("Categories"), 
        related_name='products'
    )
    main_image_url = models.ImageField(upload_to=product_image_path, blank=True)
    recommended_products = models.ManyToManyField(
        "Product",
        through="ProductRecommendation",
        blank=True,
        verbose_name=_("Recommended products"),
        help_text=_(
            "These are products that are recommended to accompany the main product."
        ),
    )
    source_country = models.ManyToManyField('Country', 
                                verbose_name=_("Source Country"), 
                                related_name='products')
    
    rating = models.FloatField(_("Rating"), null=True, editable=False)

    date_created = models.DateTimeField(
        _("Date created"), auto_now_add=True, db_index=True
    )

    # This field is used by Haystack to reindex search
    date_updated = models.DateTimeField(_("Date updated"), auto_now=True, db_index=True)

    objects = ProductQuerySet.as_manager()

    class Meta:
        ordering = ["-date_created"]
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
    
    def __str__(self):
        return self.get_translatable_str

    def clean(self):
        super().clean()

        if self.price_with_discount < 0:
            raise ValidationError(_("The price after discount cannot be negative."))

        if self.quantity < 1:
            raise ValidationError(_("Quantity must be at least 1."))
        
        if self.weight <= 1:
            raise ValidationError(_("Weight must be greater than 0."))

    @property
    def get_translatable_str(self):
        """
        Returns a translatable string including the product name and last modification date.
        """
        formatted_date = localtime(self.date_updated).strftime('%d %B %Y')
        return _('%(title)s, Last updated: %(date)s') % {
            'title': self.title,
            'date': formatted_date
        }
    
    @property
    def price_with_discount(self):
        """
        Returns calculated price with discount.
        """
        price_with_discount = get_discount(self.price, self.discount)
        return price_with_discount

    @property
    def get_product_country(self):
        """
        Returns a comma-separated list of countries associated with the product.
        """
        return ', '.join([country.name for country in self.source_country.all()])


class ProductImage(models.Model):
    product = models.ForeignKey(Product, verbose_name=_("Product"), on_delete=models.CASCADE, related_name='images')
    image_url = models.ImageField(_("Image URL"), upload_to=product_image_path, blank=True)
    alt_text = models.CharField(_("Missing Image"), max_length=100)

    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")

    def __str__(self):
        return _('%(product_title)s - %(alt_text)s') % {
            'product_title': self.product.title,
            'alt_text': self.alt_text
        }


class Country(models.Model):
    name = models.CharField(_("Country Name"), max_length=100)
    icon = models.ImageField(_("Country Icon"), upload_to="country_icons/", blank=True, null=True)

    class Meta:
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")
    
    def __str__(self):
        return self.name


class ProductSpecification(models.Model):
    PREDEFINED_NAME_CHOICES = [
        ('weight', _('Weight')),
        ('expiry_date', _('Expiry Date')),
        ('fat_content', _('Fat Content')),
        ('other', _('Other')),
    ]

    WEIGHT_UNIT_CHOICES = [
        ('kg', _('Kilograms')),
        ('g', _('Grams')),
        ('ton', _('Tons')),
        ('<2_days', _('Less than two days')),
        ('2-4_days', _('Two to four days')),
        ('>4_days', _('More than four days')),
        ('other', _('Other')),
    ]

    PREDEFINED_NAME_CHOICES_AR = [
        ('weight', 'الوزن'),
        ('expiry_date', 'تاريخ انتهاء الصلاحية'),
        ('fat_content', 'محتوى الدهون'),
        ('other', 'أخرى'),
    ]

    WEIGHT_UNIT_CHOICES_AR = [
        ('kg', 'كيلوجرامات'),
        ('g', 'جرامات'),
        ('ton', 'أطنان'),
        ('<2_days', 'أقل من يومين'),
        ('2-4_days', 'من يومين إلى أربعة أيام'),
        ('>4_days', 'أكثر من أربعة أيام'),
        ('other', 'أخرى'),
    ]


    product = models.ForeignKey('Product', 
                                verbose_name=_("Product"), 
                                on_delete=models.CASCADE, 
                                related_name='specifications')

    predefined_name = models.CharField(_("Specification Name"), 
                                       max_length=50, 
                                       choices=PREDEFINED_NAME_CHOICES, 
                                       default='weight')
    
    predefined_unit = models.CharField(_("Unit"), 
                                       max_length=50, 
                                       choices=WEIGHT_UNIT_CHOICES, 
                                       blank=True, 
                                       null=True)

    custom_name = models.CharField(
        _("Custom Specification Name"),
        max_length=100,
        blank=True,
        null=True,
        help_text=_("For example: weight")
    )
    custom_unit = models.CharField(
        _("Custom Unit"),
        max_length=50,
        blank=True,
        null=True,
        help_text=_("For example: gram")
    )
    custom_value = models.CharField(
        _("Custom Value"),
        max_length=100,
        blank=True,
        null=True,
        help_text=_("For example: 500")
    )

    def clean(self):
        if self.custom_name:
            self.custom_name = self.custom_name.lower().replace(' ', '')
        if self.custom_unit:
            self.custom_unit = self.custom_unit.lower().replace(' ', '')
        if self.custom_value:
            self.custom_value = self.custom_value.lower().replace(' ', '')

        if self.predefined_name == 'other':
            if not self.custom_name or not self.custom_unit or not self.custom_value:
                raise ValidationError(_('Custom fields must be filled when "Other" is selected.'))
            self.predefined_unit = None
        else:
            self.custom_name = None
            self.custom_unit = None
            # self.custom_value = None

        super().clean()

    class Meta:
        verbose_name = _("Product Specification")
        verbose_name_plural = _("Product Specifications")
    
    def __str__(self):
        if self.predefined_name != 'other':
            return _('%(product_title)s - %(spec_name)s (%(spec_unit)s)') % {
                'product_title': self.product.title,
                'spec_name': dict(self.PREDEFINED_NAME_CHOICES).get(self.predefined_name, self.predefined_name),
                'spec_unit': dict(self.WEIGHT_UNIT_CHOICES).get(self.predefined_unit, self.predefined_unit)
            }
        return _('%(product_title)s - %(custom_name)s (%(custom_unit)s)') % {
            'product_title': self.product.title,
            'custom_name': self.custom_name,
            'custom_unit': self.custom_unit
        }


class ProductRecommendation(models.Model):
    """
    'Through' model for product recommendations
    """

    primary = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="primary_recommendations",
        verbose_name=_("Primary product"),
    )
    recommendation = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name=_("Recommended product"),
    )
    ranking = models.PositiveSmallIntegerField(
        _("Ranking"),
        default=0,
        db_index=True,
        help_text=_(
            "Determines order of the products. A product with a higher"
            " value will appear before one with a lower ranking."
        ),
    )

    class Meta:
        ordering = ["primary", "-ranking"]
        unique_together = ("primary", "recommendation")
        verbose_name = _("Product recommendation")
        verbose_name_plural = _("Product recomendations")

    def __str__(self):
        return _('%(primary_title)s recommended %(recommendation_title)s') % {
            'primary_title': self.primary.title,
            'recommendation_title': self.recommendation.title
        }

class Review(models.Model):
    ''' Field : user_id, product_id, rating, review '''
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("User"))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_("Product"))
    rating = models.IntegerField(verbose_name=_("Rating"), null=True, blank=True)
    review = models.TextField(max_length=250, verbose_name=_("Review"), null=True, blank=True)
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        blank=True, null=True, 
        related_name='reply', 
        verbose_name=_("Parent Review")
    )
    verified = models.BooleanField(default=False, verbose_name=_("Verified"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    def __str__(self):
        return _('%(user_email)s reviewed %(product_title)s') % {
            'user_email': self.user.email,
            'product_title': self.product.title
        }

    @property
    def children(self):
        return Review.objects.filter(parent=self).reverse()

    @property
    def is_parent(self):
        return self.parent is None

    class Meta:
        verbose_name = _("Review")
        verbose_name_plural = _("Reviews")