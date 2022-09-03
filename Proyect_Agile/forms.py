from django.forms import ModelForm
from .models import *

class ProyectoForm(ModelForm):
    class Meta:
        model = Proyecto
        fields = ['nombre','descripcion','miembros','scrumMaster','fechainicio','fechafin']

    def __init__(self, *args, **kwargs):
        super(ProyectoForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'form-control'})
            print(field)
