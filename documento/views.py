import os
from django.shortcuts import render, redirect
from modelo.models import Documento, Usuario
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse

@login_required
def subir_archivo(request):
    user = request.user
    if request.method == 'POST':
        usuario = Usuario.objects.filter(correo=user.email)
        if  usuario.exists():
            usuario = Usuario.objects.get(correo=user.email)
            documento=Documento.objects.filter(usuario=usuario).last()
            documento.visible = False
            documento.save()

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
            documento.save()

            # return redirect(visualizar_archivo,documento.documento_id)
            response_data = {'redirect_url': reverse('visualizar_archivo', args=[documento.documento_id])}
            return JsonResponse(response_data)
        else:
            return render(request,'documento/subir_archivo.html',{'mensaje':'Usuario no encontrado'}) #ojo registrar el usuario, en el caso de un registro erroneo
    return  render(request, 'documento/subir_archivo.html')

@login_required
def visualizar_archivo(request, documento_id):
    user = request.user
    documento = Documento.objects.get(documento_id = documento_id)
    usuario = Usuario.objects.get(correo=user.email)
    # if documento.usuario == usuario:
    if request.method == 'GET': #post bajar toda la logica fuera del return. 
            
        context = {
        'documento': documento,
        }
        return render(request, 'documento/visualizar.html', context)
            #return HttpResponseRedirect(reverse('modelo'))
    # else: 
    #     return render(request, 'login/forbidden.html', locals())
       
    return render(request,'documento/visualizar.html', context)