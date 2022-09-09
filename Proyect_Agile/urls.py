from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path("",views.iniciosesion),
    path('Proyecto/' , views.listarProyectos.as_view(),name='listarproyecto'),
    path('Proyecto/crear/',views.crearProyecto.as_view(),name='crearproyecto'),
    path('Proyecto/<pk>/editar/',views.editarProyecto.as_view(),name='editarproyecto'),
    path('Proyecto/<id>/ver/',views.verproyecto,name='verproyecto'),
    path('Proyecto/<id>/miembros/', views.miembrosProyecto, name="miembrosproyecto"),
    path('UserStory/', views.crearUser_Story.as_view(), name='crearUS'),
    path('Proyecto/agregarMiembro/<int:id>/<int:socialUserId>', views.formCrearMiembro, name="agregarMiembros"),
    path('listarUsuarios/<int:id>/', views.ListarUsuarios, name='listarUsuarios'),


]
