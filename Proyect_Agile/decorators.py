from ast import arg
from calendar import c
from .models import Proyecto, Miembro, Rol
from django.http import HttpResponse

def permisoVista(permiso):
    def decorator(view_func):
        def wrapper_func(request,*args,**kwargs):
            # Tratando de obtener el id del proyecto
            if 'id' in kwargs:
                print("funciona?")
                proyectoid = kwargs['id']
            elif 'idproyecto' in kwargs:
                proyectoid  = kwargs['idproyecto']
            else:
                proyectoid = kwargs['pk']
            
            print(proyectoid)
            # el usuario logueado
            usuario = request.user
            
            # comprobar si el miembro tiene el rol requerido
            miembro = Miembro.objects.filter(idproyecto=proyectoid,usuario=usuario).first()
            permisos = miembro.idrol.obtener_permisos()
            print(permisos)
            if permisos[permiso]:
                return view_func(request,*args,**kwargs)
            else:
                return HttpResponse("No tienes acceso a este modulo")
        return wrapper_func        
    return decorator
