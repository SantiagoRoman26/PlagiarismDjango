from django.shortcuts import render

from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
# Create your views here.

def emailAutorizacion(User_mail, User_nombre, Admin_Email, Admin_nombre, url):
    context = { 
        'user_mail' : User_mail,
        'user_nombre' : User_nombre,
        'url' : url,
        'admin' : Admin_nombre
               }
    template = get_template('correo/Autorizacion.html')
    content = template.render(context)
    email = EmailMultiAlternatives(
        'Registro de docente',
        'Nuevo Registro',
        settings.EMAIL_HOST_USER,
        [Admin_Email] #todos los destinatarios a quien enviarlos
        #cc= [] #envio de una copia
    )
    email.attach_alternative(content, 'text/html')
    email.send()
    print ('Correo Enviado!')

def emailRegistroCompletado(User_mail, User_nombre, url):
    context = { 
        'user_mail' : User_mail,
        'user_nombre' : User_nombre,
        'url' : url,
               }
    template = get_template('correo/cuenta_registrada.html')
    content = template.render(context)
    email = EmailMultiAlternatives(
        'Registro de docente',
        'Nuevo Registro',
        settings.EMAIL_HOST_USER,
        [User_mail] #todos los destinatarios a quien enviarlos
        #cc= [] #envio de una copia
    )
    email.attach_alternative(content, 'text/html')
    email.send()
    print ('Correo Enviado!')

def emailCompartir(mail):
    context = { 'mail' : mail }
    template = get_template('correo/Compartir.html')
    content = template.render(context)
    email = EmailMultiAlternatives(
        'Un correo de prueba',
        'Descripcion del correo',
        settings.EMAIL_HOST_USER,
        [mail] #todos los destinatarios a quien enviarlos
        #cc= [] #envio de una copia
    )
    email.attach_alternative(content, 'text/html')
    email.send()

def emailResultado(mail):
    context = { 'mail' : mail }
    template = get_template('correo/proceso_concluido.html')
    content = template.render(context)
    email = EmailMultiAlternatives(
        'Un correo de prueba',
        'Descripcion del correo',
        settings.EMAIL_HOST_USER,
        [mail] #todos los destinatarios a quien enviarlos
        #cc= [] #envio de una copia
    )
    email.attach_alternative(content, 'text/html')
    email.send()

