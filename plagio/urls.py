from django.urls import path
from . import views

urlpatterns = [
    path('detectar/<int:gestion_id>/', views.detectar, name='detectar'),
    path('', views.index, name='resultados'),
    path('revision/<int:resultado_id>/', views.revision, name='revision'),
    path('eliminar/<int:resultado_id>/', views.eliminarResultado, name='eliminar_resultado'),
    # path('compartir_documento/<int:documento_id>/', views.compartirDocumento, name='compartir_documento'),
    path('compartir_documento/<int:resultado_id>/', views.compartirDocumento, name='compartir_documento'),
]
