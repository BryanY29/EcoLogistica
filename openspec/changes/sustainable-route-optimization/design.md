# Design

## Context

No existe código fuente en el repositorio: solo documentación de las fases de inicio y planificación (docs/). El stack definido es Python + FastAPI + React + PostgreSQL, con arquitectura en capas Presentación → Controladores → Servicios → Repositorios → PostgreSQL (Modelo C4) y un enfoque híbrido (planificación predictiva + ejecución iterativa). Se implementa por primera vez el repositorio, partiendo de cero, por lo que este cambio también establece la base estructural que usarán cambios futuros (pedidos, vehículos, indicadores).

Ver proposal.md para motivación y alcance.

## Goals / Non-Goals

**Goals:**
- Establecer la estructura de repositorio (backend + frontend) alineada al stack documentado.
- Gestión completa de puntos de entrega (registro, consulta, modificación, desactivación) validando el ámbito El Tambo / Huancayo / Chilca.
- Generar rutas deterministas que minimicen la distancia total y estimen emisiones de CO₂.
- API REST documentada (OpenAPI) y UI React funcional para ambos flujos.
- Pruebas automatizadas del backend (>= 80 % cobertura según DoD).

**Non-Goals:**
- No se implementa en este cambio: pedidos, vehículos, rutas persistentes con vehículo/pedidos (RN-004, RN-008), autenticación/roles, indicadores históricos, re-optimización por cambios operativos, servicios de mapas externos.
- La ruta se calcula bajo demanda; no se persiste (las tablas `rutas`/`detalle_ruta` quedan reservadas para cuando existan pedidos y vehículos).

## Decisions

### 1. Estructura de repositorio (monorepo)
```
backend/          # FastAPI, separado por capas
  app/
    core/         # configuración, constantes (distritos, factor emisión)
    api/routes/   # controladores (endpoints)
    services/     # lógica de negocio y optimización
    repositories/ # acceso a PostgreSQL
    models/       # SQLAlchemy
    schemas/      # Pydantic (validación)
  alembic/        # migraciones
  tests/
frontend/         # React (Vite)
db/               # docker-compose, init
README.md
```
Razón: refleja el Modelo C4 y la separación controladores/servicios/repositorios documentada. Alternativa: monorepo sin separación de módulos — descartada por baja mantenibilidad (EN-007).

### 2. Cálculo de distancia y factor de emisión
- Distancia entre puntos con **haversine** (distancia geodésica de gran círculo) entre coordenadas lat/lng. Es determinista, sin dependencias externas y suficiente para el MVP; la documentación contempla evaluar servicios de mapas en iteraciones posteriores.
- Emisiones CO₂ = distancia_total_recorrida × factor de emisión (kg CO₂/km). Factor configurable vía `core/config.py` (env `CO2_FACTOR`) con valor por defecto documentado (p. ej. 0.254 kg CO₂/km), representativo de un vehículo liviano de reparto. No se implementa administración de parámetros (RF-015) en este cambio; el factor es una constante configurable.

### 3. Algoritmo de optimización de ruta
- TSP abierto (path) desde el origen hasta el último destino, minimizando la distancia total.
- `n <= 8` destinos: **búsqueda exhaustiva** de la permutación mínima (garantiza el óptimo y es viable por el bajo tamaño típico y el ámbito local).
- `n > 8`: heurística **vecino más cercano + 2-opt** (mejora local determinista). 
- Determinista: mismo origen y destinos ⇒ mismo orden (requisito del spec). Alternativas: solo greedy (calidad menor), metaheurísticas tipo GA (no deterministas y excesivas para el MVP).

### 4. Modelo de datos (delta sobre el modelo documentado)
- Tabla `puntos_entrega` conforme al doc (punto_id UUID, nombre, direccion, latitud NUMERIC(9,6), longitud NUMERIC(9,6), distrito).
- **Adición:** columna `estado VARCHAR(20) NOT NULL DEFAULT 'ACTIVO'` para soportar la desactivación lógica exigida por RF-004/generalización y RN-012 (eliminación lógica). La desactivación excluye el punto de la generación de rutas.
- Normalización e índices según doc (idx por distrito si se filtra por distrito).
- Se usa **Alembic** para migraciones (mantenibilidad, EN-004/EN-007).
- `rutas`/`detalle_ruta` no se crean ni modifican en este cambio (dependen de vehículos y pedidos; RN-008).

### 5. API (FastAPI, versión `/api/v1`)
| Método | Ruta | Función |
|---|---|---|
| GET | `/api/v1/delivery-points?distrito=` | Listar puntos habilitados (filtro opcional por distrito) |
| POST | `/api/v1/delivery-points` | Registrar punto |
| GET | `/api/v1/delivery-points/{punto_id}` | Consultar por id |
| PUT | `/api/v1/delivery-points/{punto_id}` | Modificar datos permitidos |
| DELETE | `/api/v1/delivery-points/{punto_id}` | Desactivar (lógica) |
| POST | `/api/v1/routes/optimize` | Generar ruta: body `{ origin: {lat, lng}, delivery_point_ids: [] }`; responde `{ order: [...], total_distance_km, co2_emissions_kg }` |

Validación con **Pydantic**: campos obligatorios, lat∈[-90,90], lng∈[-180,180], distrito ∈ {EL TAMBO, HUANCAYO, CHILCA} (case-insensitive, RN-014). Errores → 400/404 con detalle. Lat/lng adicionalmente dentro de los límites del ámbito geográfico (bounding box aproximado de los tres distritos) — decisión de validación razonable para reforzar RN-014; se registra como supuesto.

### 6. Frontend (React + Vite)
- Rutas/vistas: listado y alta/edición de puntos de entrega (formulario con validación de distrito), y vista de optimización (selección de destinos habilitados + origen + panel de resultados con orden de visita, distancia y CO₂).
- Llamadas HTTP al backend vía cliente API simple; sin servicio de mapas en esta iteración (visualización textual/ordenada). Interfaz en español.

### 7. Persistencia y eco-diseño (RNF-012)
- Listar puntos: 1 consulta. Generar ruta: 1 consulta (obtener destinos) + cómputo en memoria. ≤ 2 consultas principales por operación funcional.

## Risks / Trade-offs

- [Distancia geodésica (haversine) ≠ distancia real por calles] → Acto seguido en MVP sin servicio de mapas; se documenta para evaluar OSRM/mapas en iteraciones futuras manteniendo la interfaz del servicio de optimización aislada.
- [Heurística 2-opt para n>8 puede no ser el óptimo global] → Aceptable para el ámbito local (decenas de puntos máximo); determinismo garantiza reproducibilidad y pruebas.
- [Columna `estado` añadida al modelo documentado] → Supuesto registrado en el spec; la migración Alembic lo hace explícito y reversible.
- [Factor de emisión es una aproximación] → Configurable en `core/config.py`; su administración por parámetros (RF-015) queda fuera de alcance.
- [`puntos_entrega.estado` no está en el modelo documentado; pedidos/vehículos no existen aún] → Sin impacto en este cambio; las FKs de `rutas`/`detalle_ruta` se crearán cuando existan pedidos/vehículos.

## Migration Plan

- Repositorio nuevo (sin datos previos). El despliegue consiste en: levantar PostgreSQL (docker-compose), aplicar migraciones Alembic (`upgrade head`) y arrancar backend y frontend.
- Rollback: reversionar la migración Alembic (`downgrade`) elimina la tabla/schema; al no existir datos de producción previos, no requiere estrategia adicional.