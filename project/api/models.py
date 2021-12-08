from django.db import models
from phone_field import PhoneField

# Create your models here.
class RestaurantList(models.Model):
    profile_picture = models.ImageField()
    name = models.CharField(max_length=30)
    address = models.TextField()
    owner_name = models.CharField(max_length=30)
    contact_person = models.CharField(max_length=30)
    mobile = PhoneField(blank=True, help_text='Contact phone number')
    email = models.EmailField(null=True)
    opening_time = models.TimeField(null=True)
    closing_time = models.TimeField(null=True)
    rating = models.IntegerField(null=True)
    active = models.BooleanField(default=False)
    disable = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True,editable=False)
    updated_date = models.DateTimeField(auto_now=True,editable=True)


gender_choices = (('M','Male'),('F','Female'),)
class Customer(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    profile_picture = models.ImageField()
    dob = models.DateTimeField()
    mobile = PhoneField()
    address = models.TextField()
    gender = models.CharField(max_length=1,choices=gender_choices,default='M')
    nationality = models.CharField(max_length=20)
    created_date = models.DateTimeField(auto_now_add=True,editable=False)
    updated_date = models.DateTimeField(auto_now=True, editable=True)


class RestaurantOwner(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    mobile = PhoneField()
    profile_picture = models.ImageField()
    address = models.TextField()
    gender = models.CharField(max_length=1,choices=gender_choices,default='M')
    created_date = models.DateTimeField(auto_now_add=True,editable=False)
    updated_date = models.DateTimeField(auto_now=True, editable=True)