from django.contrib import admin
from .models import Usuario, Mecanico

admin.site.register(Usuario),
admin.site.register(Mecanico)

class TuModeloAdmin(admin.ModelAdmin):
    def delete_model(self, request, obj):
        # Aquí puedes personalizar la lógica para enviar el correo electrónico de notificación
        subject = 'Objeto eliminado: {}'.format(obj.__class__.__name__)
        message = 'Se ha eliminado el objeto {} con ID {}'.format(obj.__class__.__name__, obj.id)
        from_email = 'tu@email.com'
        to_emails = ['destinatario1@email.com', 'destinatario2@email.com']
        
        # Envía el correo electrónico de notificación
        send_mail(subject, message, from_email, to_emails)
        
        # Llama al método delete_model predeterminado para eliminar el objeto
        super(TuModeloAdmin, self).delete_model(request, obj)

# Registra tu modelo personalizado con el administrador de Django
admin.site.register(TuModelo, TuModeloAdmin)