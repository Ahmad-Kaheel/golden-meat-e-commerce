from modeltranslation.translator import translator, TranslationOptions
from catalogue.models import (
    Category, 
    Product, 
    ProductSpecification, 
    Review, 
    Country
)

class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

translator.register(Category, CategoryTranslationOptions)

class ProductTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

translator.register(Product, ProductTranslationOptions)

class ProductSpecificationTranslationOptions(TranslationOptions):
    fields = ('predefined_name', 'predefined_unit', 'custom_name', 'custom_unit')

translator.register(ProductSpecification, ProductSpecificationTranslationOptions)

class ReviewTranslationOptions(TranslationOptions):
    fields = ('review',)

translator.register(Review, ReviewTranslationOptions)

class CountryTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(Country, CountryTranslationOptions)
