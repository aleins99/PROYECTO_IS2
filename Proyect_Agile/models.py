from datetime import datetime
from django.db import models
from django.contrib.postgres.fields import ArrayField
from allauth.account.models import EmailAddress
from allauth import app_settings
from allauth.account.models import EmailAddress
# Create your models here
class Proyecto(models.Model):

    nombre = models.CharField(max_length=200, null=False, blank=False)
    descripcion = models.TextField(null= True, blank= True, max_length=200)
    miembros = models.ManyToManyField('Miembro')
    scrumMaster = models.ForeignKey(EmailAddress, on_delete=models.RESTRICT, blank=False)
    fechainicio = models.DateField(default=datetime.now)
    fechafin = models.DateField(blank=False, null=False)
    ESTADOS = (

        ('P', 'Pendiente'),
        ('E', 'En ejecucion'),
        ('C' , 'Cancelado'),
        ('F', 'Finalizado'),
    )
    estado = models.CharField(max_length=1 , choices=ESTADOS , default= 'P')
    def __str__(self):
       return self.nombre

    def get_absolute_url(self):
        return '/Proyecto'
class Miembro(models.Model):	
    correo = models.ForeignKey(EmailAddress, on_delete=models.RESTRICT, null=True, blank=False)
    cargahoraria = models.IntegerField(default=0)
    def __str__(self):
       return self.correo.email
class Rol(models.Model):

    idProyecto = models.ForeignKey(Proyecto, on_delete=models.RESTRICT)  # Proyecto al que pertenece el rol
    nombre = models.CharField(max_length=250)
    descripcion = models.TextField()  # Describir el rol

    # Campos de Permisos
    agregarUserStory = models.BooleanField(default=False)
    eliminarUserStory = models.BooleanField(default=False)
    modificarUserStory = models.BooleanField(default=False)
    agregarMiembro = models.BooleanField(default=False)
    modificarMiembro = models.BooleanField(default=False)
    eliminarMiembro = models.BooleanField(default=False)
    crearRol = models.BooleanField(default=False)
    modificarRol = models.BooleanField(default=False)
    eliminarRol = models.BooleanField(default=False)
    crearSprint = models.BooleanField(default=False)
    empezarSprint = models.BooleanField(default=False)
    finalizarSprint = models.BooleanField(default=False)
    agregarSprintBacklog = models.BooleanField(default=False)
    modificarSprintBacklog = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre


class TipoUS(models.Model):

    nombre= models.CharField(max_length=100)

    ESTADOS = [
        ('N', 'Nuevo'),
        ('PP', 'En Planning Pocker'),
        ('P', 'Pendiente'),
        ('EP', 'En Proceso'),
        ('STSA', 'Sin Terminar Sprint Anterior'),
        ('A', 'Aprobado'),
        ('H', 'Hecho'),
        ('C', 'Cancelado'),
    ]
class User_Story(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    comentarios = models.TextField()
    estimaciones = models.IntegerField()
    historial = models.TextField()
    UP = models.IntegerField()
    BV = models.IntegerField()
    tipo = models.ForeignKey(TipoUS , on_delete=models.RESTRICT)
    estado = models.CharField(max_length=10,default='N')
