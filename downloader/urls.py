from django.urls import path
from . import views

app_name = 'downloader'

urlpatterns = [
    path('', views.index, name='index'),
    path('download/', views.download, name='download'),
    path('status/<str:task_id>/', views.download_status, name='download_status'),
    path('files/', views.list_files, name='list_files'),
    path('files/download/<path:filename>/', views.download_file, name='download_file'),
]
