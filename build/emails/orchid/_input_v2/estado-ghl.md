# Estado publicado en GHL (26 nov 2026, 11:30 a. m. Bogotá)

Remitente (correo) en todos: `growth@orchidpros.com`. Dominio de envío: `mail.orchidpros.com`.

## Workflows (contenido en plantillas Code editor)
| # | Workflow → acción | Plantilla de GHL usada | Nombre remitente | Asunto | Pre-header |
|---|---|---|---|---|---|
| 01 | "01 - Lead nuevo - Respuesta Inmediata" → "Email Descarte" | Orchid · 01 Email Descarte | Orchid | Thanks for your interest in Orchid, {{contact.first_name}} | Our careers page is the right place for you. |
| 02 | "01 - Lead nuevo - Respuesta Inmediata" → "Email Bienvenida" | Orchid · 02 Email Bienvenida | Andrea Bolanos \| Orchid | We got your request, {{contact.first_name}} | Here's how to book your discovery call with Orchid. |
| 04 | "02 - Cita agendada" → "Email cita cancelada" | Orchid · 04 Email cita cancelada | Orchid | About your discovery call with Orchid | An update on the appointment you booked. |
| 05 | "Newsletter · Bienvenida" → "Bienvenida Delegate Brief" | Orchid · 05 Delegate Brief (con oferta) | Orchid | Welcome to The Delegate Brief | One task worth delegating, every other week. |

Plantilla extra creada, aún sin usar: **Orchid · 05 Delegate Brief (sin oferta, desde 2 dic)**.
La URL de empleo ya va pegada en las plantillas 01 y 04: `https://orchidpros.com/work-with-us/`.
En las cuatro acciones "Sync Edits to Template" está **desactivado**.

## Workflow, interno
| # | Acción | Formato | Asunto | Para |
|---|---|---|---|---|
| 03 | "01 - Lead nuevo" → "Aviso interno - Nuevo lead" | Quick compose (Source code) | Nuevo lead Orchid: {{contact.name}} | Dueño del contacto; CC marketing@ y hector@orchidpros.com (sin cambios) |

## Notificaciones de calendario (pegadas en los dos calendarios)
Calendarios: "Orchid - Discovery Call" (`739uffEjsGH7PH0Zaovn`) y "Orchid - Discovery Call (Newsletter)" (`jgKkDzsDyVnOGqklMxaT`).
Nombre remitente en todas: **Andrea Bolanos | Orchid**. El editor de calendario **no tiene campo de pre-header**: el pre-header va solo en el `div` oculto del HTML.

| # | Notificación | Cuándo | Asunto |
|---|---|---|---|
| 06 | Appointment booked (Unconfirmed) | Al crear la cita sin confirmar | Request received: your Orchid call on {{appointment.start_time}} |
| 07 | Appointment booked (Confirmed) | Al crear o confirmar la cita | You're booked: Orchid discovery call on {{appointment.start_time}} |
| 08 | Cancellation | Al cancelar, no-show o inválida | Your Orchid call was canceled |
| 09 | Reschedule | Al reprogramar | New time: your Orchid call on {{appointment.start_time}} |
| 10 | Reminder | 24 h y 1 h antes (mismo correo) | Reminder: your Orchid call on {{appointment.start_time}} |

Copias internas (Additional emails) de 06 a 10: sin cambios.
Follow-Up: desactivado.

## Pruebas enviadas a hmlizarralde+57@gmail.com
02, 06, 07, 08, 09 y 10 llegaron bien. En las pruebas de calendario GHL usa una cita de ejemplo: fecha, zona horaria, enlace de Meet, reprogramar y cancelar se resuelven. `{{contact.first_name}}` sale vacío en las pruebas porque no hay contacto real.

## Diferencias conocidas entre el repo y lo publicado
- La etiqueta amarilla del encabezado se ve sin fondo en 06 a 10 (el editor de calendario la borra). En las plantillas Code editor (01, 02, 04, 05) sí se ve.
- 01 y 04 publicados ya tienen la URL de empleo; en el repo siguen con `TODO_URL_CAREERS`.
- 08 usa el enlace del calendario principal en ambos calendarios.
