from django.urls import path
from . import views

app_name = 'users_app'

urlpatterns = [
    path(
        'register/',
        views.UserRegisterView.as_view(),
        name='user_register'
    ),
    path(
        'login/',
        views.LoginUser.as_view(),
        name='user_login'
    ),
    path(
        'logout/',
        views.LogOutView.as_view(),
        name='user_logout'
    ),
    path(
        'update/',
        views.UpdatePassword.as_view(),
        name='user_update_password'
    ),
    path(
        'user-verification/<pk>/',
        views.CodeVerificationView.as_view(),
        name='user_verification'
    ),
]