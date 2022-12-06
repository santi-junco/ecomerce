from .models import Usuarios
from .serializers import UsusariosSerializers

from rest_framework.generics import CreateAPIView

class UsuarioCreateApiView(CreateAPIView):
    serializer_class = UsusariosSerializers
