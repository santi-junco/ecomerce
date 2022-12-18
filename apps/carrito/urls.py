from django.urls import path

from .apiviews import *

urlpatterns = [
    path('agregar/', AgregarProductoApiView.as_view()),
    path('quitar/<int:pk>/', QuitarProductoApiView.as_view()),
    path('ver/<user>/', CarritoEnCursoRetrieveApiView.as_view()),
    path('ver-finalizados/<user>/', CarritoFinalizadoListApiView.as_view()),
    path('eliminar/<int:pk>/', CarritoDeleteApiView.as_view()),
    path('finalizar/<int:pk>/', FinalizarCarritoApiView.as_view())
]