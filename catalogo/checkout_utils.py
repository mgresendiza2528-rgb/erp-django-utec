from datetime import date
from decimal import Decimal, ROUND_HALF_UP

from clientes.models import Cliente
from configuracion.models import ConfiguracionERP
from ventas.models import Pedido

CENTAVOS = Decimal('0.01')


def calcular_totales(carrito):
    config = ConfiguracionERP.get_instance()
    iva_porcentaje = Decimal(str(config.iva_porcentaje))
    subtotal = sum(
        (Decimal(str(d['precio'])) * int(d['cantidad'])
         for d in carrito.values()),
        Decimal('0'),
    ).quantize(CENTAVOS, rounding=ROUND_HALF_UP)
    iva_monto = (subtotal * iva_porcentaje / Decimal('100')).quantize(
        CENTAVOS, rounding=ROUND_HALF_UP
    )
    return {
        'subtotal': subtotal,
        'iva_pct': iva_porcentaje,
        'iva_monto': iva_monto,
        'total': subtotal + iva_monto,
    }


def armar_items(carrito):
    items = []
    for d in carrito.values():
        precio = Decimal(str(d['precio']))
        cantidad = int(d['cantidad'])
        items.append({
            'nombre': d['nombre'],
            'precio': precio,
            'cantidad': cantidad,
            'subtotal': precio * cantidad,
        })
    return items


def obtener_o_crear_cliente(user):
    correo = user.email or f'{user.username}@erp.local'
    nombre = user.get_full_name() or user.username
    cliente, _ = Cliente.objects.get_or_create(
        correo=correo,
        defaults={'nombre': nombre, 'activo': True},
    )
    if user.get_full_name() and cliente.nombre != nombre:
        cliente.nombre = nombre
        cliente.save(update_fields=['nombre'])
    return cliente


def generar_numero_pedido():
    prefijo = f'PED-{date.today().year}-'
    ultimo = (
        Pedido.objects.filter(numero_pedido__startswith=prefijo)
        .order_by('-numero_pedido')
        .values_list('numero_pedido', flat=True)
        .first()
    )
    siguiente = int(ultimo.split('-')[-1]) + 1 if ultimo else 1
    return f'{prefijo}{siguiente:04d}'