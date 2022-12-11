from django.db import models

from apps.core.models import TimeStampedModel
from apps.producto.models import Productos

class Categorias(TimeStampedModel):
    nombre = models.CharField(max_length=50, null=False, blank=False)

    class Meta:
        db_table = "categorias_Categorias"
        verbose_name_plural = "Categorias"

class RelacionCategoriasProductos(TimeStampedModel):
    categoria = models.ForeignKey(Categorias, null=False, blank=False, on_delete=models.CASCADE)
    producto = models.ForeignKey(Productos, null=False, blank=False, on_delete=models.CASCADE)

    class Meta:
        db_table = "categorias_RelacionCategoriasProductos"
        verbose_name_plural = "Relacion Categorias Productos"
