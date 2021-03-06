# Generated by Django 3.0.2 on 2020-01-29 01:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DukeDidi', '0003_auto_20200129_0058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ride',
            name='owner',
            field=models.CharField(default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='ride',
            name='remaining_size',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(7), django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='ride',
            name='sharers',
            field=models.TextField(default='', null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='account',
            field=models.CharField(default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='encrypted_password',
            field=models.CharField(default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='license_plate_number',
            field=models.CharField(default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='rides_arr',
            field=models.TextField(default='', null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='vehicle_capacity',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(8), django.core.validators.MinValueValidator(0)]),
        ),
    ]
