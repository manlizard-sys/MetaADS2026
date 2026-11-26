Necesito montar en GHL (sub-cuenta Orchid, Location r5demglXbNG9LoCszFIw) la página a la que llega el newsletter de Mailchimp. El diseño ya está hecho; solo hay que pegarlo y conectarle el calendario. La persona llega con sus datos ya llenos, elige la hora y queda agendada. No toques las landings de Black Friday de los anuncios, ni Meta, ni los formularios existentes. No hagas reservas de prueba sin avisarme.

PARTE 1 · El calendario
1. Ve a Calendars y dime qué calendarios hay. Usa el que ya está en las páginas de gracias de Black Friday (practices-free-month-thanks), el que pone la etiqueta "agendo".
2. En ese calendario → Form (formulario de la reserva): deja SOLO Nombre, Teléfono y Email, los tres obligatorios.
3. Copia el ID del calendario: está en su enlace de reserva o en el código de inserción, en la parte que dice /widget/booking/<ID>.
4. Abre su enlace público agregando ?first_name=TEST%2052&email=hmlizarralde%2B52%40gmail.com&phone=3057124052 y dime si nombre, email y teléfono aparecen llenos. Si no, dime con qué nombres de parámetro sí se llenan. NO confirmes la reserva.

PARTE 2 · La página
1. En el funnel del newsletter (el de go.orchidpros.com/brief), crea un paso nuevo llamado "Agendar" con path: book-a-call
2. Una sola sección de ancho completo, padding y márgenes en 0, con un elemento Custom Code.
3. Abre https://github.com/manlizard-sys/metaads2026/blob/claude/admiring-franklin-wrfknt/build/landings/newsletter_book/book_a_call.html → "Raw" → copia TODO y pégalo en ese Custom Code.
4. En lo que pegaste, reemplaza __CALENDAR_ID__ por el ID del calendario de la Parte 1. Si en la Parte 1.4 los parámetros tenían otros nombres, avísame antes de publicar.
5. Settings del paso → Tracking Code: deja el Header y el Footer SIN el píxel de Meta. La página ya carga el píxel ella misma, después de borrar los datos personales de la barra de direcciones. Revisa también el Tracking Code del funnel: si ahí está el píxel, dime antes de quitarlo.
6. SEO: título "Black Friday at Orchid | $0 Down + 50% Off Your First Month".
7. En el calendario, la confirmación de la reserva debe llevar a la página de gracias de llamadas que ya existe. Si no hay una, dime y la creamos.
8. Publica.

PARTE 3 · Comprobación (sin reservar)
1. Abre en celular y en escritorio:
   https://go.orchidpros.com/book-a-call?utm_source=newsletter&utm_medium=email&utm_campaign=test52&first_name=TEST%2052&email=hmlizarralde%2B52%40gmail.com&phone=3057124052
2. Confirma que:
   - el calendario aparece en el recuadro blanco, a la derecha en escritorio y debajo del texto en celular;
   - nombre, email y teléfono ya vienen llenos y solo falta elegir día y hora;
   - la barra de direcciones ya no muestra first_name, email ni phone, pero sí los utm_;
   - en DevTools → Network, filtrando "facebook.com/tr", sale un PageView y su URL NO contiene el email ni el teléfono.

AL TERMINAR, dime:
- Qué calendario usaste, su ID y la URL pública de la página.
- Los nombres exactos de los parámetros que prellenan el calendario.
- Si el píxel estaba en el Tracking Code del funnel.
- Si algo no se pudo hacer como se describe.
