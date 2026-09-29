"""Step 2 (read-only): find interest/behavior IDs, estimate audience sizes, list custom audiences for exclusion."""
import json, pathlib
import config as C
from meta import get, get_all, MetaError

BUILD = pathlib.Path(__file__).resolve().parent.parent / "build"
out = {"interests": [], "behaviors": [], "custom_audiences": [], "estimate": None, "errors": []}


def size(o):
    lo, hi = o.get("audience_size_lower_bound"), o.get("audience_size_upper_bound")
    return f"{lo:,} - {hi:,}" if lo and hi else "n/a"


for vertical, queries in C.INTEREST_QUERIES.items():
    for q in queries:
        try:
            for r in get("search", type="adinterest", q=q, limit=5)["data"]:
                out["interests"].append({"vertical": vertical, "query": q, "id": r["id"], "name": r["name"],
                                         "path": " > ".join(r.get("path", [])), "size": size(r)})
        except MetaError as e:
            out["errors"].append(f"adinterest '{q}': {e}")

try:
    behaviors = get("search", type="adTargetingCategory", **{"class": "behaviors"}, limit=1000)["data"]
    for q in C.BEHAVIOR_QUERIES:
        for r in behaviors:
            if q.lower() in r["name"].lower():
                out["behaviors"].append({"query": q, "id": r["id"], "name": r["name"],
                                         "path": " > ".join(r.get("path", [])), "size": size(r)})
except MetaError as e:
    out["errors"].append(f"behaviors: {e}")

try:
    out["custom_audiences"] = get_all(f"{C.AD_ACCOUNT}/customaudiences",
                                      fields="id,name,subtype,approximate_count_lower_bound,"
                                             "approximate_count_upper_bound,time_updated", limit=200)
except MetaError as e:
    out["errors"].append(f"customaudiences: {e}")

# Full-audience estimate uses the approved lists if present, else every exact-name match found above
t = C.targeting()
if not C.APPROVED_INTERESTS and not C.APPROVED_BEHAVIORS:
    exact = [{"id": i["id"], "name": i["name"]} for i in out["interests"] if i["name"].lower() == i["query"].lower()]
    beh = [{"id": b["id"], "name": b["name"]} for b in out["behaviors"]]
    t["flexible_spec"] = [{k: v for k, v in (("interests", exact), ("behaviors", beh)) if v}]
try:
    out["estimate"] = get(f"{C.AD_ACCOUNT}/delivery_estimate", optimization_goal="OFFSITE_CONVERSIONS",
                          promoted_object=json.dumps(C.PROMOTED_OBJECT), targeting_spec=json.dumps(t))["data"]
    out["estimate_targeting"] = t
except MetaError as e:
    out["errors"].append(f"delivery_estimate: {e}")

(BUILD / "audience.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
print("| Tipo | Vertical | Búsqueda | ID | Nombre | Tamaño |\n|---|---|---|---|---|---|")
for i in out["interests"]:
    print(f"| Interest | {i['vertical']} | {i['query']} | {i['id']} | {i['name']} | {i['size']} |")
for b in out["behaviors"]:
    print(f"| Behavior | General | {b['query']} | {b['id']} | {b['name']} | {b['size']} |")
if out["estimate"]:
    e = out["estimate"][0]
    print(f"\nAudiencia completa: {e.get('estimate_mau_lower_bound', 0):,} - {e.get('estimate_mau_upper_bound', 0):,}")
print("\nCustom audiences:")
for a in out["custom_audiences"]:
    print(f"- {a['id']} | {a['name']} | {a.get('subtype')} | ~{a.get('approximate_count_lower_bound')}")
for err in out["errors"]:
    print("ERROR", err)
