"""Tests W09: allauth + RBAC (10 pruebas)."""
from io import StringIO

from django.contrib.auth.models import Group, User
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse


class AuthBasicTest(TestCase):
    def test_login_http_200(self):
        self.assertEqual(self.client.get(reverse('account_login')).status_code, 200)

    def test_login_usa_template_propio(self):
        r = self.client.get(reverse('account_login'))
        self.assertTemplateUsed(r, 'account/login.html')

    def test_login_correcto_redirige(self):
        User.objects.create_user('testlogin', password='pass12345')
        r = self.client.post(reverse('account_login'),
                             {'login': 'testlogin', 'password': 'pass12345'})
        self.assertRedirects(r, '/productos/', fetch_redirect_response=False)


class RBACTest(TestCase):
    def setUp(self):
        call_command('crear_grupos', stdout=StringIO())

    def _user(self, nombre, grupo):
        u = User.objects.create_user(nombre, password='pass12345')
        u.groups.add(Group.objects.get(name=grupo))
        return u

    def test_eliminar_producto_sin_login_redirige(self):
        r = self.client.get(reverse('productos:eliminar', args=[1]))
        self.assertIn(r.status_code, (302, 403))

    def test_vendedor_no_elimina_producto_403(self):
        self.client.force_login(self._user('vend', 'Vendedor'))
        r = self.client.post(reverse('productos:eliminar', args=[1]))
        self.assertEqual(r.status_code, 403)

    def test_vendedor_ve_lista_productos(self):
        self.client.force_login(self._user('vend2', 'Vendedor'))
        self.assertEqual(self.client.get(reverse('productos:lista')).status_code, 200)

    def test_vendedor_puede_crear_venta(self):
        self.client.force_login(self._user('vend3', 'Vendedor'))
        self.assertEqual(self.client.get(reverse('ventas:crear')).status_code, 200)

    def test_gerente_pasa_permiso_producto(self):
        # pk inexistente: 404 prueba que el permiso paso (no es 403)
        self.client.force_login(self._user('ger', 'Gerente'))
        r = self.client.post(reverse('productos:eliminar', args=[999999]))
        self.assertEqual(r.status_code, 404)

    def test_gerente_pasa_permiso_cliente(self):
        self.client.force_login(self._user('ger2', 'Gerente'))
        r = self.client.post(reverse('clientes:eliminar', args=[999999]))
        self.assertEqual(r.status_code, 404)

    def test_command_crea_3_grupos(self):
        for n in ('Gerente', 'Vendedor', 'Almac\u00e9n'):
            self.assertTrue(Group.objects.filter(name=n).exists(), n)
