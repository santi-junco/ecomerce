from rest_framework import serializers

from .models import Categorias

class CategoriaSerializers(serializers.ModelSerializer):
    class Meta:
        model = Categorias
        fields = '__all__'
