from django.shortcuts import render
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


# ---- W08: vistas de escritura ----
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView

from .forms import ProveedorForm
from .models import Proveedor


class ProveedorCreateView(LoginRequiredMixin, CreateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'proveedores/crear.html'
    success_url = reverse_lazy('proveedores:lista')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'"{self.object}" creado exitosamente.')
        return response


class ProveedorUpdateView(LoginRequiredMixin, UpdateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'proveedores/editar.html'
    pk_url_kwarg = 'proveedor_id'
    success_url = reverse_lazy('proveedores:lista')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'"{self.object}" actualizado.')
        return response


class ProveedorDeleteView(LoginRequiredMixin, DeleteView):
    model = Proveedor
    template_name = 'proveedores/eliminar.html'
    pk_url_kwarg = 'proveedor_id'
    success_url = reverse_lazy('proveedores:lista')

    def form_valid(self, form):
        nombre = str(self.object)
        try:
            response = super().form_valid(form)
        except ProtectedError:
            messages.error(self.request, f'No se puede eliminar "{nombre}": tiene registros relacionados.')
            return redirect('proveedores:detalle', self.object.pk)
        messages.success(self.request, f'"{nombre}" eliminado.')
        return response
