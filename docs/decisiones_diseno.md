# Decisiones de Diseño — ERP Django
## Espiral 2 · Modelo Entidad-Relación

---

### D-01: Producto → Categoria usa on_delete=PROTECT

**Decisión:** No permitir borrar una categoría si tiene productos asociados.

**Alternativas consideradas:**
- `CASCADE`: borraría todos los productos de esa categoría (peligroso)
- `SET_NULL`: dejaría productos sin categoría (viola integridad de negocio)

**Consecuencia:** Para borrar una categoría, primero hay que reasignar sus productos.

---

### D-02: Producto → Proveedor usa on_delete=SET_NULL, null=True

**Decisión:** Un producto puede existir sin proveedor asignado.

**Justificación:** Productos fabricados internamente o de proveedor desconocido.
Al borrar un proveedor, los productos no desaparecen; quedan sin proveedor.

---

### D-03: Venta → Cliente usa on_delete=PROTECT

**Decisión:** No borrar un cliente con historial de ventas.

**Justificación:** El historial de ventas es un registro contable.
Se usa `activo=False` para dar de baja sin borrar datos.

---

### D-04: Venta.total es propiedad calculada (NO campo de BD)

**Decisión:** `total` se calcula en tiempo de ejecución, no se almacena.

```python
@property
def total(self):
    return sum(d.subtotal for d in self.detalles.all())
```

**Justificación:** Almacenar `total` crearía una dependencia transitiva
(viola 3FN). Además, si se modifica una línea, el total calculado
siempre es correcto.

**Advertencia de rendimiento:** Para dashboards con miles de ventas,
usar `annotate(total=Sum(...))` en lugar de la property.

---

### D-05: DetalleVenta → Producto usa on_delete=PROTECT

**Decisión:** No borrar un producto que tuvo ventas históricas.

**Justificación:** Los reportes históricos referencian productos.
Se usa `activo=False` en Producto para descontinuar sin borrar.

---

### D-06: DetalleVenta.precio_unitario es campo almacenado

**Decisión:** Almacenar el precio al momento de la venta, no derivarlo
de `Producto.precio`.

**Justificación:** El precio de un producto puede cambiar después de la
venta. El histórico debe reflejar el precio realmente cobrado.

---

### D-07: ConfiguracionERP como singleton

**Decisión:** Una sola fila de configuración global del sistema.

**Implementación:** Sobrescribir `save()` para que siempre use `pk=1`,
y en el admin deshabilitar el botón "Agregar".