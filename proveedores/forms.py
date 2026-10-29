from django import forms

from .models import Proveedor


class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'contacto', 'correo', 'telefono', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'erp-input'}),
            'contacto': forms.TextInput(attrs={'class': 'erp-input'}),
            'correo': forms.EmailInput(attrs={'class': 'erp-input'}),
            'telefono': forms.TextInput(attrs={'class': 'erp-input'}),
        }
