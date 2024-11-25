from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthViewSet, ClienteViewSet, ProveedorViewSet, FacturaViewSet

router = DefaultRouter()
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'clientes', ClienteViewSet)
router.register(r'proveedores', ProveedorViewSet)
router.register(r'facturas', FacturaViewSet, basename='facturas')

urlpatterns = [
    path('', include(router.urls)),
]