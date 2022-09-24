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

def crearRolEquipoDesarrollador(proyecto):
    ed = Rol()
    ed.idProyecto = proyecto
    ed.nombre = 'Equipo Desarrollador'
    ed.descripcion = 'Es parte del equipo de desarrollo del proyecto.'

    ed.save()
    return Rol.objects.order_by('-id')[0]


def asignarRolScrumMaster(proyecto, usuario, rol ):
    sm = Miembro()
    sm.idrol = rol
    sm.idproyecto = proyecto
    sm.usuario = usuario
    sm.cargahoraria = 0
    sm.isActivo = True
    sm.save()


def obtenerPermisosProyecto(request, proyecto):
    # obtenemos los datos del miembro
    miembro = Miembro.objects.all().filter(idproyecto=proyecto, usuario=request.user).first()
    permisos = []
    # si el user es miembro del proyecto
    if miembro:
        rol = miembro.idrol
        # cargar permisos
        permisos.append(rol.agregarUserStory)
        permisos.append(rol.eliminarUserStory)
        permisos.append(rol.modificarUserStory)
        permisos.append(rol.agregarMiembro)
        permisos.append(rol.modificarMiembro)
        permisos.append(rol.eliminarMiembro)
        permisos.append(rol.crearRol)
        permisos.append(rol.modificarRol)
        permisos.append(rol.eliminarRol)
        permisos.append(rol.crearSprint)
        permisos.append(rol.empezarSprint)
        permisos.append(rol.finalizarSprint)
        permisos.append(rol.agregarSprintBacklog)
        permisos.append(rol.modificarSprintBacklog)

    else:
        # verificamos si el user es scrum master
        if request.user == proyecto.scrumMaster:
            # cargar permisos
            permisos.append(True)
            permisos.append(True)
            permisos.append(True)
            permisos.append(True)
            permisos.append(True)
            permisos.append(True)
            permisos.append(True)
            permisos.append(True)
            permisos.append(True)
            permisos.append(True)
            permisos.append(True)
            permisos.append(True)
            permisos.append(True)
            permisos.append(True)
    # retornamos una lista de permisos o una lista vacia
    return permisos

def nombreproyecto(proyecto):
    return proyecto.nombre

def obtenerlistaDeProyectosUser(request):
    listaDeProyectos = list(Proyecto.objects.filter(scrumMaster=request.user))
    miembro = Miembro.objects.filter(usuario=request.user, isActivo=True)
    for x in miembro:
        if not x.idproyecto in listaDeProyectos:
            listaDeProyectos.append(x.idproyecto)
    listaDeProyectos.sort(key=nombreproyecto)
    return listaDeProyectos


# obtener los permisos del usuario
def obtenerPermisos(proyectoid, usuario):
    miembro = Miembro.objects.filter(idproyecto=proyectoid,usuario=usuario).first()
    permisos = miembro.idrol.obtener_permisos()
    return permisos





