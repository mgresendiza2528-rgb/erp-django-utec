"""Suite W07: vistas de lectura (ListView y DetailView)."""
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from clientes.models import Cliente
from productos.models import Categoria, Producto
from proveedores.models import Proveedor
from ventas.models import DetalleVenta, Venta


class ProductoVistaTest(TestCase):
    def setUp(self):
        self.cat = Categoria.objects.create(nombre='Cat Test')
        self.prod = Producto.objects.create(
            nombre='Laptop Test', precio=Decimal('10000.00'),
            stock=5, categoria=self.cat
        )

    def test_lista_productos_http_200(self):
        r = self.client.get(reverse('productos:lista'))
        self.assertEqual(r.status_code, 200)

    def test_lista_productos_template_correcto(self):
        r = self.client.get(reverse('productos:lista'))
        self.assertTemplateUsed(r, 'productos/lista.html')

    def test_lista_muestra_producto(self):
        r = self.client.get(reverse('productos:lista'))
        self.assertIn('productos', r.context)
        self.assertContains(r, 'Laptop Test')

    def test_detalle_producto_http_200(self):
        r = self.client.get(reverse('productos:detalle', args=[self.prod.pk]))
        self.assertEqual(r.status_code, 200)

    def test_detalle_producto_404(self):
        r = self.client.get(reverse('productos:detalle', args=[9999]))
        self.assertEqual(r.status_code, 404)

    def test_lista_paginacion_20_por_pagina(self):
        for i in range(24):
            Producto.objects.create(
                nombre=f'Prod {i}', precio=Decimal('10.00'),
                stock=1, categoria=self.cat
            )
        r = self.client.get(reverse('productos:lista'))
        self.assertEqual(len(r.context['productos']), 20)
        self.assertTrue(r.context['is_paginated'])


class ClienteVistaTest(TestCase):
    def setUp(self):
        self.cli = Cliente.objects.create(nombre='Ana García', correo='ana@test.com')

    def test_lista_clientes_http_200(self):
        r = self.client.get(reverse('clientes:lista'))
        self.assertEqual(r.status_code, 200)

    def test_lista_clientes_template_correcto(self):
        r = self.client.get(reverse('clientes:lista'))
        self.assertTemplateUsed(r, 'clientes/lista.html')

    def test_detalle_cliente_contiene_nombre(self):
        r = self.client.get(reverse('clientes:detalle', args=[self.cli.pk]))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Ana García')


class ProveedorVistaTest(TestCase):
    def setUp(self):
        self.prov = Proveedor.objects.create(nombre='Dist. Norte', correo='norte@dist.com')

    def test_lista_proveedores_http_200(self):
        r = self.client.get(reverse('proveedores:lista'))
        self.assertEqual(r.status_code, 200)

    def test_detalle_proveedor_http_200(self):
        r = self.client.get(reverse('proveedores:detalle', args=[self.prov.pk]))
        self.assertEqual(r.status_code, 200)


class VentaVistaTest(TestCase):
    def setUp(self):
        cat = Categoria.objects.create(nombre='Cat')
        prod = Producto.objects.create(
            nombre='P', precio=Decimal('100.00'), stock=5, categoria=cat
        )
        cli = Cliente.objects.create(nombre='C', correo='c@t.com')
        self.venta = Venta.objects.create(cliente=cli)
        DetalleVenta.objects.create(
            venta=self.venta, producto=prod,
            cantidad=2, precio_unitario=Decimal('100.00')
        )

    def test_lista_ventas_http_200(self):
        r = self.client.get(reverse('ventas:lista'))
        self.assertEqual(r.status_code, 200)

    def test_detalle_venta_muestra_total(self):
        r = self.client.get(reverse('ventas:detalle', args=[self.venta.pk]))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, '200.00')
