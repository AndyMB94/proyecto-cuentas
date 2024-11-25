from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class Usuario(AbstractUser):
    ROL_CHOICES = [
        ('Administrador', 'Administrador'),
        ('Contador', 'Contador'),
        ('Gerente', 'Gerente'),
    ]
    
    rol = models.CharField(max_length=20, choices=ROL_CHOICES)
    email = models.EmailField(unique=True)

    
    groups = models.ManyToManyField(
        Group,
        related_name='usuarios', 
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='usuarios_permissions',  
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'rol']

    def __str__(self):
        return self.email 

class Cliente(models.Model):
    nombre = models.CharField(max_length=200)
    email = models.EmailField(unique=True, null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.nombre

class Proveedor(models.Model):
    nombre = models.CharField(max_length=200)
    email = models.EmailField(unique=True, null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.nombre

class Factura(models.Model):
    ESTADO_CHOICES = [
        ('Pagada', 'Pagada'),
        ('Pendiente', 'Pendiente'),
        ('Vencida', 'Vencida'),
    ]
    
    TIPO_CHOICES = [
        ('Emitida', 'Emitida'),
        ('Recibida', 'Recibida'),
    ]

    numero_factura = models.CharField(max_length=50, unique=True)
    cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.SET_NULL)
    proveedor = models.ForeignKey(Proveedor, null=True, blank=True, on_delete=models.SET_NULL)
    fecha_emision = models.DateField()
    fecha_vencimiento = models.DateField()
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=['cliente']),
            models.Index(fields=['proveedor']),
            models.Index(fields=['estado']),
            models.Index(fields=['fecha_vencimiento']),
            models.Index(fields=['usuario']),
        ]

    def __str__(self):
        return f"{self.numero_factura} - {self.get_tipo_display()}"