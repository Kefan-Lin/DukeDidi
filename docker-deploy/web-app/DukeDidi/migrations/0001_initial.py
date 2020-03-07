# Generated by Django 3.0.2 on 2020-01-28 03:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_logged_in', models.BooleanField(default=False)),
                ('is_driver', models.BooleanField(default=False)),
                ('is_owner', models.BooleanField(default=False)),
                ('is_sharer', models.BooleanField(default=False)),
                ('account', models.CharField(max_length=100)),
                ('encrypted_password', models.CharField(max_length=100)),
                ('vehicle_capacity', models.IntegerField(default=0)),
                ('license_plate_number', models.CharField(default='', max_length=100)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Ride',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_sharable', models.BooleanField(default=False)),
                ('remaining_size', models.IntegerField(default=0)),
                ('is_confirmed', models.BooleanField(default=False)),
                ('is_conpleted', models.BooleanField(default=False)),
                ('arrive_time', models.DateTimeField()),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ride_owners_set', to='DukeDidi.User')),
                ('sharers', models.ManyToManyField(blank=True, null=True, related_name='ride_sharers_set', to='DukeDidi.User')),
            ],
        ),
    ]
