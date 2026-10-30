# Sprint 2 Retrospective — ERP Django
## Semanas W07–W09 · Espiral 3: CRUD Web y Autenticación

**Fecha:** 29/10/2026

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
