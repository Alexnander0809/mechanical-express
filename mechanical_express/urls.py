from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from mechanical_express.views import (
    principal, solicitar_servicio, contactenos, miperfil, 
    perfiles, configuracion, loginusuario, insertarusuario, logoutusuario
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Páginas
    path('', principal, name='principal'),
    path('home/solicitar_servicio/', solicitar_servicio, name='solicitar_servicio'),
    path('home/contactenos/', contactenos, name='contactenos'),
    
    # Perfiles y configuración
    path('home/perfiles/<int:id>/', perfiles, name='perfiles'),
    path('usuarios/miperfil/<int:idmecanico>/', miperfil, name='miperfil'),
    path('usuarios/configuracion/', configuracion, name='configuracion'),
    
    # Registro, login y logout
    path('login/insertar/', insertarusuario, name='registro'),
    path('login/', loginusuario, name='login'),
    path('login/olvidaste_contrasena/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('login/reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('login/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('login/reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='Login/password_reset_complete.html'), name='password_reset_complete'),
    path('login/salir/', logoutusuario, name='salir'),
]
