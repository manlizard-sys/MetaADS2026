Necesito crear en GHL (sub-cuenta Orchid, Location r5demglXbNG9LoCszFIw) una página simple para agendar llamadas desde el newsletter de Mailchimp. La persona llega desde el newsletter, ve el calendario con sus datos ya llenos, elige la hora y queda agendada. No toques las landings de Black Friday, ni Meta, ni los formularios existentes. No hagas reservas de prueba sin avisarme.

PARTE 1 · El calendario
1. Ve a Calendars y dime qué calendarios hay. Usa el que ya está en las páginas de gracias de Black Friday (practices-free-month-thanks), el que pone la etiqueta "agendo".
2. En ese calendario → Form (formulario de la reserva): deja SOLO Nombre, Teléfono y Email, los tres obligatorios. No agregues más campos.
3. Dime si el calendario acepta datos prellenados por la URL (parámetros como first_name, email, phone) y con qué nombres exactos. Prueba abriendo su enlace público con ?first_name=TEST%2052&email=hmlizarralde%2B52%40gmail.com&phone=3057124052 y dime si aparecen llenos. NO confirmes la reserva.

PARTE 2 · La página
1. En el funnel del newsletter (el de go.orchidpros.com/brief), crea un paso nuevo llamado "Agendar" con path: book-a-call
2. Contenido, de arriba hacia abajo, fondo violeta #3F1D82 y textos blancos como las otras landings:
   - Título: "Pick a time. We'll call you."
   - Una línea: "A free 30-minute call to see what a bilingual assistant from Colombia can take off your plate."
   - El widget del calendario de la Parte 1, a todo el ancho de la columna.
3. Settings → Tracking Code → Header: solo el código base del píxel de Meta 2271987886986577 con PageView, igual que en las otras páginas. Footer: pega esto, que borra los datos personales de la barra de direcciones después de que el calendario los lee, para no mandárselos a Meta:
   <script>setTimeout(function(){try{var u=new URL(location.href);['first_name','last_name','name','email','phone'].forEach(function(k){u.searchParams.delete(k)});history.replaceState(null,'',u.toString());}catch(e){}},4000);</script>
4. Después de reservar, que lleve a la página de gracias de llamadas que ya existe (la del calendario). Si no hay una, dime y la creamos.
5. Publica.

PARTE 3 · Comprobación (sin reservar)
1. Abre en celular y en escritorio:
   https://go.orchidpros.com/book-a-call?utm_source=newsletter&utm_medium=email&utm_campaign=test52&first_name=TEST%2052&email=hmlizarralde%2B52%40gmail.com&phone=3057124052
2. Confirma que el calendario carga con nombre, email y teléfono ya llenos y que solo falta elegir día y hora.
3. Confirma que a los pocos segundos la barra de direcciones ya no muestra first_name, email ni phone, pero sí los utm_.

AL TERMINAR, dime:
- Qué calendario usaste y la URL pública de la página.
- Los nombres exactos de los parámetros que prellenan el calendario (para armar el enlace de Mailchimp).
- Si algo no se pudo hacer como se describe.
