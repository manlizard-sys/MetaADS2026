"""Nov 19 (user order "Hazlo"): move the BF lead ad sets to landing-page-view optimization.
- New ad set per campaign (healthcare, entrepreneurs): LANDING_PAGE_VIEWS, Advantage+ placements, no day-parting,
  $9/day each until Nov 30 23:59 ET, same audience (Advantage+ with the same suggestions and exclusion).
- New creative per vertical: 4:5 image on feeds, 9:16 on stories/reels (placement asset customization), first copy
  variant, same landing, same UTM (utm_content = ad name, so GHL/tracker keep matching).
- Old ad sets are paused only after the new ad is created and active.
Usage: python3 lpv_switch_nov19.py [--validate]   (--validate: Meta checks everything, creates nothing)"""
import json, sys, time
from meta import get, post, BUILD, MetaError

ACT, PAGE, IG, PIXEL = "act_1806647434085082", "1132642053254708", "17841430599113385", "2271987886986577"
VALIDATE = "--validate" in sys.argv
STATE = BUILD / "nov2026.json"
st = json.loads(STATE.read_text()); b = st["build"]["bf16"]; s = st["build"].setdefault("lpv19", {})
save = lambda: None if VALIDATE else STATE.write_text(json.dumps(st, indent=2, ensure_ascii=False))
COPY = json.loads((BUILD / "copy_bf_nov16.json").read_text())
LP = {"hc": "https://go.orchidpros.com/practices-free-month", "ent": "https://go.orchidpros.com/business-free-month"}
CAMP = {"hc": "bf_healthcare_nov26", "ent": "bf_entrepreneurs_nov26"}
NAME = {"hc": "Healthcare", "ent": "Entrepreneurs"}
UTM = "utm_source=meta&utm_medium=paid&utm_campaign={c}&utm_term={{{{adset.name}}}}&utm_content={{{{ad.name}}}}"
OPT_OUT = ["text_optimizations", "image_touchups", "image_templates", "image_uncrop", "image_animation",
           "enhance_cta", "description_automation", "add_text_overlay", "adapt_to_placement"]
END = "2026-11-30T23:59:00-0500"
EXTRA = {"execution_options": ["validate_only"]} if VALIDATE else {}


def retry(fn, *a, **k):
    for _ in range(8):
        try:
            return fn(*a, **k)
        except MetaError as e:
            if any(c in str(e) for c in ('"code": 17', "(#613)", "2446079", "80004")):
                time.sleep(45); continue
            raise


def creative(key):
    c, link, img = COPY[key], LP[key], b["images"]
    feed_spec = {"publisher_platforms": ["facebook", "instagram"],
                 "facebook_positions": ["feed", "marketplace", "video_feeds", "search", "profile_feed"],
                 "instagram_positions": ["stream", "profile_feed", "ig_search"]}
    story_spec = {"publisher_platforms": ["facebook", "instagram"],
                  "facebook_positions": ["story", "facebook_reels"], "instagram_positions": ["story", "reels"]}
    afs = {"images": [{"hash": img[f"{key}_4x5"], "adlabels": [{"name": "feed"}]},
                      {"hash": img[f"{key}_9x16"], "adlabels": [{"name": "vertical"}]}],
           "bodies": [{"text": c["bodies"][0]}], "titles": [{"text": c["titles"][0]}],
           "descriptions": [{"text": c["description"]}],
           "link_urls": [{"website_url": link, "display_url": "orchidpros.com"}],
           "call_to_action_types": ["SIGN_UP"], "ad_formats": ["SINGLE_IMAGE"], "optimization_type": "PLACEMENT",
           "asset_customization_rules": [
               {"customization_spec": feed_spec, "image_label": {"name": "feed"}, "priority": 1},
               {"customization_spec": story_spec, "image_label": {"name": "vertical"}, "priority": 2},
               {"customization_spec": {}, "image_label": {"name": "feed"}, "priority": 3, "is_default": True}]}
    return retry(post, f"{ACT}/adcreatives", name=f"lpv19 · {NAME[key]} · Get started free · 4x5+9x16",
                 object_story_spec={"page_id": PAGE, "instagram_user_id": IG}, asset_feed_spec=afs,
                 degrees_of_freedom_spec={"creative_features_spec": {k: {"enroll_status": "OPT_OUT"} for k in OPT_OUT}},
                 url_tags=UTM.format(c=CAMP[key]), **EXTRA)


for key in ("hc", "ent"):
    old = b[f"{key}_adset"]
    if f"{key}_creative" not in s:
        r = creative(key); print(key, "creative", r)
        if VALIDATE:
            continue
        s[f"{key}_creative"] = r["id"]; save()
    if f"{key}_adset" not in s:
        t = get(old, fields="targeting")["targeting"]
        for k in ("publisher_platforms", "facebook_positions", "device_platforms"):
            t.pop(k, None)  # Advantage+ placements
        s[f"{key}_adset"] = retry(post, f"{ACT}/adsets", name=f"BF · {NAME[key]} · Get started free · LPV · Nov19",
                                  campaign_id=b[f"{key}_campaign"], status="ACTIVE", daily_budget=900, end_time=END,
                                  billing_event="IMPRESSIONS", bid_strategy="LOWEST_COST_WITHOUT_CAP",
                                  optimization_goal="LANDING_PAGE_VIEWS", destination_type="WEBSITE",
                                  promoted_object={"pixel_id": PIXEL, "custom_event_type": "LEAD"}, targeting=t)["id"]
        save(); print(key, "adset", s[f"{key}_adset"])
    if f"{key}_ad" not in s:
        s[f"{key}_ad"] = retry(post, f"{ACT}/ads", name=f"BF · {NAME[key]} · Get started free · LPV · Nov19",
                               adset_id=s[f"{key}_adset"], creative={"creative_id": s[f"{key}_creative"]},
                               status="ACTIVE")["id"]; save(); print(key, "ad", s[f"{key}_ad"])
    if not s.get(f"{key}_old_paused"):
        retry(post, old, status="PAUSED"); s[f"{key}_old_paused"] = True; save(); print(key, "old adset paused", old)
print(json.dumps(s, indent=1))
