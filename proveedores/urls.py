from django.urls import path
from . import views

app_name = __name__.split('.')[0]

urlpatterns = [
    path('', views.ProveedorListView.as_view(), name='lista'),
    path('inicio/', views.index, name='inicio'),
    path('<int:proveedor_id>/', views.ProveedorDetailView.as_view(), name='detalle'),
]
