from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import BaseRegisterView, LoginCredentialView, LoginKeyView

urlpatterns = [
    path('login/',
         LoginCredentialView.as_view(template_name = 'sign/login_credential.html'),
         name='login'),
    path('login/key/', LoginKeyView.as_view(), name='login_key'),
    path('logout/',
         LogoutView.as_view(template_name = 'sign/logout.html'),
         name='logout'),
    path('signup/',
         BaseRegisterView.as_view(template_name = 'sign/signup.html'),
         name='signup'),
]