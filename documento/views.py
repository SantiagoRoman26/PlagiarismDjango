import os
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from modelo.models import Documento, Usuario, GestionDocumentos, Estudiante, Docente
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse

@login_required
def subir_archivo(request):
    user = request.user
    usuario = Usuario.objects.get(correo=user.email)
    print(usuario.usuario_id)
    if usuario.estado:
        if request.method == 'POST':
            
            # documento=Documento.objects.filter(usuario=usuario).last()
            # documento.visible = False
            # documento.save()
            documento = Documento()
            archivo = request.FILES['archivo']
            ext = os.path.splitext(archivo.name)[-1].lower()
            if ext == '.pdf':
                documento.tipo = 'pdf'
            elif ext in ['.doc', '.docx']:
                documento.tipo = 'word'
            elif ext == '.txt':
                documento.tipo = 'texto'
            else:
                documento.tipo = 'other'
            # documento.usuario = usuario
            documento.archivo = archivo
            documento.visible = True

            if Docente.objects.filter(usuario = usuario).exists():
                docente = Docente.objects.get(usuario = usuario)
                ########################################
                if GestionDocumentos.objects.filter(docente = docente.docente_id).exists():
                    listaGestion = GestionDocumentos.objects.filter(docente = docente.docente_id).last()
                    
                    ultimo_documento = listaGestion.documento
                    ultimo_documento.visible = False
                    ultimo_documento.save()
                #######################################
                documento.save()
                
                gestion = GestionDocumentos()
                gestion.docente = docente
                gestion.documento = documento
                gestion.save()

            elif Estudiante.objects.filter(usuario = usuario.usuario_id).exists():
                estudiante = Estudiante.objects.get(usuario = usuario.usuario_id)
                documento.save()
                #envio a una view de gestionDocumentos para la asignacion al docente.
                response_data = {'redirect_url': reverse('gestion_estudiante', args=[estudiante.estudiante_id, documento.documento_id])}
                return JsonResponse(response_data)
                # return HttpResponseRedirect(reverse('gestion_estudiante', args=[estudiante.estudiante_id, documento.documento_id]))
            else:
                return HttpResponseRedirect(reverse('no_activo'))

            # return redirect(visualizar_archivo,documento.documento_id)
            response_data = {'redirect_url': reverse('visualizar_archivo', args=[documento.documento_id])}
            return JsonResponse(response_data)
            # else:
            #     return render(request,'documento/subir_archivo.html',{'mensaje':'Usuario no encontrado'}) #ojo registrar el usuario, en el caso de un registro erroneo
        return  render(request, 'documento/subir_archivo.html')
    else :
        return render(request, 'homepage.html')
#Cambio por realizar en la logica, antes de almacenar el archivo, deberia ser posible subir el archivo solo para ver una visualizacion del documento a analizar
#una vez seleccionado para analizar el documento debe guardarse, se puede mandar a anlizar o cancelar el documento que se subio.
@login_required
def visualizar_archivo(request, gestion_id):
    user = request.user
    gestion = GestionDocumentos.objects.get(gestion_id = gestion_id)
    # documento = Documento.objects.get(documento_id = gestion.documento_id)
    documento = gestion.documento #ojo
    if request.method == 'GET': #post bajar toda la logica fuera del return. 7-
            
        context = {
        'gestion' : gestion,
        'documento': documento,
        }
        return render(request, 'documento/visualizar.html', context)
       
    return render(request,'documento/visualizar.html', context)