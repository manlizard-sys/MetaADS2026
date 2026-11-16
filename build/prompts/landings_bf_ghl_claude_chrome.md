Necesito que crees tres landings nuevas en GoHighLevel (cuenta Orchid): una para consultorios médicos, una para empresas y emprendedores y una para el newsletter. Son cortas, con el formulario arriba y una cuenta regresiva hasta Thanksgiving. El código ya está escrito; tú armas las páginas, pegas el código y conectas los formularios. Trabaja en este orden, avísame al terminar cada paso y detente si algo no coincide.

DATOS
- Dominio: go.orchidpros.com · Píxel de Meta: 2271987886986577
- Landing de referencia (no se toca): https://go.orchidpros.com/hire-50off
- Código de cada página (abre el enlace, botón "Raw", copia todo):
  Base: https://github.com/manlizard-sys/metaads2026/blob/claude/admiring-franklin-wrfknt/build/landings/short/
  - Salud: healthcare/block1.html · healthcare/block2.html · healthcare/block3.html
  - Emprendedores: entrepreneurs/block1.html · entrepreneurs/block2.html · entrepreneurs/block3.html
  - Newsletter: newsletter/block1.html · newsletter/block2.html · newsletter/block3.html
  La primera línea de cada block1 dice el título y la descripción SEO de esa página.

REGLAS
- No toques hire-50off, su formulario ni sus workflows.
- No toques anuncios ni campañas en Meta.
- Si GHL no deja hacer algo como lo describo, detente y dime qué opciones aparecen.

ESTRUCTURA DE CADA PÁGINA (igual en las tres)
1. Sección 1: fondo #3F1D82, ancho completo, una fila con 2 columnas.
   - Columna izquierda: elemento Custom Code con block1.html (trae todos los estilos y la cuenta regresiva).
   - Columna derecha: el formulario de GHL (ver cada paso). En celular la columna izquierda va primero y el formulario justo después.
2. Sección 2: ancho completo, padding y márgenes 0, un elemento Custom Code con block2.html.
3. Sección 3: ancho completo, padding y márgenes 0, un elemento Custom Code con block3.html (pie de página).
4. Nada más en la página: sin menú, sin otras secciones.

PASO 1 · Consultorios médicos
1. Sites → Funnels → abre el funnel de hire-50off y agrega un paso nuevo DENTRO de ese funnel (así hereda el código de seguimiento del funnel). Nombre "BF Healthcare", path practices-free-month, página en blanco.
2. Formulario: en Sites → Forms duplica el formulario que usa hire-50off y nómbralo "Orchid · BF Healthcare". En la copia cambia solo la pregunta del tipo de firma: "What type of practice do you run?" con opciones Primary care · Dental · Physical therapy · Chiropractic · Specialty clinic · Other. Deja igual "Hiring or job seeking", nombre, email, teléfono, los campos ocultos de UTM y el evento de píxel que ya tenga. Agrega la etiqueta "bf-healthcare". Al enviar: redirigir al paso de gracias (punto 4).
3. Arma la página con la estructura de arriba usando los bloques de healthcare y este formulario. Pon el título y descripción SEO de block1.
4. Paso de gracias: clona el paso de gracias de hire-50off (el que tiene el calendario) dentro del mismo funnel, path practices-free-month-thanks.
5. Publica y abre https://go.orchidpros.com/practices-free-month en una ventana nueva: confirma que carga, que la cuenta regresiva corre y que el botón "Get Started Free" del final sube al formulario.

PASO 2 · Empresas y emprendedores
Igual al paso 1, con estos cambios:
- Paso "BF Entrepreneurs", path business-free-month; gracias: business-free-month-thanks.
- Formulario "Orchid · BF Entrepreneurs": la pregunta del tipo de firma pasa a "What type of business do you run?" con opciones Home services (roofing, HVAC, plumbing) · Construction · Insurance · Real estate or mortgage · E-commerce · Professional services · Other. Etiqueta "bf-business".
- Bloques de entrepreneurs.

PASO 3 · Newsletter (va en un funnel aparte)
1. Crea un funnel nuevo "Orchid · Newsletter" en el dominio go.orchidpros.com. Paso "Brief", path brief.
2. Código de seguimiento del funnel (Settings → Head tracking code): solo el código base del píxel 2271987886986577 con PageView. Cópialo del funnel de hire-50off pero SIN ningún evento Lead.
3. Formulario nuevo "Orchid · Newsletter": First name (obligatorio), Email (obligatorio), "What type of business do you run?" (Law firm · Medical or dental practice · Real estate · Accounting or finance · Home services · Other), y los mismos campos ocultos de UTM de hire-50off. Sin teléfono. Etiqueta "newsletter". Si el formulario tiene opción de evento de píxel al enviar, elige "Subscribe" (NO "Lead"). Al enviar: redirigir al paso de gracias.
4. Paso de gracias "Brief Thanks", path brief-thanks, con este texto: título "You're in." · texto "Your first Delegate Brief lands in your inbox soon. Want help now? Our Black Friday offer ($0 upfront + 50% off your first month) runs until Thanksgiving." · botón "Book a free call" que lleva a https://go.orchidpros.com/business-free-month.
5. Arma la página con la estructura de arriba usando los bloques de newsletter. Publica y comprueba que https://go.orchidpros.com/brief carga.

PASO 4 · Workflow de la API de Conversiones
1. Automation → Workflows → "Meta CAPI · Lead calificado".
2. Si el disparador filtra por formulario, agrega "Orchid · BF Healthcare" y "Orchid · BF Entrepreneurs" (NO el de newsletter). Si filtra solo por el campo "Hiring or job seeking", no cambies nada.

AL TERMINAR, dime:
- Las tres URLs y si cargan bien en celular.
- Qué evento de píxel dispara cada formulario.
- Si cambiaste el workflow de CAPI.
- Cualquier paso que no coincidió.

No hagas envíos de prueba: los hace Claude Code después para verificar la medición.
