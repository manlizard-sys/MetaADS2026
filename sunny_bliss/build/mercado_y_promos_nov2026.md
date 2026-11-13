# Sunny Bliss · Formulario a GHL, mercado y promociones (noviembre 2026)

> **Actualización 2026-11-06:** electricidad queda **suspendida** por orden del usuario. Las promociones y conceptos eléctricos se guardan aquí y en `build/ads/source/Electrical.dc.html` para retomarlos más adelante. Precios aprobados: AC tune-up $129, reemplazo de AC desde $5,800 (oferta por tiempo limitado), inspección con cámara desde $249, Holiday Guest-Ready $149.

## 1. Conectar el formulario de Meta con GoHighLevel

**Diagnóstico:** los leads del formulario dejaron de llegar el 1 de octubre. La causa más común es que se venció o se perdió la conexión de Facebook dentro de GHL (por ejemplo, la persona que la conectó perdió su rol en la página o cambió su contraseña), o que la página restringió el acceso a leads. Desde aquí no lo puedo confirmar: el usuario del sistema ML_Ads no tiene permiso de leads sobre la página.

### Paso A · Meta Business Suite (5 minutos)
1. Entra a business.facebook.com > **Configuración** > **Integraciones** > **Acceso a clientes potenciales** (Leads Access).
2. Elige la página **Sunny Bliss Plumbing & Air**.
3. Pestaña **CRM**: tiene que aparecer **LeadConnector** (la app de HighLevel). Si dice que el acceso está restringido y LeadConnector no está, agrégalo con **Asignar CRM**.
4. Pestaña **Personas**: la persona que conecta GHL debe tener acceso a leads. Agrégate tú si no estás.
5. Opcional, para que yo pueda vigilar los leads: en **Usuarios del sistema** > ML_Ads > **Asignar activos** > la página, con el permiso de **clientes potenciales**.

### Paso B · GHL, reconectar Facebook (5 minutos)
1. En la subcuenta de Sunny Bliss: **Settings** > **Integrations** > **Facebook & Instagram**.
2. Si aparece conectado, haz **Disconnect** y luego **Connect** con un usuario que sea administrador de la página.
3. Selecciona la página Sunny Bliss y acepta **todos** los permisos que pida, sobre todo el de leads.

### Paso C · GHL, mapear los campos de cada formulario
1. **Settings** > **Integrations** > **Facebook** > **Form Fields Mapping**.
2. Mapea cada pregunta de cada formulario a un campo del contacto: nombre, teléfono, correo, ZIP, servicio y las preguntas de calificación.

| Formulario (ID) | Anuncio |
|---|---|
| 1706144103786572 | L1 · Tank Flush $149 · EN |
| 1042561781716942 | L2 · 0% 60 meses · ES (prospecting y retargeting) |
| 2492686487841896 | L2 · 0% 60 months · EN (prospecting y retargeting) |
| 1554567089328909 | L3 · AC de 25 años · EN |
| 1689115782782234 | L5 · Instalación $5,800 · ES |

### Paso D · GHL, workflow para saber qué anuncio trajo cada lead
Cada anuncio usa su propio formulario, así que el formulario identifica al anuncio.
1. **Automation** > **Workflows** > nuevo workflow, con el trigger **Facebook Lead Form Submitted**. Usa un filtro por formulario, con un workflow o una rama por cada formulario.
2. Acciones:
   - **Add tag**: `meta-L1-tankflush`, `meta-L2-financing-es`, etc.
   - **Update contact field**: rellena **Ad Name** con el nombre del anuncio. Mi reporte de GHL ya lee ese campo.
   - **Create opportunity**: en el pipeline de leads, etapa **New lead**.
   - **Internal notification**: un SMS al equipo con el nombre y el teléfono, para llamar en menos de 5 minutos.
   - **Send SMS** al lead, en inglés o español según el formulario: "Thanks! A Sunny Bliss tech will call you in the next few minutes."

### Paso E · Prueba
1. Abre la herramienta de prueba de Meta: developers.facebook.com/tools/lead-ads-testing.
2. Elige la página y un formulario, y crea un lead de prueba.
3. En menos de un minuto tiene que aparecer en GHL con su etiqueta y su oportunidad. Repite con un segundo formulario.
4. Avísame y lo verifico con el reporte de GHL. Después borras los leads de prueba.

---

## 2. El mercado: 21 ZIP codes del sur y el este de Miami-Dade

### Quién vive aquí
- **Edad:** es un mercado maduro. La edad mediana es de 44 años en Pinecrest, Kendall y Palmetto Bay. En Kendall el **20.9%** de los residentes tiene 65 años o más, y en Pinecrest el **17.7%**. Coral Gables es algo más joven (mediana de 39), porque ahí está la Universidad de Miami.
- **Ingreso:** Pinecrest, Coral Gables, Key Biscayne y South Miami concentran ingresos altos y casas propias de gran valor. Kendall, Cutler Bay y Miami Shores son de clase media propietaria.
- **Idioma:** la mayoría de los hogares de Miami-Dade son hispanos. En esta cuenta, los anuncios en español tuvieron el costo por lead más bajo ($27.72). El español es una ventaja, no una traducción.
- **Veteranos:** hay unos **44,000 en todo Miami-Dade**, cerca del 2% de la población, y la cifra viene bajando. La mayoría son adultos mayores.

### Antigüedad de las casas (lo más importante para eléctrico y plomería)

| Zona | Año mediano de construcción | Qué significa |
|---|---|---|
| Coral Gables (33134 centro) | 1951 a 1968; 12% de las casas son de antes de 1940 | Paneles de 100A, cableado viejo, tuberías de hierro fundido bajo el piso |
| Coral Gables (33146) | 1956 | Igual |
| Pinecrest (33156) | 1969 a 1972 | Época de los paneles Federal Pacific y Zinsco, y del cableado de aluminio (1965 a 1973) |
| Kendall, Palmetto Bay | Sobre todo 1960 a 1985 | Muchos sistemas originales o de segunda generación |
| Cutler Bay y el sur de Palmetto Bay | Reconstruidas tras el huracán Andrew (1992) | Equipos y paneles de 1993 a 1996, ya con más de 30 años: ola de reemplazo |

**Conclusión:** el cliente típico es dueño de una casa de 50 a 70 años con equipos que nadie revisa hasta que fallan o hasta que el seguro los rechaza.

### El seguro como motor de ventas (clave para eléctrico)
- Las aseguradoras de Florida piden una **inspección de 4 puntos** (techo, electricidad, plomería y A/C) en casas de más de 20 a 30 años, al contratar o renovar.
- Los paneles **Federal Pacific (Stab-Lok)** y **Zinsco** suelen causar rechazo directo. El cableado de **aluminio** genera recargos o rechazos.
- Cambiar un panel cuesta entre $2,500 y $6,000. Es un trabajo grande, urgente y con fecha límite (la renovación), ideal para Meta.
- La recertificación de 40/30 años de Miami-Dade **no aplica a casas unifamiliares**, solo a edificios. No sirve como gancho para este público.

### Servicios eléctricos con más demanda en esta zona
1. **Cambio y mejora de panel** (Federal Pacific, Zinsco, 100A a 200A): por el seguro y por la carga moderna.
2. **Correcciones eléctricas de la inspección de 4 puntos**.
3. **Generador con transfer switch** ($7,000 a $13,000): el invierno es el momento de planear antes de junio.
4. **Protección contra sobretensión para toda la casa**: Florida es la capital de los rayos en EE. UU.
5. **Cargador de auto eléctrico Nivel 2** ($1,500 a $2,800): casi siempre necesita revisar o mejorar el panel.
6. GFCI y tomas exteriores, iluminación, ventiladores y revisión de seguridad.

### La temporada: noviembre a marzo
- **Temporada seca y fresca:** el A/C baja de uso pero no se apaga. Es la temporada del mantenimiento y del reemplazo planificado, sin urgencia ni calor.
- **Frentes fríos:** las noches frías hacen que se usen las resistencias de calefacción y la bomba de calor. Llegan llamadas por olor a quemado o porque la calefacción no funciona.
- **Agua caliente:** el agua entra más fría y el calentador trabaja más. Por eso el Tank Flush funciona en invierno.
- **Fiestas y visitas:** más uso de baños y cocina, con drenajes tapados y calentadores que no alcanzan.
- **Residentes de temporada (snowbirds):** vuelven a Miami Beach y Key Biscayne. Encuentran casas cerradas por meses, con moho, drenajes del A/C tapados o grifos que gotean.
- **El Niño, invierno húmedo:** más lluvia de lo normal, con filtraciones, drenajes exteriores y tomas exteriores mojadas (GFCI).
- **Fin de la temporada de huracanes (30 de noviembre):** el mejor momento para vender generadores y protección contra sobretensión es antes del 1 de junio, sin la urgencia que dispara los precios.
- **Renovaciones del seguro:** son todo el año. Las casas viejas reciben la carta de inspección y necesitan corregir algo para conservar la póliza.

### ¿Una campaña para retirados y veteranos?
**Sí, pero como un conjunto de anuncios dentro de la campaña de leads, no como una campaña aparte.** Empezaría después de las dos primeras semanas.

- **Retirados (60+):**
  - Son 1 de cada 5 residentes de Kendall, y la mayoría es dueña de su casa sin hipoteca.
  - Tienen las casas más viejas, valoran la confianza y prefieren hablar por teléfono.
  - Meta **sí permite segmentar por edad** en servicios para el hogar. Es un público grande dentro de los 21 ZIP codes.
- **Veteranos:**
  - Meta **no permite segmentar por estatus militar**.
  - Son el 2% de la población, demasiado pocos para una campaña propia.
  - La solución es incluirlos en la oferta: "Seniors and veterans save 10%". Funciona como mensaje de confianza para todos, y un hijo adulto también lo ve y se lo pasa a su papá.
- **Regla de Meta, atributos personales:** no se puede escribir "¿Eres veterano?", "¿Estás jubilado?" ni "Para personas de tu edad". Sí se puede: "Seniors and veterans save 10% on every service". La oferta describe el servicio, no a la persona.
- **Creativo:** un cliente mayor real hablando a cámara. El técnico explica sin presión y entrega un presupuesto por escrito. Técnicos con licencia, verificados y bilingües. El "Safety Check" gratis abre la puerta a panel, calentador y A/C.
- **Presupuesto:** unos $10 al día dentro de la campaña de leads, desde la semana 3, sin subir el tope.

---

## 3. Promotions to propose to Mehdi (English)

Prices marked [$__] need Mehdi's approval. Proven offers are marked ✓.

| # | Promotion | Service | Why now | Meta angle |
|---|---|---|---|---|
| 1 | **Winter Home Check** [$__]: AC tune-up + plumbing inspection + electrical safety check in one visit | All three | Launches electrical with a low-cost entry offer; one visit shows the age of every system | Lead campaign hero offer |
| 2 | **Tank Flush $149** ✓ | Plumbing | Colder water makes heaters work harder in winter; 17 leads at $48 each | Keep running |
| 3 | **0% interest for 60 months** on AC replacement ✓ | HVAC | Best ad in the account ($27.72 per lead in Spanish); planned replacement season | Keep running, EN + ES |
| 4 | **Insurance-Ready Electrical Inspection** [$__], credited toward any repair | Electrical | Florida insurers ask for 4-point inspections on homes over 20 to 30 years; most homes here are from the 1950s to 1970s | "Keep your home insurable" |
| 5 | **Panel Replacement** [$__] off Federal Pacific, Zinsco or 100A panels, permit included | Electrical | These panels lead to insurance declines; a $2,500 to $6,000 job | Photo of an old panel next to a new one |
| 6 | **Generator Season Pre-Booking**: book by Feb 28, install before June, [$__] off or free transfer switch | Electrical | Hurricane season ends Nov 30; best time to plan without storm pricing | Retargeting and awareness |
| 7 | **Whole-Home Surge Protector** [$__] with any electrical service | Electrical | Florida leads the US in lightning; protects AC, TVs and appliances | Add-on and upsell |
| 8 | **Seniors and Veterans Save 10%**, every service, every day | All three | 1 in 5 residents in Kendall is 65+; builds trust | Dedicated 60+ ad set, policy-safe copy |
| 9 | **Bliss Care Plan** [$__]/month: 2 AC visits, 1 plumbing visit, 1 electrical safety check, priority service, no dispatch fee | All three | Turns one-time jobs into recurring revenue | Retargeting (R1) |
| 10 | **Holiday Guest-Ready** [$__] drain cleaning + water heater check | Plumbing | Guests, cooking and showers stress drains in Nov and Dec | Seasonal, Nov 15 to Dec 31 |
| 11 | **Back-in-Town Home Check** [$__] for seasonal residents | All three | Snowbirds return to Miami Beach and Key Biscayne to homes closed for months | Miami Beach and Key Biscayne ZIPs only |
| 12 | **EV Charger Install** from [$__], panel check included | Electrical | Growing demand, and most 1960s to 1980s homes need a panel review first | Coral Gables, Pinecrest and Key Biscayne |

**Questions for Mehdi before electrical ads run:**
1. Electrical contractor license number (EC or ER), which must appear on ads and the landing page.
2. Which electrical services the team does in-house, and which ones are subcontracted.
3. Approved prices for promotions 1, 4 to 12.
4. Lender terms for the 0% financing (required in the ad text).
5. Who answers electrical calls, and how fast.

---

Sources:
- Census Reporter, Coral Gables profile: censusreporter.org/profiles/16000US1214250-coral-gables-fl
- Wikipedia, 2020 census data: Pinecrest, Kendall, Palmetto Bay
- Point2Homes, median year built (ACS 2019 to 2023): Coral Gables, Pinecrest
- Elizabeth Costare, Coral Gables Market Report Q2 2026
- US Census QuickFacts, Miami-Dade County (veterans)
- CoolToday, "Dangerous Breaker Panels"
- latentinsure.com, Florida 4-point inspection
- Miami-Dade County, 40-year recertification
- ACHR News, snowbird HVAC services
- Lindstrom Air, South Florida winter tips
- Miami electrical cost guide (vanderflip-home.pages.dev), generator, EV charger and panel costs
- Third-party guides on Meta's personal attributes policy (stackmatix.com, auditsocials.com)
