from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import SlidingToken,AccessToken
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Customer
from .serializers import CustomerSerializer
from datetime import datetime
import sys


# Create your views here.
class CustomerView(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    
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

    @action(methods=['get'], detail=False)
    def signup(self,request):
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

    
    @action(detail=False, methods=['POST'])
    def login(self,request):
        try:
            data=request.data
            phone = data.get('phone')
            otp=data.get('otp')
            if '123456'==otp or 123456==otp:
                try:
                    user = User.objects.get(username=phone)
                    customer=Customer.objects.get(mobile=phone)
                    customer=CustomerSerializer(customer)
                    token = AccessToken(user)
                    data = {
                        'status':True,
                        'data':token,
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
            