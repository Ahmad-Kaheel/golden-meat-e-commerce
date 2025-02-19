# Generated by Django 4.2 on 2024-10-27 12:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0003_alter_review_review_alter_review_review_ar_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_wholesale',
            field=models.BooleanField(default=False, help_text='Indicates if this product is available for wholesale.', verbose_name='Is wholesale'),
        ),
        migrations.AddField(
            model_name='product',
            name='weight',
            field=models.DecimalField(decimal_places=2, default=1, help_text='Total weight of the product in kilograms.', max_digits=10, validators=[django.core.validators.MinValueValidator(1.0)]),
        ),
        migrations.AddField(
            model_name='product',
            name='wholesale_quantity_threshold',
            field=models.IntegerField(default=0, help_text='Minimum quantity required for wholesale.', verbose_name='Wholesale Quantity Threshold'),
        ),
        migrations.AddField(
            model_name='product',
            name='wholesale_weight_threshold',
            field=models.DecimalField(decimal_places=2, default=0.0, help_text='Minimum weight required for wholesale.', max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Wholesale Weight Threshold (kg)'),
        ),
        migrations.AlterField(
            model_name='product',
            name='discount',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(60)], verbose_name='Discount (Optional)'),
        ),
    ]
