"""Step 5: activate ads -> ad set -> campaign. Only run after the user replies "publicar".

Usage: python3 step5_activate.py --publicar
"""
import json, sys, datetime
import config as C
from meta import get, post, MetaError, BUILD

if "--publicar" not in sys.argv:
    sys.exit("Refusing to activate without --publicar (explicit user confirmation).")
ids = json.loads((BUILD / "ids.json").read_text())

adset = get(ids["adset_id"], fields="start_time")
if not adset["start_time"].startswith("2026-10-01T00:00:00-0400"):
    sys.exit(f"STOP: start_time is {adset['start_time']}, expected 2026-10-01T00:00:00-0400")
print("start_time OK:", adset["start_time"])

order = [(k, a["ad_id"]) for k, a in ids["ads"].items()] + [("adset", ids["adset_id"]), ("campaign", ids["campaign_id"])]
for label, oid in order:
    try:
        post(oid, status="ACTIVE")
        print("ACTIVE", label, oid)
    except MetaError as e:
        sys.exit(f"API ERROR activating {label} {oid}:\n{e}")

report = {}
for k, a in ids["ads"].items():
    report[k] = get(a["ad_id"], fields="name,effective_status,review_feedback,ad_review_feedback")
print(json.dumps(report, indent=2, ensure_ascii=False))

now = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
lines = [f"# {C.CAMPAIGN_NAME}", "", f"Activado: {now} (entrega desde 2026-10-01 00:00 America/New_York)", "",
         f"- Cuenta: {C.AD_ACCOUNT}", f"- Campaña: {ids['campaign_id']}", f"- Conjunto: {ids['adset_id']}"]
for k, a in ids["ads"].items():
    lines.append(f"- {a['name']}: ad {a['ad_id']} · creative {a['creative_id']} · {report[k].get('effective_status')}")
lines += ["", "Videos:"] + [f"- {p}: {v['id']}" for p, v in ids.get("videos", {}).items()]
(BUILD / "README.md").write_text("\n".join(lines) + "\n")
