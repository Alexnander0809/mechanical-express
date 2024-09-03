from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from mechanical_express.views import (
    like_mecanico, principal, report_mecanico, solicitar_servicio, contactenos, miperfil, 
    perfiles, configuracion, loginusuario, insertarusuario, logoutusuario
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Páginas principales
    path('', principal, name='principal'),
    # path('home/seleccion_rol/<int:id>/', seleccion_rol, name='seleccion_rol'),  # Añadí la barra "/" al final de la ruta
    path('home/solicitar_servicio/', solicitar_servicio, name='solicitar_servicio'),
    path('home/contactenos/', contactenos, name='contactenos'),
    path('home/perfiles/<int:id>/', perfiles, name='perfiles'),
    path('mecanicos/like/<int:id>/', like_mecanico, name='like_mecanico'),
    path('mecanicos/reportar/<int:id>/', report_mecanico, name='report_mecanico'),
    
    # Perfiles y configuración
    path('mecanicos/miperfil/<int:id>/', miperfil, name='miperfil'),
    path('usuarios/configuracion/<int:id>/', configuracion, name='configuracion'),
    
    # Registro, login y logout
    path('login/insertar/', insertarusuario, name='registro'),
    path('login/', loginusuario, name='login'),
    path('login/olvidaste_contrasena/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('login/reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('login/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('login/reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='Login/password_reset_complete.html'), name='password_reset_complete'),
    path('login/salir/', logoutusuario, name='salir'),
]
