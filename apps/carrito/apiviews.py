from rest_framework.generics import RetrieveAPIView, DestroyAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from django.db import transaction

from .models import Carrito, RelacionCarritoProducto
from .serializers import CarritoSerializers, CarritoListSerializers, RelacionCarritoProductoSerializers

from apps.producto.models import Productos, Imagenes
from apps.core.exception import CustomException

# Ver carrito en curso
class CarritoEnCursoRetrieveApiView(APIView):
    def get(self, request, user):
        with transaction.atomic():
            try:
                carrito = Carrito.objects.get(usuario=user, estado='en curso')
            except:
                raise CustomException('El usuario no tiene carrito en curso')

            try:
                productos = RelacionCarritoProducto.objects.filter(carrito=carrito)
            except:
                raise CustomException('Error al obtener productos')
            
            data_list = []
            for producto in productos:
                try:
                    imagen = Imagenes.objects.filter(producto=producto['producto']).last()
                except:
                    imagen = None

                data = {
                    'nombre': producto['producto__nombre'],
                    'descripcion': producto['producto__descripcion'],
                    'precio': producto['producto__precio'],
                    'cantidad': producto['cantidad'],
                    'imagen': imagen.imagen if imagen else imagen
                }
                data_list.append(data)

            return Response(data_list)

# Ver carritos finalizados
class CarritoFinalizadoListApiView(ListAPIView):
    queryset = Carrito.objects.all()
    serializer_class = CarritoListSerializers

# Eliminar carrito
class CarritoRetrieveApiView(DestroyAPIView):
    queryset = Carrito.objects.all()
    serializer_class = CarritoSerializers

# Agregar producto al carrito
class AgregarProductoApiView(APIView):
    
    def post(self, request):
        with transaction.atomic():
            
            usuario = request.data['usuario']
            producto_body = request.data['producto']

            # pregunto si tiene algun carrito en curso
            try:
                carrito = Carrito.objects.get(usuario=usuario, estado='en curso')
            except:
                carrito = None

            if carrito:
                # obtengo el producto y creo una nueva relacion
                # try:
                #     producto = Productos.objects.get(id=produto_body)
                # except:
                #     raise CustomException('Error al obtener el producto')
                
                data = {
                    'usuario': usuario,
                    'producto': producto_body
                }

                relacion = RelacionCarritoProductoSerializers(data=data)
                if relacion.is_valid():
                    relacion.save()
                else:
                    return Response({'detail': 'Error al agregar producto al carrito'})

            else:
                data_carrito = {
                    'usuario': usuario,
                    'estado': 'en curso'
                }
                carrito = CarritoSerializers(data=data_carrito)

                if carrito.is_valid():
                    carrito.save()
                else:
                    return Response({'detail': 'Error al agregar producto al carrito'})

                data_relacion = {
                    'carrito': carrito.id,
                    'producto': producto_body
                }
                
                relacion = RelacionCarritoProductoSerializers(data=data_relacion)

                if relacion.is_valid():
                    relacion.save()
                else:
                    return Response({'detail': 'Error al agregar producto al carrito'})

            return Response({'detail':'Producto agregado correctamente'})