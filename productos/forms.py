from django import forms

from .models import Producto


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'precio', 'stock', 'categoria', 'proveedor', 'activo', 'imagen']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'erp-input'}),
            'precio': forms.NumberInput(attrs={'class': 'erp-input', 'step': '0.01', 'min': '0'}),
            'stock': forms.NumberInput(attrs={'class': 'erp-input', 'min': '0'}),
            'categoria': forms.Select(attrs={'class': 'erp-input'}),
            'proveedor': forms.Select(attrs={'class': 'erp-input'}),
            'imagen': forms.ClearableFileInput(attrs={
                'class': 'erp-input',
                'accept': 'image/jpeg,image/png,image/webp',
            }),
        }
