"""Full read-only analytics for the OrchidPros ad account.

Pulls the last N days (default 30) and writes, under build/reports/:
  stats-<today>.json        every number used below
  stats-<today>-*.csv       one CSV per table (ads, campaigns, breakdowns, daily)
  dashboard-<today>.html    KPI tiles, daily spend/leads charts, funnel, breakdowns, creative ranking, alerts

Never creates, edits, pauses or activates anything.
Usage: python3 analytics.py [--days 30]
"""
import csv, datetime as dt, html, json, sys
import config as C
from meta import get, get_all, MetaError, BUILD

LEAD_TYPES = ("offsite_conversion.fb_pixel_lead", "lead", "onsite_conversion.lead_grouped")
BASE = ("spend,impressions,reach,frequency,inline_link_clicks,actions,"
        "video_p25_watched_actions,video_p100_watched_actions")
BREAKDOWNS = {
    "placement": "publisher_platform,platform_position",
    "age": "age",
    "gender": "gender",
    "device": "device_platform",
    "region": "region",
}


def act(row, types):
    acts = {a["action_type"]: float(a["value"]) for a in row.get("actions") or []}
    return next((acts[t] for t in types if t in acts), 0.0)


def first(row, key):
    v = row.get(key) or []
    return float(v[0]["value"]) if v else 0.0


def summarize(rows):
    spend = sum(float(r.get("spend", 0)) for r in rows)
    imp = sum(float(r.get("impressions", 0)) for r in rows)
    clicks = sum(float(r.get("inline_link_clicks", 0)) for r in rows)
    lpv = sum(act(r, ("landing_page_view",)) for r in rows)
    leads = sum(act(r, LEAD_TYPES) for r in rows)
    p25 = sum(first(r, "video_p25_watched_actions") for r in rows)
    p100 = sum(first(r, "video_p100_watched_actions") for r in rows)
    div = lambda a, b, k=1: round(k * a / b, 2) if b else None
    return {"spend": round(spend, 2), "impressions": int(imp), "link_clicks": int(clicks),
            "landing_page_views": int(lpv), "leads": int(leads),
            "cpl": div(spend, leads), "cpm": div(spend, imp, 1000), "cpc": div(spend, clicks),
            "ctr": div(clicks, imp, 100), "lpv_rate": div(lpv, clicks, 100), "lead_rate": div(leads, lpv or clicks, 100),
            "hook": div(p25, imp, 100), "hold": div(p100, imp, 100),
            "frequency": round(max((float(r.get("frequency", 0)) for r in rows), default=0), 2)}


def group(rows, keys):
    out = {}
    for r in rows:
        out.setdefault(tuple(r.get(k, "") for k in keys), []).append(r)
    return out


def alerts(account, ads):
    f = []
    cpl = account["cpl"]
    if account["link_clicks"] >= 50 and account["landing_page_views"] < 0.5 * account["link_clicks"]:
        f.append(("serious", f"Solo {account['lpv_rate']}% de los clics llega a cargar la landing. Revisa velocidad de go.orchidpros.com/hire."))
    if account["landing_page_views"] >= 100 and (account["lead_rate"] or 0) < 2:
        f.append(("serious", f"Conversión de landing a lead de {account['lead_rate']}%. El cuello de botella está en la landing o el formulario, no en los anuncios."))
    if account["leads"] and account["leads"] * 7 / DAYS < 10:
        f.append(("warning", f"Ritmo de ~{account['leads'] * 7 / DAYS:.1f} leads/semana: muy lejos de las ~50 que Meta necesita para salir de aprendizaje."))
    for a in ads:
        name = a["name"]
        if a["frequency"] >= 3:
            f.append(("warning", f"{name}: frecuencia {a['frequency']}; posible fatiga."))
        if cpl and a["spend"] >= 2 * cpl and a["leads"] == 0:
            f.append(("critical", f"{name}: gastó ${a['spend']:.2f} (más de 2 CPL) sin leads."))
        if a["impressions"] >= 1000 and (a["ctr"] or 0) < 0.5:
            f.append(("warning", f"{name}: CTR de enlace {a['ctr']}%."))
        if a["impressions"] >= 1000 and a["hook"] is not None and a["hook"] < 15:
            f.append(("warning", f"{name}: solo {a['hook']}% de las impresiones ve el 25% del video; gancho débil."))
        if a.get("status") in ("DISAPPROVED", "WITH_ISSUES"):
            f.append(("critical", f"{name}: estado {a['status']}."))
    return f


def fetch(days):
    since, until = dt.date.today() - dt.timedelta(days=days), dt.date.today() - dt.timedelta(days=1)
    tr = json.dumps({"since": since.isoformat(), "until": until.isoformat()})
    common = dict(time_range=tr, limit=500)
    data = {"range": [since.isoformat(), until.isoformat()]}
    data["account"] = get(C.AD_ACCOUNT, fields="name,currency,timezone_name,account_status,amount_spent")
    data["daily"] = get_all(f"{C.AD_ACCOUNT}/insights", level="account", time_increment=1, fields=BASE, **common)
    data["ads"] = get_all(f"{C.AD_ACCOUNT}/insights", level="ad",
                          fields=BASE + ",campaign_id,campaign_name,adset_name,ad_id,ad_name", **common)
    data["breakdowns"] = {k: get_all(f"{C.AD_ACCOUNT}/insights", level="account", breakdowns=b, fields=BASE, **common)
                          for k, b in BREAKDOWNS.items()}
    data["ad_status"] = {a["id"]: a for a in get_all(f"{C.AD_ACCOUNT}/ads", fields="id,name,effective_status,"
                                                     "creative{thumbnail_url}", limit=500)}
    return data


def build(data):
    acct = summarize(data["daily"])
    daily = [{"date": r["date_start"], **summarize([r])} for r in data["daily"]]
    ads = []
    for (aid,), rows in group(data["ads"], ["ad_id"]).items():
        st = data["ad_status"].get(aid, {})
        ads.append({"id": aid, "name": rows[0]["ad_name"], "campaign": rows[0]["campaign_name"],
                    "adset": rows[0]["adset_name"], "status": st.get("effective_status"),
                    "thumb": (st.get("creative") or {}).get("thumbnail_url"), **summarize(rows)})
    ads.sort(key=lambda a: (a["cpl"] is None, a["cpl"] or 0, -a["spend"]))
    camps = [{"name": rows[0]["campaign_name"], **summarize(rows)}
             for _, rows in group(data["ads"], ["campaign_id"]).items()]
    bds = {}
    for k, rows in data["breakdowns"].items():
        keys = BREAKDOWNS[k].split(",")
        bds[k] = sorted(({"segment": " / ".join(v for v in key if v), **summarize(rs)}
                         for key, rs in group(rows, keys).items()), key=lambda x: -x["spend"])
    return {"range": data["range"], "account_info": data["account"], "account": acct, "daily": daily,
            "campaigns": camps, "ads": ads, "breakdowns": bds, "alerts": alerts(acct, ads)}


# ---------------------------------------------------------------- output
def money(v):
    return "-" if v is None else f"${v:,.2f}"


def pct(v):
    return "-" if v is None else f"{v}%"


def bar_chart(series, key, title, fmt):
    w, h, pad = 640, 180, 28
    vals = [d[key] or 0 for d in series]
    top = max(vals) or 1
    bw = (w - pad) / max(len(vals), 1)
    bars = []
    for i, (d, v) in enumerate(zip(series, vals)):
        bh = (h - pad) * v / top
        x, y = pad + i * bw + 1, h - pad - bh
        bars.append(f'<rect class="bar" x="{x:.1f}" y="{y:.1f}" width="{max(bw - 2, 1):.1f}" height="{bh:.1f}" rx="2">'
                    f'<title>{d["date"]}: {fmt(v)}</title></rect>')
    first_d, last_d = (series[0]["date"], series[-1]["date"]) if series else ("", "")
    return (f'<figure class="chart"><figcaption>{title}</figcaption>'
            f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{title}">'
            f'<line class="axis" x1="{pad}" x2="{w}" y1="{h - pad}" y2="{h - pad}"/>'
            f'<text class="tick" x="0" y="12">{fmt(top)}</text><text class="tick" x="0" y="{h - pad}">0</text>'
            f'{"".join(bars)}<text class="tick" x="{pad}" y="{h - 8}">{first_d}</text>'
            f'<text class="tick" x="{w}" y="{h - 8}" text-anchor="end">{last_d}</text></svg></figure>')


def table(rows, cols, bar_key=None):
    top = max((r[bar_key] or 0 for r in rows), default=0) or 1 if bar_key else 1
    head = "".join(f"<th>{c[0]}</th>" for c in cols)
    body = []
    for r in rows:
        cells = []
        for label, key, f in cols:
            v = r.get(key)
            txt = html.escape(str(f(v) if f else v if v is not None else "-"))
            if key == bar_key:
                cells.append(f'<td class="num"><span class="cellbar" style="width:{100 * (v or 0) / top:.0f}%"></span>{txt}</td>')
            else:
                cells.append(f'<td class="{"num" if f else ""}">{txt}</td>')
        body.append("<tr>" + "".join(cells) + "</tr>")
    return f'<div class="tw"><table><thead><tr>{head}</tr></thead><tbody>{"".join(body)}</tbody></table></div>'


STD = [("Gasto", "spend", money), ("Impr.", "impressions", lambda v: f"{v:,}"), ("Clics", "link_clicks", lambda v: f"{v:,}"),
       ("CTR", "ctr", pct), ("LPV", "landing_page_views", lambda v: f"{v:,}"), ("Leads", "leads", lambda v: f"{v:,}"),
       ("CPL", "cpl", money), ("CPM", "cpm", money)]


def dashboard(s):
    a, info = s["account"], s["account_info"]
    tiles = [("Gasto", money(a["spend"])), ("Leads", a["leads"]), ("Costo por lead", money(a["cpl"])),
             ("CTR de enlace", pct(a["ctr"])), ("CPM", money(a["cpm"])), ("Frecuencia máx.", a["frequency"])]
    funnel = [("Impresiones", a["impressions"]), ("Clics de enlace", a["link_clicks"]),
              ("Visitas a landing", a["landing_page_views"]), ("Leads", a["leads"])]
    ftop = funnel[0][1] or 1
    icon = {"critical": "⛔", "serious": "⚠️", "warning": "△"}
    parts = [
        f"<header><h1>{html.escape(info['name'])} · Meta Ads</h1><p class='muted'>{s['range'][0]} a {s['range'][1]} · "
        f"{info['currency']} · {info['timezone_name']} · generado {dt.date.today()}</p></header>",
        '<section class="tiles">' + "".join(f'<div class="tile"><div class="muted">{k}</div><div class="big">{v}</div></div>' for k, v in tiles) + "</section>",
        '<section class="charts">' + bar_chart(s["daily"], "spend", "Gasto diario", money)
        + bar_chart(s["daily"], "leads", "Leads diarios", lambda v: f"{v:.0f}") + "</section>",
        "<h2>Embudo</h2><div class='funnel'>" + "".join(
            f'<div class="frow"><span>{k}</span><span class="fbar"><span class="cellbar" style="width:{100 * v / ftop:.1f}%"></span></span>'
            f'<span class="num">{v:,}</span></div>' for k, v in funnel) +
        f"<p class='muted'>Clic → landing: {pct(a['lpv_rate'])} · Landing → lead: {pct(a['lead_rate'])}</p></div>",
        "<h2>Alertas</h2><ul class='alerts'>" + ("".join(f"<li><span aria-hidden='true'>{icon[l]}</span> <b>{l}</b> · {html.escape(t)}</li>"
                                                      for l, t in s["alerts"]) or "<li>Sin alertas.</li>") + "</ul>",
        "<h2>Creativos (por costo por lead)</h2>" + table(s["ads"], [("Anuncio", "name", None), ("Estado", "status", None)] + STD
                                                       + [("Gancho 25%", "hook", pct), ("Ret. 100%", "hold", pct), ("Frec.", "frequency", str)], "spend"),
        "<h2>Campañas</h2>" + table(s["campaigns"], [("Campaña", "name", None)] + STD, "spend"),
    ]
    names = {"placement": "Ubicación", "age": "Edad", "gender": "Género", "device": "Dispositivo", "region": "Estado (EE. UU.)"}
    for k, rows in s["breakdowns"].items():
        parts.append(f"<h2>{names[k]}</h2>" + table(rows[:25], [(names[k], "segment", None)] + STD, "spend"))
    parts.append("<p class='muted'>LPV = visitas a la landing. Gancho = vistas al 25% / impresiones. Datos de la Marketing API; "
                 "pueden diferir levemente de Ads Manager por la ventana de atribución.</p>")
    css = """
:root{--surface:#fcfcfb;--card:#ffffff;--ink:#0b0b0b;--ink2:#52514e;--line:#e4e3df;--s1:#2a78d6}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--surface:#1a1a19;--card:#232322;--ink:#fff;--ink2:#c3c2b7;--line:#3a3a38;--s1:#3987e5}}
:root[data-theme="dark"]{--surface:#1a1a19;--card:#232322;--ink:#fff;--ink2:#c3c2b7;--line:#3a3a38;--s1:#3987e5}
*{box-sizing:border-box}.tiles>*,.charts>*{min-width:0}body{margin:0;padding:16px;background:var(--surface);color:var(--ink);font:14px/1.45 system-ui,sans-serif;max-width:1100px;margin-inline:auto}
h1{font-size:22px;margin:0}h2{font-size:16px;margin:28px 0 8px}.muted{color:var(--ink2)}
.tiles{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin-top:16px}
.tile{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:12px}.big{font-size:22px;font-weight:600}
.charts{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:12px;margin-top:16px}
.chart{margin:0;background:var(--card);border:1px solid var(--line);border-radius:8px;padding:12px}.chart svg{width:100%;height:auto}
.bar{fill:var(--s1)}.bar:hover{opacity:.75}.axis{stroke:var(--line)}.tick{fill:var(--ink2);font-size:11px}
.tw{overflow-x:auto}table{border-collapse:collapse;width:100%;font-size:13px}th,td{padding:6px 8px;border-bottom:1px solid var(--line);text-align:left;white-space:nowrap}
th{color:var(--ink2);font-weight:500}.num{text-align:right;position:relative}
td.num .cellbar{position:absolute;left:0;top:25%;height:50%;background:var(--s1);opacity:.18;border-radius:0 4px 4px 0}
.funnel .frow{display:grid;grid-template-columns:150px 1fr 90px;gap:8px;align-items:center;margin:4px 0}
.fbar{position:relative;height:14px}.fbar .cellbar{position:absolute;left:0;top:0;height:100%;background:var(--s1);border-radius:0 4px 4px 0}
.alerts{padding-left:18px}"""
    return (f"<!doctype html><html lang='es'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
            f"<title>Orchid Ads Dashboard</title><style>{css}</style></head><body>{''.join(parts)}</body></html>")


def write(s):
    out = BUILD / "reports"
    out.mkdir(parents=True, exist_ok=True)
    stamp = dt.date.today().isoformat()
    (out / f"stats-{stamp}.json").write_text(json.dumps(s, indent=2, ensure_ascii=False), encoding="utf-8")
    tables = {"daily": s["daily"], "ads": s["ads"], "campaigns": s["campaigns"],
              **{f"by-{k}": v for k, v in s["breakdowns"].items()}}
    for name, rows in tables.items():
        if rows:
            with open(out / f"stats-{stamp}-{name}.csv", "w", newline="", encoding="utf-8") as fh:
                w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
                w.writeheader()
                w.writerows(rows)
    (out / f"dashboard-{stamp}.html").write_text(dashboard(s), encoding="utf-8")
    return out / f"dashboard-{stamp}.html"


DAYS = int(sys.argv[sys.argv.index("--days") + 1]) if "--days" in sys.argv else 30

if __name__ == "__main__":
    try:
        stats = build(fetch(DAYS))
    except MetaError as e:
        sys.exit(f"API ERROR:\n{e}")
    path = write(stats)
    a = stats["account"]
    print(f"Últimos {DAYS} días: gasto {money(a['spend'])} · leads {a['leads']} · CPL {money(a['cpl'])} · "
          f"CTR {pct(a['ctr'])} · LPV {a['landing_page_views']}")
    for level, text in stats["alerts"]:
        print(f"[{level}] {text}")
    print("Dashboard:", path)
