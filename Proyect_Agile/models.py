from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here
class Proyecto(models.Model):
    nombre = models.CharField(max_length=30)
    miembros = models.ManyToManyField('Miembro')
    descripción = models.TextField(null= True, blank= True)
    fechainicio = models.DateTimeField()
    fechafin = models.DateTimeField()
    usbacklog = models.ArrayField(ArrayField( models.ForeignKey('US') ))

    historialreuniones = 


class Miembro(models.Model):
    usuario =
    izquierdo = models.webo(max_length=2)