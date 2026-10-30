"""Step 2 structure audit for Sunny Bliss (read-only).

Campaigns (objective, CBO/ABO budget), ad sets (optimization, Advantage+ Audience, ages, geo,
exclusions, placements, dates) and ads (copy, CTA, real click destination), with flags for the
lessons learned on Orchid. Writes build/reports/structure-<today>.json and .md.
Usage: python3 audit_structure.py
"""
import datetime as dt, json, sys
import config as C
from meta import get, get_all, MetaError, BUILD

C.require("AD_ACCOUNT")
ACT = C.AD_ACCOUNT
money = lambda cents: f"${int(cents) / 100:,.2f}" if cents else "-"

try:
    camps = get_all(f"{ACT}/campaigns", limit=200, fields="id,name,objective,status,effective_status,buying_type,"
                    "daily_budget,lifetime_budget,bid_strategy,special_ad_categories,start_time,stop_time,created_time")
    adsets = get_all(f"{ACT}/adsets", limit=500, fields="id,name,campaign_id,status,effective_status,daily_budget,"
                     "lifetime_budget,optimization_goal,billing_event,bid_strategy,promoted_object,destination_type,"
                     "targeting,attribution_spec,pacing_type,adset_schedule,start_time,end_time,learning_stage_info")
    ads = get_all(f"{ACT}/ads", limit=500, fields="id,name,adset_id,campaign_id,status,effective_status,"
                  "creative{id,name,object_type,call_to_action_type,object_story_spec,asset_feed_spec,url_tags,"
                  "effective_object_story_id}")
except MetaError as e:
    sys.exit(f"API ERROR:\n{e}")


def creative_info(c):
    """Copy, CTA and click destination, whichever creative format it is."""
    oss, afs = c.get("object_story_spec") or {}, c.get("asset_feed_spec") or {}
    link = oss.get("link_data") or {}
    video = oss.get("video_data") or {}
    cta = link.get("call_to_action") or video.get("call_to_action") or {}
    dest = (cta.get("value") or {}).get("link") or link.get("link")
    if afs:
        dest = dest or next((u.get("website_url") for u in afs.get("link_urls", [])), None)
    return {
        "format": "flexible/dinámico" if afs else ("video" if video else "imagen/carrusel" if link else c.get("object_type")),
        "cta": c.get("call_to_action_type") or cta.get("type") or next(iter(afs.get("call_to_action_types", [])), None),
        "destination": dest or ("formulario instantáneo" if (cta.get("value") or {}).get("lead_gen_form_id") else None),
        "lead_form": (cta.get("value") or {}).get("lead_gen_form_id"),
        "primary_text": link.get("message") or video.get("message") or next((b["text"] for b in afs.get("bodies", [])), None),
        "headline": link.get("name") or video.get("title") or next((t["text"] for t in afs.get("titles", [])), None),
        "url_tags": c.get("url_tags"),
    }


flags = []
for s in adsets:
    t = s.get("targeting") or {}
    adv = (t.get("targeting_automation") or {}).get("advantage_audience")
    s["_summary"] = {
        "advantage_audience": {1: "sí", 0: "no"}.get(adv, "sin dato"),
        "ages": f"{t.get('age_min', '?')}-{t.get('age_max', '?')}",
        "genders": t.get("genders") or "todos",
        "geo": t.get("geo_locations"),
        "excluded_geo": t.get("excluded_geo_locations"),
        "custom_audiences": [a.get("name") for a in t.get("custom_audiences", [])],
        "excluded_audiences": [a.get("name") for a in t.get("excluded_custom_audiences", [])],
        "interests": [i.get("name") for f in t.get("flexible_spec", []) for i in f.get("interests", [])],
        "placements": "Advantage+ (automáticas)" if not t.get("publisher_platforms") else {
            "plataformas": t.get("publisher_platforms"), "facebook": t.get("facebook_positions"),
            "instagram": t.get("instagram_positions"), "audience_network": t.get("audience_network_positions"),
            "messenger": t.get("messenger_positions")},
        "budget": money(s.get("daily_budget")) + "/día" if s.get("daily_budget") else money(s.get("lifetime_budget")) + " total",
        "learning": (s.get("learning_stage_info") or {}).get("status"),
    }
for a in ads:
    a["_c"] = creative_info(a.get("creative") or {})
    live = a["effective_status"] in ("ACTIVE", "WITH_ISSUES", "PENDING_REVIEW")
    if live and a["_c"]["cta"] == "BOOK_NOW" and not a["_c"]["lead_form"]:
        flags.append(f"{a['name']}: botón BOOK_NOW en anuncio de enlace; puede abrir el calendario nativo de la página "
                     "en vez de la landing. Verificar en el celular.")
    if live and C.LANDING and a["_c"]["destination"] and C.LANDING.split("//")[-1].split("/")[0] not in a["_c"]["destination"]:
        flags.append(f"{a['name']}: el clic lleva a {a['_c']['destination']}, no a la landing configurada.")
    if live and not a["_c"]["url_tags"] and not a["_c"]["lead_form"]:
        flags.append(f"{a['name']}: sin parámetros UTM; el CRM no podrá atribuir el lead al anuncio.")
    if a["effective_status"] in ("DISAPPROVED", "WITH_ISSUES"):
        flags.append(f"{a['name']}: estado {a['effective_status']}.")
live_by_set = {}
for a in ads:
    if a["effective_status"] == "ACTIVE":
        live_by_set[a["adset_id"]] = live_by_set.get(a["adset_id"], 0) + 1
for s in adsets:
    n = live_by_set.get(s["id"], 0)
    if s["effective_status"] == "ACTIVE" and n > 4:
        flags.append(f"{s['name']}: {n} anuncios activos en un conjunto; con presupuesto chico conviene 2–3 conceptos distintos.")
if sum(1 for s in adsets if s["effective_status"] == "ACTIVE") > 2:
    flags.append("Más de 2 conjuntos activos: el presupuesto se reparte y ninguno sale de aprendizaje.")

# ---------------------------------------------------------------- output
by_camp = {c["id"]: c for c in camps}
L = [f"# Estructura de la cuenta {ACT} · {dt.date.today()}", ""]
for c in camps:
    budget = (money(c.get("daily_budget")) + "/día" if c.get("daily_budget") else
              money(c.get("lifetime_budget")) + " total" if c.get("lifetime_budget") else None)
    L += [f"## {c['name']}", f"- Estado: {c['effective_status']} · objetivo {c['objective']} · "
          f"{'CBO ' + budget if budget else 'ABO (presupuesto por conjunto)'} · creada {c['created_time'][:10]}"]
    for s in (x for x in adsets if x["campaign_id"] == c["id"]):
        m = s["_summary"]
        L += [f"### Conjunto: {s['name']}",
              f"- Estado: {s['effective_status']} · presupuesto {m['budget'] if not budget else 'de la campaña'} · "
              f"optimiza {s.get('optimization_goal')} · evento {json.dumps(s.get('promoted_object'), ensure_ascii=False)}",
              f"- Advantage+ Audience: {m['advantage_audience']} · edades {m['ages']} · géneros {m['genders']} · aprendizaje: {m['learning']}",
              f"- Ubicación geográfica: {json.dumps(m['geo'], ensure_ascii=False)}",
              f"- Públicos: {m['custom_audiences'] or '-'} · excluidos: {m['excluded_audiences'] or '-'} · intereses: {m['interests'] or '-'}",
              f"- Ubicaciones: {json.dumps(m['placements'], ensure_ascii=False)}",
              f"- Fechas: {s.get('start_time', '')[:10]} → {(s.get('end_time') or 'sin fin')[:10]} · programación horaria: "
              f"{'sí' if s.get('adset_schedule') else 'no'}"]
        for a in (x for x in ads if x["adset_id"] == s["id"]):
            ci = a["_c"]
            L += [f"  - **{a['name']}** ({a['effective_status']}) · {ci['format']} · CTA {ci['cta']} · destino {ci['destination']}",
                  f"    - Titular: {ci['headline']!r} · Texto: {(ci['primary_text'] or '')[:160]!r}"]
    L.append("")
L += ["## Alertas de estructura"] + ([f"- {f}" for f in flags] or ["- Sin alertas."])

out = BUILD / "reports"
out.mkdir(parents=True, exist_ok=True)
stamp = dt.date.today().isoformat()
(out / f"structure-{stamp}.json").write_text(json.dumps({"campaigns": camps, "adsets": adsets, "ads": ads, "flags": flags},
                                                        indent=2, ensure_ascii=False), encoding="utf-8")
(out / f"structure-{stamp}.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L))
