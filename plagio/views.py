import os
import glob
import shutil
from django.shortcuts import render, redirect
from modelo.models import Documento, Usuario, Resultado
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from .nlp.src.python import main

 

# Create your views here.
@login_required
def detectar(request, documento_id):
    user = request.user
    documento = Documento.objects.get(documento_id = documento_id)
    usuario = Usuario.objects.get(correo=user.email)
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
    resultado.archivo.save(nombre, archivo_django)
    resultado.estado = True
    resultado.save()
    return render(request,'plagio/Success.html',locals())
    # else: 
    #     return render(request, 'login/forbidden.html', locals())
