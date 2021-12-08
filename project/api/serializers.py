from rest_framework import fields, serializers
from .models import RestaurantList, Customer, RestaurantOwner


class RestDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model= RestaurantList
        fields = ['id','profile_picture','name','address','owner_name','contact_person','mobile','email',
                    'opening_time','closing_time','rating','active','disable','created_date','updated_date']

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantOwner
        fields = '__all__'

