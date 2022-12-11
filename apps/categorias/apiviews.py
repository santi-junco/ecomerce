from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

from .seriralizers import CategoriaSerializers
from .models import Categorias

# crear
class CategoriaCreateApiView(CreateAPIView):
    serializer_class = CategoriaSerializers

# listar
class CategoriasListApiview(ListAPIView):
    queryset = Categorias.objects.all()
    serializer_class = CategoriaSerializers

# Ver
class CategoriaRetrieveApiView(RetrieveAPIView):
    queryset = Categorias.objects.all()
    serializer_class = CategoriaSerializers

# Editar
class CategoriasEditApiView(UpdateAPIView):
    queryset = Categorias.objects.all()
    serializer_class = CategoriaSerializers

class CategoriasDeleteApiView(DestroyAPIView):
    queryset = Categorias.objects.all()
    serializer_class = CategoriaSerializers

