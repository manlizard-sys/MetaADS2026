# Palabras clave y competencia · Orchid

Fecha: 27 nov 2026.

**Archivos**
- [`keywords.csv`](keywords.csv): 53 palabras clave con país, mercado, intención, grupo, volumen, dificultad, quién aparece y página de Orchid.
- [`competencia_paginas.csv`](competencia_paginas.csv) y [`competencia_paginas.json`](competencia_paginas.json): tipos de página que publica cada competidor, con ejemplos. Salen de `scripts/seo/competitor_sitemaps.mjs`.

## Qué datos hay y cuáles no

| Dato | Estado | Fuente |
|---|---|---|
| Volumen de búsqueda | **sin dato** en todas las filas | No hay conector de Semrush, Ahrefs ni OpenSEO en esta sesión |
| Dificultad | **sin dato** | Igual |
| Quién aparece hoy | Parcial: 17 búsquedas revisadas | Buscador web de la herramienta (WebSearch), 27 nov 2026. **No es la página de resultados de Google**: sirve para ver qué tipo de páginas compiten, no posiciones exactas. |
| Qué páginas tiene cada competidor | 22 de 23 competidores | El sitemap XML público de cada uno, 27 nov 2026. Time etc no respondió. |
| Precios y ofertas de la competencia | Sí | `build/research/competencia/Competencia_Orchid_2026-11-24.pdf` |

### Cómo conseguir volumen y dificultad, de más barato a más completo
1. **Google Keyword Planner** (gratis con una cuenta de Google Ads, sin gastar). Ve a Herramientas → Planificador de palabras clave → "Obtener volumen de búsqueda y previsiones" y pega la columna `palabra_clave` del CSV. Elige EE. UU., y aparte Canadá. Sin campañas activas muestra rangos (por ejemplo, 100–1K), que alcanzan para priorizar.
2. **Microsoft Advertising → Keyword Planner** (gratis). Da los volúmenes de Bing, que importan porque Bing alimenta a Copilot y a ChatGPT.
3. **Semrush, Ahrefs u OpenSEO.** Si conectas uno a esta app, relleno `volumen_mensual`, `dificultad` y las posiciones reales de cada competidor en una sola pasada. Semrush y Ahrefs tienen prueba de 7 días.
4. **Search Console.** Después de 4–8 semanas con las páginas nuevas, da las búsquedas reales por las que aparece Orchid. Es el mejor dato para ajustar.

Exporta el CSV del planificador a `seo/keywords/volumenes/` y yo lo cruzo con `keywords.csv`.

---

## Grupos por mercado e intención (EE. UU.)

La lista completa, palabra por palabra, está en el CSV. Aquí va lo que importa de cada grupo.

### 1. Salud (prioridad 1)
| Grupo | Intención | Ejemplos | Quién aparece (de la lista) | Página de Orchid |
|---|---|---|---|---|
| medical-va | comercial | hire a medical virtual assistant, medical virtual assistant services, bilingual medical virtual assistant | Wishup (guías), Wing (página bilingüe de salud) | `/solutions/healthcare/` (reescribir) |
| hipaa | comercial / informativa | HIPAA trained virtual assistant, HIPAA compliant virtual assistant | Ninguno en los primeros resultados: blogs de cumplimiento y software de IA | `/solutions/healthcare/` + guía nueva `/guides/hipaa-virtual-assistant/` |
| dental | comercial | virtual receptionist for dental office, dental virtual assistant | Ninguno: recepcionistas con IA (Weave, My AI Front Desk) | nueva `/solutions/healthcare/dental/` |
| quiro-pt | comercial | chiropractic virtual assistant, physical therapy virtual assistant | Wing, Wishup y HelpSquad (blog) | nueva `/solutions/healthcare/chiropractic-physical-therapy/` |
| roles | comercial | remote medical billing specialist, insurance verification VA, patient scheduling coordinator | sin revisar | secciones de `/solutions/healthcare/` |
| comparativas | comparativa | medical virtual assistant companies, medical virtual assistant cost | HelpSquad (comparativa de precios), Wbcom (lista) | nueva `/compare/medical-virtual-assistant-companies/` y `/pricing/` |

**Lo que se ve:** "medical virtual assistant" y "virtual receptionist" son búsquedas **ambiguas**. Buena parte de los resultados son productos de IA (RingCentral, Weave, recepcionistas con IA), no personas. Orchid gana con las palabras que piden una persona: "hire", "bilingual", "Spanish-speaking", "dedicated", "HIPAA-trained". Además, la página tiene que decir desde el título que es una persona real.

**Regla:** la página dice "HIPAA-trained". Puede haber una guía informativa que explique qué es un BAA y qué significa "HIPAA compliant", sin afirmar que Orchid lo es.

### 2. Pequeñas empresas y emprendedores (prioridad 2)
| Grupo | Intención | Ejemplos | Quién aparece | Página |
|---|---|---|---|---|
| pymes-va | comercial | virtual assistant for small business, bilingual virtual assistant, spanish speaking virtual assistant | Time etc, Prialto; Wing en "bilingual" | `/other-professionals/` → renombrar a `/solutions/small-business/` + nueva `/bilingual-virtual-assistant/` |
| nearshore | comercial | nearshore staffing Colombia, hire virtual assistant from Colombia | Somewhere (lista), VA Masters (costos); agencias nearshore de TI | nueva `/why-colombia/` |
| precio | informativa / comercial | how much does a virtual assistant cost, virtual assistant pricing, employee vs VA cost | Prialto; Upwork, Fiverr, Airtasker | nuevas `/pricing/` y `/tools/us-hire-vs-orchid-calculator/` |
| país vs país | comparativa | Colombia vs Philippines virtual assistants | Stealth Agents, VA Masters | nueva `/compare/colombia-vs-philippines-virtual-assistants/` |
| alternativas | comparativa | BELAY alternatives, Virtual Latinos alternatives, Wing Assistant alternatives | Wishup, VA Masters, Stealth Agents, South, Wing, Persona, Prialto | nuevas `/compare/...` (después de salud) |

### 3. Abogados (prioridad 3; Meta en pausa para este mercado)
| Grupo | Intención | Ejemplos | Quién aparece | Página |
|---|---|---|---|---|
| legal-va | comercial | virtual assistant for law firms, bilingual legal assistant, immigration law firm virtual assistant, spanish speaking legal intake | Ninguno de la lista: Legal Soft, Answering Legal y **ofertas de empleo** | `/law-firm/` + nueva `/law-firm/immigration/` |
| legal-tools | informativa | attorney hourly rate calculator | sin revisar | `/attorney-income-calculator/` (unificar las 2) |

**Ojo:** en "bilingual legal assistant" aparecen ofertas de empleo de Workana y Workable. Esa búsqueda atrae a candidatos, el mismo problema de calidad de leads que hubo en Meta. Hay que apuntar a "for law firms", "hire" y "services".

### 4. Contadores y finanzas (prioridad 4)
virtual assistant for accountants, CPA firm virtual assistant, tax season virtual assistant, remote bookkeeper. Aparecen **Time etc, Prialto y VA Masters**, con páginas de industria. Orchid no tiene página para este mercado: nueva `/solutions/accounting/`. **Es estacional:** conviene publicarla antes de la temporada de impuestos (enero).

### 5. Bienes raíces (prioridad 5)
real estate virtual assistant, real estate ISA, transaction coordinator VA, bilingual real estate assistant. Aparece **MyOutDesk** con página de servicio y guía. Orchid ya tiene `/real-estate/` (458 palabras, con un enlace roto); hay que ampliarla, no crear otra.

---

## Canadá (aparte)

Las 5 búsquedas de muestra están en el CSV con `pais = CA`.
- **Salud:** "virtual medical office assistant Canada" devuelve sobre todo **ofertas de empleo** (Indeed, WELL Health). Hoy no se ve demanda de empresas contratando agencias. Además, en Canadá la privacidad de salud se rige por PHIPA/PIPEDA y leyes provinciales, no por HIPAA, así que el mensaje "HIPAA-trained" no aplica tal cual.
- **Pymes:** dominan Upwork, Indeed y guías públicas (Small Business BC, BDC). Ningún competidor de la lista aparece.
- **"Bilingual" en Canadá suele significar inglés-francés.** Orchid es inglés-español: hay que decir "English-Spanish" siempre.
- **Horario:** Colombia (UTC−5) coincide con Toronto y Montreal (UTC−5 en invierno), pero tiene 3 horas de diferencia con Vancouver.
- **Decisión (27 nov 2026): Orchid arranca en Canadá ya.** Se empieza con una sola página `/ca/` (brief en la sección 8 de `seo/plan.md`) y se amplía según lo que diga Search Console. El precio va en dólares de EE. UU. ("from US$15/hour").

---

## Brechas: qué tiene la competencia y Orchid no

Conteo de URLs por tipo en el sitemap de cada competidor (27 nov 2026). Es un conteo por patrones en la URL: sirve como orden de magnitud. Los ejemplos de cada uno están en el JSON.

| Competidor | URLs totales | Precios / costos | "Alternatives" | "vs" / comparativas | Calculadoras* | Salud | Ejemplo útil |
|---|---|---|---|---|---|---|---|
| Stealth Agents | 38,166 | 621 | 1,840 | 433 | `/roi-calculator` | 2,509 | `/services/hipaa-compliant-virtual-assistant`, `/spanish-speaking-virtual-assistant` |
| VA Masters | 1,667 | 65 | 31 | 96 | artículos de ROI | 45 | `/bilingual-spanish-english-virtual-assistants/`, `/va-masters-vs-belay/` |
| Wing Assistant | 1,018 | 16 | 5 | 95 | `/roi-calculator/`, `/mgma-calculator/` | 124 | `/hellorache-vs-wing-assistant/`, `/medva-vs-wing-assistant/`, `/bilingual-healthcare-virtual-assistant/` |
| South | 2,202 | 126 | 10 | 97 | — | 32 | `/post/bilingual-virtual-assistant`, `/post/best-virtual-medical-assistant-services` |
| Virtustant | 535 | 40 | 15 | 41 | — | 21 | `/hipaa-virtual-assistant`, `/blog/bilingual-virtual-assistant-rates-by-country`, `/blog/2026-nearshore-rate-report` |
| Rose Talent (Colombia) | 741 | 80 | 0 | 55 | artículos de ROI | 55 | `/blog/best-bilingual-virtual-assistant-companies-in-colombia`, `/blog/average-monthly-cost-for-remote-dental-virtual-assistant` |
| HelpSquad | 570 | 16 | 0 | 16 | artículos de ROI | 241 | `/healthcare/chiropractors/`, `/blog/is-an-offshore-virtual-assistant-hipaa-compliant/` |
| HelloRache | 246 | 6 | 0 | 11 | `/medical-practice-calculators/` | 163 | `/virtual-assistant-cost/`, `/virtual-receptionist-pricing/` |
| MedVA | 91 | 3 | 0 | 0 | `/virtual-assistant-savings-calculator/` | 47 | alianza con la Michigan Dental Association |
| CallForce (Colombia) | 337 | 24 | 5 | 23 | `/calculator/` y herramientas | 16 | `/services/dental-answering-service/`, `/blog/canadian-smb-nearshore-outsourcing/` |
| Somewhere | 1,610 | 18 | 1 | 17 | `/calculator` | 24 | **casos con precio real** ("chiropractic care provider hired an insurance verifier for $1,010/month") |
| Virtual Latinos | 622 | 22 | 4 | 20 | — | 17 | 74 páginas legales: `/blog/bilingual-legal-virtual-assistant/` |
| **Orchid** | **20** | **0** | **0** | **0** | 2 calculadoras de abogados, sin enlaces | **1** (con título equivocado) | — |

\* La columna de calculadoras del CSV también cuenta URLs que contienen "roi" (como "android"). Aquí solo se citan calculadoras verificadas en la URL.

### Las brechas, en orden de impacto en leads
1. **Página de servicio de salud bilingüe que diga lo que la competencia no junta.** Wing, Stealth Agents, Virtustant y HelpSquad tienen páginas de "HIPAA" y "bilingual". Ninguna junta Colombia, mismo horario, HIPAA-trained, apoyo de RR. HH. incluido y fundadores con cara (según el PDF de competencia). Es la página que más leads puede traer, y hoy la de Orchid tiene el título de abogados.
2. **Precios y calculadora.** Casi todos tienen `/pricing`. HelloRache, MedVA, Wing, Somewhere y CallForce tienen calculadora. Orchid no publica precio en el sitio, aunque tiene un dato mejor documentado que la mayoría: BLS OEWS mayo 2025, SOC 43-6014, más ECEC y SHRM.
3. **Subpáginas por especialidad de salud:** dental, quiropráctica y fisioterapia, facturación, verificación de seguros. HelpSquad, Portiva y Stealth Agents las tienen. Calzan con el público de las campañas de Meta.
4. **Comparativas honestas.** Wing tiene páginas como "hellorache-vs-wing-assistant" y "medva-vs-wing-assistant", y VA Masters, Stealth Agents y Virtustant tienen "alternatives". Para Orchid tienen sentido `colombia-vs-philippines` y un "Orchid vs" contra competidores de salud (Wing, HelloRache, MedVA, Portiva), con datos públicos fechados.
5. **Casos con números reales**, como hace Somewhere: rol, especialidad, costo al mes y resultado. Solo con clientes que lo autoricen. Sirven para Google, para la IA y para los anuncios.
6. **Guías de costo por rol y país** (Rose Talent, Virtustant y su "nearshore rate report"). Orchid puede publicar su propia tabla de costos con fuentes.
7. **Página de "bilingual / Spanish-speaking virtual assistant".** La tienen Wing, VA Masters, Stealth Agents y South. Es el núcleo de la propuesta de Orchid y no tiene página propia.

**Lo que NO conviene copiar:** el volumen de Stealth Agents (38 mil URLs y 1,840 páginas de "alternatives"). Es contenido generado en masa. Con un sitio de 20 páginas, Orchid gana con pocas páginas muy buenas y con datos propios.
