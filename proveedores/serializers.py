from rest_framework import serializers
from .models import Proveedor

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = ['id', 'nombre', 'contacto', 'correo', 'telefono', 'activo', 'creado']
        read_only_fields = ['id', 'creado']
