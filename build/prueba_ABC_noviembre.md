# Prueba A/B/C de ruta de conversión · Noviembre 2026

**Pregunta:** ¿qué destino trae más leads calificados (firmas que quieren contratar) por dólar?

| | Versión | Estado |
|---|---|---|
| **A** | Landing de solo formulario | **Falta crearla en GHL** (instrucciones abajo) |
| **B** | Landing completa (go.orchidpros.com/hire) | **Falta corregirla en GHL** (instrucciones abajo) |
| **C** | Formulario instantáneo de Meta | **Creado por Claude** el 23 oct (id `2620655611681341`). Falta conectarlo a GHL |

## Diseño de la prueba

- **Herramienta:** Meta → Experimentos → Prueba A/B. Tres conjuntos de anuncios; Meta reparte el público para que nadie vea dos versiones.
- **Una sola variable:** el destino. Mismos anuncios (S9, 🔵 H3, 🔵 H5), mismo público, mismo presupuesto.
- **Público:** dueños y abogados de firmas en NY, NJ y PA, 30–65 años, intereses Law firm, Lawyer y Bar association. El hiperlocal (~1,800 personas alcanzadas) es demasiado chico para partirlo en tres.
- **Presupuesto:** $15/día por versión ($45/día en total), de lunes a viernes, con la pausa automática de fin de semana. Esto usa prácticamente todo el presupuesto de noviembre ($1,000), así que el piloto hiperlocal se pausa mientras dura la prueba.
- **Duración:** del lunes 2 al viernes 20 de noviembre (15 días hábiles).
- **Métrica que decide:** costo por **lead calificado** en GHL (respondió "I want to hire"). Métricas secundarias: tasa de conversión y % de buscadores de empleo.
- **Advertencia:** con $15/día por versión, el resultado es una tendencia, no una prueba estadística concluyente.

## Calendario

| Fecha | Qué | Quién |
|---|---|---|
| Hasta el jue 29 oct | Crear landing A, corregir landing B, conectar formulario C a GHL | Equipo Orchid |
| Vie 30 oct | Envío de prueba en A, B y C (llega a GHL con etiquetas y UTMs; Meta registra el Lead) | Equipo + Claude |
| Vie 30 oct | Crear la prueba A/B en Meta, pausada | Claude |
| Lun 2 nov | Activar la prueba | Claude, con OK del dueño |
| Vie 20 nov | Resultado y recomendación | Claude |

---

## B · Correcciones a la landing actual (go.orchidpros.com/hire)

Problema: el anuncio dice *"bilingual legal assistant for law firms, from $15/hr"* y la landing dice *"Buy your time back hiring a bilingual professional assistant"*: no menciona abogados ni precio. Quien hace clic no ve lo que le prometieron.

### Encabezado (primera pantalla)

- **Etiqueta pequeña:** `For U.S. law firms`
- **Título:** `A bilingual legal assistant for your firm, from $15/hr`
- **Subtítulo:** `A dedicated assistant from Colombia who works your business hours. Intake calls, scheduling, client follow-ups and document collection, in English and Spanish.`
- **Viñetas:**
  - `Works U.S. business hours`
  - `Fluent in English and Spanish`
  - `Same person every week, trained on your firm`
  - `Replaced at no extra cost if it's not the right fit`
- **Botón:** `Book a free call` (baja al formulario)
- **Quitar del encabezado:** `Matched to your business in about 20 business days`. Se queda solo en "How it works".

### Sección "Your week, delegated"

Cambiar las filas por tareas de una firma legal:

| Tarea | Quién |
|---|---|
| Intake calls and scheduling | Assistant |
| Client follow-ups in Spanish | Assistant |
| Document collection | Assistant |
| Your cases | You |

### Formulario (menos fricción)

- **Título:** `Book your free call` · **Subtítulo:** `Takes about 20 seconds.`
- **Campos, en este orden:**
  1. `Are you looking to hire an assistant, or looking for a job?` (obligatorio). Es el filtro actual "How can we help you?"; mantener las mismas respuestas para no romper el reporte de GHL.
  2. `What type of firm do you run?` (obligatorio). Opciones: Immigration law · Personal injury · Family law · Other law practice · Other business.
  3. `First Name` (obligatorio)
  4. `Email` (obligatorio)
  5. `Phone` (opcional)
- **Quitar:** `Last Name`.
- **Casilla de SMS:** dejarla **opcional**. El consentimiento no puede ser condición para enviar el formulario.
- **Mantener** el enlace `Looking for a job at Orchid? Apply here` justo debajo del formulario. Es un buen filtro.

### Testimonio

El único testimonio es de un agente inmobiliario (Keller Williams). Si hay un cliente del sector legal, reemplazarlo. Si no, moverlo al final de la página. **No inventar testimonios.**

### Seguimiento (no tocar)

Mantener el píxel de Meta, el evento Lead al enviar y los campos ocultos de UTM (`utm_content` = nombre del anuncio).

---

## A · Landing de solo formulario (página nueva en GHL)

- **URL sugerida:** `go.orchidpros.com/hire-form`
- **Contenido, nada más:**
  1. Logo de Orchid
  2. Título: `A bilingual legal assistant for your firm, from $15/hr`
  3. Una línea: `Book a free 30-minute call. Takes about 20 seconds.`
  4. **El mismo formulario que B** (mismos campos, mismo orden, mismas respuestas)
  5. Enlace `Looking for a job at Orchid? Apply here`
  6. Pie: Privacy Policy · Terms of Service
- **Sin** menú, sin secciones, sin testimonios.
- **Mismo píxel, mismo evento Lead y mismos campos ocultos de UTM que B.**

---

## C · Formulario instantáneo de Meta (ya creado)

**Nombre:** `Orchid · Law firms · Higher intent · Test C · 2026 Nov` · **id:** `2620655611681341`

- **Tipo:** Mayor intención. La persona revisa sus datos antes de enviar, lo que filtra envíos accidentales.
- **Preguntas:**
  1. `Are you looking to hire an assistant for your firm, or looking for a job?` → `I want to hire an assistant` / `I'm looking for a job`
  2. `What type of firm do you run?` → Immigration law · Personal injury · Family law · Other law practice · Other business
  3. Nombre completo, email y teléfono (Meta los llena automáticamente)
- **Privacidad:** orchidpros.com/privacy-policy-2/
- **Pantalla final:** `Thanks! We'll reach out to book your free call.`, con botón a go.orchidpros.com/hire

### Lo que falta: conectarlo a GHL (lo hace un administrador)

1. GHL → **Settings → Integrations → Facebook** → **Facebook Form Fields Mapping** (Lead Ads).
2. Elegir el formulario `Orchid · Law firms · Higher intent · Test C · 2026 Nov`.
3. Asignar los campos:
   - `hire_or_job` → campo personalizado **"Hiring or job seeking"**
   - `firm_type` → campo **"Vertical"**
   - nombre, email y teléfono → campos estándar
4. Agregar la etiqueta `fb-instant-form` y enviar el contacto al mismo pipeline que la landing.
5. Avisar a Claude para hacer un envío de prueba con la herramienta de prueba de Lead Ads de Meta.

---

## Además

- **Citas de Facebook:** desactivar las citas en la página de Orchid Pros. Con el botón "Book Now" abrían el calendario de Facebook en vez de la landing.
- **Categorías de la página:** quitar Recruiter y Real Estate (pendiente desde el 17 oct).
