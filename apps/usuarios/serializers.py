from rest_framework import serializers

from .models import Usuarios

class UsuariosSerializers(serializers.ModelSerializer):
    class Meta:
        model = Usuarios
        fields = [
            'id',
            'first_name',
            'last_name',
            'email'
        ]

