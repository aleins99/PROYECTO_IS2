from datetime import datetime
from django.db import models
from django.contrib.postgres.fields import ArrayField
from allauth import app_settings
from django.contrib.auth.models import Permission, User, GroupManager
# Create your models here 

# Modelo para los proyectos
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

# Modelo para los miembros dentro de un proyecto en especifico
class Miembro(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, blank=True)
    cargahoraria = models.IntegerField(default=0)
    idproyecto = models.ForeignKey(Proyecto, on_delete=models.RESTRICT, null=True)
    idrol = models.ForeignKey('Rol', on_delete=models.RESTRICT, null=True, blank=True)
    isActivo = models.BooleanField(default=False)

    def __str__(self):
        return self.usuario.first_name


# Modelo para los roles dentro de un proyecto en especifico
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

# Modelo para los tipos de us dentro de un proyecto en especifico
class TipoUS(models.Model):

    nombre= models.CharField(max_length=100)

    idproyecto = models.ForeignKey(Proyecto, on_delete=models.RESTRICT, null=True)
    estado = models.TextField(default= 'Por hacer, En Proceso, Hecho, Cancelado')


    def __str__(self):
        return self.nombre

# Modelo para los us primitivos ( que aun no se agregan al sprint backlog )
class User_Story(models.Model):
    idproyecto = models.ForeignKey(Proyecto, on_delete=models.RESTRICT, null=True)
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    comentarios = models.TextField()
    historial = models.TextField(blank=True)
    tipo = models.ForeignKey(TipoUS , on_delete=models.RESTRICT)
    estado = models.CharField(max_length=30,default='Pendiente')

    #encargado = models.ForeignKey(User, on_delete=models.RESTRICT, null=True, blank=True)  # Miembro encargado en trabajar el

    def __str__(self):
        return self.nombre

# Modelo para un sprint de un proyecto en especifico
class Sprint(models.Model):
    nombre = models.CharField(max_length=200)
    fechainicio = models.DateField(default=datetime.now)
    fechafin = models.DateField(blank=False, null=False)
    idproyecto = models.ForeignKey(Proyecto, on_delete=models.RESTRICT)
    numero = models.IntegerField(null=True)
    ESTADOS = (
        ('P', 'Pendiente'),
        ('E', 'En ejecucion'),
        ('F', 'Finalizado'),
    )
    estado = models.CharField(max_length=1, choices=ESTADOS, default='P')
    def __str__(self):
        return self.nombre

# Modelo para el planning poker de un proyecto ( se complementa el modelo de us primitivo con este )
# Se trata de un modelo para los us que van a pasar al sprint backlog
class PlanningPoker(models.Model):
    ESTADOS = (
        ('N', 'Nuevo'),
        ('PP', 'En Planning Pocker'),
        ('P', 'Pendiente'),
        ('EP', 'En Proceso'),
        ('STSA', 'Sin Terminar en Sprint Anterior'),
        ('A', 'Aprobado'),
        ('H', 'Hecho'),
        ('C', 'Cancelado'),
    )

    estimacion = models.FloatField()  # Estimacion en horas
    UP= models.IntegerField(blank=True, null=True)  # Estimacion en horas
    BV = models.IntegerField(blank=True, null=True)
    prioridad = models.FloatField(blank=True, null=True)
    # miembroSM = models.ForeignKey(miembros, on_delete=models.RESTRICT)
    estado = models.CharField(max_length=4, choices=ESTADOS, default='N')
    miembroEncargado = models.ForeignKey(Miembro, on_delete=models.RESTRICT)  # Al definirse debe de tener un encargado si o si
    idUs = models.ForeignKey(User_Story, on_delete=models.RESTRICT)
    idSprint = models.ForeignKey(Sprint, on_delete=models.RESTRICT)  # Debe pertenecer a un sprintPlanning#o idSprint

