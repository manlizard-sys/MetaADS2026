# Reporte: publicación de correos Orchid v2 en GHL

Fecha: 2026-11-26, entre las 11:30 y las 12:30 (hora de Bogotá).
Ejecutado por: Claude (en Chrome, sesión GHL de Héctor), a pedido de Manuel.

## Contexto

- Sub-cuenta GHL: Orchid. Location `r5demglXbNG9LoCszFIw`.
- Fuente de verdad: repo `manlizard-sys/metaads2026`, rama `claude/admiring-franklin-wrfknt`, commit `3b2bc66` ("Emails v2: table-based header tag and buttons (bgcolor)...").
- Carpeta: `build/emails/orchid/`. Guía: `ghl-cheatsheet.md` (secciones "Cómo publicar un cambio" y "Cambios de la v2").
- Método de copia: abrí cada archivo en `raw.githubusercontent.com/.../build/emails/orchid/<archivo>`, verifiqué la longitud (`document.body.innerText.length`) contra la v2 y copié todo el contenido.
- Longitudes verificadas:

| Archivo | Longitud |
|---|---|
| 01 | 4470 |
| 02 | 4609 |
| 04 | 4574 |
| 05 con oferta | 4550 |
| 05 sin oferta | 3282 |
| 06 | 5263 |
| 07 | 6864 |
| 08 | 4485 |
| 08-newsletter | 4485 |
| 09 | 5547 |
| 10 | 5506 |

  La 05 con oferta midió 4550; mi nota anterior decía 4551. Parece un salto de línea final y no lo considero un cambio de contenido.

## Qué no se tocó

- Disparadores y esperas.
- Ramas y destinatarios.
- Copias internas (Additional emails).
- Follow-Up.
- Remitentes.
- "Sync Edits to Template" (sigue apagado).

Los asuntos tampoco cambiaron de texto. En los workflows hubo que reescribirlos (ver punto 2).

No se enviaron correos a contactos reales.

## 1. Notificaciones de calendario (método B)

Calendarios:
- Principal: "Orchid - Discovery Call", ID `739uffEjsGH7PH0Zaovn`.
- Newsletter: "Orchid - Discovery Call (Newsletter)", ID `jgKkDzsDyVnOGqkIMxaT`.

El ID del Newsletter lleva una "I" mayúscula. El BRIEF de la v2 decía "l" minúscula, y eso estaba mal.

Ruta: Settings → Calendars → editar calendario → Notifications.

Pasos para cada notificación:
1. Lápiz de la notificación.
2. Expandir Contact.
3. En Email body, abrir "Source code".
4. Seleccionar todo, borrar y pegar.
5. "Save changes" del diálogo.
6. "Save changes" del modal y confirmar el aviso "Settings saved!".
7. Close.

| Notificación GHL | Archivo (principal) | Archivo (Newsletter) | Estado |
|---|---|---|---|
| Appointment booked (Unconfirmed) | 06-cal-reserva-sin-confirmar.html | 06-cal-reserva-sin-confirmar.html | Guardado en ambos |
| Confirmed | 07-cal-reserva-confirmada.html | 07-cal-reserva-confirmada.html | Guardado en ambos |
| Cancellation | 08-cal-cancelacion.html | 08-cal-cancelacion-newsletter.html | Guardado en ambos |
| Reschedule | 09-cal-reprogramacion.html | 09-cal-reprogramacion.html | Guardado en ambos |
| Reminder (24 h y 1 h antes) | 10-cal-recordatorio.html | 10-cal-recordatorio.html | Guardado en ambos |

- Remitente sin cambios en todas: "Andrea Bolanos | Orchid" <growth@orchidpros.com>.
- Asuntos que vi:
  - 09: "New time: your Orchid call on {{appointment.start_time}}"
  - 10: "Reminder: your Orchid call on {{appointment.start_time}}"
- La etiqueta amarilla del encabezado (pill v2 con `bgcolor` en tabla) se ve con fondo amarillo en la vista previa del editor en las 5 notificaciones.
- Incidente: un modal "Confirmed" del calendario Newsletter se quedó cargando. Lo cerré sin guardar y lo reabrí, sin efectos.

## 2. Plantillas y workflows (método A)

### 2a. Plantillas

Ruta: Marketing → Emails → Templates. Las 5 son de tipo Code editor.

Pasos: abrir la plantilla, seleccionar todo en el panel Code, borrar, pegar y guardar (icono arriba a la derecha) hasta ver el aviso "Saved".

| Plantilla | Archivo | Guardada |
|---|---|---|
| Orchid · 01 Email Descarte | 01-email-descarte.html | Sí |
| Orchid · 02 Email Bienvenida | 02-email-bienvenida.html | Sí |
| Orchid · 04 Email cita cancelada | 04-email-cita-cancelada.html | Sí |
| Orchid · 05 Delegate Brief (con oferta) | 05-bienvenida-delegate-brief.html | Sí |
| Orchid · 05 Delegate Brief (sin oferta, desde 2 dic) | 05-bienvenida-delegate-brief-sin-oferta.html | Sí |

Nota: la lista se reordena por "Last updated" después de cada guardado. Un clic por posición abrió primero la 05 sin oferta en vez de la 01. La actualicé con su archivo correcto, así que no hubo daño. Hay que verificar siempre el título del editor antes de pegar.

### 2b. Volver a elegir la plantilla en las acciones de los workflows

Comportamiento de GHL observado:
1. En la acción, el menú (⋮) de la vista previa del correo solo ofrece "Edit design" y "Remove".
2. "Remove" muestra "Select existing template", pero **también vacía Subject y Pre-Header**.
3. Después de elegir la plantilla, "Save action" muestra el aviso "Changing template? ... discard all your previous edits". Hay que confirmarlo.
4. Por último se guarda el workflow.

Por eso, en cada acción anoté antes el asunto y el pre-header, los volví a escribir con el mismo texto y verifiqué que persistieran.

| Workflow | Acción | Plantilla enlazada | From | Subject | Pre-Header |
|---|---|---|---|---|---|
| 01 - Lead nuevo - Respuesta Inmediata (`6ebffa31-74ae-4b27-b135-af6c9a6158ef`) | Email Descarte (rama "Busca empleo") | Orchid · 01 Email Descarte | Orchid / growth@orchidpros.com | Thanks for your interest in Orchid, {{contact.first_name}} | Our careers page is the right place for you. |
| 01 (mismo) | Email Bienvenida (rama "No Agendo") | Orchid · 02 Email Bienvenida | Andrea Bolanos \| Orchid / growth@orchidpros.com | We got your request, {{contact.first_name}} | Here's how to book your discovery call with Orchid. |
| 02 - Cita agendada (ID no anotado) | Email cita cancelada (rama "Descartado") | Orchid · 04 Email cita cancelada | Orchid / growth@orchidpros.com | About your discovery call with Orchid | An update on the appointment you booked. |
| Newsletter · Bienvenida (`b942ef3a-f7f9-4c61-9171-00be90353051`) | Bienvenida Delegate Brief | Orchid · 05 Delegate Brief (con oferta) | Orchid / growth@orchidpros.com | Welcome to The Delegate Brief | One task worth delegating, every other week. |

- Los tres workflows quedaron guardados ("Workflow has been saved") con el interruptor Publish encendido. Ya estaban publicados y siguen publicados.
- "Newsletter · Bienvenida" está en la raíz del listado de workflows, no dentro de la carpeta "Marketing Workflows". Se encuentra con el buscador.

## 3. Pruebas (Send test a hmlizarralde+57@gmail.com)

| Correo | Desde dónde | Hora | Resultado en Gmail |
|---|---|---|---|
| 07 Reserva confirmada | Calendario principal, notificación Confirmed | 12:10 PM | Etiqueta "Your call is booked" con fondo amarillo y botón "Reschedule my call" amarillo |
| 02 Bienvenida | WF 01, acción Email Bienvenida, campo "Test Emails" | 12:25 PM | Etiqueta "Request received" con fondo amarillo y botón "Book my free call" amarillo |

- Se revisó en Gmail `mail.google.com/mail/u/1/` (hmlizarralde@gmail.com). El conector de Gmail es otra cuenta (manlizard@gmail.com) y no sirve para esto.
- La prueba 02 v2 llegó en el mismo hilo que la prueba v1 de las 11:26. Gmail la colapsa como contenido repetido ("•••").
- Capturas incluidas: `07_v2_header.jpg`, `07_v2_boton.jpg` y `02_v2.jpg`.

## 4. Diferencias y observaciones

1. **Contraste en modo oscuro de Gmail:** el texto de la etiqueta y de los botones se ve claro sobre el amarillo. Parece que Gmail invierte los colores de texto oscuro. No se revisó en modo claro ni en otros clientes. Un arreglo posible es forzar el color del texto con `color` en el `<a>`/`<td>` y agregar `<font color>`, o aceptar el comportamiento.
2. **Nombre vacío en las pruebas:** sale "You're booked, ." y "We got your request, ." porque los envíos de prueba no tienen contacto. Es lo esperado.
3. **Asuntos y pre-headers de las acciones:** se reescribieron a mano (ver 2b). Si se vuelve a cambiar la plantilla, hay que repetir el proceso.
4. **ID del calendario Newsletter:** `jgKkDzsDyVnOGqkIMxaT`, con "I" mayúscula. Hay que corregir el BRIEF de la v2.
5. **Prueba del calendario Newsletter:** no se envió ninguna prueba desde ahí. Solo se verificó la vista previa del editor.

## 5. Pendientes

- **2 de diciembre:** en "Newsletter · Bienvenida", cambiar la acción "Bienvenida Delegate Brief" a la plantilla "Orchid · 05 Delegate Brief (sin oferta, desde 2 dic)". Hay que volver a escribir "Welcome to The Delegate Brief" y "One task worth delegating, every other week.", guardar la acción y luego el workflow. La plantilla ya está actualizada con la v2.
- Opcional: revisar en Gmail en modo claro y en Outlook o Apple Mail el contraste de la etiqueta y los botones.
- Opcional: anotar el ID del workflow "02 - Cita agendada".
