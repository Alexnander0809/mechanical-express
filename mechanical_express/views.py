from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Mecanico, Usuario,  Profile, create_profile_for_user
from django.core.mail import send_mail
from django.contrib.auth import login, authenticate, logout

def principal(request):
    return render(request, "Home/principal.html")

def solicitar_servicio(request):
    mecanico = Mecanico.objects.filter(estado='Activo')
    return render(request, "Home/solicitar_servicio.html", {'mecanico': mecanico})

def contactenos(request):
    return render(request, "Home/contactenos.html")

def perfiles(request, id):
    mecanico = Mecanico.objects.filter(id=id)
    return render(request, "Home/perfiles.html", {'mecanico': mecanico})

def miperfil(request):
    return render(request, "Home/miperfil.html")

def configuracion(request):
    return render(request, "Home/configuracion.html")


def insertarusuario(request):
    if request.method == "POST":
        role = request.POST.get("role")
        nombres = request.POST.get("nombres")
        apellidos = request.POST.get("apellidos")
        telefono = request.POST.get("telefono")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(email=email).exists():
            messages.error(request, "El correo electrónico ya está en uso.")
            return render(request, 'Login/insertar.html', {'mensaje': "El correo electrónico ya está en uso."})

        if role and nombres and apellidos and password and email:
            usuario = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=nombres,
                last_name=apellidos
            )

            # Crear perfil de usuario en tu aplicación
            profile = create_profile_for_user(usuario, role)
            
            if role == "mecanico":
                messages.info(request, "¡Tu cuenta de mecánico ha sido creada! Por favor, inicia sesión para continuar con tu información profesional.")
            else:
                messages.success(request, "¡Tu cuenta ha sido creada! Por favor, inicia sesión.")

            return redirect('/Login/login')

    return render(request, 'Login/insertar.html')


def loginusuario(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username and password:
            usuario = authenticate(username=username, password=password)
            if usuario is not None:
                login(request, usuario)
                messages.success(request, "¡Bienvenido! Si eres mecánico, puedes actualizar tus datos personales en tu perfil.")
                return redirect('/')
            else:
                mensaje = "Usuario o Contraseña incorrectos, intente de nuevo"
                return render(request, 'Login/login.html', {'mensaje': mensaje})
    return render(request, 'Login/login.html')

def logoutusuario(request):
    logout(request)
    return redirect("/Login/login")

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            user = User.objects.filter(email=email).first()
            if user:
                subject = 'Restablecer Contraseña'
                message = 'Sigue este enlace para restablecer tu contraseña: http://yourwebsite.com/reset/{}/{}'.format(user.id, user.password)
                sender = 'your_email@example.com'
                recipient = [email]
                send_mail(subject, message, sender, recipient)
                messages.success(request, 'Se ha enviado un correo electrónico con instrucciones para restablecer tu contraseña.')
                return redirect('login')
            else:
                messages.error(request, 'No hay una cuenta asociada a este correo electrónico.')
        else:
            messages.error(request, 'Por favor, proporciona tu dirección de correo electrónico.')

    return render(request, 'Login/olvidaste_contraseña.html')
