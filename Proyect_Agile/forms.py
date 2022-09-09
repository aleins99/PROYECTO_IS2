from cProfile import label
from datetime import date, datetime
from mimetypes import init
from django import forms
from .models import *

# The ProyectoForm class inherits from forms.ModelForm, and it defines a Meta class that tells Django
# which model should be used to create this form (model = Proyecto) and which fields should be used
# (fields = ['nombre','descripcion','scrumMaster','fechainicio', 'fechafin', 'usbacklog', 'estado'])
class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ['nombre','descripcion','scrumMaster','fechainicio', 'fechafin']
        labels = {'descripcion':'Descripción','scrumMaster':'Scrum Master','fechainicio':'Fecha Inicio', 'fechafin':'Fecha Fin'}
        widgets = {
            'descripcion': forms.Textarea(attrs={'cols': 1, 'rows': 2}),
            'fechainicio': forms.DateInput(attrs={'type': 'date'}),
            'fechafin': forms.DateInput(attrs={'type': 'date'}),
        }


    def __init__(self, *args, **kwargs):
        """
        The function takes in a list of fields and a list of widgets, and returns a list of fields with
        the widgets replaced
        """
        super(ProyectoForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'form-control'})



class UserStoryForm(forms.ModelForm):
    class Meta:
        model = User_Story
        fields = '__all__'



    def __init__(self, *args, **kwargs):
        """
        The function takes in a list of fields and a list of widgets, and returns a list of fields with
        the widgets replaced
        """
        super(UserStoryForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'form-control'})


class MiembroForm(forms.ModelForm):
    class Meta:
        model = Miembro
        fields = '__all__'
        widgets = {
            'usuario': forms.HiddenInput(),
            'idproyecto': forms.HiddenInput(),

        }


