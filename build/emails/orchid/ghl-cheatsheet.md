# Correos automáticos de Orchid · guía para pegar en GHL

Los archivos HTML están en `build/emails/orchid/` y se generan con `python3 scripts/build_emails.py`. Vista previa: `index.html`.
Cómo pegar: abrir el correo en GHL → editor → botón **Source code** (`</>`) → borrar todo → pegar el archivo completo → guardar. Cada archivo es un fragmento que empieza en `<table>`.

## Remitente propuesto
- Cita y bienvenida (02, 06, 07, 08, 09, 10): **Andrea Bolanos | Orchid** <growth@orchidpros.com>
- Descarte y newsletter (01, 04, 05): **Orchid** <growth@orchidpros.com>
- Interno (03): sin cambios.

## Por correo

| # | Archivo | Dónde va en GHL | Asunto | Pre-header |
|---|---|---|---|---|
| 01 | `01-email-descarte.html` | Workflow "01 - Lead nuevo - Respuesta Inmediata" → rama "Busca empleo" → "Email Descarte" | Thanks for your interest in Orchid, {{contact.first_name}} | Our careers page is the right place for you. |
| 02 | `02-email-bienvenida.html` | Workflow 01 → rama "None" → "Ya agendó?" → "No Agendo" → "Email Bienvenida" | We got your request, {{contact.first_name}} | Here's how to book your discovery call with Orchid. |
| 03 | `03-aviso-interno-nuevo-lead.html` | Workflow 01 → rama "None" → "Aviso interno - Nuevo lead" | Nuevo lead Orchid: {{contact.name}} | (no aplica) |
| 04 | `04-email-cita-cancelada.html` | Workflow "02 - Cita agendada" → rama "Descartado" → "Email cita cancelada" | About your discovery call with Orchid | An update on the appointment you booked. |
| 05 | `05-bienvenida-delegate-brief.html` (hasta el 1 dic) / `05-bienvenida-delegate-brief-sin-oferta.html` (desde el 2 dic) | Workflow "Newsletter · Bienvenida" → "Bienvenida Delegate Brief" | Welcome to The Delegate Brief | One task worth delegating, every other week. |
| 06 | `06-cal-reserva-sin-confirmar.html` | Calendario → Notifications → Appointment booked (Unconfirmed) → Email → Contact | Request received: your Orchid call on {{appointment.start_time}} | We'll confirm your discovery call shortly. |
| 07 | `07-cal-reserva-confirmada.html` | Calendario → Notifications → Appointment booked (Confirmed) → Email → Contact | You're booked: Orchid discovery call on {{appointment.start_time}} | Your discovery call details are inside. |
| 08 | `08-cal-cancelacion.html` | Calendario → Notifications → Cancellation → Email → Contact | Your Orchid call was canceled | Book a new time whenever it works for you. |
| 09 | `09-cal-reprogramacion.html` | Calendario → Notifications → Reschedule → Email → Contact | New time: your Orchid call on {{appointment.start_time}} | Here are the updated details of your call. |
| 10 | `10-cal-recordatorio.html` | Calendario → Notifications → Reminder (24 h y 1 h) → Email → Contact | Reminder: your Orchid call on {{appointment.start_time}} | A quick reminder of your discovery call details. |

Los correos 06 a 10 se pegan en **los dos calendarios**: "Orchid - Discovery Call" (739uffEjsGH7PH0Zaovn) y "Orchid - Discovery Call (Newsletter)" (jgKkDzsDyVnOGqkIMxaT). Las copias internas (Additional emails) no cambian.

## Enlaces usados
- Reservar llamada (02, 08): `https://api.leadconnectorhq.com/widget/booking/739uffEjsGH7PH0Zaovn`
- Black Friday (05 con oferta): `https://go.orchidpros.com/business-free-month`

## Pendientes
1. **TODO_URL_CAREERS** en 01 y 04: falta la URL de la página de empleo de Orchid. Reemplazarla antes de publicar esos dos.
2. **Dirección legal:** el pie usa "P.O. Box 463, Rutherford, NJ 07070"; el 07 actual tenía "120 Chubb Ave, Lyndhurst, NJ 07071". Confirmar cuál es la correcta.
3. **Dominio:** el dominio de envío es `mail.orchidpros.com` y el remitente `growth@orchidpros.com` ("Sender domain mismatch" en GHL). Usar un remitente del mismo dominio o autenticar `orchidpros.com`.
4. **Doble correo al descartar:** un buscador de empleo que agenda recibe 04 (workflow) y 08 (calendario). Opción: en el workflow, quitar 04 y dejar que el 08 avise, o desactivar la notificación 08 para citas canceladas por el workflow.
5. **Campos de la cita:** `{{appointment.reschedule_link}}`, `{{appointment.cancellation_link}}`, `{{appointment.meeting_location}}`, `{{appointment.start_time}}`, `{{appointment.timezone}}` están confirmados. El asesor se escribe fijo ("Andrea Bolanos").
6. **05:** el 2 de diciembre cambiar al archivo sin oferta.
