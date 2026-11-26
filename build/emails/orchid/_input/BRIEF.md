# Brief para Claude Code: rediseño de correos automáticos de Orchid (GoHighLevel)

## Objetivo
Rediseñar los 10 correos automáticos de la sub-cuenta Orchid en GoHighLevel (GHL) con un solo sistema visual de Orchid, coherente y listo para pegar en GHL.

Claude Code no tiene acceso a GHL. Todo lo necesario está en esta carpeta:

| Archivo | Contenido |
|---|---|
| `BRIEF.md` | Este documento: tarea, reglas y entregables |
| `inventario.md` | Los 10 correos: ubicación, disparador, remitente, asunto, pre-header y cuerpo actual completo |
| `design-tokens.md` | Colores, tipografías, medidas y estructura HTML que ya usan los correos con estilo Orchid |
| `merge-fields.md` | Campos dinámicos válidos en GHL (contacto, cita, asesor) |
| `capturas/` | Capturas de cada correo tal como se ve hoy en el editor de GHL (ojo: el editor lo muestra en modo oscuro; el HTML real es claro) |

## Qué entregar
Crear una carpeta `emails/` con:

1. **Un archivo HTML por correo**, nombrado como en el inventario:
   - `01-email-descarte.html`
   - `02-email-bienvenida.html`
   - `03-aviso-interno-nuevo-lead.html` (interno; puede quedar en texto simple con formato mínimo)
   - `04-email-cita-cancelada.html`
   - `05-bienvenida-delegate-brief.html`
   - `06-cal-reserva-sin-confirmar.html`
   - `07-cal-reserva-confirmada.html`
   - `08-cal-cancelacion.html`
   - `09-cal-reprogramacion.html`
   - `10-cal-recordatorio.html`
2. **`_layout.html`**: plantilla base (cabecera, cuerpo, firma, pie) que comparten todos.
3. **`index.html`**: página de vista previa con todos los correos en iframes, con los merge fields reemplazados por datos de ejemplo, para revisar en el navegador.
4. **`ghl-cheatsheet.md`**: por cada correo, dónde pegarlo en GHL (ver "Dónde va en GHL" en el inventario), asunto, pre-header y remitente a configurar.

## Reglas técnicas (GHL)
- El HTML se pega en GHL en el editor "Quick compose" → botón **Source code** (`</>`), o en el cuerpo de la notificación del calendario → Source code. Debe ser **un fragmento** (empezar en `<table>`), sin `<html>`, `<head>`, `<style>` ni `<script>`: GHL los elimina.
- **Todo con estilos inline** y maquetación con **tablas** (`role="presentation"`). Nada de flexbox, grid, clases ni CSS externo.
- Ancho máximo 600px, centrado, que funcione en móvil sin media queries (ancho 100% + max-width).
- Fuentes web seguras: titulares en Georgia, cuerpo en Arial (como hoy).
- Botones como `<a>` con fondo y padding inline (bulletproof simple); sin imágenes de botón.
- Imágenes solo con URL absoluta pública. Logo actual: `https://orchidpros.com/wp-content/uploads/2026/01/cropped-cropped-LOGO_WHITE-scaled-1.png` (blanco, para fondo oscuro).
- Merge fields exactamente con la sintaxis de `merge-fields.md`, p. ej. `{{contact.first_name}}`. No inventar campos.
- Probar contraste en modo claro y que no se rompa en modo oscuro de Gmail/Apple Mail (evitar texto oscuro sobre fondo transparente).
- Incluir texto alternativo (`alt`) en el logo.

## Reglas de copy
- Correos al contacto en **inglés** (EE. UU.); el aviso interno en **español**.
- Conservar el sentido y la información de cada correo actual; se permite mejorar redacción y jerarquía.
- **No usar guiones largos (—)**; usar punto y coma, comas o frases separadas.
- Tono: cálido, profesional, directo. Firma personal de Andrea Bolanos en los correos de cita y bienvenida; "The Orchid Team" en los de descarte.
- Usar `{{contact.first_name}}` (no `{{contact.name}}`) en saludos al contacto.

## Decisiones ya conocidas y problemas a corregir
1. **Pie legal inconsistente**: hoy hay dos direcciones ("120 Chubb Ave, Lyndhurst, NJ 07071" y "P.O Box 463, Rutherford, NJ 07070"). Usar una sola variable en `_layout.html` y dejar marcado `TODO: confirmar dirección legal` hasta que Manuel confirme.
2. **06 Reserva sin confirmar** y **08 Cancelación** usan el texto por defecto de GHL: rediseñarlos con el mismo sistema que 07, 09 y 10.
3. **05 Bienvenida Delegate Brief** es texto plano y trae la oferta Black Friday que vence el 1 de diciembre de 2026: hacer el diseño con un bloque de oferta **opcional y fácil de quitar** (comentario HTML `<!-- OFERTA: borrar después del 1 dic -->`), y una versión sin oferta.
4. **Remitentes mezclados** ("Orchid Pros", "Andrea Bolanos | Orchid", "Orchid | Ethical Outsourcing"): proponer uno en `ghl-cheatsheet.md` (sugerido: "Andrea Bolanos | Orchid" para cita/bienvenida, "Orchid" para el resto), pero no es parte del HTML.
5. **Desajuste de dominio**: el dominio de envío es `mail.orchidpros.com` y el remitente `growth@orchidpros.com`; GHL lo marca como "Sender domain mismatch". Solo documentarlo en el cheatsheet como pendiente; no se resuelve en el HTML.
6. **Doble correo al descartar**: un job-seeker que agenda recibe 04 (workflow) y 08 (calendario). Documentarlo en el cheatsheet como pendiente de lógica.
7. Los dos calendarios ("Orchid - Discovery Call" y "Orchid - Discovery Call (Newsletter)") tienen las mismas notificaciones: el cheatsheet debe indicar pegar cada una en **ambos**.
8. Enlaces que no se pudieron leer en los correos actuales: "Apply to work with Orchid" (01 y 04) y "Book my free call" (02). Dejar `href="TODO_URL_CAREERS"` y `href="TODO_URL_BOOKING"` y listarlos en el cheatsheet. El de Delegate Brief sí se conoce: `https://go.orchidpros.com/business-free-month`.

## Criterio de terminado
- Los 10 HTML se ven bien en `index.html` a 600px y a 375px.
- Ningún HTML contiene `<style>`, `<head>`, clases ni `—`.
- Todos los merge fields usados están en `merge-fields.md`.
- `ghl-cheatsheet.md` lista asunto, pre-header, remitente, ubicación en GHL y TODOs pendientes por correo.
