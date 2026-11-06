# Bitácora de cambios · Meta Ads Sunny Bliss

Registro de todo lo que se cambia en la cuenta de Sunny Bliss (ID pendiente de confirmar), en orden cronológico, con el motivo de cada cambio.
Los informes semanales leen este archivo para explicar qué se hizo cada semana.
**Regla:** cada vez que se cambia algo en Meta, en el formulario o en el seguimiento, se agrega una línea aquí el mismo día.
Las horas están en la zona horaria de la cuenta.

| Fecha | Quién | Qué cambió | Por qué |
|---|---|---|---|
| 2026-10-30 | Claude | Se crea la carpeta `sunny_bliss/` con los scripts de lectura reutilizados de Orchid (IDs en `scripts/config.py`). No se tocó la cuenta. | Onboarding. |
| 2026-10-30 | Claude | Auditoría de 30 días (30 sep – 29 oct), solo lectura. IDs confirmados: cuenta act_406803358900425, página 115885981512163, Instagram 17841463167723871, píxel de landing 1576525677606884. Dashboard, Excel técnico y capturas de anuncios. No se cambió nada en Meta. | Onboarding. |
| 2026-10-30 11:40 | Claude (orden del dueño) | **Todas las campañas activas pausadas** a nivel campaña: "HVAC Landing – 2026-10-08 – EN + ES – CBO" ($60/día, ya sin conjuntos activos), "SB – Plumbing Leads – Instant Form – Sep 24" ($30/día) y "Sunny Bliss – Tech Hiring – HVAC & Plumbing – Aug 2026" ($40/día). La cuenta queda sin gasto. Respaldo: `build/backup-2026-10-30-before-pause-all.json`. Script: `scripts/pause_all.py`. | Preparar la nueva campaña hiperlocal (18 ZIP en Coral Gables, Miami Beach, Miami Shores, Pinecrest, South Miami, Cutler Bay, Key Biscayne y Palmetto Bay). |
| 2026-11-06 | Claude (orden del usuario: "empecemos") | **Creadas en PAUSA, sin gasto:** "SB · Awareness · Top-rated · Nov 2026" (alcance, $12/día, 21 ZIP, 30-65, anuncios A1 Vecinos y A2 Reseñas en video, con creativos nuevos hechos desde los posts originales, sin el botón de formulario) y "SB · Leads · Nov 2026" (ABO: Prospecting $40/día con L1 Tank Flush $149, L2 0% 60 meses ES y EN, L3 AC de 25 años, L5 Instalación $5,800 ES; Retargeting $8/día con visitantes web 180d y seguidores FB/IG 365d, 2 anuncios de financiamiento). Excluye a quienes enviaron formulario en 90d. Total $60/día (ritmo de $1,800/mes). IDs en `build/ids.json`. Script: `scripts/launch_nov2026.py`. Las campañas de hiring no se tocaron. | Plan de dos semanas para juntar datos (`build/concepts_nov2026.md`). Se activan solo con la orden del usuario y cuando el formulario llegue a GHL. |
