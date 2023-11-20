from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('jobs/', views.jobs, name='jobs'),
    path('jobs/add/', views.add_edit_job, name='add_job'),
    path('jobs/edit/<int:job_id>/', views.add_edit_job, name='edit_job'),

    path('jobs/delete/', views.delete_job, name='delete_job'),
    path('jobs/<int:job_id>/', views.view_job, name='view_job'),

    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
