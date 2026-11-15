"""Nov 15 (user order): build everything PAUSED for the Nov 16 launch.
- Engagement (IG Followers campaign 120257780775350196): $3/day, new videos (3:4 feed, 9:16 reels/stories).
- BF images uploaded (healthcare + entrepreneurs; 4:5 used on Facebook feed).
- BF · Healthcare: creative ready (ad created only once the landing is live).
- New campaign "Orchid · Entrepreneurs · BF · Nov 2026": ad set (entrepreneurs signals + Advantage+), creative ready.
State: build/nov2026.json -> build.bf16."""
import base64, json, sys, time, requests
from pathlib import Path
from meta import get, post, BUILD, MetaError, GRAPH, HEADERS, _handle

ACT, PAGE, IG, PIXEL = "act_1806647434085082", "1132642053254708", "17841430599113385", "2271987886986577"
SRC = BUILD / "creatives" / "bf_nov16"
STATE = BUILD / "nov2026.json"
st = json.loads(STATE.read_text()); b = st["build"]; s = b.setdefault("bf16", {})
save = lambda: STATE.write_text(json.dumps(st, indent=2, ensure_ascii=False))
START, END = "2026-11-16T06:00:00-0500", "2026-11-30T23:59:00-0500"
UTM = "utm_source=meta&utm_medium=paid&utm_campaign={c}&utm_term={{{{adset.name}}}}&utm_content={{{{ad.name}}}}"
OPT_OUT = ["text_optimizations", "image_touchups", "image_templates", "image_uncrop", "image_animation",
           "enhance_cta", "description_automation", "add_text_overlay", "adapt_to_placement", "video_auto_crop"]
dof = lambda: {"creative_features_spec": {k: {"enroll_status": "OPT_OUT"} for k in OPT_OUT}}
LP = {"hc": "https://go.orchidpros.com/practices-free-month", "ent": "https://go.orchidpros.com/business-free-month"}
COPY = json.loads((BUILD / "copy_bf_nov16.json").read_text())


def retry(fn, *a, **k):
    for _ in range(8):
        try:
            return fn(*a, **k)
        except MetaError as e:
            if any(c in str(e) for c in ('"code": 17', "(#613)", "2446079", "80004")):
                time.sleep(45); continue
            raise


# 1) uploads
imgs = s.setdefault("images", {})
for n in ("hc_4x5", "hc_9x16", "hc_1x1", "ent_4x5", "ent_9x16", "ent_1x1"):
    if n not in imgs:
        r = retry(post, f"{ACT}/adimages", bytes=base64.b64encode((SRC / f"{n}.png").read_bytes()).decode(), name=f"bf16_{n}.png")
        imgs[n] = next(iter(r["images"].values()))["hash"]; save(); print("img", n)
vids = s.setdefault("videos", {})
for n in ("eng_3x4", "eng_9x16"):
    if n not in vids:
        with open(SRC / f"{n}.mov", "rb") as fh:
            r = _handle(requests.post(f"{GRAPH}/{ACT}/advideos", headers=HEADERS, data={"name": f"Engagement · {n} · Nov26"},
                                      files={"source": (f"{n}.mov", fh, "video/quicktime")}, timeout=600))
        vids[n] = r["id"]; save(); print("video", n, r["id"])


def thumb(v):
    for _ in range(40):
        try:
            d = get(v, fields="status,thumbnails{uri,is_preferred}")
            th = (d.get("thumbnails") or {}).get("data") or []
            if d.get("status", {}).get("video_status") == "ready" and th:
                return next((t["uri"] for t in th if t.get("is_preferred")), th[0]["uri"])
        except MetaError:
            pass
        time.sleep(15)
    raise SystemExit(f"video {v} not processed yet")


# 2) engagement: $3/day, IG feed + reels + stories, two video ads (paused)
e = b["engagement"]
retry(post, e["adset"], daily_budget=300, targeting={"geo_locations": {"countries": ["US"]}, "age_min": 25, "age_max": 65,
      "targeting_automation": {"advantage_audience": 1}, "publisher_platforms": ["instagram"],
      "instagram_positions": ["stream", "story", "reels"]})
ENG_MSG = "Does your assistant speak Spanish? Orchid places bilingual professionals from Colombia on U.S. teams, working your hours. Follow us for what that looks like day to day."
for n, label in (("eng_3x4", "Feed 3x4"), ("eng_9x16", "Vertical 9x16")):
    k = f"ad_{n}"
    if k in e:
        continue
    cr = retry(post, f"{ACT}/adcreatives", name=f"IG followers · VA Spanish · {label}",
               object_story_spec={"page_id": PAGE, "instagram_user_id": IG,
                                  "video_data": {"video_id": vids[n], "image_url": thumb(vids[n]), "message": ENG_MSG,
                                                 "call_to_action": {"type": "VIEW_INSTAGRAM_PROFILE"}}})
    ad = retry(post, f"{ACT}/ads", name=f"IG Followers · VA Spanish · {label} · Nov15", adset_id=e["adset"],
               creative={"creative_id": cr["id"]}, status="PAUSED")
    e[k] = ad["id"]; save(); print("engagement ad", n, ad["id"])
if e.get("ad"):
    retry(post, e["ad"], status="PAUSED")  # old POV ad stays off


def image_creative(name, key, camp):
    c = COPY[key]; link = LP[key]
    feed = {"bodies": [{"text": t} for t in c["bodies"]], "titles": [{"text": t} for t in c["titles"]],
            "descriptions": [{"text": c["description"]}], "images": [{"hash": imgs[f"{key}_4x5"]}],
            "link_urls": [{"website_url": link, "display_url": "orchidpros.com"}],
            "call_to_action_types": ["SIGN_UP"], "ad_formats": ["SINGLE_IMAGE"], "optimization_type": "DEGREES_OF_FREEDOM"}
    oss = {"page_id": PAGE, "instagram_user_id": IG,
           "link_data": {"link": link, "image_hash": imgs[f"{key}_4x5"], "message": c["bodies"][0], "name": c["titles"][0],
                         "call_to_action": {"type": "SIGN_UP", "value": {"link": link}}}}
    return retry(post, f"{ACT}/adcreatives", name=name, object_story_spec=oss, asset_feed_spec=feed,
                 degrees_of_freedom_spec=dof(), url_tags=UTM.format(c=camp))["id"]


# 3) healthcare creative (ad is created at launch, once the landing answers 200)
if "hc_creative" not in s:
    s["hc_creative"] = image_creative("bf16 · Healthcare · Get started free", "hc", "bf_healthcare_nov26"); save(); print("hc creative")

# 4) entrepreneurs campaign + ad set + creative
if "ent_campaign" not in s:
    s["ent_campaign"] = retry(post, f"{ACT}/campaigns", name="Orchid · Entrepreneurs · BF · Nov 2026", objective="OUTCOME_LEADS",
                              status="PAUSED", special_ad_categories=[], is_adset_budget_sharing_enabled="false")["id"]; save()
if "ent_adset" not in s:
    attr = get("120257589638070196", fields="attribution_spec")["attribution_spec"]
    t = {"geo_locations": {"countries": ["US"], "location_types": ["home", "recent"]},
         "age_min": 25, "age_max": 65, "age_range": [30, 65],
         "flexible_spec": [{"interests": [{"id": "6003371567474"}, {"id": "6002884511422"}],
                            "behaviors": [{"id": "6002714898572"}, {"id": "6020530281783"}]}],
         "excluded_custom_audiences": [{"id": "120257005715340196"}],
         "targeting_automation": {"advantage_audience": 1},
         "publisher_platforms": ["facebook"], "facebook_positions": ["feed"], "device_platforms": ["mobile", "desktop"]}
    s["ent_adset"] = retry(post, f"{ACT}/adsets", name="BF · Entrepreneurs · Get started free · 6am-10pm · Nov26",
                           campaign_id=s["ent_campaign"], status="PAUSED", lifetime_budget=12000, start_time=START, end_time=END,
                           pacing_type=["day_parting"],
                           adset_schedule=[{"days": [0, 1, 2, 3, 4, 5, 6], "start_minute": 360, "end_minute": 1320, "timezone_type": "USER"}],
                           billing_event="IMPRESSIONS", bid_strategy="LOWEST_COST_WITHOUT_CAP", optimization_goal="OFFSITE_CONVERSIONS",
                           destination_type="WEBSITE", promoted_object={"pixel_id": PIXEL, "custom_event_type": "LEAD"},
                           attribution_spec=attr, targeting=t)["id"]; save(); print("ent adset", s["ent_adset"])
if "ent_creative" not in s:
    s["ent_creative"] = image_creative("bf16 · Entrepreneurs · Get started free", "ent", "bf_entrepreneurs_nov26"); save(); print("ent creative")
print(json.dumps(s, indent=1))
