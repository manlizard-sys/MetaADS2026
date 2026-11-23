En GHL hay que reemplazar un parche en la variante "B · Larga" de dos landings de Orchid. La versión anterior no oculta la barra roja fija porque corre antes de que GHL dibuje el formulario. No toques nada más: ni la variante A, ni el reparto 50/50, ni Meta. No hagas envíos de formulario.

1. Funnel "Orchid - Hire a VA" → paso "BF Healthcare" → variante "B · Larga" (página MqIOQ8wLuRHrqYTuBi8N) → Custom Code del bloque 1.
2. Al final está el parche anterior (líneas ~886–903). Empieza con "<!-- Orchid · arreglos de formulario para la variante" y termina con "</script>". Bórralo completo, de ese comentario hasta su </script>. No borres nada más.
3. En su lugar pega TODO el contenido de https://github.com/manlizard-sys/metaads2026/blob/claude/admiring-franklin-wrfknt/build/landings/long_designs/form_ux_patch.html (botón "Raw"). Empieza con "<!-- v2 · Orchid · arreglos". Guarda y publica.
4. Repite los pasos 1–3 en "BF Entrepreneurs" → variante "B · Larga" (página WULGDyew7eTJjueLQlC7); ahí el parche anterior está en las líneas ~787–804.
5. Comprueba en vista de celular https://go.orchidpros.com/practices-free-month-page-865761 y https://go.orchidpros.com/business-free-month-page:
   - arriba de la página la barra roja "Get Started Free" se ve;
   - al llegar al formulario (desde el primer menú hasta el botón) la barra desaparece;
   - al volver a subir, reaparece;
   - el texto del botón "Book My Free Call" se ve violeta.

Al terminar, dime si quedó en las dos y si la barra se oculta y reaparece como se describe.
