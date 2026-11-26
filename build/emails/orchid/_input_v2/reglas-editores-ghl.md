# Cómo trata el HTML cada editor de GHL (probado el 26 nov 2026)

## 1. Workflow → Email → "Quick compose" → Source code — NO USAR para correos con diseño
- Envuelve todo el texto en `<p>` y le pone `font-family:verdana,geneva,sans-serif;font-size:16px; padding-left:0px!important`. Los titulares pierden Georgia y su tamaño.
- Borra **todos** los estilos de los `<a>`: los botones quedan como enlaces simples (se pierde fondo, padding y radio).
- Borra `background-color`, `display`, `padding` y `border-radius` de los `<span>`.
- Conserva tablas, `bgcolor` y estilos de los `<td>`.
- Uso aceptable: correos internos de texto (03).

## 2. Marketing → Emails → Templates → Code editor — USAR para workflows
- Conserva el HTML tal cual (probado con 01, 02, 04 y 05).
- La acción del workflow guarda una **copia** al elegir la plantilla. Si cambias la plantilla, hay que volver a elegirla en la acción (o activar "Sync Edits to Template").
- La acción del workflow sí tiene campos de asunto y pre-header; el pre-header del campo y el `div` oculto deben coincidir.

## 3. Calendario → Notifications → Email body → Source code — USAR para 06 a 10
- Envuelve el texto en `<p style="margin:0px">`, sin forzar fuente: conserva Georgia, tamaños y colores del `<td>`.
- **Conserva** los estilos de los `<a>` (los botones se ven bien).
- **Borra** `background-color`, `display`, `padding` y `border-radius` de los `<span>` (por eso se pierde el fondo de la etiqueta del encabezado).
- Conserva el `div` oculto del pre-header.
- No tiene campo de pre-header ni de plantilla útil para esto.

## Regla práctica para escribir el HTML
- Cualquier fondo, padding o radio va en un `<td>` (con `bgcolor` además del `style`), nunca en un `<span>`.
- Botones: `<a>` con estilos inline dentro de un `<td>` que también tenga `bgcolor` y `border-radius`, para que si un editor limpia el `<a>` el fondo siga.
- Nada de `<style>`, `<head>` ni clases.

## Seguimiento de clics
En los correos de calendario GHL reescribe los enlaces a `https://email.mail.orchidpros.com/c/...` (tracking). Es normal.
