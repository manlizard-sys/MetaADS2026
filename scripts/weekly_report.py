"""Weekly Meta Ads performance report for OrchidPros (read-only).

Compares the last complete week (Mon-Sun, account timezone) with the week before, at account, campaign
and ad level. Writes build/reports/<monday>.md and .json. Never modifies anything in the ad account.

Usage: python3 weekly_report.py [--end YYYY-MM-DD]   (end = the Sunday that closes the week; default: last Sunday)
"""
import datetime as dt, json, pathlib, sys
import config as C
from meta import get, get_all, MetaError, BUILD

FIELDS = ("campaign_id,campaign_name,ad_id,ad_name,spend,impressions,reach,frequency,inline_link_clicks,"
          "inline_link_click_ctr,cpm,actions,video_p25_watched_actions,video_p100_watched_actions")
LEAD_TYPES = ("lead", "offsite_conversion.fb_pixel_lead", "onsite_conversion.lead_grouped")
SCHEDULE_TYPES = ("schedule", "offsite_conversion.fb_pixel_schedule", "offsite_conversion.fb_pixel_custom")


def week_bounds():
    if "--end" in sys.argv:
        end = dt.date.fromisoformat(sys.argv[sys.argv.index("--end") + 1])
    else:
        today = dt.date.today()
        end = today - dt.timedelta(days=today.weekday() + 1)  # last Sunday
    start = end - dt.timedelta(days=6)
    return (start, end), (start - dt.timedelta(days=7), start - dt.timedelta(days=1))


def action(row, types):
    acts = {a["action_type"]: float(a["value"]) for a in row.get("actions") or []}
    for t in types:  # first matching type only, to avoid double counting
        if t in acts:
            return acts[t]
    return 0.0


def first(row, key):
    v = row.get(key) or []
    return float(v[0]["value"]) if v else 0.0


def metrics(rows):
    spend = sum(float(r.get("spend", 0)) for r in rows)
    imp = sum(float(r.get("impressions", 0)) for r in rows)
    clicks = sum(float(r.get("inline_link_clicks", 0)) for r in rows)
    leads = sum(action(r, LEAD_TYPES) for r in rows)
    p25 = sum(first(r, "video_p25_watched_actions") for r in rows)
    p100 = sum(first(r, "video_p100_watched_actions") for r in rows)
    return {
        "spend": round(spend, 2), "impressions": int(imp), "link_clicks": int(clicks), "leads": int(leads),
        "cpl": round(spend / leads, 2) if leads else None,
        "ctr": round(100 * clicks / imp, 2) if imp else None,
        "cpm": round(1000 * spend / imp, 2) if imp else None,
        "cpc": round(spend / clicks, 2) if clicks else None,
        "lead_rate": round(100 * leads / clicks, 2) if clicks else None,
        "hook": round(100 * p25 / imp, 1) if imp else None,
        "hold": round(100 * p100 / imp, 1) if imp else None,
        "frequency": max((float(r.get("frequency", 0)) for r in rows), default=0),
    }


def fetch(rng):
    tr = json.dumps({"since": rng[0].isoformat(), "until": rng[1].isoformat()})
    return get_all(f"{C.AD_ACCOUNT}/insights", level="ad", time_range=tr, fields=FIELDS, limit=500)


def delta(cur, prev, lower_is_better=False):
    if cur is None or prev in (None, 0):
        return ""
    pct = 100 * (cur - prev) / prev
    good = pct < 0 if lower_is_better else pct > 0
    return f" ({'+' if pct >= 0 else ''}{pct:.0f}% {'🟢' if good else '🔴' if abs(pct) >= 5 else '⚪'})"


def fmt(v, money=False, pct=False):
    if v is None:
        return "-"
    return f"${v:,.2f}" if money else f"{v}%" if pct else f"{v:,}"


def main():
    cur_rng, prev_rng = week_bounds()
    try:
        acct = get(C.AD_ACCOUNT, fields="name,currency,timezone_name,account_status")
        cur, prev = fetch(cur_rng), fetch(prev_rng)
        active = get_all(f"{C.AD_ACCOUNT}/ads", fields="id,name,effective_status",
                         effective_status=json.dumps(["ACTIVE", "WITH_ISSUES", "DISAPPROVED", "PENDING_REVIEW"]),
                         limit=200)
    except MetaError as e:
        sys.exit(f"API ERROR:\n{e}")

    m, p = metrics(cur), metrics(prev)
    by = lambda rows, key: {k: [r for r in rows if r[key] == k] for k in {r[key] for r in rows}}
    camps_cur, camps_prev = by(cur, "campaign_id"), by(prev, "campaign_id")
    ads_cur, ads_prev = by(cur, "ad_id"), by(prev, "ad_id")
    ads = []
    for aid, rows in ads_cur.items():
        am, ap = metrics(rows), metrics(ads_prev.get(aid, []))
        ads.append({"id": aid, "name": rows[0]["ad_name"], "campaign": rows[0]["campaign_name"], **am, "prev": ap})
    ads.sort(key=lambda a: (a["cpl"] is None, a["cpl"] or 0, -a["spend"]))

    # Flags (rules of thumb, explained in the report)
    flags = []
    for a in ads:
        if a["frequency"] >= 3:
            flags.append(f"Fatiga probable: **{a['name']}** tiene frecuencia {a['frequency']:.1f} en 7 días.")
        if a["spend"] >= 2 * (m["cpl"] or 1e9) and a["leads"] == 0:
            flags.append(f"Sin leads: **{a['name']}** gastó {fmt(a['spend'], money=True)} (más de 2 CPL promedio) sin generar leads.")
        if a["ctr"] is not None and a["impressions"] >= 1000 and a["ctr"] < 0.5:
            flags.append(f"CTR bajo: **{a['name']}** con {a['ctr']}% de CTR de enlace.")
        if a["hook"] is not None and a["impressions"] >= 1000 and 0 < a["hook"] < 15:
            flags.append(f"Gancho débil: **{a['name']}**; solo {a['hook']}% de las impresiones llega al 25% del video.")
    for ad in active:
        if ad["effective_status"] in ("DISAPPROVED", "WITH_ISSUES"):
            flags.append(f"Estado: **{ad['name']}** está en {ad['effective_status']}.")

    monday = cur_rng[0].isoformat()
    L = [f"# Informe semanal Meta Ads · {acct['name']}",
         f"Semana {cur_rng[0]:%d %b} – {cur_rng[1]:%d %b %Y} vs. {prev_rng[0]:%d %b} – {prev_rng[1]:%d %b} · "
         f"moneda {acct['currency']} · zona {acct['timezone_name']}", "",
         "## Resumen de la cuenta", "| Métrica | Esta semana | Semana anterior |", "|---|---|---|",
         f"| Gasto | {fmt(m['spend'], money=True)}{delta(m['spend'], p['spend'])} | {fmt(p['spend'], money=True)} |",
         f"| Leads | {fmt(m['leads'])}{delta(m['leads'], p['leads'])} | {fmt(p['leads'])} |",
         f"| Costo por lead | {fmt(m['cpl'], money=True)}{delta(m['cpl'], p['cpl'], True)} | {fmt(p['cpl'], money=True)} |",
         f"| Impresiones | {fmt(m['impressions'])}{delta(m['impressions'], p['impressions'])} | {fmt(p['impressions'])} |",
         f"| CTR de enlace | {fmt(m['ctr'], pct=True)}{delta(m['ctr'], p['ctr'])} | {fmt(p['ctr'], pct=True)} |",
         f"| CPM | {fmt(m['cpm'], money=True)}{delta(m['cpm'], p['cpm'], True)} | {fmt(p['cpm'], money=True)} |",
         f"| CPC (enlace) | {fmt(m['cpc'], money=True)}{delta(m['cpc'], p['cpc'], True)} | {fmt(p['cpc'], money=True)} |",
         f"| Clic → lead | {fmt(m['lead_rate'], pct=True)}{delta(m['lead_rate'], p['lead_rate'])} | {fmt(p['lead_rate'], pct=True)} |",
         "", "## Por campaña", "| Campaña | Gasto | Leads | CPL | CTR | CPM |", "|---|---|---|---|---|---|"]
    for cid, rows in sorted(camps_cur.items(), key=lambda kv: -metrics(kv[1])["spend"]):
        cm, cp = metrics(rows), metrics(camps_prev.get(cid, []))
        L.append(f"| {rows[0]['campaign_name']} | {fmt(cm['spend'], money=True)} | {cm['leads']}{delta(cm['leads'], cp['leads'])} | "
                 f"{fmt(cm['cpl'], money=True)}{delta(cm['cpl'], cp['cpl'], True)} | {fmt(cm['ctr'], pct=True)} | {fmt(cm['cpm'], money=True)} |")
    L += ["", "## Creativos (ordenados por costo por lead)",
          "| Anuncio | Gasto | Leads | CPL | CTR | Frec. | Gancho 25% | Retención 100% |", "|---|---|---|---|---|---|---|---|"]
    for a in ads:
        L.append(f"| {a['name']} | {fmt(a['spend'], money=True)} | {a['leads']} | {fmt(a['cpl'], money=True)}"
                 f"{delta(a['cpl'], a['prev']['cpl'], True)} | {fmt(a['ctr'], pct=True)} | {a['frequency']:.1f} | "
                 f"{fmt(a['hook'], pct=True)} | {fmt(a['hold'], pct=True)} |")
    L += ["", "## Alertas"] + ([f"- {f}" for f in flags] or ["- Sin alertas esta semana."])
    L += ["", "_Gancho 25% = vistas al 25% / impresiones. Retención 100% = vistas completas / impresiones. "
          "Umbrales de alerta: frecuencia ≥ 3, CTR < 0.5%, gancho < 15%, gasto ≥ 2 CPL sin leads. "
          "Datos de la Marketing API; pueden variar levemente frente a Ads Manager por la ventana de atribución._"]

    out = BUILD / "reports"
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{monday}.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    (out / f"{monday}.json").write_text(json.dumps({"account": acct, "week": [str(d) for d in cur_rng],
                                                     "prev_week": [str(d) for d in prev_rng], "totals": m,
                                                     "prev_totals": p, "ads": ads, "flags": flags},
                                                    indent=2, ensure_ascii=False), encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
