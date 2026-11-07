# Sunny Bliss · Lanzamiento v2 (noviembre 2026)

Todo está creado **en pausa**. Se activa solo con la orden del usuario y después de que los formularios lleguen a GHL.

## Estructura

| Campaña | Conjunto | Presupuesto inicial | Anuncios |
|---|---|---|---|
| SB · Leads · Nov 2026 v2 (80%) | 21 ZIP de Mehdi, 25+, Advantage+ audience, inglés y español, formulario Higher Intent | $53/día | 4 ofertas × EN/ES = 8 |
| SB · Awareness · Reviews · Nov 2026 v2 (20%) | 21 ZIP, 25+, alcance | $13/día | 2 conceptos × EN/ES = 4 |
| **Total** | | **$66/día ≈ $2,000/mes** | 12 |

Ofertas de leads:
- TU: mantenimiento de A/C a $129 (antes $325)
- SI: plan Silver con 50% de descuento, $150 al año (antes $300)
- AC: A/C nuevo desde $5,800 por tiempo limitado, con 0% de interés por 60 meses
- FL: Tank Flush $149 (antes $279)

Awareness:
- A1: el equipo 4.9 estrellas de Miami
- A2: más de 1,000 reseñas de 5 estrellas

## Aumento semanal (+$50 por semana, hasta $3,000 al mes)

Se cuenta desde el día de la activación. Cada aumento mantiene el reparto de 80% leads y 20% awareness.

| Semana | Total/día | Leads | Awareness | Ritmo mensual |
|---|---|---|---|---|
| 1 | $66 | $53 | $13 | $2,000 |
| 2 | $73 | $58 | $15 | $2,220 |
| 3 | $80 | $64 | $16 | $2,430 |
| 4 | $87 | $70 | $17 | $2,650 |
| 5 | $94 | $75 | $19 | $2,860 |
| 6 en adelante | $99 | $79 | $20 | $3,000 (tope) |

Cada aumento es de un 10% aproximado. Andromeda y la fase de aprendizaje toleran bien subidas menores al 20% semanal. Si el costo por lead calificado de una semana sale más del doble del objetivo ($60), la subida de esa semana se frena y se revisan los creativos.

## Reglas de Andromeda aplicadas

1. **Estructura consolidada:** una campaña y un solo conjunto de leads, sin dividir por idioma, servicio ni retargeting. Andromeda aprende más rápido con todo el presupuesto junto.
2. **Segmentación amplia:** la única restricción fija son los 21 ZIP que pidió Mehdi. Edad 25+ y Advantage+ audience activado. El creativo hace la segmentación.
3. **Diversidad real de creativos:** cuatro conceptos distintos (precio de temporada, plan anual, reemplazo con financiamiento y plomería), con fondos, fotos y estructuras diferentes. Andromeda agrupa como uno solo los anuncios que se ven parecidos, así que no se hacen variantes de texto sobre la misma plantilla.
4. **Mensaje claro en la imagen:** el servicio, el precio y la oferta se leen en un segundo. El texto del anuncio repite la oferta, y el formulario la vuelve a mostrar en la tarjeta de contexto.
5. **Calidad del lead:**
   - formulario **Higher Intent**, con una pantalla de revisión antes de enviar;
   - preguntas de calificación: qué necesita, si es dueño de la casa, cuándo lo quiere y la edad del A/C en la oferta de reemplazo;
   - se excluye a quien ya envió un formulario en los últimos 90 días.
6. **Siguiente paso (Conversion Leads):** cuando GHL esté conectado y marque las etapas (calificado, estimado agendado, vendido), conectar la Conversions API para CRM y optimizar por lead calificado. Meta reporta alrededor de 21% menos costo por lead de calidad con ese objetivo.
7. **Renovación de creativos:** con Andromeda la fatiga llega antes, en 2 a 3 semanas. A partir de la semana 3 entran conceptos nuevos (inspección con cámara $249, Holiday Guest-Ready $149) y sale el de peor resultado. También conviene sumar versiones 9:16 para Reels y Stories.

## Formularios: mapa para el workflow de GHL

Cada formulario manda con cada lead `utm_source=facebook`, `utm_medium=paid_social`, `utm_campaign=sb_leads_nov2026_v2` y `utm_content=<oferta>_<idioma>` (por ejemplo `tu_en`). Los anuncios de awareness llevan a sunnybliss.com con `utm_source=facebook&utm_medium=paid_social&utm_campaign={{campaign.name}}&utm_content={{ad.name}}`. Los 8 primeros formularios (sin UTM) quedaron archivados.

| Formulario | Anuncio | Etiqueta sugerida en GHL |
|---|---|---|
| 1643919603937060 | TU · Mantenimiento $129 · EN | meta-tu-en |
| 1152152620696238 | TU · Mantenimiento $129 · ES | meta-tu-es |
| 1505083551681279 | SI · Plan Silver 50% · EN | meta-si-en |
| 1587832526363738 | SI · Plan Silver 50% · ES | meta-si-es |
| 1184339093920318 | AC · A/C nuevo desde $5,800 · EN | meta-ac-en |
| 1374469254565758 | AC · A/C nuevo desde $5,800 · ES | meta-ac-es |
| 1537487624893874 | FL · Tank Flush $149 · EN | meta-fl-en |
| 2154961215229218 | FL · Tank Flush $149 · ES | meta-fl-es |

## Antes de activar

1. **GHL:** los leads del formulario llegan a Meta pero no aparecen en GHL desde octubre. La causa no está confirmada: la revisión del 2026-11-06 que decía que la página no tenía ninguna app suscrita era un error de permiso mal leído. Hay que reconectar Facebook en GHL, mapear estos 8 formularios y probar con un lead de prueba.
2. **Teléfono:** el botón de llamada del formulario usa el +1 305-707-6081, igual que los formularios anteriores. La web muestra el 305-504-6091. Hay que confirmar cuál quiere Mehdi.
3. **Revisión de Meta:** los 12 anuncios están en revisión. Se activan cuando estén aprobados.

Fuentes: confect.io, segwise.ai, theoptimizer.io, adsuploader.com y jetfuel.agency (Andromeda 2026); clickheredigital.com y lilachbullock.com (Conversion Leads). Son guías de agencias y proveedores, no documentación oficial de Meta.
