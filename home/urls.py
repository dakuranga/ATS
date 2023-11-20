from django.urls import path
from . import views

urlpatterns = [
    path('', views.myview, name='home'),
    path('today/', views.todayview, name='today'),
    path('dashboard/', views.dashboardview, name='dashboard'),
]
