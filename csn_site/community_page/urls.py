from pathlib import Path
from django.urls import path, include
from . import views
from .views import *

#좋아요
# from django.contrib import admin
#
urlpatterns = [
    path('comment_delete/<int:pk>/', views.CommentDelete),
    path("",views.PostList.as_view(), name="community_page"),
    path("<int:pk>/", views.PostDetail.as_view(), name="community"),
    # path('post_create/', views.post_create, name="post_create"),
    path('post_create/', views.PostCreate.as_view(), name="post_create"),
    # path('<int:pk>/post_update/', views.post_update, name="post_update"),
    path('post_update/<int:pk>/', views.PostUpdate.as_view()),
    path('post_delete/<int:pk>/', views.PostDelete, name="post_delete"),
    path('<int:pk>/new_comment/', views.new_comment),
    path('comment_update/<int:pk>/', views.CommentUpdate.as_view()),

    #좋아요
    # path('<int:pk>/', views.PostDetail.as_view(), name="post_like"),
    path('<int:post_id>/post_like', post_like, name="post_like"),
]