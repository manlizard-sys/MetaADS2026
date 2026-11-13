"""Nov 13 prep (approved by the user): everything created PAUSED for the Nov 16 launch.
1) Ad set "BF · Healthcare · Free month" inside the leads campaign (no ads yet: creatives and landing pending).
2) Engagement campaign for Instagram followers ($2/day, broad), reusing the awareness video.
State saved to build/nov2026.json -> build.bf_health / build.engagement."""
import json, time
from meta import get, post, BUILD, MetaError

ACT, PAGE, IG, PIXEL = "act_1806647434085082", "1132642053254708", "17841430599113385", "2271987886986577"
LEAD_CAMPAIGN, SRC_ADSET = "120257579673320196", "120257589638070196"
START, END = "2026-11-16T06:00:00-0500", "2026-11-30T23:59:00-0500"
STATE = BUILD / "nov2026.json"
st = json.loads(STATE.read_text())
b = st["build"]

HEALTH_POSITIONS = [{"id": "108768179146852"}, {"id": "148866958458716"}, {"id": "149072445110317"},
                    {"id": "1569299249954237"}, {"id": "1595394480678734"}, {"id": "911356208895948"},
                    {"id": "109487152410372"}]  # dentist, PT, chiropractor/owner, medical/dental office & practice managers, medical director


def retry(fn, **kw):
    for _ in range(8):
        try:
            return fn(**kw)
        except MetaError as e:
            if any(c in str(e) for c in ('"code": 17', "613", "2446079", "80004")):
                time.sleep(45); continue
            raise


# 1) Healthcare ad set (paused, lifetime $150 = 15 days x $10, 6am-10pm viewer time)
if "bf_health" not in b:
    attr = get(SRC_ADSET, fields="attribution_spec")["attribution_spec"]
    t = {"geo_locations": {"countries": ["US"], "location_types": ["home", "recent"]},
         "age_min": 25, "age_max": 65, "age_range": [30, 65],
         "flexible_spec": [{"work_positions": HEALTH_POSITIONS}],
         "excluded_custom_audiences": [{"id": "120257005715340196"}],
         "targeting_automation": {"advantage_audience": 1},
         "publisher_platforms": ["facebook"], "facebook_positions": ["feed"], "device_platforms": ["mobile", "desktop"]}
    a = retry(post, path=None) if False else None
    a = retry(lambda **k: post(f"{ACT}/adsets", **k),
              name="BF · Healthcare · Free month · 6am-10pm · Nov26", campaign_id=LEAD_CAMPAIGN, status="PAUSED",
              lifetime_budget=15000, start_time=START, end_time=END, pacing_type=["day_parting"],
              adset_schedule=[{"days": [0, 1, 2, 3, 4, 5, 6], "start_minute": 360, "end_minute": 1320, "timezone_type": "USER"}],
              billing_event="IMPRESSIONS", bid_strategy="LOWEST_COST_WITHOUT_CAP", optimization_goal="OFFSITE_CONVERSIONS",
              destination_type="WEBSITE", promoted_object={"pixel_id": PIXEL, "custom_event_type": "LEAD"},
              attribution_spec=attr, targeting=t)
    b["bf_health"] = {"adset": a["id"], "lifetime": 15000, "status": "PAUSED (sin anuncios: faltan creativos y landing)"}
    STATE.write_text(json.dumps(st, indent=2, ensure_ascii=False))
    print("Healthcare ad set:", a["id"])

# 2) Engagement campaign: Instagram profile visits, broad US, $2/day, paused
if "engagement" not in b:
    camp = retry(lambda **k: post(f"{ACT}/campaigns", **k), name="Orchid · IG Followers · Nov 2026", objective="OUTCOME_TRAFFIC",
                 status="PAUSED", special_ad_categories=[], is_adset_budget_sharing_enabled="false")
    b["engagement"] = {"campaign": camp["id"]}
    STATE.write_text(json.dumps(st, indent=2, ensure_ascii=False))
    print("Engagement campaign:", camp["id"])
e = b["engagement"]
e.pop("adset_error", None)
if "adset" not in e:
    try:
        a = retry(lambda **k: post(f"{ACT}/adsets", **k), name="IG profile visits · US broad 25-65 · Nov26", campaign_id=e["campaign"],
                  status="PAUSED", daily_budget=200, start_time=START, billing_event="IMPRESSIONS", bid_strategy="LOWEST_COST_WITHOUT_CAP",
                  optimization_goal="VISIT_INSTAGRAM_PROFILE", destination_type="INSTAGRAM_PROFILE",
                  targeting={"geo_locations": {"countries": ["US"]}, "age_min": 25, "age_max": 65,
                             "targeting_automation": {"advantage_audience": 1},
                             "publisher_platforms": ["instagram"], "instagram_positions": ["stream", "reels"]})
        e["adset"] = a["id"]
        print("Engagement ad set:", a["id"])
    except MetaError as err:
        e["adset_error"] = str(err)[:400]; print("Engagement ad set ERROR:", str(err)[:400])
    STATE.write_text(json.dumps(st, indent=2, ensure_ascii=False))
if "adset" in e and "ad" not in e:
    try:
        cr = retry(lambda **k: post(f"{ACT}/adcreatives", **k), name="IG followers · POV Email video",
                   object_story_spec={"page_id": PAGE, "instagram_user_id": IG,
                                      "video_data": {"video_id": "1489888606331620",
                                                     "image_url": next(t["uri"] for t in get("1489888606331620", fields="thumbnails{uri,is_preferred}")["thumbnails"]["data"]),
                                                     "message": "Running a business shouldn't mean answering every call yourself. Follow Orchid for real ways U.S. teams get time back with bilingual professionals from Colombia.",
                                                     "call_to_action": {"type": "VIEW_INSTAGRAM_PROFILE"}}})
        ad = retry(lambda **k: post(f"{ACT}/ads", **k), name="IG Followers · POV Email · Nov26", adset_id=e["adset"],
                   creative={"creative_id": cr["id"]}, status="PAUSED")
        e.update(creative=cr["id"], ad=ad["id"]); print("Engagement ad:", ad["id"])
    except MetaError as err:
        e["ad_error"] = str(err)[:400]; print("Engagement ad ERROR:", str(err)[:400])
    STATE.write_text(json.dumps(st, indent=2, ensure_ascii=False))
