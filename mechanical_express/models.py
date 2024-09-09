from datetime import timedelta, timezone
from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail

class Pago(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Relación con la tabla de usuarios
    name = models.CharField(max_length=255)  # Nombre del propietario de la cuenta
    cardnumber = models.CharField(max_length=19)  # Número de tarjeta (formato 1234 5678 1234 5678)
    expirationdate = models.CharField(max_length=5)  # Fecha de expiración en formato MM/AA
    securitycode = models.CharField(max_length=4)  # Código de seguridad de 3 o 4 dígitos
    description = models.CharField(max_length=255, default="PLAN MECANICO PREMIUM")  # Descripción del plan
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=15000.00)  # Monto del pago en COP
    date = models.DateTimeField(auto_now_add=True)  # Fecha y hora del pago

    def __str__(self):
        return f"Pago de {self.name} - {self.amount} COP"
    class Meta:
        db_table = "pago"

class Mecanico(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    foto = models.CharField(max_length=150)
    telefono = models.CharField(max_length=10, null=True, blank=True)
    direccion = models.CharField(max_length=150, null=True, blank=True)
    ubicacion = models.CharField(max_length=150, null=True, blank=True)
    descripcion = models.CharField(max_length=300, null=True, blank=True)
    num_likes = models.PositiveIntegerField(default=0)
    tipo_afiliacion = models.CharField(max_length=150, null=True, blank=True)
    profesion = models.CharField(max_length=300, null=True, blank=True)
    estado = models.CharField(max_length=20, null=True, blank=True)

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
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En Proceso'),
        ('completado', 'Completado'),
    ]

    PRIORIDAD_CHOICES = [
        ('alta', 'Alta'),
        ('media', 'Media'),
        ('baja', 'Baja'),
    ]

    descripcion = models.CharField(max_length=255)
    fecha_programada = models.DateField()
    prioridad = models.CharField(max_length=20, choices=PRIORIDAD_CHOICES)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    comentarios = models.TextField(blank=True)

    def __str__(self):
        return f'{self.descripcion} - {self.estado}'

    def esta_proximo(self):
        # Verifica si el mantenimiento está próximo a realizarse (dentro de 7 días)
        return self.fecha_programada <= timezone.now().date() + timedelta(days=7)

    def enviar_alerta(self):
        # Método para enviar alerta por email
        subject = 'Alerta de Mantenimiento Programado'
        message = f'El mantenimiento "{self.descripcion}" está programado para el {self.fecha_programada}.'
        recipient_list = [user.email for user in User.objects.all()]  # Enviar a todos los usuarios
        send_mail(subject, message, 'from@example.com', recipient_list)
        
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


