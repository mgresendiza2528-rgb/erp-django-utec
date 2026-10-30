# Ficha de Sistematización — Espiral 3
## ERP Django · Espiral E3: CRUD Web y Autenticación

| Campo | Contenido |
|---|---|
| **Número de espiral** | 3 |
| **Nombre del ciclo** | CRUD Web y Autenticación |
| **Semanas** | W07 – W09 |
| **Fecha de inicio** | 29/10/2026 |
| **Fecha de cierre** | 29/10/2026 |
| **Responsable** | Resendiz Araiza Maya Gpe |
| **Asesor** | MC. Román Fernando López González |

## 1. Objetivo del ciclo
Implementar la interfaz web del ERP con vistas de lectura y escritura, formularios validados, autenticación con allauth y control de acceso por rol (RBAC) con 3 grupos.

## 2. Tareas realizadas
1. ListView + DetailView x 4 entidades (W07)
2. Formularios y vistas Create/Update/Delete (W08)
3. django-allauth, templates login/signup (W09)
4. Command crear_grupos (Gerente, Vendedor, Almacén)
5. PermissionRequiredMixin en borrado y decoradores en crear_venta
6. 10 tests RBAC; suite acumulada de 108 tests

## 3. Evidencias
- Tests: Ran 108 tests -> OK
- Grupos: 32 / 6 / 7 permisos
- Repositorio: github.com/mgresendiza2528-rgb/erp-django-utec

## 4. Problemas encontrados
- crear_grupos no se detectaba hasta agregar 'core' a INSTALLED_APPS.
- Tests de W08 dieron 403 al exigir permisos; se usó create_superuser.
- Un anónimo recibe 403 (no redirección) por raise_exception=True.

## 5. Lecciones aprendidas
1. Los management commands solo se detectan en apps instaladas.
2. Los permisos nuevos obligan a ajustar los tests anteriores.
3. Conviene probar cada rol a mano además de los tests.

## 6. Tiempo total invertido

| Categoría | Horas |
|---|---|
| Diseño | |
| Implementación | |
| Pruebas | |
| Documentación | |
| **Total Espiral 3** | |
