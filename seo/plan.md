# Plan SEO de Orchid · 90 días (7 dic 2026 – 7 mar 2027)

Se basa en [`audit/auditoria.md`](audit/auditoria.md) (Paso 1) y [`keywords/keywords.md`](keywords/keywords.md) (Paso 2). La prioridad es por **impacto en leads**, no por volumen: primero lo que convierte (salud, precios, pymes), después lo que trae tráfico.

**Quién lo hace:** **Tú** = WordPress, Yoast o GHL sin código. **Diseño** = texto y aspecto de la página. **Desarrollo** = código, plugins o rendimiento.
Nada de esto se publica sin tu aprobación.

---

## 1. Arquitectura: mapa de palabras clave → páginas

```
orchidpros.com/
├── /                                   marca + "bilingual remote staff from Colombia"
├── /solutions/                         índice de mercados (enlaza a todos)
│   ├── /solutions/healthcare/          ★ medical virtual assistant, hire a medical VA, bilingual medical VA, HIPAA-trained VA
│   │   ├── /dental/                    virtual receptionist for dental office, dental virtual assistant
│   │   └── /chiropractic-physical-therapy/  chiropractic VA, physical therapy VA
│   ├── /solutions/small-business/      ★ virtual assistant for small business (hoy /other-professionals/ → 301)
│   ├── /solutions/accounting/          VA for accountants, CPA firm VA, tax season VA, remote bookkeeper
│   └── /solutions/marketing-creative/  (existente; corregir título)
├── /law-firm/                          VA for law firms, bilingual legal assistant (existente)
│   └── /law-firm/immigration/          immigration law firm VA, Spanish-speaking legal intake
├── /real-estate/                       real estate VA, real estate ISA, transaction coordinator (existente, ampliar)
├── /bilingual-virtual-assistant/       bilingual VA, Spanish-speaking VA (página de la propuesta central)
├── /ca/                                hire virtual assistant Canada, English-Spanish virtual assistant Canada (Canadá, en-CA)
├── /why-colombia/                      nearshore staffing Colombia, hire VA from Colombia, Colombian VA
├── /pricing/                           ★ virtual assistant pricing, medical VA cost
├── /tools/us-hire-vs-orchid-calculator/  cost of hiring an employee vs VA
├── /compare/
│   ├── colombia-vs-philippines-virtual-assistants/
│   ├── medical-virtual-assistant-companies/
│   └── orchid-vs-[competidor]/ y [competidor]-alternatives/ (de a una, con datos fechados)
├── /guides/
│   ├── hipaa-virtual-assistant/        HIPAA compliant VA (informativa, honesta)
│   └── virtual-assistant-cost/         how much does a VA cost
├── /about/                             fundadores, E-E-A-T (Person schema)
├── /how-we-select/                     selección humana, pruebas, reemplazo (E-E-A-T)
├── /the-delegate-brief/                archivo del newsletter + registro (hoy solo en GHL)
├── /frequently-asked-questions/        FAQ general (FAQPage)
├── /contact/
└── Candidatos (separados de clientes): /work-with-us/, /orchid-academy/
```
★ = las 3 primeras páginas, con brief completo en la sección 3.

**Enlaces internos, reglas fijas:**
- Cada página de mercado enlaza a `/pricing/`, a la calculadora, a `/about/` y a la cita.
- Cada subpágina enlaza a su página madre, y la madre a todas sus subpáginas.
- Cada comparativa y cada guía enlaza a la página de servicio que corresponde.
- Las páginas de candidatos no se enlazan desde el cuerpo de las páginas de clientes.

---

## 2. Plan por semana

| Semana | Fechas | Qué | Quién | Por qué ahora |
|---|---|---|---|---|
| 1 | 7–13 dic | **Arreglos críticos de la auditoría:** C1 (títulos de salud y marketing), C2 (enlaces 404), C3 (salud en el menú), C4 (tagline del sitio), C6 (quitar el "setup fee" del FAQ). **Configurar** Search Console (propiedad de dominio + sitemap), Bing Webmaster (importar desde GSC) e IndexNow. **Noindex** en las landings de GHL (con tu aprobación); las de Black Friday ya vencieron. Medir PageSpeed con la llave. | Tú | Es lo que más rinde por hora: hoy Google muestra a la página de salud como si fuera de abogados. |
| 1 | 7–13 dic | **Medición orgánica** (sección 4): script de fuente orgánica en los botones a GHL y canal de IA en GA4. | Desarrollo | Sin esto no se puede contar un solo lead orgánico. |
| 2 | 14–20 dic | **Publicar la página de salud nueva** (brief 1) con schema Service + FAQPage. Arreglos I2, I4, I6, I7 e I10. Pedir reseñas a clientes reales (ver sección 5). | Diseño + Tú | Mercado prioritario y el de la campaña de Meta. |
| 3 | 21–27 dic | Texto de **/pricing/** (brief 2) y especificación de la calculadora. Unificar calculadoras de abogados (I8). Noindex o enlaces de huérfanas (I9). | Diseño + Desarrollo | Semana de fiestas: trabajo de escritorio. |
| 4 | 28 dic – 3 ene | **Publicar /pricing/ y la calculadora.** Reescribir el FAQ con H1, respuestas cortas y FAQPage. | Desarrollo + Tú | Intención comercial alta; además sirve de destino para los anuncios. |
| 5 | 4–10 ene | **Publicar /solutions/small-business/** (brief 3), con 301 desde /other-professionals/. Crear **/the-delegate-brief/** con el archivo. **Publicar /ca/** (sección 8). | Diseño + Tú | Segundo mercado de Meta (emprendedores). Canadá arranca ya. |
| 6 | 11–17 ene | **/solutions/accounting/** (antes de la temporada de impuestos). **/about/** con fundadores, H1 y Person schema. **/how-we-select/**. | Diseño + Tú | Temporada de impuestos; E-E-A-T para todas las páginas. |
| 7 | 18–24 ene | **/solutions/healthcare/dental/**. Primer **caso de cliente** con números, si un cliente lo autoriza. | Diseño + Tú | Subnicho de salud con anuncios activos. |
| 8 | 25–31 ene | **/solutions/healthcare/chiropractic-physical-therapy/**. **/bilingual-virtual-assistant/**. | Diseño + Tú | |
| 9 | 1–7 feb | **/why-colombia/** y **/compare/colombia-vs-philippines-virtual-assistants/**. Mejoras de velocidad (I11). **Informe del mes 2.** | Diseño + Desarrollo | Comparativas: ahí hoy rankean Stealth Agents y VA Masters. |
| 10 | 8–14 feb | **/guides/hipaa-virtual-assistant/** y **/compare/medical-virtual-assistant-companies/** (honesta, con fuentes y fecha). | Diseño | Para las búsquedas informativas de salud. |
| 11 | 15–21 feb | **/law-firm/immigration/**. Actualizar /law-firm/ con enlaces a la calculadora. | Diseño + Tú | Mercado en pausa en Meta; el orgánico sigue sumando. |
| 12 | 22–28 feb | Ampliar **/real-estate/**. Primera **"Orchid vs [competidor]"**, empezando por uno de salud (Wing, HelloRache o MedVA), solo con datos públicos fechados. | Diseño + Tú | |
| 13 | 1–7 mar | **/guides/virtual-assistant-cost/**. **Revisión de 90 días:** qué páginas traen leads, qué ajustar y si Canadá necesita más páginas. Plan del siguiente trimestre. | Tú + Claude | |
| Cada 2 semanas | — | **The Delegate Brief → artículo en el sitio** (sección 6). | Tú | Contenido fresco sin escribir de cero. |
| Cada mes | 1.º de cada mes | Informe de KPIs (sección 4) y prueba de visibilidad en IA (sección 5). | Claude | |

Si el diseño no alcanza el ritmo, se mueven las semanas 10–13 y se mantienen las 1–6.

---

## 3. Brief de las 3 primeras páginas

Todo el texto para el sitio va en inglés de EE. UU. Los datos que hay que confirmar contigo están marcados **[CONFIRMAR]**.

### Brief 1 · Healthcare (reescritura)

| Campo | Valor |
|---|---|
| URL / slug | `/solutions/healthcare/` (**se mantiene**: ya existe y `/healthcare/` hace 301 a ella) |
| SEO title (≤60) | `Bilingual Medical Virtual Assistants, HIPAA-Trained \| Orchid` |
| Meta description (≤155) | `Hire a dedicated, HIPAA-trained medical virtual assistant from Colombia. English and Spanish, working your hours. From $15/hour. Book a free call.` |
| H1 | `Bilingual Medical Virtual Assistants for Your Practice` |
| Palabra clave principal | hire a medical virtual assistant |
| Secundarias | bilingual medical virtual assistant, HIPAA trained virtual assistant, medical virtual assistant services, remote medical receptionist, insurance verification virtual assistant |

**Secciones (H2), en orden**
1. **Hero.** Subtítulo: `Dedicated, HIPAA-trained remote staff from Colombia who speak English and Spanish and work your hours. From $15/hour.` Botón principal: `Book a free call` (a `go.orchidpros.com/book-a-call`). Secundario: `See pricing` (a `/pricing/`). Foto real de los fundadores o del equipo, no de banco.
2. **A real person, not a bot.** Dos frases: Orchid da una persona dedicada, no un software de IA. Distingue la página de los resultados de IA que dominan la búsqueda.
3. **What your medical virtual assistant can handle.** Los 6 roles actuales (billing & coding, insurance verification & prior authorization, scheduling & intake, virtual medical assistant & receptionist, revenue cycle & claims follow-up, bilingual patient communication), cada uno con 2–3 tareas. H3 por rol.
4. **Why practices choose Orchid.** Seis puntos:
   - Same business hours. Colombia está en hora del Este de EE. UU. en invierno y una hora atrás en verano, no 12 horas como Filipinas.
   - Bilingual English–Spanish.
   - HIPAA-trained.
   - HR support and coaching included.
   - Free replacement if it is not a fit.
   - People choose people (selección humana, no por IA).
5. **What HIPAA-trained means at Orchid.** Recuadro honesto, con datos del FAQ actual: capacitación en PHI, acceso por roles, acuerdos de confidencialidad y trabajo dentro de los sistemas y políticas de la práctica. **Orchid firma un Business Associate Agreement (BAA)** con la práctica (confirmado el 27 nov 2026). Se dice "HIPAA-trained" y "we sign a BAA"; nunca "HIPAA-compliant".
6. **By specialty.** Tarjetas con enlace a Dental, Chiropractic & Physical Therapy y, más adelante, otras especialidades.
7. **What it costs.** `From $15/hour.` Comparación: contratación local de tiempo completo ~$78k/año frente a ~$31k/año con Orchid. Fuente en pie de nota: BLS OEWS May 2025, SOC 43-6014 + BLS ECEC + SHRM cost-per-hire. Enlace a la calculadora. **`$0 to begin`**: no se cobra cuota de inicio. Hay que quitar del FAQ actual el "one-time setup fee" (ver C6 en la auditoría).
8. **How it works.** Los 3 pasos actuales, más el plazo: candidatos en 20 días hábiles (dato del FAQ actual).
9. **Meet the founders.** Andrea Bolaños (Co-Founder & COO) y Josué Barros, con foto, 2 líneas cada uno y enlace a `/about/`. Si hay video, incrustarlo.
10. **What practices say.** Solo reseñas reales y verificables (las 4 de Google, con permiso). Si no hay permiso, omitir la sección.
11. **FAQ** (ver abajo).
12. **CTA final:** `Book a free call` + `Get The Delegate Brief`.

**FAQ (H3 + respuesta de 40–60 palabras)**
1. What does a medical virtual assistant do?
2. Are Orchid assistants HIPAA-trained?
3. Do your assistants speak Spanish? (Sí: fluidez verificada en inglés y español.)
4. What hours do they work? (Las de la práctica; Colombia coincide con la hora del Este en invierno.)
5. How much does a medical virtual assistant cost? (Desde $15/hora; enlace a /pricing/.)
6. How fast can I start? (Candidatos en 20 días hábiles.)
7. What if the assistant isn't a good fit? (Reemplazo sin costo.)
8. Which EHR and practice software can they use? (Los que la práctica ya usa: el asistente trabaja dentro de sus sistemas, con el acceso que la práctica le da. No nombrar marcas de EHR.)
9. Do you sign a Business Associate Agreement (BAA)? (Sí.)

**Schema (JSON-LD, en un widget HTML de Elementor al final de la página; no hace falta Yoast Premium)**
```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Service",
      "@id": "https://orchidpros.com/solutions/healthcare/#service",
      "name": "Bilingual Medical Virtual Assistants",
      "serviceType": "Medical virtual assistant staffing",
      "description": "Dedicated, HIPAA-trained, English-Spanish bilingual remote staff from Colombia for U.S. healthcare practices.",
      "provider": { "@id": "https://orchidpros.com/#organization" },
      "areaServed": { "@type": "Country", "name": "United States" },
      "availableLanguage": ["English", "Spanish"],
      "offers": {
        "@type": "Offer",
        "priceCurrency": "USD",
        "priceSpecification": { "@type": "UnitPriceSpecification", "minPrice": 15, "priceCurrency": "USD", "unitCode": "HUR" }
      }
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        { "@type": "Question", "name": "Are Orchid assistants HIPAA-trained?", "acceptedAnswer": { "@type": "Answer", "text": "…(misma respuesta visible en la página)…" } }
      ]
    }
  ]
}
```
Yoast ya genera WebPage, Organization y BreadcrumbList. Las respuestas del FAQPage tienen que ser idénticas al texto visible.

**Enlaces internos**
- **Entrantes:** menú (Industries → Healthcare), home (tarjeta de industria, con la URL final y no `/healthcare/`), `/solutions/`, `/pricing/`, `/frequently-asked-questions/` (sección Healthcare), `/about/`, subpáginas de especialidad y artículos del Brief sobre salud.
- **Salientes:** `/pricing/`, `/tools/us-hire-vs-orchid-calculator/`, `/about/`, `/how-we-select/`, subpáginas de especialidad y la cita en GHL (con el parámetro de fuente de la sección 4).

---

### Brief 2 · Pricing + calculadora

| Campo | Valor |
|---|---|
| URL / slug | `/pricing/` (nueva) + `/tools/us-hire-vs-orchid-calculator/` (nueva; también puede ir dentro de /pricing/) |
| SEO title | `Orchid Pricing: Bilingual Remote Staff From $15/Hour` |
| Meta description | `What a dedicated bilingual assistant from Colombia costs: from $15/hour, with recruiting, HR support and free replacement. Compare with a U.S. hire.` |
| H1 | `Simple Pricing for Dedicated Bilingual Staff` |
| Palabra clave principal | virtual assistant pricing |
| Secundarias | how much does a virtual assistant cost, medical virtual assistant cost, cost of hiring an employee vs virtual assistant |

**Secciones**
1. **Starting rate:** `From $15/hour` en grande. Una frase sobre de qué depende el precio: rol, horas y experiencia **[CONFIRMAR los factores reales y si hay tarifas por rol que quieras publicar]**.
2. **What's included.** Lista tomada de la página actual de salud y del FAQ: recruiting and verification, background screening, onboarding, HR support and coaching, time and accountability tools, replacement protection, business email, phone number and Google Workspace.
3. **`$0 to begin`.** No se cobra cuota de inicio: la búsqueda de candidatos, las entrevistas y la incorporación no tienen costo previo. Se dice igual en todo el sitio y nunca como oferta "por tiempo limitado", porque no lo es. Se pueden reutilizar las frases "No setup fee" y "Review and interview candidates before committing".
4. **U.S. hire vs Orchid (calculadora).** Campos: rol (por defecto, administrative assistant), horas por semana y salario local (opcional). Resultado: costo anual estimado de una contratación local frente a Orchid, con el desglose (salario, beneficios e impuestos patronales, costo de contratación).
   - **Fuentes visibles bajo la calculadora:** BLS OEWS May 2025, SOC 43-6014 (salario); BLS ECEC (beneficios como % de la remuneración); SHRM (costo por contratación). Cada una con su enlace y la fecha de consulta.
   - Valores por defecto que dan ~$78k frente a ~$31k: **~60% menos**. Es la única cifra de ahorro en todo el sitio (decidido el 27 nov 2026). El "40–50%" del video de los fundadores no se repite en texto.
   - **Desarrollo:** JavaScript en un bloque HTML, sin servicios externos. El número se calcula en el navegador. Botón `Book a free call` debajo del resultado.
5. **How Orchid compares.** Tabla por modelo, no por marca: freelancer de marketplace, agencia offshore (Filipinas), Orchid (Colombia) y empleado local. Filas: horario, idioma, quién maneja RR. HH., reemplazo y rango de precio. Los rangos salen del PDF de competencia del 24 nov 2026, con esa fecha.
6. **FAQ:**
   - Is there a setup fee? (No: $0 to begin.)
   - What's included in the hourly rate?
   - What if the hire doesn't work out? (Reemplazo sin costo.)
   - Do you sign a BAA for healthcare practices? (Sí.)
   - Part-time or full-time? (Ambos: Orchid ofrece medio tiempo y tiempo completo.)
   - **No incluir "Is there a long-term contract?".** El mínimo de 6 meses se explica en la llamada. Ninguna página puede decir "no contract" ni "cancel anytime".
7. **CTA:** `Book a free call to get your exact quote`.

**Schema:** `Service` con `Offer` + `UnitPriceSpecification` (minPrice 15, USD, unitCode HUR) y `FAQPage`. La calculadora puede llevar `WebApplication`, que es opcional.

**Enlaces internos**
- **Entrantes:** todas las páginas de mercado (sección "What it costs"), menú principal ("Pricing"), home y FAQ ("Are there hidden fees?").
- **Salientes:** páginas de mercado (Healthcare, Small business, Law firm, Real estate), `/how-we-select/` y la cita.

---

### Brief 3 · Small business (reemplaza /other-professionals/)

| Campo | Valor |
|---|---|
| URL / slug | `/solutions/small-business/` (nueva) con **301 desde `/other-professionals/`**, hecho con el plugin gratuito Redirection |
| SEO title | `Bilingual Virtual Assistants for Small Businesses \| Orchid` |
| Meta description | `A dedicated assistant from Colombia who speaks English and Spanish and works your hours: admin, operations, customer service. From $15/hour.` |
| H1 | `A Bilingual Virtual Assistant for Your Small Business` |
| Palabra clave principal | virtual assistant for small business |
| Secundarias | bilingual virtual assistant, spanish speaking virtual assistant, executive assistant for small business owner, hire virtual assistant from Colombia |

**Secciones**
1. **Hero:** `Get your hours back. A dedicated assistant who speaks English and Spanish, works your business hours, and comes with HR support. From $15/hour.` Botones: `Book a free call` y `See pricing`.
2. **Signs you're ready to delegate.** 5 señales concretas (bandeja de entrada, agenda, facturas, seguimiento a clientes, clientes que hablan español). Enlace a la calculadora.
3. **What your assistant can do.** H3 por área: admin & inbox, operations & scheduling, bookkeeping support (sin decir "contador"), marketing support (enlace a `/solutions/marketing-creative/`), customer service in Spanish and English.
4. **Industries we support.** Tarjetas a Accounting, Real Estate, Law Firms y Healthcare.
5. **Why Orchid.** Los mismos 6 diferenciadores del brief 1, contados para dueños de pyme.
6. **How it works + timing:** 3 pasos; candidatos en 20 días hábiles.
7. **Pricing snapshot:** desde $15/hora, la comparación anual con su fuente y el enlace a /pricing/.
8. **Meet the founders** (corto) + enlace a /about/.
9. **FAQ:**
   - How is Orchid different from hiring on Upwork?
   - Can I hire part-time? (Sí: medio tiempo o tiempo completo.)
   - Will my assistant work only for me? (Sí, dedicado: dato de la página actual de salud.)
   - What hours?
   - What if it's not a fit?
   - Do they speak Spanish?
10. **CTA final.**

**Schema:** `Service` (serviceType "Virtual assistant staffing for small businesses", areaServed US, availableLanguage en/es, offer desde $15/h) + `FAQPage`.

**Enlaces internos**
- **Entrantes:** menú (renombrar "Other professionals" a "Small Business"), home, `/solutions/`, `/pricing/`, `/bilingual-virtual-assistant/`, `/why-colombia/` y los artículos del Brief para emprendedores.
- **Salientes:** `/solutions/accounting/`, `/real-estate/`, `/law-firm/`, `/solutions/marketing-creative/`, `/pricing/`, la calculadora, `/about/` y la cita.

---

## 4. KPIs mensuales y cómo se miden

| KPI | Herramienta | Cómo se lee | Meta a 90 días |
|---|---|---|---|
| Impresiones y clics orgánicos (Google) | Search Console → Rendimiento | Total y por página. Filtro de consulta por grupo con expresión regular, por ejemplo `medical\|dental\|hipaa\|patient\|chiropract` | Base en el mes 1; después, crecer mes a mes |
| Impresiones y clics (Bing) | Bing Webmaster → Search Performance | Igual | Base en el mes 1 |
| Posición media por grupo de palabras | Search Console (filtros por grupo) | Salud, pymes, abogados, contadores, bienes raíces y marca | Salud: entrar al top 20 en ≥5 consultas del grupo |
| Páginas indexadas / con problemas | Search Console → Indexación | Sitemap enviado frente a indexadas; ninguna URL de go.orchidpros.com indexada | 100% de las páginas nuevas indexadas en ≤14 días |
| Sesiones orgánicas en páginas de servicio | GA4 → Adquisición de tráfico, canal "Organic Search" + página de destino | Solo páginas de mercado, precios y calculadora | Base en el mes 1 |
| Clics a la cita desde el sitio | GA4, evento `cta_book_call` (nuevo, ver abajo) | Por página de origen | Base en el mes 1 |
| **Leads orgánicos** | GoHighLevel: contactos con `utm_source=organic` o `utm_source=ai` (ver abajo) | Excluyendo etiquetas spam/lead-falso, igual que `scripts/ghl.py` | El número que importa; base en el mes 1 |
| **Citas agendadas orgánicas** | GHL: citas del calendario de esos contactos | Calificadas = "I want to hire" | Igual |
| Tráfico desde IA | GA4, canal personalizado "AI" (abajo) | chatgpt.com, perplexity.ai, copilot.microsoft.com, gemini.google.com, claude.ai | Base |
| Menciones en IA | Prueba manual mensual (sección 5) | Prompts con Orchid citado / total | ≥2 de 10 al día 90 |

No pongo metas numéricas de leads porque hoy no hay ninguna medición orgánica. Las metas salen del mes 1.

**Cómo se marca el tráfico orgánico en GoHighLevel (Desarrollo, semana 1)**

El formulario y la cita viven en go.orchidpros.com. Si alguien llega de Google a orchidpros.com y hace clic en "Book a free call", GHL solo ve que viene de orchidpros.com y se pierde que era orgánico. La solución:
1. Un script pequeño en WordPress (en el header, o con un plugin de código como WPCode). En la primera página que ve el visitante, mira `document.referrer`:
   - google, bing, duckduckgo, yahoo o ecosia → `organic`
   - chatgpt.com, perplexity.ai, copilot.microsoft.com o gemini.google.com → `ai`
   - Si la URL ya trae `utm_*` (anuncios), lo respeta.

   Guarda la fuente y la página de entrada en una cookie propia por 30 días. No guarda datos personales.
2. A cada enlace hacia `go.orchidpros.com` le agrega `utm_source=<organic|ai|direct|referral>&utm_medium=<motor>&utm_campaign=seo&utm_content=<página de entrada>`.
3. GHL ya guarda las UTM del formulario y de la cita (así se leen hoy `utm_content` y `lp_variant`). Hay que crear un Smart List "Leads orgánicos" con `utm_source = organic` y otra para `ai`, y agregar la etiqueta en el workflow "01 - Lead nuevo".
4. En GA4: un evento `cta_book_call` al hacer clic en esos enlaces. Revisar que orchidpros.com y go.orchidpros.com estén en la misma propiedad con dominios cruzados (Admin → Flujos de datos → Configurar dominios). No pude verificar qué etiqueta de GA4 tiene GHL **[CONFIRMAR]**. Agregar un grupo de canales personalizado "AI" con la expresión regular de dominios de IA.

`scripts/ghl.py` puede sumar un conteo de leads con `utm_source=organic` o `ai` al informe de los lunes.

---

## 5. Visibilidad en buscadores con IA (Copilot/Bing, ChatGPT, Google AI Overviews)

Copilot y la búsqueda de ChatGPT usan en buena parte el índice de Bing. Las AI Overviews usan el de Google. Todo empieza por estar bien indexado y por ser una entidad clara.

1. **Bing primero:** Bing Webmaster + IndexNow en la semana 1. Revisar que nada bloquee a `bingbot`, `OAI-SearchBot`, `GPTBot`, `PerplexityBot` ni `Google-Extended`. Hoy `robots.txt` está abierto, pero hay que confirmar si el hosting o Cloudflare tienen bloqueo de bots **[CONFIRMAR]**.
2. **Entidad clara.** Un solo nombre y una sola descripción en todas partes: "Orchid (N3XUS, LLC d/b/a ORCHID), bilingual remote staffing from Colombia for U.S. businesses".
   - Organization schema con `founder`, `sameAs` corregido (Instagram, LinkedIn, Facebook, TikTok), `contactPoint` y `areaServed`.
   - Mismo texto en LinkedIn, Instagram, Clutch o G2 y en el perfil de Google, si se mantiene.
3. **llms.txt correcto:** las 8 páginas clave y la descripción nueva (I7).
4. **Respuesta directa arriba.** Cada página de servicio y cada guía empieza con un párrafo de 2–3 frases que responde la pregunta (qué es, para quién, cuánto cuesta, en qué se diferencia). La IA cita párrafos así.
5. **Datos con fuente.** La calculadora y la tabla de costos con BLS, ECEC y SHRM citados y fechados. Los modelos citan más las páginas con números verificables.
6. **FAQ visibles + FAQPage.** Preguntas reales, con respuestas de 40–60 palabras.
7. **Personas reales (E-E-A-T).** /about/ y /how-we-select/ con los fundadores, su experiencia, el proceso de selección y el video. Person schema con `sameAs` a sus LinkedIn **[CONFIRMAR URLs]**.
8. **Menciones de terceros.** Perfil en Clutch o G2 con reseñas pedidas a clientes reales. Directorios de la industria (asociaciones dentales o médicas estatales, cámaras de comercio). Podcasts o artículos donde hablen los fundadores. Nunca reseñas falsas ni incentivadas sin decirlo.
9. **Comparativas honestas** (Colombia vs Philippines, Orchid vs X): la IA las usa para preguntas como "best bilingual medical VA company".
10. **Prueba mensual.** 10 preguntas fijas en ChatGPT (con búsqueda), Copilot, Perplexity y Google (AI Overview). Por ejemplo:
    - "best bilingual medical virtual assistant company"
    - "virtual assistant from Colombia for dental office"
    - "HIPAA trained Spanish speaking virtual receptionist"
    - "Orchid Pros reviews"
    - "Colombia vs Philippines virtual assistant"
    - "how much does a medical virtual assistant cost"
    - "nearshore virtual assistant same time zone"
    - "virtual assistant for small business Spanish"
    - "Wing Assistant alternatives"
    - "bilingual legal intake assistant"

    Anotar si Orchid aparece, si la cita es a orchidpros.com y qué competidores salen. Se guarda en `seo/ai-visibility/AAAA-MM.md`.

---

## 6. Calendario de contenido con The Delegate Brief

Cada edición (quincenal) se convierte en un artículo en `orchidpros.com/the-delegate-brief/<slug>/`, con el mismo texto ampliado a ~600–900 palabras. Lleva un enlace a la página de servicio del tema y un CTA de suscripción. El sitio es la URL original: el correo enlaza al sitio, no al revés.

| Edición (aprox.) | Tema sugerido | Enlaza a |
|---|---|---|
| 10 dic | One task to delegate before year-end: insurance verification | /solutions/healthcare/ |
| 24 dic | Year-end admin a bilingual assistant can take off your plate | /solutions/small-business/ |
| 7 ene | Tax season prep: what to delegate in a CPA firm | /solutions/accounting/ |
| 21 ene | Missed calls in Spanish: what they cost a dental practice | /solutions/healthcare/dental/ |
| 4 feb | Same hours vs 12-hour gap: how time zones change delegation | /why-colombia/ |
| 18 feb | Intake calls for immigration firms | /law-firm/immigration/ |
| 4 mar | The real cost of a U.S. admin hire in 2027 (con la calculadora) | /pricing/ |

Los temas se ajustan a lo que salga en cada edición real.

---

## 7. Fuera del sitio (en paralelo)

- **Google Business Profile:** Orchid es 100% virtual y su única dirección es el P.O. Box, así que no cumple las reglas de perfiles locales (ver sección 5 de la auditoría). No invertir en él ni editar su dirección: un cambio de dirección dispara una nueva verificación que no se puede pasar con un P.O. Box. El SEO no depende de él.
- **Reseñas reales:** desde la semana 2, pedir a los clientes activos una reseña en **Clutch** (y G2 si aplica), que aceptan negocios remotos. Sin incentivos ocultos y sin redactarlas por ellos. Las 4 reseñas de Google se pueden citar en el sitio solo con permiso de sus autores.
- **Bing Places:** no crearlo, por la misma razón.

---

## 8. Canadá (arranca ya)

Orchid empieza a atender Canadá (decidido el 27 nov 2026). Para no abrir un segundo sitio, se hace en **una sola página** al principio, `/ca/`, y se crece según lo que diga Search Console.

| Campo | Valor |
|---|---|
| URL | `/ca/` |
| SEO title | `English-Spanish Virtual Assistants for Canadian Businesses \| Orchid` (63: recortar si el diseño lo pide) |
| H1 | `Bilingual (English–Spanish) Virtual Assistants for Canadian Businesses` |
| Palabras clave | hire virtual assistant Canada, virtual assistant for small business Canada, Spanish speaking virtual assistant Canada |
| Idioma | inglés en el texto; los precios siempre en US$ |

**Reglas para Canadá**
- **"Bilingual" en Canadá se entiende como inglés-francés.** Decir siempre "English–Spanish".
- **HIPAA no aplica en Canadá.** La privacidad de salud se rige por PIPEDA y por leyes provinciales como PHIPA en Ontario. La página de Canadá no usa "HIPAA-trained" ni promete cumplimiento canadiense hasta confirmar qué capacitación reciben los asistentes **[CONFIRMAR]**.
- **Horario:** Colombia (UTC−5) coincide con Toronto, Ottawa y Montreal en invierno, va una hora detrás en verano y tiene 3 horas de diferencia con Vancouver. Decirlo así, sin "same time zone" genérico.
- **Precio:** se cobra en dólares de EE. UU. (confirmado el 27 nov 2026). En la página de Canadá siempre "from US$15/hour", con el "US$" explícito para que nadie lo lea como dólares canadienses. Medio tiempo y tiempo completo, igual que en EE. UU.
- **Calculadora:** los datos de BLS son de EE. UU. Para Canadá haría falta Statistics Canada; hasta tenerlos, la página enlaza a la de precios sin la comparación de ahorro.

**Secciones:** hero con la propuesta, qué puede hacer el asistente, por qué Colombia (horario real), cómo funciona, precio, fundadores, FAQ y cita.

**Medición:** en GoHighLevel se separan los leads de Canadá por el país del formulario y por `utm_content=/ca/` (sección 4). En Search Console, filtrar por país = Canadá.

**Datos de palabras clave:** siguen "sin dato". En el Planificador de Google Ads, exporta las palabras del CSV con `pais = CA` eligiendo la ubicación "Canadá".
