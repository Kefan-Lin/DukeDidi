# Generated by Django 3.0.2 on 2020-01-29 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DukeDidi', '0002_auto_20200128_0307'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ride',
            old_name='is_conpleted',
            new_name='is_completed',
        ),
        migrations.AddField(
            model_name='user',
            name='rides_arr',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='ride',
            name='owner',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.RemoveField(
            model_name='ride',
            name='sharers',
        ),
        migrations.AddField(
            model_name='ride',
            name='sharers',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='user',
            name='account',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='encrypted_password',
            field=models.CharField(default='', max_length=100),
        ),
    ]
