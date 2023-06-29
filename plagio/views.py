import os
import glob
import shutil
from django.shortcuts import render, redirect
from modelo.models import Documento, Usuario, Resultado, GestionDocumentos, Docente
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from .nlp.src.python import main

 

# Esta logica solo funciona en la fase de pruebas, en produccion se debe tomar el documento desde la ruta base, en donde se va a cambiar el config para ingresar al
# documento a analizar.
@login_required
def detectar(request, gestion_id):
    user = request.user
    usuario = Usuario.objects.get(correo=user.email)
    if usuario.estado:
        #Cambio: agregar si el usuario pertenece al grupo de docentes
        gestion = GestionDocumentos.objects.get(gestion_id = gestion_id)
        # documento = Documento.objects.get(documento_id = gestion.documento_id) 
        documento = gestion.documento #ojo
        ruta=os.getcwd()
        new = ruta.replace('\\','/')
        file_path= new +'/plagio/nlp/Test'
        # if documento.usuario == usuario:
        try:
            resultado = Resultado.objects.filter(usuario=usuario).last()
            resultado.estado = False
            resultado.save()
        except Exception as e:
                # Manejar el error de manera general
                # Puedes imprimir el mensaje de error, realizar alguna acción alternativa, etc.
            print(f"Ocurrió un error: {str(e)}")

        ruta_documento_original = documento.archivo.path
            
        print(os.path)
        archivos_existentes = glob.glob(os.path.join(file_path, '*'))
        for archivo in archivos_existentes:
            os.remove(archivo)
        nombre_documento = os.path.basename(ruta_documento_original)
        ruta_documento_nuevo = os.path.join(file_path, nombre_documento)
        shutil.copy2(ruta_documento_original, ruta_documento_nuevo)

        documento_generado, nombre= main.main()
        with open(documento_generado, 'rb') as archivo:
            archivo_django = ContentFile(archivo.read(), name=nombre)

        resultado = Resultado()
        resultado.documento = documento
        resultado.management = gestion
        resultado.archivo.save(nombre, archivo_django)
        resultado.estado = True
        resultado.save()
        return HttpResponseRedirect(reverse('revision',resultado.resultado_id))
    return render(request, 'homepage.html')
    
@login_required
def index(request):
    user = request.user
    usuario = Usuario.objects.get(correo=user.email)
    if usuario.estado:
        #Cambio: agregar si el usuario pertenece al grupo de docentes
        cond = False
        docente = Docente.objects.get(usuario = usuario)
        listaGestion = GestionDocumentos.objects.filter(docente = docente)
        listaResultado = []
        for gestion in listaGestion:
            resultado = Resultado.objects.get(management=gestion)
            
            listaResultado.append(resultado)
            if gestion.estudiante:
                cond = True
        # busqueda = request.POST.get("busqueda")
        # if busqueda:
        #     listaResultado = Resultado.objects.filter(
        #         Q(numero__icontains = busqueda) |
        #         Q(aereolinea__icontains = busqueda) 
        #     ).distinct() 
        return render (request, 'plagio/index.html', locals())
    return render(request, 'homepage.html')

@login_required
def revision(request,resultado_id):
    user = request.user
    usuario = Usuario.objects.get(correo=user.email)
    if usuario.estado:
        resultado = Resultado.objects.get(resultado_id = resultado_id)
        return render(request,'plagio/Success.html',locals())
    return