from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path("",views.iniciosesion),
    # vista del login
    path('home/' , views.listarProyectos,name='listarproyecto'),
    # vista en donde se listan los proyectos
    path('home/', views.listarProyectos, name='home'),
    # index
    path('listarUsuarios/<int:id>/', views.ListarUsuarios, name='listarUsuarios'),
    # vista en donde se listan los usuarios
    path('EditarPerfil/<pk>/', views.editarPerfil.as_view(), name='editarPerfil' ),
    # vista para editar el perfil de un usuario
    path('Administracion/Proyectos', views.listarProyectosAdmin, name='listaAdministracion'),
    # vista para el adminsitrador en donde se pueden ver todos los proyectos creados y otras utilidades
    path('Proyecto/crear/',views.crearProyecto,name='crearproyecto'),
    # vista para la creacion de un proyecto
    path('Proyecto/<pk>/editar/',views.editarProyecto.as_view(),name='editarproyecto'),
    # vista para editar un proyecto en especifico
    path('Proyecto/<id>/ver/',views.verproyecto,name='verproyecto'),
    # vista para ver un proyecto en especifico
    path('Proyecto/<id>/miembros/', views.miembrosProyecto, name="miembrosproyecto"),
    # vista para ver los miembros de un proyecto en especifico
    path('Proyecto/agregarMiembro/<int:id>/<int:socialUserId>', views.formCrearMiembro, name="agregarMiembros"),
    # form para agregar miembros desde la lista de usuarios a un proyecto en especifico
    path('Proyecto/<id>/miembros/<idmiembro>/eliminarMiembro', views.eliminarMiembro, name="eliminarMiembro"),
    # vista para quitar a miembros del proyecto
    path('Proyecto/<id>/miembro/<pk>/editar/', views.editarMiembro.as_view(), name='editarmiembro'),
    # form para editar el perfil de un miembro dentro de un proyecto
    path('Proyecto/<id>/roles/crear/', views.crearRol, name='agregarrol'),
    # form para agregar un rol a un proyecto en especifico
    path('Proyecto/<id>/roles/', views.verRolProyecto, name='rolproyecto'),
    # vista en donde se listan los roles de un proyecto en especifico
    path('Proyecto/<idproyecto>/roles/<pk>/editarRoles/', views.editarRol.as_view(), name='editarRol'),
    # form en donde se permite editar el rol de un miembro de un proyecto en especifico
    path('Proyecto/<id>/roles/importarRoles/<id_rol>/', views.importarRol, name='importarRol'),
    path('Roles/Proyecto/<id>/', views.listarRolesProyectos, name='listarRoles'),
    path('Proyecto/<id>/Roles/<id_rol>/permisos/', views.permisosRol, name='permisosRol'),
    # vista en donde se permite importar roles de otros proyectos
    path('Proyecto/<id>/roles/importarRoles/', views.listarRolesProyecto, name='listarRolesProyecto'),
    # vista en donde se listan todos los roles presentes en un proyecto en especifico
    path('Proyecto/<id>/tipoUS/', views.tipoUSProyecto, name='listarTipoUS'),
    #vista en donde se listan todos los tipos de us dentro de un proyecto en especifico
    path('Proyecto/<id>/tipoUS/crear/',views.crearTipoUS, name='crearTipoUS'),
    # form para la creacion de un tipo de us para un proyecto en especifico
    path('Proyecto/<id>/US/crear/', views.crearUser_Story, name='crearUS'),
    # form para la creacion de un us para un proyecto en especifico
    path('Proyecto/<id>/listaUS/', views.verListaUS, name='listarUS'),
    # vista en donde se listan todos los us presentes dentro de un proyecto en especifico
    path('Proyecto/<idproyecto>/US/<pk>/editarUS/', views.editarUS.as_view(), name='editarUS'),
    # form para editar un us de un proyecto
    path('Proyecto/<id>/TipoUS/', views.listarTipoUsProyectos, name='listarTipoUSProyectos'),
    path('Proyecto/<id>/tipoUS/importarTipoUS/<id_tipo>/', views.importarTipoUS, name='importarTipoUS'),
    # vista para importar tipos de us de otros proyectos
    path('Proyecto/<id>/tipoUS/importarTUS/', views.listarTUSproyectos, name='listarUSProyectos'),
    # vista para listar los us de un proyecto
    # vista en donde se muestran la documentacion
    path('Proyecto/<id>/verSprint/', views.verSprint, name='verSprint'),
    # vista en donde se puede ver un sprint en especifico
    path('Proyecto/<id>/crearSprint/', views.crearSprint, name='crearSprint'),
    # form en donde se permite la creacion de un sprint en un proyecto
    path('Proyecto/<id>/Sprint/<id_sprint>/listarUS_para_Sprint/',views.listarUS_para_Sprint, name='listarUS_para_Sprint' ),
    # vista para listar los us dentro del sprint backlog
    path('Proyecto/<id>/Sprint/<id_sprint>/agregarUs_para_Sprint/<id_us>/<estimacion>/', views.agregarUs_para_Sprint, name='agregarUs_para_Sprint'),
    # vista para agregar us al sprint backlog
    path('Proyecto/<id>/Sprint/<id_sprint>/listaMiembroSprint/', views.listaMiembroSprint, name='miembroSprint'),
    # vista para listar los miembros presentes dentro del sprint
    path('Proyecto/<id>/Sprint/<id_sprint>/listarPlanningPoker/', views.listarPlanningPoker, name='listarPlanningPoker'),
    #vista para ver los us del sprint backlog
    path('Proyecto/<id>/Sprint/<id_sprint>/iniciarSprint/', views.iniciarSprint, name='iniciarSprint'),
    # vista para iniciar un nuevo sprint
    path('Proyecto/<id>/Sprint/<id_sprint>/finalizarSprint/', views.finalizarSprint, name='finalizarSprint'),
    # vista para finalizar el sprint
    path('Proyecto/<id>/Sprint/<id_sprint>/kanban/tipo/<id_tipo>/', views.mostrarKanban, name='mostrarKanban'),
    # vista para el tablero kan ban dentro de la pestaña de sprint 
    path('Proyecto/Sprint/kanban/cambiarEstadoUs', views.cambiarEstadoUs, name="cambiarEstadoUs"),
    # vista para el cambio de estado dentro del tablero kan ban
    path('Proyecto/<id>/Sprint/<id_sprint>/us/<id_us>/quitar/',views.quitarUSsprint, name='quitarUSsprint'),
    # vista para quitar un us del kan ban
    path('Proyecto/<id>/us/<id_us>/tareas/',views.listarTareas, name='listarTareas'),
    # vista para listar las tareas de un us dentro de un sprint
    path('Proyecto/<id>/us/<id_us>/tareas/crearTarea/',views.crearTarea, name='crearTarea'),
    # vista para crear una tarea para un us
    path('Proyecto/<id>/revisionUs/',views.revisionUs,name='revisionUs'),
    # vista para la revision de un us como scrum master , el scrum master debe aprobar el us o cancelarlo
    path('Proyecto/<id>/Sprint/<id_sprint>/cambiarEncargardo/<id_miembro>/', views.cambiarEncargado, name="cambiarEncargado") ,
    # vista para cambiar el encargado de un us en un sprint , todos los us a los que pertenecia se reasignan al nuevo encargado
    path('Proyecto/<id>/decision/<opcion>/us/<id_us>/', views.decisionScrumUS, name= 'decisionUS'),
    # vista para la aprobacion del us o su cancelacion
    path('Proyecto/<id>/US/<id_us>/historial/', views.historialUs, name='historialUs'),
    # vista para el historial de US
    path('Proyecto/<id>/finalizar', views.finalizarProyecto, name='finalizarProyecto'),
    # vista para finalizar un proyecto
    path('Proyecto/<idproyecto>/TipoUs/<pk>/editar/', views.editarTipoUS.as_view(), name='editarTipoUS'),
    # vista para editar los tipos de US
    path('Proyecto/<id>/burndownChart/', views.burndownChart, name='burndownChart')
    #vista para ver el burndown chart del proyecto

]
