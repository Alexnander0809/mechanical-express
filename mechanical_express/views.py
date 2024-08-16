from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Mecanico, PerfilUsuario, Usuario
from django.core.mail import send_mail
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

@login_required
def principal(request):
    # Verificar si el usuario es mecánico basado en rol_id
    is_mechanic = hasattr(request.user, 'perfilusuario') and request.user.perfilusuario.rol_id == 1

    context = {
        'is_mechanic': is_mechanic,
    }
    return render(request, 'Home/principal.html', context)

def solicitar_servicio(request):
    mecanicos = Mecanico.objects.filter(estado='Activo')
    return render(request, "Home/solicitar_servicio.html", {'mecanicos': mecanicos})

def contactenos(request):
    return render(request, "Home/contactenos.html")

def perfiles(request, id):
    mecanico = get_object_or_404(Mecanico, id=id)
    return render(request, "Home/perfiles.html", {'mecanico': mecanico})

@login_required
def miperfil(request):
    # Obtener el perfil del mecánico
    mecanico = get_object_or_404(Mecanico, user=request.user)

    if request.method == 'POST':
        mecanico.foto = request.POST.get("foto")
        mecanico.nombres = request.POST.get("nombres")
        mecanico.apellidos = request.POST.get("apellidos")
        mecanico.telefono = request.POST.get("telefono")
        mecanico.email = request.POST.get("email")
        mecanico.direccion = request.POST.get('direccion')
        mecanico.ubicacion = request.POST.get('ubicacion')
        mecanico.descripcion = request.POST.get('descripcion')
        mecanico.profesion = request.POST.get("profesion")
        mecanico.save()

        messages.success(request, 'Perfil actualizado correctamente.')
        return redirect('miperfil')

    return render(request, "Usuarios/miperfil.html", {'mecanico': mecanico})

def configuracion(request):
    user = request.user
    is_mechanic = hasattr(user, 'perfilusuario') and user.perfilusuario.rol_id == 1
    return render(request, "Usuarios/configuracion.html", {'is_mechanic': is_mechanic})

def planes(request):
    return render(request, "Mecanicos/planes.html")

def insertarusuario(request):
    if request.method == "POST":
        role = request.POST.get("role")
        nombres = request.POST.get("nombres")
        apellidos = request.POST.get("apellidos")
        telefono = request.POST.get("telefono")
        email = request.POST.get("email")
        password = request.POST.get("password")
        profesion = request.POST.get("profesion") if role == "mecanico" else None

        if User.objects.filter(email=email).exists():
            messages.error(request, "El correo electrónico ya está en uso.")
            return render(request, 'Login/insertar.html')

        if role and nombres and apellidos and password and email:
            usuario = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=nombres,
                last_name=apellidos
            )

            if role == "mecanico":
                mecanico = Mecanico.objects.create(
                    user=usuario,
                    nombres=nombres,
                    apellidos=apellidos,
                    telefono=telefono,
                    email=email,
                    profesion=profesion,
                    estado='Activo'
                )
                messages.success(request, "¡Cuenta de mecánico creada con éxito!")
            else:
                PerfilUsuario.objects.create(
                    user=usuario,
                    rol_id=2  # Rol para usuarios comunes
                )
                messages.success(request, "¡Cuenta creada con éxito!")

            return redirect('login')

    return render(request, 'Login/insertar.html')

def loginusuario(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username and password:
            usuario = authenticate(username=username, password=password)
            if usuario is not None:
                login(request, usuario)
                
                # Verificar el rol del usuario basado en rol_id
                perfil_usuario = PerfilUsuario.objects.get(user=usuario)
                if perfil_usuario.rol_id == 1:  # Si es mecánico
                    return redirect('ruta_para_mecanicos')
                else:
                    return redirect('ruta_para_usuarios')
            else:
                messages.error(request, "Usuario o contraseña incorrectos.")
    return render(request, 'Login/login.html')

def logoutusuario(request):
    logout(request)
    return redirect('login')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            user = User.objects.filter(email=email).first()
            if user:
                subject = 'Restablecer Contraseña'
                message = f'Sigue este enlace para restablecer tu contraseña: http://yourwebsite.com/reset/{user.id}/{user.password}'
                sender = 'your_email@example.com'
                send_mail(subject, message, sender, [email])
                messages.success(request, 'Se ha enviado un correo electrónico con instrucciones para restablecer tu contraseña.')
            else:
                messages.error(request, 'No hay una cuenta asociada a este correo electrónico.')
        else:
            messages.error(request, 'Por favor, proporciona tu dirección de correo electrónico.')

    return render(request, 'Login/olvidaste_contraseña.html')
