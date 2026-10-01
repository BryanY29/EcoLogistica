# Spec Delta

## Purpose

Permite que los usuarios de EcoLogística consulten y operen la interfaz web en un tema claro u oscuro, con una paleta oscura legible en todos los elementos de la aplicación y una preferencia que se recuerda entre visitas.

## ADDED Requirements

### Requirement: Alternar el tema de la interfaz
El sistema SHALL ofrecer un control en la interfaz web que permita al usuario cambiar entre el tema claro y el tema oscuro. El tema activo SHALL aplicarse a todas las vistas de la aplicación de forma inmediata al activar el control.

#### Scenario: Cambio a tema oscuro
- **WHEN** el usuario activa el modo oscuro desde el control de tema
- **THEN** el sistema aplica la paleta oscura a la vista visible

#### Scenario: Regreso al tema claro
- **WHEN** el usuario activa el modo claro desde el control de tema
- **THEN** el sistema aplica la paleta clara a la vista visible

#### Scenario: El tema activo alcanza a todas las vistas
- **WHEN** el usuario cambia de tema y luego navega entre las vistas de puntos de entrega y de optimización de rutas
- **THEN** el sistema mantiene el tema activo en todas las vistas

### Requirement: Persistir la preferencia de tema
El sistema SHALL recordar el tema elegido por el usuario y SHALL reaplicarlo al volver a cargar la aplicación o al iniciar una sesión posterior, sin requerir que el usuario vuelva a seleccionarlo.

#### Scenario: Preferencia conservada tras recargar
- **WHEN** el usuario selecciona el tema oscuro y luego recarga la página
- **THEN** el sistema presenta la aplicación en tema oscuro

#### Scenario: Preferencia conservada en una visita posterior
- **WHEN** el usuario seleccionó un tema en una visita anterior y vuelve a abrir la aplicación sin haber cambiado la configuración del sistema
- **THEN** el sistema presenta la aplicación en el tema que el usuario había seleccionado

### Requirement: Seguir la preferencia del sistema en ausencia de elección
Cuando el usuario no haya realizado una selección de tema, el sistema SHALL determinar el tema a partir de la preferencia de tema del sistema operativo o del navegador.

#### Scenario: El sistema operativo prefiere el tema oscuro
- **WHEN** el usuario no ha seleccionado un tema y su sistema operativo está configurado en modo oscuro
- **THEN** el sistema presenta la aplicación en tema oscuro

#### Scenario: El sistema operativo prefiere el tema claro
- **WHEN** el usuario no ha seleccionado un tema y su sistema operativo está configurado en modo claro
- **THEN** el sistema presenta la aplicación en tema claro

#### Scenario: La selección del usuario prevalece sobre la del sistema
- **WHEN** el usuario ha seleccionado un tema y su sistema operativo está configurado en el modo contrario
- **THEN** el sistema presenta la aplicación en el tema seleccionado por el usuario

### Requirement: Paleta oscura legible en todos los elementos
El sistema SHALL presentar en tema oscuro todos los elementos visuales de la aplicación con colores adaptados a dicho tema. SHALL mantener legibles el contraste entre texto y superficie de fondo en superficies, textos, campos de entrada, selectores, tablas, botones y mensajes de aviso, incluidos los estados primario, secundario y de peligro.

#### Scenario: Superficies, texto y campos de entrada
- **WHEN** la aplicación se presenta en tema oscuro
- **THEN** el fondo general, las tarjetas y los campos de entrada y selectores presentan fondos oscuros con texto legible

#### Scenario: Tablas de listados
- **WHEN** la aplicación se presenta en tema oscuro y se visualiza un listado de puntos de entrega
- **THEN** el texto de las celdas y de los encabezados, así como los separadores entre filas, resultan legibles sobre el fondo del tema oscuro

#### Scenario: Mensajes de aviso
- **WHEN** la aplicación se presenta en tema oscuro y se muestra un mensaje de éxito o de error
- **THEN** el texto y el fondo del mensaje resultan legibles y el mensaje mantiene su distinción entre éxito y error

#### Scenario: Estados de los botones
- **WHEN** la aplicación se presenta en tema oscuro y se visualizan los botones de acción, secundario y de peligro
- **THEN** el texto de cada botón resulta legible sobre su propio fondo en todos los estados, incluido el estado deshabilitado

### Requirement: Aplicar el tema sin parpadeo inicial
El sistema SHALL determinar y aplicar el tema vigente antes de representar el contenido de la aplicación, de modo que no se presente un destello del tema contrario antes de estabilizarse el tema correcto.

#### Scenario: Carga con tema oscuro almacenado
- **WHEN** el usuario tiene el tema oscuro almacenado y carga la aplicación
- **THEN** el sistema no muestra contenido en tema claro antes de presentar la aplicación en tema oscuro

### Requirement: El tema no altera el comportamiento funcional
El cambio de tema SHALL NOT modificar el comportamiento de los flujos funcionales de la aplicación. El registro, la consulta, la modificación y la desactivación de puntos de entrega, así como la generación de rutas, SHALL producir los mismos resultados independientemente del tema activo.

#### Scenario: Registro de un punto de entrega en tema oscuro
- **WHEN** el usuario registra un punto de entrega válido desde la interfaz en tema oscuro
- **THEN** el sistema lo almacena y lo muestra en el listado, con el mismo resultado que en tema claro

#### Scenario: Generación de ruta en tema oscuro
- **WHEN** el usuario solicita la generación de una ruta desde la interfaz en tema oscuro
- **THEN** el sistema devuelve el mismo orden de visita, la misma distancia total y la misma estimación de emisiones que en tema claro
