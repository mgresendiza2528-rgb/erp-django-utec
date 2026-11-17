from django.urls import path
from . import views
from .pdf_views import venta_pdf

app_name = __name__.split('.')[0]

urlpatterns = [
    path('', views.VentaListView.as_view(), name='lista'),
    path('inicio/', views.index, name='inicio'),
    path('<int:venta_id>/', views.VentaDetailView.as_view(), name='detalle'),
    path('nueva/', views.crear_venta, name='crear'),
    path('<int:venta_id>/eliminar/', views.VentaDeleteView.as_view(), name='eliminar'),
    path('<int:venta_id>/pdf/', venta_pdf, name='pdf'),
]