
from django.contrib import admin
from django.urls import path, include, re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('clients.urls')),
    path('', include('signuplogin.urls')),
    path('', include('home.urls')),
    path('', include('jobs.urls')),
    path('settings/', include('settingsapp.urls')),

]
