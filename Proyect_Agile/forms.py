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
    def clean(self):
        us = super(UserStoryForm, self).clean()
        up = us.get("UP")
        bv = us.get("BV")

        if up <= 0 or bv <= 0:
            raise forms.ValidationError('ERROR!!!!. BV o UP inválidos, cargue un valor mayor a cero')
    class Meta:
        model = User_Story
        fields = ['idproyecto', 'estado', 'prioridad', 'nombre','UP', 'BV',  'descripcion', 'historial', 'tipo']
        labels = {'idproyecto': '', 'historial': 'Comentarios', 'estado':'', 'prioridad':''}
        widgets = {
            'idproyecto': forms.HiddenInput(),
            'estado': forms.HiddenInput(),
            'prioridad': forms.HiddenInput(),  # oculta el label del priorida
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
    def clean(self):
        miembro = super(MiembroForm, self).clean()
        cargaHoraria = miembro.get("cargahoraria")

        if cargaHoraria <= 0:
            raise forms.ValidationError('ERROR!!!!. Estimación inválida, cargue un valor mayor a cero')
    class Meta:
        model = Miembro
        fields = '__all__'
        labels = {'cargahoraria':'Carga Horaria', 'idrol': 'Rol', 'isActivo': 'Activo', 'usuario':'', 'idproyecto':'', 'horasDisponibles':''}

        widgets = {
            'usuario': forms.HiddenInput(),
            'idproyecto': forms.HiddenInput(),
            'isActivo': forms.CheckboxInput(attrs={'class':''}),
            'horasDisponibles': forms.HiddenInput(),

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
        fields = ['nombre', 'numero', 'fechainicio', 'fechafin', 'estado', 'idproyecto', 'duracion']
        labels = {'fechainicio':'Fecha Inicio', 'fechafin':'Fecha Fin', 'duracion':''}
        widgets = {
            'descripcion': forms.Textarea(attrs={'cols': 1, 'rows': 2}),
            'numero': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Numero de sprint', 'type': 'number',
                       'readonly': 'readonly'}),
            'fechainicio': forms.DateInput(attrs={'type': 'date'}),
            'fechafin': forms.DateInput(attrs={'type': 'date'}),
            'idproyecto': forms.HiddenInput(),
            'estado': forms.HiddenInput(),
            'duracion': forms.HiddenInput()
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

    def clean(self):
        us = super(formCrearPlanningPoker, self).clean()
        estimacion = us.get('estimacion')
        encargado = us.get('miembroEncargado')
        idsprint = us.get('idSprint').id
        sprint = Sprint.objects.get(id=idsprint)
        duracion = sprint.duracion

        try:
            miembro = Miembro.objects.get(usuario=encargado.usuario, idproyecto=encargado.idproyecto)
            cargahoraria = miembro.cargahoraria
            horasDisponibles = miembro.horasDisponibles
        except:
            raise forms.ValidationError("El scrum master no puede ser el encargado de un US")
        if estimacion > duracion:
            raise forms.ValidationError('ERROR!!! Su valor supera a la capacidad del sprint. Puede asignar hasta un máximo de: ' + str(duracion) + ' horas disponibles')
        if estimacion <= 0 and horasDisponibles > 0:

            raise forms.ValidationError('ERROR!!!!. Estimación inválida, cargue un valor mayor a cero. Puede asignar hasta un máximo de: ' + str(horasDisponibles) + ' horas disponibles.')

        elif horasDisponibles >= estimacion:
            miembro.horasDisponibles = horasDisponibles - estimacion
            sprint.duracion = duracion - estimacion
            sprint.save()
            miembro.save()
        elif horasDisponibles == 0:
            raise forms.ValidationError('ERROR!!!! NO QUEDAN HORAS DISPONIBLES PARA ESTE MIEMBRO')
        else :
            raise forms.ValidationError('ERROR!!!! LAS HORAS ASIGNADAS SON MAYORES A LAS HORAS DISPONIBLES.\n Puede asignar hasta un máximo de: '+ str(horasDisponibles) + ' horas disponibles.' )


    class Meta:
        model = User_Story
        fields = ['miembroEncargado', 'estado', 'estimacion', 'idSprint']
        labels = {
            'miembroEncargado': 'Encargado',
        }

        widgets = {
            'idSprint': forms.HiddenInput(),  # oculta el label del idSprint
            'estado': forms.HiddenInput(), #oculta el label del estado

        }

    def __init__(self, *args, **kwargs):
        """
        The function takes in a list of fields and a list of widgets, and returns a list of fields with
        the widgets replaced
        """
        super(formCrearPlanningPoker, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

# formulario para la creacion de tareas
class FormTarea(forms.ModelForm):

    def clean(self):
        tarea= super(FormTarea, self).clean()
        estimacion = tarea.get('idUs').estimacion
        duracion = tarea.get('duracion')
        if duracion <= 0 and estimacion > 0:

            raise forms.ValidationError('ERROR!!!!. Estimación inválida, cargue un valor mayor a cero. Puede asignar hasta un máximo de: ' + str(estimacion) + ' duracion.')

        elif duracion <= estimacion:
            us = tarea.get('idUs')
            us.estimacion = estimacion - duracion
            us.save()
        elif estimacion == 0:
            raise forms.ValidationError('ERROR!!!! NO QUEDAN HORAS DISPONIBLES PARA ESTE US')
        else:
            raise forms.ValidationError('ERROR!!!! LAS HORAS ASIGNADAS SON MAYORES A LAS HORAS DISPONIBLES.\n Puede asignar hasta un máximo de: '+ str(estimacion) + ' horas disponibles.' )

    class Meta:
        model = Tarea
        fields = '__all__'
        labels = {'idUs':''}
        widgets = {
            'idUs': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        """
        The function takes in a list of fields and a list of widgets, and returns a list of fields with
        the widgets replaced
        """
        super(FormTarea, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

# form para cambiar el encargado de un us dentro de un sprint
class FormCambiarEncargado(forms.ModelForm):
    class Meta:
        model = User_Story
        fields = ['miembroEncargado']
        labels = {'miembroEncargado':'Encargado'}
    

    def __init__(self, *args, **kwargs):
        """
        The function takes in a list of fields and a list of widgets, and returns a list of fields with
        the widgets replaced
        """
        super(FormCambiarEncargado, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

class FormDecisionScrum(forms.ModelForm):
    class Meta:
        model = User_Story
        fields = ['comentarios']
        labels = {'comentarios': 'Comentario'}

    def __init__(self, *args, **kwargs):
        """
        The function takes in a list of fields and a list of widgets, and returns a list of fields with
        the widgets replaced
        """
        super(FormDecisionScrum, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})