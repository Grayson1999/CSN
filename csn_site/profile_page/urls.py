from django.contrib import admin
from pathlib import Path
from django.urls import include, path
from . import views

urlpatterns = [
    path("",views.index),
    path('common/', include('common.urls')),
    path('', views.index, name='index'), #추가
    
]