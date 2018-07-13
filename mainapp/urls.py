"""AXF_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path, include

from mainapp import views

urlpatterns = [
    path('', views.home),
    path('market/<int:categoryid>/<int:childcid>/<int:sortid>', views.market),
    path('register', views.register),
    path('cart', views.cart),
    path('mine', views.mine),
    path('upload', views.upload),
    path('login', views.login),
    path('logout', views.logout),
    path('select/<int:cart_id>', views.selectCart),
    path('addCart/<int:cart_id>', views.addCart),
    path('subCart/<int:cart_id>', views.subCart),
    path('order/<str:num>', views.order),
    path('pay/<str:num>/<int:payType>', views.pay),
    path('noPayOrder/<int:condition>', views.noPayOrder),
    path('address', views.address),
    path('editAddress', views.editAddress),
    path('addAddress', views.addAddress),
    path('delAddress', views.delAddress),

]
