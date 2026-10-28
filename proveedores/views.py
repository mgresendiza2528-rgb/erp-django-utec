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
