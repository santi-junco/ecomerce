from django.db import models
from django.core.validators import FileExtensionValidator

from apps.core.models import TimeStampedModel
from apps.usuarios.models import Usuarios

class Productos(TimeStampedModel):
    nombre = models.CharField(max_length=50, null=False, blank=False)
    descripcion = models.TextField(null=True, blank=True)
    precio = models.DecimalField(max_digits=7, decimal_places=2, null=False, blank=False)
    cantidad = models.PositiveIntegerField(null=False, blank=False)

    class Meta:
        db_table = "productos_Productos"
        verbose_name_plural = "Productos"

class Imagenes(TimeStampedModel):
    producto = models.ForeignKey(Productos, null=False, blank=False, on_delete=models.CASCADE)
    imagen = models.FileField(null=False, blank=False, upload_to='producto/', validators=[FileExtensionValidator(['jpg', 'jpeg', 'PNG'])])

    class Meta:
        db_table = 'productos_Imagen'
        verbose_name_plural = 'Imagenes'

# Realcion Usuario Producto
class Favorito(TimeStampedModel):
    usuario = models.ForeignKey(Usuarios, null=False, blank=False, on_delete=models.CASCADE)
    producto = models.ForeignKey(Productos, null=False, blank=False, on_delete=models.CASCADE)

    class Meta:
        db_table = "productos_Favoritos"
        verbose_name_plural = "Favoritos"