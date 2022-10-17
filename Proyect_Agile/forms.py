from cProfile import label
from datetime import date, datetime
from mimetypes import init
from django import forms
from .models import *
from django.contrib.auth.models import AbstractUser
from allauth.utils import get_user_model
#Formularios para la creacion instancias de los diferentes modelos
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

# formulario para el modelo de us primitivo
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

# formulario para agregar un miembro del proyecto
class MiembroForm(forms.ModelForm):
    class Meta:
        model = Miembro
        fields = '__all__'
        labels = {'cargahoraria':'Carga Horaria', 'idrol': 'Rol', 'isActivo': 'Activo', 'usuario':'', 'idproyecto':''}

        widgets = {
            'usuario': forms.HiddenInput(),
            'idproyecto': forms.HiddenInput(),
            'isActivo': forms.CheckboxInput(attrs={'class':''}),
        }


    def __init__(self, *args, **kwargs):
        """
        The function takes in a list of fields and a list of widgets, and returns a list of fields with
        the widgets replaced
        """
        super(MiembroForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if name == 'isActivo':
                field.widget.attrs.update({'class':'form-check-input'})
            else:
                field.widget.attrs.update({'class':'form-control'})


   
    
# formulario para agregar roles dentro de un proyecto
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

# formulario para agregar un nuevo tipo de us al proyecto
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


# formulario para agregar un nuevo sprint al proyecto
class SprintForm(forms.ModelForm):
    class Meta:
        model = Sprint
        fields = ['nombre', 'numero', 'fechainicio', 'fechafin', 'estado', 'idproyecto']
        labels = {'fechainicio':'Fecha Inicio', 'fechafin':'Fecha Fin'}
        widgets = {
            'descripcion': forms.Textarea(attrs={'cols': 1, 'rows': 2}),
            'numero': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Numero de sprint', 'type': 'number',
                       'readonly': 'readonly'}),
            'fechainicio': forms.DateInput(attrs={'type': 'date'}),
            'fechafin': forms.DateInput(attrs={'type': 'date'}),
            'idproyecto': forms.HiddenInput(),
            'estado': forms.HiddenInput(),

        }


    def __init__(self, *args, **kwargs):
        """
        The function takes in a list of fields and a list of widgets, and returns a list of fields with
        the widgets replaced
        """
        super(SprintForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'form-control'})

# formulario para el planning poker ( para los us que se agregan al sprint backlog )

class formCrearPlanningPoker(forms.ModelForm):

    # metodo para validar el dominio de los inputs de los campos


    class Meta:
        model = PlanningPoker
        fields = '__all__'
        labels = {
            'miembroEncargado': 'Encargado',
        }

        widgets = {
            'idUs': forms.HiddenInput(),  # oculta el label del idUserStory
            'idSprint': forms.HiddenInput(),  # oculta el label del idSprint
            'prioridad': forms.HiddenInput(), # oculta el label del priorida
            'estado' : forms.HiddenInput(), # oculta el label del estado
        }

    def __init__(self, *args, **kwargs):
        """
        The function takes in a list of fields and a list of widgets, and returns a list of fields with
        the widgets replaced
        """
        super(formCrearPlanningPoker, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
