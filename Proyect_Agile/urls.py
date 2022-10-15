from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path("",views.iniciosesion),
    path('home/' , views.listarProyectos,name='listarproyecto'),
    path('home/', views.listarProyectos, name='home'),
    path('listarUsuarios/<int:id>/', views.ListarUsuarios, name='listarUsuarios'),
    path('EditarPerfil/<pk>/', views.editarPerfil.as_view(), name='editarPerfil' ),
    path('Administracion/Proyectos', views.listarProyectosAdmin, name='listaAdministracion'),
    path('Proyecto/crear/',views.crearProyecto,name='crearproyecto'),
    path('Proyecto/<pk>/editar/',views.editarProyecto.as_view(),name='editarproyecto'),
    path('Proyecto/<id>/ver/',views.verproyecto,name='verproyecto'),
    path('Proyecto/<id>/miembros/', views.miembrosProyecto, name="miembrosproyecto"),
    path('Proyecto/agregarMiembro/<int:id>/<int:socialUserId>', views.formCrearMiembro, name="agregarMiembros"),
    path('Proyecto/<id>/miembros/<idmiembro>/eliminarMiembro', views.eliminarMiembro, name="eliminarMiembro"),
    path('Proyecto/<id>/miembro/<pk>/editar/', views.editarMiembro.as_view(), name='editarmiembro'),
    path('Proyecto/<id>/roles/crear/', views.crearRol, name='agregarrol'),
    path('Proyecto/<id>/roles/', views.verRolProyecto, name='rolproyecto'),
    path('Proyecto/<idproyecto>/roles/<pk>/editarRoles/', views.editarRol.as_view(), name='editarRol'),
    path('Proyecto/<id>/roles/importarRoles/<idproyecto>/', views.importarRol, name='importarRol'),
    path('Proyecto/<id>/roles/importarRoles/', views.listarRolesProyecto, name='listarRolesProyecto'),
    path('Proyecto/<id>/tipoUS/', views.tipoUSProyecto, name='listarTipoUS'),
    path('Proyecto/<id>/tipoUS/crear/',views.crearTipoUS, name='crearTipoUS'),
    path('Proyecto/<id>/US/crear/', views.crearUser_Story, name='crearUS'),
    path('Proyecto/<id>/listaUS/', views.verListaUS, name='listarUS'),
    path('Proyecto/<idproyecto>/listaUS/<pk>/editarUS/', views.verListaUS, name='editarUS'),
    path('Proyecto/<id>/tipoUS/importarTipoUS/<idproyecto>/', views.importarTipoUS, name='importarTipoUS'),
    path('Proyecto/<id>/tipoUS/importarTUS/', views.listarTUSproyectos, name='listarUSProyectos'),
    path('home/documentacion/', views.verDocumentacion, name='documentacion'),
    path('Proyecto/<id>/verSprint/', views.verSprint, name='verSprint')
]
