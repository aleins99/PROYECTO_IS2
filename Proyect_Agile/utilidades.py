from .models import *

from django import template
from .models import Miembro,Proyecto
from django.shortcuts import get_object_or_404
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User







def crearRolScrumMaster(proyecto):
    sm = Rol()
    sm.idProyecto = proyecto
    sm.nombre = 'Scrum Master'
    sm.descripcion = 'Es la figura que lidera a los equipos en la gestión ágil de proyectos.'
    sm.agregarUserStory = True
    sm.eliminarUserStory = True
    sm.modificarUserStory = True
    sm.agregarMiembro = True
    sm.modificarMiembro = True
    sm.eliminarMiembro = True
    sm.crearRol = True
    sm.modificarRol = True
    sm.eliminarRol = True
    sm.crearSprint = True
    sm.empezarSprint = True
    sm.finalizarSprint = True
    sm.agregarSprintBacklog = True
    sm.modificarSprintBacklog = True
    sm.save()
    return Rol.objects.order_by('-id')[0]


def asignarRolScrumMaster(proyecto, usuario, rol ):
    sm = Miembro()
    sm.idrol = rol
    sm.idproyecto = proyecto
    sm.usuario = usuario
    sm.cargahoraria = 0
    sm.isActivo = True
    sm.save()




