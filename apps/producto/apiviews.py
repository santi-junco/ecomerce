from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView

from django.db import transaction

from .models import Productos, Imagenes
from .serializers import ProductoSerializers

from apps.core.exception import CustomException

# crear 
class ProductoCreateApiView(CreateAPIView):
    serializer_class = ProductoSerializers

    def perform_create(self, serializer):
        with transaction.atomic():
            producto = serializer.save()
            try:
                imagenes = int(self.request.data['cantidad_imagenes'])
            except:
                raise CustomException('Debe ingresar al menos una imagen del producto')

            for imagen in range(1, imagenes+1):
                try:
                    Imagenes.objects.create(
                        producto = producto,
                        imagen = self.request.data[f'imagen{imagen}']
                    )
                except Exception as e:
                    raise CustomException('Error al crear producto')

            return super().perform_create(serializer)

# listar
class ProductosListApiView(ListAPIView):
    queryset = Productos.objects.all()
    serializer_class = ProductoSerializers

# ver 
class ProductoRetrieveApiView(RetrieveAPIView):
    queryset = Productos.objects.all()
    serializer_class = ProductoSerializers

# Editar
class ProductoEditApiView(UpdateAPIView):
    queryset = Productos.objects.all()
    serializer_class = ProductoSerializers

    def perform_update(self, serializer):
        with transaction.atomic():
            producto = serializer.save()
            imagen_eliminar = self.request.data.get('imagen_eliminar', [])
            imagenes = int(self.request.data.get('cantidad_imagenes', 0))
            
            for imagen in imagen_eliminar:
                try:
                    Imagenes.objects.get(id=imagen).delete()
                except:
                    raise CustomException('Error al eliminar imagen')

            if imagenes > 0:
                for imagen in range(1, imagenes+1):
                    try:
                        Imagenes.objects.create(
                            producto = producto,
                            imagen = self.request.data[f'imagen{imagen}']
                        )
                    except:
                        raise CustomException('Error al agregar nueva imagen')

            return super().perform_update(serializer)

# Eliminar
class ProductoDeleteApiView(DestroyAPIView):
    queryset = Productos.objects.all()
    serializer_class = ProductoSerializers
