from django.urls import path
from . import views

urlpatterns = [
    path('detectar/<int:documento_id>/', views.detectar, name='detectar'),
    # path('upload', views.subir_archivo, name='subir_archivo'),
    # path('visualizar/<int:documento_id>/', views.visualizar_archivo, name='visualizar_archivo'),
]
