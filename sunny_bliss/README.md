# Sunny Bliss · Meta Ads

Scripts de solo lectura reutilizados de Orchid. Todos los IDs viven en `scripts/config.py` o en variables de entorno.

## Conectar
1. Token de un **usuario del sistema** del Business Manager de Sunny Bliss (`ads_management`, `ads_read`,
   `business_management`, `pages_read_engagement`, `pages_manage_ads`; `leads_retrieval` si hay formularios instantáneos).
2. Guardarlo en `sunny_bliss/.env` como `META_ACCESS_TOKEN=...` o como secreto del entorno `SUNNY_META_ACCESS_TOKEN`.
   La variable `META_ACCESS_TOKEN` del entorno es de Orchid y estos scripts no la usan.
3. IDs: `SUNNY_AD_ACCOUNT`, `SUNNY_BUSINESS_ID`, `SUNNY_PAGE_ID`, `SUNNY_IG_ID`, `SUNNY_PIXEL`, `SUNNY_EVENT`
   (LEAD / PURCHASE / SCHEDULE / COMPLETE_REGISTRATION), `SUNNY_LANDING`.

## Auditoría (todo solo lectura, desde `sunny_bliss/scripts`)
```
python3 step1_verify.py      # token, cuenta, pago, límite de gasto, píxel, dominios, página
python3 audit_structure.py   # campañas, conjuntos, segmentación, ubicaciones, CTA y destino de cada anuncio
python3 analytics.py         # 30 días: dashboard HTML + CSV (campaña, anuncio, edad, género, región, ubicación, dispositivo, hora)
python3 tech_report.py       # Excel técnico con fórmulas
python3 ad_previews.py       # capturas de cada anuncio en feed móvil
python3 weekly_report.py     # semana vs. semana anterior
```
`weekend_pause.py` **sí escribe** en Meta: solo con orden explícita del dueño, y se anota en `build/CHANGELOG_META.md`.
