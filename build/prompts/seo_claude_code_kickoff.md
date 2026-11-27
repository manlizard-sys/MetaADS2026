Arranquemos el SEO de Orchid (Google y Bing) desde este repo. Trabaja en la rama actual, guarda todo en `seo/` y haz commit y push al terminar cada paso. Respóndeme en español; el contenido del sitio va en inglés de EE. UU.

## Contexto (no lo vuelvas a preguntar)
- Lee primero `build/prompts/seo_kickoff_dic2026.md` (empresa, mercados, diferenciadores, competidores y reglas) y `build/research/competencia/` (capturas y PDF de competidores).
- Sitio: https://orchidpros.com, WordPress con Yoast. Sitemap: https://orchidpros.com/sitemap_index.xml. API pública de WordPress: https://orchidpros.com/wp-json/wp/v2/ (pages, posts).
- Landings de anuncios en GoHighLevel: https://go.orchidpros.com (su robots.txt está vacío). Ver `build/landings/` y `build/CHANGELOG_META.md`.
- Conexiones disponibles (usa las que existan en esta sesión; si falta alguna, dilo y sigue con lo demás):
  - Search Console, GA4 y Business Profile: por el conector de datos de marketing (Windsor.ai o similar) si está conectado.
  - Palabras clave y competencia: conector Semrush, Ahrefs u OpenSEO si está conectado. Si no hay ninguno, NO inventes volúmenes: marca "sin dato" y dime cómo obtenerlo.
  - PageSpeed Insights: llave de Google en la variable de entorno PAGESPEED_API_KEY (pásala como ?key=; no la imprimas nunca). Sin llave, la cuota pública suele estar agotada.
  - WordPress: solo lectura por la API pública. Para publicar hará falta una Application Password guardada como secreto de red para orchidpros.com; no publiques nada sin mi aprobación.
  - Bing: sin API por ahora. Dame los pasos para importar desde Search Console y activar IndexNow con Yoast.

## Paso 1 · Auditoría técnica (scripts en `scripts/seo/`, resultados en `seo/audit/`)
1. Rastrea todas las URLs del sitemap. Por cada una: código HTTP, redirecciones, canonical, meta robots, título (longitud), meta descripción (longitud), H1 (cuántos y texto), número de palabras, enlaces internos salientes y entrantes, imágenes sin alt, datos estructurados (tipos de schema).
2. PageSpeed Insights (celular y escritorio) de la home y de las 5 páginas más importantes: puntajes y Core Web Vitals.
3. go.orchidpros.com: lista qué páginas existen (landings, gracias, book-a-call, brief) y si tienen noindex. Recomiéndame qué debería ser noindex; no lo cambies.
4. Si hay Search Console: páginas indexadas, no indexadas y por qué, consultas y páginas con más impresiones de los últimos 3 meses.
5. Entrega `seo/audit/auditoria.md` con los problemas priorizados (crítico / importante / menor), el arreglo de cada uno y quién lo hace (yo en WordPress, diseño o desarrollo), más un CSV con el detalle por URL.

## Paso 2 · Palabras clave y competencia (`seo/keywords/`)
- Grupos por mercado e intención (salud, pequeñas empresas, abogados, contadores, bienes raíces; informativa, comparativa, comercial), para EE. UU. y Canadá aparte.
- Por grupo: palabras, volumen y dificultad con su fuente, intención, quién rankea hoy (de nuestra lista de competidores) y la página de Orchid que debería posicionar (existente o nueva).
- Brechas: temas y tipos de página que traen tráfico a la competencia (precios, "alternatives to", comparativas, calculadoras, guías por industria).

## Paso 3 · Plan (`seo/plan.md`)
- Mapa de palabras clave → páginas (arquitectura del sitio).
- Plan de 90 días por semana, desde el 7 de diciembre de 2026, priorizado por impacto en leads.
- Brief completo de las 3 primeras páginas: título SEO, meta descripción, slug, H1, secciones, FAQ, schema sugerido y enlaces internos.
- KPIs mensuales y cómo se miden (Search Console, GA4, leads orgánicos y citas en GoHighLevel con utm_source=organic o referrer).
- Visibilidad en buscadores con IA (Bing Copilot, ChatGPT, Google AI Overviews): acciones concretas.

## Reglas
- Nada inventado. Todo dato de terceros con su fuente.
- Nunca reseñas falsas. "HIPAA-trained", no "HIPAA-compliant". Precio "desde $15/hora". Dirección: P.O. Box 463, Rutherford, NJ 07070 (no sirve para Google Business Profile; dime las opciones reales).
- No cambies nada en WordPress, GoHighLevel, Search Console, Bing ni Meta sin mi aprobación.
- No imprimas llaves ni contraseñas en el chat, archivos, logs ni commits.
- Al final de cada paso: resumen corto en español y las preguntas que necesitas que responda.
