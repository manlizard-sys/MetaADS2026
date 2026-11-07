"""Builds the November 2026 launch for Sunny Bliss: one awareness campaign (20%, $12/day) and one
leads campaign (80%, $48/day: prospecting $40 + retargeting $8). Everything is created PAUSED and
reuses the account's proven creatives (same posts, so likes and comments carry over).
Dry run by default; --apply creates the objects and saves their IDs in build/ids.json.
Awareness ads use creatives built from the original posts (object_story_id) without the lead-form
button, because a lead CTA is refused under the awareness objective. Safe to re-run: campaigns,
ad sets and ads that already exist by name are reused, not duplicated.
Usage: python3 launch_nov2026.py [--apply]
"""
import json, sys
import meta, config

APPLY = "--apply" in sys.argv
ACT = config.AD_ACCOUNT
GEO = config.zip_geo()
AGE = {"age_min": 30, "age_max": 65}
EXCLUDE = [{"id": "120254170491030640"}]          # SB – Lead Form Submitted – 90d
RETARGET = [{"id": "120253643074120640"},          # Website Visitors – 180 Days
            {"id": "120254170489520640"},          # IG Engagers – 365d
            {"id": "120254170489470640"}]          # FB Page Engagers – 365d

PLAN = [
  {"campaign": {"name": "SB · Awareness · Top-rated · Nov 2026", "objective": "OUTCOME_AWARENESS"},
   "adsets": [{"name": "Awareness · 21 ZIPs · 30-65 · EN+ES", "daily_budget": 1200,
               "optimization_goal": "REACH", "billing_event": "IMPRESSIONS",
               "promoted_object": {"page_id": config.PAGE_ID},
               "targeting": {**AGE, "geo_locations": GEO},
               "ads": [("A1 · Neighbors · ES", "1478232510843631"),
                       ("A2 · Real customer reviews · Video", "1651829703116939")]}]},
  {"campaign": {"name": "SB · Leads · Nov 2026", "objective": "OUTCOME_LEADS"},
   "adsets": [{"name": "Prospecting · 21 ZIPs · 30-65 · Instant form", "daily_budget": 4000,
               "optimization_goal": "LEAD_GENERATION", "billing_event": "IMPRESSIONS",
               "destination_type": "ON_AD", "promoted_object": {"page_id": config.PAGE_ID},
               "targeting": {**AGE, "geo_locations": GEO, "excluded_custom_audiences": EXCLUDE},
               "ads": [("L1 · Tank Flush $149 · EN", "1101774245562036"),
                       ("L2 · 0% 60 meses · Video · ES", "4534089476877858"),
                       ("L2 · 0% 60 months · Video · EN", "1070823208860016"),
                       ("L3 · 25-year-old AC · 0% 24mo · EN", "2533799250460158"),
                       ("L5 · Instalación Miami-Dade $5,800 · ES", "1091357636971444")]},
              {"name": "Retargeting · Visitors 180d + Engagers 365d · Instant form", "daily_budget": 800,
               "optimization_goal": "LEAD_GENERATION", "billing_event": "IMPRESSIONS",
               "destination_type": "ON_AD", "promoted_object": {"page_id": config.PAGE_ID},
               "targeting": {**AGE, "geo_locations": GEO, "custom_audiences": RETARGET,
                             "excluded_custom_audiences": EXCLUDE},
               "ads": [("R0 · 0% 60 months · Video · EN", "1070823208860016"),
                       ("R0 · 0% 60 meses · Video · ES", "4534089476877858")]}]},
]

config.require() if hasattr(config, "require") else None
def existing(edge, parent_field=None, parent_id=None):
    rows = meta.get_all(f"{ACT}/{edge}", fields="name,campaign_id,adset_id", limit=200,
                        filtering=json.dumps([{"field": "name", "operator": "CONTAIN", "value": " "}]))
    return {(r.get(parent_field) if parent_field else None, r["name"]): r["id"] for r in rows
            if not parent_field or r.get(parent_field) == parent_id}

created = {}
for block in PLAN:
    c = block["campaign"]
    print(f"\nCAMPAIGN {c['name']} ({c['objective']}, PAUSED)")
    cid = None
    if APPLY:
        cid = existing("campaigns").get((None, c["name"])) or meta.post(f"{ACT}/campaigns", name=c["name"], objective=c["objective"], status="PAUSED",
                        special_ad_categories=[], is_adset_budget_sharing_enabled=False,
                        buying_type="AUCTION")["id"]
        created[c["name"]] = {"id": cid, "adsets": {}}
    for s in block["adsets"]:
        print(f"  ADSET {s['name']}  ${s['daily_budget']/100:.0f}/day  {s['optimization_goal']}")
        params = {k: v for k, v in s.items() if k not in ("ads",)}
        params["targeting"] = {**params["targeting"], "targeting_automation": {"advantage_audience": 0}}
        sid = None
        if APPLY:
            sid = existing("adsets", "campaign_id", cid).get((cid, s["name"])) or meta.post(f"{ACT}/adsets", campaign_id=cid, status="PAUSED",
                            bid_strategy="LOWEST_COST_WITHOUT_CAP", **params)["id"]
            created[c["name"]]["adsets"][s["name"]] = {"id": sid, "ads": {}}
        for name, creative in s["ads"]:
            print(f"    AD {name}  creative {creative}")
            if APPLY:
                aid = existing("ads", "adset_id", sid).get((sid, name)) or meta.post(f"{ACT}/ads", adset_id=sid, name=name, status="PAUSED",
                                creative={"creative_id": creative})["id"]
                created[c["name"]]["adsets"][s["name"]]["ads"][name] = aid

total = sum(s["daily_budget"] for b in PLAN for s in b["adsets"]) / 100
print(f"\nTotal ${total:.0f}/day  ·  {'CREATED (PAUSED)' if APPLY else 'dry run, nothing created'}")
if APPLY:
    meta.save_ids(launch_nov2026=created)
    print(json.dumps(created, indent=1, ensure_ascii=False))
