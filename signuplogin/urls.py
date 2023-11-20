# inout/urls.py

from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('confirm-email/<str:uidb64>/<str:token>/',
         views.confirm_email,
         name='confirm-email'),
    path('account_activation_sent/',
         views.account_activation_sent,
         name='account_activation_sent'),
    path('logout/', LogoutView.as_view(next_page='login'),
         name='logout'),  # Update this line
    path('resend_activation/',
         views.resend_activation,
         name='resend_activation'),

    path('password_reset/', views.password_reset_view, name='password_reset'),
    path('password_reset/done/', views.password_reset_done_view, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.password_reset_confirm_view, name='password_reset_confirm'),
    path('reset/done/', views.password_reset_complete_view, name='password_reset_complete'),
]
