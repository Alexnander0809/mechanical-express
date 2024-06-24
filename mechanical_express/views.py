from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Mecanico, Usuario

from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth import login, authenticate, logout

#region principal

def principal(request):
    return render(request, "Home/principal.html")

def solicitar_servicio(request):
    mecanico = Mecanico.objects.filter(estado='Activo')
    return render(request, "Home/solicitar_servicio.html", {
        'mecanico':mecanico
        }
    )

def contactenos(request):
    return render(request, "Home/contactenos.html")

def perfiles(request, id):
    mecanico = Mecanico.objects.filter(id=id)
    
    return render(request, "Home/perfiles.html", {
        'mecanico':mecanico
        })
    
def miperfil(request):
    
    return render(request, "Home/miperfil.html")

def configuracion(request):
    return render(request, "Home/configuracion.html")

#endregion

#region usuario

def insertarusuario(request):
    if request.method == "POST":
        role = request.POST.get("role")
        nombres = request.POST.get("nombres")
        apellidos = request.POST.get("apellidos")
        telefono = request.POST.get("telefono")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Verificar si el correo electrónico ya está en uso
        if User.objects.filter(email=email).exists():
            messages.error(request, "El correo electrónico ya está en uso.")
            return render(request, 'Login/insertar.html')

        # Verificar que todos los campos requeridos estén presentes
        if role and nombres and apellidos and password and email:
            # Crear un usuario regular
            usuario = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=nombres,
                last_name=apellidos
            )

            # Guardar el usuario en la base de datos
            usuario.save()

            # Crear un perfil de usuario
            usuario_db = Usuario.objects.create(
                nombres=nombres,
                apellidos=apellidos,
                telefono=telefono,
                email=email,
                contraseña=password
            )

            if role == "mecanico":
                # Si el rol es mecánico, crear un perfil de mecánico
                foto = request.POST.get("foto")
                direccion = request.POST.get("direccion")
                ubicacion = request.POST.get("ubicacion")
                descripcion = request.POST.get("descripcion")
                num_likes = request.POST.get("num_likes")
                tipo_afiliacion = request.POST.get("tipo_afiliacion")
                tipo_servicio = request.POST.get("tipo_servicio")
                certificados = request.POST.get("certificados")
                estado = request.POST.get("estado")
                
                mecanico = Mecanico.objects.create(
                    foto=foto,
                    nombres=nombres,
                    apellidos=apellidos,
                    telefono=telefono,
                    email=email,
                    contraseña=password,
                    direccion=direccion,
                    ubicacion=ubicacion,
                    descripcion=descripcion,
                    num_likes=num_likes,
                    tipo_afiliacion=tipo_afiliacion,
                    tipo_servicio=tipo_servicio,
                    certificados=certificados,
                    estado=estado
                )

            # Redirigir al usuario a la página de inicio de sesión
            return redirect('/Login/login')

    # Si la solicitud no es POST, renderiza el formulario nuevamente
    return render(request, 'Login/insertar.html')

    
def loginusuario(request):
    if request.method=="POST":
        if request.POST.get("username") and request.POST.get("password"):
            usuario = authenticate(username=request.POST.get("username"), password=request.POST.get("password"))
            if usuario is not None:
                login(request, usuario)
                return redirect('/')
            else:
                mensaje = "Usuario o Contraseña incorrectos, intente de nuevo"
                return render(request, 'Login/login.html', {
                    'mensaje':mensaje
                })
    
    return render(request, 'Login/login.html') 

def logoutusuario(request):
    logout(request)
    return redirect("/Login/login")

#endregion