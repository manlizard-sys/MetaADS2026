Necesito que conectes GoHighLevel (cuenta Orchid) con la API de Conversiones de Meta, para que Meta sepa qué leads son firmas que quieren contratar y cuáles agendan llamada. Trabaja en este orden, avísame al terminar cada paso y detente si algo no coincide con lo que describo.

DATOS
- Píxel / dataset de Meta: OrchidPixel, ID 2271987886986577
- Business Manager: OrchidPros (1534891157898770)
- Campo de GHL con la respuesta del filtro: "Hiring or job seeking" (la opción buena es "I want to hire." en la landing y "I want to hire an assistant" en el formulario de Meta)
- Etiqueta de citas agendadas: "agendo"

REGLAS
- El token de acceso de Meta solo se copia de Events Manager y se pega en GHL. No lo escribas en el chat, ni en notas, ni en ningún otro lugar.
- No crees un evento "Lead" por esta vía: el píxel de la landing ya lo envía y quedaría duplicado. Solo vamos a enviar los dos eventos nuevos de abajo.
- No toques anuncios, campañas ni presupuestos en Meta.

PASO 1 · Generar el token en Meta
1. Abre https://business.facebook.com/events_manager2 y elige el dataset "OrchidPixel" (2271987886986577).
2. Ve a Configuración (Settings) → sección "API de conversiones" → "Generar token de acceso" (Generate access token).
3. Copia el token y déjalo en el portapapeles para el paso 3. No lo pegues en ningún otro lado.

PASO 2 · Workflow 1 en GHL: "Meta CAPI · Lead calificado"
1. En GHL ve a Automation → Workflows → Create workflow → Start from scratch. Nombre: "Meta CAPI · Lead calificado".
2. Trigger: "Contact Changed" (o "Form Submitted" si no existe), con filtro: campo "Hiring or job seeking" contiene "hire". Si el formulario de Meta usa el trigger "Facebook Lead Form Submitted", agrega un segundo trigger igual con el mismo filtro.
3. Acción: "Facebook Conversion API" (puede llamarse "Meta Conversions API" o estar dentro de "Send Data").
   - Pixel ID: 2271987886986577
   - Access token: el del paso 1
   - Event name: Custom → "QualifiedLead"
   - Action source: website
   - Mapea email, teléfono, nombre y apellido del contacto (Meta los cifra; mejoran la coincidencia).
4. Guarda y publica el workflow.

PASO 3 · Workflow 2 en GHL: "Meta CAPI · Cita agendada"
1. Nuevo workflow: "Meta CAPI · Cita agendada".
2. Trigger: "Appointment Status" = Booked/Confirmed (o "Contact Tag Added" = "agendo", el que exista).
3. Acción: "Facebook Conversion API" con los mismos datos, Event name: "Schedule" (evento estándar de Meta).
4. Guarda y publica.

PASO 4 · Probar
1. En Events Manager → OrchidPixel → pestaña "Probar eventos" (Test events), copia el código de prueba (TEST…).
2. Si la acción de GHL tiene campo "Test event code", pégalo temporalmente en los dos workflows.
3. Llena el formulario de https://go.orchidpros.com/50off-form con: nombre "Test CAPI", email test.capi@example.com, "I want to hire.", "Immigration law", y agenda una cita.
4. En "Probar eventos" deberían aparecer "QualifiedLead" y "Schedule" en 1–2 minutos, recibidos por "Servidor" (Server).
5. Borra el código de prueba de los workflows y vuelve a publicarlos.
6. Borra en GHL el contacto "Test CAPI" y cancela su cita.

AL TERMINAR, dime:
- Si los dos eventos aparecieron en "Probar eventos" y desde qué fuente.
- El nombre exacto de la acción que usaste en GHL.
- Cualquier paso que no coincidió con estas instrucciones.
