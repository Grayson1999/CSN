from pathlib import Path
from django.urls import path, include
from . import views

urlpatterns = [
    path("",views.PostList.as_view(), name="community_page"),
    path("<int:pk>/", views.PostDetail.as_view()),
    path('post_create/', views.post_create, name="post_create"),
]