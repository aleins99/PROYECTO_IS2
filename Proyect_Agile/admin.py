from django.contrib import admin
from .models import Proyecto, Miembro, Rol
# Register your models here.
admin.site.register(Proyecto)
admin.site.register(Miembro)
admin.site.register(Rol)
