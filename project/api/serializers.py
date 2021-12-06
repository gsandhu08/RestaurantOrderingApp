from rest_framework import serializers
from .models import RestaurantList


class RestDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model= RestaurantList
        fields = ['id','profile_picture','name','address','owner_name','contact_person','mobile','email',
                    'opening_time','closing_time','rating','active','disable','created_date','updated_date']