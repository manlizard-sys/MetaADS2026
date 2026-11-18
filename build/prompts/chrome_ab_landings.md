Necesito crear una prueba A/B (split test) en dos landings de Orchid en GHL: la versión corta que ya existe (A) contra una versión larga nueva (B), 50/50, en la misma URL. Hazlo en orden, avísame al terminar cada parte y detente si algo no coincide.

REGLAS
- No toques hire-50off ni nada de abogados. No toques Meta.
- No cambies la variante A (la que está publicada hoy), salvo lo indicado en la Parte 0.
- No hagas envíos de prueba.

CÓDIGO (abre cada enlace, botón "Raw", copia TODO)
Base: https://github.com/manlizard-sys/metaads2026/blob/claude/admiring-franklin-wrfknt/build/landings/
- Salud B: healthcare/piece1.html · healthcare/piece2.html · healthcare/piece3.html
- Emprendedores B: entrepreneurs/piece1.html · entrepreneurs/piece2.html · entrepreneurs/piece3.html
- Salud A (actualización pendiente): short/healthcare/block1.html · short/healthcare/block2.html

PARTE 0 · Actualizar la variante A de salud (si no se hizo ya)
En el paso "BF Healthcare" (practices-free-month), variante actual: reemplaza el Custom Code del bloque 1 por short/healthcare/block1.html y el del bloque 2 por short/healthcare/block2.html. Publica. Debe verse "HIPAA-trained" y "Ongoing HR support from Orchid" como etiquetas blancas bajo el título.

PARTE 1 · Variante B de salud
1. Sites → Funnels → funnel de hire-50off → paso "BF Healthcare" (path practices-free-month).
2. Crea una variante para split test ("Create Variation" / "Split Test"), desde página en blanco. Nombre: "B · Larga".
3. Estructura de la variante B:
   - Sección 1: ancho completo, padding y márgenes 0, un Custom Code con healthcare/piece1.html (trae todos los estilos).
   - Sección 2: fondo #3F1D82, una fila con 2 columnas: columna izquierda Custom Code con healthcare/piece2.html; columna derecha el MISMO formulario "Orchid · BF Healthcare" que usa la variante A.
   - Sección 3: ancho completo, padding y márgenes 0, Custom Code con healthcare/piece3.html (pie).
4. Ajustes de la página B: copia exactamente el código de seguimiento de la variante A (píxel 2271987886986577 con PageView) y el título/descripción SEO de A. El formulario debe redirigir a la misma página de gracias que A (practices-free-month-thanks).
5. Reparto de tráfico: 50% A / 50% B. Publica la prueba.
6. Abre https://go.orchidpros.com/practices-free-month varias veces en ventana incógnito hasta ver la variante B. Confirma: carga, la cuenta regresiva dice "Ends Dec 1 · days / hrs / min", los botones "Get Started Free" bajan al formulario, y la URL termina agregando "lp_variant=long".

PARTE 2 · Variante B de emprendedores
Igual a la Parte 1 en el paso "BF Entrepreneurs" (business-free-month), con entrepreneurs/piece1-3.html, el formulario "Orchid · BF Entrepreneurs" y la página de gracias business-free-month-thanks.

AL TERMINAR, dime:
- Si las dos pruebas quedaron activas al 50/50.
- Si viste la variante B en cada URL y si la URL mostró lp_variant=long.
- Dónde muestra GHL las estadísticas de la prueba (vistas y conversiones por variante).
- Cualquier paso que no coincidió.
