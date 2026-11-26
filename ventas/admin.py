# ventas/admin.py
from django.contrib import admin, messages

from .models import DetalleVenta, Pedido, Venta
from .tasks import enviar_confirmacion_pedido


class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 1


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'fecha')
    inlines = [DetalleVentaInline]


@admin.action(description="Enviar correo de confirmación (pagados sin correo)")
def enviar_correo_confirmacion(modeladmin, request, queryset):
    pendientes = queryset.filter(estado='pagado', correo_enviado=False)
    enviados = 0
    for pedido in pendientes:
        try:
            enviar_confirmacion_pedido.delay(pedido.pk)
            enviados += 1
        except Exception as exc:
            messages.error(
                request,
                f"No se pudo encolar {pedido.numero_pedido}: {exc}",
            )
    omitidos = queryset.count() - pendientes.count()
    if enviados:
        messages.success(request, f"{enviados} correo(s) en cola.")
    if omitidos:
        messages.warning(
            request,
            f"{omitidos} pedido(s) omitidos (no pagados o ya con correo enviado).",
        )


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('numero_pedido', 'cliente', 'estado', 'total_pagado', 'correo_enviado')
    list_filter = ('estado', 'correo_enviado')
    search_fields = ('numero_pedido',)
    actions = [enviar_correo_confirmacion]
    from django.contrib import messages as _messages
from .tasks import enviar_confirmacion_pedido


@admin.action(description="Enviar correo de confirmación (pagados sin correo)")
def enviar_correo_confirmacion(modeladmin, request, queryset):
    n = 0
    for pedido in queryset.filter(estado='pagado', correo_enviado=False):
        enviar_confirmacion_pedido.delay(pedido.pk)
        n += 1
    _messages.success(request, f"{n} correo(s) en cola.")


PedidoAdmin.actions = list(PedidoAdmin.actions or []) + [enviar_correo_confirmacion]
