from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Proyecto)
admin.site.register(Miembro)
admin.site.register(Rol)
admin.site.register(User_Story)
admin.site.register(TipoUS)
admin.site.register(Sprint)

