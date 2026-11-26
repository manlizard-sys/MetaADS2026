# Merge fields confirmados en correos publicados (26 nov 2026)

## Contacto
- `{{contact.first_name}}`, `{{contact.last_name}}`, `{{contact.name}}`
- `{{contact.email}}`, `{{contact.phone}}`
- Personalizados: `{{contact.vertical}}`, `{{contact.monthly_budget}}`, `{{contact.team_size}}`

## Cita (solo en notificaciones de calendario 06 a 10)
Confirmados en la prueba con cita de ejemplo:
- `{{appointment.start_time}}` → "Thursday, November 26, 2026 11:59 AM"
- `{{appointment.timezone}}` → "EST"
- `{{appointment.meeting_location}}` → enlace de Google Meet
- `{{appointment.reschedule_link}}`, `{{appointment.cancellation_link}}`
- `{{appointment.title}}`

Disponibles en el selector de GHL pero sin probar: `only_start_date`, `only_start_time`, `end_time`, `day_of_week`, `month_name`, `notes`, `cancellation_reason`, `add_to_google_calendar`, `add_to_ical_outlook`, Assigned User (nombre, email, teléfono, firma).

## Notas de calendario (Meeting invite notes, invitación de Google)
Usan otra sintaxis: `{{reschedule_link}}`, `{{cancellation_link}}`. No es parte de este trabajo.
