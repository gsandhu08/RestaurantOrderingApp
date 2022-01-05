
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import ModelViewSet
from .models import RestaurantList, MenuItems, Order, RestaurantOwner
from .serializers import RestDetailSerializer, PartnerSerializer, MenuItemsSerializer, OrderSerializer, OrderSerializer_create
import sys
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import SlidingToken,AccessToken
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class RestaurantDetailView(ModelViewSet):
    queryset = RestaurantList.objects.all()
    permission_classes = [IsAuthenticated]
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

    @action (detail=False,methods=['GET'], permission_classes=[])
    def restaurants(self,request):
        data = RestaurantList.objects.values_list('id','name','profile_picture')
        # data_serializer = RestDetailSerializer(data, many=True)
        data={
                'status': True,
                'data' : data
            }
        return Response(data)
    

# location search
    @action (detail=False, methods=['GET'], permission_classes=[])
    def location_search(self,request):
        try:
            search_query= request.GET.get('location')
            queryset = RestaurantList.objects.filter(city__contains=search_query)
            serializer= RestDetailSerializer(queryset, many=True)
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
            queryset = RestaurantList.objects.filter(name__contains=search_query)
            serializer = RestDetailSerializer(queryset, many = True)
            data = {
                'status':True,
                'data': serializer.data,
                'error': None
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
            users= {1:{'username':'9876501234','password':'password'},
                    2:{'username':'9887766550','password':'password'},
                    3:{'username':'9876655443','password':'password'},
                    4:{'username':'9876543201','password':'password'},
                    5:{'username':'9080706050','password':'password'},
                    6:{'username':'9181716151','password':'password'},
                    7:{'username':'9282726252','password':'password'},
                    8:{'username':'9383736353','password':'password'},
                    9:{'username':'9484746454','password':'password'},
                    10:{'username':'9585756555','password':'password'},
                    11:{'username':'9686766656','password':'password'}
            }
            for i in [1,2,3,4,5,6,7,8,9,10,11]:
                if data.get('mobile')==users[i]['username']:
                    user= User.objects.create_user(username=users[i]['username'],password=users[i]['password'])
                    user.save()
                    print('user saved')
                    serializer = PartnerSerializer(data= data)
                    serializer.is_valid(raise_exception= True)
                    serializer.save()
                    print('serializer saved')
            # user = User.objects.create_user(username=str(data.get('mobile')),password='password')
            # user.save()
            return Response({'status':'user created'})
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
            return Response('this is an exception'+str(e))
    # def list(self,request):
    #     data= User.objects.all()
    #     serializer = Serializer(data, many=True)
    #     return Response(serializer.data)

    @action(detail=False, methods=['POST'])
    def signup(self,request):
        users= {1:{'username':'9876501234','password':'password'},
                    2:{'username':'9887766550','password':'password'},
                    3:{'username':'9876655443','password':'password'},
                    4:{'username':'9876543201','password':'password'},
                    5:{'username':'9080706050','password':'password'},
                    6:{'username':'9181716151','password':'password'},
                    7:{'username':'9282726252','password':'password'},
                    8:{'username':'9383736353','password':'password'},
                    9:{'username':'9484746454','password':'password'},
                    10:{'username':'9585756555','password':'password'},
                    11:{'username':'9686766656','password':'password'}
            }
        phone = request.data.get('mobile')
        password= request.data.get('password')
        for i in [1,2,3,4,5,6,7,8,9,10,11]:
            if phone==users[i]['username'] and password==users[i]['password']:
                user = User.objects.get(username= phone)
                data= RestaurantOwner.objects.get(mobile=phone)
                serializer= PartnerSerializer(data)
                token= AccessToken.for_user(user)
                email= serializer.data.get('email')
                model= RestaurantList.objects.filter(email=email)
                rest_serializer= RestDetailSerializer(model, many=True)
                rest_name= rest_serializer.data.get('name')
                data= {
                'status': True,
                'data': rest_name,
                'token': str(token),
                'error': False
                    }
                return Response(data)
        else:
            data={'status':True,
            'data':'Account does not exist',
            'error':False}
            return Response(data)
            
                # return Response(str(AccessToken.for_user(user)))

class MenuItemsView(ModelViewSet):
    queryset = MenuItems.objects.all()
    serializer_class = MenuItemsSerializer
    # permission_classes = [IsAuthenticated]
    def list(self, request, *args, **kwargs):
        try:
            data = request.GET.get('restaurant')
            queryset =MenuItems.objects.filter(restaurant=data)
            serializer = MenuItemsSerializer(queryset,many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(str(e))
        
#test

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