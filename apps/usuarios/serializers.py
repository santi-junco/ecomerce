from rest_framework import serializers

from .models import Usuarios

class UsusariosSerializers(serializers.ModelSerializer):
    class Meta:
        model = Usuarios
        fields = '__all__'

