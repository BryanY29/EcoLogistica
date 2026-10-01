# Spec Delta

## Purpose

Define la gestión de puntos de entrega dentro de El Tambo, Huancayo y Chilca y la generación de rutas sostenibles que ordenan la visita de destinos minimizando la distancia recorrida y estimando las emisiones de CO₂, base del módulo de optimización de rutas de EcoLogística.

## ADDED Requirements

### Requirement: Registrar punto de entrega
El sistema SHALL permitir registrar un punto de entrega cuando se proporcione nombre, dirección, latitud, longitud y distrito válidos. El distrito SHALL pertenecer exclusivamente al ámbito geográfico El Tambo, Huancayo o Chilca. La latitud SHALL estar entre -90 y 90 y la longitud entre -180 y 180.

#### Scenario: Registro exitoso en el ámbito geográfico
- **WHEN** se registra un punto de entrega con datos válidos y distrito El Tambo, Huancayo o Chilca
- **THEN** el sistema almacena el punto de entrega y lo deja disponible para la planificación de rutas

#### Scenario: Distrito fuera del ámbito geográfico
- **WHEN** se intenta registrar un punto de entrega con un distrito distinto de El Tambo, Huancayo o Chilca
- **THEN** el sistema rechaza el registro e indica que el ámbito geográfico no es válido

#### Scenario: Ubicación inválida
- **WHEN** se intenta registrar un punto de entrega con latitud o longitud fuera de los rangos válidos
- **THEN** el sistema rechaza el registro e informa el error de ubicación

#### Scenario: Datos obligatorios incompletos
- **WHEN** se intenta registrar un punto de entrega omitiendo un dato obligatorio
- **THEN** el sistema impide el registro y señala los campos requeridos

### Requirement: Consultar puntos de entrega
El sistema SHALL permitir consultar los puntos de entrega registrados y SHALL retornar la información de cada punto (identificador, nombre, dirección, latitud, longitud y distrito).

#### Scenario: Consulta del listado
- **WHEN** se consulta el listado de puntos de entrega
- **THEN** el sistema retorna todos los puntos de entrega registrados y habilitados con su información

#### Scenario: Consulta por identificador inexistente
- **WHEN** se consulta un punto de entrega por un identificador que no existe
- **THEN** el sistema informa que el punto de entrega no está disponible

### Requirement: Modificar punto de entrega
El sistema SHALL permitir modificar los datos permitidos de un punto de entrega registrado, aplicando las mismas validaciones de ámbito geográfico y ubicación del registro.

#### Scenario: Modificación exitosa
- **WHEN** se modifican datos válidos de un punto de entrega existente
- **THEN** el sistema guarda la información actualizada

#### Scenario: Modificación hacia un distrito no permitido
- **WHEN** se intenta modificar el distrito de un punto de entrega hacia un valor fuera de El Tambo, Huancayo o Chilca
- **THEN** el sistema rechaza el cambio e indica el motivo

### Requirement: Desactivar punto de entrega
El sistema SHALL permitir desactivar un punto de entrega registrado. Un punto de entrega desactivado SHALL conservar su registro y NO SHALL ser considerado como destino en la generación de rutas.

#### Scenario: Desactivación de un punto de entrega
- **WHEN** se desactiva un punto de entrega
- **THEN** el sistema mantiene el registro con estado desactivado y lo excluye de la planificación de rutas

#### Scenario: Desactivar un punto de entrega inexistente
- **WHEN** se intenta desactivar un punto de entrega por un identificador que no existe
- **THEN** el sistema informa que el punto de entrega no está disponible

### Requirement: Generar ruta sostenible
El sistema SHALL generar una propuesta de ruta cuando se proporciona un punto de origen válido y al menos un punto de entrega válido y habilitado. La ruta SHALL retornar el orden de visita de los puntos, la distancia total recorrida y la estimación de emisiones de CO₂. El orden de visita SHALL minimizar la distancia total recorrida entre los destinos solicitados.

#### Scenario: Generación exitosa de ruta
- **WHEN** se solicitan rutas con un origen válido y dos o más puntos de entrega habilitados
- **THEN** el sistema retorna una propuesta que visita todos los puntos solicitados exactamente una vez, comenzando por el origen, sin repetir destinos

#### Scenario: Consistencia de la distancia total
- **WHEN** se genera una ruta
- **THEN** el sistema retorna una distancia total igual a la suma de las distancias geodésicas entre cada par de puntos consecutivos del orden de visita

#### Scenario: Estimación de emisiones de CO₂
- **WHEN** se genera una ruta
- **THEN** el sistema retorna una estimación de emisiones de CO₂ calculada a partir de la distancia total recorrida y el factor de emisión configurado

#### Scenario: Determinismo de la propuesta
- **WHEN** se solicitan rutas con los mismos puntos de origen y destinos en más de una ocasión
- **THEN** el sistema retorna el mismo orden de visita en todas las ocasiones

#### Scenario: Origen inexistente o inválido
- **WHEN** se solicitan rutas con un punto de origen inexistente o inválido
- **THEN** el sistema rechaza la solicitud e informa el error

#### Scenario: Sin destinos disponibles
- **WHEN** se solicitan rutas sin puntos de entrega válidos y habilitados
- **THEN** el sistema informa que no es posible generar la ruta porque no existen destinos disponibles

### Requirement: Gestionar puntos de entrega desde la interfaz
El sistema SHALL permitir desde la interfaz web registrar, consultar, modificar y desactivar puntos de entrega, y solicitar la generación de la ruta sobre los puntos habilitados.

#### Scenario: Registro desde la interfaz
- **WHEN** un usuario registra un punto de entrega con datos válidos desde la interfaz
- **THEN** el sistema muestra el punto de entrega registrado en el listado

#### Scenario: Solicitud de ruta desde la interfaz
- **WHEN** un usuario solicita la generación de la ruta seleccionando puntos de entrega habilitados desde la interfaz
- **THEN** el sistema muestra el orden de visita, la distancia total y la estimación de emisiones de CO₂ de la ruta generada