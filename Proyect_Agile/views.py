from gc import get_objects
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

estados_Proyecto = {
    'P':'Pendiente',
    'E':'En ejecucion',
    'C':'Cancelado',
    'F':'Finalizado',
}
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

def iniciosesion(request):
    login = reverse('account_login')
    return HttpResponseRedirect(login)

# The class crearProyecto inherits from CreateView, and it's model is Proyecto, it's template is
# proyect.html, it's form is ProyectoForm, and it's extra context is the ProyectoForm
class crearProyecto(CreateView):
    model = Proyecto
    template_name = 'Proyect_Agile/proyecto.html'
    form_class = ProyectoForm
    extra_context = {'form': ProyectoForm }

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

class listarProyectos(ListView):
    model= Proyecto
    template_name = 'Proyect_Agile/listarProyectos.html'
    extra_context = {'estados': estados_Proyecto}
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

    
    proyecto = Proyecto.objects.get(id=id)
    proyecto_id = str(id)
    print(id)
    context = {
        'proyecto':proyecto,
        'estados': estados_Proyecto,
        'proyecto_id':proyecto_id
    }
    print(type(proyecto.estado))
    return render(request,'Proyect_Agile/verProyecto.html', context)


@login_required(login_url="login")
def miembrosProyecto(request, id):
    proyecto = Proyecto.objects.get(id=id)
    miembros = proyecto.miembros
    proyecto_id = str(id)
    context = {
        'proyecto':proyecto,
        'estados': estados_Proyecto,
        'proyecto_id':proyecto_id
    }
    return render(request, 'Proyect_Agile/proyectoMiembros.html', context)

