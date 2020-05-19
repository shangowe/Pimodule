"""Pimodule URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import url,include

from django.urls import include, path
from rest_framework import routers
from Pimoduleapp import views

router = routers.DefaultRouter()
router.register(r'module', views.ModuleViewSet)


urlpatterns = [
    path('',include(router.urls)),
    path('getall/',views.ModuleData.as_view()),
    path('bts/',views.BTS.as_view()), # endpoint to get status of bts
    path('btsoff/',views.BTSOFF.as_view()), # endpoint to switch off bts
    path('btson/',views.BTSON.as_view()), # endpoint to switch on bts
    path('hvac/',views.HVAC.as_view()), # endpoint to  get status of HVAC
    path('hvacoff/',views.HVACOFF.as_view()), # endpoint to  switch hvac off
    path('hvacon/',views.HVACON.as_view()), # endpoint to set hvac on
    path('gen/',views.GEN.as_view()), # endpoint to  get status of GEN
    path('genoff/',views.GENOFF.as_view()), # endpoint to  switch gen off
    path('genon/',views.GENON.as_view()), # endpoint to set gen on
    path('setup/<str:pk>',views.SetupView.as_view()) #endpoint to setup the device attributes
]