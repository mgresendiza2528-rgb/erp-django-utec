# Sprint 4 Retrospective — ERP Django
## Semanas W13–W15 · Espiral 5: E-commerce y Pagos

**Fecha:** ___/___/_____

## ¿Qué funcionó bien? (Keep)
1. items_snapshot en el Pedido permite recuperar los items del carrito
   después de que la sesión fue limpiada.
2. La expresión F() actualiza el stock de forma atómica en la base de datos.
3. unittest.mock.patch permitió testear checkout y webhook sin claves reales.
4. Respaldar a la USB con robocopy evitó perder trabajo cuando una copia
   del proyecto resultó dañada.

## ¿Qué mejorar? (Improve)
1. Verificar la copia de trabajo (archivos vacíos o con bytes nulos) antes
   de empezar una sesión.
2. Hacer la prueba real con Stripe sandbox el mismo día, no dejarla pendiente.
3. Mantener sincronizadas las copias del proyecto para evitar push rechazados.

## Acción de mejora (Kaizen) para Sprint 5
> "Al iniciar cada sesión correré check y los tests antes de escribir código,
>  para detectar a tiempo archivos dañados."

## Velocidad del Sprint 4

| HU | Pts plan. | Pts ent. |
|---|---|---|
| HU-E5-01 Catálogo sin registro | 2 | 2 |
| HU-E5-02 Filtrar por categoría/precio | 3 | 3 |
| HU-E5-03 Agregar al carrito | 3 | 3 |
| HU-E5-04 Ver contenido del carrito | 2 | 2 |
| HU-E5-05 Checkout con datos del cliente | 3 | 3 |
| HU-E5-06 Pago con Stripe sandbox | 5 | 5 |
| HU-E5-07 Confirmar pago vía webhook | 5 | 5 |
| HU-E5-08 Descontar stock al confirmar | 3 | 3 |
| **Total** | **26** | **26** |

**Velocidad Sprint 4:** 26 puntos
**Velocidad acumulada (S0–S4):** 105 puntos
