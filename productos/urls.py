# productos/urls.py
from django.urls import path
from . import views

app_name = __name__.split('.')[0]

urlpatterns = [
    path('', views.ProductoListView.as_view(), name='lista'),
    path('inicio/', views.index, name='inicio'),
    path('<int:producto_id>/', views.ProductoDetailView.as_view(), name='detalle'),
]