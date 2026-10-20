# Sprint 0 Planning - ERP Django
## Semanas W01-W03 - Espiral 1: Infraestructura

**Sprint Goal:**
Al finalizar el Sprint 0, existira un proyecto Django 4.2 con estructura de 5 apps del ERP, desplegado en Render.com con URL publica funcional y repositorio en GitHub con al menos 10 commits.

## HUs seleccionadas para este sprint

| ID | Historia | Puntos | Estado |
|---|---|---|---|
| HU-E1-01 | Entorno portable USB | 3 | En progreso |
| HU-E1-02 | Scripts de sincronizacion | 2 | En progreso |
| HU-E1-03 | Repositorio en GitHub | 2 | Pendiente |
| HU-E1-04 | Despliegue en Render.com | 3 | Pendiente |

**Total de puntos del sprint:** 10

## Sprint Backlog - Tareas tecnicas W01

| Tarea | Responsable | Estado | Horas est. |
|---|---|---|---|
| Configurar Python 3.11 embeddable | Dev | Hecho | 0.5 h |
| Instalar pip y virtualenv | Dev | Hecho | 0.3 h |
| Configurar Git Portable | Dev | Hecho | 0.3 h |
| Crear scripts .bat de sesion | Dev | Hecho | 0.5 h |
| Crear proyecto Django core | Dev | Hecho | 0.5 h |
| Crear 5 apps y urls minimas | Dev | Hecho | 1.0 h |
| Configurar settings.py base | Dev | Hecho | 0.5 h |
| Crear vista de bienvenida | Dev | Hecho | 0.3 h |
| product_backlog.md + sprint0_planning.md | Dev | Hecho | 0.5 h |
| Primer commit en GitHub | Dev | Pendiente | 0.3 h |

## Criterios de aceptacion del Sprint 0
- python manage.py check -> 0 issues
- http://127.0.0.1:8000/ -> HTTP 200 (W01)
- URL publica en Render -> HTTP 200 (W03)
- Repositorio con rama main + historial de commits
- Ficha Schmelkes E1 completa (W03)

## Sprint Backlog - W02 (actualizacion de estados)

| Tarea | Estado |
|---|---|
| Crear templates/base.html con Fable 5 AzulERP | Hecho |
| Crear 5 plantillas index.html por app | Hecho |
| Migrar vistas a views.py con render() | Hecho |
| Configurar WhiteNoise y STATIC_ROOT | Hecho |
| Crear core/settings_prod.py borrador | Hecho |
| Actualizar requirements.txt (gunicorn, psycopg2) | Hecho |
| Crear tests/test_w02_mvt.py | Hecho |
| HU-E1-03 Repositorio GitHub: avance W02 commiteado | Hecho |


## Sprint 0 - Estado final W03

| HU | Estado | Puntos entregados |
|---|---|---|
| HU-E1-01 Entorno portable USB | Completada | 3 |
| HU-E1-02 Scripts sincronizacion | Completada | 2 |
| HU-E1-03 Repositorio GitHub | Completada | 2 |
| HU-E1-04 Despliegue Render.com | Completada | 3 |
| **Total entregado** | | **10 / 10** |

## Hito M1 - ALCANZADO
- URL publica: https://erp-django-utec-3116.onrender.com
- Tests: 35 tests OK
- Fecha: 15/10/2026
