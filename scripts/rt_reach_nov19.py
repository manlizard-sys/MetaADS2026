"""Nov 19 (user order): retargeting moves to REACH optimization. New ad set in the same campaign (frequency caps
cannot be changed after start; not allowed on a Leads campaign anyway): video-engaged 60D audience only (no custom-audience expansion), FB + IG feeds,
~$11.50 lifetime (Meta minimum) to Nov 30, no day-parting. Same ad (Book now
creative, same name/UTM). Old ad set paused after the new ad exists. Usage: python3 rt_reach_nov19.py [--validate]"""
import json, sys
from meta import get, post, BUILD

ACT = "act_1806647434085082"; OLD = "120257827382480196"; CAMP = "120257827382350196"; PIXEL = "2271987886986577"
V = "--validate" in sys.argv; EX = {"execution_options": ["validate_only"]} if V else {}
STATE = BUILD / "nov2026.json"; st = json.loads(STATE.read_text()); s = st["build"].setdefault("rt_reach19", {})
save = lambda: None if V else STATE.write_text(json.dumps(st, indent=2, ensure_ascii=False))
t = get(OLD, fields="targeting")["targeting"]
t["targeting_relaxation_types"] = {"lookalike": 0, "custom_audience": 0}
t["publisher_platforms"] = ["facebook", "instagram"]; t["facebook_positions"] = ["feed"]; t["instagram_positions"] = ["stream"]
if "adset" not in s:
    r = post(f"{ACT}/adsets", name="RT · Video engaged 60D · Reach · Nov19", campaign_id=CAMP, status="ACTIVE",
             lifetime_budget=1150, end_time="2026-11-30T23:59:00-0500", billing_event="IMPRESSIONS",
             optimization_goal="REACH", bid_strategy="LOWEST_COST_WITHOUT_CAP", destination_type="WEBSITE",
             promoted_object={"pixel_id": PIXEL, "custom_event_type": "LEAD"}, targeting=t, **EX)
    print("adset", r)
    if V: sys.exit()
    s["adset"] = r["id"]; save()
if "ad" not in s:
    s["ad"] = post(f"{ACT}/ads", name="RT · Get started free · Nov16", adset_id=s["adset"],
                   creative={"creative_id": st["build"]["content19"]["rt_creative"]}, status="ACTIVE")["id"]; save(); print("ad", s["ad"])
if not s.get("old_paused"):
    post(OLD, status="PAUSED"); s["old_paused"] = True; save(); print("old paused")
print(s)
