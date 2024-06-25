from django.contrib import admin
from .models import Usuario, Mecanico, Mantenimientos
from django.core.mail import send_mail

admin.site.register(Usuario)
admin.site.register(Mecanico)
admin.site.register(Mantenimientos)