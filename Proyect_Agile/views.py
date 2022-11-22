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
from allauth.account.models import EmailAddress
from django.contrib.auth.models import AbstractUser
from allauth.utils import get_user_model

# estados por defecto de los proyectos
estados_Proyecto = {
    'P':'Pendiente',
    'PP':'En Planning Poker',
    'E':'En ejecucion',
    'EP': 'En Proceso',
    'STSA': 'Sin Terminar en Sprint Anterior',
    'A': 'Aprobado',
    'C':'Cancelado',
    'F':'Finalizado',
}

# para decoradores
@register.filter
def tareasUS(US):
    return tarea.objects.filter(idUs=US)

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

# editar un proyecto del sistema
class editarProyecto(UpdateView):
    model= Proyecto
    template_name = 'Proyect_Agile/Proyecto/editarProyecto.html'
    form_class = ProyectoForm
    success_url = '/'

# ver detalles de un proyecto del sistema
def verproyecto(request,id):
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
        'proyecto':proyecto,
        'estados': estados_Proyecto,
        'proyecto_id':id,
        'scrum': scrum,
        'rol': rol,
        'permisos': permisosUsuario
    }
    return render(request,'Proyect_Agile/Proyecto/verProyecto.html', context)

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
    scrum= False

    if request.user == proyecto.scrumMaster:
        scrum = True

    permisosMiembro = obtenerPermisos(id, request.user)
    context = {
        'proyecto':proyecto,
        'estados': estados_Proyecto,
        'proyecto_id':id,
        'scrum': scrum,
        'miembros': listaMiembros,
        'usuario' : usuario,
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

# decorador y funciones para editar un miembro de proyecto
@method_decorator(permisoVista(permiso="modificarMiembro"), name='dispatch')
class editarMiembro(UpdateView):
    model= Miembro
    template_name = 'Proyect_Agile/Miembros/editarMiembro.html'
    form_class = MiembroForm
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
        return reverse('miembrosproyecto',kwargs={'id':id})

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
            'form': formrol
        }
        return render(request, 'Proyect_Agile/Rol/crearRol.html', context)

# ver los roles de un proyecto
def verRolProyecto(request, id):
    proyecto = Proyecto.objects.get(id=id)
    usuario = request.user
    roles = Rol.objects.filter(idProyecto=proyecto)

    context = {
        'roles': roles,
        'proyecto': proyecto,
        'usuario': usuario,
        'estados': estados_Proyecto,
        'proyecto_id': id,
        'permisos': obtenerPermisos(id, request.user)
    }
    return render(request, 'Proyect_Agile/Rol/verRolesProyecto.html', context)

# editar un rol de un proyecto
@method_decorator(permisoVista(permiso="modificarRol"), name='dispatch')
class editarRol(UpdateView):
    model= Rol
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

        return reverse('rolproyecto',kwargs={'id':id})

# lista los roles de un proyecto
@permisoVista(permiso="crearRol")
def listarRolesProyecto(request, id):
    proyectos = Proyecto.objects.exclude(id=id)
    context = {
        'proyectos': proyectos,
        'estados': estados_Proyecto,
        'idproyecto': id,
        'flag': 0,
    }
    return render(request,'Proyect_Agile/Rol/listarProyectoRol.html',context)

# importar roles de otros proyectos al proyecto actual
def importarRol(request,id, idproyecto):
    rolImportado = importarRolProyecto(id, idproyecto)
    rolImportado.save()
    return redirect('rolproyecto', id)


### DOCUMENTACION ###
def verDocumentacion(request):

    context={}

    return render(request,'Proyect_Agile/Docs/Documentacion_index.html',context)


#### TIPO US ####
def tipoUSProyecto(request, id):
    proyecto = get_object_or_404(Proyecto, pk=id)
    tipoUS = TipoUS.objects.filter(idproyecto=proyecto)
    permisosMiembro = obtenerPermisos(id, request.user)
    context = {
        'proyecto':proyecto,
        'estados': estados_Proyecto,
        'tiposUS':tipoUS,
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
            'form': form
        }
        return render(request, 'Proyect_Agile/US/crearTipoUS.html', context)

### USER STORY ###
@permisoVista(permiso="agregarUserStory")
def crearUser_Story(request,id):
    proyecto = Proyecto.objects.get(id=id)


    if request.method == 'POST':
        form =UserStoryForm(request.POST)
        if form.is_valid():
            form.save()

        planning = User_Story.objects.filter(idproyecto=id).last()
        UP = planning.UP
        BV = planning.BV

        planning.prioridad = ((0.6 * BV + 0.4 * UP) / 2)

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

    context = {
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
    tipoUS= TipoUS.objects.filter(idproyecto=proyecto2)

    for tipos in tipoUS:
        if not TipoUS.objects.filter(idproyecto=proyecto1, nombre=tipos.nombre).exists():
            tipoImportado = TipoUS.objects.create(nombre=tipos.nombre,idproyecto=proyecto1, estado=tipos.estado)
            tipoImportado.save()


    return redirect('listarTipoUS' , id)

# Muestra el listado de sprints del proyecto

def verSprint(request, id):
    sprint = Sprint.objects.filter(idproyecto= id)
    proyecto = Proyecto.objects.get(id=id)
    usuario = request.user
    ban = True
    if Sprint.objects.filter(idproyecto= id,estado='P').exists() or Sprint.objects.filter(idproyecto= id,estado='E').exists() :
        ban= False

    context = {
        'proyecto': proyecto,
        'crear' : ban,
        'sprints' : sprint,
        'usuario': usuario,
        'estados': estados_Proyecto,
        'proyecto_id': id,
        'permisos': obtenerPermisos(id, request.user)
    }
    return render(request,'Proyect_Agile/Sprint/verSprint.html',context)

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
            'ultimoSprint' : Sprint.objects.filter(idproyecto=id).last()
        }
    return render(request, 'Proyect_Agile/Sprint/crearSprint.html', context)

# Muestra los us que se pueden agregar al sprint backlog

def listarUS_para_Sprint(request,id,id_sprint):
    USs = User_Story.objects.filter(idproyecto=id, estado='N').order_by('-prioridad') | User_Story.objects.filter(idproyecto=id, estado='STSA').order_by('-prioridad')

    context = {
        'USs': USs,
        'proyecto_id' : id,
        'id_sprint' : id_sprint,
    }
    return render(request, 'Proyect_Agile/Sprint/listarUS.html', context)

# Para agregar un us al sprint backlog

def agregarUs_para_Sprint(request,id,id_us,id_sprint):
    proyecto = get_object_or_404(Proyecto, pk=id)
    if request.method == 'POST':

        form = formCrearPlanningPoker(request.POST)
        print("hasta aca llego")

        if form.is_valid():
            us = User_Story.objects.get(id=id_us)
            us.miembroEncargado = form.cleaned_data['miembroEncargado']
            estado = form.cleaned_data['estado']

            if estado == 'N' or estado == 'STSA':
                us.estado = 'PP'

            us.estimacion = form.cleaned_data['estimacion']
            us.idSprint = form.cleaned_data['idSprint']



            us.save()

            return redirect('listarPlanningPoker', id, id_sprint)
        else:
            form = formCrearPlanningPoker(request.POST or None)
            context = {
                'form': form,

                'us': User_Story.objects.get(id=id_us),
                'idProyecto': id,
            }
            return render(request, 'Proyect_Agile/Sprint/agregarUSSprint.html', context, None, 200)

    else:
        form = formCrearPlanningPoker()
        form.fields["idSprint"].initial = Sprint.objects.get(id=id_sprint)


        # se excluye el rol
        form.fields["miembroEncargado"].queryset = Miembro.objects.filter(idproyecto=proyecto)
        context = {
            'form': form,

            'us' : User_Story.objects.get(id=id_us),
            'idProyecto': id,
        }
        return render(request, 'Proyect_Agile/Sprint/agregarUSSprint.html', context, None, 200)

# Muestra los miembros del proyecto que trabajan en ese sprint

def listaMiembroSprint(request, id, id_sprint): 

    miembros =[]
    sprint = Sprint.objects.get(id=id_sprint) # recupera el sprint
    listaUS = User_Story.objects.filter(idSprint=sprint) # recupera us del sprint


    for us in listaUS: # itera por cada us los miembros encargados
        band=0
        for miembro in miembros:
            if miembro == us.miembroEncargado:
                band=1
        if band == 0:
            miembros.append(us.miembroEncargado)

    context = {
        'miembros' : miembros,
    }
    return render(request, 'Proyect_Agile/Sprint/mostrarMiembrosSprint.html', context, None, 200)

# muestra los us del sprint backlog

def listarPlanningPoker(request, id, id_sprint):
    planningPoker = User_Story.objects.filter(idSprint=id_sprint).order_by('-prioridad') # listar us dentro del sprint backlog

    context = {

        'proyecto_id' : id,
        'USs' : planningPoker,
        'id_sprint' : id_sprint,

    }
    return render(request,'Proyect_Agile/Sprint/listarPlanningPoker.html', context)

# inicia el sprint del proyecto

def iniciarSprint(request,id, id_sprint):
    sprint = Sprint.objects.get(id=id_sprint) # para iniciar el sprint seleccionado
    sprint.estado = 'E' # cambia el estado
    for us in User_Story.objects.filter(idSprint=id_sprint): # cambia el estado de los us dentro del sprint
        us.estado = 'P'
        us.save()

    sprint.save()
    return redirect('verSprint', id)

# finaliza el sprint del proyecto

def finalizarSprint(request,id, id_sprint):
    sprint = Sprint.objects.get(id=id_sprint) # tomar el sprint seleccionado
    sprint.estado = 'F' # estado de finalizado
    sprint.save() # guardar el estado
    planning = User_Story.objects.filter(idSprint=id_sprint, estado='EP' ) | User_Story.objects.filter(idSprint=id_sprint, estado='P' )
    for us in planning:
        UP = us.UP
        BV = us.BV
        us.estado = 'STSA'
        us.prioridad = ((0.6 * BV + 0.4 * UP) / 2) + 3
        us.save()
    return redirect('verSprint', id)


# Mostrar el kan ban dentro de la pestaña de sprint
def mostrarKanban(request, id, id_sprint):
    us = User_Story.objects.filter(idSprint=id_sprint) # kan ban del sprint seleccionado
    context = {
        'proyecto_id': id,
        'uss': us,
        'sprint' : id_sprint
    }
    return render(request, 'Proyect_Agile/Sprint/kanban.html', context)

# Cambiar el estado del us dentro del tablero kan ban 

def cambiarEstadoUS(request, id, id_sprint, estado, id_us):
    estados = {
        'P' : 'EP',
        'EP' : 'H',
        'H' : 'C'
    }
    us= User_Story.objects.get(id=id_us) # id del us para cambiar el estado
    us.estado = estados.get(estado) # asignar nuevo estado
    us.save() # guardar cambios
    return redirect('mostrarKanban', id, id_sprint)

def quitarUSsprint(request, id, id_sprint, id_us):

    us = User_Story.objects.get(id= id_us)
    miembro = Miembro.objects.get(usuario= us.miembroEncargado.usuario, idproyecto= id)
    miembro.horasDisponibles += us.estimacion
    us.miembroEncargado = None
    us.idSprint = None
    us.estado = 'N'
    miembro.save()
    us.save()

    return redirect('listarPlanningPoker', id, id_sprint)
