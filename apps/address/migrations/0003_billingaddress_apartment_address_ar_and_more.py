# Generated by Django 4.2 on 2024-08-21 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0002_remove_billingaddress_apartment_address_ar_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='billingaddress',
            name='apartment_address_ar',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Apartment Address'),
        ),
        migrations.AddField(
            model_name='billingaddress',
            name='apartment_address_en',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Apartment Address'),
        ),
        migrations.AddField(
            model_name='billingaddress',
            name='city_ar',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='City'),
        ),
        migrations.AddField(
            model_name='billingaddress',
            name='city_en',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='City'),
        ),
        migrations.AddField(
            model_name='billingaddress',
            name='street_address_ar',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Street Address'),
        ),
        migrations.AddField(
            model_name='billingaddress',
            name='street_address_en',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Street Address'),
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='apartment_address_ar',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Apartment Address'),
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='apartment_address_en',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Apartment Address'),
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='city_ar',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='City'),
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='city_en',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='City'),
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='street_address_ar',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Street Address'),
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='street_address_en',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Street Address'),
        ),
    ]