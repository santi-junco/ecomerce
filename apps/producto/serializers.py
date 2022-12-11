from rest_framework import serializers

from .models import Productos, Imagenes

from apps.core.exception import CustomException

from django.db import transaction

class ProductoSerializers(serializers.ModelSerializer):
    imagenes = serializers.SerializerMethodField()

    class Meta:
        model = Productos
        fields = '__all__'

    def get_imagenes(self, instance):
        try:
            imagenes = Imagenes.objects.filter(producto=instance).values('id','imagen')
        except Exception as e:
            print(e)
            raise CustomException(f"Error al obtener imagenes del producto {instance.nombre}")
        
        return imagenes