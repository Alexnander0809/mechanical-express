from django.contrib import admin
from django.urls import path
from mechanical_express.views import principal, solicitar_servicio, contactenos, miperfil, perfiles, configuracion, loginusuario, insertarusuario, logoutusuario

urlpatterns = [
    path('admin/', admin.site.urls),

    # Paginas
    path('', principal, name='principal'),
    path('Home/solicitar_servicio/', solicitar_servicio, name='solicitar_servicio'),
    path('Home/contactenos/', contactenos, name='contactenos'),
    
    # perfiles y configuración
    path('Home/perfiles/<int:id>', perfiles, name='perfiles'),
    path('Home/miperfil/', miperfil, name='miperfil'),
    path('Home/configuracion/', configuracion, name='configuracion'),
    
    # Registro, login y logout
    path('Login/insertar/',  insertarusuario, name='registro'),
    path('Login/login/', loginusuario, name='login'),
    path('Login/salir/', logoutusuario, name='salir'),
]
