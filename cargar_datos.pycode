from decimal import Decimal

from clientes.models import Cliente
from productos.models import Categoria, Producto
from proveedores.models import Proveedor
from ventas.models import DetalleVenta, Venta

cat, _ = Categoria.objects.get_or_create(nombre='Electrónica')

prov1, _ = Proveedor.objects.get_or_create(
    correo='ventas@techmx.com', defaults={'nombre': 'Tech MX'})
prov2, _ = Proveedor.objects.get_or_create(
    correo='contacto@distnorte.com', defaults={'nombre': 'Distribuidora Norte'})

cli1, _ = Cliente.objects.get_or_create(
    correo='juan@utec.com', defaults={'nombre': 'Juan Pérez'})
cli2, _ = Cliente.objects.get_or_create(
    correo='ana@utec.com', defaults={'nombre': 'Ana García'})

prod1, _ = Producto.objects.get_or_create(
    nombre='Laptop HP',
    defaults={'precio': Decimal('12500.00'), 'stock': 5,
              'categoria': cat, 'proveedor': prov1})
prod2, _ = Producto.objects.get_or_create(
    nombre='Mouse inalámbrico',
    defaults={'precio': Decimal('250.00'), 'stock': 20,
              'categoria': cat, 'proveedor': prov2})

if not Venta.objects.filter(cliente=cli1).exists():
    venta = Venta.objects.create(cliente=cli1)
    DetalleVenta.objects.create(
        venta=venta, producto=prod1, cantidad=1,
        precio_unitario=Decimal('12500.00'))
    DetalleVenta.objects.create(
        venta=venta, producto=prod2, cantidad=2,
        precio_unitario=Decimal('250.00'))

print('Productos:', Producto.objects.count())
print('Clientes:', Cliente.objects.count())
print('Proveedores:', Proveedor.objects.count())
print('Ventas:', Venta.objects.count())