from decimal import Decimal

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView

from productos.models import Producto

from .filters import ProductoFilter


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