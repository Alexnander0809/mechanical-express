from django.db import models
from django.contrib.auth.models import User

class Usuario(models.Model):
    nombres = models.CharField(max_length=150)
    apellidos = models.CharField(max_length=150)
    telefono = models.CharField(max_length=20)
    email = models.CharField(max_length=150)
    contraseña = models.CharField(max_length=30)
    class Meta:
        db_table = "usuario"

class Mecanico(models.Model):
    foto = models.CharField(max_length=150)
    nombres = models.CharField(max_length=150)
    apellidos = models.CharField(max_length=150)
    telefono = models.CharField(max_length=20)
    email = models.CharField(max_length=150)
    contraseña = models.CharField(max_length=30)
    direccion = models.CharField(max_length=150)
    ubicacion = models.CharField(max_length=150)
    descripcion = models.CharField(max_length=300)
    num_likes = models.CharField(max_length=11)
    tipo_afiliacion = models.CharField(max_length=150)
    profesion = models.CharField(max_length=300)
    estado = models.CharField(max_length=20)
    class Meta:
        db_table = "mecanico"



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    certificacion = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.username