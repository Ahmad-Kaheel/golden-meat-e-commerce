# Generated by Django 4.2 on 2024-11-25 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0007_alter_category_is_wholesale'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='is_wholesale',
            field=models.BooleanField(default=False, help_text='Indicates if this product is available for B2B.', verbose_name='B2B'),
        ),
    ]