"""Read-only Mailchimp health check before migrating to GHL.

Per audience: members by status, engagement (member rating, average open/click rate),
and the last 12 months of sent campaigns (opens, clicks, bounces, unsubscribes).
Writes build/reports/mailchimp_health.md. Never prints or saves emails or names.
Needs MAILCHIMP_API_KEY (.env or environment variable).
"""
import collections, datetime as dt, os, pathlib, sys
import requests

ROOT = pathlib.Path(__file__).resolve().parent.parent


def env(name):
    f = ROOT / ".env"
    if f.exists():
        for line in f.read_text(encoding="utf-8-sig").splitlines():
            if line.startswith(name + "="):
                return line.split("=", 1)[1].strip()
    return os.environ.get(name, "").strip() or sys.exit(f"{name} missing (.env or environment variable)")


KEY = env("MAILCHIMP_API_KEY")
API = f"https://{KEY.rsplit('-', 1)[-1]}.api.mailchimp.com/3.0"
S = requests.Session()
S.auth = ("orchid", KEY)


def get(path, **params):
    try:
        r = S.get(API + path, params=params, timeout=60)
    except requests.RequestException as e:
        sys.exit(str(e).replace(KEY, "***"))
    if r.status_code >= 400:
        sys.exit(f"GET {path}: HTTP {r.status_code} {r.text[:400].replace(KEY, '***')}")
    return r.json()


def members(list_id):
    out, offset = [], 0
    while True:
        d = get(f"/lists/{list_id}/members", count=1000, offset=offset,
                fields="members.status,members.member_rating,members.stats,members.last_changed,total_items")
        out += d.get("members") or []
        offset += 1000
        if offset >= d.get("total_items", 0):
            return out


def pct(x):
    return f"{x * 100:.1f}%"


def main():
    since = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=365)).isoformat()
    lines = [f"# Salud de Mailchimp — {dt.date.today()}", ""]
    for a in get("/lists", count=100, fields="lists.id,lists.name").get("lists") or []:
        ms = members(a["id"])
        status = collections.Counter(m["status"] for m in ms)
        subs = [m for m in ms if m["status"] == "subscribed"]
        rating = collections.Counter(m.get("member_rating", 0) for m in subs)
        engaged = sum(1 for m in subs if (m.get("stats") or {}).get("avg_open_rate", 0) > 0)
        lines += [f"## {a['name']}", "",
                  f"- Contactos: {len(ms)} — " + ", ".join(f"{k}: {v}" for k, v in status.most_common()),
                  f"- Suscritos que alguna vez abrieron: {engaged} de {len(subs)}",
                  "- Calificación de suscritos (1 = frío, 5 = muy activo): "
                  + ", ".join(f"{k}★ {rating.get(k, 0)}" for k in range(1, 6)), ""]
        camps = get("/campaigns", list_id=a["id"], status="sent", since_send_time=since, count=100,
                    sort_field="send_time", sort_dir="DESC",
                    fields="campaigns.id,campaigns.send_time,campaigns.settings.subject_line,campaigns.emails_sent").get("campaigns") or []
        if not camps:
            lines += ["Sin campañas enviadas en los últimos 12 meses.", ""]
            continue
        lines += ["| Fecha | Asunto | Enviados | Apertura | Clic | Rebotes | Bajas |", "|---|---|---|---|---|---|---|"]
        for c in camps:
            r = get(f"/reports/{c['id']}", fields="opens,clicks,bounces,unsubscribed,emails_sent")
            sent = r.get("emails_sent") or 1
            bounces = sum((r.get("bounces") or {}).values())
            lines.append(f"| {c['send_time'][:10]} | {c['settings'].get('subject_line', '')[:50]} | {sent} | "
                         f"{pct((r.get('opens') or {}).get('open_rate', 0))} | {pct((r.get('clicks') or {}).get('click_rate', 0))} | "
                         f"{pct(bounces / sent)} | {r.get('unsubscribed', 0)} |")
        lines.append("")
    out = ROOT / "build" / "reports" / "mailchimp_health.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
