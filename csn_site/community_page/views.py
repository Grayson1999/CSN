from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post

# Create your views here.
# def community(request):
#     return render(
#         request,
#         'community_page/community.html'
#     )

class PostList(ListView):
    model = Post
    ordering = '-pk'
    template_name = 'community_page/community.html'

class PostDetail(DetailView):
    model = Post
    template_name = 'community_page/community_detail.html'