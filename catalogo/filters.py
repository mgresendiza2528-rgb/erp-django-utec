import django_filters
from productos.models import Categoria, Producto


class ProductoFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(field_name='nombre', lookup_expr='icontains')
    categoria = django_filters.ModelChoiceFilter(queryset=Categoria.objects.all(), empty_label='Todas')
    precio_min = django_filters.NumberFilter(field_name='precio', lookup_expr='gte')
    precio_max = django_filters.NumberFilter(field_name='precio', lookup_expr='lte')

    class Meta:
        model = Producto
        fields = ['nombre', 'categoria', 'precio_min', 'precio_max']