"""November 2026 launch: Awareness (20%) + Leads (80%) for $1,000/month, starting Nov 2 00:00 New York.

Stage 1 (--upload): images (A1, B1 in 4:5 and 9:16) and the POV video (9:16 + 1:1) uploaded once per
awareness vertical, so each vertical gets its own video IDs and its own "video viewers" audience.
Stage 2 (--audiences): website visitors 180D and video viewers 50% (all verticals) for the warm ad set.
Stage 3 (--build): both campaigns, ad sets and ads, ACTIVE with start_time at midnight (they wait for it).
State lives in build/nov2026.json so each stage can be re-run without duplicating anything.
"""
import json, sys, time, base64, datetime as dt
from pathlib import Path
import requests
from meta import get, post, GRAPH, HEADERS, BUILD, MetaError, _handle
from nov2026_audiences import VERTICALS, ATTORNEYS, targeting

ACT = "act_1806647434085082"
PAGE, IG, PIXEL = "1132642053254708", "17841430599113385", "2271987886986577"
SRC = Path("/tmp/claude-0/-home-user-MetaADS2026/27e2161b-3c6a-5b52-b16f-7542f191664c/scratchpad/nov")
STATE = BUILD / "nov2026.json"
START = "2026-11-02T00:00:00-0500"
END = "2026-11-30T23:59:00-0500"
DAYS = 29
st = json.loads(STATE.read_text()) if STATE.exists() else {}
save = lambda: STATE.write_text(json.dumps(st, indent=2, ensure_ascii=False))

# ---------------- Stage 1: uploads ----------------
if "--upload" in sys.argv:
    imgs = st.setdefault("images", {})
    for n in ("A1_4x5", "A1_9x16", "B1_4x5", "B1_9x16", "A1_1x1", "B1_1x1"):
        if n not in imgs:
            r = post(f"{ACT}/adimages", bytes=base64.b64encode((SRC / f"{n}.png").read_bytes()).decode(), name=f"nov26_{n}.png")
            imgs[n] = next(iter(r["images"].values()))["hash"]; save(); print("img", n, imgs[n])
    vids = st.setdefault("videos", {})
    for v in VERTICALS:
        for fmt, f in (("9x16", "V1.mp4"), ("1x1", "V1b.mp4")):
            key = f"{v}_{fmt}"
            if key in vids:
                continue
            with open(SRC / f, "rb") as fh:
                r = _handle(requests.post(f"{GRAPH}/{ACT}/advideos", headers=HEADERS,
                                          data={"name": f"POV email · {v} · {fmt} · Nov26"}, files={"source": (f, fh, "video/mp4")}, timeout=600))
            vids[key] = r["id"]; save(); print("video", key, r["id"])

# ---------------- Stage 2: audiences ----------------
if "--audiences" in sys.argv:
    aud = st.setdefault("audiences", {})
    if "web180" not in aud:
        rule = {"inclusions": {"operator": "or", "rules": [{"event_sources": [{"id": PIXEL, "type": "pixel"}],
                "retention_seconds": 15552000, "filter": {"operator": "and", "filters": [{"field": "url", "operator": "i_contains", "value": "orchidpros.com"}]}}]}}
        aud["web180"] = post(f"{ACT}/customaudiences", name="WEB - Visitantes 180D", rule=json.dumps(rule), prefill="true")["id"]; save()
    if "video50" not in aud:
        ids = list(st["videos"].values())
        rule = [{"event_name": "video_view_50_percent", "object_id": i} for i in ids]
        aud["video50"] = post(f"{ACT}/customaudiences", name="VIDEO - 50% POV email Nov26 (todos los mercados)",
                              subtype="ENGAGEMENT", rule=json.dumps(rule), prefill="true")["id"]; save()
    print(aud)

print(json.dumps({k: (len(v) if isinstance(v, dict) else v) for k, v in st.items()}, indent=1))

# ---------------- Stage 3: campaigns, ad sets, ads ----------------
AW_BODY = ("Running a business shouldn't mean answering every call yourself. Orchid places verified, bilingual "
           "professionals from Colombia on your team, working your U.S. hours. Intake, scheduling, admin and "
           "back-office, handled. Terms apply.")
AW_TITLE = "Your bilingual assistant, U.S. hours"
A_BODIES = Path(__file__).with_name("nov2026_copy.json")
FEED = {"publisher_platforms": ["facebook", "instagram"], "facebook_positions": ["feed"], "instagram_positions": ["stream"]}
VERT = {"publisher_platforms": ["facebook", "instagram"], "facebook_positions": ["story", "facebook_reels"], "instagram_positions": ["story", "reels"]}
OPT_OUT = ["text_optimizations", "image_touchups", "image_templates", "image_uncrop", "image_animation",
           "enhance_cta", "description_automation", "add_text_overlay", "adapt_to_placement", "video_auto_crop"]
LEADS_180 = "120257005715340196"
ENGAGERS = ["120257005754220196", "120257005748740196"]  # FB / IG engagement 365D
UTM = "utm_source=meta&utm_medium=paid&utm_campaign={c}&utm_term={{{{adset.name}}}}&utm_content={{{{ad.name}}}}"


def dof():
    return {"creative_features_spec": {k: {"enroll_status": "OPT_OUT"} for k in OPT_OUT}}


def video_creative(name, v916, v11, link):
    pic = lambda v: get(v, fields="picture")["picture"]
    feed = {"videos": [{"video_id": v916, "thumbnail_url": pic(v916), "adlabels": [{"name": "vert"}]},
                       {"video_id": v11, "thumbnail_url": pic(v11), "adlabels": [{"name": "sq"}]}],
            "bodies": [{"text": AW_BODY}], "titles": [{"text": AW_TITLE}],
            "link_urls": [{"website_url": link, "display_url": "orchidpros.com"}],
            "call_to_action_types": ["LEARN_MORE"], "ad_formats": ["SINGLE_VIDEO"],
            "asset_customization_rules": [
                {"customization_spec": FEED, "video_label": {"name": "sq"}, "priority": 1},
                {"customization_spec": VERT, "video_label": {"name": "vert"}, "priority": 2}],
            "optimization_type": "PLACEMENT"}
    return post(f"{ACT}/adcreatives", name=name, object_story_spec={"page_id": PAGE, "instagram_user_id": IG},
                asset_feed_spec=feed, degrees_of_freedom_spec=dof(), url_tags=UTM.format(c="awareness_nov26"))["id"]


def image_creative(name, h45, h916, bodies, titles, link, cta):
    common = {"bodies": [{"text": b} for b in bodies], "titles": [{"text": t} for t in titles],
              "link_urls": [{"website_url": link, "display_url": "orchidpros.com"}],
              "call_to_action_types": [cta], "ad_formats": ["SINGLE_IMAGE"]}
    tries = [  # 1) per-placement images + 3 text variations; 2) flexible format, Meta picks the ratio per placement
        {**common, "images": [{"hash": h45, "adlabels": [{"name": "feed"}]}, {"hash": h916, "adlabels": [{"name": "vert"}]}],
         "asset_customization_rules": [{"customization_spec": FEED, "image_label": {"name": "feed"}, "priority": 1},
                                       {"customization_spec": VERT, "image_label": {"name": "vert"}, "priority": 2}],
         "optimization_type": "PLACEMENT"},
        {**common, "images": [{"hash": h45}, {"hash": h916}], "optimization_type": "DEGREES_OF_FREEDOM"},
    ]
    last = None
    for i, feed in enumerate(tries):
        for c in ([cta] if cta != "GET_STARTED" else ["GET_STARTED", "SIGN_UP"]):
            feed["call_to_action_types"] = [c]
            oss = {"page_id": PAGE, "instagram_user_id": IG}
            if i == 1:
                oss["link_data"] = {"link": link, "image_hash": h45, "message": bodies[0], "name": titles[0],
                                    "call_to_action": {"type": c, "value": {"link": link}}}
            try:
                cid = post(f"{ACT}/adcreatives", name=name, object_story_spec=oss, asset_feed_spec=feed,
                           degrees_of_freedom_spec=dof(), url_tags=UTM.format(c="attorneys_nov26"))["id"]
                print(f"   creativo {name}: modo {'placement' if i == 0 else 'flexible'} · CTA {c}")
                return cid
            except MetaError as e:
                last = e; print(f"   intento {i+1}/{c} rechazado: {str(e)[:160].replace(chr(10), ' ')}")
    raise last


if "--build" in sys.argv:
    b = st.setdefault("build", {})
    copy = json.loads(A_BODIES.read_text())
    aw_day = round(20000 / DAYS / len(VERTICALS))          # cents per vertical
    lead_day = round(80000 / DAYS)
    warm_day = 800
    if "aw_campaign" not in b:
        b["aw_campaign"] = post(f"{ACT}/campaigns", name="Orchid · Awareness · Video POV · Nov 2026",
                                objective="OUTCOME_AWARENESS", special_ad_categories="[]", is_adset_budget_sharing_enabled="false", status="PAUSED")["id"]; save()
    for v in VERTICALS:
        k = f"aw_{v}"
        if k in b:
            continue
        aset = post(f"{ACT}/adsets", name=f"AW · {v} · US 25-65 · Nov26", campaign_id=b["aw_campaign"],
                    daily_budget=aw_day, billing_event="IMPRESSIONS", optimization_goal="THRUPLAY",
                    bid_strategy="LOWEST_COST_WITHOUT_CAP", start_time=START, end_time=END,
                    targeting=targeting(VERTICALS[v]), status="PAUSED")["id"]
        cr = video_creative(f"nov26 · AW · {v}", st["videos"][f"{v}_9x16"], st["videos"][f"{v}_1x1"], "https://orchidpros.com/")
        ad = post(f"{ACT}/ads", name=f"V1 · POVEmail · {v} · Nov01", adset_id=aset, creative={"creative_id": cr}, status="ACTIVE")["id"]
        b[k] = {"adset": aset, "creative": cr, "ad": ad}; save(); print("AW", v, aset, ad)

    if "lead_campaign" not in b:
        b["lead_campaign"] = post(f"{ACT}/campaigns", name="Orchid · Attorneys · Nov 2026", objective="OUTCOME_LEADS",
                                  special_ad_categories="[]", is_adset_budget_sharing_enabled="false", status="PAUSED")["id"]; save()
    if "cr_A1" not in b:
        b["cr_A1"] = image_creative("nov26 · A1 · $0Upfront · Black", st["images"]["A1_4x5"], st["images"]["A1_9x16"],
                                    copy["A"]["bodies"], copy["A"]["titles"], "https://go.orchidpros.com/hire-50off", "GET_OFFER"); save()
    if "cr_B1" not in b:
        b["cr_B1"] = image_creative("nov26 · B1 · GetStartedFree · Color", st["images"]["B1_4x5"], st["images"]["B1_9x16"],
                                    copy["B"]["bodies"], copy["B"]["titles"], "https://go.orchidpros.com/50off-form", "GET_STARTED"); save()
    lead_common = dict(campaign_id=b["lead_campaign"], billing_event="IMPRESSIONS", optimization_goal="OFFSITE_CONVERSIONS",
                       bid_strategy="LOWEST_COST_WITHOUT_CAP", promoted_object={"pixel_id": PIXEL, "custom_event_type": "LEAD"},
                       destination_type="WEBSITE", start_time=START, end_time=END, status="PAUSED",
                       attribution_spec=[{"event_type": "CLICK_THROUGH", "window_days": 7}, {"event_type": "VIEW_THROUGH", "window_days": 1}])
    warm_t = {"geo_locations": {"countries": ["US"]}, "age_min": 25, "age_max": 65,
              "custom_audiences": [{"id": st["audiences"]["web180"]}] + [{"id": i} for i in ENGAGERS],
              "excluded_custom_audiences": [{"id": LEADS_180}], "targeting_automation": {"advantage_audience": 0},
              **{k: v for k, v in targeting([]).items() if k.endswith("positions") or k == "publisher_platforms"}}
    pros_t = {**targeting(ATTORNEYS, 30, 65), "excluded_custom_audiences": [{"id": LEADS_180}]}
    for key, name, t, day in (("lead_warm", "Warm · Web 180D + FB/IG engagers + video 50% · US 25-65", warm_t, warm_day),
                              ("lead_pros", "Prospecting · Attorneys (law + SMB owners) · US 30-65", pros_t, lead_day - warm_day)):
        if key in b:
            continue
        aset = post(f"{ACT}/adsets", name=name, daily_budget=day, targeting=t, **lead_common)["id"]
        ads = {}
        for adname, cr in (("A1 · $0Upfront · Black · Nov01", b["cr_A1"]), ("B1 · GetStartedFree · Color · Nov01", b["cr_B1"])):
            ads[adname] = post(f"{ACT}/ads", name=adname, adset_id=aset, creative={"creative_id": cr}, status="ACTIVE")["id"]
        b[key] = {"adset": aset, "ads": ads, "daily": day}; save(); print("LEAD", key, aset, ads)

if "--activate" in sys.argv:
    b = st["build"]
    for k, v in b.items():
        if isinstance(v, dict) and "adset" in v:
            post(v["adset"], status="ACTIVE")
    for c in ("aw_campaign", "lead_campaign"):
        post(b[c], status="ACTIVE")
    print("Activado: campañas y conjuntos ACTIVE con inicio", START)
