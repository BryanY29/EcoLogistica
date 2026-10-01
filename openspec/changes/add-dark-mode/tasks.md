# Tasks

> El proyecto no tiene framework de pruebas para el frontend, de modo que la verificación de este cambio es `npm run lint`, `npm run build` y comprobación manual en navegador. Cada tarea indica cómo se comprueba; no se crean suites de pruebas nuevas.

## 1. Tokens de color

- [ ] 1.1 Convertir los 9 literales de color de `frontend/src/styles.css` en variables CSS semánticas en `:root`, dividiendo los dos literales que cumplen roles opuestos (`#fff` en `--on-accent` y `--field-bg`; `#e8f5e9` en `--on-accent-soft` y `--success-bg`) y mapeando el resto 1:1. Verificar que no queda ningún literal de color fuera de los bloques de variables y que `npm run lint` pasa sin errores.
- [ ] 1.2 Comprobar en el navegador que el tema claro es visualmente idéntico al previo en las dos vistas. Verificar por comparación del header, la navegación, las tarjetas, la tabla, los botones (incluidos secundario, hover de secundario y hover de peligro), los campos de entrada, los selectores y los avisos de éxito y de error.

## 2. Paleta oscura

- [ ] 2.1 Añadir en `frontend/src/styles.css` el bloque `[data-theme="dark"]` que redefine todas las variables, conservando los bordes en oscuro en lugar de eliminarlos. Verificar que solo se añaden valores de variables y que no se duplica ninguna regla de estilo, y que `npm run lint` pasa sin errores.
- [ ] 2.2 Ajustar los valores de la paleta oscura hasta alcanzar contraste WCAG AA: 4.5:1 para texto normal y 3:1 para texto grande y bordes de componente. Verificar con un comprobador de contraste todos los pares texto-superficie, con atención especial a los fondos de los avisos de éxito y de error, y registrar los valores medidos.

## 3. Resolución y persistencia de la preferencia

- [ ] 3.1 Crear `frontend/src/theme.js` con el orden de resolución elección guardada → preferencia del sistema → tema claro, la aplicación del tema sobre el elemento raíz y la persistencia de la elección explícita. Verificar en el navegador que, sin elección guardada, la aplicación sigue la preferencia del sistema en ambos sentidos, y que tras elegir un tema la elección prevalece sobre la del sistema.
- [ ] 3.2 Escuchar los cambios de la preferencia del sistema solo mientras no exista elección guardada, y dejar de seguir al sistema una vez que el usuario elija. Verificar que, sin elección guardada, un cambio de tema del sistema se refleja sin recargar, y que, con elección guardada, un cambio del sistema no altera el tema de la aplicación.

## 4. Aplicación del tema antes del render

- [ ] 4.1 Insertar en el `<head>` de `frontend/index.html` un script síncrono y mínimo que lea la preferencia y fije el atributo del tema antes de cargar el módulo de la aplicación, sin replicar la lógica de escritura ni de escucha. Verificar que, con el tema oscuro almacenado, una recarga con la red limitada no muestra contenido en tema claro antes de estabilizarse el tema oscuro.

## 5. Control de tema en la interfaz

- [ ] 5.1 Añadir el control de tema en la cabecera, junto a la navegación, conectado al módulo de tema, con nombre accesible y estado correctamente reflejado. Verificar que al activarlo el tema cambia de inmediato en la vista visible, en ambos sentidos, y que `npm run lint` pasa sin errores.
- [ ] 5.2 Comprobar que el tema activo se conserva al navegar. Verificar que, tras cambiar el tema, se recorren las vistas de puntos de entrega y de optimización de rutas y ambas mantienen el tema, sin que el diseño se rompa en anchos pequeños.

## 6. Verificación de integración

- [ ] 6.1 Ejecutar `npm run lint` y `npm run build` en `frontend/` y confirmar que terminan con código de salida 0 y sin advertencias nuevas. Verificar la salida completa de ambos comandos.
- [ ] 6.2 Comprobar la equivalencia funcional entre temas. Verificar que registrar, consultar, modificar y desactivar un punto de entrega, y generar una ruta, producen en tema oscuro exactamente los mismos resultados que en tema claro, incluido el orden de visita, la distancia total y la estimación de emisiones, y que la cobertura de pruebas del backend sigue pasando.
