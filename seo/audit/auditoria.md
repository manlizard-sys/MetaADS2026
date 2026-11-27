# Auditoría técnica SEO · orchidpros.com

Fecha del rastreo: 27 nov 2026. Solo lectura: no se cambió nada en WordPress, GoHighLevel ni ningún otro sistema.

**Cómo se hizo**
- `scripts/seo/crawl.mjs`: rastrea las 21 URLs del sitemap de Yoast y las 20 páginas publicadas de la API de WordPress (no hay entradas de blog), más los enlaces internos que apuntan fuera de ese grupo.
- `scripts/seo/ghl_pages.mjs`: revisa las páginas de go.orchidpros.com citadas en este repo.
- `scripts/seo/pagespeed.mjs`: PageSpeed Insights de 6 páginas.

**Archivos de detalle**
- [`urls.csv`](urls.csv): una fila por URL con código, canonical, robots, título, descripción, H1, palabras, enlaces, imágenes y schema.
- [`links_not_in_sitemap.csv`](links_not_in_sitemap.csv): enlaces internos rotos o con redirección.
- [`ghl_pages.csv`](ghl_pages.csv): páginas de GoHighLevel.
- [`crawl.json`](crawl.json): datos completos del rastreo.
- [`pagespeed.csv`](pagespeed.csv): por ahora solo trae errores; ver sección 3.

**Quién hace cada arreglo:** **Tú** = tú en WordPress/Yoast o en GoHighLevel, sin código. **Diseño** = cambia el aspecto o el texto de la página. **Desarrollo** = plantilla, plugins, código o rendimiento.

---

## 1. Resumen

La base técnica está sana:
- HTTPS en todo el sitio, con redirecciones 301 de `http` y de `www` hacia la versión correcta.
- Un 404 real cuando la página no existe.
- `robots.txt` abierto y con el sitemap declarado.
- Canonical propio en todas las páginas, todas indexables y todas en `lang="en-US"`.

**Los problemas que importan están en el contenido y en la estructura, no en el servidor:**
1. **La página de salud, que es el mercado prioritario, está mal configurada.** Usa el título y la meta descripción de la página de abogados, no está en el menú y no dice HIPAA-trained, ni el precio, ni Colombia o el mismo horario.
2. **El sitio todavía se presenta como "for Law Firms & Real Estate".** Eso sale en el título de 10 páginas, en el schema del sitio y en `llms.txt`.
3. **Hay enlaces rotos en la home y en la página de bienes raíces.** En bienes raíces, uno de ellos es probablemente un botón de contacto.
4. **Las landings de anuncios de go.orchidpros.com son indexables.** Dos de ellas son copias exactas, y las de Black Friday vencen el 1 de diciembre.
5. **No hay contenido informativo:** 0 entradas de blog. Tampoco hay schema de servicio, FAQ ni de los fundadores.

---

## 2. Problemas priorizados

### Crítico (esta semana)

| # | Problema | Evidencia | Arreglo | Quién |
|---|---|---|---|---|
| C1 | **Salud y Marketing tienen el título y la descripción de la página de abogados** | `/solutions/healthcare/` y `/solutions/marketing-creative/` muestran "Legal Outsourcing & Bilingual Paralegals for Law Firms \| Orchid" y "Scale your practice with vetted bilingual paralegals…". Google muestra ese texto en los resultados. | En cada página: Yoast → pestaña SEO → "SEO title" y "Meta description". Propuesta para salud: título `Bilingual Medical Virtual Assistants, HIPAA-Trained \| Orchid` y descripción `Hire a dedicated, HIPAA-trained medical virtual assistant from Colombia. English and Spanish, working your hours. From $15/hour. Book a free call.` (es la misma del brief 1 en `seo/plan.md`). | Tú |
| C2 | **Enlaces internos rotos (404)** | La home y el pie de página enlazan `/operations-administration/` y `/technology-data/`, que dan 404. En `/real-estate/` hay un enlace a `orchidpros.com/contact/` sin `https://`, que lleva a `/real-estate/orchidpros.com/contact/` (404). | En Elementor: corregir el botón de bienes raíces a `https://orchidpros.com/contact/`. Quitar las dos tarjetas de la home o apuntarlas a páginas que existan. | Tú |
| C3 | **La página de salud no está en el menú y le llega un solo enlace, con redirección** | El menú "Industries" lista Law Firm, Real Estate y Other professionals. La home enlaza `/healthcare/`, que hace 301 a `/solutions/healthcare/`. Ninguna página del sitio enlaza directo a la URL final. | Agregar "Healthcare" al menú (Apariencia → Menús, o el header de Elementor). Cambiar los enlaces de la home a `/solutions/healthcare/` y `/solutions/marketing-creative/`. | Tú |
| C4 | **El nombre del sitio dice "for Law Firms & Real Estate"** | Es el sufijo de 10 títulos (por ejemplo, "FAQ - Orchid – Ethical Outsourcing for Law Firms & Real Estate"). También sale en la descripción del schema WebSite y en `llms.txt`, que es lo que leen los buscadores con IA. | Ajustes → Generales → "Descripción corta" (tagline) y Yoast → Ajustes → Site basics. Propuesta: `Bilingual Remote Staff from Colombia`. Dejar el separador de título en `\|`. | Tú |
| C5 | **La página de salud no usa los diferenciadores** | Su texto no dice HIPAA-trained, "desde $15/hora", Colombia ni el mismo horario de EE. UU. Tiene 431 palabras de contenido, solo 3 preguntas frecuentes y errores de ortografía ("commiting", "proffesionals"). | Reescribirla con el brief del Paso 3. Mientras tanto, corregir los errores de ortografía. | Diseño (texto), Tú (publicar) |
| C6 | **El FAQ contradice la oferta "$0 to begin"** | `/frequently-asked-questions/` dice "We do charge a one-time setup fee" y explica qué incluye. La página de salud dice "$0 to begin", y en la práctica nunca se cobra (confirmado el 27 nov 2026). | Reescribir las dos respuestas del FAQ ("Are there any hidden fees?" y "What is included in the setup fee?") con "No setup fee: $0 to begin". Lo que hoy describe la cuota (selección, verificación, incorporación) pasa a "What's included". | Tú |
| C7 | **No hay Google Analytics (GA4) en ninguno de los dos sitios** | Revisado el 27 nov 2026: el HTML de orchidpros.com (WordPress) no tiene ninguna etiqueta `G-…` ni de Google Tag Manager. Las páginas de go.orchidpros.com (GoHighLevel) solo tienen el píxel de Meta. Sin GA4 no se puede medir el tráfico orgánico ni de dónde vienen los leads. | Instalar la misma propiedad GA4 en los dos dominios, con dominios cruzados. Pasos en la sección 4 de `seo/plan.md`. | Tú |

### Importante (próximas 2–4 semanas)

| # | Problema | Evidencia | Arreglo | Quién |
|---|---|---|---|---|
| I1 | **Landings de anuncios indexables y duplicadas** | Ninguna página de go.orchidpros.com tiene `noindex` (ver sección 4). `practices-free-month` y `practices-free-month-page-865761` son idénticas (2,301 palabras). Las de Black Friday vencen el 1 dic. | Poner noindex como en la sección 4. Necesita tu aprobación. | Tú (GHL) |
| I2 | **9 páginas sin meta descripción** | cookie-policy, frequently-asked-questions, privacy-policy-2, guillermo-enmovimiento, solutions, iwill-orchid, interview-scorecard, attorney-calculator y terms-and-conditions. | Escribir una descripción de 120–155 caracteres en Yoast para FAQ, solutions, interview-scorecard y las calculadoras. Las páginas legales pueden quedar sin descripción. | Tú |
| I3 | **12 títulos pasan de 60 caracteres** | Van de 62 a 85 caracteres y Google los corta. En 9 la causa es el sufijo de C4; los otros 3 son los títulos copiados de C1. | Se corrige con C4 y C1. Revisar después en `urls.csv` (columna `title_len`). | Tú |
| I4 | **Faltan H1 en páginas clave** | About, FAQ y las 3 páginas legales tienen 0 H1. La home usa "Buy Your Time Back", que no dice qué vende Orchid. | About: H1 `About Orchid: Bilingual Remote Staffing from Colombia`. FAQ: `Orchid FAQ: Hiring Remote Bilingual Staff`. En Elementor, cambiar la etiqueta del encabezado principal a H1. Para la home, ver el brief del Paso 3. | Tú |
| I5 | **Schema mínimo** | Solo hay el schema por defecto de Yoast (Organization, WebSite, WebPage y BreadcrumbList). No hay Service, FAQPage ni Person para los fundadores. Organization no tiene teléfono, email, fundadores ni área de servicio. | Organization con `founder`, `contactPoint` (+1 973-283-5923, info@orchidpros.com) y `areaServed` US/CA. `Service` en cada página de mercado. `FAQPage` en `/frequently-asked-questions/`; ojo: Google ya casi no muestra FAQ enriquecidos, sirve sobre todo para Bing y la IA. `Person` en About. Se hace con un widget HTML de Elementor por página que lleva el bloque JSON-LD, sin plugins pagos; el plan (`seo/plan.md`) trae el JSON listo. | Desarrollo |
| I6 | **El sitemap y llms.txt incluyen el pie de página de Elementor** | `/elementor-hf/footer/` está en el sitemap (`elementor-hf-sitemap.xml`) y en `llms.txt`, y hace 301 a la home. | Yoast → Ajustes → Content types → "Elementor Header & Footer" → "Show in search results" en **off**. | Tú |
| I7 | **llms.txt incompleto y desactualizado** | Lista solo 5 páginas (Work with us, Home, Terms, Healthcare, Marketing) y dice "for Law Firms & Real Estate". | Yoast → Site features → llms.txt → elegir las páginas a mano: home, healthcare, law-firm, real-estate, other-professionals, about, FAQ y contact. Se actualiza solo con C4. | Tú |
| I8 | **Dos calculadoras de abogados duplicadas y huérfanas** | `/attorney-calculator/` y `/attorney-income-calculator/` hacen lo mismo y no reciben ningún enlace interno. | Quedarse con `/attorney-income-calculator/`, que tiene título y descripción. Hacer 301 de la otra con el plugin gratuito Redirection, y enlazarla desde `/law-firm/`. | Tú |
| I9 | **Páginas huérfanas e indexables** | `guillermo-enmovimiento`, `iwill-orchid` e `interview-scorecard` no reciben ningún enlace del sitio. | Si las dos primeras son de alianzas o campañas, ponerles noindex en Yoast → Avanzado. `interview-scorecard` es un recurso útil: enlazarla desde About o desde una guía. | Tú |
| I10 | **Datos de contacto y de marca inconsistentes** | El pie de página dice "proffesionals with law and real estate teams" y el horario "Mon–Tues… Fri" no incluye miércoles ni jueves. En el schema, Instagram es `instagram.com/orchid.pros`, pero el brief dice `@orchidpros.staffing`. La foto de los fundadores dice "Andrea and Josue Bolanos" (el apellido es Barros). En About aparece "and and pending admissi…". | Corregir el pie de página y la descripción de la foto. En Yoast → Ajustes → Site representation, cambiar Instagram a `https://www.instagram.com/orchidpros.staffing/` (el correcto, confirmado el 27 nov 2026) y usar ese usuario en todas partes. | Tú |
| I11 | **Velocidad sin medir; la home es pesada** | PageSpeed falló: cuota pública agotada. Indicadores del HTML de la home: 342 KB de HTML, 17 scripts, 35 hojas de estilo, 101 KB de CSS en línea y 58 imágenes. El servidor responde rápido (~180 ms). | Medir con la llave (sección 3). Los arreglos típicos en Elementor y Astra son cargar solo los recursos que se usan, posponer el JavaScript, convertir imágenes a WebP con medidas fijas y precargar la imagen principal. | Desarrollo |
| I12 | **No hay contenido informativo** | 0 entradas en `/wp-json/wp/v2/posts`. The Delegate Brief solo vive en GHL. | Ver el plan del Paso 3: guías por industria, comparativas y archivo del newsletter. | Diseño / Tú |
| I13 | **Páginas para candidatos mezcladas con las de clientes** | `/work-with-us/` tiene título y descripción en español ("¿Buscás…? Postulate"), pero H1 en inglés y `lang=en-US`. Esto, más Orchid Academy, atrae a quien busca empleo, el mismo problema de calidad de leads que hubo en Meta. | Escribir todo en un solo idioma por página: español neutro para Colombia ("¿Buscas…? Postúlate"). Si queda en español, cambiar el `lang` de esa página. No enlazar estas páginas desde las de clientes, salvo desde el menú. | Tú / Desarrollo |

### Menor

| # | Problema | Arreglo | Quién |
|---|---|---|---|
| M1 | Falta la imagen para redes (og:image) en 15 de 20 páginas | Yoast → Ajustes → Site basics → imagen por defecto para compartir | Tú |
| M2 | Error de ortografía en la meta descripción de la home: "Ethical oursourcing" | Reescribirla; el brief del Paso 3 trae la versión nueva | Tú |
| M3 | `http://www` hace 2 saltos antes de llegar (http→https www→https) | Opcional: una sola regla 301 en el hosting | Desarrollo |
| M4 | 172 de 285 imágenes con `alt=""` vacío (ninguna sin el atributo) | Las decorativas pueden quedar así. Las fotos del equipo, los logos de clientes y las capturas de proceso necesitan texto alternativo descriptivo. La lista por página está en `crawl.json` (`_img_missing`). | Tú |
| M5 | Varias landings de GHL no tienen `<title>` (hire, hire-form, hire-50off, 50off-form y las de gracias) | En la configuración SEO de cada página de GHL. No afecta los anuncios, pero sí cómo se ven al compartirlas. | Tú (GHL) |
| M6 | La raíz `go.orchidpros.com/` da 404 | Opcional: redirigirla a https://orchidpros.com | Tú (GHL) |

---

## 3. PageSpeed Insights (celular y escritorio)

**Estado: sin datos.** La variable `PAGESPEED_API_KEY` no existe en este equipo, y la cuota pública respondió `HTTP 429 Quota exceeded` en las 12 pruebas: home, healthcare, law-firm, other-professionals, real-estate y about, cada una en celular y escritorio.

Para medir:
1. Crea la llave en Google Cloud: activa la API "PageSpeed Insights API" y ve a Credenciales → Crear llave de API. Restríngela a esa API.
2. Guárdala sin pegarla en el chat. Abre el archivo `.env` de la carpeta del repo con el Bloc de notas (si no existe, créalo con "Todos los archivos (\*.\*)" como en `GUIA_WINDOWS.md`) y agrega una línea: `PAGESPEED_API_KEY=tu_llave`. `.env` está en `.gitignore`, así que nunca se sube a GitHub.
3. Corre `node scripts/seo/pagespeed.mjs`, o pídeme que lo corra. Llena `pagespeed.csv` con puntajes, LCP, CLS, TBT y datos de campo (CrUX) si hay suficiente tráfico. La llave nunca se imprime ni se guarda.

Si prefieres no crear la llave, corre las 6 URLs a mano en https://pagespeed.web.dev y pásame las capturas.

---

## 4. go.orchidpros.com (GoHighLevel)

`robots.txt` vacío, y `sitemap.xml` responde 200 pero sin ninguna URL. Ninguna página tiene `noindex` ni `X-Robots-Tag`. Detalle en [`ghl_pages.csv`](ghl_pages.csv).

| Página | Qué es | Palabras | ¿noindex hoy? | Recomendación |
|---|---|---|---|---|
| /hire | landing de Meta (oct) | 493 | No | **noindex** |
| /hire-form | solo formulario | 94 | No | **noindex** |
| /hire-50off | oferta 50% (nov) | 1,429 | No | **noindex** |
| /50off-form | solo formulario 50% | 1,477 | No | **noindex** |
| /practices-free-month | BF salud | 2,301 | No | **noindex** (vence el 1 dic y repite el contenido de la página de salud) |
| /practices-free-month-page-865761 | copia exacta de la anterior | 2,301 | No | **noindex** o borrarla si ya no se usa |
| /business-free-month | BF emprendedores | 447 | No | **noindex** |
| /business-free-month-page | variante larga | 1,548 | No | **noindex** |
| /practices-free-month-thanks, /business-free-month-thanks, /book-a-call-thanks, /brief-thanks | páginas de gracias | 33–186 | No | **noindex, nofollow**. Además, si se indexan, entran visitas sin conversión que ensucian la medición. |
| /book-a-call | agendar llamada | 325 | No | **noindex**. La página para buscadores debe ser `/contact/` en el sitio principal. |
| /brief | registro a The Delegate Brief | 301 | No | **noindex** aquí, y crear `orchidpros.com/the-delegate-brief/` en WordPress con el formulario incrustado y el archivo de ediciones (contenido que sí posiciona). |

**Cómo hacerlo en GHL, cuando lo apruebes:** en cada página, Settings → Tracking Code → Head, pegar:
```html
<meta name="robots" content="noindex, nofollow">
```
Si tu versión de GHL tiene la opción en Page Settings → SEO, úsala. **No uses `Disallow` en robots.txt:** si Google no puede rastrear la página, tampoco ve el noindex. El noindex no afecta los anuncios de Meta ni su píxel.

---

## 5. Search Console, Bing y Business Profile

### Search Console (Paso 1.4): sin datos
En esta sesión no hay ningún conector de datos de marketing (Windsor.ai u otro), así que no tengo páginas indexadas, motivos de exclusión ni consultas. Dos formas de conseguirlos:
- **Conectar Windsor.ai** (o similar) a esta app con Search Console, GA4 y Business Profile. Así saco el informe en la próxima sesión.
- **Exportar a mano** desde search.google.com/search-console, propiedad `orchidpros.com` (si no existe, créala como "Dominio", verificada por DNS):
  - Rendimiento → últimos 3 meses → Exportar → CSV. Trae consultas y páginas.
  - Indexación → Páginas: captura de "Por qué las páginas no se indexan", con cada motivo abierto.
  - Guarda los archivos en `seo/audit/gsc/` y yo los analizo.

Revisa también que la propiedad tenga el sitemap enviado: Sitemaps → `https://orchidpros.com/sitemap_index.xml`.

### Bing Webmaster Tools (sin API)
1. Entra a https://www.bing.com/webmasters con una cuenta Microsoft o Google.
2. Elige **Import from Google Search Console**, autoriza y selecciona `orchidpros.com`. Importa el sitio verificado y los sitemaps.
3. Revisa Sitemaps: debe aparecer `sitemap_index.xml`. Si no, agrégalo.
4. **IndexNow** (avisa a Bing y a Yandex cada vez que publicas o cambias una página). No hace falta pagar Yoast Premium:
   - Instala el plugin gratuito oficial **"IndexNow"** de Microsoft Bing desde Plugins → Añadir nuevo. Él genera y aloja la llave solo.
   - Si algún día activas Yoast Premium, que trae su propio IndexNow, desactiva uno de los dos: no conviene tener dos integraciones a la vez.
   - Para confirmar: en Bing Webmaster → IndexNow, en 1–2 días deben aparecer URLs enviadas.
5. En Bing Webmaster → Site Explorer y URL Inspection, confirma que no haya URLs de go.orchidpros.com.

### Google Business Profile y Bing Places
Google no acepta apartados postales (P.O. Box) ni oficinas virtuales sin personal como dirección. Además, exige que el negocio tenga **contacto en persona** con los clientes, en un local o yendo hasta ellos. Un servicio 100% remoto en principio no es elegible. El brief dice que ya hay 4 reseñas en Google, así que **ya existe un perfil**: revisa qué dirección usa y de qué tipo es. Las opciones reales son tres:

1. **Negocio de área de servicio, con la dirección oculta.** Solo si de verdad atienden en persona (por ejemplo, visitas a consultorios o firmas en NJ y NY). La dirección de verificación tiene que ser real, como la casa u oficina de un socio, y no se muestra. El área de servicio serían los estados o ciudades que visitan.
2. **Oficina real con personal en horario de atención.** Por ejemplo, la oficina en Colombia, si existe, con su propio perfil en Colombia. No sirve para búsquedas locales de EE. UU.
3. **No tener perfil local** y construir la entidad de la marca de otra forma: schema Organization completo, LinkedIn, Crunchbase, Clutch o G2 con reseñas reales y el Knowledge Panel. Es lo más seguro si no hay atención en persona.

**Decisión (27 nov 2026):** Orchid es 100% virtual y su única dirección es el P.O. Box. Eso deja solo la **opción 3**:
- No invertir en el perfil de Google ni en Bing Places, y no editar la dirección del perfil actual: el cambio dispara una verificación que no se puede pasar con un P.O. Box. Hay que saber que el perfil puede ser suspendido en cualquier momento por no cumplir las reglas, y con él se perderían las 4 reseñas.
- Las reseñas nuevas se piden en Clutch o G2, que aceptan negocios remotos.
- La "presencia de marca" se construye con el schema Organization, LinkedIn y las menciones de terceros (sección 5 del plan).

---

## 6. Inventario rápido

| URL | Rol | Palabras* | Enlaces entrantes desde contenido** | Comentario |
|---|---|---|---|---|
| / | home | 1,415 | — | H1 genérico; enlaza 2 URLs rotas |
| /solutions/healthcare/ | salud | 431 | 0 | ver C1, C3 y C5 |
| /law-firm/ | abogados | 690 | 3 | la mejor configurada |
| /real-estate/ | bienes raíces | 458 | 3 | enlace roto a contact (C2) |
| /other-professionals/ | pymes, contadores y otros | 212 | 1 | contenido muy corto para pymes, contadores y finanzas |
| /solutions/marketing-creative/ | marketing | 410 | 0 | ver C1 |
| /solutions/ | índice de soluciones | 247 | 0 | sin meta descripción |
| /about/ | fundadores | 771 | 0 | sin H1, sin schema Person |
| /frequently-asked-questions/ | FAQ | 881 | 0 | 14 preguntas; sin H1, sin FAQPage |
| /contact/ | contacto | 129 | 1 | ok |
| /attorney-income-calculator/, /attorney-calculator/ | calculadoras | 315 / 250 | 0 | duplicadas (I8) |
| /interview-scorecard/ | recurso | 229 | 0 | huérfana |
| /orchid-academy/, /work-with-us/ | candidatos | 96 / 843 | 0 | separar de las páginas de clientes (I13) |
| /guillermo-enmovimiento/, /iwill-orchid/ | alianzas o campañas | 574 / 652 | 0 | huérfanas (I9) |

\* Palabras sin contar el encabezado ni el pie del sitio.
\** Enlaces desde el cuerpo de otras páginas, sin contar el menú ni el pie, que enlazan casi todo.
