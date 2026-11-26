# Handoff: flujo del newsletter (Orchid, GHL)

Última actualización: 2026-11-25, 22:30 (Bogotá).
Sub-cuenta GHL: **Orchid**, Location `r5demglXbNG9LoCszFIw`. Dominio: `go.orchidpros.com`.
Repo: `manlizard-sys/metaads2026`, rama `claude/admiring-franklin-wrfknt`, carpeta `build/landings/newsletter_book/`.

## 1. Flujo completo

1. Mailchimp envía el newsletter. El botón lleva a `/book-a-call` con los datos del suscriptor en la URL.
2. `/book-a-call` pasa `first_name`, `email`, `phone` (y `utm_*`) al calendario embebido, borra los datos personales de la barra de direcciones y luego carga el píxel de Meta (PageView).
3. La persona elige día y hora (nombre, teléfono y email ya vienen llenos) y reserva.
4. El calendario redirige a `/book-a-call-thanks`, que limpia la URL y manda a Meta PageView + Schedule, sin datos personales.
5. GHL crea el contacto y la cita, envía el correo de confirmación y dispara el workflow "02 - Cita agendada".

Enlace del botón en Mailchimp (pendiente de pegar por Manuel):

```
https://go.orchidpros.com/book-a-call?utm_source=newsletter&utm_medium=email&utm_campaign=newsletter-black-friday-2026&first_name=*|URL:FNAME|*&email=*|URL:EMAIL|*&phone=*|URL:PHONE|*
```

Usar `*|URL:...|*`: sin la codificación, un email con "+" llega con espacio. Si la audiencia usa otras merge tags para nombre o teléfono, cambiarlas.

## 2. Páginas (funnel "Orchid · Agendar")

El funnel es nuevo y separado del funnel "Orchid · Newsletter" (`/brief`), porque ese tiene el píxel 2271987886986577 en su Head tracking code (no se tocó).

Settings del funnel "Orchid · Agendar":
- Head y Body tracking code: vacíos (sin píxel).
- "Optimize JavaScript": apagado (si se enciende, el Custom Code carga en diferido y el calendario tarda).

| Paso | Path | Archivo en el repo | SEO title |
|---|---|---|---|
| Agendar | `/book-a-call` | `book_a_call.html` | Black Friday at Orchid \| $0 Down + 50% Off Your First Month |
| Gracias | `/book-a-call-thanks` | `book_a_call_thanks.html` | You're booked \| Orchid |

Estructura de cada paso en el builder: 1 sección full width, fila de 1 columna, columna y elemento Custom Code; padding y márgenes en 0 en sección, fila y columna. El Custom Code contiene el archivo HTML completo. Header y Footer Tracking Code del paso: vacíos.

GHL también sirve las páginas en slugs internos (`/book-a-call-page`, `/book-a-call-page-209305`); no importa.

### book_a_call.html (publicado = repo, commit 2f10f44)
- `CONFIG.CALENDAR_URL` = `https://api.leadconnectorhq.com/widget/booking/jgKkDzsDyVnOGqkIMxaT` (calendario Newsletter).
- El script de configuración va justo después del iframe para que el calendario empiece a cargar antes.
- Preconnects a `api.leadconnectorhq.com` y `stcdn.leadconnectorhq.com`, logo superior con `fetchpriority="high"`, logo del pie con `loading="lazy"`.
- Orden importante: asigna `src` del iframe con los datos, luego `history.replaceState` (deja solo `utm_*`), luego carga el píxel y `PageView`.
- `form_embed.js` de GHL se carga al final (sin `async`): ajusta la altura del iframe y ejecuta la redirección del calendario a la página de gracias.

### book_a_call_thanks.html (nuevo)
- Mismo estilo. Contenido: "You're booked. Talk soon.", oferta bloqueada ($0 down, 50% off, reservado antes del 1 de diciembre), "Before the call" (3 pasos), "Need a different time?".
- Script: borra de la URL todo lo que no sea `utm_*`, carga el píxel, `PageView` y `Schedule` (`content_name: 'Newsletter discovery call'`), este último una vez por sesión (`sessionStorage` clave `orx_nl_schedule`).
- Tiene `<meta name="robots" content="noindex">` dentro del Custom Code.

### Cómo actualizar una página en GHL
1. Sites → Funnels → "Orchid · Agendar" → paso → Edit.
2. Clic en el elemento Custom Code → Open Code Editor → seleccionar todo → pegar el archivo completo → Save.
3. Publish. En este editor el primer clic en Publish a veces solo abre el panel de SEO; repetir hasta ver el aviso "Page published successfully".
4. Verificar trayendo el HTML publicado con un `fetch` desde una página del mismo dominio (por ejemplo `go.orchidpros.com/<ruta-inexistente>`, que no carga píxel) para no disparar eventos de Meta.

## 3. Calendarios

| Calendario | ID | Uso | Meta pixel ID | Confirmación |
|---|---|---|---|---|
| Orchid - Discovery Call | `739uffEjsGH7PH0Zaovn` | Páginas de gracias de Black Friday (ads) | 2271987886986577 (sin tocar) | Mensaje de gracias (sin tocar) |
| Orchid - Discovery Call (Newsletter) | `jgKkDzsDyVnOGqkIMxaT` | Página `/book-a-call` | Vacío | Redirect URL `https://go.orchidpros.com/book-a-call-thanks` |

- El calendario Newsletter es un duplicado del original (staff Andrea Bolanos, Google Meet, misma disponibilidad y duración), slug `orchid-discovery-call-newsletter`.
- Motivo del duplicado: el widget del calendario carga el píxel configurado dentro del iframe y manda un PageView con la URL del iframe, que contiene `first_name`, `email` y `phone`. El duplicado sin píxel evita esa fuga.
- **Problema abierto:** el calendario original sigue enviando email y teléfono a Meta desde las páginas de gracias de los ads. No se cambió porque los ads dependen de ese píxel; decisión pendiente de Manuel.

## 4. Formulario de reserva

Formulario nuevo **"Orchid · Booking (Discovery Call)"**, asignado a ambos calendarios (en el original reemplazó al "Default", que no se puede editar):

| Campo | Tipo | Obligatorio | Query Key |
|---|---|---|---|
| Full Name | Full Name | Sí | `first_name` (cambiado a propósito) |
| Phone | Phone | Sí | `phone` |
| Email | Email | Sí | `email` |

- El Query Key de Full Name es `first_name` para que el parámetro `first_name` del enlace lo prellene. Con el valor por defecto (`full_name`) no se llenaba; `name` tampoco funciona.
- Al reservar, GHL separa el nombre en First name / Last name (probado: "TEST 52" queda First "TEST", Last "52").
- El teléfono toma el código de país según la ubicación del visitante (desde Colombia quedó +57; un visitante en EE. UU. queda +1).
- Se quitaron las casillas de consentimiento SMS de plantilla ("[BUSINESS NAME]") y el texto Privacy/Terms de plantilla.
- No se tocaron los formularios existentes.

## 5. Workflow "02 - Cita agendada"

- Trigger original "Customer Booked Appointment" (filtro: calendario Orchid - Discovery Call): sin cambios.
- Trigger nuevo **"Customer Booked Appointment (Newsletter)"** (filtro: calendario Orchid - Discovery Call (Newsletter)), duplicado del original. Workflow guardado y publicado.
- Verificado: la reserva de prueba en el calendario Newsletter inscribió al contacto (31 → 32 inscritos).
- Ramas del workflow (sin cambios): Descartado (tag job-seeker → cancela la cita), Lead calificado, Sin formulario (crea tarea de revisión).
- El workflow "Meta CAPI · Lead calificado" se dispara por formularios con el campo "Hiring or job seeking"; el formulario de reserva no lo tiene, así que no se dispara.

## 6. Pruebas realizadas

- Prefill, layout escritorio (calendario a la derecha) y móvil (debajo del texto), URL limpia y `fbq.getState()` con 1 evento sin advanced matching.
- El iframe del calendario Newsletter no carga `connect.facebook.net` (0 peticiones, `fbq` indefinido).
- Reserva TEST 52 (calendario original, 8 dic 3:30 PM): contacto y separación de nombre correctos. Cita cancelada; contacto borrado.
- Reserva TEST 53 (calendario Newsletter, 8 dic 3:00 PM): redirección a `/book-a-call-thanks` con URL limpia, PageView + Schedule sin datos personales, workflow disparado. Cita cancelada; contacto borrado.
- No se pudo ver la petición `facebook.com/tr` en el navegador de Manuel (parece bloqueada por una extensión); la verificación se hizo con `fbq.getState()` y Resource Timing.

## 7. Notas y trampas conocidas

- El Header Tracking Code del paso lo inserta GHL con JavaScript después de cargar, así que no sirve para preconnects; se dejó vacío.
- GHL registra el origen de estos contactos como "Direct traffic" aunque la URL traiga `utm_source`; la campaña sí se guarda. La redirección a la página de gracias no conserva los `utm_*`.
- La primera visita a `/book-a-call` antes de publicar quedó en caché en blanco unos minutos; con parámetros en la URL no pasa.
- El Chrome de Manuel tiene modo oscuro forzado: las tarjetas blancas se ven oscuras, pero el color calculado es blanco.
- Cambiar el estado de una cita a Cancelled abrió un diálogo nativo que bloqueó la extensión del navegador. Solución usada: ejecutar antes `window.confirm = () => true` en la pestaña.
- La edición de workflows fue bloqueada una vez por el clasificador de permisos; se hizo después con autorización explícita de Manuel.
- Rendimiento: la página carga en ~0.6-1.5 s; el cuello de botella es el widget de GHL (~104 archivos, contenido a ~1.8 s), que no se puede acelerar desde la página.

## 8. Pendientes

1. **Manuel:** pegar el enlace en el botón del newsletter en Mailchimp y enviarse una prueba a un correo que esté en la audiencia (la vista previa no llena las merge tags).
2. **Decisión de Manuel:** qué hacer con el píxel del calendario original (fuga de email/teléfono en las páginas de gracias de los ads).
3. Opcional: cambiar Fraunces por una versión más liviana (sin eje `opsz`) para bajar el peso de las fuentes; cambia un poco el aspecto de los títulos.
4. Opcional: borrar los contactos de prueba TEST 50 y TEST 51 (del 23 de noviembre).

## 9. No se tocó

Landings y páginas de gracias de Black Friday de los ads, Meta (Ads Manager / Events Manager), formularios existentes, funnel "Orchid · Newsletter" (`/brief`), disponibilidad y duración de los calendarios, y la confirmación del calendario original.
