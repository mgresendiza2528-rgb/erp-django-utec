# Ficha de Sistematización — Espiral 2
## ERP Django · Espiral E2: Modelado de Datos y ORM
## UTEC Celaya · Técnico en Programación (SEP 3061300006-23)

| Campo | Contenido |
|---|---|
| **Número de espiral** | 2 |
| **Nombre del ciclo** | Modelado de Datos y ORM |
| **Semanas** | W04 – W06 |
| **Fecha de inicio** | 19/10/2026 |
| **Fecha de cierre** | 27/10/2026 |
| **Responsable** | Resendiz Araiza Maya Gpe |
| **Asesor** | MC. Román Fernando López González |

---

## 1. Objetivo del ciclo

Diseñar, implementar y validar el esquema de base de datos completo del
ERP en Django, garantizando integridad referencial, normalización 3FN y
cobertura de pruebas ≥ 15 tests de modelo.

---

## 2. Tareas realizadas

| # | Tarea | Estado | Tiempo invertido |
|---|---|---|---|
| 1 | Diseño diagrama ER (8 entidades) | ✅ W04 | h:mm |
| 2 | Normalización 3FN y decisiones de diseño | ✅ W04 | h:mm |
| 3 | Aprobación del asesor | ⏳ al revisar W05/W06 | — |
| 4 | Implementar models.py × 5 apps | ✅ W05 | h:mm |
| 5 | Ejecutar makemigrations + migrate | ✅ W05 | h:mm |
| 6 | Registrar en admin.py | ✅ W05 | h:mm |
| 7 | Agregar validators y clean() | ✅ W06 | h:mm |
| 8 | Suite de ≥ 15 tests de modelo | ✅ W06 | h:mm |
| 9 | Instalar django-jazzmin | ✅ W06 | h:mm |

---

## 3. Evidencias generadas

- [x] Diagrama ER: `docs/diagramas/diagrama_er.md`
- [ ] Imagen exportada: `evidencias/espiral_02/diagrama_er.png` (pendiente)
- [x] Decisiones de diseño: `docs/decisiones_diseno.md`
- [x] Tabla de entidades: `docs/entidades_atributos.md`
- [x] Migraciones: `ventas/migrations/0002_validators_pedido.py` y `0001_initial.py` de las apps
- [x] Tests: `tests/test_w06_validadores.py` — resultado: 17/17 OK (suite completa: 72 OK)
- [x] Panel admin con tema Jazzmin (azul marino y dorado)

Registro de commits de W06:

```
e5c362a Sprint 1 W06: Jazzmin + estilos AzulERP
0463271 Sprint 1 W06: clean() + migracion 0002 + 72 tests OK [pre-M2]
```

---

## 4. Criterios de aceptación

| Criterio | Estado | Evidencia |
|---|---|---|
| Diagrama ER aprobado por el asesor | ⏳ | Firma en ficha |
| `showmigrations` → `[X] 0001_initial` en 5 apps | ✅ | Terminal |
| `[X] 0002_validators_pedido` en ventas | ✅ | Terminal |
| `/admin/` muestra las 8 entidades | ⏳ | Captura |
| ≥ 15 tests de modelo PASSED | ✅ | 17 OK en test_w06_validadores |
| Precio negativo → ValidationError | ✅ | test_precio_negativo_lanza_validation_error |
| Correo duplicado → IntegrityError | ✅ | test_correo_duplicado_cliente_lanza_integrity_error |

---

## 5. Problemas encontrados y soluciones

| Problema | Causa | Solución aplicada |
|---|---|---|
| La terminal del plantel no llegó a GitHub ni a PyPI | La red bloquea las conexiones de la terminal | Se usó la red del celular para el push |
| sprint1_planning.md se pegó sobre sprint0_planning.md | Archivo equivocado al pegar | Se restauró con git checkout y se separaron los dos archivos |
| La suite acumulada falló 1 test de W05 (`__str__` de Producto) | Al reemplazar el archivo completo se perdió el precio en el `__str__` | Se restauró `f"{nombre} (${precio:.2f})"` y la suite quedó en 72 OK |
| `makemigrations` decía "No changes detected" | La migración 0002 ya se había creado en un intento anterior | Se verificó con `dir` y solo se aplicó con `migrate` |

---

## 6. Lecciones aprendidas

1. `save()` no ejecuta los validators; hay que usar `full_clean()` en los tests
   para que `ValidationError` se dispare.
2. Correr la suite completa de tests después de cada cambio detecta a tiempo
   errores en código que ya funcionaba.
3. Antes de reemplazar un archivo completo hay que revisar su contenido
   actual, para no perder detalles de semanas anteriores.

---

## 7. Aprobación formal

| Campo | Contenido |
|---|---|
| **Fecha de aprobación** | ___/___/_____ |
| **Observaciones del asesor** | |
| **Firma** | |