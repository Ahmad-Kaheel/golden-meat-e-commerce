# Generated by Django 4.0.4 on 2024-08-11 09:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=100, verbose_name='City')),
                ('street_address', models.CharField(max_length=100, verbose_name='Street')),
                ('apartment_address', models.CharField(max_length=100, verbose_name='Apartment Address')),
                ('postal_code', models.CharField(blank=True, max_length=20, verbose_name='Postal Code')),
                ('is_default_for_billing', models.BooleanField(default=False, verbose_name='Default billing address?')),
                ('is_default_for_shipping', models.BooleanField(default=False, verbose_name='Default shipping address?')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, help_text='In case we need to call you about your order', max_length=128, region=None, verbose_name='Phone number')),
                ('notes', models.TextField(blank=True, help_text='Tell us anything we should know when delivering your order.', verbose_name='Instructions')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('search_text', models.TextField(editable=False, verbose_name='Search text - used only for searching addresses')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'User Address',
                'verbose_name_plural': 'User Addresses',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='ShopAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=100, verbose_name='City')),
                ('street_address', models.CharField(max_length=100, verbose_name='Street')),
                ('apartment_address', models.CharField(max_length=100, verbose_name='Apartment Address')),
                ('postal_code', models.CharField(blank=True, max_length=20, verbose_name='Postal Code')),
                ('shop_name', models.CharField(max_length=255, verbose_name='Shop Name')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shop_addresses', to=settings.AUTH_USER_MODEL, verbose_name='Owner')),
            ],
            options={
                'verbose_name': 'Shop Address',
                'verbose_name_plural': 'Shop Addresses',
                'ordering': ('-created_at',),
            },
        ),
    ]