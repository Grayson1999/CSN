from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")
    password1 = forms.Field(label="비밀번호")
    password2 = forms.Field(label="비밀번호 확인")
    username = forms.Field(label="사용자 이름")


    class Meta:
        model = User
        fields = ("username", "email")