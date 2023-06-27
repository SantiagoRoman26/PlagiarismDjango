from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from modelo.models import Usuario
from django.contrib import messages

# #app autorizar 
# def solicitarRol (request, usuario_id):
#     user = request.user 
#     usuario = Usuario.objects.get(usuario_id=usuario_id)
#     if request.method == 'POST':
#         role = request.POST.get('role')            
#         if role == 'teacher':
#             usuario.autorizado = True
#             usuario.estado = False
#             usuario.save()
#         else:
#             return render(request, 'login/deactive.html')                                             #pagina de muestra de errores
#         return HttpResponseRedirect(reverse('autenticar'))
#     return render(request, 'autorizar/solicitarRol.html') 

@login_required
def generarRol (request,usuario_id):
    usuario = Usuario.objects.get(usuario_id=usuario_id)
    if request.method == 'POST':
        usuario.autorizado = True                           # el usuario es considerado un docente
        usuario.estado = True 
        usuario.save()
        return ""
    usuario.autorizado = False                              # el usuario es considerado un alumno
    usuario.estado = True
    usuario.save()
    return HttpResponseRedirect(reverse('homepage'))