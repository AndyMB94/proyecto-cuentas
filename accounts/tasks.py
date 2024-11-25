from background_task import background
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime, timedelta
from django.utils.timezone import now
from .models import Factura
import logging


logger = logging.getLogger(__name__)

def actualizar_facturas_vencidas(today):

    vencidas = Factura.objects.filter(
        fecha_vencimiento=today,
        estado='Pendiente'
    )
    vencidas.update(estado='Vencida')

def enviar_notificaciones(proximas):

    for factura in proximas:
        try:
           
            if factura.tipo == 'Emitida' and factura.cliente and factura.cliente.email:
                send_mail(
                    'Factura próxima a vencer',
                    f'Estimado cliente, la factura {factura.numero_factura} vencerá en 3 días.',
                    settings.DEFAULT_FROM_EMAIL,
                    [factura.cliente.email],
                    fail_silently=False,
                )
        
            elif factura.tipo == 'Recibida' and factura.proveedor and factura.proveedor.email:
                send_mail(
                    'Factura próxima a vencer',
                    f'Estimado proveedor, la factura {factura.numero_factura} vencerá en 3 días.',
                    settings.DEFAULT_FROM_EMAIL,
                    [factura.proveedor.email],
                    fail_silently=False,
                )
        except Exception as e:
            logger.error(f"Error al enviar email para factura {factura.numero_factura}: {e}")

@background(schedule=60*60*24)  # Ejecutar diariamente
def check_facturas_vencimiento():

    today = now().date()
    tres_dias = today + timedelta(days=3)

    actualizar_facturas_vencidas(today)
    proximas = Factura.objects.filter(
        fecha_vencimiento=tres_dias,
        estado='Pendiente'
    ).only('numero_factura', 'tipo', 'cliente__email', 'proveedor__email')

    enviar_notificaciones(proximas)
