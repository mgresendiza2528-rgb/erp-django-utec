# Sprint 1 Retrospective — ERP Django
## Semanas W04–W06 · Espiral 2: Modelado de Datos y ORM

**Fecha:** 27/10/2026

## ¿Qué funcionó bien? (Keep)
1. Diseñar el diagrama ER antes de escribir código evitó errores de claves foráneas.
2. Correr la suite completa de tests después de cada cambio detectó a tiempo un error en el `__str__` de Producto.
3. Jazzmin mejora mucho la experiencia del panel admin con poco código.

## ¿Qué mejorar? (Improve)
1. Documentar el diagrama ER con más detalle antes de la revisión del asesor.
2. Usar `full_clean()` en los tests desde el principio, no solo `save()`.
3. Guardar copias de los archivos antes de reemplazarlos completos, para no perder detalles de la W05.

## Acción de mejora (Kaizen) para Sprint 2
> "En el Sprint 2 voy a crear primero los templates y las rutas
>  en urls.py antes de escribir las vistas, y voy a correr la suite
>  completa de tests antes de cada commit."

## Velocidad del Sprint 1

| HU | Puntos planificados | Puntos entregados |
|---|---|---|
| HU-E2-01 Diagrama ER aprobado | 3 | 3 |
| HU-E2-02 Modelo Cliente | 2 | 2 |
| HU-E2-03 Modelo Proveedor | 2 | 2 |
| HU-E2-04 Modelo Categoria | 1 | 1 |
| HU-E2-05 Modelo Producto | 3 | 3 |
| HU-E2-06 Modelos Venta + Detalle | 5 | 5 |
| HU-E2-07 Suite ≥ 15 tests | 3 | 3 |
| HU-E2-08 Admin con Jazzmin | 2 | 2 |
| **Total** | **21** | **21** |

**Velocidad del equipo Sprint 1:** 21 puntos
**Velocidad acumulada (S0 + S1):** 31 puntos