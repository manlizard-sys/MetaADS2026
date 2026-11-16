Necesito que completes las tareas pendientes de Orchid en GoHighLevel y en Meta Ads Manager para el lanzamiento de Black Friday. Son 4 partes. Hazlas en este orden, avísame al terminar cada una y detente si algo no coincide con lo que describo.

DATOS
- GHL: cuenta Orchid · dominio go.orchidpros.com
- Meta: cuenta publicitaria act_1806647434085082 (Orchid Pros) · página Orchid Pros (1132642053254708) · píxel 2271987886986577
- Landing de referencia (NO se toca): https://go.orchidpros.com/hire-50off
- Código de las landings (abre cada enlace, botón "Raw", copia TODO):
  Base: https://github.com/manlizard-sys/metaads2026/blob/claude/admiring-franklin-wrfknt/build/landings/short/
  - Salud: healthcare/block1.html · healthcare/block2.html · healthcare/block3.html
  - Emprendedores: entrepreneurs/block1.html · entrepreneurs/block2.html · entrepreneurs/block3.html
  - Newsletter: newsletter/block1.html · newsletter/block2.html · newsletter/block3.html
  La primera línea de cada block1 trae el título y la descripción SEO de esa página.

REGLAS
- No toques hire-50off, su formulario, sus workflows ni nada de abogados.
- En Meta no toques campañas, conjuntos, anuncios ni presupuestos. Solo creas el público de la Parte 4.
- Los tokens o claves nunca se escriben en el chat ni en notas.
- Si GHL o Meta no dejan hacer algo como lo describo, detente y dime qué opciones aparecen.
- No hagas envíos de prueba en los formularios: los hace Claude Code después para verificar la medición.

======================================================================
PARTE 1 · Tres landings en GHL
======================================================================
Estructura de CADA página (igual en las tres):
1. Sección 1: fondo #3F1D82, ancho completo, una fila con 2 columnas.
   - Columna izquierda: elemento Custom Code con block1.html (trae los estilos y la cuenta regresiva).
   - Columna derecha: el formulario de GHL de esa página. En celular la columna izquierda va primero y el formulario justo debajo.
2. Sección 2: ancho completo, padding y márgenes 0, un Custom Code con block2.html.
3. Sección 3: ancho completo, padding y márgenes 0, un Custom Code con block3.html (pie de página).
Nada más en la página: sin menú ni otras secciones.

1A · Consultorios médicos
1. Sites → Funnels → abre el funnel de hire-50off y agrega un paso nuevo DENTRO de ese funnel (hereda el código de seguimiento). Nombre "BF Healthcare", path: practices-free-month, página en blanco.
2. Sites → Forms: duplica el formulario de hire-50off → "Orchid · BF Healthcare". En la copia cambia SOLO la pregunta del tipo de firma: "What type of practice do you run?" con opciones Primary care · Dental · Physical therapy · Chiropractic · Specialty clinic · Other. Deja igual "Hiring or job seeking", nombre, email, teléfono, campos ocultos de UTM y el evento de píxel que ya tenga (Lead). Etiqueta al enviar: "bf-healthcare". Al enviar redirige al paso de gracias (punto 4).
3. Arma la página con la estructura de arriba usando los bloques de healthcare y este formulario. Pon el título y la descripción SEO de block1.
4. Paso de gracias: clona el paso de gracias de hire-50off (el del calendario) dentro del mismo funnel, path: practices-free-month-thanks.
5. Publica. Abre https://go.orchidpros.com/practices-free-month en una ventana nueva y confirma: carga, la cuenta regresiva corre y el botón "Get Started Free" del final sube al formulario.

1B · Empresas y emprendedores
Igual a 1A con estos cambios:
- Paso "BF Entrepreneurs", path: business-free-month · gracias: business-free-month-thanks.
- Formulario "Orchid · BF Entrepreneurs": la pregunta del tipo de firma pasa a "What type of business do you run?" con opciones Home services (roofing, HVAC, plumbing) · Construction · Insurance · Real estate or mortgage · E-commerce · Professional services · Other. Etiqueta "bf-business".
- Bloques de entrepreneurs.

1C · Newsletter (funnel APARTE)
1. Funnel nuevo "Orchid · Newsletter" en go.orchidpros.com. Paso "Brief", path: brief.
2. Código de seguimiento del funnel (Settings → Head tracking code): solo el código base del píxel 2271987886986577 con PageView. Cópialo del funnel de hire-50off pero SIN ningún evento Lead.
3. Formulario nuevo "Orchid · Newsletter": First name (obligatorio), Email (obligatorio), "What type of business do you run?" (Law firm · Medical or dental practice · Real estate · Accounting or finance · Home services · Other) y los mismos campos ocultos de UTM de hire-50off. Sin teléfono. Etiqueta "newsletter". Si el formulario tiene evento de píxel al enviar, elige "Subscribe" (NO "Lead"). Al enviar redirige al paso de gracias.
4. Paso de gracias "Brief Thanks", path: brief-thanks. Texto:
   Título: You're in.
   Texto: Your first Delegate Brief lands in your inbox soon. Want help now? Our Black Friday offer ($0 upfront + 50% off your first month) runs until December 1st.
   Botón: "Book a free call" → https://go.orchidpros.com/business-free-month
5. Arma la página con los bloques de newsletter, publica y confirma que https://go.orchidpros.com/brief carga.

======================================================================
PARTE 2 · Correo de bienvenida del newsletter (GHL)
======================================================================
1. Automation → Workflows → nuevo: "Newsletter · Bienvenida".
2. Disparador: Form Submitted = "Orchid · Newsletter".
3. Acción: Send Email, de inmediato. Remitente: el que usa Orchid para correos a clientes.
   Asunto: Welcome to The Delegate Brief
   Cuerpo:
   Hi {{contact.first_name}},

   Thanks for subscribing to The Delegate Brief. Every other week you'll get one task worth delegating, a ready-to-use template and the real numbers behind it. It takes 3 minutes to read.

   While you're here: our Black Friday offer runs until December 1st. Get started free with a bilingual professional from Colombia, then 50% off your first month.
   Book a free call: https://go.orchidpros.com/business-free-month

   Talk soon,
   Josué & Andrea, Orchid
4. Guarda y publica. No envíes el correo de prueba a ningún contacto real.

======================================================================
PARTE 3 · Workflow de la API de Conversiones (GHL)
======================================================================
1. Automation → Workflows → "Meta CAPI · Lead calificado".
2. Si el disparador filtra por formulario, agrega "Orchid · BF Healthcare" y "Orchid · BF Entrepreneurs" (NO el de newsletter). Si filtra solo por el campo "Hiring or job seeking", no cambies nada.
3. Guarda y publica solo si cambiaste algo.

======================================================================
PARTE 4 · Público de video en Meta Ads Manager
======================================================================
1. Abre https://adsmanager.facebook.com/adsmanager/audiences?act=1806647434085082
2. Crear público → Público personalizado → Fuente de Meta: Video.
3. Interacción: "Personas que vieron al menos el 50% de tu video".
4. Videos: todos los de la campaña "🟢 Orchid · Awareness · Video POV · Nov 2026" (6 verticales: Legal, Real Estate, Accounting, Finance, Entrepreneurs, Healthcare) y el POV Email. Si pide la fuente, busca en la página Orchid Pros y en "Cuenta publicitaria" / "Campañas".
5. Retención: 60 días. Nombre: VIDEO - 50% Awareness Nov26 - 60D. Crear.

======================================================================
AL TERMINAR, dime:
- Las tres URLs (practices-free-month, business-free-month, brief) y si cargan bien en celular.
- Qué evento de píxel dispara cada formulario.
- Si quedó publicado el workflow "Newsletter · Bienvenida".
- Si cambiaste el workflow de CAPI.
- El nombre exacto y el ID del público de video, y cuántos videos incluye.
- Cualquier paso que no coincidió con estas instrucciones.
