from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import DO_NOTHING
from django.db.models.fields import CharField
from customer.models import Customer

# Create your models here.


# gender_choices = (('M','Male'),('F','Female'),)

# class RestaurantOwner(models.Model):
#     name = models.CharField(max_length=30)
#     email = models.EmailField()
#     mobile = PhoneField()
#     profile_picture = models.ImageField(upload_to='images/restaurant')
#     address = models.TextField()
#     gender = models.CharField(max_length=1,choices=gender_choices,default='M')
#     created_date = models.DateTimeField(auto_now_add=True,editable=False)
#     updated_date = models.DateTimeField(auto_now=True, editable=True)

# class RestaurantList(models.Model):
#     profile_picture = models.ImageField(upload_to='images/restaurant')
#     name = models.CharField(max_length=30)
#     address = models.TextField()
#     owner_name = models.CharField(max_length=30)
#     contact_person = models.CharField(max_length=30)
#     mobile = PhoneField(blank=True, help_text='Contact phone number')
#     email = models.CharField(max_length=30,null=True)
#     opening_time = models.TimeField(null=True)
#     closing_time = models.TimeField(null=True)
#     rating = models.IntegerField(null=True)
#     active = models.BooleanField(default=False)
#     disable = models.BooleanField(default=False)
#     created_date = models.DateTimeField(auto_now_add=True,editable=False)
#     updated_date = models.DateTimeField(auto_now=True,editable=True)
#     category = models.CharField(max_length=30, default=None, null=True)
#     city= models.CharField(max_length=15, default=None, null=True)
    

# class MenuItems(models.Model):
#     name = models.CharField(max_length=30)
#     category = models.CharField(max_length=50)
#     price = models.IntegerField()
#     description = models.TextField()
#     picture = models.ImageField(upload_to='images/restaurant')
#     prep_time = models.IntegerField()
#     is_veg = models.BooleanField()
#     created_date = models.DateTimeField(auto_now_add=True,editable=False)
#     updated_date = models.DateTimeField(auto_now=True, editable=True)
#     is_available = models.BooleanField()
#     restaurant = models.ForeignKey(RestaurantList, on_delete=models.DO_NOTHING)

# class Order(models.Model):
#     created_date = models.DateTimeField(auto_now_add=True,editable=False)
#     updated_date = models.DateTimeField(auto_now=True, editable=True)
#     rest_id= models.ForeignKey(RestaurantList, on_delete=models.DO_NOTHING)
#     customer_id = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
#     total_amount = models.IntegerField()
#     list_of_items= models.TextField(default=None,null=True)
#     status = models.TextField(default='New')





# class NewRestaurantOwner(models.Model):
#     name = models.CharField(max_length=30)
#     email = models.EmailField()
#     mobile = models.CharField(max_length=10)
#     profile_picture = models.ImageField(upload_to='images/restaurant')
#     address = models.TextField()

class NewRestaurant(models.Model):
    profile_picture = models.ImageField(upload_to='images/restaurant')
    name = models.CharField(max_length=30)
    address = models.TextField()
    owner= models.ForeignKey(User, on_delete=models.DO_NOTHING)
    contact_person = models.CharField(max_length=30)
    mobile = CharField(max_length=10,unique=True)
    email = models.CharField(max_length=30,null=True)
    opening_time = models.TimeField(null=True)
    closing_time = models.TimeField(null=True)
    rating = models.IntegerField(null=True)
    active = models.BooleanField(default=False)
    disable = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True,editable=False)
    updated_date = models.DateTimeField(auto_now=True,editable=True)
    category = models.CharField(max_length=30, default=None, null=True)
    city= models.CharField(max_length=15, default=None, null=True)


class NewMenuItems(models.Model):
    name = models.CharField(max_length=30)
    category = models.CharField(max_length=50)
    price = models.IntegerField()
    description = models.TextField()
    picture = models.ImageField(upload_to='images/restaurant')
    prep_time = models.IntegerField()
    is_veg = models.BooleanField()
    created_date = models.DateTimeField(auto_now_add=True,editable=False)
    updated_date = models.DateTimeField(auto_now=True, editable=True)
    is_available = models.BooleanField()
    restaurant = models.ForeignKey(NewRestaurant, on_delete=models.DO_NOTHING)