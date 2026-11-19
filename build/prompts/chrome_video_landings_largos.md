Necesito poner el video de Andrea y Josué en la variante "B · Larga" de dos landings de Orchid en GHL. Hoy esa variante tiene un video de YouTube de relleno que NO es nuestro: es un video musical de otra marca. Por eso es urgente. Hazlo en orden y avísame al terminar.

REGLAS
- Solo toca la variante "B · Larga". No cambies la variante corta (A) ni el reparto 50/50 de la prueba.
- No toques hire-50off, abogados ni Meta. No hagas envíos de prueba del formulario.

PASO 1 · Subir el video a GHL
1. Descarga el video desde https://github.com/manlizard-sys/metaads2026/blob/claude/admiring-franklin-wrfknt/build/landings/long_designs/video/video_web_2_web720.mp4 (botón "Download" / "View raw"). Pesa 5.5 MB y dura 1:05.
2. En GHL ve a Sites → Media (Media Library) y súbelo.
3. Copia la URL pública del archivo; debe terminar en .mp4. Ábrela en una pestaña nueva y confirma que el video se reproduce.

PASO 2 · Parche en la landing de salud
1. Sites → Funnels → funnel de hire-50off → paso "BF Healthcare" (practices-free-month) → variante "B · Larga" → editar.
2. Abre el Custom Code del bloque 1 (la sección grande de arriba).
3. Abre https://github.com/manlizard-sys/metaads2026/blob/claude/admiring-franklin-wrfknt/build/landings/long_designs/video_patch.html, pulsa "Raw" y copia TODO el contenido.
4. Pégalo AL FINAL del Custom Code del bloque 1, después de todo lo que ya hay. No borres nada.
5. En lo que pegaste, reemplaza __VIDEO_URL__ por la URL del Paso 1.3. Debe quedar entre las comillas simples: var URL_MP4='https://…mp4';
6. Guarda y publica.

PASO 3 · Parche en la landing de emprendedores
Haz lo mismo que en el Paso 2, en el paso "BF Entrepreneurs" (business-free-month) → variante "B · Larga".

PASO 4 · Comprobación
1. En ventana de incógnito, abre https://go.orchidpros.com/practices-free-month varias veces hasta que salga la versión larga. La reconoces porque la URL agrega "lp_variant=long".
2. Pulsa el botón rojo de play sobre la foto de Andrea y Josué. Debe reproducirse el video de ellos dos ("Hi, I'm Andrea…"), no un video de YouTube.
3. Repite con https://go.orchidpros.com/business-free-month.
4. Prueba también en vista de celular.

AL TERMINAR, dime:
- La URL del video en GHL.
- Si en las dos landings largas el play reproduce el video de Andrea y Josué.
- Cualquier paso que no coincidió.
