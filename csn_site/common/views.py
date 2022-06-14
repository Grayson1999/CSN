from django.contrib.auth import authenticate, login
# from django.contrib.auth.views import LoginView 
from django.shortcuts import render, redirect
from requests import request

from .forms import UserForm


def signup(request):
    """
    계정생성
    """
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'common/sign_up.html', {'form': form})

# class UserLoginView(LoginView, request):
#     template_name='common/log_in.html'

#     class Meta():
#         redirect_to = request.REQUEST.get('next', '')

    # def get_success_url(self):
    #     return super().get_redirect_url()

    # def get_redirect_url(self):
    # """Return the user-originating redirect URL if it's safe."""
    #     redirect_to = self.request.POST.get(
    #         self.redirect_field_name, self.request.GET.get(self.redirect_field_name, "")
    #     )
    #     url_is_safe = url_has_allowed_host_and_scheme(
    #         url=redirect_to,
    #         allowed_hosts=self.get_success_url_allowed_hosts(),
    #         require_https=self.request.is_secure(),
    #     )
    #     return redirect_to if url_is_safe else ""