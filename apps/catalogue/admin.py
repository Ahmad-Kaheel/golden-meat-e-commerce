from django.utils.translation import gettext_lazy as _
from django import forms
from django.contrib import admin
from catalogue.models import (
    Category,
    Product,
    ProductImage,
    ProductSpecification,
    ProductRecommendation,
    Country,
    Review
)

class ReviewForm(forms.ModelForm):
    review = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 2, 'cols': 20})
    )

    class Meta:
        model = Review
        fields = '__all__'


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductSpecificationForm(forms.ModelForm):
    custom_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'size': 20,
            'placeholder': 'Enter custom name...',
        })
    )
    custom_unit = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'size': 10,
            'placeholder': 'Enter custom unit...',
        })
    )
    custom_value = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'size': 10,
            'placeholder': 'Enter value...',
        })
    )

    class Media:
        js = (
            'admin/js/vendor/jquery/jquery.js',
            'admin/js/specification_dynamic_fields.js',
        )
        model = ProductSpecification
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()

        predefined_name = cleaned_data.get('predefined_name')
        custom_name = cleaned_data.get('custom_name')
        predefined_unit = cleaned_data.get('predefined_unit')
        custom_unit = cleaned_data.get('custom_unit')

        if predefined_name == 'other' and not custom_name:
            self.add_error('custom_name', _('Please provide a custom name when "Other" is selected.'))

        if predefined_unit == 'other' and not custom_unit:
            self.add_error('custom_unit', _('Please provide a custom unit when "Other" is selected.'))

        return cleaned_data

class ProductSpecificationInline(admin.StackedInline):
    model = ProductSpecification
    form = ProductSpecificationForm
    extra = 1

    fieldsets = (
        (None, {
            'fields': ('predefined_name', 'predefined_unit', 'custom_name', 'custom_unit', 'custom_value'),
        }),
        ('Arabic Translation', {
            'fields': ('predefined_name_ar', 'predefined_unit_ar', 'custom_name_ar', 'custom_unit_ar'),
        }),
        ('English Translation', {
            'fields': ('predefined_name_en', 'predefined_unit_en', 'custom_name_en', 'custom_unit_en'),
        }),
    )


class ProductRecommendationInline(admin.TabularInline):
    model = ProductRecommendation
    fk_name = 'primary'
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('get_translatable_str', 'get_product_country', 'category_display', 'price', 'is_public')
    search_fields = ('is_public', 'categories__name')
    list_filter = ('is_public', 'categories', 'source_country', 'date_updated')
    inlines = [
        ProductImageInline,
        ProductSpecificationInline,
        ProductRecommendationInline
    ]

    def category_display(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])
    category_display.short_description = 'Categories'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'is_public')
    search_fields = ('name',)
    list_filter = ('is_public',)

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(ProductRecommendation)
class ProductRecommendationAdmin(admin.ModelAdmin):
    list_display = ('primary', 'recommendation', 'ranking')
    search_fields = ('primary', 'recommendation', 'ranking')
    list_filter = ('primary', 'ranking')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'product_title', 'rating', 'review')
    search_fields = ('product__title', 'rating', 'review')
    list_filter = ('product__title', 'rating', 'review')

    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User Email'

    def product_title(self, obj):
        return obj.product.title
    product_title.short_description = 'Product Title'