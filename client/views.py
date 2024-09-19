from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login 
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.contrib.auth import  authenticate, login as auth_login     
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import CustomerUser, Like, Mecanico, Mantenimiento, Denuncia, Pago, Rol
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist

#region vistas principales

def principal(request):
    if request.user.is_authenticated:
        rol_usuario = request.user.rol.id if request.user.rol else None
    else:
        rol_usuario = None  # Usuario no autenticado

    return render(request, 'Home/principal.html', {'rol_usuario': rol_usuario})

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
    # Obtener el perfil del mecánico a partir del id
    mecanico = get_object_or_404(Mecanico, id=id)
    mecanico_user = mecanico.user  # Usuario asociado al mecánico
    current_user = request.user  # Usuario actual autenticado

    # Verificación de autenticación
    if not current_user.is_authenticated:
        messages.warning(request, "Debes iniciar sesión para interactuar.")
        return redirect('login')

    # Verificación de si el usuario está viendo su propio perfil
    is_own_profile = current_user.id == mecanico_user.id

    # Obtener el rol del usuario actual
    user_rol = getattr(current_user, 'rol', None)
    is_current_user_mechanic = user_rol and user_rol.nombre == 'Mecanico'

    # Condiciones para permitir dar like o reportar
    can_like = not is_own_profile and not is_current_user_mechanic
    can_report = not is_own_profile and user_rol and user_rol.nombre == 'Usuario'

    # Verificar si ya se ha reportado o dado like
    has_reported = Denuncia.objects.filter(user=current_user, mecanico=mecanico).exists() if can_report else False
    has_liked = Like.objects.filter(user=current_user, mecanico=mecanico).exists() if can_like else False

    # Limitar a una denuncia por usuario
    if Denuncia.objects.filter(user=current_user).count() >= 1:
        can_report = False

    # Renderizar la vista con las variables de contexto
    return render(request, "Home/perfiles.html", {
        'mecanico': mecanico,
        'mecanico_user': mecanico_user,
        'current_user': current_user,
        'is_own_profile': is_own_profile,
        'is_current_user_mechanic': is_current_user_mechanic,
        'can_like': can_like and not has_liked,
        'can_report': can_report and not has_reported,
        'has_liked': has_liked
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

def registrar(request):
    if request.method == "POST":
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()
        rol_id = request.POST.get('rol', '').strip()

        # Validaciones básicas
        if not email or not password or not confirm_password or not rol_id:
            messages.error(request, "Todos los campos son obligatorios y no pueden estar vacíos o contener solo espacios.")
        elif password != confirm_password:
            messages.error(request, "Las contraseñas no coinciden.")
        else:
            # Verificar si el correo electrónico ya está registrado
            if CustomerUser.objects.filter(email=email).exists():
                messages.error(request, "El correo electrónico ya está registrado.")
            else:
                try:
                    # Crear el usuario
                    user = CustomerUser.objects.create_user(
                        username=email,
                        email=email,
                        password=password
                    )

                    # Asignar el rol
                    try:
                        rol = Rol.objects.get(id=rol_id)
                        user.rol = rol
                        user.save()

                        if rol.id == 2:  # Si el rol es mecánico
                            tipo_afiliacion = "Regular"
                            estado = "Inactivo"
                            Mecanico.objects.create(tipo_afiliacion=tipo_afiliacion, estado=estado, user=user)

                        messages.success(request, "Usuario registrado exitosamente.")
                        auth_login(request, user)  # Iniciar sesión automáticamente

                        # Redirigir según el rol
                        return redirect('login')  # O redirigir a una vista de usuario normal

                    except Rol.DoesNotExist:
                        messages.error(request, "El rol especificado no existe.")
                        
                except Exception as e:
                    messages.error(request, f"Ocurrió un error: {str(e)}")

    # Manejar GET request
    roles = Rol.objects.all()
    return render(request, 'Login/registrar.html', {'roles': roles})

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        # Validación de campos vacíos
        if not email or not password:
            messages.error(request, 'Ambos campos son obligatorios y no pueden estar vacíos.')
            return render(request, 'Login/login.html')

        # Autenticación del usuario por email usando el backend personalizado
        user = authenticate(request, username=email, password=password)

        if user is not None:
            auth_login(request, user)

            # Verificar si el usuario es superusuario
            if user.is_superuser:
                return redirect('/admin/')

            # Redirigir según el rol del usuario
            if user.rol_id == 2:
                return redirect('miperfil', id=user.id)
            elif user.rol_id == 1:
                return redirect('principal')
            else:
                messages.error(request, 'Rol no reconocido.')
                return redirect('login')

        else:
            messages.error(request, 'Credenciales incorrectas.')

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
    user = request.user

    if user.id != id:
        messages.error(request, "No tienes permiso para acceder a este perfil.")
        return redirect('principal')

    try:
        mecanico = user.mecanico
    except ObjectDoesNotExist:
        mecanico = None

    if request.method == 'POST':
        nombres = request.POST.get("nombres")
        apellidos = request.POST.get("apellidos")
        telefono = request.POST.get("telefono")
        direccion = request.POST.get('direccion')
        ubicacion = request.POST.get('ubicacion')
        descripcion = request.POST.get('descripcion')
        profesion = request.POST.get('profesion')
        foto = request.FILES.get("foto")

        try:
            # Actualizar datos del CustomUser
            if nombres:
                user.first_name = nombres
            if apellidos:
                user.last_name = apellidos
            user.save()

            # Actualizar datos del Mecanico
            if mecanico:
                if foto:
                    imagen = FileSystemStorage()
                    filename = imagen.save(foto.name, foto)
                    mecanico.foto = filename

                mecanico.telefono = telefono or mecanico.telefono
                mecanico.direccion = direccion or mecanico.direccion
                mecanico.ubicacion = ubicacion or mecanico.ubicacion
                mecanico.descripcion = descripcion or mecanico.descripcion
                mecanico.profesion = profesion or mecanico.profesion

                if mecanico.estado == 'Inactivo':
                    mecanico.estado = 'Activo'

                mecanico.save()
                
                messages.success(request, "Perfil actualizado con éxito.")
            else:
                messages.error(request, "No se encontró el perfil del mecánico.")
                
        except Exception as e:
            messages.error(request, f"Error al actualizar el perfil: {e}")

        return redirect('miperfil', id=id)

    context = {
        'user': user,
        'mec': mecanico,
        'is_premium': mecanico.tipo_afiliacion == 'premium' if mecanico else False
    }

    return render(request, 'mecanicos/miperfil.html', context)


@login_required
def planes(request, id):
    try:
        user = CustomerUser.objects.get(id=id)  # Usa CustomerUser en lugar de User
        mecanico = Mecanico.objects.get(user=user)  # Suponiendo que hay una relación entre CustomerUser y Mecanico
        is_mechanic = True
    except (CustomerUser.DoesNotExist, Mecanico.DoesNotExist):
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
        user = CustomerUser.objects.get(id=id)
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
        user = CustomerUser.objects.get(id=id)
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
    # Asegurarse de que el usuario actual es el propietario de la cuenta
    if request.user.id != id:
        return redirect('principal')

    user = get_object_or_404(CustomerUser, id=id)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'Actualizar Información':
            # Limpiar espacios en los campos
            first_name = request.POST.get('first_name', '').strip()
            last_name = request.POST.get('last_name', '').strip()
            email = request.POST.get('email', '').strip()
            username = request.POST.get('username', '').strip()

            # Actualizar los datos del usuario con los valores limpios
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
def report_mecanico(request, mecanico_id):
    mecanico = get_object_or_404(Mecanico, id=mecanico_id)
    user = request.user

    # Verificar si el usuario ya ha realizado una denuncia
    if Denuncia.objects.filter(user=user, mecanico=mecanico).exists():
        messages.warning(request, "Ya has realizado una denuncia sobre este mecánico.")
        return redirect('perfiles', id=mecanico_id)

    if request.method == 'POST':
        tipo_denuncia = request.POST.get('tipo_denuncia')
        descripcion = request.POST.get('descripcion')

        # Crear una nueva denuncia
        Denuncia.objects.create(
            user=user,
            mecanico=mecanico,
            tipo_denuncia=tipo_denuncia,
            descripcion=descripcion
        )
        messages.success(request, "Tu denuncia ha sido enviada.")

    return redirect('perfiles', id=mecanico_id)