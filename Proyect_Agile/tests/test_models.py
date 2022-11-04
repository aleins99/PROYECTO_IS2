from django.test import TestCase
from Proyect_Agile.models import *
from django.contrib.auth.models import Permission, User, GroupManager
import datetime


class modeloProyectoTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Crear Usuario de prueba
        Usuario = User.objects.create(username='Usuario Prueba', first_name='Usuario', last_name='Prueba',
                                      email='prueba@gmail.com')
        # Crear Proyecto de Prueba
        Proyecto.objects.create(nombre='ProyectoPrueba', fechainicio="2022-10-17", scrumMaster=Usuario, fechafin="2022-11-24")
        # Crear Rol de Prueba
        Rol.objects.create(nombre='Rol de prueba', descripcion='Descripcion Rol',
                             idProyecto=Proyecto.objects.get(id=1))
        # Crear Sprint de prueba
        Sprint.objects.create(idproyecto=Proyecto.objects.get(id=1), numero=1, fechafin="2022-10-24")
        # Crear Miembro de prueba
        Miembro.objects.create(usuario=User.objects.get(id=1), idrol=Rol.objects.get(id=1),
                                idproyecto=Proyecto.objects.get(id=1), isActivo=True, cargahoraria=40)

        # Crear Tipo de Us
        TipoUS.objects.create(nombre='Tipo de Us de prueba', idproyecto=Proyecto.objects.get(id=1))
        # Crear User_Story
        User_Story.objects.create(idproyecto=Proyecto.objects.get(id=1), UP=5,BV=7, idSprint=Sprint.objects.get(id=1), miembroEncargado= Miembro.objects.get(id=1), nombre='Us de Prueba',
                                 tipo=TipoUS.objects.get(id=1), descripcion='Descripcion de Us de prueba', comentarios="Descripcion de comentario")


    # Prueba de __str__() definidos en Proyecto.models

    def test_User_str(self):
        u = User.objects.get(id=1)
        self.assertEquals(str(u), 'Usuario Prueba')


    def test_Proyecto_str(self):
        p = Proyecto.objects.get(id=1)
        u = User.objects.get(id=1)
        self.assertEquals(str(p), p.nombre)


    def test_Rol_str(self):
        r = Rol.objects.get(id=1)
        p = Proyecto.objects.get(id=1)
        self.assertEquals(str(r), r.nombre)
       

    def test_Sprint_str(self):
        s = Sprint.objects.get(id=1)
        self.assertEquals(str(s), str(s.nombre))
     

    # Prueba de verificacion de valores por default
    def test_default_value(self):
        # Para Proyecto
        p = Proyecto.objects.get(id=1)
        self.assertEquals(p.estado, 'P')
        # Para Rol
        r = Rol.objects.get(id=1)
        self.assertFalse(r.agregarUserStory)
        self.assertFalse(r.modificarUserStory)
        self.assertFalse(r.eliminarUserStory)
        # Para Sprint
        s = Sprint.objects.get(id=1)
        self.assertEquals(s.estado, 'P')
        # Para miembro
        m = Miembro.objects.get(id=1)
        self.assertTrue(m.isActivo)
        self.assertEquals(m.cargahoraria, 40)
     
        # Para User_Story
        us = User_Story.objects.get(id=1)
        self.assertEquals(us.estado, 'N')
        # self.assertEquals(us.fechaIngreso, date.today)
        # Para planning Poker
        us = User_Story.objects.get(id=1)
        self.assertEquals(us.estado, 'N')
        # self.assertEquals(actividad.hora, datetime.time())

    # Prueba de verificacion de que trae bien los datos de Proyecto
    def test_get_Proyecto(self):
        p = Proyecto.objects.get(id=1)
        self.assertEquals(p.nombre, 'ProyectoPrueba')
        self.assertEquals(p.fechainicio, datetime.date(2022, 10, 17))

    # Prueba de verificacion de que trae bien los datos de Rol
    def test_get_Rol(self):
        p = Proyecto.objects.get(id=1)
        r = Rol.objects.get(id=1)
        self.assertEquals(r.nombre, 'Rol de prueba')
        self.assertEquals(r.descripcion, 'Descripcion Rol')
        self.assertEquals(r.idProyecto, p)

    # Prueba de verificacion de que trae bien los datos de Sprint
    def test_get_Sprint(self):
        p = Proyecto.objects.get(id=1)
        s = Sprint.objects.get(id=1)
        self.assertEquals(s.numero, 1)
        self.assertEquals(s.idproyecto, p)

    # Prueba de verificacion de que trae bien los datos de miembro
    def test_get_Mienbros(self):
        p = Proyecto.objects.get(id=1)
        r = Rol.objects.get(id=1)
        m = Miembro.objects.get(id=1)
        self.assertEquals(m.idproyecto, p)
        self.assertEquals(m.idrol, r)

    # Prueba de verificacion de que trae bien los datos de User_Story
    def test_get_US(self):
        p = Proyecto.objects.get(id=1)
        m = Miembro.objects.get(id=1)
        us = User_Story.objects.get(id=1)
        self.assertEquals(us.nombre, 'Us de Prueba')
        self.assertEquals(us.idproyecto, p)

    # Prueba de verificacion de que trae bien los datos de planning Poker
    def test_get_PP(self):
        us = User_Story.objects.get(id=1)
        m = Miembro.objects.get(id=1)
        s = Sprint.objects.get(id=1)
        pp = User_Story.objects.get(id=1)
        self.assertEqual(pp.UP, 5)
        self.assertEqual(pp.BV, 7)
        self.assertEquals(pp.idSprint, s)
        self.assertEquals(pp.miembroEncargado, m)


