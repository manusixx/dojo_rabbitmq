# Guía de contribución

Este documento describe cómo se colabora en el repositorio. Toda contribución debe seguir este flujo.

## Estrategia de ramas

```
main  <-- PR <--  develop  <-- PR <--  mpastrana
```

### Ramas principales

| Rama | Propósito | Reglas |
| --- | --- | --- |
| `main` | Versión validada del dojo | Se actualiza solo desde `develop` y con una versión completa y probada. Cada merge lleva una etiqueta semántica (por ejemplo `v1.0.0`). Protegida |
| `develop` | Integración | Solo recibe cambios mediante PR. Protegida |
| `mpastrana` | Rama personal del director del proyecto | Aquí se desarrolla el trabajo antes de promoverlo. Permite push directo |

### Reglas del flujo

**Trabajo en `mpastrana`**

- Commits frecuentes y con mensajes que sigan la convención de este documento.
- Validación local antes de cada push (Puerta 1).
- Antes de abrir un PR, traer los últimos cambios de `develop`.

**Promoción a `develop`**

- Solo cuando el cambio está completo y probado.
- El PR debe describir qué se hizo y cómo se verificó.
- Se hace merge con *merge commit* (no squash), para que `mpastrana` y `develop` mantengan el mismo historial y no aparezcan conflictos en el siguiente PR.

**Promoción a `main`**

- Solo con una versión validada de extremo a extremo.
- Requiere etiqueta semántica sobre el commit de merge (por ejemplo `v1.0.0`).
- Se hace merge con *merge commit*, igual que en `develop`.

Las ramas `main` y `develop` están protegidas por un ruleset de GitHub: no admiten push directo ni force push, y solo se actualizan mediante PR. El dueño del repositorio fusiona sus propios PR con un bypass limitado a pull requests.

## Umbral de calidad

**Umbral 1: validación local (antes de cada push)**

1. `docker-compose config -q` no muestra errores.
2. `docker-compose up -d --build` deja los servicios en `Up`.
3. Prueba de extremo a extremo: se publica un mensaje, la cola queda en 0 y aparece la fila en SQLite.

**Umbral 2: revisión del diff**

Antes de fusionar un PR, el director del proyecto revisa el diff completo y confirma que el cambio corresponde con lo descrito.

## Convención de commits

Se usa Conventional Commits: `tipo: descripción corta en minúscula y sin punto final`.

| Tipo | Uso |
| --- | --- |
| `feat` | Funcionalidad nueva |
| `fix` | Corrección de un error |
| `docs` | Cambios en documentación (README, guía, este archivo) |
| `refactor` | Reorganización de código sin cambiar su comportamiento |
| `chore` | Configuración, dependencias y tareas de mantenimiento |
| `test` | Pruebas |

Ejemplos: `feat: persistir notificaciones en SQLite`, `docs: aclarar merge commit y protección de ramas`.

## Pull requests

- Se abre desde `mpastrana` hacia `develop`, y luego desde `develop` hacia `main`.
- Se completa la plantilla de `.github/pull_request_template.md`. Solo se marca lo que realmente se verificó.
- Si el PR resuelve un issue, se vincula con `Closes #N`.

## Issues

Los errores y las mejoras se registran como issues, con una descripción clara, los pasos para reproducirlo y el resultado esperado.

## Definición de terminado

Un cambio se considera terminado cuando:

- Pasó la Puerta 1 y la Puerta 2.
- La documentación afectada (README o guía en `docs/`) está actualizada.
- No incluye secretos reales ni archivos generados.
- El PR fue fusionado y las ramas locales quedaron sincronizadas.