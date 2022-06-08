from django import forms
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin

from django_summernote.widgets import SummernoteWidget

class PostForm(forms.ModelForm, LoginRequiredMixin):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'content': SummernoteWidget(),
        }