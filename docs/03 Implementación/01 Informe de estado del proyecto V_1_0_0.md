# Revisión del sprint

**Nombre del Proyecto:** EcoLogística
**Líder del Proyecto:** ZEVALLOS MELENDRES YIMER EDYSON

[← Volver al README](../../README.md)

## Historias de Usuario completadas en este Sprint

Durante el Sprint 1 se completaron las funcionalidades relacionadas con la gestión de puntos de entrega y la optimización de rutas mediante el backend del sistema.

* Gestión de la estructura base del proyecto, separando `backend/`, `frontend/` y `db/`.
* Implementación del backend con FastAPI y configuración de la aplicación.
* Implementación y verificación del endpoint de salud `GET /health`.
* Implementación de la aplicación frontend con Vite + React y verificación de compilación mediante `npm run build`.
* Configuración de PostgreSQL mediante Docker Compose.
* Implementación del modelo `DeliveryPoint` y su repositorio.
* Implementación de validaciones para los puntos de entrega, considerando los distritos de El Tambo, Huancayo y Chilca.
* Implementación de los endpoints CRUD para puntos de entrega.
* Implementación de la documentación automática mediante OpenAPI/Swagger.
* Implementación del cálculo de distancia mediante Haversine.
* Implementación del optimizador de rutas.
* Implementación del cálculo de emisiones de CO₂.
* Implementación del endpoint de optimización de rutas.
* Implementación de pruebas de integración para el flujo de registro de puntos, optimización de ruta y verificación de distancia y emisiones.

## Demostración del trabajo completado

Demostración a los stakeholders de las funcionalidades implementadas durante el Sprint 1, considerando principalmente el funcionamiento del backend, la gestión de puntos de entrega, la optimización de rutas y el cálculo de emisiones de CO₂.

## Pendientes

Quedan pendientes para las siguientes iteraciones las funcionalidades de interfaz web y las actividades de calidad y cierre técnico:

* Implementar la vista de listado y registro de puntos de entrega.
* Implementar la edición y desactivación de puntos desde la interfaz.
* Implementar la vista de optimización de rutas.
* Mostrar los errores de validación al usuario en español.
* Ejecutar el análisis estático/lint del backend y frontend.
* Medir y verificar la cobertura de pruebas con el objetivo establecido.
* Completar el README con las instrucciones de instalación, migración y ejecución.
* Realizar la verificación final end-to-end con backend, frontend y PostgreSQL.
