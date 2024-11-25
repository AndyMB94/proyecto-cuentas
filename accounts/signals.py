from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Factura

@receiver(pre_save, sender=Factura)
def update_factura_status(sender, instance, **kwargs):
    if instance.estado == 'Pendiente':
        today = timezone.now().date()
        if instance.fecha_vencimiento < today:
            instance.estado = 'Vencida'