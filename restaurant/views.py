from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from models import RestaurantList, MenuItems, Order, RestaurantOwner
from serializers import RestDetailSerializer, PartnerSerializer, MenuItemsSerializer, OrderSerializer, OrderSerializer_create
import sys
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import SlidingToken,AccessToken

# Create your views here.
class RestaurantDetailView(ModelViewSet):
    queryset = RestaurantList.objects.all()

    serializer_class = RestDetailSerializer
    def create(self,request):
        try:
            data= request.data
            serializer = RestDetailSerializer(data= data)
            serializer.is_valid(raise_exception= True)
            serializer.save()
            data= {
                    'status': True,
                    'data': serializer.data,
                    'error':None
                    }
            return Response(data)
        except Exception as e:
            exception_type, exception_object, exception_traceback = sys.exc_info()
            filename = exception_traceback.tb_frame.f_code.co_filename
            line_number = exception_traceback.tb_lineno
            data= {
                'status': False,
                'data': [],
                'error': str(e)
            }
            print(filename,line_number)
            return Response(data)

    def list(self,request):
        try:
            data = RestaurantList.objects.all()
            data_serializer = RestDetailSerializer(data, many = True)
            data ={
                    'status':True,
                    'data': data_serializer.data,
                    'error':None
                    }
            return Response(data)
        except Exception as e:
            return Response(str(e))

class PartnerView(ModelViewSet):
    queryset = RestaurantOwner.objects.all()
    serializer_class = PartnerSerializer
    def create(self,request):
        try:
            data = request.data
            user = User.objects.create_user(username=str(data.get('mobile')),password='password')
            user.save()
            return Response({'status':'user created'})
        except Exception as e:
            return Response(str(e))

    @action(detail=False, methods=['POST'])
    def signup(self,request):
        phone = request.data.get('mobile')
        user = User.objects.get(username= str(phone))
        return Response(str(AccessToken.for_user(user)))

class MenuItemsView(ModelViewSet):
    queryset = MenuItems.objects.all()
    serializer_class = MenuItemsSerializer
    def list(self, request, *args, **kwargs):
        try:
            data = request.GET.get('restaurant')
            queryset =MenuItems.objects.filter(restaurant=data)
            serializer = MenuItemsSerializer(queryset,many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(str(e))
        
    

class OrderView(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

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