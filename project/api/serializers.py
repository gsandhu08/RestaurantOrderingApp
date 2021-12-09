from rest_framework import fields, serializers
from .models import MenuItems, Order, RestaurantList, Customer, RestaurantOwner


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


class MenuItemsSerializer(serializers.ModelSerializer):
    restname = serializers.SerializerMethodField()
    def get_restname(self,instance):
        return instance.restaurant.name
    # restaurant = RestDetailSerializer()
    
    class Meta:
        model = MenuItems
        fields = '__all__'
        extra_fields = ['restname']

class OrderSerializer(serializers.ModelSerializer):
    list_of_items = serializers.SerializerMethodField(read_only=True)
    def get_list_of_items(self,obj):
        items_list=[]
        list = obj.list_of_items
        if obj.list_of_items:
            list= list.split(',')
        else:
            return []
        for i in list:
            try:
                items = MenuItems.objects.get(id=i)
                items_serializer = MenuItemsSerializer(items)
                items_list.append(items_serializer.data.get('name'))
            except Exception as e:
                print(str(e))
        return items_list
    class Meta:
        model = Order
        fields ='__all__'
class OrderSerializer_create(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'