from rest_framework import serializers

from django.db import transaction

from .models import Carrito, RelacionCarritoProducto

from apps.core.exception import CustomException
from apps.producto.models import Imagenes

class CarritoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Carrito
        fields = '__all__'

class CarritoListSerializers(serializers.ModelSerializer):
    producto = serializers.SerializerMethodField()
    modificado = serializers.DateTimeField(format='%d/%m/%Y')
    class Meta:
        model = Carrito
        fields = [
            'id',
            'modificado',
            'monto',
            'producto'
        ]

    def get_producto(self, instance):
        with transaction.atomic():
            try:
                productos = RelacionCarritoProducto.objects.filter(carrito=instance)
            except:
                raise CustomException('Error a obter productos')

            producto_list = []
            for producto in productos:

                try:
                    imagen = Imagenes.objects.filter(producto=producto.producto).last().imagen
                except:
                    imagen = None

                data = {
                    'nombre': producto.producto.nombre,
                    'descripcion': producto.producto.descripcion,
                    'precio': producto.producto.precio,
                    'cantidad': producto.cantidad,
                    'imagen': imagen.name if imagen else imagen
                }

                producto_list.append(data)

            return producto_list

class RelacionCarritoProductoSerializers(serializers.ModelSerializer):
    class Meta:
        model = RelacionCarritoProducto
        fields = '__all__'