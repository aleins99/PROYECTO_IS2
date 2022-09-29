from cProfile import label
from datetime import date, datetime
from mimetypes import init
from django import forms
from .models import *
from django.contrib.auth.models import AbstractUser
from allauth.utils import get_user_model
class UsuarioForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username','first_name','last_name',]
        labels = {'username':'Nombre de Usuario', 'first_name':'Nombres', 'last_name':'Apellidos'}

    def __init__(self, *args, **kwargs):
        """
        The function takes in a list of fields and a list of widgets, and returns a list of fields with
        the widgets replaced
        """
        super(UsuarioForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'form-control'})

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
        labels = {'idproyecto': '', 'historial': '', 'estado':''}
        widgets = {
            'idproyecto': forms.HiddenInput(),
            'historial': forms.HiddenInput(),
            'estado': forms.HiddenInput(),
        }


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
        labels = {'cargahoraria':'Carga Horaria', 'idrol': 'Rol', 'isActivo': 'Activo'}
        widgets = {
            'usuario': forms.HiddenInput(),
            'idproyecto': forms.HiddenInput(),
        }
    
       
    def __init__(self, *args, **kwargs):
        """
        The function takes in a list of fields and a list of widgets, and returns a list of fields with
        the widgets replaced
        """
        super(MiembroForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'form-control'})


class rolForm(forms.ModelForm):
    class Meta:
        model= Rol
        fields = '__all__'
        labels = {'idProyecto':'','nombre': 'Nombre', 'descripcion': 'Descripción'}
        widgets = {
            'idProyecto': forms.HiddenInput(attrs={'style':'display:none'}),
            'nombre': forms.TextInput(attrs={'class':'form-control'}),     
            'descripcion': forms.TextInput(attrs={'class':'form-control'}),  
        }

class tipoUSForm(forms.ModelForm):
    class Meta:
        model = TipoUS
        fields = '__all__'
        widgets = {
            'idproyecto': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        """
        The function takes in a list of fields and a list of widgets, and returns a list of fields with
        the widgets replaced
        """
        super(tipoUSForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'form-control'})


class SprintForm(forms.ModelForm):
    class Meta:
        model = Sprint
        fields = ['nombre', 'descripcion', 'fechainicio', 'fechafin', 'estado']
        labels = {'fechainicio':'Fecha Inicio', 'fechafin':'Fecha Fin'}
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
        super(SprintForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'form-control'})
