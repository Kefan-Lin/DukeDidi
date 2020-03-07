from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.postgres.fields import ArrayField


# Create your models here.


class User(models.Model):
    is_logged_in = models.BooleanField(default=False)
    is_driver = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)
    is_sharer = models.BooleanField(default=False)
    #candidate_sharable_rides = ArrayField(models.CharField(max_length=100,default='',null=True),null=True,default=None)
    sharer_party_size = models.IntegerField(default=0)  # Just store the latest sharer party size
    encrypted_password = models.CharField(max_length=254, default="", null=True)
    salt = models.CharField(max_length=254,default="",null=True)
    # rides_arr = models.TextField(default="", null=True)      # history rides
    vehicle_capacity = models.IntegerField(default=0, validators=[
        MaxValueValidator(8), MinValueValidator(0)])
    license_plate_number = models.CharField(max_length=100, default="", null=True)
    email = models.EmailField(max_length=100)


class Ride(models.Model):
    owner = models.CharField(max_length=100, default="", null=True)
    driver = models.CharField(max_length=100, default="", null=True)
    license_plate_number = models.CharField(max_length=100, default="", null=True)
    sharers = ArrayField(models.EmailField(max_length=100,blank=True,null=True),default=list)
    sharer_partysize_pair = models.TextField(blank=True,null=True)
    is_sharable = models.BooleanField(default=False)
    remaining_size = models.IntegerField(default=0, validators=[
        MaxValueValidator(8), MinValueValidator(0)])
    is_confirmed = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    arrival_time = models.DateTimeField(null=True)
    destination = models.CharField(default='', max_length=100)
    total_size = models.IntegerField(default=8)


