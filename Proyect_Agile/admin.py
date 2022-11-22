from django.contrib import admin
from .models import *
# Register your models here.
class usadmin(admin.ModelAdmin):
    readonly_fields = ("id", )
admin.site.register(Proyecto)
admin.site.register(Miembro)
admin.site.register(Rol)
admin.site.register(User_Story, usadmin)
admin.site.register(TipoUS)
admin.site.register(Sprint)

