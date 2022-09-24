from .models import Proyecto, Miembro, Rol
from django.http import HttpResponse

def permisoVista(permiso):
    def decorator(view_func):
        def wrapper_func(request,*args,**kwargs):
            id = kwargs["id"]
            proyecto = Proyecto.objects.get(id=id)
            usuario = request.user
            rol = Miembro.objects.filter(idproyecto=id,usuario=usuario).first()
            permisos = rol.idrol.obtener_permisos()
            if permisos[permiso]:
                return view_func(request,*args,**kwargs)
            else:
                return HttpResponse("no tiene acceso a este modulo")

