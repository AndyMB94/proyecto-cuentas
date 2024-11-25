from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Cliente, Proveedor, Factura

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    nombre = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'nombre', 'rol')
        read_only_fields = ('id',)

    def get_nombre(self, obj):
        # Concatenar first_name y last_name para obtener el nombre completo
        return f"{obj.first_name} {obj.last_name}".strip()

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ('id', 'nombre', 'email', 'telefono')

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = ('id', 'nombre', 'email', 'telefono')

class FacturaSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.CharField(source='cliente.nombre', read_only=True)
    proveedor_nombre = serializers.CharField(source='proveedor.nombre', read_only=True)
    
    class Meta:
        model = Factura
        fields = (
            'id', 'numero_factura', 'cliente', 'proveedor',
            'cliente_nombre', 'proveedor_nombre', 'fecha_emision',
            'fecha_vencimiento', 'monto_total', 'estado', 'tipo'
        )
        read_only_fields = ('id',)