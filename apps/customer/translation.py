from modeltranslation.translator import translator, TranslationOptions

from customer.models import Profile


class ProfileTranslationOptions(TranslationOptions):
    fields = ('first_name', 'last_name', 'bio')

translator.register(Profile, ProfileTranslationOptions)
