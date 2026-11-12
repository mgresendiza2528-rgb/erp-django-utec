# Sprint 3 Planning - ERP Django
## Semanas W10-W12 - Espiral 4: API REST y Media

**Sprint Goal:**
Al finalizar el Sprint 3, el ERP expondra una API REST completa con autenticacion por token, gestion de imagenes de productos y generacion de PDFs de facturas.

## HUs seleccionadas

| ID | Historia | Puntos | Semana |
|---|---|---|---|
| HU-E4-01 | Como dev externo, quiero listar productos via API sin auth | 2 | W10 |
| HU-E4-02 | Como dev, quiero crear productos via API con token | 3 | W10 |
| HU-E4-03 | Como dev, quiero API para clientes, proveedores y ventas | 3 | W10 |
| HU-E4-04 | Como admin, quiero subir imagen de producto | 3 | W11 |
| HU-E4-05 | Como dev, quiero que la imagen aparezca en la API | 2 | W11 |
| HU-E4-06 | Como cliente, quiero descargar la factura en PDF | 5 | W12 |
| HU-E4-07 | Como admin, quiero exportar inventario a Excel | 3 | W12 |

**Total Sprint 3:** 21 puntos

## DoD - Sprint 3
- GET /api/productos/ -> JSON 200 sin autenticacion
- POST /api/productos/ sin token -> 403
- POST /api/productos/ con token valido -> 201
- Imagen de producto visible en /media/
- GET /ventas/ID/pdf/ -> descarga PDF con lineas de detalle
- GET /productos/exportar-excel/ -> archivo .xlsx descargable
- python manage.py test tests -> 107 tests OK o mas

## Sprint Backlog - actualizacion W10

| Tarea | Estado |
|---|---|
| rest_framework.authtoken instalado | W10 |
| Serializers x 5 entidades | W10 |
| ListCreateAPIView + RetrieveUpdateDestroyAPIView x 5 | W10 |
| api_urls.py x 4 apps + /api/ en core/urls.py | W10 |
| Token endpoint /api/auth/token/ | W10 |
| 7 tests APIClient escritos (pendiente ejecutar) | W10 |
| ImageField + Pillow + MEDIA_ROOT | W11 |
| Generacion PDF WeasyPrint | W12 |
| Exportacion Excel openpyxl | W12 |
