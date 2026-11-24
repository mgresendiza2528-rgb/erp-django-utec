import logging
from decimal import Decimal, InvalidOperation

from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models import DecimalField, ExpressionWrapper, F, Sum
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone

logger = logging.getLogger(__name__)


def _url_absoluta(nombre_url: str) -> str:
    return f'{settings.SITE_URL}{reverse(nombre_url)}'


def _items_con_subtotal(items_snapshot: list) -> list:
    items = []
    for item in items_snapshot or []:
        try:
            precio = Decimal(str(item.get('precio', '0')))
            cantidad = int(item.get('cantidad', 0))
        except (InvalidOperation, TypeError, ValueError):
            precio, cantidad = Decimal('0.00'), 0
        items.append({
            **item,
            'precio': precio.quantize(Decimal('0.01')),
            'cantidad': cantidad,
            'subtotal': (precio * cantidad).quantize(Decimal('0.01')),
        })
    return items


@shared_task(
    bind=True,
    max_retries=3,
    default_retry_delay=60,
    name='ventas.enviar_confirmacion_pedido',
)
def enviar_confirmacion_pedido(self, pedido_id: int) -> dict:
    from configuracion.models import ConfiguracionERP
    from ventas.models import Pedido

    try:
        pedido = Pedido.objects.select_related('cliente').get(pk=pedido_id)
    except Pedido.DoesNotExist:
        logger.error(f'[correo_confirmacion] Pedido {pedido_id} no existe.')
        return {'estado': 'error', 'pedido_id': pedido_id, 'razon': 'Pedido no encontrado'}

    if pedido.correo_enviado:
        logger.info(f'[correo_confirmacion] Pedido {pedido.numero_pedido}: ya enviado — skip.')
        return {'estado': 'skip', 'pedido_id': pedido_id, 'razon': 'correo ya enviado'}

    config = ConfiguracionERP.get_instance()
    contexto = {
        'pedido': pedido,
        'config': config,
        'items': _items_con_subtotal(pedido.items_snapshot),
        'url_tienda': _url_absoluta('catalogo:catalogo'),
    }
    asunto = f'Confirmación de pedido {pedido.numero_pedido} — {config.nombre_empresa}'
    msg = EmailMultiAlternatives(
        subject=asunto,
        body=render_to_string('emails/confirmacion_pedido.txt', contexto),
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[pedido.cliente.correo],
    )
    msg.attach_alternative(render_to_string('emails/confirmacion_pedido.html', contexto), 'text/html')

    try:
        msg.send()
    except Exception as exc:
        logger.error(f'[correo_confirmacion] Error en pedido {pedido.numero_pedido}: {exc}')
        raise self.retry(exc=exc, countdown=60 * (self.request.retries + 1))

    Pedido.objects.filter(pk=pedido.pk).update(correo_enviado=True)
    return {'estado': 'ok', 'pedido_id': pedido_id, 'correo': pedido.cliente.correo}


@shared_task(
    bind=True,
    max_retries=1,
    name='ventas.verificar_stock_bajo',
)
def verificar_stock_bajo(self, umbral: int = 5) -> dict:
    from configuracion.models import ConfiguracionERP
    from productos.models import Producto

    productos_bajos = list(
        Producto.objects.filter(activo=True, stock__lt=umbral)
        .values('pk', 'nombre', 'stock', 'categoria__nombre')
        .order_by('stock')
    )
    if not productos_bajos:
        return {'umbral': umbral, 'total': 0, 'productos_bajos': [], 'alerta_enviada': False}

    alerta_enviada = False
    if settings.ADMINS:
        config = ConfiguracionERP.get_instance()
        contexto = {
            'productos_bajos': productos_bajos,
            'total_productos': len(productos_bajos),
            'umbral': umbral,
            'fecha': timezone.localtime().strftime('%d/%m/%Y %H:%M'),
            'url_admin': _url_absoluta('admin:productos_producto_changelist'),
            'config': config,
        }
        msg = EmailMultiAlternatives(
            subject=f'[ALERTA] {len(productos_bajos)} producto(s) con stock menor a {umbral}',
            body=render_to_string('emails/alerta_stock.txt', contexto),
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.ADMINS[0][1]],
        )
        msg.attach_alternative(render_to_string('emails/alerta_stock.html', contexto), 'text/html')
        try:
            msg.send()
            alerta_enviada = True
        except Exception as exc:
            logger.error(f'[stock_bajo] Error: {exc}')

    return {
        'umbral': umbral,
        'total': len(productos_bajos),
        'productos_bajos': productos_bajos,
        'alerta_enviada': alerta_enviada,
    }


@shared_task(
    bind=True,
    max_retries=2,
    name='ventas.reporte_ventas_diario',
)
def reporte_ventas_diario(self) -> dict:
    from configuracion.models import ConfiguracionERP
    from ventas.models import DetalleVenta, Pedido

    hoy = timezone.localdate()
    config = ConfiguracionERP.get_instance()
    pedidos_hoy = Pedido.objects.filter(fecha_pedido__date=hoy, estado='pagado')
    total_pedidos = pedidos_hoy.count()
    total_facturado = pedidos_hoy.aggregate(total=Sum('total_pagado'))['total'] or Decimal('0.00')

    acumulado = {}
    internas = (
        DetalleVenta.objects.filter(venta__fecha__date=hoy)
        .values(nombre=F('producto__nombre'))
        .annotate(
            unidades=Sum('cantidad'),
            ingreso=Sum(
                ExpressionWrapper(
                    F('cantidad') * F('precio_unitario'),
                    output_field=DecimalField(max_digits=12, decimal_places=2),
                )
            ),
        )
    )
    for fila in internas:
        d = acumulado.setdefault(fila['nombre'], {'unidades': 0, 'ingreso': Decimal('0.00')})
        d['unidades'] += fila['unidades'] or 0
        d['ingreso'] += fila['ingreso'] or Decimal('0.00')

    for pedido in pedidos_hoy.only('items_snapshot'):
        for item in _items_con_subtotal(pedido.items_snapshot):
            d = acumulado.setdefault(
                item.get('nombre', '¿?'),
                {'unidades': 0, 'ingreso': Decimal('0.00')},
            )
            d['unidades'] += item['cantidad']
            d['ingreso'] += item['subtotal']

    top_productos = sorted(
        (
            {
                'nombre': nombre,
                'unidades': d['unidades'],
                'ingreso': str(d['ingreso'].quantize(Decimal('0.01'))),
            }
            for nombre, d in acumulado.items()
        ),
        key=lambda x: Decimal(x['ingreso']),
        reverse=True,
    )[:5]

    if settings.ADMINS:
        contexto = {
            'fecha': hoy.strftime('%d/%m/%Y'),
            'config': config,
            'total_pedidos': total_pedidos,
            'total_facturado': total_facturado,
            'top_productos': top_productos,
            'url_admin': _url_absoluta('admin:ventas_pedido_changelist'),
            'hora_programada': settings.REPORTE_DIARIO_HORA,
        }
        msg = EmailMultiAlternatives(
            subject=f'Reporte de ventas del {hoy.strftime("%d/%m/%Y")} — {config.nombre_empresa}',
            body=render_to_string('emails/reporte_ventas.txt', contexto),
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.ADMINS[0][1]],
        )
        msg.attach_alternative(render_to_string('emails/reporte_ventas.html', contexto), 'text/html')
        try:
            msg.send()
        except Exception as exc:
            logger.error(f'[reporte_diario] Error: {exc}')

    return {
        'fecha': str(hoy),
        'total_pedidos': total_pedidos,
        'total_facturado': str(total_facturado),
        'top_productos': top_productos,
    }