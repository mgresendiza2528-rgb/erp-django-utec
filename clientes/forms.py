from django import forms

from .models import Cliente


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'correo', 'telefono', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'erp-input'}),
            'correo': forms.EmailInput(attrs={'class': 'erp-input'}),
            'telefono': forms.TextInput(attrs={'class': 'erp-input'}),
        }
