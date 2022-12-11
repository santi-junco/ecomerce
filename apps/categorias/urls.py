from django.urls import path

from .apiviews import *

urlpatterns = [
    path('crear/', CategoriaCreateApiView.as_view()),
    path('listar/', CategoriasListApiview.as_view()),
    path('ver/<int:pk>/', CategoriaRetrieveApiView.as_view()),
    path('editar/<int:pk>/', CategoriasEditApiView.as_view()),
    path('eliminar/<int:pk>/', CategoriasDeleteApiView.as_view()),
]