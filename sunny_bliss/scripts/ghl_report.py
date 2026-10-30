"""Read-only GoHighLevel summary for Sunny Bliss: lead counts by day, source, qualification and
pipeline stage, plus data-quality checks. Writes aggregates only (no names, phones or emails) to
build/reports/ghl-<today>.json.

Needs only GHL_TOKEN (Private Integration token, read scopes) in the environment or in
sunny_bliss/.env; the location ID is built in (GHL_LOCATION_ID overrides it). The token is never printed.
Usage: python3 ghl_report.py
"""
import collections, datetime as dt, json, os, pathlib, sys
import requests

ROOT = pathlib.Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"
API = "https://services.leadconnectorhq.com"


def env(name):
    f = ROOT / ".env"
    if f.exists():
        for line in f.read_text(encoding="utf-8-sig").splitlines():
            if line.startswith(name + "="):
                return line.split("=", 1)[1].strip()
    return os.environ.get(name, "").strip() or sys.exit(f"{name} missing (.env or environment variable)")


# Sunny Bliss sub-account; not a secret, so it lives here and only the token comes from the environment.
LOCATION_ID = "FWSYVq6jT5aL8WUhVV5E"
TOKEN = env("GHL_TOKEN")
LOC = os.environ.get("GHL_LOCATION_ID", "").strip() or LOCATION_ID
S = requests.Session()
S.headers.update({"Authorization": f"Bearer {TOKEN}", "Version": "2021-07-28", "Accept": "application/json"})


def call(method, path, **kw):
    r = S.request(method, API + path, timeout=30, **kw)
    if not r.ok:
        sys.exit(f"GHL {r.status_code} on {path}: {r.text[:200].replace(TOKEN, '***')}")
    return r.json()


def contacts():
    out, after = [], None
    while True:
        body = {"locationId": LOC, "pageLimit": 100}
        if after:
            body["searchAfter"] = after
        page = call("POST", "/contacts/search", json=body)["contacts"]
        out += page
        if len(page) < 100:
            return out
        after = page[-1]["searchAfter"]


def opportunities():
    out, page = [], 1
    while True:
        data = call("GET", "/opportunities/search", params={"location_id": LOC, "limit": 100, "page": page})
        out += data["opportunities"]
        if len(out) >= data.get("meta", {}).get("total", 0) or not data["opportunities"]:
            return out
        page += 1


fields = {f["id"]: f["name"] for f in call("GET", f"/locations/{LOC}/customFields")["customFields"]}
stages = {p["id"]: (p["name"], {s["id"]: s["name"] for s in p["stages"]})
          for p in call("GET", "/opportunities/pipelines", params={"locationId": LOC})["pipelines"]}
stage_of = {}
for o in opportunities():
    pipe, names = stages.get(o["pipelineId"], ("?", {}))
    stage_of[o.get("contactId")] = {"pipeline": pipe, "stage": names.get(o["pipelineStageId"], "?"), "status": o.get("status")}

leads, checks = [], collections.Counter()
for c in contacts():
    tags = set(c.get("tags") or [])
    cf = {fields.get(x["id"], x["id"]): x.get("value") for x in c.get("customFields") or []}
    st = stage_of.get(c["id"], {})
    leads.append({
        "day": (c.get("dateAdded") or "")[:10],
        "source": c.get("source") or "Sin fuente",
        "service": "HVAC" if "hvac lead" in tags else "Plomería" if "plumbing lead" in tags else "Sin dato",
        "language": "Español" if "spanish" in tags or "(ES)" in (c.get("source") or "") else "Inglés",
        "qualification": "Calificado" if "qualified" in tags else "No calificado" if "unqualified" in tags else "Sin clasificar",
        "pipeline": st.get("pipeline", "Sin oportunidad"),
        "stage": st.get("stage", "Sin oportunidad"),
        "has_ad_name": bool(cf.get("Ad Name") or cf.get("UTM Ad ID")),
        "has_phone": bool(c.get("phone")),
    })
    checks["contactos"] += 1
    checks["sin_fuente"] += not c.get("source")
    checks["sin_anuncio_utm"] += not (cf.get("Ad Name") or cf.get("UTM Ad ID"))
    checks["sin_telefono"] += not c.get("phone")
    checks["sin_oportunidad"] += c["id"] not in stage_of

BUILD.joinpath("reports").mkdir(parents=True, exist_ok=True)
out = BUILD / "reports" / f"ghl-{dt.date.today()}.json"
out.write_text(json.dumps({"location": LOC, "generated": dt.datetime.now(dt.timezone.utc).isoformat(),
                           "checks": checks, "leads": leads}, indent=2, ensure_ascii=False), encoding="utf-8")
print(json.dumps(checks, ensure_ascii=False))
print(out)
