from decimal import Decimal
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase
from clientes.models import Cliente
from productos.models import Categoria, Producto
from ventas.models import DetalleVenta, Venta

class ProductoAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('apiuser', password='pass')
        self.token = Token.objects.create(user=self.user)
        self.cat = Categoria.objects.create(nombre='Cat API')
        self.producto = Producto.objects.create(
            nombre='Teclado API', precio=Decimal('450.00'), stock=10, categoria=self.cat)

    def test_get_lista_sin_auth_devuelve_200(self):
        self.assertEqual(self.client.get('/api/productos/').status_code, 200)

    def test_get_lista_devuelve_json_con_productos(self):
        data = self.client.get('/api/productos/').json()
        self.assertIn('results', data)
        self.assertIn('Teclado API', [p['nombre'] for p in data['results']])

    def test_post_sin_auth_devuelve_403(self):
        r = self.client.post('/api/productos/', {'nombre': 'Sin Auth', 'precio': '100.00',
                             'stock': 1, 'categoria': self.cat.pk}, format='json')
        self.assertEqual(r.status_code, 403)

    def test_post_con_token_crea_producto_201(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        r = self.client.post('/api/productos/', {'nombre': 'Monitor API', 'precio': '5500.00',
                             'stock': 3, 'categoria': self.cat.pk}, format='json')
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json()['nombre'], 'Monitor API')
        self.assertTrue(Producto.objects.filter(nombre='Monitor API').exists())

    def test_get_detalle_producto_devuelve_nombre(self):
        r = self.client.get(f'/api/productos/{self.producto.pk}/')
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertEqual(data['nombre'], 'Teclado API')
        self.assertIn('categoria_nombre', data)

    def test_get_detalle_404_id_inexistente(self):
        self.assertEqual(self.client.get('/api/productos/9999/').status_code, 404)

    def test_venta_api_incluye_total_y_detalles(self):
        cli = Cliente.objects.create(nombre='CLI', correo='c@t.com')
        venta = Venta.objects.create(cliente=cli)
        DetalleVenta.objects.create(venta=venta, producto=self.producto,
                                    cantidad=2, precio_unitario=Decimal('450.00'))
        r = self.client.get(f'/api/ventas/{venta.pk}/')
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertIn('total', data)
        self.assertIn('detalles', data)
        self.assertEqual(len(data['detalles']), 1)
        self.assertEqual(data['detalles'][0]['cantidad'], 2)
