from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path("",views.iniciosesion),
    path('home/' , views.listarProyectos,name='listarproyecto'),
    path('home/', views.listarProyectos, name='home'),
    path('Administracion/Proyectos', views.listarProyectosAdmin, name='listaAdministracion'),
    path('Proyecto/crear/',views.crearProyecto,name='crearproyecto'),
    path('Proyecto/<pk>/editar/',views.editarProyecto.as_view(),name='editarproyecto'),
    path('Proyecto/<id>/ver/',views.verproyecto,name='verproyecto'),
    path('Proyecto/<id>/miembros/', views.miembrosProyecto, name="miembrosproyecto"),
    path('UserStory/', views.crearUser_Story.as_view(), name='crearUS'),
    path('Proyecto/agregarMiembro/<int:id>/<int:socialUserId>', views.formCrearMiembro, name="agregarMiembros"),
    path('listarUsuarios/<int:id>/', views.ListarUsuarios, name='listarUsuarios'),
    path('Proyecto/<idproyecto>/miembro/<pk>/editar/', views.editarMiembro.as_view(), name='editarmiembro'),
    path('Proyecto/<id>/roles/crear/', views.crearRol, name='agregarrol'),
    path('Proyecto/<id>/roles/', views.crearRol, name='rolproyecto'),
]
