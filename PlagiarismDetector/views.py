from django.shortcuts import render
from modelo.models import Usuario

def index(request):
    user = request.user 
    usuario = Usuario.objects.get(correo=user.email)
    if usuario.estado:                         
        return render(request, 'homepage.html')
    else:
        return render(request, 'login/deactive.html')

def about(request):
     return render(request, 'about.html')