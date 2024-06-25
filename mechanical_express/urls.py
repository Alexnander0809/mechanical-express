from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from mechanical_express.views import (
    principal, solicitar_servicio, contactenos, miperfil, 
    perfiles, configuracion, loginusuario, insertarusuario, logoutusuario
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Paginas
    path('', principal, name='principal'),
    path('Home/solicitar_servicio/', solicitar_servicio, name='solicitar_servicio'),
    path('Home/contactenos/', contactenos, name='contactenos'),
    
    # Perfiles y configuración
    path('Home/perfiles/<int:id>/', perfiles, name='perfiles'),
    path('Usuarios/miperfil/<int:idmecanico>', miperfil, name='miperfil'),
    path('Usuarios/configuracion/', configuracion, name='configuracion'),
    
    # Registro, login y logout
    path('Login/insertar/', insertarusuario, name='registro'),
    path('Login/login/', loginusuario, name='login'),
    path('Login/olvidaste_contraseña/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('Login/reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('Login/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('Login/reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='Login/password_reset_complete.html'), name='password_reset_complete'),
    path('Login/salir/', logoutusuario, name='salir')
]
