from django.urls import path

from .apiviews import RecuperarPasswordApiView, CambiarPasswordApiView, UsuarioCreateApiView, UsuarioRetrieveApiView, UsuarioUpdateApiView, FinalizarRegistroApiView

urlpatterns = [
    path('crear/', UsuarioCreateApiView.as_view()),
    path('ver/<int:pk>/', UsuarioRetrieveApiView.as_view()),
    path('editar/<int:pk>/', UsuarioUpdateApiView.as_view()),
    path('finalizar-registro/<int:pk>/', FinalizarRegistroApiView.as_view()),
    path('recuperar-password/', RecuperarPasswordApiView.as_view()),
    path('cambiar-password/<pk>/', CambiarPasswordApiView.as_view()),
]