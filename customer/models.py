from django.db import models
# from phone_field import PhoneField

# Create your models here.
gender_choices = (('M','Male'),('F','Female'),)
class Customer(models.Model):
    name = models.CharField(max_length=30,null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    profile_picture = models.ImageField(upload_to='images/customer',null=True,blank=True)
    dob = models.DateField(null=True, blank=True)
    mobile = models.CharField(max_length=10,unique=True)
    address = models.TextField(null=True, blank=True)
    gender = models.CharField(max_length=1,choices=gender_choices,default='M')
    nationality = models.CharField(max_length=20,null=True,blank=True)
    created_date = models.DateTimeField(auto_now_add=True,editable=False)
    updated_date = models.DateTimeField(auto_now=True, editable=True)
    description = models.TextField(default=None,null=True)