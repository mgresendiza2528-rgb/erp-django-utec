# Ficha Schmelkes - Espiral 1
## ERP Django - Espiral E1: Infraestructura y Configuracion Base
## UTEC Celaya - Tecnico en Programacion (SEP 3061300006-23)

| Campo | Contenido |
|---|---|
| **Numero de espiral** | 1 |
| **Nombre del ciclo** | Infraestructura y Configuracion Base |
| **Semanas** | W01 - W03 |
| **Fecha de inicio** | 28/09/2026 |
| **Fecha de cierre** | 15/10/2026 |
| **Responsable** | Resendiz Araiza Maya Gpe |
| **Asesor** | MC. Roman Fernando Lopez Gonzalez |

## 1. Objetivo del ciclo

Establecer el entorno de desarrollo portable en USB y desplegar el proyecto Django base en Render.com, de modo que cualquier avance posterior tenga una URL publica verificable desde el inicio del proyecto.

## 2. Tareas realizadas

| # | Tarea | Estado | Tiempo invertido |
|---|---|---|---|
| 1 | Configurar Python 3.11 embeddable en USB | Hecho | |
| 2 | Instalar pip y virtualenv | Hecho | |
| 3 | Configurar Git Portable | Hecho | |
| 4 | Crear scripts iniciar/finalizar sesion | Hecho | |
| 5 | Crear proyecto Django con 5 apps | Hecho | |
| 6 | Sistema de templates Fable 5 AzulERP | Hecho | |
| 7 | Configurar WhiteNoise y estaticos | Hecho | |
| 8 | Completar settings_prod.py con PostgreSQL | Hecho | |
| 9 | Crear Procfile, Dockerfile, docker-compose.yml | Hecho | |
| 10 | Crear render.yaml | Hecho | |
| 11 | Desplegar en Render.com (URL publica) | Hecho | |
| 12 | Sprint 0 Review y Retrospectiva | Pendiente (review en vivo) | |

## 3. Evidencias generadas

- Repositorio GitHub: https://github.com/mgresendiza2528-rgb/erp-django-utec
- URL publica Render: https://erp-django-utec-3116.onrender.com/
- Captura de pantalla: evidencias/espiral_01/render_url.png
- Resultado de tests: Ran 35 tests - OK
- Retrospectiva: sprint0_retrospective.md

## 4. Criterios de aceptacion verificados

| Criterio | Cumplido | Evidencia |
|---|---|---|
| manage.py check sin errores | Si | Terminal: 0 issues |
| URL publica responde HTTP 200 | Si | Pagina cargando en Render |
| Repositorio con al menos 6 commits en main | Si | git log --oneline |
| Tests pasando (W01 + W02 + W03) | Si | 35 tests OK |
| Ficha Schmelkes E1 completa | Si | Este documento |

## 5. Problemas encontrados y soluciones

| Problema | Causa | Solucion aplicada |
|---|---|---|
| Git decia "not a git repository" | La variable GIT_DIR apuntaba a Git_Portable | Se borro con SET GIT_DIR= y se agrego al script de inicio |
| Git no veia mis cambios | Edite la copia de la USB y no la de la PC | Copiar el archivo a ERP_Work y abrir el proyecto con "code ." |
| Un test del admin fallaba | Faltaba la carpeta staticfiles con el manifiesto | Ejecutar python manage.py collectstatic antes de correr los tests |
| Falto psycopg2-binary en requirements.txt | No se habia instalado | Lo detecto un test de W03; se instalo y se actualizo el archivo |
| La red del aula bloqueaba PyPI y GitHub | El firewall del aula | Usar los datos del celular y guardar get-pip.py en la USB |
| Python y Git quedaban vacios (0 bytes) y el perfil se borraba al cerrar sesion | La USB escribia lento y el aula limpia el perfil | Respaldos .zip y .7z.exe en la USB y reinstalacion automatica desde iniciar_sesion.bat |

## 6. Lecciones aprendidas

1. Los tests automaticos encuentran errores antes de desplegar.
2. Hay que verificar siempre en que carpeta se esta editando un archivo.
3. Un commit pequeno se puede deshacer sin perder trabajo.

## 7. Tiempo total invertido

| Categoria | Horas |
|---|---|
| Diseno / planeacion | |
| Implementacion | |
| Pruebas | |
| Despliegue | |
| Documentacion | |
| **Total Espiral 1** | |

## 8. Conexion con el trabajo recepcional

Esta espiral aporta evidencia para el Capitulo 4 (Desarrollo), seccion 4.1 "Espiral 1: Infraestructura", y para el Capitulo 3 (Metodologia), subseccion "Ciclos del modelo espiral".

## 9. Resultado de git log --oneline -5
2694771 Sprint 0 W03: evidencias de la Espiral 1 (capturas de Render)
1880d7d Sprint 0 W03: estado final del sprint y hito M1
1d6493b Sprint 0 W03: retrospectiva y ficha Schmelkes E1
6ede581 Sprint 0 W03: Procfile sin espacios extra
24a2f3d Sprint 0 W03: tests de despliegue y psycopg2-binary en requirements (35 tests OK)
