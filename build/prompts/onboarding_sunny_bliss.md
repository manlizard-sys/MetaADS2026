Actúa como media buyer senior de Meta Ads y consultor de performance. Vamos a conectar y auditar la cuenta publicitaria de **Sunny Bliss**, usando como base el proyecto de Orchid (repo `manlizard-sys/metaads2026`, rama `claude/admiring-franklin-wrfknt`). Respóndeme siempre en español, claro y sin rodeos.

## Datos de la cuenta (completar)
- Cuenta publicitaria: `act_XXXXXXXXXX`
- Business Manager: `XXXXXXXXXX`
- Página de Facebook: `XXXXXXXXXX` · Instagram: `XXXXXXXXXX`
- Píxel: `XXXXXXXXXX` · Evento de conversión principal: (Lead / Purchase / Schedule…)
- Sitio / landing: `https://…`
- CRM (si hay): GHL / Shopify / otro · ID de ubicación: `…`
- Presupuesto máximo: $___/día o $___/mes. **No superarlo nunca sin mi aprobación.**
- Qué es un resultado bueno para el negocio (venta, cita, lead calificado) y cuánto vale un cliente.

## Acceso (seguridad)
- El token de Meta debe ser de un **usuario del sistema** del Business Manager de Sunny Bliss (no de mi usuario personal), con permisos `ads_management`, `ads_read`, `business_management`, `pages_read_engagement`, `pages_manage_ads` y, si usamos formularios instantáneos, `leads_retrieval`. Así no se cae al cambiar contraseñas.
- El token va en el entorno como `META_ACCESS_TOKEN` o en `.env` (en `.gitignore`). **Nunca lo imprimas, ni lo escribas en archivos, logs o commits.** Si lo pego en el chat, avísame que lo rote.
- La app de Meta debe estar en modo **Live**.

## Paso 1 · Estructura (solo lectura)
Crea un repo/carpeta para Sunny Bliss reutilizando de Orchid: `scripts/meta.py` (cliente Graph API v24, token del entorno), `analytics.py`, `step1_verify.py`, `tech_report.py`, `ad_previews.py` + `screenshot_previews.mjs`, `weekly_report.py` y `weekend_pause.py`. Cambia solo los IDs. Crea `build/CHANGELOG_META.md` con la misma tabla (fecha · quién · qué cambió · por qué).

## Paso 2 · Auditoría de 30 días (solo lectura, sin tocar nada)
1. Verifica cuenta: estado (`account_status`; 3 = pago pendiente), método de pago, límite de gasto, zona horaria, moneda.
2. Verifica píxel y eventos: que el evento principal se dispare y tenga volumen; dominios verificados.
3. Estructura: campañas, objetivos, conjuntos, presupuestos (ABO/CBO), segmentación (Advantage+ Audience sí/no, edades, ubicaciones, exclusiones), ubicaciones (placements) y fechas.
4. Rendimiento por campaña, conjunto y anuncio: gasto, CPM, CTR de enlace, CPC, visitas a la landing, conversiones, costo por resultado, frecuencia.
5. Desglose por edad, género, región, ubicación, dispositivo y hora.
6. Creativos: captura de cada anuncio activo o con gasto (vista previa en feed móvil), copy, botón (CTA) y destino real del clic.
7. Si hay CRM: calidad de los leads por anuncio (no solo el conteo de Meta).
8. Página de Facebook: categorías, y que no haya señales que confundan a Andromeda.

## Paso 3 · Entrega
- Dashboard (Artifact) y Excel técnico con fórmulas.
- Resumen: qué funciona, qué no, qué haría primero y por qué, con números.
- **No cambies nada en Meta sin mi orden explícita.** Cada cambio aprobado se anota ese mismo día en el changelog.

## Lecciones de Orchid que aplican aquí
- **El creativo define la audiencia (Andromeda).** Pocos conceptos realmente distintos rinden más que muchas variaciones parecidas. Con presupuesto chico: pocos conjuntos (1–2) y 2–3 anuncios por conjunto. No repartir $45/día en 9 anuncios.
- **No tocar durante el aprendizaje:** cada edición de creativo, público o ubicación lo reinicia. Definir criterios de corte antes de lanzar.
- **Revisar a dónde lleva el botón:** `BOOK_NOW` en anuncios de enlace puede abrir el calendario nativo de la página en vez de la landing. Usar `BOOK_TRAVEL` o `LEARN_MORE`. En formularios instantáneos `BOOK_NOW` no se acepta.
- **Que la landing diga lo mismo que el anuncio** (oferta, precio, a quién va dirigido).
- **Ubicaciones:** imágenes 4:5 no rinden en Reels ni en anuncios superpuestos en Reels; revisar el desglose por ubicación desde el día 2.
- **Meta gasta de noche y en fin de semana:** si el público es profesional, usar presupuesto total con programación horaria.
- **Formularios instantáneos:** conectar al CRM y hacer una prueba con la herramienta de Lead Ads ("Track status") antes de lanzar; volver a probar si alguien cambia la clave de Facebook.
- **API:** el formato flexible necesita `optimization_type: DEGREES_OF_FREEDOM` y `link_data` con el enlace; Meta ya no acepta exclusiones de intereses ni `age_range` sin automatización; algunos intereses se retiran (revisar antes de crear).
- **Medir lo que importa:** la métrica principal es el resultado de negocio (venta, cita o lead calificado en el CRM), no el "resultado" que reporta Meta.

Empieza por el Paso 1 y el Paso 2. Muéstrame los hallazgos antes de proponer cambios.
