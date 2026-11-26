# ventas/admin.py
from django.contrib import admin, messages

from .models import DetalleVenta, Pedido, Venta


class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 1


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'fecha')
    inlines = [DetalleVentaInline]


@admin.action(description="Enviar correo de confirmación (pagados sin correo)")
def enviar_correo_confirmacion(modeladmin, request, queryset):
    from .tasks import enviar_confirmacion_pedido

    n = 0
    for pedido in queryset.filter(estado='pagado', correo_enviado=False):
        enviar_confirmacion_pedido.delay(pedido.pk)
        n += 1
    messages.success(request, f"{n} correo(s) en cola.")


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('numero_pedido', 'cliente', 'estado', 'total_pagado', 'correo_enviado')
    list_filter = ('estado', 'correo_enviado')
    search_fields = ('numero_pedido',)
    actions = [enviar_correo_confirmacion]
