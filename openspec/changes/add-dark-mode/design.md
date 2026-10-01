# Design

## Context

El frontend (`frontend/`) es una SPA de Vite + React con CSS plano, sin librería de estilos y solo dos dependencias en tiempo de ejecución (`react`, `react-dom`). No hay framework de pruebas para el frontend.

El punto de partida relevante es que `styles.css` ya define ocho custom properties en `:root` (`--green`, `--green-dark`, `--bg`, `--card`, `--text`, `--muted`, `--danger`, `--border`), pero **9 literales de color están escritos directamente en 11 reglas**, evitando por completo ese sistema de variables:

```
  #fff                  x3  header{color}, button{color}, input/select{background}
  #e8f5e9               x3  nav button{color}, nav button.active{border-color},
                           .alert.success{background}
  rgba(255,255,255,.15)     nav button.active{background}
  #eef3ee                   button.secondary{background}
  #e2eae2                   button.secondary:hover{background}
  #8e0000                   button.danger:hover{background}
  #fdecea                   .alert.error{background}
  #f5c6c0                   .alert.error{border}
  #bfe3c3                   .alert.success{border}
```

Ver `proposal.md` para la motivación. Los requisitos están en `specs/dark-mode/spec.md`.

## Goals / Non-Goals

**Goals:**
- Llevar el 100 % de los colores de la aplicación a variables CSS, de modo que el tema sea un dato y no una regla duplicada.
- Añadir la paleta oscura como una redefinición de variables, sin duplicar ninguna regla de estilo existente.
- Prevenir el parpadeo de tema incorrecto en la carga inicial.
- Mantener la dependencia mínima del proyecto: cero paquetes nuevos.

**Non-Goals:**
- No se toca el backend ni la API; el contrato HTTP no cambia.
- No se themea la documentación OpenAPI/Swagger en `/docs` (superficie dirigida al desarrollador, con su propio tema).
- No se introduce un framework de pruebas para el frontend ni se amplía la cobertura de pruebas automatizadas. La verificación es lint, build y comprobación manual en navegador.
- No se migra a CSS Modules, Tailwind ni a una librería de theming: la reescritura de estilos excede el alcance de un cambio de tema.

## Decisions

### 1. Mecanismo: atributo `data-theme` en `<html>` y redefinición de variables

La paleta oscura se define en un bloque `[data-theme="dark"]` que solo reescribe valores de variables. Ninguna regla de estilo se duplica.

Razón: el proyecto ya usa custom properties, de modo que las variables ya son la capa de tematización; falta únicamente la segunda paleta y el selector que la activa. Alternativas descartadas:
- **Solo `@media (prefers-color-scheme: dark)`** — no ofrece control explícito al usuario ni persistencia, y el requisito de alternancia no se cumpliría.
- **Librería de theming** — desproporcionada para una SPA con dos dependencias; introduciría estado global y dependencias para algo que el CSS resuelve.

### 2. Los literales hardcodeados se convierten en variables semánticas, y dos de ellos se dividen

Este es el trabajo de fondo del cambio y la razón por la que «agregar modo oscuro» no es solo agregar un interruptor. Una sustitución literal de `#fff` por una variable fallaría: el mismo literal cumple dos roles opuestos.

```
  #fff    ->  --on-accent      texto sobre fondo verde (header, botones)
             --field-bg        fondo de campos de entrada y selectores

  #e8f5e9 ->  --on-accent-soft texto de la navegación sobre el header
             --success-bg      fondo del aviso de éxito
```

En ambos casos un valor funciona como *texto claro sobre superficie oscura* y como *superficie clara para texto oscuro*. Una sola variable no puede servir a los dos roles, y elegir una dejaría el otro desatendido. Las demás literales sí mapean 1:1 a una variable.

Razón: la legibilidad en tema oscuro es un requisito normativo (`specs/dark-mode/spec.md`), no una preferencia estética, así que el mapeo debe ser semántico y no nominal.

### 3. Preferencia del sistema por defecto, con prioridad a la elección explícita

Orden de resolución: **elección guardada → preferencia del sistema → tema claro**.

Además, si el usuario no ha realizado ninguna elección, la aplicación **escucha en caliente** los cambios de la preferencia del sistema, para que un cambio de tema del sistema operativo se refleje sin recargar. Una vez que el usuario elige explícitamente, deja de seguir al sistema.

Razón: seguir al sistema por defecto es la convención esperable y evita una pantalla clara inesperada a quien trabaja de noche. Registrar el evento del sistema solo mientras no exista elección explícita mantiene esa expectativa sin sorprender al usuario que sí expresa una preferencia.

### 4. Aplicación antes del render: script bootstrap en `index.html`

Un `useEffect` en React aplicaría el tema **después** del primer render, produciendo un parpadeo. Se inserta un script pequeño y síncrono en el `<head>` de `index.html` que lee la preferencia y fija el atributo del tema antes de que se cargue el módulo de la aplicación.

Razón: el requisito de ausencia de parpadeo es observable por el usuario, no un detalle interno, por lo que no puede depender del momento de hidratación. Alternativa descartada: aplicar una clase desde el propio React (produce el mismo parpadeo).

### 5. Contraste como criterio de aceptación de la paleta

La paleta oscura se elige con contraste mínimo WCAG AA: 4.5:1 para texto normal y 3:1 para texto grande y bordes de componente. Al elegirse a mano, ese umbral es el criterio objetivo de «legible» del requisito, y no un juicio subjetivo.

## Risks / Trade-offs

- **[Dos literales cumplen roles opuestos y una sustitución ingenua rompe la legibilidad]** → El mapeo por rol de la decisión 2 es explícito y es tarea propia; se verifica en navegador cada elemento afectado, no solo el conjunto.
- **[Contraste insuficiente en la paleta oscura, especialmente en los avisos de éxito y error]** → Umbral WCAG AA como criterio; los avisos son los fondos más propensos a fallar por ser tintes suaves.
- **[El script bootstrap duplica la lógica de resolución del tema con el módulo React]** → Riesgo real de divergencia. Se mitiga manteniendo el bootstrap mínimo (leer preferencia, fijar atributo) y delegando en React toda la lógica de escritura y de escucha; el valor por defecto se declara en un único lugar mediante variable CSS.
- **[No hay pruebas automatizadas que protejan la legibilidad]** → Se acepta explícitamente. La verificación es lint, build y revisión manual en navegador, lo que deja la comprobación de contraste fuera de la regresión automática.
- **[Un tema oscuro sobre tablas y separadores puede reducir la densidad visual]** → Se conservan los bordes en el tema oscuro en lugar de eliminarlos, para no perder la legibilidad de la estructura del listado.
- **[El control de tema es un elemento nuevo en la cabecera y altera la composición existente]** → Se ubica junto a la navegación, que ya es el único chrome persistente; verificar que no rompe el diseño en anchos pequeños.

## Migration Plan

- Sin migración de datos ni de esquema: el cambio es exclusivamente de presentación.
- No requiere coordinación de despliegue con el backend; puede publicarse de forma independiente.
- Reversión: revertir el commit del frontend. No hay estado persistente en el servidor ni migraciones que deshacer. La única traza en el cliente es una entrada en `localStorage`, cuya presencia es inocua si la aplicación vuelve a la versión anterior.
