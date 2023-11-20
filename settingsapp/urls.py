from django.urls import path, re_path
from . import views
from django.views.decorators.cache import never_cache
from ckeditor_uploader import views as ckeditor_views


urlpatterns = [

    path('', views.settings, name='settings'),

    path('clients/', views.settings_clients, name='settings_clients'),

    path('users/', views.settings_users, name='settings_users'),
    path('users/edit/<int:user_id>/', views.settings_users_edit, name='settings_users_edit'),
    path('users/delete/<int:user_id>/', views.settings_users_delete, name='settings_users_delete'),


    path('email/', views.settings_email, name='settings_email'),
    path('email/start-auth/', views.start_microsoft_auth, name='start_microsoft_auth'),
    path('auth-callback2/', views.microsoft_auth_callback, name='microsoft_auth_callback'),
    path('disconnect-email/', views.disconnect_email, name='disconnect_email'),


    path('email/signature', views.settings_email_signature, name='settings_email_signature'),
    re_path(r'^upload/', ckeditor_views.upload, name='ckeditor_upload'),
    re_path(r'^browse/', never_cache(ckeditor_views.browse), name='ckeditor_browse'),
    path('email/signature/create/', views.create_email_signature, name='create_email_signature'),

]
