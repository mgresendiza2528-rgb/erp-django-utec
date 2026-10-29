from django.shortcuts import render
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


# ---- W08: vistas de escritura ----
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.db.models import ProtectedError
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from .forms import DetalleVentaForm, VentaForm
from .models import Venta


def crear_venta(request):
    if not request.user.is_authenticated:
        return redirect_to_login(request.get_full_path())

    venta_form = VentaForm(request.POST or None)
    detalle_form = DetalleVentaForm(request.POST or None)

    if request.method == 'POST' and venta_form.is_valid() and detalle_form.is_valid():
        venta = venta_form.save()
        detalle = detalle_form.save(commit=False)
        detalle.venta = venta
        detalle.save()
        messages.success(request, f'Venta #{venta.pk} registrada. Total: ${venta.total:.2f}')
        return redirect('ventas:detalle', venta_id=venta.pk)

    return render(request, 'ventas/crear.html', {
        'venta_form': venta_form,
        'detalle_form': detalle_form,
    })


class VentaDeleteView(LoginRequiredMixin, DeleteView):
    model = Venta
    template_name = 'ventas/eliminar.html'
    pk_url_kwarg = 'venta_id'
    success_url = reverse_lazy('ventas:lista')

    def form_valid(self, form):
        pk = self.object.pk
        try:
            response = super().form_valid(form)
        except ProtectedError:
            messages.error(self.request, f'No se puede eliminar la venta #{pk}.')
            return redirect('ventas:detalle', pk)
        messages.success(self.request, f'Venta #{pk} eliminada.')
        return response
