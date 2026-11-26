Hacer SOLO después de que Manuel haya agregado el calendario "Orchid - Discovery Call (Newsletter)" al workflow "02 - Cita agendada".

En GHL (sub-cuenta Orchid), funnel "Orchid · Agendar" → paso "Agendar" (path book-a-call):
1. Abre el Custom Code de la página.
2. Abre https://github.com/manlizard-sys/metaads2026/blob/claude/admiring-franklin-wrfknt/build/landings/newsletter_book/book_a_call.html → "Raw" → copia TODO.
3. Reemplaza TODO el contenido del Custom Code por lo copiado (es igual al de ahora, solo cambia el calendario a jgKkDzsDyVnOGqkIMxaT). Guarda y publica.
4. Comprueba en una ventana sin bloqueadores, sin reservar:
   https://go.orchidpros.com/book-a-call?utm_source=test&first_name=TEST%2053&email=hmlizarralde%2B53%40gmail.com&phone=3057124053
   - El calendario se llama "Orchid - Discovery Call (Newsletter)" y trae nombre, email y teléfono llenos.
   - DevTools → Network, filtro "facebook.com/tr": solo sale el PageView de la página, sin email ni teléfono; el iframe del calendario ya no carga connect.facebook.net.
No toques el calendario original, las landings de Black Friday ni Meta. Dime si quedó y cualquier cosa que no coincidió.
