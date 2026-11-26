# Correos automáticos de Orchid · guía de GHL (v2, 26 nov 2026)

HTML en `build/emails/orchid/`, generados con `python3 scripts/build_emails.py`. Vista previa: `index.html`.
Estado publicado: todos los correos están en GHL desde el 26 nov (11:30 a. m. Bogotá). Remitente (correo): `growth@orchidpros.com`.
Dirección legal en el pie: siempre "P.O. Box 463, Rutherford, NJ 07070".

## Cómo publicar un cambio (dos métodos)

### A. Workflows 01, 02, 04 y 05: plantillas Code editor
1. Marketing → Emails → Templates → abrir la plantilla "Orchid · NN …" → Code editor → borrar todo → pegar el archivo completo → guardar.
2. Volver a la acción del workflow → "Select existing template" → elegir otra vez esa plantilla. La acción guarda una copia y NO se actualiza sola ("Sync Edits to Template" está desactivado).
3. Revisar asunto y pre-header de la acción (el pre-header debe coincidir con el `div` oculto del HTML) → guardar y publicar el workflow.
No usar "Quick compose" para estos correos: cambia la fuente a Verdana y borra el estilo de los botones.

### B. Calendarios 06 a 10: notificaciones
Settings → Calendars → editar calendario → Advanced settings → Notifications & policies → lápiz de la notificación → pestaña Email → Contact → Email body → Source code → borrar todo → pegar → guardar.
Pegar en LOS DOS calendarios: "Orchid - Discovery Call" (`739uffEjsGH7PH0Zaovn`) y "Orchid - Discovery Call (Newsletter)" (`jgKkDzsDyVnOGqkIMxaT`, con I mayúscula antes de MxaT; comprobado por API).
Este editor no tiene campo de pre-header: el pre-header va solo en el `div` oculto del HTML.

### C. 03 interno
Workflow 01 → acción "Aviso interno - Nuevo lead" → Source code → pegar. El editor le pone Verdana; es aceptable.

## Qué va en cada lugar

| # | Archivo | Dónde | Plantilla / notificación | Nombre remitente | Asunto | Pre-header |
|---|---|---|---|---|---|---|
| 01 | `01-email-descarte.html` | Workflow "01 - Lead nuevo - Respuesta Inmediata" → "Email Descarte" | Orchid · 01 Email Descarte | Orchid | Thanks for your interest in Orchid, {{contact.first_name}} | Our careers page is the right place for you. |
| 02 | `02-email-bienvenida.html` | Workflow 01 → "Email Bienvenida" | Orchid · 02 Email Bienvenida | Andrea Bolanos \| Orchid | We got your request, {{contact.first_name}} | Here's how to book your discovery call with Orchid. |
| 03 | `03-aviso-interno-nuevo-lead.html` | Workflow 01 → "Aviso interno - Nuevo lead" | Source code (método C) | (sin cambio) | Nuevo lead Orchid: {{contact.name}} | (no aplica) |
| 04 | `04-email-cita-cancelada.html` | Workflow "02 - Cita agendada" → "Email cita cancelada" | Orchid · 04 Email cita cancelada | Orchid | About your discovery call with Orchid | An update on the appointment you booked. |
| 05 | `05-bienvenida-delegate-brief.html` | Workflow "Newsletter · Bienvenida" → "Bienvenida Delegate Brief" | Orchid · 05 Delegate Brief (con oferta) | Orchid | Welcome to The Delegate Brief | One task worth delegating, every other week. |
| 05b | `05-bienvenida-delegate-brief-sin-oferta.html` | Mismo lugar, desde el 2 dic | Orchid · 05 Delegate Brief (sin oferta, desde 2 dic) | Orchid | Welcome to The Delegate Brief | One task worth delegating, every other week. |
| 06 | `06-cal-reserva-sin-confirmar.html` | Ambos calendarios | Appointment booked (Unconfirmed) | Andrea Bolanos \| Orchid | Request received: your Orchid call on {{appointment.start_time}} | (en el HTML) |
| 07 | `07-cal-reserva-confirmada.html` | Ambos calendarios | Appointment booked (Confirmed) | Andrea Bolanos \| Orchid | You're booked: Orchid discovery call on {{appointment.start_time}} | (en el HTML) |
| 08 | `08-cal-cancelacion.html` | Calendario "Orchid - Discovery Call" | Cancellation | Andrea Bolanos \| Orchid | Your Orchid call was canceled | (en el HTML) |
| 08n | `08-cal-cancelacion-newsletter.html` | Calendario "Orchid - Discovery Call (Newsletter)" | Cancellation | Andrea Bolanos \| Orchid | Your Orchid call was canceled | (en el HTML) |
| 09 | `09-cal-reprogramacion.html` | Ambos calendarios | Reschedule | Andrea Bolanos \| Orchid | New time: your Orchid call on {{appointment.start_time}} | (en el HTML) |
| 10 | `10-cal-recordatorio.html` | Ambos calendarios | Reminder (24 h y 1 h) | Andrea Bolanos \| Orchid | Reminder: your Orchid call on {{appointment.start_time}} | (en el HTML) |

Copias internas (Additional emails) y Follow-Up: sin cambios.

## Enlaces
- Empleo (01, 04): `https://orchidpros.com/work-with-us/`
- Reservar llamada (02, 08): `https://api.leadconnectorhq.com/widget/booking/739uffEjsGH7PH0Zaovn`
- Reservar llamada (08n): `https://api.leadconnectorhq.com/widget/booking/jgKkDzsDyVnOGqkIMxaT`
- Black Friday (05 con oferta): `https://go.orchidpros.com/business-free-month`

## Cambios de la v2 que hay que publicar
1. Etiqueta amarilla del encabezado rehecha como tabla con `bgcolor`: así se ve también en 06 a 10 (antes el editor de calendario le quitaba el fondo). Republicar 06 a 10 en ambos calendarios.
2. Botones envueltos en una celda con `bgcolor`: si un editor limpia el enlace, el fondo amarillo se mantiene.
3. 08 en el calendario Newsletter: pegar `08-cal-cancelacion-newsletter.html`, que manda a reservar en ese mismo calendario.
4. Las plantillas 01, 02, 04 y 05 se pueden actualizar también para que queden iguales al repo; cambian solo la etiqueta y los botones (01 y 04 ya tenían la URL de empleo).

## Pendientes
- **2 de diciembre de 2026:** en la acción "Bienvenida Delegate Brief", elegir la plantilla "Orchid · 05 Delegate Brief (sin oferta, desde 2 dic)".
- **Dominio:** remitente `growth@orchidpros.com` con dominio de envío `mail.orchidpros.com` ("Sender domain mismatch"). Se resuelve en la configuración de GHL, no en el HTML.

## Decisiones de Manuel (no tocar)
- Doble correo al descartar (04 + 08): se dejan los dos.
- Dirección legal: siempre P.O. Box 463, Rutherford, NJ 07070.
