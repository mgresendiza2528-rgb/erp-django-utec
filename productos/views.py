# productos/views.py
"""Vistas de la app productos.

W02: index (placeholder). W07: ListView y DetailView.
"""
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import Producto


def index(request):
    app = __name__.split('.')[0]
    context = {'titulo': app.capitalize()}
    return render(request, app + '/index.html', context)


class ProductoListView(ListView):
    """Lista paginada de productos activos."""

    model = Producto
    template_name = 'productos/lista.html'
    context_object_name = 'productos'
    paginate_by = 20

    def get_queryset(self):
        return (
            Producto.objects
            .select_related('categoria', 'proveedor')
            .filter(activo=True)
            .order_by('nombre')
        )


class ProductoDetailView(DetailView):
    """Detalle de un producto."""

    model = Producto
    template_name = 'productos/detalle.html'
    context_object_name = 'producto'
    pk_url_kwarg = 'producto_id'

    def get_queryset(self):
        return Producto.objects.select_related('categoria', 'proveedor')


# ---- W08: vistas de escritura ----
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView

from .forms import ProductoForm
from .models import Producto


class ProductoCreateView(LoginRequiredMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'productos/crear.html'
    success_url = reverse_lazy('productos:lista')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'"{self.object}" creado exitosamente.')
        return response


class ProductoUpdateView(LoginRequiredMixin, UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'productos/editar.html'
    pk_url_kwarg = 'producto_id'
    success_url = reverse_lazy('productos:lista')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'"{self.object}" actualizado.')
        return response


class ProductoDeleteView(LoginRequiredMixin, DeleteView):
    model = Producto
    template_name = 'productos/eliminar.html'
    pk_url_kwarg = 'producto_id'
    success_url = reverse_lazy('productos:lista')

    def form_valid(self, form):
        nombre = str(self.object)
        try:
            response = super().form_valid(form)
        except ProtectedError:
            messages.error(self.request, f'No se puede eliminar "{nombre}": tiene registros relacionados.')
            return redirect('productos:detalle', self.object.pk)
        messages.success(self.request, f'"{nombre}" eliminado.')
        return response
