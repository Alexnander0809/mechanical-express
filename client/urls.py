from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    confirmacion_pago, like_mecanico, pagos, planes, principal, report_mecanico, solicitar_servicio, contactenos, miperfil, 
    perfiles, configuracion, login, registrar, logoutusuario
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Páginas principales
    path('', principal, name='principal'),
    path('Home/solicitar_servicio/', solicitar_servicio, name='solicitar_servicio'),
    path('Home/contactenos/', contactenos, name='contactenos'),
    path('Home/perfiles/<int:id>/', perfiles, name='perfiles'),
    path('Home/like/<int:mecanico_id>/', like_mecanico, name='like_mecanico'),
    path('Home/reportar/<int:id>/', report_mecanico, name='report_mecanico'),
    
    # Perfiles y configuración
    path('Mecanicos/miperfil/<int:id>/', miperfil, name='miperfil'),
    path('Mecanicos/planes/<int:id>/', planes, name='planes'),
    path('Mecanicos/pagos/<int:id>/', pagos, name='pagos'),
    path('Mecanicos/confirmacion_pago/<int:id>/', confirmacion_pago, name='confirmacion_pago'),

    path('usuarios/configuracion/<int:id>/', configuracion, name='configuracion'),
    
    # Registro, login y logout
    path('login/registrar/', registrar, name='registrar'),
    path('login/', login, name='login'),
    path('login/olvidaste_contrasena/', auth_views.PasswordResetView.as_view(), name='olvidaste_contrasena'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='Login/password_reset_complete.html'), name='password_reset_complete'), 
    path('salir/', logoutusuario, name='salir'),
]


