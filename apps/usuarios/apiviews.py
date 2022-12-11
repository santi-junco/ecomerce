from .models import Usuarios
from .serializers import UsuariosSerializers

from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from django.db import transaction
from django.conf import settings
from django.http.response import HttpResponseRedirect
from django.contrib.auth.hashers import make_password

from apps.core.email import enviarMail
from apps.core.exception import CustomException
from apps.core.crypt import encrypt, decrypt

# Crear usuario
class UsuarioCreateApiView(CreateAPIView):
    serializer_class = UsuariosSerializers
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        with transaction.atomic():
            usuario = serializer.save()
            usuario.username = usuario.email
            usuario.password = make_password(self.request.data['password'])
            usuario.save()
            
            url = f'{settings.URL_BASE}{settings.PORT_BACK}api/v1/usuarios/finalizar-registro/{usuario.id}'

            enviarMail('registro', 'Registro Exitoso', usuario.email, url )

        # return super().perform_create(serializer)

# Ver usuario
class UsuarioRetrieveApiView(RetrieveAPIView):
    queryset = Usuarios.objects.all()
    serializer_class = UsuariosSerializers

# Editar usuario
class UsuarioUpdateApiView(UpdateAPIView):
    queryset = Usuarios.objects.all()
    serializer_class = UsuariosSerializers

    def perform_update(self, serializer):
        with transaction.atomic():
            usuario = serializer.save()
            usuario.username = usuario.email
            if self.request.data.get('password', None):
                usuario.password = make_password(self.request.data['password'])
            usuario.save()

            return super().perform_update(serializer)

# Finalizar registro
class FinalizarRegistroApiView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        with transaction.atomic():
            try:
                usuario = Usuarios.objects.get(id=pk)
            except:
                url = f'{settings.URL_BASE}{settings.PORT_FRONT}{settings.PATH_ERROR}'
                return HttpResponseRedirect(redirect_to=url)

            if usuario.is_active:
                url = f'{settings.URL_BASE}{settings.PORT_FRONT}{settings.PATH_ERROR_VERIF}'
                return HttpResponseRedirect(redirect_to=url)

            usuario.is_active = True
            usuario.save()
            
            url = f'{settings.URL_BASE}{settings.PORT_FRONT}{settings.PATH_URL_REDIRECT}'
            return HttpResponseRedirect(redirect_to=url)

# Recuperar contraseña
class RecuperarPasswordApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        with transaction.atomic():
            email = request.data.get('email')
            if not email:
                raise CustomException('Debe ingresar un email valido')

            try:
                usuario = Usuarios.objects.get(email=email)
                id_encypt = encrypt(usuario.id)
            except:
                raise CustomException('Usuario no encontrado')

            url = f'{settings.URL_BASE}{settings.PORT_FRONT}auth/change-password/{id_encypt}'
            tipo = 'recuperarContraseña'
            asunto = 'Recuperacion de Contraseña'

            enviarMail(tipo, asunto, email, url)

            print(id_encypt)

            return Response({'detail': 'Se envio un email para recuperar la contraseña'}, status=200)

# Cambiar contraseña
class CambiarPasswordApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, pk):
        with transaction.atomic():
            id = decrypt(pk)

            try:
                usuario = Usuarios.objects.get(id=id)
            except:
                raise CustomException('Error al obtener usuario')

            password_body = request.data.get('password', None)
            if not password_body:
                raise CustomException('Debe ingresar una contraseña')

            usuario.password = make_password(password_body)
            usuario.save()

            url = f'{settings.URL_BASE}{settings.PORT_FRONT}auth/login'
            tipo = 'contraseñaCambiada'
            asunto = 'Cambio de contraseña exitosa'
            
            enviarMail(tipo, asunto, usuario.email, url)

            return Response({'detail': 'Contraseña modificada exitosamente'}, status=200)

