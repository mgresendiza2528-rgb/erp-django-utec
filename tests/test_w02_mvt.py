from django.test import TestCase
from django.urls import reverse
from django.conf import settings


class TemplatesRenderTest(TestCase):
    def test_bienvenida_usa_template_correcto(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bienvenida.html')

    def test_bienvenida_extiende_base(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'base.html')

    def test_productos_usa_template_correcto(self):
        response = self.client.get(reverse('productos:inicio'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'productos/index.html')

    def test_clientes_usa_template_correcto(self):
        response = self.client.get(reverse('clientes:inicio'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'clientes/index.html')

    def test_proveedores_usa_template_correcto(self):
        response = self.client.get(reverse('proveedores:inicio'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'proveedores/index.html')

    def test_ventas_usa_template_correcto(self):
        response = self.client.get(reverse('ventas:inicio'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ventas/index.html')

    def test_reportes_usa_template_correcto(self):
        response = self.client.get(reverse('reportes:inicio'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reportes/index.html')


class ContextoBienvenidaTest(TestCase):
    def test_contexto_contiene_modulos(self):
        response = self.client.get('/')
        self.assertIn('modulos', response.context)

    def test_contexto_tiene_seis_modulos(self):
        response = self.client.get('/')
        self.assertEqual(len(response.context.get('modulos', [])), 6)


class StaticFilesConfigTest(TestCase):
    def test_static_url_es_slash_static(self):
        self.assertEqual(settings.STATIC_URL, '/static/')

    def test_static_root_configurado(self):
        self.assertTrue(bool(settings.STATIC_ROOT))

    def test_whitenoise_en_middleware(self):
        self.assertIn('whitenoise.middleware.WhiteNoiseMiddleware',
                      settings.MIDDLEWARE)

    def test_whitenoise_despues_de_security(self):
        m = settings.MIDDLEWARE