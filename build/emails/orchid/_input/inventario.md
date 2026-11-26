# Inventario de correos automáticos de GHL Orchid (26 nov 2026)

Sub-cuenta: Orchid, Location `r5demglXbNG9LoCszFIw`.
Dominio de envío: `mail.orchidpros.com` (dedicated). Remitente por defecto de los workflows: `Orchid | Ethical Outsourcing <growth@orchidpros.com>`. Reply-to y reenvío: sin configurar.
Fallidos en los últimos 7 días (19 al 25 nov): 0 de 6 enviados.

No envían correo: "03 - FB Instant Form - Tag", "BF · Etiqueta Entrepreneurs", "BF · Etiqueta Healthcare", "Meta CAPI · Lead calificado". Los de la carpeta "Marketing Workflows" están en Draft.

---

## 01 · Email Descarte
- **Dónde va en GHL:** Automation → Workflows → "01 - Lead nuevo - Respuesta Inmediata" → rama "Busca empleo" → acción "Email Descarte" → Quick compose → Source code.
- **Disparador:** formulario "Orchid · BF Entrepreneurs", "Orchid - Hire a VA", "Orchid · BF Healthcare" o Facebook Lead Form (página "Orchid Pros"), cuando "Hiring or job seeking" indica que busca empleo. Envío inmediato.
- **Remitente:** Orchid Pros <growth@orchidpros.com>
- **Asunto:** `Thanks for your interest in Orchid, {{contact.first_name}}`
- **Pre-header:** vacío
- **Formato actual:** HTML con estilo Orchid. Captura: `capturas/01a`, `01b`.

```
Thanks for your interest in Orchid, {{contact.first_name}}.

The form you filled out is for businesses looking to hire an Orchid professional.

[Bloque destacado] Looking to work with Orchid? We're always glad to meet bilingual professionals in Colombia. Apply through our careers page and our talent team will review your application.

[Enlace] Apply to work with Orchid   (URL no leída: TODO_URL_CAREERS)

Thank you again for thinking of us.

Best regards,
The Orchid Team
orchidpros.com

[Pie] N3XUS, LLC d/b/a ORCHID, P.O Box 463, Rutherford, NJ 07070 · orchidpros.com
```

## 02 · Email Bienvenida
- **Dónde va en GHL:** Workflow "01 - Lead nuevo - Respuesta Inmediata" → rama "None" → … → "Esperar agenda" (10 min) → "Ya agendó?" → rama "No Agendo" → acción "Email Bienvenida".
- **Disparador:** mismos formularios; se envía 10 minutos después si el contacto no tiene el tag "agendo".
- **Remitente:** Andrea Bolanos | Orchid <Growth@orchidpros.com>
- **Asunto:** `We got your request, {{contact.first_name}}`
- **Pre-header:** `Here's how to book your discovery call with Orchid.`
- **Formato actual:** HTML con estilo Orchid. Captura: `02a`, `02b`.

```
We got your request, {{contact.first_name}}.

Thanks for reaching out to Orchid. If you already booked a discovery call, your confirmation is in a separate email and we'll talk then.

[Bloque destacado] Haven't booked yet? Pick a time that works for you. On the call, Andrea will learn about your workload and explain how Orchid matches you with a bilingual professional from Colombia.

[Enlace] Book my free call   (URL no leída: TODO_URL_BOOKING)

Otherwise, I'll reach out within one business day to learn more about your team and the role you're looking to fill.

Warmly,
Andrea Bolanos
Orchid

[Pie] N3XUS, LLC d/b/a ORCHID, P.O Box 463, Rutherford, NJ 07070 · orchidpros.com
```

## 03 · Aviso interno · Nuevo lead (interno)
- **Dónde va en GHL:** Workflow 01 → rama "None" → acción "Aviso interno - Nuevo lead" (Internal notification, tipo Email).
- **Para:** dueño del contacto (Contact owner). CC: marketing@orchidpros.com, hector@orchidpros.com. Envío inmediato.
- **Remitente:** sin nombre, growth@orchidpros.com
- **Asunto:** `Nuevo lead Orchid: {{contact.name}}`
- **Formato actual:** texto simple. Captura: `03`.

```
Entró un nuevo lead del formulario de Facebook (Orchid Pros).
Nombre: {{contact.name}}
Teléfono: {{contact.phone}}
Email: {{contact.email}}
Llámalo lo antes posible. La oportunidad ya está en VENTAS - ORCHID > Nuevo Lead.
```
Nota: dice "formulario de Facebook" pero sale para los 4 disparadores.

## 04 · Email cita cancelada
- **Dónde va en GHL:** Automation → Workflows → "02 - Cita agendada" → rama "Descartado" (tag job-seeker) → "Cancelar cita" → acción "Email cita cancelada".
- **Disparador:** cita agendada en cualquiera de los dos calendarios Discovery Call por alguien con tag job-seeker. Se envía ~1 min después (espera "Esperar tag").
- **Remitente:** Orchid Pros <growth@orchidpros.com>
- **Asunto:** `About your discovery call with Orchid`
- **Pre-header:** `An update on the appointment you booked.`
- **Formato actual:** HTML con estilo Orchid. Captura: `04a`, `04b`.

```
About your call request, {{contact.first_name}}.

Thanks for booking time with us. Our discovery calls are for businesses in the United States looking to hire an Orchid professional, so we've canceled this appointment.

[Bloque destacado] Looking to work with Orchid? If you're a bilingual professional in Colombia, you can apply through our careers page and our talent team will review your application.

[Enlace] Apply to work with Orchid   (URL no leída: TODO_URL_CAREERS)

If you believe this was a mistake, just reply to this email and we'll take a look.

Best regards,
The Orchid Team
orchidpros.com

[Pie] N3XUS, LLC d/b/a ORCHID, P.O Box 463, Rutherford, NJ 07070 · orchidpros.com
```
Nota: al cancelar la cita también se dispara la notificación 08 del calendario (doble correo).

## 05 · Bienvenida Delegate Brief
- **Dónde va en GHL:** Automation → Workflows → "Newsletter · Bienvenida" → acción "Bienvenida Delegate Brief".
- **Disparador:** formulario "Orchid · Newsletter…". Envío inmediato.
- **Remitente:** Orchid Pros <growth@orchidpros.com>
- **Asunto:** `Welcome to The Delegate Brief`
- **Pre-header:** vacío
- **Formato actual:** texto simple. Captura: `05`.

```
Hi {{contact.first_name}},

Thanks for subscribing to The Delegate Brief. Every other week you'll get one task worth delegating, a ready-to-use template and the real numbers behind it. It takes 3 minutes to read.

While you're here: our Black Friday offer runs until December 1st. Get started free with a bilingual professional from Colombia, then 50% off your first month.
Book a free call: https://go.orchidpros.com/business-free-month

Talk soon,
Josué & Andrea, Orchid
```

---

## Notificaciones de calendario (06 a 10)
**Dónde van en GHL:** Settings → Calendars → editar calendario → Advanced settings → Notifications & policies → lápiz de cada notificación → pestaña Email → Contact → Email body → Source code.
**Aplican a dos calendarios con contenido idéntico:** "Orchid - Discovery Call" (ID `739uffEjsGH7PH0Zaovn`) y "Orchid - Discovery Call (Newsletter)" (ID `jgKkDzsDyVnOGqklMxaT`). Hay que pegar cada correo en ambos.
**Remitente en todas:** Orchid | Ethical Outsourcing <growth@orchidpros.com>. Plantilla: ninguna ("start from scratch").
**Asesor:** Andrea Bolanos. **Ubicación:** Google Meet. Llamada de 30 minutos.
**Además:** está activo "Allow Google / Outlook / iCloud calendar to send invitation & update emails to attendees", así que Google envía su propia invitación con las notas de reprogramar/cancelar.
**Follow-Up:** desactivado.

## 06 · Reserva sin confirmar (Appointment booked · Unconfirmed)
- **Cuándo:** al crear una cita con estado Unconfirmed.
- **Asunto:** `Appointment Request Received for {{appointment.start_time}} ({{appointment.timezone}})`
- **Formato actual:** texto por defecto de GHL. Captura: `06`.
```
Hi {{contact.name}},

We've received your appointment request and will confirm it shortly.

Here are the details of your requested appointment:

Appointment Title: {{appointment.title}}

Date and Time: {{appointment.start_time}} ({{appointment.timezone}})

Meeting Link / Location: {{appointment.meeting_location}}
```
Copia interna (Additional emails → Growth@orchidpros.com), asunto `New Appointment Requested by {{contact.name}} on {{appointment.start_time}} ({{appointment.timezone}})`, texto por defecto de GHL. Fuera del alcance del rediseño.

## 07 · Reserva confirmada (Appointment booked · Confirmed)
- **Cuándo:** al crear la cita confirmada o pasarla a Confirmed.
- **Asunto:** `You're booked: Orchid discovery call on {{appointment.start_time}}`
- **Formato actual:** HTML con estilo Orchid (referencia de `design-tokens.md`). Captura: `07`.
```
You're booked, {{contact.first_name}}.
Your discovery call with Orchid is confirmed. Here are the details.

[Bloque] When: {{appointment.start_time}} ({{appointment.timezone}})
         Where: {{appointment.meeting_location}}

On the call, Andrea will learn about your workload and the tasks you want to delegate, and explain how Orchid matches you with a bilingual professional from Colombia.

[Botón → {{appointment.reschedule_link}}] Reschedule my call
Can't make it? [Enlace → {{appointment.cancellation_link}}] Cancel your call.

Talk soon,
Andrea Bolanos
Orchid

[Pie] N3XUS, LLC d/b/a ORCHID, 120 Chubb Ave, Lyndhurst, NJ 07071 · orchidpros.com
```
Copia interna (Additional emails → hector@orchidpros.com, Growth@orchidpros.com), en español, texto simple; fuera del alcance del rediseño:
```
Asunto: Nueva cita: {{contact.first_name}} {{contact.last_name}} - {{appointment.start_time}}

Nueva llamada de descubrimiento AGENDADA.
Lead: {{contact.first_name}} {{contact.last_name}}
Correo: {{contact.email}}
Teléfono: {{contact.phone}}
Cuándo: {{appointment.start_time}} ({{appointment.timezone}})
Vertical: {{contact.vertical}}
Presupuesto: {{contact.monthly_budget}}
Equipo: {{contact.team_size}}
```

## 08 · Cancelación
- **Cuándo:** al cancelar, marcar no-show o marcar inválida.
- **Asunto:** `Appointment Cancelled: {{appointment.start_time}} ({{appointment.timezone}})`
- **Formato actual:** texto por defecto de GHL. Captura: `08`.
```
Hi {{contact.name}},

We regret to inform you that your upcoming appointment, originally scheduled for {{appointment.start_time}} ({{appointment.timezone}}), has been cancelled.

Here are the details for your reference:

Appointment Title: {{appointment.title}}

Date and Time: {{appointment.start_time}} ({{appointment.timezone}})

Meeting Link / Location: {{appointment.meeting_location}}
```
Tiene copia interna activa (Additional emails), fuera del alcance.

## 09 · Reprogramación
- **Cuándo:** al reprogramar (solo si la cita está Unconfirmed o Confirmed).
- **Asunto:** `New time: your Orchid call on {{appointment.start_time}}`
- **Formato actual:** HTML con estilo Orchid. Captura: `09a`, `09b`.
```
Your call has a new time, {{contact.first_name}}.
Your discovery call with Orchid was rescheduled. Here are the updated details.

[Bloque] When: {{appointment.start_time}} ({{appointment.timezone}})
         Where: {{appointment.meeting_location}}

Nothing else changes: Andrea will learn about your workload and the tasks you want to delegate, and explain how Orchid matches you with a bilingual professional from Colombia.

[Botón] Change the time again
Can't make it? [Enlace] Cancel your call.

Talk soon,
Andrea Bolanos
Orchid

[Pie] N3XUS, LLC d/b/a ORCHID, P.O Box 463, Rutherford, NJ 07070 · orchidpros.com
```

## 10 · Recordatorio
- **Cuándo:** 24 horas y 1 hora antes (el mismo correo para ambos).
- **Asunto:** `Reminder: your Orchid call on {{appointment.start_time}}`
- **Formato actual:** HTML con estilo Orchid. Captura: `10a`, `10b`.
```
Your call with Orchid is coming up, {{contact.first_name}}.
Here's a quick reminder of your discovery call details.

[Bloque] When: {{appointment.start_time}} ({{appointment.timezone}})
         Where: {{appointment.meeting_location}}

It's a relaxed 30-minute conversation. It helps to have in mind the tasks that take most of your week; Andrea will take it from there.

[Botón] Reschedule my call
Can't make it? [Enlace] Cancel your call.

Talk soon,
Andrea Bolanos
Orchid

[Pie] N3XUS, LLC d/b/a ORCHID, P.O Box 463, Rutherford, NJ 07070 · orchidpros.com
```
