from pathlib import Path

NOMBRE = "Resendiz Araiza Maya Gpe"
INICIO = "__/__/2026"
CIERRE = "29/10/2026"

Path("fichas").mkdir(exist_ok=True)

Path("sprint2_retrospective.md").write_text(f"""# Sprint 2 Retrospective — ERP Django
## Semanas W07–W09 · Espiral 3: CRUD Web y Autenticación

**Fecha:** {CIERRE}

## ¿Qué funcionó bien? (Keep)
1. select_related() en W07 evitó queries N+1 desde el inicio.
2. reverse_lazy() en las vistas basadas en clases evitó errores de configuración.
3. El management command crear_grupos permite configurar roles sin tocar el admin.
4. Usar scripts generadores (gen_w08/gen_w09) aceleró la creación de archivos.

## ¿Qué mejorar? (Improve)
1. Documentar el orden de LoginRequiredMixin + PermissionRequiredMixin.
2. Con raise_exception=True, un anónimo recibe 403 en lugar de redirigir al login.
3. Agregar la app 'core' a INSTALLED_APPS para que se detecte crear_grupos.
4. Agregar template 403.html personalizado.

## Acción de mejora (Kaizen) para Sprint 3
> En el Sprint 3 (DRF) documentaré los endpoints con docstrings desde el inicio.

## Velocidad del Sprint 2

| HU | Pts plan. | Pts ent. |
|---|---|---|
| HU-E3-01 a HU-E3-09 | 27 | 27 |

**Velocidad Sprint 2:** 27 puntos
**Velocidad acumulada (S0+S1+S2):** 58 puntos
""", encoding="utf-8")

Path("fichas/espiral_03_crud_auth.md").write_text(f"""# Ficha de Sistematización — Espiral 3
## ERP Django · Espiral E3: CRUD Web y Autenticación

| Campo | Contenido |
|---|---|
| **Número de espiral** | 3 |
| **Nombre del ciclo** | CRUD Web y Autenticación |
| **Semanas** | W07 – W09 |
| **Fecha de inicio** | {INICIO} |
| **Fecha de cierre** | {CIERRE} |
| **Responsable** | {RESENDIA ARAIZA MAYA GPE.} |
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
""", encoding="utf-8")

print("listo")
## Hito M3 - ALCANZADO
- CRUD: 4 modulos con lectura y escritura
- Auth: allauth con login/logout
- RBAC: 3 grupos (Gerente/Vendedor/Almacen)
- Tests: Ran 108 tests - OK
- Fecha: 29/10/2026
