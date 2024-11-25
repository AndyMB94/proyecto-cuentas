from django.test import TestCase
from .models import Factura, Cliente, Usuario
from .tasks import check_facturas_vencimiento
from django.utils.timezone import now, timedelta

class FacturaTasksTestCase(TestCase):
    def setUp(self):
        today = now().date()
        
        # Crear un cliente de prueba
        self.cliente = Cliente.objects.create(
            nombre="Cliente de Prueba",
            email="cliente@example.com",
            telefono="123456789"
        )
        
        # Crear un usuario de prueba
        self.usuario = Usuario.objects.create_user(
            username="usuario_prueba",
            email="usuario@example.com",
            password="password123",
            rol="Administrador"
        )
        
        # Crear una factura vencida
        self.factura_vencida = Factura.objects.create(
            numero_factura='001',
            fecha_emision=today - timedelta(days=30),  # Fecha de emisión válida
            fecha_vencimiento=today - timedelta(days=1),
            monto_total=100.00,  # Monto total válido
            estado='Pendiente',
            tipo='Emitida',
            cliente=self.cliente,
            usuario=self.usuario
        )
        
        # Crear una factura próxima a vencer
        self.factura_proxima = Factura.objects.create(
            numero_factura='002',
            fecha_emision=today - timedelta(days=27),  # Fecha de emisión válida
            fecha_vencimiento=today + timedelta(days=3),
            monto_total=200.00,  # Monto total válido
            estado='Pendiente',
            tipo='Emitida',
            cliente=self.cliente,
            usuario=self.usuario
        )
    
    def test_check_facturas_vencimiento(self):
        # Ejecutar la tarea para verificar vencimientos
        check_facturas_vencimiento()
        
        # Actualizar la instancia de la factura vencida desde la base de datos
        self.factura_vencida.refresh_from_db()
        
        # Verificar que el estado de la factura vencida haya cambiado a 'Vencida'
        self.assertEqual(self.factura_vencida.estado, 'Vencida')
