from rest_framework.generics import DestroyAPIView, ListAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from django.db import transaction

from .models import Carrito, RelacionCarritoProducto
from .serializers import CarritoSerializers, CarritoListSerializers, RelacionCarritoProductoSerializers

from apps.producto.models import Imagenes, Productos
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
            respuesta = {'monto': carrito.monto}
            data_list = []
            for producto in productos:
                try:
                    imagen = Imagenes.objects.filter(producto=producto.producto).last().imagen
                except:
                    imagen = None

                data = {
                    'id_relacion': producto.id,
                    'nombre': producto.producto.nombre,
                    'descripcion': producto.producto.descripcion,
                    'precio': producto.producto.precio,
                    'cantidad': producto.cantidad,
                    'imagen': imagen.name if imagen else imagen
                }
                data_list.append(data)

            respuesta['productos'] = data_list

            return Response(respuesta)

# Ver carritos finalizados
class CarritoFinalizadoListApiView(ListAPIView):
    serializer_class = CarritoListSerializers

    def get_queryset(self):
        queryset = Carrito.objects.filter(usuario=self.kwargs['user'], estado='finalizado')
        return queryset

# Eliminar carrito
class CarritoDeleteApiView(DestroyAPIView):
    queryset = Carrito.objects.all()
    serializer_class = CarritoSerializers

    def perform_destroy(self, instance):
        with transaction.atomic():
            if instance.estado == 'en curso':
                
                try:
                    productos = RelacionCarritoProducto.objects.filter(carrito=instance)
                except:
                    raise CustomException('Error al obtener productos')

                for producto in productos:
                    try:
                        prod = Productos.objects.get(id=producto.producto)
                    except:
                        raise CustomException('Error al obtener un producto')

                    prod.cantidad += producto.cantidad
                    prod.save()

            return super().perform_destroy(instance)

# Agregar producto al carrito
class AgregarProductoApiView(APIView):
    
    def post(self, request):
        with transaction.atomic():
            
            usuario = request.data['usuario']
            producto_body = request.data['producto']
            producto_cantidad = request.data['cantidad']
            
            try:
                producto = Productos.objects.get(id=producto_body)
            except:
                raise CustomException('Producto inexistente')

            if producto.cantidad < producto_cantidad:
                raise CustomException('No hay cantidad suficiente de este producto')

            # pregunto si tiene algun carrito en curso
            try:
                carrito = Carrito.objects.get(usuario=usuario, estado='en curso')
            except:
                carrito = None
            
            # creo el carrito si no tiene uno en curso
            if not carrito:

                data_carrito = {
                    'usuario': usuario,
                    'estado': 'en curso'
                }

                carrito = CarritoSerializers(data=data_carrito)

                if carrito.is_valid():
                    carrito.save()
                else:
                    print('carrito no valido')
                    return Response({'detail': 'Error al agregar producto al carrito'})
            
            # creo una nueva relacion de producto y carrito
            data = {
                'carrito': carrito.id,
                'producto': producto.id,
                'cantidad': producto_cantidad
            }

            relacion = RelacionCarritoProductoSerializers(data=data)
            if relacion.is_valid():
                relacion.save()
            else:
                print('relacion no valida')
                return Response({'detail': 'Error al agregar producto al carrito'})

            # actualizo el monto del carrito
            carrito.monto += (producto.precio * producto_cantidad)
            carrito.save()
            
            # atalizo la cantidad restante del producto
            producto.cantidad -= producto_cantidad
            producto.save()

            return Response({'detail':'Producto agregado correctamente'})

# Quitar producto del carrito
class QuitarProductoApiView(DestroyAPIView):
    queryset = RelacionCarritoProducto.objects.all()
    serializer_class = RelacionCarritoProductoSerializers

    def perform_destroy(self, instance):
        with transaction.atomic():
            producto = instance.producto
            producto.cantidad = instance.cantidad
            producto.save()
            return super().perform_destroy(instance)

# Finalizar carrito
class FinalizarCarritoApiView(UpdateAPIView):
    queryset = Carrito.objects.all()
    serializer_class = CarritoSerializers

    def perform_update(self, serializer):
        carrito = serializer.save()
        carrito.estado = 'finalizado'
        carrito.save()
        return super().perform_update(serializer)
