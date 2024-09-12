from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Mecanico, Mantenimiento, Denuncia, Rol

admin.site.register(Rol)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'rol')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'rol')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'rol'),
        }),
    )
    search_fields = ('username',)
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)

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
