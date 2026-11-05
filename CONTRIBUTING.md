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
- Se hace merge con squash, para dejar un commit por cambio.

**Promoción a `main`**

- Solo con una versión validada de extremo a extremo.
- Requiere etiqueta