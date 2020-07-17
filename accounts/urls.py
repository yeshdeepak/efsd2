from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import *

#app_name = 'accounts'

urlpatterns = [
    path('register', views.register, name='register'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('login', views.user_login, name='login'),
    #path('register_done', views.user_login, name='register_done'),
    #path('search', views.search, name='search'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('accounts/password_reset', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
