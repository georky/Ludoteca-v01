from datetime import datetime
from django.db import models
from django.utils import timezone
import pytz
# Creclass Curso(models.Model):
class Clientes(models.Model):
    telefono = models.CharField(primary_key=True, max_length=15)
    nombreC = models.CharField(max_length=100)
    nombreR = models.CharField(max_length=100)
    tiempoH = models.PositiveSmallIntegerField(null=False)
    mensaje = models.CharField(max_length=500,null=False)
    campo11 = models.DateTimeField(null=True)
    campo12 = models.DurationField(null=True)
    campo13 = models.IntegerField(null=True)
    campo1 = models.IntegerField(null=True)
    campo3 = models.CharField(max_length=100,null=True)
    campo4 = models.CharField(max_length=100,null=True)
    campo5 = models.CharField(max_length=100,null=True)
    campo6 = models.CharField(max_length=100,null=True)
   

    def __str__(self):
        texto = "{0} ({1})"
        return texto.format(self.nombreC, self.tiempoH)
    

        # return self.campo11.strftime("%Y-%m-%d %H:%M:%S")
