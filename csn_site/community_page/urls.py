from pathlib import Path
from django.urls import path
from . import views

urlpatterns = [
    path("",views.community)
]