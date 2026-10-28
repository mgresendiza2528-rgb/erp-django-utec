# Sprint 2 Planning — ERP Django
## Semanas W07–W09 · Espiral 3: CRUD Web y Autenticación

**Sprint Goal:**
Al finalizar el Sprint 2, el ERP mostrará lista y detalle de las
entidades principales, con formularios de alta/edición/borrado
protegidos por autenticación y 3 roles de acceso.

**Duración:** W07 (ListView/DetailView) · W08 (Create/Update/Delete) · W09 (Auth + RBAC · M3)

## HUs seleccionadas

| ID | Historia | Puntos | Semana |
|---|---|---|---|
| HU-E3-01 | Ver la lista de productos | 2 | W07 |
| HU-E3-02 | Ver el detalle de un producto | 2 | W07 |
| HU-E3-03 | Ver listas de clientes y proveedores | 2 | W07 |
| HU-E3-04 | Ver el detalle de ventas con sus líneas | 3 | W07 |
| HU-E3-05 | Crear y editar productos | 3 | W08 |
| HU-E3-06 | Registrar nuevas ventas con detalles | 5 | W08 |
| HU-E3-07 | Eliminar registros con confirmación | 2 | W08 |
| HU-E3-08 | Autenticación login/logout funcional | 3 | W09 |
| HU-E3-09 | 3 roles con permisos diferenciados | 5 | W09 |

**Total Sprint 2:** 27 puntos

## Sprint Backlog — estado W07

| Tarea | Estado |
|---|---|
| ListView + DetailView para productos, clientes, proveedores y ventas | ✅ W07 |
| 8 templates lista.html + detalle.html | ✅ W07 |
| urls.py con rutas lista y detalle | ✅ W07 |
| select_related / prefetch_related anti N+1 | ✅ W07 |
| Tests de vistas de lectura | ✅ W07 |
| CreateView + UpdateView + DeleteView | ⏳ W08 |
| Login/Logout + LoginRequiredMixin | ⏳ W09 |
| 3 roles RBAC | ⏳ W09 |
