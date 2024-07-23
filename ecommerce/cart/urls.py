"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from cart import views
app_name='cart'

urlpatterns = [
    path('add_to_cart/<int:pk>/',views.add_to_cart,name="add_to_cart"),
    path('cart_view',views.cart_view,name="cart_view"),
    path('cart_decrement/<int:p>/',views.cart_decrement,name="cart_decrement"),
    path('remove/<int:p>/',views.remove,name="remove"),
    path('order_form',views.order_form,name="order_form"),
    path('payment_status/<u>',views.payment_status,name="payment_status"),
    path('order_view',views.order_view,name="order_view"),
]



