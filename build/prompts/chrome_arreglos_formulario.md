Necesito 4 arreglos en GHL para las landings Black Friday de Orchid (funnel "Orchid - Hire a VA", sub-cuenta Orchid, Location r5demglXbNG9LoCszFIw). No toques Meta ni el reparto 50/50 de la prueba A/B. No hagas envíos de formulario. El editor de código de GHL no tiene búsqueda, así que ubica los textos leyendo.

PARTE 1 · Evento Lead en las páginas de gracias (lo más importante)
Hoy el evento Lead del píxel se dispara justo cuando GHL redirige a la página de gracias, y la petición se pierde. Lo vamos a mandar desde la página de gracias.
1. Abre el paso de gracias de salud (path practices-free-month-thanks) → Settings → Tracking Code.
   a. Si en Header aparece DOS veces el código base del píxel 2271987886986577 (fbq('init'...) + PageView), deja solo uno y borra el duplicado. Dime qué encontraste.
   b. En Footer, pega esto y guarda:
      <script>(function(){var n=0;(function f(){if(window.fbq){fbq('track','Lead');}else if(n++<20){setTimeout(f,250);}})();})();</script>
2. Repite el paso 1 en el paso de gracias de emprendedores (path business-free-month-thanks).
3. Busca de dónde sale hoy el Lead al enviar el formulario, para que no se cuente doble:
   - En Sites → Forms → "Orchid · BF Healthcare" y "Orchid · BF Entrepreneurs" → Settings / Integrations: si hay una opción de "Facebook Pixel" con evento Lead al enviar, desactívala.
   - En el Tracking Code de los pasos practices-free-month y business-free-month (ambas variantes): si hay un script con fbq('track','Lead'), bórralo. NO borres el código base del píxel ni el PageView.
   Dime exactamente qué quitaste y de dónde.
4. Publica los pasos.

PARTE 2 · Landing larga en celular (solo la variante "B · Larga" de los dos pasos)
1. Paso "BF Healthcare" (practices-free-month) → variante "B · Larga" → Custom Code del bloque 1.
2. Abre https://github.com/manlizard-sys/metaads2026/blob/claude/admiring-franklin-wrfknt/build/landings/long_designs/form_ux_patch.html → "Raw" → copia todo.
3. Pégalo AL FINAL del Custom Code del bloque 1, después de lo último que hay. No borres nada. Guarda y publica.
4. Repite en "BF Entrepreneurs" (business-free-month) → variante "B · Larga".
Resultado esperado: el botón "Book My Free Call" se ve con letra violeta sobre amarillo, y la barra roja fija de abajo desaparece mientras el formulario está en pantalla.

PARTE 3 · Campo de nombre (en los dos formularios)
En Sites → Forms → "Orchid · BF Healthcare" y "Orchid · BF Entrepreneurs", campo "Full Name": cambia el placeholder "Enter your first name" por "Enter your full name". Guarda.

PARTE 4 · Comprobación (sin enviar el formulario)
1. Abre en vista de celular https://go.orchidpros.com/practices-free-month-page-865761 y https://go.orchidpros.com/business-free-month-page. Baja hasta el formulario y confirma que la barra roja se oculta y que el botón se lee bien.
2. Abre directamente https://go.orchidpros.com/practices-free-month-thanks y https://go.orchidpros.com/business-free-month-thanks. En DevTools → Network, filtra "facebook.com/tr" y confirma que sale UNA petición con ev=PageView y UNA con ev=Lead.

AL TERMINAR, dime:
- Qué duplicado de píxel encontraste en las páginas de gracias y si lo quitaste.
- De dónde salía el Lead del formulario y qué desactivaste.
- Si en las páginas de gracias ahora sale exactamente 1 PageView y 1 Lead.
- Si el parche de la landing larga quedó en las dos variantes.
- Si cambiaste el placeholder en los dos formularios.
