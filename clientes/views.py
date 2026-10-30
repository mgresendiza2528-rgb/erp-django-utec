from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
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


# ---- W08: vistas de escritura ----
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView

from .forms import ClienteForm
from .models import Cliente


class ClienteCreateView(LoginRequiredMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/crear.html'
    success_url = reverse_lazy('clientes:lista')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'"{self.object}" creado exitosamente.')
        return response


class ClienteUpdateView(LoginRequiredMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/editar.html'
    pk_url_kwarg = 'cliente_id'
    success_url = reverse_lazy('clientes:lista')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'"{self.object}" actualizado.')
        return response


class ClienteDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'clientes.delete_cliente'
    raise_exception = True
    model = Cliente
    template_name = 'clientes/eliminar.html'
    pk_url_kwarg = 'cliente_id'
    success_url = reverse_lazy('clientes:lista')

    def form_valid(self, form):
        nombre = str(self.object)
        try:
            response = super().form_valid(form)
        except ProtectedError:
            messages.error(self.request, f'No se puede eliminar "{nombre}": tiene registros relacionados.')
            return redirect('clientes:detalle', self.object.pk)
        messages.success(self.request, f'"{nombre}" eliminado.')
        return response
