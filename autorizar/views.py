from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from modelo.models import Usuario, Docente
from django.contrib import messages
from .forms import FormularioAutorizacion

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
    user = request.user
    if user.is_superuser:
        
        usuario = Usuario.objects.get(usuario_id=usuario_id)
        formulario_autorizacion = FormularioAutorizacion(request.POST)
        if request.method == 'POST':
            if formulario_autorizacion.is_valid():
                opcion_seleccionada = formulario_autorizacion.cleaned_data['seleccion']
                if opcion_seleccionada == 'autorizar':
                    docente_model = Docente()
                    docente_model.usuario = usuario
                    usuario.autorizado = True                           # el usuario es considerado un docente
                    usuario.estado = True 
                    usuario.save()
                    docente_model.save()
                    print('docente Guardado')
                    return HttpResponseRedirect(reverse('homepage'))
                else:
                    usuario.autorizado = False                              # el usuario es considerado un alumno
                    usuario.estado = True
                    usuario.save()
                    print('docente no guardado')
        print("#################aqui#############################")
        return render(request, 'autorizar/autorizar.html',locals()) 
    return render(request, 'login/forbidden.html') 