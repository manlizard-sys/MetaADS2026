# Guía del informe semanal para los dueños de Orchid

Lo lee la dirección de Orchid, no un especialista en anuncios. Debe entenderse en 3 minutos y decir con claridad qué pasó, por qué y qué sigue.

## Reglas

- Español claro, frases cortas, sin jerga. Si hace falta un término (CPL, CTR), se explica la primera vez entre paréntesis.
- **La métrica principal es el lead calificado**: alguien que en GHL respondió "I want to hire." (no tiene la etiqueta `job-seeker`). El "lead" que cuenta Meta va aparte, como dato secundario.
- Semana = lunes a domingo, en hora de Nueva York (zona de la cuenta). El informe sale el lunes siguiente.
- Solo cifras de los scripts (`analytics.py`, `weekly_report.py`, `ghl.py`) y de `build/CHANGELOG_META.md`. Nada inventado. Si falta un dato, se dice que falta.
- Cada cambio de la semana se cuenta con su motivo y con lo que se espera que produzca.

## Estructura

1. **Título**: "Informe Meta Ads Orchid – Semana del <lunes> al <domingo>".
2. **Resumen en 3 líneas**: inversión, leads calificados, costo por lead calificado y una frase sobre si la semana fue mejor o peor que la anterior y por qué.
3. **Números de la semana** (tabla contra la semana anterior): inversión, impresiones, clics, visitas a la landing, leads en Meta, leads en GHL, leads calificados (quieren contratar), buscadores de empleo, llamadas agendadas, costo por lead calificado.
4. **Qué hicimos esta semana y por qué** (de `CHANGELOG_META.md`): una línea por cambio.
5. **Qué aprendimos**: 2–4 puntos. Qué anuncio, audiencia o mensaje trajo compradores reales y cuál no.
6. **Anuncios**: una ficha por anuncio con su **captura** (como se ve en el feed del celular), y debajo inversión, leads calificados, buscadores de empleo y estado (activo/pausado). Primero los activos, luego los que gastaron en la semana. Las capturas salen de `python3 scripts/ad_previews.py --days 7` (carpeta `build/reports/previews/<fecha>/`, con `index.json` que dice qué imagen es de qué anuncio). Cada vez que el informe mencione un anuncio por su nombre (V2, S8…), el lector debe poder ubicar su captura.
7. **Plan para la próxima semana**: 3 acciones concretas como máximo.
8. **Decisiones que necesitamos de ustedes**: si no hay ninguna, decirlo.

## Archivos

- Las capturas se suben al documento (o al Artifact) junto al informe; no se guardan en git.
- Copia del informe en `build/reports/informes/<lunes-de-entrega>.md`.
- Si existe el tipo de documento Claude Docs, el informe se publica como documento para que los dueños puedan comentarlo y exportarlo a PDF. Si no existe, se publica como página (Artifact).
