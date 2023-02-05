from django.db import models
from core.ruleta.models import Ruleta

# Create your models here.
class Apuesta(models.Model):
    ruleta = models.ForeignKey(Ruleta, on_delete=models.CASCADE)
    usuario = models.CharField(max_length=100)
    cantidad = models.PositiveIntegerField()
    numero = models.PositiveSmallIntegerField(null=True)
    color = models.CharField(max_length=10, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'Apuesta No.{self.pk} en la Ruleta No{self.ruleta.pk}'