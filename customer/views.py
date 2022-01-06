from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.decorators import action, permission_classes
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import SlidingToken,AccessToken
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from restaurant.models import Order
from restaurant.serializers import OrderSerializer
from .models import Customer
from .serializers import CustomerSerializer
from datetime import datetime
import sys
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class CustomerView(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self,request):
        try:
            rawData = request.data
            # dob = rawData.get('dob').split('-')
            # dob = datetime(int(dob[0]),int(dob[1]),int(dob[2]))
            # rawData['dob']=dob
            data = rawData
            serializer = CustomerSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            data = {'status': True,
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
                'error': str(e),
            }
            
            return Response(data, filename, line_number)
    def list(self,request):
        try:
            data = Customer.objects.all()
            data_serializer = CustomerSerializer(data, many = True)
            data ={
                    'status':True,
                    'data': data_serializer.data,
                    'error':None
                    }
            return Response(data)
        except Exception as e:
            return Response(str(e))

    # def update(self, request, *args, **kwargs):
    #     user=request.user
    #     try:
    #         rawData = request.data
    #         # dob = rawData.get('dob').split('-')
    #         # dob = datetime(int(dob[0]),int(dob[1]),int(dob[2]))
    #         # rawData['dob']=dob
    #         data = rawData
    #         serializer = CustomerSerializer(user, data=data, partial=True)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()
    #         data = {'status': True,
    #                 'data': serializer.data,
    #                 'error':None
    #         }
    #         return Response(data)
    #     except Exception as e:
    #         exception_type, exception_object, exception_traceback = sys.exc_info()
    #         filename = exception_traceback.tb_frame.f_code.co_filename
    #         line_number = exception_traceback.tb_lineno
    #         data= {
    #             'status': False,
    #             'data': [],
    #             'error': str(e),
    #             'line_number':line_number,
    #         }
            
    #         return Response(data)

    @action(methods=['get'], detail=False,permission_classes=[])
    def send_otp(self,request):
        try:
            phone=request.GET.get('phone')
            user=User.objects.get(username=phone)
            data = {
                'status':True,
                'data':'OTP Sent',
                'error':None
            }
            return Response(data)
        except Exception as e:
            phone=request.GET.get('phone')
            user=User.objects.create_user(username=phone,password='password')
            data = {
                'status':True,
                'data':'OTP Sent',
                'error':None
            }
            return Response(data)

    
    @action(detail=False, methods=['POST'], permission_classes=[])
    def login(self,request):
        try:
            phone=request.GET.get('phone')
            otp=request.GET.get('otp')
            if '123456'==otp or 123456==otp:
                try:
                    user = User.objects.get(username=phone)
                    token = AccessToken.for_user(user)
                    try:
                        customer=Customer.objects.create(mobile=phone)
                    except:
                        customer=Customer.objects.get(mobile=phone)
                    customer=CustomerSerializer(customer)
                    data = {
                        'status':True,
                        'token':str(token),
                        'user':customer.data,
                        'error':None
                    }
                    return Response(data)
                except Exception as e:
                    data = {
                        'status':False,
                        'data':'User not found',
                        'error':str(e)
                    }
                    return Response(data)
            else:
                data = {
                    'status':False,
                    'data':'Invalid OTP',
                    'error':None
                }
                return Response(data)
        except Exception as e:
            data = {
                'status':False,
                'data':'Something went wrong',
                'error':str(e)
            }
            return Response(data)
            

    @action(detail=False,methods=['GET'])
    def order_history(self,request):
        id= request.GET.get('id')
        data= Order.objects.filter(customer_id=id)
        serializer = OrderSerializer(data, many=True)
        data={
            'status':True,
            'data': serializer.data,
            'error':False
        }
        return Response(data)