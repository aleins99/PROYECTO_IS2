from django.forms import ModelForm
from .models import *

class crearProyectoForm(ModelForm):
    class Meta:
        model = Proyecto
        fields = ['nombre','descripcion','miembros','scrumMaster','fechainicio','fechafin']
