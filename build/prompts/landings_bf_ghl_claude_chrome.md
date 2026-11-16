Necesito que crees dos landings nuevas en GoHighLevel (cuenta Orchid), clonando la landing de abogados que ya funciona (go.orchidpros.com/hire-50off). Trabaja en este orden, avísame al terminar cada paso y detente si algo no coincide con lo que describo.

DATOS
- Landing de origen: https://go.orchidpros.com/hire-50off (funnel de GHL, dominio go.orchidpros.com)
- Píxel de Meta: 2271987886986577
- Código nuevo (copiar desde GitHub, vista "Raw"):
  - Salud, pieza 1: https://github.com/manlizard-sys/metaads2026/blob/claude/admiring-franklin-wrfknt/build/landings/healthcare/piece1.html
  - Salud, pieza 2: https://github.com/manlizard-sys/metaads2026/blob/claude/admiring-franklin-wrfknt/build/landings/healthcare/piece2.html
  - Emprendedores, pieza 1: https://github.com/manlizard-sys/metaads2026/blob/claude/admiring-franklin-wrfknt/build/landings/entrepreneurs/piece1.html
  - Emprendedores, pieza 2: https://github.com/manlizard-sys/metaads2026/blob/claude/admiring-franklin-wrfknt/build/landings/entrepreneurs/piece2.html
  - La pieza 3 (footer) no cambia.

REGLAS
- No toques la landing hire-50off ni su formulario original: todo se hace sobre copias.
- No cambies el código de seguimiento (píxel, evento Lead, campos ocultos de UTM). Solo verifica que esté.
- No toques anuncios ni campañas en Meta.

PASO 1 · Landing de salud
1. En GHL ve a Sites → Funnels → abre el funnel de hire-50off. Clona el paso de hire-50off dentro del MISMO funnel (así hereda el código de seguimiento del funnel).
2. Nombre del paso: "BF Healthcare". Path: practices-free-month.
3. En el editor, abre el bloque Custom Code de la PIEZA 1 (el primero de la página), borra todo su contenido y pega el contenido completo de "Salud, pieza 1". Haz lo mismo con el bloque de la PIEZA 2 (columna izquierda de la sección morada del formulario) usando "Salud, pieza 2".
4. Formulario (columna derecha): duplica el formulario actual en Sites → Forms, nómbralo "Orchid · BF Healthcare" y en la copia cambia solo la pregunta del tipo de firma: texto "What type of practice do you run?" con opciones Primary care · Dental · Physical therapy · Chiropractic · Specialty clinic · Other. Deja igual la pregunta "Hiring or job seeking", los campos de contacto, los campos ocultos de UTM y el resto. Agrega la etiqueta "bf-healthcare" al enviar. Pon este formulario nuevo en la columna derecha de la página clonada.
5. Configuración SEO del paso: título "Orchid for Healthcare Practices | Get Started Free, 50% Off Your First Month"; descripción "HIPAA-trained, bilingual healthcare support professionals from Colombia for U.S. practices, selected one by one by our HR team. Black Friday: get started free and 50% off your first month."
6. Si hire-50off tiene un paso de gracias (calendario), clónalo también con path practices-free-month-thanks y haz que el formulario nuevo redirija ahí.
7. Guarda y publica. Abre https://go.orchidpros.com/practices-free-month en una ventana nueva y confirma que carga y que los botones "Get Started Free" bajan al formulario.

PASO 2 · Landing de emprendedores
Igual al paso 1, con estos cambios:
- Nombre del paso: "BF Entrepreneurs". Path: business-free-month (gracias: business-free-month-thanks).
- Código: "Emprendedores, pieza 1" y "Emprendedores, pieza 2".
- Formulario "Orchid · BF Entrepreneurs": la pregunta del tipo de firma pasa a "What type of business do you run?" con opciones Home services (roofing, HVAC, plumbing) · Construction · Insurance · Real estate or mortgage · E-commerce · Professional services · Other. Etiqueta "bf-business".
- SEO: título "Orchid for U.S. Companies | Get Started Free, 50% Off Your First Month"; descripción "Bilingual admin, operations, bookkeeping and marketing professionals from Colombia for U.S. companies and entrepreneurs, selected one by one by our HR team. Black Friday: get started free and 50% off your first month."
- Publica y confirma que https://go.orchidpros.com/business-free-month carga.

PASO 3 · Workflow de la API de Conversiones
1. En Automation → Workflows abre "Meta CAPI · Lead calificado".
2. Revisa el disparador: si filtra por formulario específico, agrega los dos formularios nuevos ("Orchid · BF Healthcare" y "Orchid · BF Entrepreneurs"). Si filtra solo por el campo "Hiring or job seeking", no cambies nada.
3. Guarda y publica solo si cambiaste algo.

AL TERMINAR, dime:
- Las dos URLs publicadas y si cargan.
- Si el código de seguimiento del funnel (píxel 2271987886986577) aparece en las páginas nuevas.
- Si tuviste que cambiar el workflow de CAPI.
- Cualquier paso que no coincidió con estas instrucciones.

No hagas envíos de prueba: los hace Claude Code después para verificar la medición.
