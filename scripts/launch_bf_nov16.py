"""Nov 16 2am launch (user order). Measurement verified: Lead x2, CompleteRegistration x2 (server), Subscribe x1
in the 03:00 and 04:00 UTC pixel blocks after the test submissions."""
import json, time
from meta import get, post, BUILD, MetaError

ACT, PAGE, IG, PIXEL = "act_1806647434085082", "1132642053254708", "17841430599113385", "2271987886986577"
STATE = BUILD / "nov2026.json"
st = json.loads(STATE.read_text()); b = st["build"]; s = b["bf16"]; e = b["engagement"]
save = lambda: STATE.write_text(json.dumps(st, indent=2, ensure_ascii=False))
log = []


def retry(fn, *a, **k):
    for _ in range(8):
        try:
            return fn(*a, **k)
        except MetaError as err:
            if any(c in str(err) for c in ('"code": 17', "(#613)", "2446079", "80004")):
                time.sleep(45); continue
            raise


# 1-2) Healthcare and Entrepreneurs: ad + activate
for key, label, camp, adset, cr in (("hc", "Healthcare", s["hc_campaign"], s["hc_adset"], s["hc_creative"]),
                                     ("ent", "Entrepreneurs", s["ent_campaign"], s["ent_adset"], s["ent_creative"])):
    if f"{key}_ad" not in s:
        s[f"{key}_ad"] = retry(post, f"{ACT}/ads", name=f"BF · {label} · Get started free · Nov16", adset_id=adset,
                               creative={"creative_id": cr}, status="ACTIVE")["id"]; save()
    retry(post, adset, status="ACTIVE"); retry(post, camp, status="ACTIVE")
    log.append(f"{label}: activo (anuncio {s[key + '_ad']})")

# 3) Awareness: Legal off, other 5 at $0.70/day (fallback $1.00 if Meta refuses)
retry(post, b["aw_Legal"]["adset"], status="PAUSED")
aw_day = 70
for v in ("RealEstate", "Accounting", "Finance", "Entrepreneurs", "Healthcare"):
    try:
        retry(post, b[f"aw_{v}"]["adset"], daily_budget=aw_day)
    except MetaError as err:
        if aw_day == 70:
            log.append(f"Awareness: Meta no acepta $0.70/día ({str(err)[:120]}); uso $1.00")
            aw_day = 100
            retry(post, b[f"aw_{v}"]["adset"], daily_budget=aw_day)
        else:
            raise
if aw_day == 100:
    for v in ("RealEstate", "Accounting", "Finance", "Entrepreneurs", "Healthcare"):
        retry(post, b[f"aw_{v}"]["adset"], daily_budget=100)
log.append(f"Awareness: Legal en pausa; 5 mercados a ${aw_day/100:.2f}/día")
b["aw_daily_from_nov16"] = aw_day

# 4) IG Followers
for k in ("ad_eng_3x4", "ad_eng_9x16"):
    st_ad = get(e[k], fields="effective_status,ad_review_feedback")
    log.append(f"IG {k}: revisión {st_ad.get('effective_status')} {st_ad.get('ad_review_feedback') or ''}")
    retry(post, e[k], status="ACTIVE")
retry(post, e["adset"], status="ACTIVE"); retry(post, e["campaign"], status="ACTIVE")
log.append("IG Followers: activa ($3/día)")

# 5) Retargeting
if "rt_campaign" not in s:
    s["rt_campaign"] = retry(post, f"{ACT}/campaigns", name="🟢 Orchid · Retargeting video · BF · Nov 2026", objective="OUTCOME_LEADS",
                             status="PAUSED", special_ad_categories=[], is_adset_budget_sharing_enabled="false")["id"]; save()
if "rt_adset" not in s:
    src = get(s["ent_adset"], fields="attribution_spec,adset_schedule,end_time")
    s["rt_adset"] = retry(post, f"{ACT}/adsets", name="RT · Video engaged 60D · 6am-10pm · Nov26", campaign_id=s["rt_campaign"],
                          status="PAUSED", lifetime_budget=3000, start_time="2026-11-16T06:00:00-0500", end_time=src["end_time"],
                          pacing_type=["day_parting"], adset_schedule=src["adset_schedule"], billing_event="IMPRESSIONS",
                          bid_strategy="LOWEST_COST_WITHOUT_CAP", optimization_goal="OFFSITE_CONVERSIONS", destination_type="WEBSITE",
                          promoted_object={"pixel_id": PIXEL, "custom_event_type": "LEAD"}, attribution_spec=src["attribution_spec"],
                          targeting={"geo_locations": {"countries": ["US"]}, "age_min": 25, "age_max": 65,
                                     "custom_audiences": [{"id": "120257825633920196"}],
                                     "excluded_custom_audiences": [{"id": "120257005715340196"}],
                                     "targeting_automation": {"advantage_audience": 0},
                                     "publisher_platforms": ["facebook"], "facebook_positions": ["feed"],
                                     "device_platforms": ["mobile", "desktop"]})["id"]; save()
if "rt_creative" not in s:
    c = json.loads((BUILD / "copy_bf_nov16.json").read_text())["ent"]
    link, h = "https://go.orchidpros.com/business-free-month", s["images"]["ent_4x5"]
    OPT_OUT = ["text_optimizations", "image_touchups", "image_templates", "image_uncrop", "image_animation",
               "enhance_cta", "description_automation", "add_text_overlay", "adapt_to_placement", "video_auto_crop"]
    feed = {"bodies": [{"text": t} for t in c["bodies"]], "titles": [{"text": t} for t in c["titles"]],
            "descriptions": [{"text": c["description"]}], "images": [{"hash": h}],
            "link_urls": [{"website_url": link, "display_url": "orchidpros.com"}],
            "call_to_action_types": ["SIGN_UP"], "ad_formats": ["SINGLE_IMAGE"], "optimization_type": "DEGREES_OF_FREEDOM"}
    oss = {"page_id": PAGE, "instagram_user_id": IG,
           "link_data": {"link": link, "image_hash": h, "message": c["bodies"][0], "name": c["titles"][0],
                         "call_to_action": {"type": "SIGN_UP", "value": {"link": link}}}}
    s["rt_creative"] = retry(post, f"{ACT}/adcreatives", name="bf16 · Retargeting · Get started free", object_story_spec=oss,
                             asset_feed_spec=feed, degrees_of_freedom_spec={"creative_features_spec": {k: {"enroll_status": "OPT_OUT"} for k in OPT_OUT}},
                             url_tags="utm_source=meta&utm_medium=paid&utm_campaign=bf_retargeting_nov26&utm_term={{adset.name}}&utm_content={{ad.name}}")["id"]; save()
if "rt_ad" not in s:
    s["rt_ad"] = retry(post, f"{ACT}/ads", name="RT · Get started free · Nov16", adset_id=s["rt_adset"],
                       creative={"creative_id": s["rt_creative"]}, status="ACTIVE")["id"]; save()
retry(post, s["rt_adset"], status="ACTIVE"); retry(post, s["rt_campaign"], status="ACTIVE")
log.append("Retargeting: activo ($30 total)")
save()
print("\n".join(log))
for c in (s["hc_campaign"], s["ent_campaign"], s["rt_campaign"], e["campaign"], b["aw_campaign"], b["lead_campaign"]):
    r = get(c, fields="name,effective_status"); print(r["effective_status"], "·", r["name"])
for a in (s["hc_ad"], s["ent_ad"], s["rt_ad"], e["ad_eng_3x4"], e["ad_eng_9x16"]):
    r = get(a, fields="name,effective_status"); print("  ad", r["effective_status"], "·", r["name"])
