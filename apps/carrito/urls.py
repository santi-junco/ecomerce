from django.urls import path

from .apiviews import *

urlpatterns = [
    path('ver/<int:pk>/', ),
    path('eliminar/<int:pk>/', ),
]