import io
import os
from decimal import Decimal
from PIL import Image
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.test import APITestCase
from productos.models import Categoria, Producto
from productos.validators import validar_imagen_producto


def _imagen(nombre='img.jpg', formato='JPEG', ct='image/jpeg'):
    buf = io.BytesIO()
    Image.new('RGB', (100, 100), color='teal').save(buf, format=formato)
    buf.seek(0)
    return SimpleUploadedFile(nombre, buf.read(), content_type=ct)


def _invalido():
    return SimpleUploadedFile('notimage.exe', b'\x00\x01fake binary\xff\xfe',
                              content_type='application/octet-stream')


def _limpiar():
    for p in Producto.objects.all():
        if p.imagen:
            try:
                os.remove(p.imagen.path)
            except FileNotFoundError:
                pass


class ValidadorImagenTest(TestCase):
    def test_jpeg_valida_pasa(self):
        validar_imagen_producto(_imagen())

    def test_png_valida_pasa(self):
        validar_imagen_producto(_imagen('img.png', 'PNG', 'image/png'))

    def test_no_imagen_lanza_error(self):
        with self.assertRaises(ValidationError) as ctx:
            validar_imagen_producto(_invalido())
        self.assertIn('no permitido', str(ctx.exception).lower())

    def test_muy_grande_lanza_error(self):
        a = _imagen()
        a.size = 6 * 1024 * 1024
        with self.assertRaises(ValidationError) as ctx:
            validar_imagen_producto(a)
        self.assertIn('5 mb', str(ctx.exception).lower())


class ProductoImagenModelTest(TestCase):
    def setUp(self):
        self.cat = Categoria.objects.create(nombre='Cat Media')

    def tearDown(self):
        _limpiar()

    def test_sin_imagen_es_valido(self):
        p = Producto.objects.create(nombre='Sin', precio=Decimal('100.00'),
                                    stock=5, categoria=self.cat)
        self.assertFalse(bool(p.imagen))

    def test_guarda_con_imagen(self):
        p = Producto(nombre='Con', precio=Decimal('200.00'), stock=3,
                     categoria=self.cat, imagen=_imagen())
        p.save()
        self.assertIn('productos/', p.imagen.name)


class ProductoAPIImagenTest(APITestCase):
    def setUp(self):
        self.cat = Categoria.objects.create(nombre='Cat API')

    def tearDown(self):
        _limpiar()

    def test_api_imagen_url_none_sin_imagen(self):
        p = Producto.objects.create(nombre='Sin', precio=Decimal('100.00'),
                                    stock=5, categoria=self.cat)
        r = self.client.get(f'/api/productos/{p.pk}/')
        self.assertEqual(r.status_code, 200)
        self.assertIsNone(r.json().get('imagen_url'))

    def test_api_imagen_url_con_imagen(self):
        p = Producto(nombre='Con', precio=Decimal('300.00'), stock=2,
                     categoria=self.cat, imagen=_imagen())
        p.save()
        r = self.client.get(f'/api/productos/{p.pk}/')
        self.assertEqual(r.status_code, 200)
        self.assertIn('productos/', r.json().get('imagen_url'))