from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from .models import Usuario, Operacion

# Create your tests here.

class TestModel(TestCase):

    def setUp(self):
        self.usuario = Usuario.objects.create(
            nombre='Arnaldo',
            saldo=200,
            NumerosContacto=['123', '456']
        )
        self.mensaje = Mensaje.objects.create(
            usuario=self.usuario,
            texto='Hola',
            fecha='2021-05-05 12:00:00'
        )

    def test_usuario(self):
        self.assertEqual(self.usuario.nombre, 'Arnaldo')
        self.assertEqual(self.usuario.saldo, 200)
        self.assertEqual(self.usuario.NumerosContacto, ['123', '456'])

    def test_mensaje(self):
        self.assertEqual(self.mensaje.usuario, self.usuario)
        self.assertEqual(self.mensaje.texto, 'Hola')
        self.assertEqual(self.mensaje.fecha, '2021-05-05 12:00:00')

    
