from haystack import indexes
from catalogue.models import Product, Category


class ProductIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')
    title_ar = indexes.CharField(model_attr='title_ar')
    title_en = indexes.CharField(model_attr='title_en')
    description = indexes.CharField(model_attr='description')
    description_ar = indexes.CharField(model_attr='description_ar')
    description_en = indexes.CharField(model_attr='description_en')
    is_wholesale = indexes.BooleanField(model_attr='is_wholesale')

    def get_model(self):
        return Product

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(is_public=True)
    



class CategoryIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    name_ar = indexes.CharField(model_attr='name_ar')
    name_en = indexes.CharField(model_attr='name_en')
    description = indexes.CharField(model_attr='description')
    description_ar = indexes.CharField(model_attr='description_ar')
    description_en = indexes.CharField(model_attr='description_en')
    is_wholesale = indexes.BooleanField(model_attr='is_wholesale')

    def get_model(self):
        return Category

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(is_public=True)
