from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.db.models import Sum, Q
from datetime import datetime, timedelta
from .models import Cliente, Proveedor, Factura
from .serializers import (
    UserSerializer, LoginSerializer, ClienteSerializer,
    ProveedorSerializer, FacturaSerializer
)

User = get_user_model()

class AuthViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            try:
                user = User.objects.get(email=email)
                if user.check_password(password):
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        'token': str(refresh.access_token),
                        'user': UserSerializer(user).data
                    })
            except User.DoesNotExist:
                pass
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    permission_classes = [permissions.IsAuthenticated]

class FacturaViewSet(viewsets.ModelViewSet):
    serializer_class = FacturaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Factura.objects.all()
        estado = self.request.query_params.get('estado', None)
        tipo = self.request.query_params.get('tipo', None)
        
        if estado:
            queryset = queryset.filter(estado=estado)
        if tipo:
            queryset = queryset.filter(tipo=tipo)
            
        return queryset

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        today = datetime.now().date()
        thirty_days_ago = today - timedelta(days=30)
        
        # Total por cobrar y por pagar
        total_cobrar = Factura.objects.filter(
            tipo='Emitida',
            estado='Pendiente'
        ).aggregate(total=Sum('monto_total'))['total'] or 0

        total_pagar = Factura.objects.filter(
            tipo='Recibida',
            estado='Pendiente'
        ).aggregate(total=Sum('monto_total'))['total'] or 0

        # Facturas vencidas
        vencidas_cobrar = Factura.objects.filter(
            tipo='Emitida',
            estado='Vencida'
        ).aggregate(total=Sum('monto_total'))['total'] or 0

        # Próximos vencimientos (7 días)
        proximos_vencimientos = Factura.objects.filter(
            fecha_vencimiento__range=[today, today + timedelta(days=7)],
            estado='Pendiente'
        ).order_by('fecha_vencimiento')

        return Response({
            'total_por_cobrar': total_cobrar,
            'total_por_pagar': total_pagar,
            'vencidas_por_cobrar': vencidas_cobrar,
            'proximos_vencimientos': FacturaSerializer(
                proximos_vencimientos,
                many=True
            ).data
        })