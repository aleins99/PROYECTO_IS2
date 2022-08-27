from django.db import models

# Create your models here
class Proyecto(models.Model):
    nombre = models.CharField(max_length=30)
    miembros = models.CharField(max_length=20)
