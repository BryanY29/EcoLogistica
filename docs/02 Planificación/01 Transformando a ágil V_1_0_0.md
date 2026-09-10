# Transformando a ágil

[← Volver al README Principal](../../README.md)

## 1. Información general

| Campo | Detalle |
|---|---|
| Proyecto | EcoLogística |
| Fase | 02 - Planificación del Proyecto |
| Enfoque | Híbrido |
| Marco de trabajo | Scrum |
| Versión | V_1_0_0 |
| Ubicación | El Tambo, Huancayo y Chilca |
| Release inicial | v1.0.0-MVP |
| Duración del Sprint 1 | 2 semanas |

---

## 2. Objetivo

El presente documento transforma los requisitos funcionales y no funcionales definidos durante la fase de inicio del proyecto EcoLogística en un backlog ágil estructurado bajo el marco de trabajo Scrum.

La transformación considera una jerarquía compuesta por Épicas, Historias de Usuario, Enablers técnicos, tareas y subtareas. Las funcionalidades se priorizan de acuerdo con el valor de negocio y el riesgo técnico, utilizando Story Points basados en la secuencia de Fibonacci: 1, 2, 3, 5, 8 y 13.

El proyecto mantiene un enfoque híbrido, combinando una planificación inicial estructurada con una ejecución iterativa e incremental mediante Scrum.

---

# 3. Transformación de requisitos a estructura ágil

## 3.1 Jerarquía Scrum del proyecto

La estructura utilizada para organizar el backlog es la siguiente:

```mermaid
flowchart TD
    P[Proyecto EcoLogística]

    P --> EP01[EP-01 Gestión de acceso y usuarios]
    P --> EP02[EP-02 Gestión de operaciones logísticas]
    P --> EP03[EP-03 Planificación y optimización de rutas]
    P --> EP04[EP-04 Seguimiento y entregas]
    P --> EP05[EP-05 Indicadores y sostenibilidad]
    P --> EP06[EP-06 Seguridad, auditoría y plataforma]

    EP01 --> US001[US-001 Iniciar sesión]
    EP01 --> US002[US-002 Gestionar usuarios]

    EP02 --> US003[US-003 Registrar vehículos]
    EP02 --> US004[US-004 Registrar puntos de entrega]
    EP02 --> US005[US-005 Registrar pedidos]

    EP03 --> US006[US-006 Generar rutas]
    EP03 --> US007[US-007 Visualizar rutas]
    EP03 --> US008[US-008 Reoptimizar rutas]

    EP04 --> US009[US-009 Consultar pedidos]
    EP04 --> US010[US-010 Registrar entregas]

    EP05 --> US011[US-011 Consultar indicadores]
    EP05 --> US012[US-012 Consultar indicadores ambientales]
    EP05 --> US013[US-013 Exportar información]

    EP06 --> US014[US-014 Consultar auditoría]
    EP06 --> US015[US-015 Configurar parámetros]

    EP06 --> EN001[EN-001 Rendimiento de consultas]
    EP06 --> EN002[EN-002 Seguridad y autorización]
    EP06 --> EN003[EN-003 Disponibilidad]
    EP06 --> EN004[EN-004 Integridad de datos]
    EP06 --> EN005[EN-005 Pruebas de usabilidad]
    EP06 --> EN006[EN-006 Compatibilidad web]
    EP06 --> EN007[EN-007 Mantenibilidad]
    EP06 --> EN008[EN-008 Pruebas de carga]
    EP06 --> EN009[EN-009 Recuperación]
    EP06 --> EN010[EN-010 Auditoría]
    EP06 --> EN011[EN-011 Protección de información]
    EP06 --> EN012[EN-012 Optimización de consumo]