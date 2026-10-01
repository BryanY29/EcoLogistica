# Proposal

## Why

El proyecto EcoLogística (Fase de inicio y planificación ya documentadas) aún no cuenta con código fuente: el núcleo operativo definido en el MVP (vehículos, puntos de entrega, pedidos) y la optimización de rutas (RF-006, RF-007) no están implementados. Este cambio inicia la implementación del **módulo de optimización de rutas sostenibles**, la capacidad central del proyecto dentro de El Tambo, Huancayo y Chilca, generando rutas que minimizan distancia recorrida y estiman las emisiones de CO₂ conforme a RNF-012/EN-012 y al enfoque híbrido del proyecto.

## What Changes

- Crear la estructura base del repositorio (backend FastAPI + frontend React + PostgreSQL) siguiendo las capas documentadas: Presentación → Controladores → Servicios → Repositorios → PostgreSQL (Modelo C4).
- Implementar la **gestión de puntos de entrega**: registro, consulta, modificación y desactivación dentro del ámbito geográfico El Tambo, Huancayo y Chilca (RF-004, RN-014). Los destinos registran: nombre, dirección, latitud, longitud y distrito.
- Implementar la **generación de rutas sostenibles**: dado un conjunto de puntos de entrega (como destinos) y un punto de origen, el sistema genera una propuesta de ruta determinística, ordenando la visita de los puntos para minimizar la distancia recorrida y calculando como métricas derivadas la distancia total y la estimación de emisiones de CO₂ (RF-006, RF-012, EN-012).
- Exponer una API REST (FastAPI) con endpoints para puntos de entrega y generación de rutas, con validación de entradas y consistencia de datos.
- Proveer una interfaz web (React) para registrar/consultar puntos de entrega y solicitar y visualizar la ruta generada (RF-007).
- Fuera de alcance en este cambio: pedidos, vehículos, re-optimización con cambios operativos, indicadores históricos y autenticación/roles completos. La ruta se genera sobre puntos de entrega como destinos; la integración con pedidos y vehículos se realizará en cambios posteriores.

## Capabilities

### New Capabilities

- `route-optimization`: Gestión de puntos de entrega en El Tambo, Huancayo y Chilca y generación de rutas sostenibles (orden de visita por distancia mínima con estimación de emisiones de CO₂ y distancia total).

### Modified Capabilities

- Ninguna. No existen specs previas en el repositorio (`openspec list --specs` está vacío).

## Impact

- **Código nuevo**: estructura del repositorio y módulos bajo `backend/` (API FastAPI: controladores, servicios, repositorios, esquemas) y `frontend/` (React: vistas de puntos de entrega y rutas).
- **Base de datos**: esquema inicial con la tabla `puntos_entrega`, agregando una columna de estado de habilitación sobre el modelo documentado (11. Base de datos) para soportar la desactivación de destinos. Las tablas `rutas`/`detalle_ruta` documentadas no se modifican en este cambio; la ruta se calcula bajo demanda.
- **API**: endpoints REST nuevos para puntos de entrega y generación de rutas; documentación OpenAPI/Swagger.
- **Dependencias**: FastAPI, SQLAlchemy o equivalente, y en frontend React junto con los manejos de HTTP/estado básicos. Sin servicios externos de mapas en esta iteración (la distancia se calcula con geodésica / haversine entre coordenadas).
- **Sistemas**: alcance restringido a El Tambo, Huancayo y Chilca (RN-014); eficiencia de cómputo (RNF-012): máx. 2 consultas principales por operación funcional.