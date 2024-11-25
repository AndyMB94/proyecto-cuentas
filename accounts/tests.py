from django.test import TestCase
from .models import Factura
from .tasks import check_facturas_vencimiento
from django.utils.timezone import now, timedelta

class FacturaTasksTestCase(TestCase):
    def setUp(self):
        today = now().date()
        self.factura_vencida = Factura.objects.create(
            numero_factura='001',
            fecha_vencimiento=today - timedelta(days=1),
            estado='Pendiente',
            tipo='Emitida',
        )
        self.factura_proxima = Factura.objects.create(
            numero_factura='002',
            fecha_vencimiento=today + timedelta(days=3),
            estado='Pendiente',
            tipo='Emitida',
            cliente_email='cliente@example.com'
        )
    
    def test_check_facturas_vencimiento(self):
        check_facturas_vencimiento()
        self.factura_vencida.refresh_from_db()
        self.assertEqual(self.factura_vencida.estado, 'Vencida')
