import random

from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, FormView
from .models import BaseRegisterForm, OneTimeCode
from .forms import LoginCredentialForm, LoginKeyForm
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.core.mail import send_mail

class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'

class LoginCredentialView(FormView):

    form_class = LoginCredentialForm
    template_name = 'sign/login_credential.html'

    def post(self, request, *args, **kwargs):

        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        user = authenticate(request, username=username, password=password, email=email)

        if user is None:
            OneTimeCode.objects.create(secret_code=random.choice('12345'), user=user)
            send_mail(
                subject='Login to board',
                message=f'Для входа используйте ключ:',
                from_email='Tailingen1@yandex.ru',
                recipient_list=[request.user.email],
                fail_silently=False,
            )
            target = redirect('/key')
        else:
            target = redirect('/ads')

        return target

class LoginKeyView(FormView):

    form_class = LoginKeyForm
    template_name = 'sign/login_key.html'

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        secret_code = request.POST['secret_code']
        if OneTimeCode.objects.filter(secret_code=secret_code, user__username=username).exists():
            login(request, username)
            target = redirect('/ads')
        else:
            target = redirect('/ads')

        return target