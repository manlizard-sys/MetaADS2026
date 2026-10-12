"""Changes approved on 2026-10-12 for the ORCHID ad set (job-seeker cleanup).

Ad set 120257040908680196:
  - Advantage+ Audience off, age 30-65 as a hard limit, location "home" only
  (interest exclusions were planned but Meta no longer allows detailed targeting exclusions)
Ads: V2 and V1 -> ACTIVE; S1 and S6 -> PAUSED (S8 stays as the only static).

Saves the current state to build/backup-<today>-before-changes.json before writing.
Default is a dry run that only prints the changes. Usage: python3 apply_2026_10_12.py [--apply]
"""
import copy, datetime, json, sys
from meta import get, get_all, post, BUILD, MetaError

ACT = "act_1806647434085082"
ADSET = "120257040908680196"
AD_STATUS = {
    "V2 Small Law Firm - 2026 Oct": "ACTIVE",
    "V1 POV Email - 2026 Oct": "ACTIVE",
    "S1 Cost - Static - 2026 Oct": "PAUSED",
    "S6 What VA Does - Static - 2026 Oct": "PAUSED",
}

apply = "--apply" in sys.argv
ads = get_all(f"{ACT}/ads", fields="id,name,status", limit=100)
aset = get(ADSET, fields="name,targeting,status,daily_budget")

t = copy.deepcopy(aset["targeting"])
t["targeting_automation"] = {"advantage_audience": 0}
t.pop("age_range", None)  # Advantage+ suggestion field; invalid once it is off
t["age_min"], t["age_max"] = 30, 65
t["geo_locations"]["location_types"] = ["home"]

old = aset["targeting"]
print(f"Ad set: {aset['name']}")
print(f"  Advantage+ audience: {old.get('targeting_automation')} -> {t['targeting_automation']}")
print(f"  Edad: {old.get('age_min')}-{old.get('age_max')} -> 30-65")
print(f"  Ubicación: {old['geo_locations'].get('location_types')} -> ['home']")
byname = {a["name"]: a for a in ads}
for name, st in AD_STATUS.items():
    print(f"  {name}: {byname[name]['status']} -> {st}")

if not apply:
    print("\nVista previa. Nada cambió. Ejecuta con --apply para aplicar.")
    sys.exit(0)

stamp = datetime.date.today().isoformat()
(BUILD / f"backup-{stamp}-before-changes.json").write_text(
    json.dumps({"adset": aset, "ads": ads}, indent=2, ensure_ascii=False), encoding="utf-8")
print("\nCopia del estado anterior guardada.")
try:
    post(ADSET, targeting=t)
    print("Ad set actualizado.")
except MetaError as e:
    sys.exit(f"Error en el ad set; no se tocaron los anuncios:\n{e}")
for name, st in AD_STATUS.items():
    try:
        post(byname[name]["id"], status=st)
        print(f"{name}: {st}")
    except MetaError as e:
        print(f"ERROR {name}: {e}")
