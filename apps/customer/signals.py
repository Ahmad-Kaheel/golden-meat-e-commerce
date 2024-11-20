from django.db.models.signals import post_save
from django.dispatch import receiver
from customer.models import Profile
from django.contrib.auth import get_user_model
from allauth.account.models import EmailAddress

User = get_user_model()

# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     if created and not Profile.objects.filter(user=instance).exists():
#         Profile.objects.create(user=instance)


# @receiver(post_save, sender=User)
# def save_profile(sender, instance, **kwargs):
#     instance.profile.save()



@receiver(post_save, sender=EmailAddress)
def disable_vendor_account_after_email_verification(sender, instance, created, **kwargs):
    if instance.verified and instance.user.is_vendor:
        user = instance.user
        user.is_active = False
        user.save()