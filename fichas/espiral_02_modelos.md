# Ficha de Sistematización — Espiral 2
## ERP Django · Espiral E2: Modelado de Datos y ORM
## UTEC Celaya · Técnico en Programación (SEP 3061300006-23)

| Campo | Contenido |
|---|---|
| **Número de espiral** | 2 |
| **Nombre del ciclo** | Modelado de Datos y ORM |
| **Semanas** | W04 – W06 |
| **Fecha de inicio** | 19/10/2026 |
| **Fecha de cierre** | (completar en W06) |
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
| 3 | Aprobación del asesor | ⏳ W04 | — |
| 4 | Implementar models.py × 5 apps | ⏳ W05 | — |
| 5 | Ejecutar makemigrations + migrate | ⏳ W05 | — |
| 6 | Registrar en admin.py | ⏳ W05 | — |
| 7 | Agregar validators | ⏳ W06 | — |
| 8 | Suite de ≥ 15 tests de modelo | ⏳ W06 | — |
| 9 | Instalar django-jazzmin | ⏳ W06 | — |

---

## 3. Evidencias generadas (completar durante W04–W06)

- [ ] Diagrama ER aprobado: `docs/diagramas/diagrama_er.md`
- [ ] Imagen exportada: `evidencias/espiral_02/diagrama_er.png`
- [ ] Decisiones de diseño: `docs/decisiones_diseno.md`
- [ ] Tabla de entidades: `docs/entidades_atributos.md`
- [ ] Migraciones: `*/migrations/0001_initial.py` × 5 apps
- [ ] Tests: `tests/test_models.py` — resultado: ___/15 OK

---

## 4. Criterios de aceptación (se verifican en W06)

| Criterio | Estado | Evidencia |
|---|---|---|
| Diagrama ER aprobado por el asesor | ⏳ | Firma en ficha |
| `showmigrations` → `[X] 0001_initial` en 5 apps | ⏳ | Terminal |
| `/admin/` muestra las 8 entidades | ⏳ | Captura |
| ≥ 15 tests de modelo PASSED | ⏳ | Salida de tests |
| Precio negativo → ValidationError | ⏳ | Test específico |
| Correo duplicado → IntegrityError | ⏳ | Test específico |

---

## 5. Problemas encontrados y soluciones

| Problema | Causa | Solución aplicada |
|---|---|---|
| La terminal del plantel no llegó a GitHub ni a PyPI | La red bloquea las conexiones de la terminal | Se dejó el push y los tests para otra red |
| sprint1_planning.md se pegó sobre sprint0_planning.md | Archivo equivocado al pegar | Se restauró con git checkout y se separaron los dos archivos |

---

##