# Generated by Django 4.2 on 2024-11-25 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0006_country_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='is_wholesale',
            field=models.BooleanField(default=False, help_text='Indicates if this category is available for B2B.', verbose_name='B2B'),
        ),
    ]