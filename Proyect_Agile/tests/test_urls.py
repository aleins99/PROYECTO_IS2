from django.test import TestCase
from django.urls import reverse, resolve
from Proyect_Agile.views import *

class TestUrls(TestCase):
	#listar proyectos
	def test_listar_proyectos_url_is_resolved(self):
		url = reverse('listarproyecto')
		self.assertEquals(resolve(url).func, listarProyectos)

	#test de editar usuario
	def test_editar_usuario_url_is_resolved(self):
		url = reverse('editarPerfil', args=[1])
		self.assertEquals(resolve(url).func.__name__, editarPerfil.as_view().__name__)
	
	#listar proyectos del admin
	def test_listar_proyectos_admin_url_is_resolved(self):
		url = reverse('listaAdministracion')
		self.assertEquals(resolve(url).func, listarProyectosAdmin)
	
	#test de crear proyecto
	def test_crear_proyecto_url_is_resolved(self):
		url = reverse('crearproyecto')
		self.assertEquals(resolve(url).func, crearProyecto)
	
	#test de editar proyecto
	def test_editar_proyecto_url_is_resolved(self):
		url = reverse('editarproyecto', args=[1])
		self.assertEquals(resolve(url).func.__name__, editarProyecto.as_view().__name__)

	#test de ver proyecto
	def test_ver_proyecto_url_is_resolved(self):
		url = reverse('verproyecto', args=[1])
		self.assertEquals(resolve(url).func, verproyecto)

	#test de ver miembros del proyecto
	def test_ver_miembros_url_is_resolved(self):
		url = reverse('miembrosproyecto', args=[1])
		self.assertEquals(resolve(url).func, miembrosProyecto)

	#test de agregar miembro
	def test_agregar_miembro_url_is_resolved(self):
		url = reverse('agregarMiembros', args=[1,1])
		self.assertEquals(resolve(url).func, formCrearMiembro)


	#test de eliminar miembro
	def test_eliminar_miembro_url_is_resolved(self):
		url = reverse('eliminarMiembro', args=[1,1])
		self.assertEquals(resolve(url).func, eliminarMiembro)
	
	#test de editar miembro
	def test_editar_miembro_url_is_resolved(self):
		url = reverse('editarmiembro', args=[1,1])
		self.assertEquals(resolve(url).func.__name__, editarMiembro.as_view().__name__)

	#test de agregar rol
	def test_agregar_rol_url_is_resolved(self):
		url = reverse('agregarrol', args=[1])
		self.assertEquals(resolve(url).func, crearRol)
	
	#test de ver roles del proyecto
	def test_ver_roles_url_is_resolved(self):
		url = reverse('rolproyecto', args=[1])
		self.assertEquals(resolve(url).func, verRolProyecto)
	
	#test de editar rol
	def test_editar_rol_url_is_resolved(self):
		url = reverse('editarRol', args=[1,1])
		self.assertEquals(resolve(url).func.__name__, editarRol.as_view().__name__)
	
	#test de importar rol
	def test_importar_rol_url_is_resolved(self):
		url = reverse('importarRol', args=[1,1])
		self.assertEquals(resolve(url).func, importarRol)
	# test de permisos del rol
	def test_permisos_rol_url_is_resolved(self):
		url = reverse('permisosRol', args=[1,1])
		self.assertEquals(resolve(url).func, permisosRol)
	
	#test de listar roles para importar
	def test_listar_roles_importar_url_is_resolved(self):
		url = reverse('listarRolesProyecto', args=[1])
		self.assertEquals(resolve(url).func, listarRolesProyecto)

	#test de listarTipoUs
	def test_listar_tipo_us_url_is_resolved(self):
		url = reverse('listarTipoUS', args=[1])
		self.assertEquals(resolve(url).func, tipoUSProyecto)

	#test de crear tipo us
	def test_crear_tipo_us_url_is_resolved(self):
		url = reverse('crearTipoUS', args=[1])
		self.assertEquals(resolve(url).func, crearTipoUS)
	
	# test de crear US
	def test_crear_us_url_is_resolved(self):
		url = reverse('crearUS', args=[1])
		self.assertEquals(resolve(url).func, crearUser_Story)
	
	#test de listar US
	def test_listar_us_url_is_resolved(self):
		url = reverse('listarUS', args=[1])
		self.assertEquals(resolve(url).func, verListaUS)
	
	#test de editar US
	def test_editar_us_url_is_resolved(self):
		url = reverse('editarUS', args=[1,1])
		self.assertEquals(resolve(url).func.__name__, editarUS.as_view().__name__)
	
	# test de listar tipo de us para importar
	def test_listar_tipo_us_importar_url_is_resolved(self):
		url = reverse('listarTipoUSProyectos', args=[1])
		self.assertEquals(resolve(url).func, listarTipoUsProyectos)
	#test de importar tipo us
	def test_importar_tipo_us_url_is_resolved(self):
		url = reverse('importarTipoUS', args=[1,1])
		self.assertEquals(resolve(url).func, importarTipoUS)
	
	#test de listar tipo de us
	def test_listar_us_importar_url_is_resolved(self):
		url = reverse('listarUSProyectos', args=[1])
		self.assertEquals(resolve(url).func, listarTUSproyectos)

	#test de verSprint
	def test_ver_sprint_url_is_resolved(self):
		url = reverse('verSprint', args=[1])
		self.assertEquals(resolve(url).func, verSprint)

	def test_crear_sprint_url_is_resolved(self):
		url = reverse('crearSprint', args=[1])
		self.assertEquals(resolve(url).func, crearSprint)

	def test_listarUS_para_sprint_url_is_resolved(self):
		url = reverse('listarUS_para_Sprint', args=[1,1])
		self.assertEquals(resolve(url).func, listarUS_para_Sprint)

	def test_agregarUS_para_sprint_url_is_resolved(self):
		url = reverse('agregarUs_para_Sprint', args=[1,1,1,1])
		self.assertEquals(resolve(url).func, agregarUs_para_Sprint)

	def test_listar_miembro_sprint_url_is_resolved(self):
		url = reverse('miembroSprint', args=[1,1])
		self.assertEquals(resolve(url).func, listaMiembroSprint)

	def test_listar_planning_poker_url_is_resolved(self):
		url = reverse('listarPlanningPoker', args=[1,1])
		self.assertEquals(resolve(url).func, listarPlanningPoker)

	def test_iniciar_sprint_url_is_resolved(self):
		url = reverse('iniciarSprint', args=[1,1])
		self.assertEquals(resolve(url).func, iniciarSprint)

	def test_finalizar_sprint_url_is_resolved(self):
		url = reverse('finalizarSprint', args=[1,1])
		self.assertEquals(resolve(url).func, finalizarSprint)

	def test_mostrar_kanban_url_is_resolved(self):
		url = reverse('mostrarKanban', args=[1,1,1])
		self.assertEquals(resolve(url).func, mostrarKanban)

	def test_cambiar_estadoUS_url_is_resolved(self):
		url = reverse('cambiarEstadoUs')
		self.assertEquals(resolve(url).func, cambiarEstadoUs)
	def test_quitarUS_sprint_url_is_resolved(self):
		url = reverse('quitarUSsprint', args=[1,1,1])
		self.assertEquals(resolve(url).func, quitarUSsprint)
	def test_revsion_us_url_is_resolved(self):
		url = reverse('revisionUs', args=[1])
		self.assertEquals(resolve(url).func, revisionUs)
	# test de listar tarea
	def test_listar_tarea_url_is_resolved(self):
		url = reverse('listarTareas', args=[1,1])
		self.assertEquals(resolve(url).func, listarTareas)
	# test de crear tarea
	def test_crear_tarea_url_is_resolved(self):
		url = reverse('crearTarea', args=[1,1])
		self.assertEquals(resolve(url).func, crearTarea)
	# test de cambiar encargado del us
	def test_cambiar_encargado_us_url_is_resolved(self):
		url = reverse('cambiarEncargado', args=[1,1,1])
		self.assertEquals(resolve(url).func, cambiarEncargado)
	def test_decision_scrum_url_is_resolved(self):
		url = reverse('decisionUS', args=[1,1,1])
		self.assertEquals(resolve(url).func, decisionScrumUS)
	def test_historial_us_url_is_resolved(self):
		url = reverse('historialUs', args=[1,1])
		self.assertEquals(resolve(url).func, historialUs)
	def test_finalizar_proyecto_url_is_resolved(self):
		url = reverse('finalizarProyecto', args=[1])
		self.assertEquals(resolve(url).func, finalizarProyecto)
	def editarTipoUS_url_is_resolved(self):
		url = reverse('editarTipoUS', args=[1,1])
		self.assertEquals(resolve(url).func.__name__, editarTipoUS.as_view().__name__)
	def test_burn_down_chart_url_is_resolved(self):
		url = reverse('burndownChart', args=[1])
		self.assertEquals(resolve(url).func, burndownChart)