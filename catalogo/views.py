from decimal import Decimal

import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView

from productos.models import Producto
from ventas.models import Pedido

from .checkout_utils import (
    armar_items,
    calcular_totales,
    generar_numero_pedido,
    obtener_o_crear_cliente,
)
from .filters import ProductoFilter

stripe.api_key = settings.STRIPE_SECRET_KEY


class CatalogoView(ListView):
    model = Producto
    template_name = 'catalogo/catalogo.html'
    context_object_name = 'productos'
    paginate_by = 12

    def get_queryset(self):
        qs = Producto.objects.select_related('categoria').filter(activo=True).order_by('nombre')
        self.filtro = ProductoFilter(self.request.GET, queryset=qs)
        return self.filtro.qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['filtro'] = self.filtro
        return ctx


def _obtener_carrito(request):
    return request.session.get('carrito', {})


def _guardar_carrito(request, carrito):
    request.session['carrito'] = carrito
    request.session.modified = True


def ver_carrito(request):
    items = []
    total = Decimal('0.00')
    for prod_id, d in _obtener_carrito(request).items():
        precio = Decimal(d['precio'])
        cantidad = int(d['cantidad'])
        subtotal = precio * cantidad
        total += subtotal
        items.append({'prod_id': prod_id, 'nombre': d['nombre'], 'precio': precio,
                      'cantidad': cantidad, 'subtotal': subtotal, 'imagen': d.get('imagen')})
    return render(request, 'catalogo/carrito.html', {'items': items, 'total': total})


def agregar_al_carrito(request, producto_id):
    if request.method != 'POST':
        return redirect('catalogo:catalogo')
    producto = get_object_or_404(Producto, pk=producto_id, activo=True)
    carrito = _obtener_carrito(request)
    clave = str(producto_id)
    cantidad = int(request.POST.get('cantidad', 1))
    if clave in carrito:
        carrito[clave]['cantidad'] += cantidad
    else:
        carrito[clave] = {'nombre': producto.nombre, 'precio': str(producto.precio),
                          'cantidad': cantidad,
                          'imagen': producto.imagen.name if producto.imagen else None}
    _guardar_carrito(request, carrito)
    messages.success(request, f'"{producto.nombre}" agregado al carrito.')
    return redirect(request.POST.get('next') or 'catalogo:catalogo')


def remover_del_carrito(request, producto_id):
    if request.method != 'POST':
        return redirect('catalogo:carrito')
    carrito = _obtener_carrito(request)
    carrito.pop(str(producto_id), None)
    _guardar_carrito(request, carrito)
    return redirect('catalogo:carrito')


def actualizar_cantidad(request, producto_id):
    if request.method != 'POST':
        return redirect('catalogo:carrito')
    carrito = _obtener_carrito(request)
    clave = str(producto_id)
    cantidad = int(request.POST.get('cantidad', 1))
    if clave in carrito:
        if cantidad > 0:
            carrito[clave]['cantidad'] = cantidad
        else:
            carrito.pop(clave)
    _guardar_carrito(request, carrito)
    return redirect('catalogo:carrito')


def vaciar_carrito(request):
    if request.method == 'POST':
        _guardar_carrito(request, {})
    return redirect('catalogo:carrito')


@login_required
def checkout(request):
    carrito = _obtener_carrito(request)
    if not carrito:
        messages.warning(request, 'Tu carrito está vacío.')
        return redirect('catalogo:catalogo')

    totales = calcular_totales(carrito)
    items = armar_items(carrito)
    publishable_key = settings.STRIPE_PUBLISHABLE_KEY

    if request.method == 'POST':
        try:
            cliente = obtener_o_crear_cliente(request.user)
            pedido = Pedido.objects.create(
                numero_pedido=generar_numero_pedido(),
                cliente=cliente,
                estado='pendiente',
                total_pagado=totales['total'],
            )
            intent = stripe.PaymentIntent.create(
                amount=int(totales['total'] * 100),
                currency='mxn',
                metadata={
                    'pedido_id': pedido.pk,
                    'pedido_num': pedido.numero_pedido,
                    'cliente': cliente.nombre,
                },
                idempotency_key=f'pedido-{pedido.pk}',
            )
            return render(request, 'catalogo/checkout.html', {
                'carrito': carrito,
                'items': items,
                'totales': totales,
                'pedido': pedido,
                'client_secret': intent.client_secret,
                'publishable_key': publishable_key,
            })
        except stripe.StripeError as exc:
            detalle = getattr(exc, 'user_message', None) or str(exc)
            messages.error(request, f'Error al conectar con Stripe: {detalle}')
            return redirect('catalogo:pago_error')
        except Exception as exc:
            messages.error(request, f'Error inesperado en el pago: {exc}')
            return redirect('catalogo:pago_error')

    return render(request, 'catalogo/checkout.html', {
        'carrito': carrito,
        'items': items,
        'totales': totales,
        'client_secret': None,
        'publishable_key': publishable_key,
    })


def pago_exitoso(request, pedido_id):
    pedido = get_object_or_404(Pedido, pk=pedido_id)
    _guardar_carrito(request, {})
    messages.success(
        request,
        f'¡Pago exitoso! Tu pedido {pedido.numero_pedido} está confirmado. '
        f'Total: ${pedido.total_pagado}'
    )
    return render(request, 'catalogo/pago_exitoso.html', {'pedido': pedido})


def pago_error(request):
    return render(request, 'catalogo/pago_error.html')