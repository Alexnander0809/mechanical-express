from django.contrib import admin
from .models import Mecanico, Mantenimiento, Denuncia

@admin.register(Mecanico)
class MecanicoAdmin(admin.ModelAdmin):
    list_display = ('user', 'profesion', 'estado')
    search_fields = ('user__username', 'profesion')

@admin.register(Mantenimiento)
class MantenimientoAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'fecha_programada', 'prioridad', 'estado')
    list_filter = ('prioridad', 'estado')
    search_fields = ('descripcion', 'comentarios')

@admin.register(Denuncia)
class DenunciaAdmin(admin.ModelAdmin):
    list_display = ('user', 'mecanico', 'tipo_denuncia')
    search_fields = ('descripcion', 'tipo_denuncia')
