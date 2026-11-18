Necesito montar una prueba A/B (split test) en dos landings de Orchid en GHL. La versión corta que ya está publicada es la A. La versión larga nueva es la B. El tráfico va 50/50 en la misma URL. Hazlo en orden, avísame al terminar cada parte y detente si algo no coincide.

REGLAS
- No toques hire-50off ni nada de abogados. No toques Meta.
- No cambies la variante A (la publicada hoy), salvo lo que dice la Parte 0.
- No hagas envíos de prueba del formulario.
- En la página B, el píxel va solo con su código base (PageView). NO agregues ningún evento Lead: el Lead ya lo manda el formulario de GHL, y si se agrega otro, cada lead se cuenta dos veces. El bloque 1 trae un comentario que dice "Meta Pixel: pegar aquí…": déjalo como está y no pegues nada ahí.

CÓDIGO (abre cada enlace, pulsa "Raw" y copia TODO el contenido)
Base: https://github.com/manlizard-sys/metaads2026/blob/claude/admiring-franklin-wrfknt/build/landings/
- Salud B: long_designs/healthcare/block1_widget.html · long_designs/healthcare/block2_form_column.html · long_designs/healthcare/block3_footer.html
- Emprendedores B: long_designs/entrepreneurs/block1_widget.html · long_designs/entrepreneurs/block2_form_column.html · long_designs/entrepreneurs/block3_footer.html
- Salud A (actualización pendiente): short/healthcare/block1.html · short/healthcare/block2.html

PARTE 0 · Actualizar la variante A de salud (si no se hizo ya)
1. Ve al paso "BF Healthcare" (practices-free-month), variante actual.
2. Reemplaza el Custom Code del bloque 1 por short/healthcare/block1.html.
3. Reemplaza el Custom Code del bloque 2 por short/healthcare/block2.html.
4. Publica. Bajo el título deben verse dos etiquetas blancas: "HIPAA-trained" y "Ongoing HR support from Orchid".

PARTE 1 · Variante B de salud
1. Sites → Funnels → funnel de hire-50off → paso "BF Healthcare" (path practices-free-month).
2. Crea una variante de split test ("Create Variation" / "Split Test") desde página en blanco. Nómbrala "B · Larga".
3. Arma la variante B con 3 secciones:
   - Sección 1: ancho completo, padding y márgenes en 0. Dentro va un Custom Code con long_designs/healthcare/block1_widget.html. Trae todos los estilos, las imágenes y la cuenta regresiva.
   - Sección 2: fondo #3F1D82. Una fila con 2 columnas:
     - Columna izquierda: Custom Code con long_designs/healthcare/block2_form_column.html.
     - Columna derecha: el MISMO formulario "Orchid · BF Healthcare" que usa la variante A.
   - Sección 3: ancho completo, padding y márgenes en 0. Dentro va un Custom Code con long_designs/healthcare/block3_footer.html (pie de página).
4. Ajustes de la página B:
   - Copia de la variante A el código de seguimiento, exactamente igual (píxel 2271987886986577, solo PageView).
   - Copia de A el título y la descripción SEO.
   - El formulario debe llevar a la misma página de gracias que A: practices-free-month-thanks.
5. Si GHL no deja guardar el bloque 1 porque es muy grande (pesa unos 600 KB por las imágenes incrustadas), usa la versión liviana:
   a. Sube a Media Library las 7 imágenes de long_designs/healthcare/images/ (healthcare_img1.png a healthcare_img7.jpg). En GitHub, abre cada una y usa "Download".
   b. En lugar de block1_widget.html, usa long_designs/healthcare/block1_widget_light.html.
   c. Reemplaza en ese código cada marcador __IMG1__ … __IMG7__ por la URL de Media Library de la imagen con el mismo número.
6. Reparto de tráfico: 50% A / 50% B. Publica la prueba.
7. Abre https://go.orchidpros.com/practices-free-month varias veces en ventana de incógnito hasta que te salga la variante B. Confirma:
   - Carga completa y se ven todas las imágenes.
   - La barra dice "Offer ends Dec 1 at 11:59 PM (ET)" y la cuenta regresiva marca días/horas/minutos hasta el 1 de diciembre.
   - Los botones bajan al formulario.
   - La URL termina con "lp_variant=long".
   - Cómo se ve en celular (vista móvil del editor o ventana angosta).

PARTE 2 · Variante B de emprendedores
Es igual a la Parte 1, con estos cambios:
- Paso "BF Entrepreneurs" (business-free-month).
- Código de long_designs/entrepreneurs/block1-3.
- Formulario "Orchid · BF Entrepreneurs".
- Página de gracias business-free-month-thanks.
- Si hace falta la versión liviana, usa las imágenes de long_designs/entrepreneurs/images/.

AL TERMINAR, dime:
- Si las dos pruebas quedaron activas al 50/50.
- Si usaste la versión completa o la liviana en cada una.
- Si viste la variante B en cada URL y si la URL mostró lp_variant=long.
- Dónde muestra GHL las estadísticas de la prueba (vistas y conversiones por variante).
- Cualquier paso que no coincidió.
