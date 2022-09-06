from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path("",views.iniciosesion),
    path('Proyecto/' , views.listarProyectos.as_view(),name='listarproyecto'),
    path('Proyecto/crear/',views.crearProyecto.as_view(),name='crearproyecto'),
    path('Proyecto/<pk>/editar/',views.editarProyecto.as_view(),name='editarproyecto'),
    path('Proyecto/<id>/ver/',views.verproyecto,name='verproyecto'),
    path('UserStory/', views.crearUser_Story.as_view(), name='crearUS'),


]
