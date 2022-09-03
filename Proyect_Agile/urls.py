from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path("",views.iniciosesion),
    path('Proyecto/',views.crearProyecto.as_view,name='crearproyecto')
]
