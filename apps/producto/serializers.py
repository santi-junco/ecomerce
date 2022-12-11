from rest_framework import serializers

from .models import Productos, Imagenes, Favorito

from apps.core.exception import CustomException
from apps.categorias.models import RelacionCategoriasProductos

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

# favoritos
class FavoritoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Favorito
        fields = '__all__'

class FavoritosListSerializers(serializers.ModelSerializer):
    class Meta:
        model = Favorito
        fields = ['id','producto']
        depth = 1
        
    def to_representation(self, instance):
        rep = super(FavoritosListSerializers, self).to_representation(instance)
        
        try:
            imagenes = Imagenes.objects.filter(producto=instance.producto).values('id', 'imagen')
        except:
            raise CustomException('Error al obtener imagenes')

        rep['producto']['imagenes'] = imagenes

        return rep
class ProductoCategoriaSerializers(serializers.ModelSerializer):
    class Meta:
        model = RelacionCategoriasProductos
        fields = ['producto']
        depth = 1

    def to_representation(self, instance):
        rep = super(ProductoCategoriaSerializers, self).to_representation(instance)
        
        try:
            imagenes = Imagenes.objects.filter(producto=instance.producto).values('id', 'imagen')
        except:
            raise CustomException('Error al obtener imagenes')

        rep['producto']['imagenes'] = imagenes

        return rep