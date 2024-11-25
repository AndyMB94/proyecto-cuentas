from django.contrib import admin
from .models import Usuario, Cliente, Proveedor, Factura

# Registra los modelos para que aparezcan en el panel de administración
admin.site.register(Usuario)
admin.site.register(Cliente)
admin.site.register(Proveedor)
admin.site.register(Factura)
