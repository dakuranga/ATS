from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('clients/', views.clients, name='clients'),
    path('clients/add/', views.add_client, name='add_client'),
    path('clients/edit/<int:pk>/', views.add_client, name='edit_client'),  
    path('clients/delete/<int:pk>/', views.delete_client, name='delete_client'), 
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
