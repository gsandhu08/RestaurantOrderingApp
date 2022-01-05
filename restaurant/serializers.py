from rest_framework import serializers
# from .models import RestaurantList, RestaurantOwner, Order, MenuItems
from .models import NewMenuItems, NewRestaurant, Order


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
                items = NewMenuItems.objects.get(id=i)
                items_serializer = NewMenuItemsSerializer(items)
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



class NewRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewRestaurant
        fields = '__all__'


class NewMenuItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewMenuItems
        fields = '__all__'