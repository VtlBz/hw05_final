# users/urls.py

from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    # Личный кабинет
    path(
        'account/',
        views.accaunt,
        # views.AccountView.as_view(),
        name='account'
    ),
    # Авторизация
    path(
        'login/',
        views.LoginView.as_view(),
        name='login'
    ),
    # Выход
    path(
        'logout/',
        views.LogoutView.as_view(),
        name='logout'
    ),
    # Регистрация
    path(
        'signup/',
        views.SignUp.as_view(),
        name='signup'
    ),
    # Смена пароля
    path(
        'password_change/',
        views.PasswordChangeView.as_view(),
        name='password_change_form'
    ),
    # Сообщение об успешном изменении пароля
    path(
        'password_change/done/',
        views.PasswordChangeDoneView.as_view(),
        name='password_change_done'
    ),
    # Восстановление пароля
    path(
        'password_reset/',
        views.PasswordResetView.as_view(),
        name='password_reset_form'
    ),
    # Сообщение об отправке ссылки для восстановления пароля
    path(
        'password_reset/done/',
        views.PasswordResetDoneView.as_view(),
        name='password_reset_done'
    ),
    # Вход по ссылке для восстановления пароля
    path(
        'password_reset/<uidb64>/<token>/',
        views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
    # Сообщение об успешном восстановлении пароля
    path(
        'password_reset/complete/',
        views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'
    ),
    path(
        'end_of_<str:username>/',
        views.kill_me_please,
        name='kmp'
    ),
]
