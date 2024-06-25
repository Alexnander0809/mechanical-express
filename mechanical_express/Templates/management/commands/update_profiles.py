# update_profiles.py

from django.core.management.base import BaseCommand
from mechanical_express.models import Profile, User  # Ajusta esto con la ruta correcta a tus modelos

class Command(BaseCommand):
    help = 'Crea perfiles para usuarios existentes y actualiza el campo tipo_usuario'

    def handle(self, *args, **kwargs):
        total_usuarios = User.objects.count()
        self.stdout.write(f'Número total de usuarios: {total_usuarios}')

        perfiles_creados = 0
        perfiles_actualizados = 0

        for user in User.objects.all():
            if not hasattr(user, 'profile'):
                Profile.objects.create(user=user)
                perfiles_creados += 1

        for profile in Profile.objects.filter(tipo_usuario__isnull=True):
            if profile.user.email.endswith('@mecanico.com'):
                profile.tipo_usuario = 'mecanico'
            else:
                profile.tipo_usuario = 'usuario'
            profile.save()
            perfiles_actualizados += 1

        self.stdout.write(f'Perfiles creados: {perfiles_creados}')
        self.stdout.write(f'Perfiles actualizados: {perfiles_actualizados}')
        self.stdout.write(self.style.SUCCESS('Proceso completado exitosamente'))
