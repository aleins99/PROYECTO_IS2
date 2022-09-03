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

class crearProyecto(CreateView):
    model = Proyecto
    template_name = 'dashboard/proyect.html'
    form_class = crearProyectoForm