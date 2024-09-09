from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout     
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Like, Mecanico, Mantenimiento, Denuncia, Pago
from django.contrib.auth.hashers import check_password
import re
from django.contrib.auth.models import AnonymousUser

#region vistas principales

def principal(request):
    is_mechanic = request.session.get('is_mechanic', False)
    
    # Verificar si es el primer acceso
    primer_acceso = request.session.get('primer_acceso', True)
    request.session['primer_acceso'] = False  # Marcar que el usuario ya ha visto el aviso
    
    # Obtener los mantenimientos más recientes si el aviso es necesario
    mantenimientos = Mantenimiento.objects.all() if primer_acceso else []

    return render(request, 'Home/principal.html', {
        'is_mechanic': is_mechanic,
        'primer_acceso': primer_acceso,
        'mantenimientos': mantenimientos,
    })

def solicitar_servicio(request):
    filtro = request.GET.get('filtro', 'todos')

    # Filtrar solo los mecánicos con estado "Activo"
    if filtro == 'premium':
        mecanicos = Mecanico.objects.filter(tipo_afiliacion='premium', estado='Activo')
    elif filtro == 'regulares':
        mecanicos = Mecanico.objects.exclude(tipo_afiliacion='premium').filter(estado='Activo')
    else:
        mecanicos = Mecanico.objects.filter(estado='Activo')

    mecanicos = mecanicos.order_by('-id')

    paginator = Paginator(mecanicos, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'Home/solicitar_servicio.html', {
        'page_obj': page_obj,
        'filtro': filtro
    })

def contactenos(request):
    return render(request, "Home/contactenos.html")

def perfiles(request, id):
    mecanico = get_object_or_404(Mecanico, id=id)
    mecanico_user = mecanico.user  # Usuario relacionado con el mecánico
    current_user = request.user  # Usuario actual de la sesión

    is_authenticated = current_user.is_authenticated
    is_own_profile = is_authenticated and current_user.id == mecanico_user.id

    return render(request, "Home/perfiles.html", {
        'mecanico': mecanico,
        'mecanico_user': mecanico_user,  # Cambié el nombre para evitar confusión
        'current_user': current_user,  # Usuario de la sesión actual
        'is_own_profile': is_own_profile
    })

@login_required
def like_mecanico(request, mecanico_id):
    mecanico = get_object_or_404(Mecanico, id=mecanico_id)
    user = request.user

    existing_like = Like.objects.filter(user=user, mecanico=mecanico).first()

    if existing_like:
        # Si ya existe un like, lo eliminamos y restamos uno
        existing_like.delete()
        mecanico.num_likes = max(0, mecanico.num_likes - 1)  # Asegurarse que no haya valores negativos
        messages.info(request, "Has quitado tu like.")
    else:
        # Si no existe un like, creamos uno nuevo y sumamos uno
        Like.objects.create(user=user, mecanico=mecanico)
        mecanico.num_likes = mecanico.num_likes + 1
        messages.success(request, "Has dado like.")

    mecanico.save()
    
    # Redirige a la vista perfiles, pasando el ID del mecánico
    return redirect('perfiles', id=mecanico_id)

#endregion 

#region login

def insertarusuario(request):
    if request.method == 'POST':
        nombres = request.POST.get('nombres')
        apellidos = request.POST.get('apellidos')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')

        # Verificación de formato de email
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            mensaje = "El formato del correo electrónico no es válido."
            return render(request, 'Login/insertar.html', {'mensaje': mensaje})

        if password != confirm_password:
            mensaje = "Las contraseñas no coinciden."
            return render(request, 'Login/insertar.html', {'mensaje': mensaje})

        if User.objects.filter(email=email).exists():
            mensaje = "El correo electrónico ya está registrado."
            return render(request, 'Login/insertar.html', {'mensaje': mensaje})

        # Crear el usuario
        usuario = User.objects.create_user(username=email, email=email, password=password)
        usuario.first_name = nombres
        usuario.last_name = apellidos
        usuario.save()

        # Crear un perfil de Mecanico asociado al usuario recién creado
        Mecanico.objects.create(
            user=usuario,
            foto=None,
            telefono='',
            direccion='',
            ubicacion='',
            descripcion='',
            num_likes=0,
            tipo_afiliacion='Regular',
            profesion='',
            estado='Inactivo'  # Cambia el estado inicial a "Inactivo"
        )


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

            # Verificar si el usuario es mecánico
            if rol == 'mecanico':
                mecanico = Mecanico.objects.filter(user=user).first()

                if mecanico:
                    request.session['is_mechanic'] = True

                    # Activar el mecánico si su estado es "Inactivo"
                    if mecanico.estado == 'Inactivo':
                        mecanico.estado = 'Activo'
                        mecanico.save()
                else:
                    request.session['is_mechanic'] = False
            else:
                request.session['is_mechanic'] = False

            # Redirigir según el rol
            if rol == 'mecanico' and request.session['is_mechanic']:
                return redirect('miperfil', id=user.id)
            elif rol == 'usuario':
                return redirect('principal')
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
    # Obtener el objeto Mecanico basado en el user_id
    mecanico = Mecanico.objects.filter(user_id=id).first()

    # Obtener el objeto User basado en el user_id
    user = User.objects.filter(id=id).first()

    if request.method == 'POST':
        # Verificar campos obligatorios: nombres y apellidos
        if not request.POST.get("nombres") or not request.POST.get("apellidos"):
            messages.error(request, "Los campos de nombres y apellidos son obligatorios.")
            return redirect('miperfil', id=id)

        # Actualizar la información del mecánico
        if request.FILES.get("foto"):
            mecanico.foto = request.FILES.get("foto")
            imagen = FileSystemStorage()
            imagen.save(mecanico.foto.name, mecanico.foto)
        mecanico.nombres = request.POST.get("nombres")
        mecanico.apellidos = request.POST.get("apellidos")
        mecanico.telefono = request.POST.get("telefono")
        mecanico.direccion = request.POST.get('direccion')
        mecanico.ubicacion = request.POST.get('ubicacion')
        mecanico.descripcion = request.POST.get('descripcion')
        mecanico.profesion = request.POST.get('profesion')
        mecanico.save()

        messages.success(request, "Perfil actualizado con éxito.")
        return redirect('miperfil', id=id)

    # Incluir tanto el mecánico como el usuario en el contexto
    context = {
        'mec': [mecanico],
        'user': user,
        'is_premium': mecanico.tipo_afiliacion == 'premium'  # Asumiendo que el campo tipo_afiliacion indica el tipo de plan
    }
    return render(request, 'Mecanicos/miperfil.html', context)

@login_required
def planes(request, id):
    try:
        user = User.objects.get(id=id)
        mecanico = Mecanico.objects.get(user=user)  # Suponiendo que hay una relación entre User y Mecanico
        is_mechanic = True
    except (User.DoesNotExist, Mecanico.DoesNotExist):
        user = None
        mecanico = None
        is_mechanic = False
    
    return render(request, "Mecanicos/planes.html", {
        'user': user,
        'mecanico': mecanico,
        'is_mechanic': is_mechanic
    })


@login_required
def pagos(request, id):
    try:
        user = User.objects.get(id=id)
        mecanico = Mecanico.objects.get(user=user)
    except User.DoesNotExist:
        return HttpResponseNotFound("Usuario no encontrado.")
    except Mecanico.DoesNotExist:
        return HttpResponseNotFound("Mecánico no encontrado.")
    
    if request.method == 'POST':
        nombre = request.POST.get('name')
        cardnumber = request.POST.get('cardnumber')
        expirationdate = request.POST.get('expirationdate')
        securitycode = request.POST.get('securitycode')

        # Simulación de procesamiento de pago
        success = True  # Simulamos que el pago fue exitoso
        
        if success:
            # Guardar información relevante
            Pago.objects.create(
                user=user,
                name=nombre,
                cardnumber=cardnumber,
                expirationdate=expirationdate,
                securitycode=securitycode,
                description='PLAN MECANICO PREMIUM',
                amount=15000,
            )
            # Actualizar la afiliación del mecánico a 'premium'
            mecanico.tipo_afiliacion = 'premium'
            mecanico.save()
            
            # Establecer una variable en la sesión para indicar el pago realizado
            request.session['payment_success'] = True
            
            # Redirige a la página de confirmación de pago con el id del usuario
            return redirect('confirmacion_pago', id=user.id)
        
        else:
            return render(request, "Mecanicos/pagos.html", {
                'user': user,
                'user_id': id,
                'error_message': 'Error en el procesamiento del pago. Inténtalo de nuevo.'
            })

    return render(request, "Mecanicos/pagos.html", {'user': user, 'user_id': id})


@login_required
def confirmacion_pago(request, id):
    try:
        user = User.objects.get(id=id)
        if not request.session.get('payment_success', False):
            # Si la variable de sesión no está establecida, redirige al usuario a la página de pago
            return redirect('pagos', id=user.id)
        
        # Limpiar la variable de sesión después de mostrar la confirmación
        request.session.pop('payment_success', None)
    
    except User.DoesNotExist:
        return HttpResponseNotFound("Usuario no encontrado.")
    
    return render(request, 'Mecanicos/confirmacion_pago.html', {
        'user': user,
        'message': "¡Gracias por tu compra!",
        'plan_description': "Has adquirido el Plan Mecánico Premium.",
        'benefits': [
            "Atención prioritaria en soporte técnico.",
            "Acceso a descuentos exclusivos en repuestos.",
            "Estadísticas detalladas sobre tu rendimiento como mecánico.",
            "Y mucho más."
        ]
    })

@login_required
def configuracion(request, id):
    if request.user.id != id:
        return redirect('principal')

    user = get_object_or_404(User, id=id)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'Actualizar Información':
            # Actualizar información personal
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

        elif action == 'Eliminar mi cuenta':
            # Eliminar cuenta
            password = request.POST.get('password')
            if check_password(password, user.password):
                user.delete()
                messages.success(request, 'Tu cuenta ha sido eliminada.')
                return redirect('principal')
            else:
                messages.error(request, 'La contraseña ingresada es incorrecta.')

    return render(request, "Usuarios/configuracion.html", {'user': user})

#endregion

#region admin

def crear_mantenimiento(request):
    if request.method == 'POST':
        # Aquí se crearían y guardarían los datos del mantenimiento
        mantenimiento = Mantenimiento(
            descripcion=request.POST['descripcion'],
            fecha_programada=request.POST['fecha_programada'],
            prioridad=request.POST['prioridad'],
            estado=request.POST['estado'],
            comentarios=request.POST['comentarios']
        )
        mantenimiento.save()
        
        # Enviar alerta si el mantenimiento está próximo
        if mantenimiento.esta_proximo():
            mantenimiento.enviar_alerta()

        return redirect('success_url')  # Redirige a una página de éxito
    return render(request, 'crear_mantenimiento.html')

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
    