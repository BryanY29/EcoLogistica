# Artefactos Jira

[← Volver al README Principal](../../README.md)

## 1. Información general

| Campo                 | Información                     |
| --------------------- | ------------------------------- |
| Proyecto              | EcoLogística                    |
| Fase                  | 02 - Planificación del Proyecto |
| Enfoque               | Híbrido                         |
| Herramienta           | Jira                            |
| Metodología           | Scrum                           |
| Release               | v1.0.0-MVP                      |
| Sprint inicial        | Sprint 1                        |
| Duración              | 2 semanas                       |
| Ámbito                | El Tambo, Huancayo y Chilca     |
| Versión del documento | V_1_0_0                         |

---

# 2. Configuración del proyecto en Jira

El proyecto EcoLogística será configurado en Jira utilizando un proyecto de tipo Scrum.

La estructura del trabajo seguirá la jerarquía:

```text
Epic
│
├── Story
│   ├── Sub-task
│   └── Sub-task
│
├── Enabler / Task
│
└── Bug
```

El tablero utilizará cuatro estados principales:

```text
To Do → In Progress → In Review / QA → Done
```

---

# 3. Componentes

Para organizar el backlog se utilizarán componentes relacionados con los principales módulos del proyecto.

| Componente      | Descripción                                          |
| --------------- | ---------------------------------------------------- |
| Autenticación   | Inicio de sesión y control de acceso.                |
| Usuarios        | Gestión de usuarios y roles.                         |
| Operaciones     | Vehículos, puntos de entrega y pedidos.              |
| Rutas           | Generación, visualización y optimización de rutas.   |
| Entregas        | Seguimiento y registro de entregas.                  |
| Indicadores     | Indicadores operativos y ambientales.                |
| Seguridad       | Seguridad, autorización y protección de información. |
| Auditoría       | Trazabilidad y registros del sistema.                |
| Infraestructura | Despliegue, disponibilidad y configuración técnica.  |

---

# 4. Evidencia 01 - Roadmap

## Objetivo

Demostrar que el proyecto posee una planificación temporal de sus principales Épicas, funcionalidades y releases.

### Captura de Jira

> **Insertar aquí la captura real del Roadmap de Jira.**

```text
[PEGAR CAPTURA DEL ROADMAP AQUÍ]
```

### Descripción

El Roadmap permite visualizar la planificación de las principales Épicas de EcoLogística y su evolución hacia el release v1.0.0-MVP.

La planificación considera inicialmente:

* Gestión de acceso y usuarios.
* Gestión de operaciones logísticas.
* Planificación de rutas.
* Seguimiento de entregas.
* Indicadores.
* Seguridad y auditoría.

### Requisito de la captura

La captura debe mostrar únicamente el panel de Jira correspondiente al Roadmap.

**No debe aparecer:**

* Escritorio de Windows.
* Barra de tareas.
* Pestañas innecesarias del navegador.
* Ventanas externas.
* Espacios excesivos alrededor de Jira.

---

# 5. Evidencia 02 - Backlog priorizado

## Objetivo

Demostrar que las Historias de Usuario se encuentran registradas, priorizadas y estimadas mediante Story Points.

### Captura de Jira

> **Insertar aquí la captura real del backlog de Jira.**

```text
[PEGAR CAPTURA DEL BACKLOG AQUÍ]
```

### Elementos que deben ser visibles

La captura debe permitir identificar:

* Épicas.
* Historias de Usuario.
* Prioridad.
* Story Points.
* Componentes.
* Orden de prioridad.

### Historias principales

| ID     | Resumen                           | SP | Prioridad | Componente    |
| ------ | --------------------------------- | -: | --------- | ------------- |
| US-001 | Iniciar sesión                    |  3 | Alta      | Autenticación |
| US-002 | Gestionar usuarios                |  5 | Alta      | Usuarios      |
| US-003 | Registrar vehículos               |  3 | Alta      | Operaciones   |
| US-004 | Registrar puntos de entrega       |  5 | Alta      | Operaciones   |
| US-005 | Registrar pedidos                 |  5 | Alta      | Operaciones   |
| US-006 | Generar rutas                     | 13 | Muy Alta  | Rutas         |
| US-007 | Visualizar rutas                  |  5 | Alta      | Rutas         |
| US-008 | Reoptimizar rutas                 | 13 | Alta      | Rutas         |
| US-009 | Consultar pedidos                 |  3 | Alta      | Entregas      |
| US-010 | Registrar entregas                |  5 | Alta      | Entregas      |
| US-011 | Consultar indicadores             |  5 | Media     | Indicadores   |
| US-012 | Consultar indicadores ambientales |  5 | Media     | Indicadores   |
| US-013 | Exportar información              |  3 | Media     | Indicadores   |
| US-014 | Consultar auditoría               |  3 | Media     | Auditoría     |
| US-015 | Configurar parámetros             |  5 | Baja      | Seguridad     |

---

# 6. Evidencia 03 - Sprint Planning y Sprint Goal

## Objetivo

Demostrar la planificación del Sprint 1 y la definición de su objetivo.

### Sprint

**Sprint 1**

**Duración:** 2 semanas

### Sprint Goal

> Construir el núcleo operativo inicial de EcoLogística permitiendo autenticar usuarios, registrar vehículos, puntos de entrega y pedidos, dejando la información preparada para la primera planificación de rutas.

### Trabajo planificado

| ID     | Trabajo                     | Story Points |
| ------ | --------------------------- | -----------: |
| US-001 | Iniciar sesión              |            3 |
| US-002 | Gestionar usuarios          |            5 |
| US-003 | Registrar vehículos         |            3 |
| US-004 | Registrar puntos de entrega |            5 |
| US-005 | Registrar pedidos           |            5 |
| EN-002 | Seguridad y autorización    |            5 |
| EN-004 | Integridad de datos         |            5 |

**Total planificado: 31 Story Points.**

### Captura de Jira

> **Insertar aquí la captura real del Sprint Planning de Jira.**

```text
[PEGAR CAPTURA DEL SPRINT PLANNING AQUÍ]
```

La captura debe mostrar el Sprint 1, el trabajo seleccionado y, cuando sea posible, el Sprint Goal.

---

# 7. Evidencia 04 - Scrum Board activo

## Objetivo

Demostrar que el tablero Scrum se encuentra configurado y que las actividades pueden gestionarse mediante flujo de trabajo.

### Flujo

```text
To Do
   ↓
In Progress
   ↓
In Review / QA
   ↓
Done
```

### Captura de Jira

> **Insertar aquí la captura real del tablero Scrum activo.**

```text
[PEGAR CAPTURA DEL SCRUM BOARD AQUÍ]
```

### Descripción

El tablero permitirá visualizar el estado de cada Story, Enabler, Task o Bug.

La columna **To Do** representa el trabajo pendiente.

La columna **In Progress** representa las actividades actualmente en desarrollo.

La columna **In Review / QA** representa actividades implementadas que deben pasar por revisión técnica y/o pruebas.

La columna **Done** representa elementos que cumplen la Definition of Done.

---

# 8. Evidencia 05 - Releases

## Objetivo

Demostrar la creación del release v1.0.0-MVP y la asociación de las historias correspondientes.

### Release

**v1.0.0-MVP**

### Objetivo del Release

Entregar un Producto Mínimo Viable que permita gestionar el núcleo inicial de las operaciones logísticas y preparar la planificación de rutas.

### Funcionalidades asociadas

* Inicio de sesión.
* Gestión de usuarios.
* Registro de vehículos.
* Registro de puntos de entrega.
* Registro de pedidos.
* Consulta de pedidos.
* Generación de rutas.
* Visualización de rutas.
* Seguridad.
* Integridad de datos.

### Captura de Jira

> **Insertar aquí la captura real de Releases / Versions de Jira.**

```text
[PEGAR CAPTURA DE RELEASES AQUÍ]
```

La captura debe permitir comprobar:

* Nombre de la versión.
* Release v1.0.0-MVP.
* Historias asociadas.
* Estado o progreso de la versión cuando Jira lo muestre.

---

# 9. Relación entre documentación y Jira

La configuración de Jira debe mantener coherencia con el documento:

`01 Transformando a ágil V_1_0_0.md`

La correspondencia principal será:

```text
Documentación
      │
      ▼
Épicas
      │
      ▼
Historias de Usuario
      │
      ▼
Story Points
      │
      ▼
Sprint 1
      │
      ▼
v1.0.0-MVP
```

---

# 10. Calidad de las evidencias

Las capturas utilizadas como evidencia deben ser claras y legibles.

Cada captura deberá:

1. Mostrar únicamente la interfaz relevante de Jira.
2. Estar recortada al panel o contenedor correspondiente.
3. Evitar mostrar el escritorio.
4. Evitar mostrar la barra de tareas.
5. Evitar mostrar pestañas innecesarias del navegador.
6. Evitar espacios vacíos excesivos.
7. Mantener visibles los datos necesarios para comprobar la configuración.

La evidencia visual debe permitir verificar directamente la configuración descrita en este documento.

---

# 11. Conclusión

La configuración de Jira permite trasladar el backlog definido para EcoLogística hacia una herramienta de gestión ágil. Las Épicas, Historias de Usuario, Story Points, Sprint, tablero y Release permiten realizar seguimiento del desarrollo de forma iterativa.

El uso de Jira complementa el enfoque híbrido del proyecto, ya que la documentación formal se mantiene en el repositorio mientras que la ejecución y seguimiento del trabajo se realiza mediante prácticas Scrum.
