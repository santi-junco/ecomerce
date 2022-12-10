from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.core.exception import CustomException
from apps.usuarios.models import Usuarios

from django.db import transaction

class CustomeTokenObtainPairView(TokenObtainPairView):
    def get_serializer_class(self):
        try:
            usuario = Usuarios.objects.get(email=self.request.data['email'])
        except:
            raise CustomException("Usuario no encontado")

        if not usuario.is_active:
            raise CustomException("Debe activar su cuenta para iniciar sesion")
        
        return CustomeTokenObtainPairSerializer

class CustomeTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        with transaction.atomic():

            token = super().get_token(user)

            token['usuario'] = {
                'email': user.email,
                'nombre': user.first_name,
                'apellido': user.last_name,
                'super_user': user.is_superuser
            }

            return token