from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product

@receiver(post_save, sender=Product)
def update_is_public_if_quantity_zero(sender, instance, **kwargs):
    if not kwargs.get('created', False):
        if instance.quantity <= 0 and instance.is_public:
            instance.is_public = False
            instance.save(update_fields=['is_public'])
