from decimal import Decimal
from unittest.mock import patch

import stripe
from django.test import TestCase
from django.urls import reverse

from clientes.models import Cliente
from productos.models import Categoria, Producto
from ventas.models import Pedido

CONSTRUCT = 'catalogo.webhook_views.stripe.Webhook.construct_event'


def _evento(tipo, pedido_id):
    return {'type': tipo, 'data': {'object': {
        'id': f'pi_test_{pedido_id}',
        'metadata': {'pedido_id': str(pedido_id)},
    }}}


class WebhookTest(TestCase):

    def setUp(self):
        cat = Categoria.objects.create(nombre='Cat')
        self.prod = Producto.objects.create(
            nombre='P', precio=Decimal('500.00'), stock=10, categoria=cat)
        cli = Cliente.objects.create(nombre='C', correo='c@t.com')
        self.pedido = Pedido.objects.create(
            numero_pedido='PED-2025-TEST', cliente=cli, estado='pendiente',
            total_pagado=Decimal('1000.00'),
            items_snapshot=[{'producto_id': self.prod.pk, 'nombre': 'P',
                             'cantidad': 2, 'precio': '500.00'}])

    def _post(self):
        return self.client.post(
            reverse('catalogo:webhook'), data=b'{}',
            content_type='application/json',
            HTTP_STRIPE_SIGNATURE='t=123,v1=ok')

    def test_get_rechazado_con_405(self):
        r = self.client.get(reverse('catalogo:webhook'))
        self.assertEqual(r.status_code, 405)

    @patch(CONSTRUCT)
    def test_firma_invalida_devuelve_400(self, mock_c):
        mock_c.side_effect = stripe.SignatureVerificationError('x', 'sig')
        self.assertEqual(self._post().status_code, 400)

    @patch(CONSTRUCT)
    def test_payload_invalido_devuelve_400(self, mock_c):
        mock_c.side_effect = ValueError('JSON invalido')
        self.assertEqual(self._post().status_code, 400)

    @patch(CONSTRUCT)
    def test_payment_succeeded_actualiza_estado(self, mock_c):
        mock_c.return_value = _evento('payment_intent.succeeded', self.pedido.pk)
        self.assertEqual(self._post().status_code, 200)
        self.pedido.refresh_from_db()
        self.assertEqual(self.pedido.estado, 'pagado')

    @patch(CONSTRUCT)
    def test_payment_succeeded_descuenta_stock(self, mock_c):
        mock_c.return_value = _evento('payment_intent.succeeded', self.pedido.pk)
        self._post()
        self.prod.refresh_from_db()
        self.assertEqual(self.prod.stock, 8)

    @patch(CONSTRUCT)
    def test_payment_succeeded_idempotente(self, mock_c):
        mock_c.return_value = _evento('payment_intent.succeeded', self.pedido.pk)
        self._post()
        self._post()
        self.prod.refresh_from_db()
        self.assertEqual(self.prod.stock, 8)

    @patch(CONSTRUCT)
    def test_payment_failed_cancela_pedido(self, mock_c):
        mock_c.return_value = _evento('payment_intent.payment_failed', self.pedido.pk)
        self.assertEqual(self._post().status_code, 200)
        self.pedido.refresh_from_db()
        self.assertEqual(self.pedido.estado, 'cancelado')

    @patch(CONSTRUCT)
    def test_evento_stripe_object_real(self, mock_c):
        datos = _evento('payment_intent.succeeded', self.pedido.pk)
        datos['data']['object']['object'] = 'payment_intent'
        datos.update({'id': 'evt_test', 'object': 'event'})
        mock_c.return_value = stripe.Event.construct_from(datos, 'sk_test')
        self.assertEqual(self._post().status_code, 200)
        self.pedido.refresh_from_db()
        self.prod.refresh_from_db()
        self.assertEqual(self.pedido.estado, 'pagado')
        self.assertEqual(self.prod.stock, 8)
