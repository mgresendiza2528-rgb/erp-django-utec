import logging

import stripe
from django.conf import settings
from django.db.models import F
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from productos.models import Producto
from ventas.models import Pedido

logger = logging.getLogger(__name__)


@csrf_exempt
@require_POST
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')
    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=sig_header,
            secret=settings.STRIPE_WEBHOOK_SECRET,
        )
    except ValueError:
        logger.warning('Webhook: payload invalido.')
        return HttpResponse('Payload invalido.', status=400)
    except stripe.SignatureVerificationError:
        logger.warning('Webhook: firma invalida.')
        return HttpResponse('Firma invalida.', status=400)

    # stripe >= 15 devuelve StripeObject (no es dict): convertir
    if hasattr(event, 'to_dict'):
        event = event.to_dict()

    tipo = event['type']
    logger.info('Webhook recibido: %s', tipo)
    if tipo == 'payment_intent.succeeded':
        _manejar_pago_exitoso(event['data']['object'])
    elif tipo == 'payment_intent.payment_failed':
        _manejar_pago_fallido(event['data']['object'])
    return HttpResponse(status=200)


def _extraer_pedido_id(payment_intent):
    pedido_id = (payment_intent.get('metadata') or {}).get('pedido_id')
    if not pedido_id:
        logger.warning('Webhook: PaymentIntent sin pedido_id.')
        return None
    try:
        return int(pedido_id)
    except (ValueError, TypeError):
        logger.error('Webhook: pedido_id invalido: %r', pedido_id)
        return None


def _manejar_pago_exitoso(payment_intent):
    pedido_id = _extraer_pedido_id(payment_intent)
    if pedido_id is None:
        return
    try:
        pedido = Pedido.objects.get(pk=pedido_id)
    except Pedido.DoesNotExist:
        logger.error('Webhook: Pedido %s no encontrado.', pedido_id)
        return
    if pedido.estado == 'pagado':
        return  # idempotente: no descontar dos veces
    pedido.estado = 'pagado'
    pedido.save(update_fields=['estado'])
    _descontar_stock(pedido)
    try:
        from ventas.tasks import enviar_confirmacion_pedido
        enviar_confirmacion_pedido.delay(pedido.pk)
    except Exception:
        logger.exception('Webhook: no se pudo encolar el correo del pedido %s.', pedido.pk)


def _manejar_pago_fallido(payment_intent):
    pedido_id = _extraer_pedido_id(payment_intent)
    if pedido_id is None:
        return
    pedido = Pedido.objects.filter(pk=pedido_id).first()
    if pedido and pedido.estado == 'pendiente':
        pedido.estado = 'cancelado'
        pedido.save(update_fields=['estado'])


def _descontar_stock(pedido):
    for item in pedido.items_snapshot or []:
        producto_id = item.get('producto_id')
        cantidad = int(item.get('cantidad', 0))
        if not producto_id or cantidad <= 0:
            continue
        filas = Producto.objects.filter(
            pk=producto_id, stock__gte=cantidad
        ).update(stock=F('stock') - cantidad)
        if not filas:
            logger.warning('Producto %s: stock insuficiente para %s.',
                           producto_id, cantidad)
