# Generated by Django 3.1.7 on 2021-03-12 14:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='zip_code',
            field=models.CharField(max_length=10, validators=[django.core.validators.RegexValidator(message='Please enter a valid ZIP code.', regex='^\\d{5}(-\\d{4})?$')]),
        ),
    ]
