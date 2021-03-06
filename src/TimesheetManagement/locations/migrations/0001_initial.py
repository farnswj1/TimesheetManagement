# Generated by Django 3.1.7 on 2021-03-12 21:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, validators=[django.core.validators.RegexValidator(message='Please insert a valid location name.', regex='^[a-zA-Z0-9,\\. :-]+$')])),
                ('sector', models.CharField(choices=[('E', 'East'), ('W', 'West')], max_length=1, validators=[django.core.validators.RegexValidator(message='Please insert either E (East) or W (West).', regex='^[EW]$')])),
            ],
        ),
    ]
