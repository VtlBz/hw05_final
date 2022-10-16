# users/views.py

import django.contrib.auth.views as auth_

# from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from posts.models import User

from .forms import AccountForm, CreationForm

# User = get_user_model()


# Личный кабинет
def accaunt(request):
    if request.user.id is None:
        return redirect('posts:main_page')
    template = 'users/account.html'
    user = User.objects.get(pk=request.user.id)
    form = AccountForm(instance=user)
    return render(request, template, {'form': form})


# Авторизация
class LoginView(auth_.LoginView):
    template_name = 'users/login.html'


# Выход
class LogoutView(auth_.LogoutView):
    template_name = 'users/logged_out.html'


# Регистрация
class SignUp(CreateView):
    form_class = CreationForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('posts:main_page')


# Смена пароля
class PasswordChangeView(auth_.PasswordChangeView):
    template_name = 'users/password_change_form.html'
    success_url = reverse_lazy('users:password_change_done')


# Сообщение об успешном изменении пароля
class PasswordChangeDoneView(auth_.PasswordChangeDoneView):
    template_name = 'users/password_change_done.html'


# Восстановление пароля
class PasswordResetView(auth_.PasswordResetView):
    template_name = 'users/password_reset_form.html'
    email_template_name = 'users/password_reset_email.html'
    success_url = reverse_lazy('users:password_reset_done')


# Сообщение об отправке ссылки для восстановления пароля
class PasswordResetDoneView(auth_.PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'


# Вход по ссылке для восстановления пароля
class PasswordResetConfirmView(auth_.PasswordResetConfirmView):
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')


# Сообщение об успешном восстановлении пароля
class PasswordResetCompleteView(auth_.PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'


# Если не срослось
def kill_me_please(request):
    user = get_object_or_404(User, username=request.user.username)
    user.delete()
    return redirect('users:logout')
