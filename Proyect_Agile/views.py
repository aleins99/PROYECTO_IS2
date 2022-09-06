from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from .models import *
from .forms import *
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

class listarProyectos(ListView):
    model= Proyecto
    template_name = 'Proyect_Agile/listarProyectos.html'

class editarProyecto(UpdateView):
    model= Proyecto
    template_name = 'Proyect_Agile/editarProyecto.html'
    form_class = ProyectoForm


def verproyecto(request,id):
    proyecto = Proyecto.objects.get(id=id)
    context = {
        'proyecto':proyecto,

    }
    return render(request,'Proyect_Agile/verProyecto.html', context)