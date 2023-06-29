from django.urls import path
from . import views

urlpatterns = [
    # path('', views.autenticar, name="autenticar"),
    path('estudiante/<int:estudiante_id>/<int:documento_id>/', views.gestionEstudiante, name="gestion_estudiante"),
] 