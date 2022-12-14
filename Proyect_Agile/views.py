from gc import get_objects

from allauth.socialaccount.models import SocialAccount
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import *
from .forms import *
from django.template.defaulttags import register
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .utilidades import *
from .decorators import *
from django.utils.decorators import method_decorator
from allauth.account.models import EmailAddress
from django.contrib.auth.models import AbstractUser
from allauth.utils import get_user_model
from django.core.mail import send_mail
from plotly.offline import plot
from plotly.graph_objs import Scatter

from django.http import JsonResponse
# estados por defecto de los proyectos
estados_Proyecto = {
    'P': 'Pendiente',
    'PP': 'En Planning Poker',
    'E': 'En ejecucion',
    'EP': 'En Proceso',
    'STSA': 'Sin Terminar en Sprint Anterior',
    'A': 'Aprobado',
    'C': 'Cancelado',
    'F': 'Finalizado',
}


@register.filter
def cambiarEstado(us):
    print(us)
@register.filter
def tarea(us):
    tareas = Tarea.objects.filter(idUs=us)
    if tareas:
        print("true")
        return True
    print("false")
    return False


@register.filter
def idtipo(idsprint):
    # get the us of the sprint with estado != F
    if idsprint.estado != 'F':
        us = User_Story.objects.filter(idSprint=idsprint).first()
        if us:
            return us.tipo.id
    return 1


@register.filter
def toString(value):
    text = str(value)
    return text


# para decoradores
@register.filter
def tareasUS(US):
    return tarea.objects.filter(idUs=US)


@register.filter(name='has_group')
def has_group(user, groupname):
    return user.groups.filter(name=groupname).exists()


@register.filter
def get_at_index(list, index):
    return list[index]


@register.filter
def get_item(dictionary, key):
    return dictionary[key]


# comprueba si el miembro es parte del proyecto en cuestion
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


### USUARIO ###
def iniciosesion(request):
    login = reverse('account_login')
    return HttpResponseRedirect(login)


# editar perfil de un usuario
class editarPerfil(UpdateView):
    model = get_user_model()
    form_class = UsuarioForm
    template_name = 'Proyect_Agile/Usuario/editarUsuario.html'
    success_url = '/'


# lista de usuarios en el sistema
def ListarUsuarios(request, id):
    # lista de usuario del sistema autenticados por el sso
    listarUsuarios = SocialAccount.objects.order_by('id')
    context = {
        'usuarios': listarUsuarios,
        'idProyecto': id,
    }
    return render(request, 'Proyect_Agile/Usuario/listarUsuarios.html', context)


### PROYECTO ###
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


# Iniciar el proyecto
class IniciarProyecto(View):
    def post(self, request, *args, **kwargs):
        obj = get_object_or_404(Proyecto, pk=self.kwargs['pk'])
        obj.estado = 'E'
        obj.save()
        return redirect(reverse_lazy('<iniciarproyecto>', kwargs={'pk': obj.pk}))


# lista de proyectos en el sistema
@login_required(login_url="login")
def listarProyectos(request):
    if request.user.id == 1 or request.user.id == 2:
        # create a group for the user admin
        group, created = Group.objects.get_or_create(name='Administrador')
        rol, created = Rol.objects.get_or_create(nombre='admin')
        group.user_set.add(request.user)

    template_name = 'Proyect_Agile/Proyecto/listarProyectos.html'
    scrum = request.user
    usuario = request.user.groups.filter(name='Administrador').exists()
    proyectos = obtenerlistaDeProyectosUser(request)

    context = {
        'estados': estados_Proyecto,
        'Administrador': usuario,
        'proyectos': proyectos,
        'usuario': scrum
    }

    return render(request, template_name, context)


# editar un proyecto del sistema
class editarProyecto(UpdateView):
    model = Proyecto
    template_name = 'Proyect_Agile/Proyecto/editarProyecto.html'
    form_class = ProyectoForm
    success_url = '/'


# ver detalles de un proyecto del sistema
def verproyecto(request, id):
    if request.method == 'POST':
        obj = Proyecto.objects.get(id=id)
        obj.estado = 'E'
        obj.save()
        return redirect(reverse_lazy('verproyecto', kwargs={'id': obj.pk}))

    scrum = False
    proyecto = Proyecto.objects.get(id=id)
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
        'proyecto': proyecto,
        'estados': estados_Proyecto,
        'proyecto_id': id,
        'scrum': scrum,
        'rol': rol,
        'permisos': permisosUsuario
    }
    return render(request, 'Proyect_Agile/Proyecto/verProyecto.html', context)


## listar todos los proyectos para el admin
def listarProyectosAdmin(request):
    template_name = 'Proyect_Agile/Proyecto/listarProyectosAdmin.html'

    scrum = request.user
    proyectos = Proyecto.objects.all()
    context = {
        'estados': estados_Proyecto,
        'proyectos': proyectos,
    }

    return render(request, template_name, context)


### Miembro ###
@login_required(login_url="login")
def miembrosProyecto(request, id):
    proyecto = get_object_or_404(Proyecto, pk=id)
    rol = Rol.objects.filter(idProyecto=id, nombre="Scrum Master").first()
    listaMiembros = Miembro.objects.filter(idproyecto=proyecto).exclude(idrol=rol)
    usuario = request.user
    scrum = False
    error = True
    if request.user == proyecto.scrumMaster:
        scrum = True
    if scrum and Rol.objects.filter(idProyecto=id).count() > 1:
        error = False
    permisosMiembro = obtenerPermisos(id, request.user)
    context = {
        'error': error,
        'proyecto': proyecto,
        'estados': estados_Proyecto,
        'proyecto_id': id,
        'scrum': scrum,
        'miembros': listaMiembros,
        'usuario': usuario,
        'permisos': permisosMiembro
    }
    return render(request, 'Proyect_Agile/Miembros/proyectoMiembros.html', context)


# decorador para comprobar si el miembro tiene permisos para añadir mas miembros al proyecto
@permisoVista(permiso="agregarMiembro")
def formCrearMiembro(request, id, socialUserId):
    socialUser = get_object_or_404(SocialAccount, pk=socialUserId)
    user = User.objects.get(email__icontains=socialUser.extra_data['email'])
    proyecto = get_object_or_404(Proyecto, pk=id)
    miembro = Miembro.objects.filter(usuario=user.id, idproyecto=proyecto).first()

    if request.method == 'POST':
        # Se muestra el cuadro de crear miembro
        formMiembrosProyecto = MiembroForm(request.POST)
        cargahoraria = formMiembrosProyecto['cargahoraria'].value()
        if formMiembrosProyecto.is_valid():
            formMiembrosProyecto.save()
            miembro1 = Miembro.objects.filter(idproyecto=id).last()
            miembro1.horasDisponibles = cargahoraria
            miembro1.save()
            return redirect('miembrosproyecto', id)
        else:
            context = {
                'formMiembroProyecto': MiembroForm(request.POST or None),
                'proyecto_id': id,
                'Usuario': user,
            }
            return render(request, 'Proyect_Agile/Miembros/agregarMiembro.html', context, None, 200)
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
                'proyecto_id': id,
                'Usuario': user
            }
            return render(request, 'Proyect_Agile/Miembros/agregarMiembro.html', context, None, 200)


# decorador y funciones para editar un miembro de proyecto
@method_decorator(permisoVista(permiso="modificarMiembro"), name='dispatch')
class editarMiembro(UpdateView):
    model = Miembro
    template_name = 'Proyect_Agile/Miembros/editarMiembro.html'
    form_class = MiembroForm

    # change the value of the miembro.horasDisponibles when is edited
    def form_valid(self, form):
        miembro = Miembro.objects.get(id=self.kwargs['pk'])
        # get the previous value of miembro.cargahoraria
        cargahoraria = miembro.cargahoraria
        # get the new value of miembro.cargahoraria
        cargahoraria2 = form.cleaned_data['cargahoraria']
        print(cargahoraria2)
        print(cargahoraria)
        miembro.horasDisponibles = miembro.horasDisponibles + (cargahoraria2 - cargahoraria)
        print(miembro.horasDisponibles)
        # save the new value of miembro.cargahoraria
        miembro.save()
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        id = self.kwargs['id']
        form.fields["idrol"].queryset = Rol.objects.filter(idProyecto=id).exclude(nombre="Scrum Master")
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs['id']
        permisos = obtenerPermisos(id, self.request.user)
        context['idProyecto'] = id
        context['permisos'] = permisos
        return context

    def get_success_url(self):
        id = self.kwargs['id']
        return reverse('miembrosproyecto', kwargs={'id': id})


# decorador y funcion para eliminar un miembro de un proyecto
@permisoVista(permiso="eliminarMiembro")
def eliminarMiembro(request, id, idmiembro):
    proyecto = Proyecto.objects.get(id=id)
    miembro = Miembro.objects.filter(id=idmiembro, idproyecto=proyecto).first()
    miembro.delete()
    return redirect('miembrosproyecto', id=id)


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
            'form': formrol,
            'proyecto_id': id,
        }
        return render(request, 'Proyect_Agile/Rol/crearRol.html', context)


# ver los roles de un proyecto
def verRolProyecto(request, id):
    proyecto = Proyecto.objects.get(id=id)
    usuario = request.user
    roles = Rol.objects.filter(idProyecto=proyecto)
    scrum = False
    if request.user == proyecto.scrumMaster:
        scrum = True
    context = {
        'roles': roles,
        'proyecto': proyecto,
        'scrum': scrum,
        'usuario': usuario,
        'estados': estados_Proyecto,
        'proyecto_id': id,
        'permisos': obtenerPermisos(id, request.user)
    }
    return render(request, 'Proyect_Agile/Rol/verRolesProyecto.html', context)


# editar un rol de un proyecto
@method_decorator(permisoVista(permiso="modificarRol"), name='dispatch')
class editarRol(UpdateView):
    model = Rol
    template_name = 'Proyect_Agile/Rol/editarRol.html'
    form_class = rolForm

    def get_context_data(self, **kwargs):
        # get all the roles from the project      
        context = super().get_context_data(**kwargs)
        id = self.kwargs['idproyecto']
        permisos = obtenerPermisos(id, self.request.user)
        context['idProyecto'] = id
        context['permisos'] = permisos
        return context

    def get_success_url(self):
        id = self.kwargs['idproyecto']

        print(id)

        return reverse('rolproyecto', kwargs={'id': id})


# lista los roles de un proyecto
@permisoVista(permiso="crearRol")
def listarRolesProyecto(request, id):
    proyectos = Proyecto.objects.exclude(id=id)
    proyecto = Proyecto.objects.get(id=id)
    scrum = False
    if request.user == proyecto.scrumMaster:
        scrum = True
    context = {
        'proyectos': proyectos,
        'estados': estados_Proyecto,
        'idproyecto': id,
        'scrum': scrum,
        'usuario': request.user,
        'flag': 0,
    }
    return render(request, 'Proyect_Agile/Rol/listarProyectoRol.html', context)


# importar roles de otros proyectos al proyecto actual
def importarRol(request, id, idproyecto):
    rolImportado = importarRolProyecto(id, idproyecto)
    rolImportado.save()
    return redirect('rolproyecto', id)



#### TIPO US ####
def tipoUSProyecto(request, id):
    proyecto = get_object_or_404(Proyecto, pk=id)
    tipoUS = TipoUS.objects.filter(idproyecto=proyecto)
    permisosMiembro = obtenerPermisos(id, request.user)
    scrum = False
    if request.user == proyecto.scrumMaster:
        scrum = True
    context = {
        'scrum': scrum,
        'proyecto': proyecto,
        'estados': estados_Proyecto,
        'tiposUS': tipoUS,
        'permisos': permisosMiembro,
        'proyecto_id': id,
    }
    return render(request, 'Proyect_Agile/US/verTipoUS.html', context)


# funcion para crear un nuevo tipo de us
def crearTipoUS(request, id):
    proyecto = Proyecto.objects.get(id=id)
    if request.method == 'POST':
        form = tipoUSForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('listarTipoUS', id)
    else:
        form = tipoUSForm()
        form.fields['idproyecto'].initial = proyecto
        context = {
            'form': form,
            'idProyecto': id,
        }
        return render(request, 'Proyect_Agile/US/crearTipoUS.html', context)


### USER STORY ###
@permisoVista(permiso="agregarUserStory")
def crearUser_Story(request, id):
    proyecto = Proyecto.objects.get(id=id)

    if request.method == 'POST':
        form = UserStoryForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            context = {
                'form': UserStoryForm(request.POST or None)
            }
            return render(request, 'Proyect_Agile/US/crearUS.html', context)

        planning = User_Story.objects.filter(idproyecto=id).last()
        UP = planning.UP
        BV = planning.BV

        planning.prioridad = round(((0.6 * BV + 0.4 * UP) / 2), 2)

        planning.save()
        print("el estado del form es: ", form.cleaned_data["estado"])
        print("la prioridad del form es: ", form.cleaned_data["prioridad"])

        return redirect('listarUS', id)
    else:
        form = UserStoryForm()
        form.fields['idproyecto'].initial = proyecto
        form.fields['tipo'].queryset = TipoUS.objects.filter(idproyecto=proyecto)
        context = {
            'form': form
        }
        return render(request, 'Proyect_Agile/US/crearUS.html', context)


# Lista de los us dentro de un proyecto

def verListaUS(request, id):
    proyecto = Proyecto.objects.get(id=id)
    usuario = request.user
    us = User_Story.objects.filter(idproyecto=proyecto).order_by('-prioridad')
    for u in us:
        if u.estado == 'H':
            u.prioridad = 0
            u.save()
    us = User_Story.objects.filter(idproyecto=proyecto).order_by('-prioridad')
    scrum = False
    if request.user == proyecto.scrumMaster:
        scrum = True
    context = {
        'scrum': scrum,
        'USs': us,
        'proyecto': proyecto,
        'usuario': usuario,
        'estados': estados_Proyecto,
        'proyecto_id': str(id),
        'permisos': obtenerPermisos(id, request.user)
    }
    return render(request, 'Proyect_Agile/US/listarUS.html', context)


# Lista de tipo de us dentro de un proyecto

def listarTUSproyectos(request, id):
    proyectos = Proyecto.objects.exclude(id=id)
    context = {
        'proyectos': proyectos,
        'estados': estados_Proyecto,
        'idproyecto': id,
        'flag': 1,
    }
    return render(request, 'Proyect_Agile/Rol/listarProyectoRol.html', context)


# Funcion para importar tipos de us de otro proyecto al actual

def importarTipoUS(request, id, idproyecto):
    proyecto1 = Proyecto.objects.get(id=id)
    proyecto2 = Proyecto.objects.get(id=idproyecto)
    tipoUS = TipoUS.objects.filter(idproyecto=proyecto2)

    for tipos in tipoUS:
        if not TipoUS.objects.filter(idproyecto=proyecto1, nombre=tipos.nombre).exists():
            tipoImportado = TipoUS.objects.create(nombre=tipos.nombre, idproyecto=proyecto1, estado=tipos.estado)
            tipoImportado.save()

    return redirect('listarTipoUS', id)


# Muestra el listado de sprints del proyecto

def verSprint(request, id):
    iniciar = True
    if Sprint.objects.filter(idproyecto=id, estado="E").exists():
        # throw error
        iniciar = False
    sprint = Sprint.objects.filter(idproyecto=id)
    proyecto = Proyecto.objects.get(id=id)
    usuario = request.user
    ban = True
    scrum = False
    if request.user == proyecto.scrumMaster:
        scrum = True

    if Sprint.objects.filter(idproyecto=id, estado='E').exists() and Sprint.objects.filter(idproyecto=id,
                                                                                           estado='P').exists():
        ban = False
    context = {
        'proyecto': proyecto,
        'crear': ban,
        'iniciar': iniciar,
        'scrum': scrum,
        'sprints': sprint,
        'usuario': usuario,
        'estados': estados_Proyecto,
        'proyecto_id': id,
        'permisos': obtenerPermisos(id, request.user)
    }
    return render(request, 'Proyect_Agile/Sprint/verSprint.html', context)


# form para la creacion de sprints de un proyecto

def crearSprint(request, id):
    if request.method == 'POST':
        form = SprintForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('verSprint', id)
    else:
        nroultimosprint = Sprint.objects.filter(
            idproyecto=id)
        # Aqui obtiene el numero del ultimo sprint, para hacer "autoincrementable"
        proyecto = get_object_or_404(Proyecto, pk=id)
        ultimoSprint = Sprint.objects.filter(idproyecto=proyecto).order_by("-numero").first()
        formSprint = SprintForm()
        if nroultimosprint:
            numero = nroultimosprint.order_by('numero').last().numero
            formSprint.fields["numero"].initial = numero + 1
        else:
            formSprint.fields["numero"].initial = 1

        formSprint.fields["idproyecto"].initial = proyecto

        context = {
            'form': formSprint,
            'ultimoSprint': Sprint.objects.filter(idproyecto=id).last(),
            'proyecto_id': id
        }
    return render(request, 'Proyect_Agile/Sprint/crearSprint.html', context)


# Muestra los us que se pueden agregar al sprint backlog

def listarUS_para_Sprint(request, id, id_sprint):
    # USs = User_Story.objects.filter(idproyecto=id, estado='N').order_by('-prioridad') | User_Story.objects.filter(idproyecto=id, estado='STSA').order_by('-prioridad') | User_Story.objects.filter(idproyecto=id, estado='Cancelado').order_by('-prioridad')
    USs = User_Story.objects.filter(idproyecto=id, estado__in=['N', 'STSA', 'Cancelado']).order_by('-prioridad')
    context = {
        'USs': USs,
        'proyecto_id': id,
        'id_sprint': id_sprint,
    }
    return render(request, 'Proyect_Agile/Sprint/listarUS.html', context)


# Para agregar un us al sprint backlog

def agregarUs_para_Sprint(request, id, id_us, id_sprint, estimacion):
    proyecto = get_object_or_404(Proyecto, pk=id)
    if request.method == 'POST':

        if int(float(estimacion)) > 0:
            us = User_Story.objects.get(id=id_us)
            miembro = Miembro.objects.get(usuario=us.miembroEncargado.usuario, idproyecto=id)
            miembro.horasDisponibles += int(float(estimacion))
            miembro.save()

        form = formCrearPlanningPoker(request.POST)
        print("hasta aca llego")

        if form.is_valid():
            us = User_Story.objects.get(id=id_us)
            us.miembroEncargado = form.cleaned_data['miembroEncargado']
            estado = form.cleaned_data['estado']

            if estado == 'N' or estado == 'STSA':
                us.estado = 'Por hacer'

            us.estimacion = form.cleaned_data['estimacion']
            us.idSprint = form.cleaned_data['idSprint']

            us.save()

            return redirect('listarPlanningPoker', id, id_sprint)
        else:
            form = formCrearPlanningPoker(request.POST or None)
            # get all the members of the project except the scrum master
            miembros = Miembro.objects.filter(idproyecto=id).exclude(usuario=proyecto.scrumMaster)
            form.fields["miembroEncargado"].queryset = Miembro.objects.filter(idproyecto=id).exclude(
                usuario=proyecto.scrumMaster)
            context = {
                'form': form,

                'us': User_Story.objects.get(id=id_us),
                'idProyecto': id,
                'idSprint': id_sprint,
            }
            return render(request, 'Proyect_Agile/Sprint/agregarUSSprint.html', context, None, 200)

    else:

        form = formCrearPlanningPoker()
        form.fields["idSprint"].initial = Sprint.objects.get(id=id_sprint)

        # se excluye el rol
        form.fields["miembroEncargado"].queryset = Miembro.objects.filter(idproyecto=id)
        context = {
            'form': form,

            'us': User_Story.objects.get(id=id_us),
            'idProyecto': id,
            'idSprint': id_sprint,

        }
        return render(request, 'Proyect_Agile/Sprint/agregarUSSprint.html', context, None, 200)


# Muestra los miembros del proyecto que trabajan en ese sprint

def listaMiembroSprint(request, id, id_sprint):
    miembros = []
    sprint = Sprint.objects.get(id=id_sprint)  # recupera el sprint
    listaUS = User_Story.objects.filter(idSprint=sprint)  # recupera us del sprint

    for us in listaUS:  # itera por cada us los miembros encargados
        band = 0
        for miembro in miembros:
            if miembro == us.miembroEncargado:
                band = 1
        if band == 0:
            miembros.append(us.miembroEncargado)

    context = {
        'miembros': miembros,
        'proyecto_id': id,
        'id_sprint': id_sprint
    }
    return render(request, 'Proyect_Agile/Sprint/mostrarMiembrosSprint.html', context, None, 200)


# muestra los us del sprint backlog

def listarPlanningPoker(request, id, id_sprint):
    planningPoker = User_Story.objects.filter(idSprint=id_sprint).order_by(
        '-prioridad')  # listar us dentro del sprint backlog

    context = {

        'proyecto_id': id,
        'USs': planningPoker,
        'id_sprint': id_sprint,

    }
    return render(request, 'Proyect_Agile/Sprint/listarPlanningPoker.html', context)


# inicia el sprint del proyecto

def iniciarSprint(request, id, id_sprint):
    sprint = Sprint.objects.get(id=id_sprint)  # para iniciar el sprint seleccionado
    sprint.estado = 'E'  # cambia el estado
    for us in User_Story.objects.filter(idSprint=id_sprint):  # cambia el estado de los us dentro del sprint
        tipo = us.tipo.estado.split(', ')
        us.estado = tipo[0]
        us.save()

    sprint.save()
    return redirect('verSprint', id)


# finaliza el sprint del proyecto

def finalizarSprint(request, id, id_sprint):
    # check if us of the sprint are in state "N" or "STSA" or "PP"
    sprint = Sprint.objects.get(id=id_sprint)  # tomar el sprint seleccionado
    sprint.estado = 'F'  # estado de finalizado
    sprint.save()  # guardar el estado
    # para calcular las horas de las tareas del sprint
    us_sprint = User_Story.objects.filter(idSprint=id_sprint) # todos los us del sprint
    horas=0 # para cargar las horas de cada tarea
    for us in us_sprint: # cada us del sprint
        tareas = Tarea.objects.filter(idUs=us) # traemos todas las tareas que sean del us , en ese momento
        for tarea in tareas:
            horas = horas + tarea.duracion # sumamos la duracion de cada tarea
    sprint.Htrabajadas=horas
    sprint.save()  # guardar el estado
    planning = User_Story.objects.filter(idSprint=id_sprint, estado__in=['Por hacer', 'En Ṕroceso', 'Cancelado'])
    for us in planning:
        UP = us.UP
        BV = us.BV
        us.estado = 'STSA'
        us.prioridad = round(((0.6 * BV + 0.4 * UP) / 2) + 3, 2)
        us.save()
    return redirect('verSprint', id)


# Mostrar el kan ban dentro de la pestaña de sprint
def mostrarKanban(request, id, id_sprint, id_tipo):
    if id_tipo == '0':
        us = User_Story.objects.filter(idSprint=id_sprint).last()
        tipo = us.tipo
    else:
        tipo = TipoUS.objects.get(id=id_tipo)
    estados = tipo.estado.split(', ')
    us = User_Story.objects.filter(idSprint=id_sprint, tipo=tipo)  # kan ban del sprint seleccionado
    USs = []
    ruta = request.path.index("tipo")
    for i in User_Story.objects.filter(idSprint=id_sprint):
        if not i.tipo in USs:
            USs.append(i.tipo)

    context = {
        'ruta': request.path[ruta + 5:-1],
        'proyecto_id': id,
        'uss': us,
        'sprint': id_sprint,
        'tipo': estados,
        'tipos': USs,
        'usuario': request.user,
        'url': request.path
    }
    return render(request, 'Proyect_Agile/Sprint/kanban.html', context)


# Cambiar el estado del us dentro del tablero kan ban

def cambiarEstadoUs(request):
    # traemos el estado y el idus del ajax de kanban.html
    estado = request.GET.get('estado', None)
    idus = request.GET.get('idUs', None)
    us = User_Story.objects.get(id=idus)
    # cambiamos el estado al nuevo y guardamos
    us.estado = estado
    us.save()
    return HttpResponse(estado)


def quitarUSsprint(request, id, id_sprint, id_us):
    print(id_sprint, " ", id_us)
    us = User_Story.objects.get(id=id_us)
    miembro = Miembro.objects.get(usuario=us.miembroEncargado.usuario, idproyecto=id)
    miembro.horasDisponibles += us.estimacion
    us.miembroEncargado = None
    us.idSprint = None
    us.estado = 'N'
    miembro.save()
    us.save()

    return redirect('listarPlanningPoker', id, id_sprint)


# crear tareas para un us
def crearTarea(request, id, id_us):
    if request.method == 'POST':
        form = FormTarea(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listarTareas', id, id_us)
        else:
            form = FormTarea(request.POST or None)
            context = {
                'form': form,
                'us': User_Story.objects.get(id=id_us),

                'idproyecto': id
            }
            return render(request, 'Proyect_Agile/US/crearTarea.html', context)
    else:
        form = FormTarea()
        form.fields['idUs'].initial = id_us
        context = {
            'form': form,
            'us': User_Story.objects.get(id=id_us),

            'idproyecto': id
        }
        return render(request, 'Proyect_Agile/US/crearTarea.html', context)


# listar las tareas de un us
def listarTareas(request, id, id_us):
    tareas = Tarea.objects.filter(idUs=id_us)
    proyecto = Proyecto.objects.get(id=id)
    scrum = False
    if proyecto.scrumMaster == request.user:
        scrum = True
    context = {
        'idproyecto': id,
        'scrum': scrum,
        'us': User_Story.objects.get(id=id_us),
        'usuario': request.user,
        'tareas': tareas,
        'tipo': User_Story.objects.get(id=id_us).tipo.id
    }
    return render(request, 'Proyect_Agile/US/listarTareas.html', context)


# revision del us , el scrum master debe aprobar el us para que su estado pase a finalizado
def revisionUs(request, id):
    us = User_Story.objects.filter(idproyecto=id, estado='Hecho')
    proyecto = Proyecto.objects.get(id=id)
    scrum = False
    if request.user == proyecto.scrumMaster:
        scrum = True
    context = {
        'USs': us,
        'proyecto': proyecto,
        'proyecto_id': id,
        'scrum': scrum,
        'usuario': request.user,
    }
    return render(request, 'Proyect_Agile/US/revisionUs.html', context)


# comprueba la descicion del scrum para cancelar o aprovar el us
def decisionScrumUS(request, id, opcion, id_us):
    if opcion == '1':
        us = User_Story.objects.get(id=id_us)
        us.estado = 'Finalizado'
        print("rodolfovsf@gmail.com")
        print(us.miembroEncargado.usuario.email)
        send_mail(
            'US ' + us.nombre + " Aprovado",
            'El US .' + us.nombre + " ha sido aprovado por el Scrum Master",
            "rodolfovsf@gmail.com",
            [us.miembroEncargado.usuario.email],
            fail_silently=False,
        )
        us.save()
    else:
        us = User_Story.objects.get(id=id_us)
        UP = us.UP
        BV = us.BV
        us.prioridad = round(((0.6 * BV + 0.4 * UP) / 2) + 3, 2)
        us.estado = 'Cancelado'
        print("rodolfovsf@gmail.com")
        print(us.miembroEncargado.usuario.email)
        send_mail(
            'US ' + us.nombre + " Rechazado",
            'El US .' + us.nombre + " ha sido rechazado por el Scrum Master",
            "rodolfovsf@gmail.com",
            [us.miembroEncargado.usuario.email],
            fail_silently=False,
        )
        us.save()
    return redirect('revisionUs', id)


# cambia el encargado de un us en un sprint
def cambiarEncargado(request, id, id_sprint, id_miembro):
    if request.method == "POST":
        form = FormCambiarEncargado(request.POST)
        if form.is_valid():
            uss = User_Story.objects.filter(idSprint=id_sprint, miembroEncargado=id_miembro)
            miembro = form.cleaned_data['miembroEncargado']
            for us in uss:
                us.miembroEncargado = miembro
                us.save()
            return redirect('miembroSprint', id, id_sprint)

    else:
        form = FormCambiarEncargado()
        miembros = []
        USs = User_Story.objects.filter(idSprint=id_sprint).exclude(miembroEncargado=id_miembro)
        for us in USs:
            miembros.append(us.miembroEncargado.id)

        form.fields["miembroEncargado"].queryset = Miembro.objects.filter(id__in=miembros)
        context = {
            'form': form,
            'proyecto_id': id,
            'id_sprint': id_sprint
        }
        return render(request, 'Proyect_Agile/Sprint/cambiarEncargado.html', context)


def burndownChart(request,id):
    proyecto=Proyecto.objects.get(id=id)
    scrum=False;
    if request.user == proyecto.scrumMaster:
        scrum = True

    # dibujo del burndown

    # asignacion

    x_data = []
    y_data = []
    i = 0
    sprints = Sprint.objects.filter(idproyecto=proyecto)

    for sprint in sprints:

        i=i+1
        x_data.append(i)
        y_data.append(sprint.Htrabajadas)

    plot_div_i = plot({ 'data' : [Scatter(x=x_data, y=y_data,mode='lines', name='test',
                             opacity=0.8, marker_color='green')],
                    'layout': {'title': '', 'xaxis': {'title': 'Sprint','tickmode' : "linear", "tick0" : "1", "dtick" : "1" }, 'yaxis': {'title': 'UP'}},
    }, output_type='div' )

    context={

        'proyecto': proyecto,
        'usuario': request.user,
        'estados': estados_Proyecto,
        'scrum': scrum,
        'proyecto_id': id,
        'permisos': obtenerPermisos(id, request.user),
        'burndownChart':plot_div_i

    }
    return render(request, 'Proyect_Agile/Proyecto/burndownChart.html', context)