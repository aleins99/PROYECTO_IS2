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

estados_Proyecto = {
    'P':'Pendiente',
    'E':'En ejecucion',
    'C':'Cancelado',
    'F':'Finalizado',
}

@register.filter
def get_at_index(list, index):
    return list[index]

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

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


def iniciosesion(request):
    login = reverse('account_login')
    return HttpResponseRedirect(login)

# The class crearProyecto inherits from CreateView, and it's model is Proyecto, it's template is
# proyect.html, it's form is ProyectoForm, and it's extra context is the ProyectoForm
class crearProyecto(CreateView):
    model = Proyecto
    template_name = 'Proyect_Agile/proyecto.html'
    
    form_class = ProyectoForm
    extra_context = {'form': ProyectoForm}

    def form_valid(self, form):
        proyecto = Proyecto.objects.order_by('-id')[0]
        rol = crearRolScrumMaster(proyecto)
        asignarRolScrumMaster(proyecto, proyecto.scrumMaster, rol)
        return super().form_valid(form)





class crearUser_Story(CreateView):
    model = User_Story
    template_name = 'Proyect_Agile/us.html'
    form_class = UserStoryForm
    extra_context = {'form': UserStoryForm }

class IniciarProyecto(View):
    def post(self, request, *args, **kwargs):
        obj = get_object_or_404(Proyecto, pk=self.kwargs['pk'])
        print(obj)
        obj.estado = 'E'
        obj.save()
        return redirect(reverse_lazy('<iniciarproyecto>', kwargs={'pk': obj.pk}))

def listarProyectos(request):

    template_name = 'Proyect_Agile/listarProyectos.html'



    usuario = request.user.groups.filter(name='Administrador').exists()
    proyectos = obtenerlistaDeProyectosUser(request)
    context = {
        'estados': estados_Proyecto,
        'Administrador': usuario,
        'proyectos': proyectos
    }

    return render(request, template_name, context)


class editarProyecto(UpdateView):
    model= Proyecto
    template_name = 'Proyect_Agile/editarProyecto.html'
    form_class = ProyectoForm


@login_required(login_url="login")
def verproyecto(request,id):
    if request.method == 'POST':
        obj = Proyecto.objects.get(id=id)
        print(obj)
        obj.estado = 'E'
        obj.save()
        return redirect(reverse_lazy('verproyecto', kwargs={'id': obj.pk}))



    scrum = False
    proyecto = Proyecto.objects.get(id=id)
    proyecto_id = str(id)
    print(id)

    idproyecto = str(int(id)-1)

    rol = ''

    try:

        usuarios = Miembro.objects.filter(idproyecto=idproyecto, usuario=request.user).first()


        rol = usuarios.idrol
    except:
        pass

    print('rol:',rol)

    #rol = Rol.objects.get(id=usuario.id)

    print(request.user.id)

    if request.user == proyecto.scrumMaster:
        scrum = True

    print(scrum)

    context = {
        'proyecto':proyecto,
        'estados': estados_Proyecto,
        'proyecto_id':proyecto_id,
        'scrum': scrum,
        'rol': rol,

    }
    print(type(proyecto.estado))
    return render(request,'Proyect_Agile/verProyecto.html', context)


@login_required(login_url="login")
def miembrosProyecto(request, id):
    proyecto = get_object_or_404(Proyecto, pk=id)
    idproyecto = str(int(id) - 1)
    rol = Rol.objects.filter(idProyecto=idproyecto, nombre="Scrum Master").first()
    print('rol:',rol)
    listaMiembros = Miembro.objects.filter(idproyecto=proyecto).exclude(idrol=rol)
    permisos = obtenerPermisosProyecto(request, proyecto)
    print(listaMiembros)



    proyecto_id = str(id)

    scrum= False

    if request.user == proyecto.scrumMaster:
        scrum = True

    context = {
        'proyecto':proyecto,
        'estados': estados_Proyecto,
        'proyecto_id':proyecto_id,
        'scrum': scrum,
        'miembros': listaMiembros
    }
    return render(request, 'Proyect_Agile/proyectoMiembros.html', context)

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

            return render(request, 'Proyect_Agile/agregarMiembro.html', context, None, 200)

def ListarUsuarios(request, id):
    # lista de usuario del sistema autenticados por el sso
    listarUsuarios = SocialAccount.objects.order_by('id')
    context = {
        'usuarios': listarUsuarios,
        'idProyecto': id,
    }
    return render(request, 'Proyect_Agile/listarUsuarios.html', context)





