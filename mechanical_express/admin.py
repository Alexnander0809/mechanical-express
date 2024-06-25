from django.contrib import admin
from .models import Usuario, Mecanico
from django.core.mail import send_mail

admin.site.register(Usuario)

class MecanicoAdmin(admin.ModelAdmin):
    def delete_model(self, request, obj):
        # Lógica para enviar el correo electrónico de notificación
        subject = 'Cuenta eliminada en Mechanical Express'
        message = f"Estimado usuario, su cuenta en Mechanical Express ha sido eliminada debido a acumulación de denuncias. Por favor, póngase en contacto con el soporte si tiene alguna pregunta."

        from_email = 'soportemechanicalexpress@email.com'
        to_emails = Mecanico.objects.values_list('email', flat=True)
        
        # Envío del correo electrónico de notificación
        send_mail(subject, message, from_email, to_emails)
        
        # Llama al método delete_model predeterminado para eliminar el objeto
        super().delete_model(request, obj)

# Registra tu modelo personalizado con el administrador de Django
admin.site.register(Mecanico, MecanicoAdmin)
