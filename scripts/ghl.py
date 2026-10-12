"""Read-only lead quality check against GoHighLevel (LeadConnector API v2).

Pulls contacts created in the last N days, reads the form answers ("Hiring or job seeking",
"Vertical", role) and the job-seeker / agendo tags, and groups by the ad that brought each
lead (utm_content = ad name). Never writes to GHL.

Needs GHL_TOKEN (Private Integration token, read scopes: contacts, locations custom fields)
and GHL_LOCATION_ID, as environment variables or in .env. Names, emails and phones are
never printed or saved.
Usage: python3 ghl.py [--days 30]
"""
import collections, datetime as dt, json, os, re, sys
import requests
from meta import ROOT, BUILD

API = "https://services.leadconnectorhq.com"
JOB_WORDS = re.compile(r"\b(job|jobs|work for|hiring me|apply|applying|application|employment|resume|cv|"
                       r"position|vacan\w*|trabajo|empleo|aplicar|hoja de vida|busco)\b", re.I)


def env(name):
    f = ROOT / ".env"
    if f.exists():
        for line in f.read_text(encoding="utf-8-sig").splitlines():
            if line.startswith(name + "="):
                return line.split("=", 1)[1].strip()
    return os.environ.get(name, "").strip() or sys.exit(f"{name} missing (.env or environment variable)")


TOKEN, LOCATION = env("GHL_TOKEN"), env("GHL_LOCATION_ID")
S = requests.Session()
S.headers.update({"Authorization": f"Bearer {TOKEN}", "Version": "2021-07-28", "Accept": "application/json"})


def call(method, path, **kw):
    r = S.request(method, API + path, timeout=60, **kw)
    if r.status_code >= 400:
        sys.exit(f"GHL {method} {path}: HTTP {r.status_code} {r.text[:300].replace(TOKEN, '***')}")
    return r.json()


def contacts_since(start):
    out, page = [], 1
    while True:
        data = call("POST", "/contacts/search", json={
            "locationId": LOCATION, "page": page, "pageLimit": 100,
            "filters": [{"field": "dateAdded", "operator": "range", "value": {"gte": start.isoformat()}}],
            "sort": [{"field": "dateAdded", "direction": "desc"}]})
        batch = data.get("contacts") or []
        out += batch
        if len(batch) < 100:
            return out
        page += 1


def field_names():
    data = call("GET", f"/locations/{LOCATION}/customFields")
    return {f["id"]: f.get("name", f["id"]) for f in data.get("customFields", [])}


def answer(cf, names, pattern):
    for f in cf:
        if re.search(pattern, names.get(f.get("id"), ""), re.I):
            v = f.get("value", f.get("fieldValue"))
            return ", ".join(v) if isinstance(v, list) else str(v or "")
    return ""


def main():
    days = int(sys.argv[sys.argv.index("--days") + 1]) if "--days" in sys.argv else 30
    start = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=days)
    names = field_names()
    rows = []
    for c in contacts_since(start):
        cf = c.get("customFields") or []
        attr = c.get("attributionSource") or {}
        help_ = answer(cf, names, r"hiring or job")
        biz = answer(cf, names, r"^vertical$")
        role = answer(cf, names, r"your role")
        tags = c.get("tags") or []
        job = "job-seeker" in tags or bool(JOB_WORDS.search(help_))
        rows.append({"id": c.get("id"), "date": (c.get("dateAdded") or "")[:10],
                     "ad": attr.get("utmContent") or "(sin utm)", "source": attr.get("sessionSource") or c.get("source") or "",
                     "hiring_or_job": help_, "vertical": biz, "role": role, "tags": tags,
                     "booked": "agendo" in tags, "job_seeker": job})

    by_ad = collections.defaultdict(lambda: {"leads": 0, "job_seekers": 0, "booked": 0})
    for r in rows:
        by_ad[r["ad"]]["leads"] += 1
        by_ad[r["ad"]]["job_seekers"] += r["job_seeker"]
        by_ad[r["ad"]]["booked"] += r["booked"]
    total, jobs = len(rows), sum(r["job_seeker"] for r in rows)
    print(f"GHL, últimos {days} días: {total} contactos · {jobs} buscan trabajo ({100 * jobs / total:.0f}%)" if total
          else f"GHL, últimos {days} días: 0 contactos")
    for ad, v in sorted(by_ad.items(), key=lambda x: -x[1]["leads"]):
        print(f"  {ad}: {v['leads']} leads · {v['job_seekers']} buscan trabajo · {v['booked']} agendaron")
    print("\nVertical (empresas que quieren contratar):")
    for k, n in collections.Counter(r["vertical"] or "(vacío)" for r in rows if not r["job_seeker"]).most_common(15):
        print(f"  {n:>3}  {k}")

    out = BUILD / "reports"
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"ghl-{dt.date.today().isoformat()}.json"
    path.write_text(json.dumps({"days": days, "by_ad": by_ad, "contacts": rows}, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nDetalle sin datos personales: {path}")


if __name__ == "__main__":
    main()
