from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from mechanical_express.views import (
    confirmacion_pago, like_mecanico, pagos, planes, principal, report_mecanico, solicitar_servicio, contactenos, miperfil, 
    perfiles, configuracion, login, registrar, logoutusuario
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Páginas principales
    path('', principal, name='principal'),
    path('home/solicitar_servicio/', solicitar_servicio, name='solicitar_servicio'),
    path('home/contactenos/', contactenos, name='contactenos'),
    path('home/perfiles/<int:id>/', perfiles, name='perfiles'),
    path('mecanicos/like/<int:mecanico_id>/', like_mecanico, name='like_mecanico'),
    path('mecanicos/reportar/<int:id>/', report_mecanico, name='report_mecanico'),
    
    # Perfiles y configuración
    path('mecanicos/miperfil/<int:id>/', miperfil, name='miperfil'),
    path('mecanicos/planes/<int:id>/', planes, name='planes'),
    path('mecanicos/pagos/<int:id>/', pagos, name='pagos'),
    path('mecanicos/confirmacion_pago/<int:id>/', confirmacion_pago, name='confirmacion_pago'),



    path('usuarios/configuracion/<int:id>/', configuracion, name='configuracion'),
    
    # Registro, login y logout
    path('login/registrar/', registrar, name='registrar'),
    path('login/login/', login, name='login'),
    path('login/olvidaste_contrasena/', auth_views.PasswordResetView.as_view(), name='olvidaste_contrasena'),
    path('login/reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('login/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('login/reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='Login/password_reset_complete.html'), name='password_reset_complete'),
    path('login/salir/', logoutusuario, name='salir'),
]


