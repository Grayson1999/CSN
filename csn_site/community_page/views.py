from datetime import timezone
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from .models import Photo, Post
from django import forms
from django_summernote.widgets import SummernoteWidget
from .forms import PostForm

# from users.decorators import admin_required

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

def create(request):
    if(request.method == 'POST'):
        post = Post()
        post.title = request.POST['title']
        post.content = request.POST['content']
        post.pub_date = timezone.datetime.now()
        post.user = request.user
        post.save()
        # name 속성이 imgs인 input 태그로부터 받은 파일들을 반복문을 통해 하나씩 가져온다 
        for img in request.FILES.getlist('imgs'):
            # Photo 객체를 하나 생성한다.
            photo = Photo()
            # 외래키로 현재 생성한 Post의 기본키를 참조한다.
            photo.post = post
            # imgs로부터 가져온 이미지 파일 하나를 저장한다.
            photo.image = img
            # 데이터베이스에 저장
            photo.save()
        return redirect('/detail/' + str(post.id))
    else:
        return render(request, 'new.html')  

def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = Post(**form.cleaned_data)
            post.save()
            return redirect('community/')
    else:
        form = PostForm()
    context = {
        'form' : form
    }
    return render(request, 'community_page/post_create.html', context)