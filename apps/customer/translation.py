from modeltranslation.translator import translator, TranslationOptions

from customer.models import Profile


class ProfileTranslationOptions(TranslationOptions):
    fields = (
        'first_name', 'last_name', 'gender', 
        'date_of_birth', 'company_name', 'company_type', 
        'commercial_registration_number', 'tax_number', 
        'manager_name', 'company_email', 
        'mobile_number', 'website', 'business_activity'
    )

translator.register(Profile, ProfileTranslationOptions)