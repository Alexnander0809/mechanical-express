from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout     
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Like, Mecanico, Mantenimiento, Denuncia, UserProfile 

#region vistas principales

def principal(request):
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            if not user_profile.rol:
                return redirect('seleccion_rol', id=request.user.id)
            elif user_profile.rol == 'mecanico':
                print("Ta pasando algo x2")
                return render(request, 'Home/principal.html')
                
            else:
                print("Ta pasando algo")
                return render(request, 'Home/principal.html')
        except UserProfile.DoesNotExist:
            print("Ta pasando algo x3")
            return redirect('seleccion_rol', id=request.user.id)
    else:
        return render(request, 'Home/principal.html')

def solicitar_servicio(request):
    mecanicos = Mecanico.objects.filter(estado='Activo')
    paginator = Paginator(mecanicos, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'Home/solicitar_servicio.html', {
        'page_obj': page_obj,
    })

def contactenos(request):
    return render(request, "Home/contactenos.html")

def perfiles(request, id):
    mecanico = get_object_or_404(Mecanico, id=id)
    user = mecanico.user
    return render(request, "Home/perfiles.html", {'mecanico': mecanico, 'user': user})

@login_required
def like_mecanico(request, id):
    mecanico = get_object_or_404(Mecanico, id=id)

    # Verificar si el usuario ya le dio like al mecánico
    like, created = Like.objects.get_or_create(user=request.user, mecanico=mecanico)

    if created:
        mecanico.num_likes += 1
        mecanico.save()
        messages.success(request, 'Has dado un like al mecánico.')
    else:
        messages.info(request, 'Ya has dado un like a este mecánico.')

    return redirect('perfiles', id=id)

#endregion 

#region login

def insertarusuario(request):
    if request.method == 'POST':
        nombres = request.POST.get('nombres')
        apellidos = request.POST.get('apellidos')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')
        rol = 1

        if password != confirm_password:
            mensaje = "Las contraseñas no coinciden."
            return render(request, 'Login/insertar.html', {'mensaje': mensaje})

        if User.objects.filter(email=email).exists():
            mensaje = "El correo electrónico ya está registrado."
            return render(request, 'Login/insertar.html', {'mensaje': mensaje})

        usuario = User.objects.create_user(username=email, email=email, password=password)
        usuario.first_name = nombres
        usuario.last_name = apellidos
        usuario.user_profile = rol
        usuario.save()

        UserProfile.objects.create(user=usuario, user_profile=rol)

        messages.success(request, 'Usuario creado exitosamente. Ahora puedes iniciar sesión.')
        return redirect('login')

    return render(request, 'Login/insertar.html')

def loginusuario(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        rol = request.POST.get('rol')

        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            if rol == 'mecanico':
                return redirect('miperfil', id=user.id)
            else:
                return redirect('principal' )
        else:
            messages.error(request, 'Correo o contraseña incorrectos. Inténtalo de nuevo.')

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

#endregion 

#region vistas usuario y mecanico   

@login_required
def miperfil(request, id):
    mecanico = Mecanico.objects.filter(user_id=id).first()
    if not mecanico:
        messages.error(request, "No se encontró el perfil del mecánico.")
        return redirect('principal')

    if request.method == 'POST':
        if not request.POST.get("nombres") or not request.POST.get("apellidos"):
            messages.error(request, "Los campos de nombres y apellidos son obligatorios.")
            print("mi perfil 1")
            return redirect('miperfil', id=id)

        mecanico.foto = request.POST.get("foto")
        mecanico.telefono = request.POST.get("telefono")
        mecanico.direccion = request.POST.get('direccion')
        mecanico.ubicacion = request.POST.get('ubicacion')
        mecanico.descripcion = request.POST.get('descripcion')
        mecanico.profesion = request.POST.get("profesion")
        mecanico.save()

        messages.success(request, 'Perfil actualizado correctamente.')
        print("mi perfil 2")
        return redirect('miperfil', id=id)
    
    print("mi perfil 3")
    return render(request, "Mecanicos/miperfil.html", {'mecanico': mecanico})

def planes(request):
    return render(request, "Mecanicos/planes.html")

@login_required
def configuracion(request, id):
    if request.user.id != id:
        return redirect('principal')

    user = get_object_or_404(User, id=id)

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')

        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username
        user.save()

        messages.success(request, 'Tu información personal fue actualizada satisfactoriamente!!')
        return redirect('configuracion', id=id)
    
    return render(request, "Usuarios/configuracion.html", {'user': user})

#endregion

#region admin

def crear_mantenimiento(request):
    if request.method == 'POST':
        descripcion = request.POST.get('descripcion')
        fecha_programada = request.POST.get('fecha_programada')
        prioridad = request.POST.get('prioridad')
        estado = request.POST.get('estado')
        comentarios = request.POST.get('comentarios')
        
        Mantenimiento.objects.create(
            descripcion=descripcion,
            fecha_programada=fecha_programada,
            prioridad=prioridad,
            estado=estado,
            comentarios=comentarios
        )
        messages.success(request, 'El mantenimiento ha sido creado con éxito.')
        return redirect('lista_mantenimientos')

    return render(request, "Mantenimientos/crear_mantenimiento.html")

def lista_mantenimientos(request):
    mantenimientos = Mantenimiento.objects.all()
    return render(request, "Mantenimientos/lista_mantenimientos.html", {'mantenimientos': mantenimientos})

#endregion

@login_required
def report_mecanico(request, id):
    if request.method == 'POST':
        mecanico = get_object_or_404(Mecanico, id=id)
        tipo_denuncia = request.POST.get('tipo_denuncia')
        descripcion = request.POST.get('descripcion')

        # Verificar si el usuario ya ha denunciado a este mecánico
        denuncia_existente = Denuncia.objects.filter(user=request.user, mecanico=mecanico).exists()

        if denuncia_existente:
            messages.error(request, 'Ya has denunciado a este mecánico anteriormente. No puedes enviar una nueva denuncia.')
        else:
            # Crear una nueva denuncia
            Denuncia.objects.create(
                user=request.user,
                mecanico=mecanico,
                tipo_denuncia=tipo_denuncia,
                descripcion=descripcion
            )

            # Añadir un mensaje de éxito
            messages.success(request, 'Tu denuncia ha sido enviada. La revisaremos en las próximas horas.')

        # Redirigir a la página de detalles del mecánico después de hacer la denuncia o si ya ha sido denunciado
        return redirect('perfiles', id=id)

    return redirect('perfiles', id=id)