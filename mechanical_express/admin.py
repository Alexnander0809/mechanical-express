from django.contrib import admin
from .models import Usuario, Mecanico, Mantenimientos, PerfilUsuario

admin.site.register(Usuario)
admin.site.register(Mecanico)
admin.site.register(Mantenimientos)
admin.site.register(PerfilUsuario)  # Agrega esta línea para registrar el modelo PerfilUsuario
