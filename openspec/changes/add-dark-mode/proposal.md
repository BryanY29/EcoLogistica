# Proposal

## Why

La interfaz web de EcoLogística está construida sobre una paleta exclusivamente clara y fija: no ofrece ninguna forma de alternar el tema, y el color de fondo de las tarjetas, textos y botones está parcialmente desconectado del sistema de variables CSS. Esto dificulta la lectura en condiciones de poca luz a los usuarios que consultan o registran entregas en campo (operadores y planificadores), y deja la capa visual sin un mecanismo de theming que pueda crecer hacia adelante.

## What Changes

- Convertir en **variables CSS semánticas los 9 literales de color actualmente hardcodeados** en `frontend/src/styles.css` (11 sitios), de modo que toda la superficie visual pase a depender de variables y no de colores literales.
- Incorporar una **paleta oscura** como redefinición de esas variables bajo un selector de tema, sin duplicar reglas de estilo.
- Añadir un **control de tema en la interfaz** (en la cabecera de la aplicación) que permita alternar entre tema claro y oscuro de forma explícita.
- **Persistir la preferencia** del usuario en `localStorage` y, en ausencia de preferencia guardada, **seguir la preferencia del sistema** (`prefers-color-scheme`).
- Aplicar el tema **antes del primer render** mediante un script bootstrap en `index.html`, evitando un parpadeo de tema incorrecto al cargar.
- Fuera de alcance: cualquier cambio en el backend o la API, la incorporation de dependencias nuevas, el theming de la documentación OpenAPI/Swagger en `/docs`, y la incorporación de un framework de pruebas automatizadas para el frontend.

## Capabilities

### New Capabilities

- `dark-mode`: Selección, persistencia y aplicación de un tema claro u oscuro en la interfaz web de EcoLogística, incluyendo la disponibilidad de una paleta oscura legible para todos los elementos visuales de la aplicación.

### Modified Capabilities

- Ninguna. No existen specs previas en el repositorio (`openspec list --specs` está vacío). El modo oscuro no altera el comportamiento de los flujos funcionales de registro de puntos de entrega ni de generación de rutas, por lo que no modifica requisitos de ninguna capacidad existente.

## Impact

- **Código frontend (nuevo)**: un módulo de gestión de tema (p. ej. `frontend/src/theme.js`) que exponga la lectura de la preferencia persistida y su aplicación sobre el elemento raíz, y un control de tema en la cabecera de la aplicación.
- **Código frontend (modificado)**: `frontend/src/styles.css` (conversión de literales a variables y paleta oscura) e `frontend/index.html` (script bootstrap previo al render).
- **Sin impacto en la API**: no se agregan, modifican ni eliminan endpoints; el contrato de `GET /api/v1/delivery-points` y `POST /api/v1/routes/optimize` permanece igual.
- **Sin impacto en la base de datos**: no hay migraciones ni cambios de esquema.
- **Dependencias**: ninguna nueva. La implementación se apoya en CSS custom properties, `localStorage` y `window.matchMedia`, todos disponibles en el stack actual (Vite + React, CSS plano). El proyecto conserva su dependencia mínima de dos paquetes en tiempo de ejecución.
- **Verificación**: el proyecto no cuenta con framework de pruebas para el frontend, de modo que la validación de este cambio es `npm run lint` sin errores, `npm run build` sin errores y verificación manual en navegador. La cobertura de pruebas del backend no se ve afectada porque no se modifica código del backend.
