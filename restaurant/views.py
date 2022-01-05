
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import ModelViewSet
# from .models import NewRestaurant, RestaurantList, MenuItems, Order, RestaurantOwner
import sys
from django.contrib.auth.models import User
from .models import NewMenuItems, NewRestaurant, Order
from .serializers import NewMenuItemsSerializer, NewRestaurantSerializer, OrderSerializer, OrderSerializer_create
from rest_framework.decorators import action
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import SlidingToken,AccessToken
from rest_framework.permissions import IsAuthenticated


class NewRestaurantViewSet(ModelViewSet):
    queryset=NewRestaurant.objects.all()
    serializer_class= NewRestaurantSerializer
    # permission_classes = [IsAuthenticated]

    def create(self,request):
        try:
            rawData = request.data
            user=User.objects.create(username=rawData['mobile'],password='password')
            user.save()
            rawData['owner']=user.id
            serializer = NewRestaurantSerializer(data=rawData)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            data = {'status': True,
                    'data': serializer.data,
                    'error':None
            }
            return Response(data)
        except Exception as e:
            return Response(str(e))
    

    @action(detail=False,methods=['GET'])
    def login(self,request):
        mobile= request.GET.get('username')
        try:
            if request.GET.get('password')!='password':
                return Response('Invalid password')
            user = User.objects.get(username=int(mobile))
            data= NewRestaurant.objects.get(owner=user.id)
            serializer= NewRestaurantSerializer(data)
            token= AccessToken.for_user(user)
            data= {
                'status': True,
                'restaurant_data':serializer.data,
                'token': str(token),
                'error': False
            }
            return Response(data)
        except Exception as e:
            data={'status':False,
            'data':'Account does not exist',
            'error':str(e)}
            return Response(data)

    @action (detail=False,methods=['GET'], permission_classes=[])
    def restaurants(self,request):
        data = NewRestaurant.objects.values_list('id','name','profile_picture')
        data={
                'status': True,
                'data' : data
            }
        return Response(data)

    @action (detail=False, methods=['GET'], permission_classes=[])
    def location_search(self,request):
        try:
            search_query= request.GET.get('location')
            queryset = NewRestaurant.objects.filter(city__contains=search_query)
            serializer= NewRestaurantSerializer(queryset, many=True)
            data={
                    'status':True,
                    'data': serializer.data,
                    'error': None
                    }
            return Response(data)
        except Exception as e:
            return Response(str(e))
    
    @action (detail=False, methods=['GET'], permission_classes=[])
    def name_search(self,request):
        try:
            search_query = request.GET.get("name")
            queryset = NewRestaurant.objects.filter(name__contains=search_query)
            serializer = NewRestaurantSerializer(queryset, many = True)
            data = {
                'status':True,
                'data': serializer.data,
                'error': None
            }
            return Response(data)
        except Exception as e:
            return Response(str(e))


class MenuItemsView(ModelViewSet):
    queryset = NewMenuItems.objects.all()
    serializer_class = NewMenuItemsSerializer
    # permission_classes = [IsAuthenticated]
    def list(self, request, *args, **kwargs):
        try:
            data = request.GET.get('restaurant')
            queryset =NewMenuItems.objects.filter(restaurant=data)
            serializer = NewMenuItemsSerializer(queryset,many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(str(e))

class OrderView(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    def create(self,request):
        try:
            rawData = request.data
            serializer = OrderSerializer_create(data=rawData)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            data = {'status': True,
                    'data': serializer.data,
                    'error':None
            }
            return Response(data)
        except Exception as e:
            return Response(str(e))
    
    def list(self,request):
        try:
            data = request.GET.get('status')
            queryset = Order.objects.filter(status=data)
            serializer = OrderSerializer(queryset,many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(str(e))

    def patch(self,request, *args, **kwargs):
        try:
            instance = self.get_object()
            data = request.data
            serializer = OrderSerializer(instance, data, partial = True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except Exception as e:
            return Response(str(e))

    @action (detail= False, methods=['GET'])
    def status(self,request):
        status= request.GET.get('status')
        if status == 'previous':
            queryset = Order.objects.filter(status='Delivered')
        else:
            queryset = Order.objects.exclude(status ='Delivered')
        serializer = OrderSerializer(queryset,many=True)
        return Response(serializer.data)    

    @action(detail=False,methods=['GET'])
    def order_history(self,request):
        id= request.GET.get('id')
        data= Order.objects.filter(rest_id=id)
        serializer = OrderSerializer(data, many=True)
        data={
            'status':True,
            'data': serializer.data,
            'error':False
        }
        return Response(data)

