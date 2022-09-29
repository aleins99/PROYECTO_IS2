from datetime import datetime
from django.db import models
from django.contrib.postgres.fields import ArrayField
from allauth import app_settings
from django.contrib.auth.models import Permission, User, GroupManager
# Create your models here
class Proyecto(models.Model):
    nombre = models.CharField(max_length=200, null=False, blank=False)
    descripcion = models.TextField(null= True, blank= True, max_length=200)
    miembros = models.ManyToManyField('Miembro')
    scrumMaster = models.ForeignKey(User, on_delete=models.RESTRICT, blank=False)
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
    usuario = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, blank=True)
    cargahoraria = models.IntegerField(default=0)
    idproyecto = models.ForeignKey(Proyecto, on_delete=models.RESTRICT, null=True)
    idrol = models.ForeignKey('Rol', on_delete=models.RESTRICT, null=True, blank=True)
    isActivo = models.BooleanField(default=False)

    def __str__(self):
        return self.usuario.first_name


class Rol(models.Model):
    idProyecto = models.ForeignKey(Proyecto, on_delete=models.RESTRICT, null=True , blank=True)  # Proyecto al que pertenece el rol
    nombre = models.CharField(max_length=250)
    descripcion = models.TextField(null=True , blank=True)  # Describir el rol

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

    def obtener_permisos(self):
        return {
            'agregarUserStory': self.agregarUserStory,
            'eliminarUserStory': self.eliminarUserStory,
            'modificarUserStory': self.modificarUserStory,
            'agregarMiembro': self.agregarMiembro,
            'modificarMiembro': self.modificarMiembro,
            'eliminarMiembro': self.eliminarMiembro,
            'crearRol': self.crearRol,
            'modificarRol': self.modificarRol,
            'eliminarRol': self.eliminarRol,
            'crearSprint': self.crearSprint,
            'empezarSprint': self.empezarSprint,
            'finalizarSprint': self.finalizarSprint,
            'agregarSprintBacklog': self.agregarSprintBacklog,
            'modificarSprintBacklog': self.modificarSprintBacklog,
        }

    def __str__(self):
        return self.nombre


class TipoUS(models.Model):

    nombre= models.CharField(max_length=100)

    idproyecto = models.ForeignKey(Proyecto, on_delete=models.RESTRICT, null=True)
    estado = models.TextField(default= 'Por hacer, En Proceso, Hecho, Cancelado')


    def __str__(self):
        return self.nombre

class User_Story(models.Model):
    idproyecto = models.ForeignKey(Proyecto, on_delete=models.RESTRICT, null=True)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    comentarios = models.TextField()
    estimaciones = models.IntegerField()
    historial = models.TextField(blank=True)
    UP = models.IntegerField()
    BV = models.IntegerField()
    tipo = models.ForeignKey(TipoUS , on_delete=models.RESTRICT)
    estado = models.CharField(max_length=30,default='Pendiente')

    def __str__(self):
        return self.nombre


class Sprint(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    fechainicio = models.DateField(default=datetime.now)
    fechafin = models.DateField(blank=False, null=False)
    idproyecto = models.ForeignKey(Proyecto, on_delete=models.RESTRICT)
    ESTADOS = (
        ('P', 'Pendiente'),
        ('E', 'En ejecucion'),
        ('F', 'Finalizado'),
    )
    estado = models.CharField(max_length=1, choices=ESTADOS, default='P')
    def __str__(self):
        return self.nombre