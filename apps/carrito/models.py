from django.db import models

from apps.producto.models import Productos
from apps.usuarios.models import Usuarios
from apps.core.models import TimeStampedModel

ESTADO_CARRITO_CHOICES = (
    ('en curso','en curso'),
    ('finalizado','finalizado')
)

class Carrito(TimeStampedModel):
    usuario = models.ForeignKey(Usuarios, null=False, blank=False, on_delete=models.CASCADE)
    estado = models.CharField(max_length=15, choices=ESTADO_CARRITO_CHOICES, default='en curso')
    monto = models.DecimalField(max_digits=7, decimal_places=2, default=0)

    class Meta:
        db_table = 'carrito_Carrito'
        verbose_name_plural = 'Carritos'

class RelacionCarritoProducto(TimeStampedModel):
    producto = models.ForeignKey(Productos, null=False, blank=False, on_delete=models.PROTECT)
    carrito = models.ForeignKey(Carrito, null=False, blank=False, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = 'carrito_RelacionCarritoProducto'
        verbose_name_plural = 'Relacion Carrito Productos'
