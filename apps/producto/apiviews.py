from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView

from django.db import transaction

from .models import Productos, Imagenes
from .serializers import ProductoSerializers

from apps.core.exception import CustomException
from apps.categorias.models import Categorias, RelacionCategoriasProductos

# crear 
class ProductoCreateApiView(CreateAPIView):
    serializer_class = ProductoSerializers

    def perform_create(self, serializer):
        with transaction.atomic():
            producto = serializer.save()

            # relacion de imagene/s con el producto
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

            # Relacion de categoria/s con el producto
            try:
                categorias = self.request.data['categorias']
            except:
                raise CustomException('Debe seleccionar al menos una categoria')

            for categoria in categorias:
                try:
                    categoria_query = Categorias.objects.get(id=categoria)
                except:
                    raise CustomException('Categoria inexistente')

                try:
                    RelacionCategoriasProductos.objects.create(
                        categoria = categoria_query,
                        producto = producto
                    )
                except:
                    raise CustomException('Error al relacionar categoria con producto')

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

            # Agregar y/o quitar imagenes 
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

            # Agregar y/o quitar categorias
            cat_body = self.request.data.get('categorias', None)
            if cat_body:
                try:
                    # obtengo las categorias actuales del producto
                    cat_actuales = RelacionCategoriasProductos.objects.filter(producto=producto).values_list('categoria', flat=True)
                except:
                    raise CustomException('Error al obtener categorias actuales')

                # obtengo categorias a eliminar
                eliminar = list(filter(lambda item: item not in cat_body, cat_actuales))

                # obtengo los nuevos a agregar
                agregar = list(filter(lambda item: item not in cat_actuales, cat_body))

                for categoria in eliminar:
                    try:
                        RelacionCategoriasProductos.objects.get(categoria=categoria, producto=producto).delete()
                    except:
                        raise CustomException('Error al quitar categoria')

                for categoria in agregar:
                    try:
                        categoria_query = Categorias.objects.get(id=categoria)
                    except:
                        raise CustomException('Error al obtener categoria')
                    try:
                        RelacionCategoriasProductos.objects.create(
                            categoria=categoria_query,
                            producto=producto
                        )
                    except:
                        raise CustomException('Error al agregar categoria')

            return super().perform_update(serializer)

# Eliminar
class ProductoDeleteApiView(DestroyAPIView):
    queryset = Productos.objects.all()
    serializer_class = ProductoSerializers

