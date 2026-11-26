# Merge fields de GHL disponibles

✔ = clave confirmada en el código de los correos actuales. Las demás siguen el patrón estándar de GHL (el selector de GHL muestra solo la etiqueta); si se usan, verificarlas en GHL antes de publicar.

## Contacto
| Campo | Clave |
|---|---|
| Nombre | `{{contact.first_name}}` ✔ |
| Apellido | `{{contact.last_name}}` ✔ |
| Nombre completo | `{{contact.name}}` ✔ |
| Email | `{{contact.email}}` ✔ |
| Teléfono | `{{contact.phone}}` ✔ |
| Vertical (custom) | `{{contact.vertical}}` ✔ |
| Presupuesto mensual (custom) | `{{contact.monthly_budget}}` ✔ |
| Tamaño del equipo (custom) | `{{contact.team_size}}` ✔ |

## Cita (Appointment)
| Etiqueta en GHL | Clave |
|---|---|
| ID | `{{appointment.id}}` |
| Title | `{{appointment.title}}` ✔ |
| Start Date Time | `{{appointment.start_time}}` ✔ |
| Start Date | `{{appointment.only_start_date}}` |
| Start Time | `{{appointment.only_start_time}}` |
| End Date Time | `{{appointment.end_time}}` |
| End Date | `{{appointment.only_end_date}}` |
| End Time | `{{appointment.only_end_time}}` |
| Day of the week | `{{appointment.day_of_week}}` |
| Month | `{{appointment.month}}` |
| Name of Month | `{{appointment.month_name}}` |
| Timezone | `{{appointment.timezone}}` ✔ |
| Cancellation Link | `{{appointment.cancellation_link}}` ✔ |
| Reschedule Link | `{{appointment.reschedule_link}}` ✔ |
| Meeting Location (enlace de Google Meet) | `{{appointment.meeting_location}}` ✔ |
| Notes | `{{appointment.notes}}` |
| Cancellation Reason | `{{appointment.cancellation_reason}}` |
| Add to Google Calendar | `{{appointment.add_to_google_calendar}}` |
| Add to iCal/Outlook | `{{appointment.add_to_ical_outlook}}` |

## Asesor asignado (Appointment → Assigned User)
Opciones en GHL: ID, Full Name, First Name, Last Name, Email, Phone, Phone (raw format), Signature, Twilio Phone.
Claves esperadas: `{{appointment.user.name}}`, `{{appointment.user.first_name}}`, `{{appointment.user.last_name}}`, `{{appointment.user.email}}`, `{{appointment.user.phone}}`. Sin confirmar. Hoy el asesor es siempre Andrea Bolanos, así que los correos lo escriben fijo.

## Usar en correos de workflow vs. de calendario
- Correos 06 a 10 (notificaciones del calendario): todos los campos de cita están disponibles.
- Correos 01 a 05 (workflows): solo campos de contacto; 04 se dispara por cita, pero hoy no usa campos de cita.

## Datos de ejemplo para la vista previa (`index.html`)
| Clave | Valor de ejemplo |
|---|---|
| contact.first_name | Sarah |
| contact.last_name | Miller |
| contact.name | Sarah Miller |
| appointment.start_time | Tuesday, December 2, 2026 10:00 AM |
| appointment.timezone | America/New_York |
| appointment.meeting_location | https://meet.google.com/abc-defg-hij |
| appointment.reschedule_link / cancellation_link | # |
