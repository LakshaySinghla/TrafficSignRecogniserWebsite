from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload_file , name='upload'),
    path('success/<str:name>/', views.success , name='success'),
]