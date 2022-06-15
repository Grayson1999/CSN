from datetime import timezone
from urllib import response
from django.shortcuts import render, redirect, get_object_or_404
from django.test import tag
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Post, Tag, Comment
# from .models import Photo
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify
from .forms import CommentForm

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
    paginate_by = 10
    block_size = 5 # 하단의 페이지 목록 수

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data(**kwargs)

        start_index = int((context['page_obj'].number - 1) / self.block_size) * self.block_size
        end_index = min(start_index + self.block_size, len(context['paginator'].page_range))

        context['page_range'] = context['paginator'].page_range[start_index:end_index]

        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'community_page/community_detail.html'

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context['comment_form'] = CommentForm

        return context

class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'community_page/post_create.html'
    fields = ['title', 'content']

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.author = current_user
            response = super(PostCreate, self).form_valid(form)

            tags_str = self.request.POST.get('tags')
            if tags_str:
                tags_str = tags_str.strip()

                tags_str = tags_str.replace(',', ';')
                tags_list = tags_str.split(';')

                for t in tags_list:
                    t = t.strip()
                    if t != '':
                        tag, is_tag_created = Tag.objects.get_or_create(name=t)
                        if is_tag_created:
                            tag.slug = slugify(t, allow_unicode=True)
                            tag.save()
                        self.object.tags.add(tag)
            return response
            
        else:
            return redirect('/community/')

class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'community_page/post_update.html'
    fields = ['title', 'content']

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_context_data(self, **kwargs):
        context = super(PostUpdate, self).get_context_data()
        if self.object.tags.exists():
            tags_str_list = list()
            for t in self.object.tags.all():
                tags_str_list.append(t.name)
            context['tags_str_default'] = ';'.join(tags_str_list)
        post = Post.objects.get(pk=self.get_object().pk)
        context['title_default'] = post.title
        context['content_default'] = post.content

        return context

    def form_valid(self, form):
        response = super(PostUpdate, self).form_valid(form)
        self.object.tags.clear()

        tags_str = self.request.POST.get('tags')
        if tags_str:
            tags_str = tags_str.strip()

            tags_str = tags_str.replace(',', ';')
            tags_list = tags_str.split(';')

            for t in tags_list:
                t = t.strip()
                if t != '':
                    tag, is_tag_created = Tag.objects.get_or_create(name=t)
                    if is_tag_created:
                        tag.slug = slugify(t, allow_unicode=True)
                        tag.save()
                    self.object.tags.add(tag)
        return response

class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "community_page/comment_update.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(CommentUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

def PostDelete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    author = post.author
    if request.user.is_authenticated and request.user == User.objects.get(username=author):
        if request.method == 'POST':
            post.delete()        
            return redirect('../../')
        else:
            return redirect(post.get_absolute_url())
    else:
        raise PermissionDenied

def CommentDelete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post = comment.post
    if request.user.is_authenticated and request.user == comment.author:
        comment.delete()
        return redirect(post.get_absolute_url())
    else:
        raise PermissionDenied

def new_comment(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)

        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
        else:
            return redirect(post.get_absolute_url())
    else:
        raise PermissionDenied

# def create(request):
#     if(request.method == 'POST'):
#         post = Post()
#         post.title = request.POST['title']
#         post.content = request.POST['content']
#         post.pub_date = timezone.datetime.now()
#         post.user = request.user
#         post.save()
#         # name 속성이 imgs인 input 태그로부터 받은 파일들을 반복문을 통해 하나씩 가져온다 
#         for img in request.FILES.getlist('imgs'):
#             # Photo 객체를 하나 생성한다.
#             photo = Photo()
#             # 외래키로 현재 생성한 Post의 기본키를 참조한다.
#             photo.post = post
#             # imgs로부터 가져온 이미지 파일 하나를 저장한다.
#             photo.image = img
#             # 데이터베이스에 저장
#             photo.save()
#         return redirect('/detail/' + str(post.id))
#     else:
#         return render(request, 'new.html')  

# def post_create(request):
#     if request.method == "POST":
#         form = PostForm(request.POST, request.FILES)
#         if form.is_valid():
#             post = Post(**form.cleaned_data)
#             post.save()
#             return redirect('../')
#     else:
#         form = PostForm()

#     context = {
#         'form' : form,
#     }
#     return render(request, 'community_page/post_create.html', context)

# def post_update(request, pk):
#     post = Post.objects.get(id=pk)
#     # if request.method == "POST":
#     #     form = PostForm(request.POST, request.FILES)
#     #     if form.is_valid():
#     #         post = Post(**form).objects.filter(pk='pk')
#     #         post.save()
#     #         return redirect('../')
#     # else:
#     #     form = PostForm()

#     context = {
#         'form' : post,
#     }
#     return render(request, 'community_page/post_create.html', context)



#좋아요

def post_like(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    #좋아요 확인
    if request.user in post.like_user_set.all():
            post.like_user_set.remove(request.user)
    else:
            post.like_user_set.add(request.user)

    if request.GET.get('redirect_to') == 'community':
        return redirect('community',post_id)
    else:
        return redirect('community',post_id)

#