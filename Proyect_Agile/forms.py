from cProfile import label
from datetime import date, datetime
from mimetypes import init
from django import forms
from .models import *

class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ['nombre','descripcion','scrumMaster','fechainicio', 'fechafin', 'usbacklog', 'estado']
        labels = {'fechainicio':'Fecha Inicio', 'fechafin':'Fecha Fin'}
        widgets = {
            'descripcion': forms.Textarea(attrs={'cols': 1, 'rows': 2}),
            'fechainicio': forms.DateInput(attrs={'type': 'date'}),
            'fechafin': forms.DateInput(attrs={'type': 'date'}),
        }
    def __init__(self, *args, **kwargs):
        super(ProyectoForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'form-control'})
            print(field)
    