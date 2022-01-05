"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework.routers import SimpleRouter
# from restaurant.views import RestaurantDetailView, PartnerView, MenuItemsView, OrderView,
from restaurant.views import MenuItemsView, NewRestaurantViewSet, OrderView
from customer.views import CustomerView
from django.urls.conf import include


router = SimpleRouter()
# router.register('restaurantdetail', RestaurantDetailView)
router.register('customer', CustomerView)
# router.register('partner', PartnerView)
router.register('menuitems', MenuItemsView)
router.register('order', OrderView)
router.register('restaurantdetail', NewRestaurantViewSet)
urlpatterns = [
    path('',include(router.urls)),
    
]
