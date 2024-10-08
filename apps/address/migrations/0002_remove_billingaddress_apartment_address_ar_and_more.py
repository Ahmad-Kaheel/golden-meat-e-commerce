# Generated by Django 4.2 on 2024-08-21 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='billingaddress',
            name='apartment_address_ar',
        ),
        migrations.RemoveField(
            model_name='billingaddress',
            name='apartment_address_en',
        ),
        migrations.RemoveField(
            model_name='billingaddress',
            name='city_ar',
        ),
        migrations.RemoveField(
            model_name='billingaddress',
            name='city_en',
        ),
        migrations.RemoveField(
            model_name='billingaddress',
            name='street_address_ar',
        ),
        migrations.RemoveField(
            model_name='billingaddress',
            name='street_address_en',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='apartment_address_ar',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='apartment_address_en',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='city_ar',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='city_en',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='street_address_ar',
        ),
        migrations.RemoveField(
            model_name='shippingaddress',
            name='street_address_en',
        ),
        migrations.AlterField(
            model_name='billingaddress',
            name='apartment_address',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Apartment Address'),
        ),
        migrations.AlterField(
            model_name='billingaddress',
            name='city',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='City'),
        ),
        migrations.AlterField(
            model_name='billingaddress',
            name='postal_code',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Postal Code'),
        ),
        migrations.AlterField(
            model_name='billingaddress',
            name='street_address',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Street Address'),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='apartment_address',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Apartment Address'),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='city',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='City'),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='postal_code',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Postal Code'),
        ),
        migrations.AlterField(
            model_name='shippingaddress',
            name='street_address',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Street Address'),
        ),
        migrations.AlterField(
            model_name='shopaddress',
            name='apartment_address',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Apartment Address'),
        ),
        migrations.AlterField(
            model_name='shopaddress',
            name='city',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='City'),
        ),
        migrations.AlterField(
            model_name='shopaddress',
            name='postal_code',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Postal Code'),
        ),
        migrations.AlterField(
            model_name='shopaddress',
            name='street_address',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Street Address'),
        ),
    ]
