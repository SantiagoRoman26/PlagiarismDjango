from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from modelo.models import Documento, Usuario, GestionDocumentos, Estudiante, Docente
from django.contrib.auth.decorators import login_required
from .forms import FormularioGestion
from django.http import JsonResponse

# Create your views here.
@login_required
def gestionEstudiante (request,estudiante_id,documento_id):
    user = request.user
    usuario_global = Usuario.objects.get(correo=user.email)
    if usuario_global.estado:
        formulario_gestion = FormularioGestion(request.POST)
        if request.method == 'POST':
            if formulario_gestion.is_valid():
                gestion_documento = GestionDocumentos()
                datos_gestion = formulario_gestion.cleaned_data
                #verificar que el email del docente exista
                email_docente = datos_gestion.get('email')
                if Usuario.objects.filter(correo=email_docente).exists():
                    #verificar si el usuario esta registrado como docente
                    print(" ################################################################################## ")
                    print(" verificar si el usuario esta registrado como docente ")
                    print(" ################################################################################## ")
                    usuario = Usuario.objects.get(correo=email_docente)
                    if Docente.objects.filter(usuario = usuario).exists():
                        print("aqui")
                        estudiante = Estudiante.objects.get(estudiante_id = estudiante_id)
                        documento = Documento.objects.get(documento_id = documento_id)
                        ######################
                        if GestionDocumentos.objects.filter(estudiante = estudiante).exists():
                            print(" ################################################################################## ")
                            print(" entra ")
                            print(" ################################################################################## ")
                            listaGestion = GestionDocumentos.objects.filter(estudiante = estudiante).last()
                            ultimo_documento = listaGestion.documento
                            ultimo_documento.visible = False
                        ######################

                        gestion_documento.titulo = datos_gestion.get('titulo')
                        gestion_documento.comentario = datos_gestion.get('comentario')
                        gestion_documento.estudiante = estudiante
                        gestion_documento.docente = Docente.objects.get(usuario = usuario)
                        gestion_documento.documento = documento
                        gestion_documento.save()
                        documento.visible = True
                        documento.save()

                        return HttpResponseRedirect(reverse('visualizar_archivo', args=[gestion_documento.gestion_id])) #ojo
                    else:
                        return HttpResponseRedirect(reverse('homepage'))
                else:
                    return HttpResponseRedirect(reverse('homepage'))
                
            return render(request, 'gestion/gestionEstudiante.html',locals())
        
        return render(request, 'gestion/gestionEstudiante.html',locals())
    else:
        return render(request, 'homepage.html')