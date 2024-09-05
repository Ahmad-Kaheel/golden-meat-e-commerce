from modeltranslation.translator import translator, TranslationOptions
from order.models import Order

class OrderTranslationOptions(TranslationOptions):
    fields = ('comment',)

translator.register(Order, OrderTranslationOptions)