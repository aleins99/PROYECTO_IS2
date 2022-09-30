from django.test import TestCase
from .models import *
from .views import *
from allauth.account.models import EmailAddress
from django.contrib.auth.models import Permission, User, GroupManager
from allauth.utils import get_user_model, get_username_max_length

# Create your tests here.
# create a test for the model EmailAddress

# create a test for the model Proyecto
class ProyectoTest(TestCase):
	def test_proyecto(self):
		usuario = get_user_model().objects.create(username="test", email="user@example.com")
		proyecto = Proyecto.objects.create(nombre='Proyecto1', descripcion='Descripcion1', scrumMaster=usuario, fechainicio='2020-01-01', fechafin='2020-01-01')
		self.assertEqual(proyecto.nombre, 'Proyecto2')
		self.assertEqual(proyecto.descripcion, 'Descripcion1')
		self.assertEqual(proyecto.scrumMaster, usuario)
		self.assertEqual(proyecto.fechainicio, '2020-01-01')
		self.assertEqual(proyecto.fechafin, '2020-01-01')


# create a test for the model Miembro
class MiembroTest(TestCase):
	def test_miembro(self):
		usuario = get_user_model().objects.create(username="test", email="user@example.com")
		proyecto = Proyecto.objects.create(nombre='Proyecto1', descripcion='Descripcion1', scrumMaster=usuario, fechainicio='2020-01-01', fechafin='2020-01-01')
		rol = Rol.objects.create(nombre='Rol1', descripcion='Descripcion1', idProyecto=proyecto)
		miembro = Miembro.objects.create(usuario=usuario, idproyecto=proyecto, cargahoraria='1', idrol=rol, isActivo='True')
		self.assertEqual(miembro.usuario, usuario)
		self.assertEqual(miembro.idproyecto, proyecto)
		self.assertEqual(miembro.cargahoraria, '1')
		self.assertEqual(miembro.idrol, rol)
		self.assertEqual(miembro.isActivo, 'True')


# create a test for the model Rol
class RolTest(TestCase):
	def test_rol(self):
		usuario = get_user_model().objects.create(username="test", email="user@example.com")
		proyecto = Proyecto.objects.create(nombre='Proyecto1', descripcion='Descripcion1', scrumMaster=usuario, fechainicio='2020-01-01', fechafin='2020-01-01')
		rol = Rol.objects.create(nombre='Rol1', descripcion='Descripcion1', idProyecto=proyecto)
		self.assertEqual(rol.nombre, 'Rol1')
		self.assertEqual(rol.descripcion, 'Descripcion1')
		self.assertEqual(rol.idProyecto, proyecto)

