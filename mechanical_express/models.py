from django.db import models
from django.contrib.auth.models import User

class Mecanico(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    foto = models.ImageField(upload_to='fotos_mecanicos/', blank=True, null=True)
    telefono = models.CharField(max_length=10)
    direccion = models.CharField(max_length=150)
    ubicacion = models.CharField(max_length=150)
    descripcion = models.CharField(max_length=300)
    num_likes = models.IntegerField(default=0)
    tipo_afiliacion = models.CharField(max_length=150)
    profesion = models.CharField(max_length=300)
    estado = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.user.username} - {self.profesion}'

    class Meta:
        db_table = "mecanico"
        
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mecanico = models.ForeignKey(Mecanico, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'mecanico')
        db_table = "likes"

class Mantenimiento(models.Model):
    descripcion = models.CharField(max_length=255)
    fecha_programada = models.DateField()
    prioridad = models.CharField(max_length=20)
    estado = models.CharField(max_length=20)
    comentarios = models.TextField()

    def __str__(self):
        return f'{self.descripcion} - {self.estado}'

    class Meta:
        db_table = "mantenimientos"

class Denuncia(models.Model):   
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mecanico = models.ForeignKey(Mecanico, on_delete=models.CASCADE)
    tipo_denuncia = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=255) 

    def __str__(self):
        return f'{self.tipo_denuncia} - {self.mecanico.user.username}'     

    class Meta:
        db_table = "denuncia"

class UserProfile(models.Model):
    rol = models.CharField(max_length=20)
    class Meta: 
        db_table = 'userprofile'
