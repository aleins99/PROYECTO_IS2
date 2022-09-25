from gc import get_objects

from allauth.socialaccount.models import SocialAccount
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from .models import *
from .forms import *
from django.template.defaulttags import register
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .utilidades import *
from .decorators import *
from django.utils.decorators import method_decorator

estados_Proyecto = {
    'P':'Pendiente',
    'E':'En ejecucion',
    'C':'Cancelado',
    'F':'Finalizado',
}

@register.filter(name='has_group')
def has_group(user,groupname):
    return user.groups.filter(name=groupname).exists()

@register.filter
def get_at_index(list, index):
    return list[index]

@register.filter
def get_item(dictionary, key):
    return dictionary[key]

@register.filter
def esMiembroEnProyecto(element, idProyecto):
    user = User.objects.get(email__icontains=element.extra_data['email'])
    proyecto = get_object_or_404(Proyecto, pk=idProyecto)
    listaMiembros = Miembro.objects.filter(idproyecto=proyecto)
    existe = False
    if proyecto.scrumMaster == user:
        existe = True
    for x in listaMiembros:
        if x.usuario == user and x.isActivo:
            existe = True
    return existe

# USUARIO
def iniciosesion(request):
    login = reverse('account_login')
    return HttpResponseRedirect(login)

def ListarUsuarios(request, id):
    # lista de usuario del sistema autenticados por el sso
    listarUsuarios = SocialAccount.objects.order_by('id')
    context = {
        'usuarios': listarUsuarios,
        'idProyecto': id,
    }
    return render(request, 'Proyect_Agile/Usuario/listarUsuarios.html', context)
# The class crearProyecto inherits from CreateView, and it's model is Proyecto, it's template is
# proyect.html, it's form is ProyectoForm, and it's extra context is the ProyectoForm

# PROYECTO
def crearProyecto(request):
    if request.method == 'POST':
        formProyecto = ProyectoForm(request.POST)
        if formProyecto.is_valid():
            formProyecto.save()
            # crear el rol SM por debajo
            proyecto = Proyecto.objects.order_by('-id')[0]
            idRol = crearRolScrumMaster(proyecto)
            # asignar el rol al miembro SM que se asigno
            asignarRolScrumMaster(proyecto, proyecto.scrumMaster, idRol)

            return redirect('listarproyecto')
    else:
        formProyecto = ProyectoForm()
        formProyecto.fields["scrumMaster"].queryset = User.objects.all().exclude(username='admin')

    context = {'form': formProyecto}

    return render(request, 'Proyect_Agile/Proyecto/proyecto.html', context, None, 200)



class IniciarProyecto(View):
    def post(self, request, *args, **kwargs):
        obj = get_object_or_404(Proyecto, pk=self.kwargs['pk'])
        obj.estado = 'E'
        obj.save()
        return redirect(reverse_lazy('<iniciarproyecto>', kwargs={'pk': obj.pk}))


def listarProyectos(request):

    template_name = 'Proyect_Agile/Proyecto/listarProyectos.html'

    scrum=request.user


    usuario = request.user.groups.filter(name='Administrador').exists()
    proyectos = obtenerlistaDeProyectosUser(request)
    context = {
        'estados': estados_Proyecto,
        'Administrador': usuario,
        'proyectos': proyectos,
        'usuario' : scrum
    }

    return render(request, template_name, context)


class editarProyecto(UpdateView):
    model= Proyecto
    template_name = 'Proyect_Agile/Proyecto/editarProyecto.html'
    form_class = ProyectoForm


@login_required(login_url="login")
def verproyecto(request,id):
    if request.method == 'POST':
        obj = Proyecto.objects.get(id=id)
        obj.estado = 'E'
        obj.save()
        return redirect(reverse_lazy('verproyecto', kwargs={'id': obj.pk}))

    scrum = False
    proyecto = Proyecto.objects.get(id=id)
    proyecto_id = str(id)
    rol = ''
    try:

        usuarios = Miembro.objects.filter(idproyecto=id, usuario=request.user).first()


        rol = usuarios.idrol
    except:
        pass

    if request.user == proyecto.scrumMaster:
        scrum = True

    permisosUsuario = obtenerPermisos(id, request.user)
    context = {
        'proyecto':proyecto,
        'estados': estados_Proyecto,
        'proyecto_id':proyecto_id,
        'scrum': scrum,
        'rol': rol,
        'permisos': permisosUsuario
    }
    return render(request,'Proyect_Agile/Proyecto/verProyecto.html', context)


def listarProyectosAdmin(request):
    template_name = 'Proyect_Agile/Proyecto/listarProyectosAdmin.html'

    scrum = request.user
    proyectos = Proyecto.objects.all()
    context = {
        'estados': estados_Proyecto,
        'proyectos': proyectos,
    }

    return render(request, template_name, context)


# MIMBRO
@login_required(login_url="login")
def miembrosProyecto(request, id):
    proyecto = get_object_or_404(Proyecto, pk=id)
    rol = Rol.objects.filter(idProyecto=id, nombre="Scrum Master").first()
    listaMiembros = Miembro.objects.filter(idproyecto=proyecto).exclude(idrol=rol)
    permisos = obtenerPermisosProyecto(request, proyecto)

    usuario = request.user

    proyecto_id = str(id)

    scrum= False

    if request.user == proyecto.scrumMaster:
        scrum = True

    permisosMiembro = obtenerPermisos(id, request.user)
    context = {
        'proyecto':proyecto,
        'estados': estados_Proyecto,
        'proyecto_id':proyecto_id,
        'scrum': scrum,
        'miembros': listaMiembros,
        'usuario' : usuario,
        'permisos': permisosMiembro
    }
    return render(request, 'Proyect_Agile/Miembros/proyectoMiembros.html', context)

@permisoVista(permiso="agregarMiembro")
def formCrearMiembro(request, id, socialUserId):
    socialUser = get_object_or_404(SocialAccount, pk=socialUserId)
    user = User.objects.get(email__icontains=socialUser.extra_data['email'])
    proyecto = get_object_or_404(Proyecto, pk=id)
    miembro = Miembro.objects.filter(usuario=user.id, idproyecto=proyecto).first()

    if request.method == 'POST':
        # Se muestra el cuadro de crear miembro
        formMiembrosProyecto = MiembroForm(request.POST)
        if formMiembrosProyecto.is_valid():
            formMiembrosProyecto.save()
        return redirect('miembrosproyecto', id)
    else:
        if miembro:
            miembro.isActivo = True
            # Se muestra el cuadro de editar
            miembro.save()
            return redirect('miembrosproyecto', id)
        else:
            formMiembrosProyecto = MiembroForm()
            formMiembrosProyecto.fields["idproyecto"].initial = proyecto
            formMiembrosProyecto.fields["usuario"].initial = user
            formMiembrosProyecto.fields["isActivo"].initial = True
            # se busca el rol SM_under que se excluye
            rol = Rol.objects.filter(idProyecto=id, nombre="Scrum Master").first()
            # se excluye el rol
            formMiembrosProyecto.fields["idrol"].queryset = Rol.objects.filter(idProyecto=proyecto).exclude(
                nombre="Scrum Master")
            context = {
                'formMiembroProyecto': formMiembrosProyecto,
                'idProyecto': id,
                'Usuario': user
            }
            return render(request, 'Proyect_Agile/Miembros/agregarMiembro.html', context, None, 200)


@method_decorator(permisoVista(permiso="modificarMiembro"), name='dispatch')
class editarMiembro(UpdateView):
    model= Miembro
    template_name = 'Proyect_Agile/Miembros/editarMiembro.html'
    form_class = MiembroForm

    def get_success_url(self):
        id = self.kwargs['idproyecto']
        return reverse('miembrosproyecto',kwargs={'id':id})


### ROLES ###
@permisoVista(permiso="crearRol")
def crearRol(request, id):
    proyecto = Proyecto.objects.get(id=id)
    if request.method == 'POST':
        formrol = rolForm(request.POST)
        if formrol.is_valid():
            formrol.save()
        return redirect('rolproyecto', id)
    else:
        formrol = rolForm()
        formrol.fields['idProyecto'].initial = proyecto
        context = {
            'form': formrol
        }
        return render(request, 'Proyect_Agile/Rol/crearRol.html', context)


def verRolProyecto(request, id):
    proyecto = Proyecto.objects.get(id=id)
    usuario = request.user
    roles = Rol.objects.filter(idProyecto=proyecto)
    context = {
        'roles': roles,
        'proyecto': proyecto,
        'usuario': usuario,
        'estados': estados_Proyecto,
    }
    return render(request, 'Proyect_Agile/Rol/verRolesProyecto.html', context)


### USER STORY ###
class crearUser_Story(CreateView):
    model = User_Story
    template_name = 'Proyect_Agile/us.html'
    form_class = UserStoryForm
    extra_context = {'form': UserStoryForm }
@method_decorator(permisoVista(permiso="modificarRol"), name='dispatch')
class editarRol(UpdateView):
    model= Rol
    template_name = 'Proyect_Agile/Rol/editarRol.html'
    form_class = rolForm

    def get_success_url(self):

        id = self.kwargs['idproyecto']

        print(id)

        return reverse('rolproyecto',kwargs={'id':id})


def verDocumentacion(request):

    context={}

    return render(request,'Proyect_Agile/Docs/Documentacion_index.html',context)
