from django.urls import path
from . import views

app_name = __name__.split('.')[0]

urlpatterns = [
    path('', views.ClienteListView.as_view(), name='lista'),
    path('inicio/', views.index, name='inicio'),
    path('<int:cliente_id>/', views.ClienteDetailView.as_view(), name='detalle'),
]
