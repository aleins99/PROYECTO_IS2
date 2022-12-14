from .models import *

from django import template
from .models import Miembro, Proyecto
from django.shortcuts import get_object_or_404
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User


# utlilidades para la creacion de las instancias de los modelos y otras facilidades

# crea el rol y asigna todos los permisos que deberia tener el scrum master
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


# crea el por defecto de equipo desarrollador
def crearRolEquipoDesarrollador(proyecto):
    ed = Rol()
    ed.idProyecto = proyecto
    ed.nombre = 'Equipo Desarrollador'
    ed.descripcion = 'Es parte del equipo de desarrollo del proyecto.'

    ed.save()
    return Rol.objects.order_by('-id')[0]


# funcion para asignar el rol de scrum master
def asignarRolScrumMaster(proyecto, usuario, rol):
    sm = Miembro()
    sm.idrol = rol
    sm.idproyecto = proyecto
    sm.usuario = usuario
    sm.cargahoraria = 0
    sm.isActivo = True
    sm.save()


# funcion para obtener permisos de un miembro
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


# retorna el nombre del proyecto

def nombreproyecto(proyecto):
    return proyecto.nombre


# retorna la lista de los proyectos en el sistema, no se pueden ver los proyectos a los que no pertenece el usuario
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
    miembro = Miembro.objects.filter(idproyecto=proyectoid, usuario=usuario).first()
    permisos = {}
    ban = False
    try:
        permisos = miembro.idrol.obtener_permisos()
        ban = True
    except:
        ban = False

    if not usuario.groups.filter(name='Administrador').exists() or ban:
        print("aca?")
        permisos = miembro.idrol.obtener_permisos()
    else:
        print("acaaa?")
        rol = Rol.objects.filter(nombre='admin').first()
        permisos = rol.obtener_permisos()
    return permisos


# obtener los campos de Rol
def importarRolProyecto(idproyecto, idrol):
    # el rol a importar
    rol = Rol.objects.get(id=idrol)
    proyecto = Proyecto.objects.get(id=idproyecto)
    rolImportado = Rol()

    # creamos un nuevo rol con los datos del rol a importar
    rolImportado = Rol.objects.create(nombre=rol.nombre, descripcion=rol.descripcion, idProyecto=proyecto)

    # copia todos los permisos de rol a rolImportado
    for field in Rol._meta.get_fields():
        if field.name.startswith('agregar') or field.name.startswith('eliminar') or field.name.startswith(
                'modificar') or field.name.startswith('crear') or field.name.startswith(
            'empezar') or field.name.startswith('finalizar'):
            value = getattr(rol, field.name)
            setattr(rolImportado, field.name, value)
    return rolImportado
