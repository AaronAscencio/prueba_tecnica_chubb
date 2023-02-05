from django.db import models
from django.forms.models import model_to_dict

# Create your models here.

class Ruleta(models.Model):
    estatus = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Ruleta No. {self.pk} Estatus {self.get_estatus()}'
    
    def get_estatus(self):
        return 'Abierta' if self.estatus else 'Cerrada'

    def toJSON(self):
        item = model_to_dict(self)
        item['estatus'] = self.get_estatus()
        return item



    

