# Tasks

## 1. Estructura del repositorio y scaffolding

- [x] 1.1 Crear la estructura de directorios `backend/`, `frontend/` y `db/` con la separación de capas documentada y verificar que los directorios previstos existen
- [x] 1.2 Inicializar `backend/` como proyecto FastAPI con `pyproject.toml`, app factory en `app/main.py` y configuración en `app/core/config.py` (distritos permitidos, factor de emisión en env `CO2_FACTOR`) y verificar que la app responde en una ruta de salud (`GET /health` → 200)
- [x] 1.3 Inicializar `frontend/` con Vite + React y un cliente HTTP para la API, y verificar que `npm run build` compila sin errores
- [x] 1.4 Crear `docker-compose.yml` y `db/` con el servicio PostgreSQL y verificar que `docker compose up -d db` deja la base escuchando en el puerto configurado

## 2. Persistencia y modelo de datos

- [ ] 2.1 Configurar Alembic en `backend/` y crear la migración inicial con la tabla `puntos_entrega` (punto_id UUID, nombre, direccion, latitud NUMERIC(9,6), longitud NUMERIC(9,6), distrito, estado VARCHAR(20) DEFAULT 'ACTIVO') y el índice por distrito, y verificar que `alembic upgrade head` se ejecuta sin errores contra la base
- [x] 2.2 Implementar el modelo SQLAlchemy `DeliveryPoint` y el repositorio (`list_active`, `get`, `create`, `update`, `deactivate`) y verificar que las pruebas unitarias del repositorio pasan con una base de prueba SQLite/PostgreSQL
- [x] 2.3 Verificar que no se crean en este cambio las tablas `rutas`/`detalle_ruta` y que el esquema aplicado coincide con el modelo documentado más la columna `estado`

## 3. Gestión de puntos de entrega (API)

- [x] 3.1 Implementar el servicio de puntos de entrega con validaciones (campos obligatorios, latitud en [-90,90], longitud en [-180,180], distrito ∈ El Tambo/Huancayo/Chilca) y verificar que las pruebas unitarias cubren los casos válidos e inválidos
- [x] 3.2 Implementar los endpoints `GET /api/v1/delivery-points` (con filtro opcional por distrito), `POST`, `GET /{id}`, `PUT /{id}` y `DELETE /{id}` (desactivación lógica) y verificar con pruebas de API que: listado retorna solo habilitados (escenario "Consulta del listado"), 404 para id inexistente, 400 para distrito fuera de ámbito, ubicación inválida y datos incompletos
- [x] 3.3 Verificar que los errores de validación retornan `400`/`404` con mensaje descriptivo y que la documentación OpenAPI se genera automáticamente en `GET /docs`

## 4. Optimización de rutas (API)

- [x] 4.1 Implementar el módulo de geometría (distancia haversine) y verificar con pruebas unitarias que la distancia entre dos coordenadas conocidas coincide con el valor esperado dentro de una tolerancia definida
- [x] 4.2 Implementar el optimizador de ruta (TSP abierto: búsqueda exhaustiva para n ≤ 8, vecino más cercano + 2-opt para n > 8) y verificar con pruebas unitarias que cubre todos los destinos exactamente una vez, no repite destinos y es determinista (mismos inputs → mismo orden)
- [x] 4.3 Implementar el cálculo de emisiones CO₂ (distancia_total × factor de emisión) y verificar con pruebas unitarias que el resultado es el esperado para un factor y distancia dados
- [x] 4.4 Implementar el endpoint `POST /api/v1/routes/optimize` con esquema Pydantic (`origin: {lat,lng}`, `delivery_point_ids`) y verificar con pruebas de API que: retorna orden + distancia total consistente (escenario "Consistencia de la distancia total") + emisiones, rechaza origen inválido (400/404), rechaza solicitudes sin destinos habilitados y excluye puntos desactivados
- [x] 4.5 Verificar que la generación de ruta realiza como máximo 1 consulta principal a la base de datos (RNF-012) y documentar el resultado en la prueba de integración

## 5. Interfaz web (React)

- [ ] 5.1 Implementar la vista de listado y alta de puntos de entrega (formulario con validación de los tres distritos) y verificar manualmente que un punto registrado aparece en el listado (escenario "Registro desde la interfaz")
- [ ] 5.2 Implementar la edición y desactivación de puntos de entrega en la interfaz y verificar manualmente que los cambios se reflejan en el listado y que un punto desactivado deja de aparecer en selecciones de ruta
- [ ] 5.3 Implementar la vista de optimización (selección de destinos habilitados, origen, y resultado con orden de visita, distancia total y emisiones de CO₂) y verificar manualmente el escenario "Solicitud de ruta desde la interfaz"
- [ ] 5.4 Verificar que las vistas consumen el backend mediante el cliente HTTP y que los errores de validación se muestran al usuario en español

## 6. Integración, calidad y documentación

- [x] 6.1 Agregar pruebas de integración que ejecuten el flujo completo (registrar puntos → optimizar ruta → verificar distancia y emisiones) contra una base de prueba y verificar que la suite completa (`pytest`) pasa
- [ ] 6.2 Ejecutar el análisis estático/lint del backend y frontend (p. ej. `ruff`, `eslint`) sin errores y medir cobertura de pruebas del backend con objetivo ≥ 80 % (DoD)
- [ ] 6.3 Escribir el `README.md` del repositorio con instrucciones de instalación, migración y ejecución (docker compose, alembic, backend, frontend) y verificar que cada comando documentado se ejecuta tal como está escrito
- [ ] 6.4 Ejecutar una verificación final end-to-end (backend + frontend + PostgreSQL levantados con docker compose) recorriendo los flujos de puntos de entrega y generación de ruta, y confirmar funcionamiento en navegador