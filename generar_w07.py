from pathlib import Path

A = {}

A['templates/_paginacion.html'] = r'''{% if is_paginated %}
<div style="display:flex;gap:.5rem;justify-content:center;margin-top:1.5rem;">
    {% if page_obj.has_previous %}
        <a href="?page={{ page_obj.previous_page_number }}" class="btn-erp-primary btn-erp-sm">← Anterior</a>
    {% endif %}
    <span style="padding:.35rem .75rem;color:var(--clr-muted);font-size:.88rem;">
        Página {{ page_obj.number }} de {{ page_obj.paginator.num_pages }}
    </span>
    {% if page_obj.has_next %}
        <a href="?page={{ page_obj.next_page_number }}" class="btn-erp-primary btn-erp-sm">Siguiente →</a>
    {% endif %}
</div>
{% endif %}
'''

# ---------------- CLIENTES ----------------
A['clientes/views.py'] = r'''from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import Cliente


def index(request):
    app = __name__.split('.')[0]
    context = {'titulo': app.capitalize()}
    return render(request, app + '/index.html', context)


class ClienteListView(ListView):
    model = Cliente
    template_name = 'clientes/lista.html'
    context_object_name = 'clientes'
    paginate_by = 20

    def get_queryset(self):
        return Cliente.objects.order_by('nombre')


class ClienteDetailView(DetailView):
    model = Cliente
    template_name = 'clientes/detalle.html'
    context_object_name = 'cliente'
    pk_url_kwarg = 'cliente_id'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['ventas'] = self.object.ventas.order_by('-fecha')[:10]
        return ctx
'''

A['clientes/urls.py'] = r'''from django.urls import path
from . import views

app_name = __name__.split('.')[0]

urlpatterns = [
    path('', views.ClienteListView.as_view(), name='lista'),
    path('inicio/', views.index, name='inicio'),
    path('<int:cliente_id>/', views.ClienteDetailView.as_view(), name='detalle'),
]
'''

A['clientes/templates/clientes/lista.html'] = r'''{% extends "base.html" %}
{% block title %}Clientes{% endblock %}
{% block nav_clientes %}active{% endblock %}

{% block content %}
<div class="erp-page-title">
    <h2>👥 Clientes</h2>
    <span style="margin-left:auto;color:var(--clr-muted);font-size:.85rem;">
        {{ page_obj.paginator.count }} cliente(s)
    </span>
</div>

{% if clientes %}
<table class="erp-table">
    <thead>
        <tr><th>#</th><th>Nombre</th><th>Correo</th><th>Teléfono</th></tr>
    </thead>
    <tbody>
        {% for c in clientes %}
        <tr>
            <td><code>{{ c.pk }}</code></td>
            <td>
                <a href="{% url 'clientes:detalle' c.pk %}" style="color:var(--clr-royal);font-weight:600;">{{ c.nombre }}</a>
            </td>
            <td>{{ c.correo }}</td>
            <td>{{ c.telefono|default:"—" }}</td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% include "_paginacion.html" %}
{% else %}
<div class="erp-alert-info">No hay clientes registrados aún.</div>
{% endif %}
{% endblock %}
'''

A['clientes/templates/clientes/detalle.html'] = r'''{% extends "base.html" %}
{% block title %}{{ cliente.nombre }}{% endblock %}
{% block nav_clientes %}active{% endblock %}

{% block content %}
<div class="erp-page-title">
    <h2>👤 {{ cliente.nombre }}</h2>
</div>

<div class="erp-card">
    <div class="erp-card-header">Datos del cliente</div>
    <dl class="row" style="margin:0;">
        <dt class="col-sm-3">Correo</dt>
        <dd class="col-sm-9">{{ cliente.correo }}</dd>
        <dt class="col-sm-3">Teléfono</dt>
        <dd class="col-sm-9">{{ cliente.telefono|default:"—" }}</dd>
    </dl>
</div>

<div class="erp-card">
    <div class="erp-card-header">Últimas 10 ventas</div>
    {% if ventas %}
    <table class="erp-table">
        <thead><tr><th>#</th><th>Fecha</th><th>Total</th></tr></thead>
        <tbody>
            {% for v in ventas %}
            <tr>
                <td><a href="{% url 'ventas:detalle' v.pk %}" style="color:var(--clr-royal);">#{{ v.pk }}</a></td>
                <td>{{ v.fecha|date:"d/m/Y H:i" }}</td>
                <td style="color:var(--clr-gold);font-weight:600;">${{ v.total }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    {% else %}
    <p style="color:var(--clr-muted);">Este cliente aún no tiene ventas.</p>
    {% endif %}
</div>

<a href="{% url 'clientes:lista' %}" class="btn-erp-primary">← Volver</a>
{% endblock %}
'''

# ---------------- PROVEEDORES ----------------
A['proveedores/views.py'] = r'''from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import Proveedor


def index(request):
    app = __name__.split('.')[0]
    context = {'titulo': app.capitalize()}
    return render(request, app + '/index.html', context)


class ProveedorListView(ListView):
    model = Proveedor
    template_name = 'proveedores/lista.html'
    context_object_name = 'proveedores'
    paginate_by = 20

    def get_queryset(self):
        return Proveedor.objects.order_by('nombre')


class ProveedorDetailView(DetailView):
    model = Proveedor
    template_name = 'proveedores/detalle.html'
    context_object_name = 'proveedor'
    pk_url_kwarg = 'proveedor_id'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['productos'] = (
            self.object.productos
            .select_related('categoria')
            .order_by('nombre')
        )
        return ctx
'''

A['proveedores/urls.py'] = r'''from django.urls import path
from . import views

app_name = __name__.split('.')[0]

urlpatterns = [
    path('', views.ProveedorListView.as_view(), name='lista'),
    path('inicio/', views.index, name='inicio'),
    path('<int:proveedor_id>/', views.ProveedorDetailView.as_view(), name='detalle'),
]
'''

A['proveedores/templates/proveedores/lista.html'] = r'''{% extends "base.html" %}
{% block title %}Proveedores{% endblock %}
{% block nav_proveedores %}active{% endblock %}

{% block content %}
<div class="erp-page-title">
    <h2>🏭 Proveedores</h2>
    <span style="margin-left:auto;color:var(--clr-muted);font-size:.85rem;">
        {{ page_obj.paginator.count }} proveedor(es)
    </span>
</div>

{% if proveedores %}
<table class="erp-table">
    <thead>
        <tr><th>#</th><th>Nombre</th><th>Contacto</th><th>Correo</th></tr>
    </thead>
    <tbody>
        {% for p in proveedores %}
        <tr>
            <td><code>{{ p.pk }}</code></td>
            <td>
                <a href="{% url 'proveedores:detalle' p.pk %}" style="color:var(--clr-royal);font-weight:600;">{{ p.nombre }}</a>
            </td>
            <td>{{ p.contacto|default:"—" }}</td>
            <td>{{ p.correo }}</td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% include "_paginacion.html" %}
{% else %}
<div class="erp-alert-info">No hay proveedores registrados aún.</div>
{% endif %}
{% endblock %}
'''

A['proveedores/templates/proveedores/detalle.html'] = r'''{% extends "base.html" %}
{% block title %}{{ proveedor.nombre }}{% endblock %}
{% block nav_proveedores %}active{% endblock %}

{% block content %}
<div class="erp-page-title">
    <h2>🏭 {{ proveedor.nombre }}</h2>
</div>

<div class="erp-card">
    <div class="erp-card-header">Datos del proveedor</div>
    <dl class="row" style="margin:0;">
        <dt class="col-sm-3">Contacto</dt>
        <dd class="col-sm-9">{{ proveedor.contacto|default:"—" }}</dd>
        <dt class="col-sm-3">Correo</dt>
        <dd class="col-sm-9">{{ proveedor.correo }}</dd>
    </dl>
</div>

<div class="erp-card">
    <div class="erp-card-header">Productos suministrados</div>
    {% if productos %}
    <table class="erp-table">
        <thead><tr><th>Nombre</th><th>Categoría</th><th>Precio</th><th>Stock</th></tr></thead>
        <tbody>
            {% for prod in productos %}
            <tr>
                <td><a href="{% url 'productos:detalle' prod.pk %}" style="color:var(--clr-royal);">{{ prod.nombre }}</a></td>
                <td>{{ prod.categoria }}</td>
                <td style="color:var(--clr-gold);">${{ prod.precio }}</td>
                <td>{{ prod.stock }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    {% else %}
    <p style="color:var(--clr-muted);">Sin productos asignados.</p>
    {% endif %}
</div>

<a href="{% url 'proveedores:lista' %}" class="btn-erp-primary">← Volver</a>
{% endblock %}
'''

# ---------------- VENTAS ----------------
A['ventas/views.py'] = r'''from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import Venta


def index(request):
    app = __name__.split('.')[0]
    context = {'titulo': app.capitalize()}
    return render(request, app + '/index.html', context)


class VentaListView(ListView):
    model = Venta
    template_name = 'ventas/lista.html'
    context_object_name = 'ventas'
    paginate_by = 20

    def get_queryset(self):
        return Venta.objects.select_related('cliente').order_by('-fecha')


class VentaDetailView(DetailView):
    model = Venta
    template_name = 'ventas/detalle.html'
    context_object_name = 'venta'
    pk_url_kwarg = 'venta_id'

    def get_queryset(self):
        return (
            Venta.objects
            .select_related('cliente')
            .prefetch_related('detalles__producto')
        )
'''

A['ventas/urls.py'] = r'''from django.urls import path
from . import views

app_name = __name__.split('.')[0]

urlpatterns = [
    path('', views.VentaListView.as_view(), name='lista'),
    path('inicio/', views.index, name='inicio'),
    path('<int:venta_id>/', views.VentaDetailView.as_view(), name='detalle'),
]
'''

A['ventas/templates/ventas/lista.html'] = r'''{% extends "base.html" %}
{% block title %}Ventas{% endblock %}
{% block nav_ventas %}active{% endblock %}

{% block content %}
<div class="erp-page-title">
    <h2>💰 Ventas</h2>
    <span style="margin-left:auto;color:var(--clr-muted);font-size:.85rem;">
        {{ page_obj.paginator.count }} venta(s)
    </span>
</div>

{% if ventas %}
<table class="erp-table">
    <thead>
        <tr><th>#</th><th>Cliente</th><th>Fecha</th><th>Total</th></tr>
    </thead>
    <tbody>
        {% for v in ventas %}
        <tr>
            <td>
                <a href="{% url 'ventas:detalle' v.pk %}" style="color:var(--clr-royal);font-weight:600;">#{{ v.pk }}</a>
            </td>
            <td>{{ v.cliente }}</td>
            <td>{{ v.fecha|date:"d/m/Y H:i" }}</td>
            <td style="font-weight:700;color:var(--clr-gold);">${{ v.total }}</td>
        </tr>
        {% endfor %}
    </tbody>
</table>
{% include "_paginacion.html" %}
{% else %}
<div class="erp-alert-info">No hay ventas registradas aún.</div>
{% endif %}
{% endblock %}
'''

A['ventas/templates/ventas/detalle.html'] = r'''{% extends "base.html" %}
{% block title %}Venta #{{ venta.pk }}{% endblock %}
{% block nav_ventas %}active{% endblock %}

{% block content %}
<div class="erp-page-title">
    <h2>💰 Venta #{{ venta.pk }}</h2>
</div>

<div class="erp-card">
    <div class="erp-card-header">Encabezado</div>
    <dl class="row" style="margin:0;">
        <dt class="col-sm-3">Cliente</dt>
        <dd class="col-sm-9">
            <a href="{% url 'clientes:detalle' venta.cliente.pk %}" style="color:var(--clr-royal);">{{ venta.cliente }}</a>
        </dd>
        <dt class="col-sm-3">Fecha</dt>
        <dd class="col-sm-9">{{ venta.fecha|date:"d/m/Y H:i" }}</dd>
    </dl>
</div>

<div class="erp-card">
    <div class="erp-card-header">Líneas de detalle</div>
    <table class="erp-table">
        <thead>
            <tr><th>Producto</th><th>Precio unit.</th><th>Cantidad</th><th>Subtotal</th></tr>
        </thead>
        <tbody>
            {% for d in venta.detalles.all %}
            <tr>
                <td><a href="{% url 'productos:detalle' d.producto.pk %}" style="color:var(--clr-royal);">{{ d.producto.nombre }}</a></td>
                <td>${{ d.precio_unitario }}</td>
                <td>{{ d.cantidad }}</td>
                <td style="font-weight:600;">${{ d.subtotal }}</td>
            </tr>
            {% empty %}
            <tr><td colspan="4" style="text-align:center;color:var(--clr-muted);">Sin líneas de detalle.</td></tr>
            {% endfor %}
        </tbody>
        <tfoot>
            <tr>
                <td colspan="3" style="text-align:right;padding:.65rem 1rem;font-weight:600;">Total:</td>
                <td style="padding:.65rem 1rem;font-weight:700;color:var(--clr-gold);">${{ venta.total }}</td>
            </tr>
        </tfoot>
    </table>
</div>

<a href="{% url 'ventas:lista' %}" class="btn-erp-primary">← Volver</a>
{% endblock %}
'''

# ---------------- TESTS ----------------
A['tests/test_w07_vistas_lectura.py'] = r'''"""Suite W07: vistas de lectura (ListView y DetailView)."""
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
'''

# ---------------- PLANNING ----------------
A['sprint2_planning.md'] = r'''# Sprint 2 Planning — ERP Django
## Semanas W07–W09 · Espiral 3: CRUD Web y Autenticación

**Sprint Goal:**
Al finalizar el Sprint 2, el ERP mostrará lista y detalle de las
entidades principales, con formularios de alta/edición/borrado
protegidos por autenticación y 3 roles de acceso.

**Duración:** W07 (ListView/DetailView) · W08 (Create/Update/Delete) · W09 (Auth + RBAC · M3)

## HUs seleccionadas

| ID | Historia | Puntos | Semana |
|---|---|---|---|
| HU-E3-01 | Ver la lista de productos | 2 | W07 |
| HU-E3-02 | Ver el detalle de un producto | 2 | W07 |
| HU-E3-03 | Ver listas de clientes y proveedores | 2 | W07 |
| HU-E3-04 | Ver el detalle de ventas con sus líneas | 3 | W07 |
| HU-E3-05 | Crear y editar productos | 3 | W08 |
| HU-E3-06 | Registrar nuevas ventas con detalles | 5 | W08 |
| HU-E3-07 | Eliminar registros con confirmación | 2 | W08 |
| HU-E3-08 | Autenticación login/logout funcional | 3 | W09 |
| HU-E3-09 | 3 roles con permisos diferenciados | 5 | W09 |

**Total Sprint 2:** 27 puntos

## Sprint Backlog — estado W07

| Tarea | Estado |
|---|---|
| ListView + DetailView para productos, clientes, proveedores y ventas | ✅ W07 |
| 8 templates lista.html + detalle.html | ✅ W07 |
| urls.py con rutas lista y detalle | ✅ W07 |
| select_related / prefetch_related anti N+1 | ✅ W07 |
| Tests de vistas de lectura | ✅ W07 |
| CreateView + UpdateView + DeleteView | ⏳ W08 |
| Login/Logout + LoginRequiredMixin | ⏳ W09 |
| 3 roles RBAC | ⏳ W09 |
'''

for ruta, contenido in A.items():
    p = Path(ruta)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(contenido, encoding='utf-8', newline='\n')
    print('OK', ruta)