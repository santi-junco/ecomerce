from django.urls import path

from .apiviews import *

urlpatterns = [
    path('crear/', ProductoCreateApiView.as_view()),
    path('listar/', ProductosListApiView.as_view()),
    path('ver/<int:pk>/', ProductoRetrieveApiView.as_view()),
    path('editar/<int:pk>/', ProductoEditApiView.as_view()),
    path('eliminar/<int:pk>/', ProductoDeleteApiView.as_view()),
]