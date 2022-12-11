from django.db import models

from apps.core.models import TimeStampedModel

class Categorias(TimeStampedModel):
    nombre = models.CharField(max_length=50, null=False, blank=False)

    class Meta:
        db_table = "categorias_Categorias"
        verbose_name_plural = "Categorias"

