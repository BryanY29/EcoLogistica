# Revisión del sprint

**Nombre del Proyecto:** EcoLogística
**Líder del Proyecto:** ZEVALLOS MELENDRES YIMER EDYSON

[← Volver al README](../../README.md)

## Historias de Usuario completadas en este Sprint

Durante el Sprint 1 se completaron las funcionalidades correspondientes a la estructura base del sistema, backend, persistencia, gestión de puntos de entrega y optimización de rutas.

Las principales funcionalidades completadas fueron:

* Configuración de la arquitectura base `backend/`, `frontend/` y `db/`.
* Implementación y verificación del backend FastAPI.
* Configuración de PostgreSQL mediante Docker Compose.
* Gestión de puntos de entrega mediante API.
* Validación de coordenadas y distritos permitidos.
* Cálculo de distancia mediante Haversine.
* Optimización de rutas.
* Cálculo de emisiones de CO₂.
* Endpoint para solicitar la optimización de una ruta.
* Pruebas unitarias, de API e integración asociadas a las funcionalidades implementadas.

## Demostración del trabajo completado

Se realizó la revisión del trabajo desarrollado durante el Sprint 1, mostrando principalmente el funcionamiento del backend y sus servicios asociados.

La demostración contempló la gestión de puntos de entrega, las validaciones correspondientes, la generación de rutas optimizadas, el cálculo de la distancia total y la estimación de emisiones de CO₂.

También se verificó el funcionamiento del endpoint de salud y la documentación de la API mediante Swagger/OpenAPI.

## Pendientes

Las funcionalidades pendientes corresponden principalmente a la capa de interfaz y a actividades de calidad y cierre:

* Completar las vistas React para la gestión de puntos de entrega.
* Completar la interfaz de optimización de rutas.
* Integrar y validar visualmente los mensajes de error.
* Ejecutar las verificaciones de lint.
* Medir la cobertura de pruebas.
* Completar la documentación de instalación y ejecución del proyecto.
* Ejecutar la validación end-to-end del sistema completo.
