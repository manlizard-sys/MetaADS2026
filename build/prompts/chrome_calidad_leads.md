Necesito tres cambios en GHL de Orchid para que los leads falsos no ensucien la medición ni le lleguen a ventas. Hazlos en orden, avísame al terminar cada uno y detente si algo no coincide o si algo cuesta dinero.

REGLAS
- No toques anuncios ni campañas en Meta.
- No borres contactos.
- No cambies la landing de abogados (hire-50off) salvo que se indique.
- Si una opción tiene costo (por ejemplo, verificación de email de pago), NO la actives: dime cuánto cuesta y espera.

PARTE 0 · Marcar el lead falso
1. GHL → Contacts → busca el contacto creado hoy 17 nov a las 10:13 am (email que termina en @proton.com, etiqueta bf-healthcare).
2. Agrégale la etiqueta: lead-falso
3. Si su cita de hoy sigue confirmada, déjala como está (Andrea decide). Solo dime la hora de la cita.

PARTE 1 · Que el "lead calificado" lo decida la llamada, no el formulario
Hoy el workflow "Meta CAPI · Lead calificado" envía el evento a Meta en cuanto alguien responde "I want to hire." en el formulario. Un lead falso puede responder eso y Meta aprende de él. Queremos que se envíe solo cuando ventas confirme que es real.
1. Opportunities → Pipelines: dime qué pipeline usan los leads de Orchid y cuáles son sus etapas (nombres exactos).
2. Si no existe una etapa que signifique "llamada hecha y lead real" (algo como "Qualified", "Calificado" o "Discovery done"), crea la etapa "Calificado (llamada)" después de la etapa de cita agendada.
3. Automation → Workflows → "Meta CAPI · Lead calificado":
   - Cambia el disparador: quita el de "Hiring or job seeking" y pon "Pipeline Stage Changed" → ese pipeline → etapa "Calificado (llamada)" (o la equivalente que ya exista).
   - No cambies la acción de Meta (mismo píxel, mismo evento CompleteRegistration, mismo token).
4. Guarda y publica. Dime el nombre exacto de la etapa que quedó como disparador, para avisarle a ventas.

PARTE 2 · Validar el email en los formularios nuevos
En los formularios "Orchid · BF Healthcare", "Orchid · BF Entrepreneurs" y "Orchid · Newsletter":
1. Abre el campo Email y revisa qué opciones de validación ofrece GHL (por ejemplo "validate email", "block disposable emails" o verificación de email de LeadConnector).
2. Activa la que sea gratis. Si la única es de pago, NO la actives: dime el costo.
3. Guarda los tres formularios.

PARTE 3 · Pregunta obligatoria con el nombre del negocio
1. En "Orchid · BF Healthcare" agrega, después del tipo de consultorio, un campo de texto obligatorio: "Practice name or website".
2. En "Orchid · BF Entrepreneurs" agrega, después del tipo de negocio, un campo de texto obligatorio: "Business name or website".
3. Crea cada uno como campo personalizado nuevo (Practice name / Business name). No uses ni cambies el campo "Vertical" ni otros existentes.
4. No cambies nada más del formulario (preguntas, orden, evento de píxel, redirección a la página de gracias).
5. Guarda y confirma en https://go.orchidpros.com/practices-free-month y https://go.orchidpros.com/business-free-month que el campo nuevo aparece. No envíes el formulario.

AL TERMINAR, dime:
- Si el contacto quedó con la etiqueta lead-falso y la hora de su cita.
- Las etapas del pipeline y cuál quedó como disparador del CAPI.
- Qué validación de email activaste (o el costo si era de pago).
- Si los campos nuevos aparecen en las dos landings.
