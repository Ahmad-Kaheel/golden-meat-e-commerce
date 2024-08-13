from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext_lazy

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
    price = models.DecimalField(decimal_places=2, max_digits=10)
    quantity = models.IntegerField(default=1)
    
    discount = models.IntegerField(default=0,
        verbose_name=_("Discount(Optional)")
    )
    
    is_public = models.BooleanField(
        _("Is public"),
        default=True,
        db_index=True,
        help_text=_("Show this product in search results and catalogue listings."),
    )
    category = models.ForeignKey(
        Category, verbose_name=_("Category"), 
        on_delete=models.SET(get_default_product_category),
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
        if self.title:
            return self.title
        else:
            return _("product without title")
    
    def get_title(self):
        """
        Return a product's title or it's parent's title if it has no title
        """
        return self.title
    
    @property
    def price_with_discount(self):
        """
        Returns calculated price with discount.
        """
        price_with_discount = get_discount(self.price, self.discount)
        return price_with_discount


class ProductImage(models.Model):
    product = models.ForeignKey(Product, verbose_name=_("Product"), on_delete=models.CASCADE, related_name='images')
    image_url = models.ImageField(_("Image URL"), upload_to=product_image_path, blank=True)
    alt_text = models.CharField(_("Missing Image"), max_length=100)

    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")


class Country(models.Model):
    name = models.CharField(_("Country Name"), max_length=100)

    class Meta:
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")
    
    def __str__(self):
        return self.name


class ProductCountry(models.Model):
    product = models.ForeignKey(Product, verbose_name=_("Product"), on_delete=models.CASCADE, related_name='countries')
    country = models.ForeignKey(Country, verbose_name=_("Country"), on_delete=models.CASCADE, related_name='products')

    class Meta:
        verbose_name = _("Product Country")
        verbose_name_plural = _("Product Countries")


class ProductSpecification(models.Model):
    product = models.ForeignKey(Product, verbose_name=_("Product"), on_delete=models.CASCADE, related_name='specifications')
    name = models.CharField(_("Specification Name"), max_length=100)
    value = models.CharField(_("Specification Value"), max_length=100)

    class Meta:
        verbose_name = _("Product Specification")
        verbose_name_plural = _("Product Specifications")


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



class Review(models.Model):
    ''' Field : user_id, product_id, rating, review '''
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("User"))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_("Product"))
    rating = models.IntegerField(verbose_name=_("Rating"), null=True, blank=True)
    review = models.TextField(max_length=250, verbose_name=_("Review"))
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
        return self.user.email

    @property
    def children(self):
        return Review.objects.filter(parent=self).reverse()

    @property
    def is_parent(self):
        return self.parent is None

    class Meta:
        verbose_name = _("Review")
        verbose_name_plural = _("Reviews")