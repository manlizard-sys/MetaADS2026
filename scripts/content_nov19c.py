"""Nov 19 (user order): CTA "Book now" (BOOK_NOW) on every lead/retargeting ad, copy tuned for Andromeda
(audience named in the first words, one clear angle per ad, offer + deadline), and Debi's "Same work. 60% less."
comparison ad added as a 2nd ad in each LPV ad set (4:5 feeds, 9:16 stories/reels).
Usage: python3 content_nov19c.py [--validate]"""
import base64, json, sys, time
from meta import get, post, BUILD, MetaError

ACT, PAGE, IG = "act_1806647434085082", "1132642053254708", "17841430599113385"
V = "--validate" in sys.argv
EX = {"execution_options": ["validate_only"]} if V else {}
STATE = BUILD / "nov2026.json"; st = json.loads(STATE.read_text())
b, l = st["build"]["bf16"], st["build"]["lpv19"]; s = st["build"].setdefault("content19", {})
save = lambda: None if V else STATE.write_text(json.dumps(st, indent=2, ensure_ascii=False))
COPY = json.loads((BUILD / "copy_nov19.json").read_text())
LP = {"hc": "https://go.orchidpros.com/practices-free-month", "ent": "https://go.orchidpros.com/business-free-month"}
CAMP = {"hc": "bf_healthcare_nov26", "ent": "bf_entrepreneurs_nov26"}
NAME = {"hc": "Healthcare", "ent": "Entrepreneurs"}
UTM = "utm_source=meta&utm_medium=paid&utm_campaign={c}&utm_term={{{{adset.name}}}}&utm_content={{{{ad.name}}}}"
OPT_OUT = ["text_optimizations", "image_touchups", "image_templates", "image_uncrop", "image_animation",
           "enhance_cta", "description_automation", "add_text_overlay", "adapt_to_placement"]
DOF = {"creative_features_spec": {k: {"enroll_status": "OPT_OUT"} for k in OPT_OUT}}
CTA = "BOOK_TRAVEL"  # label "Book now"; BOOK_NOW is rejected for OUTCOME_LEADS asset-feed ads


def retry(fn, *a, **k):
    for _ in range(8):
        try:
            return fn(*a, **k)
        except MetaError as e:
            if any(c in str(e) for c in ('"code": 17', "(#613)", "2446079", "80004")):
                time.sleep(45); continue
            raise


imgs = s.setdefault("images", {})
for n in ("4x5", "9x16"):
    if f"sw_{n}" not in imgs and not V:
        r = retry(post, f"{ACT}/adimages", name=f"same_work_{n}.png",
                  bytes=base64.b64encode((BUILD / "creatives" / "same_work" / f"same_work_{n}.png").read_bytes()).decode())
        imgs[f"sw_{n}"] = next(iter(r["images"].values()))["hash"]; save()
imgs.setdefault("sw_4x5", b["images"]["hc_4x5"]); imgs.setdefault("sw_9x16", b["images"]["hc_9x16"])  # validate-only stand-ins


def pac(name, key, copy, feed_hash, vert_hash):
    c = COPY[copy]
    afs = {"images": [{"hash": feed_hash, "adlabels": [{"name": "feed"}]}, {"hash": vert_hash, "adlabels": [{"name": "vertical"}]}],
           "bodies": [{"text": c["body"]}], "titles": [{"text": c["title"]}], "descriptions": [{"text": c["description"]}],
           "link_urls": [{"website_url": LP[key], "display_url": "orchidpros.com"}],
           "call_to_action_types": [CTA], "ad_formats": ["SINGLE_IMAGE"], "optimization_type": "PLACEMENT",
           "asset_customization_rules": [
               {"customization_spec": {"publisher_platforms": ["facebook", "instagram"],
                                       "facebook_positions": ["feed", "marketplace", "video_feeds", "search", "profile_feed"],
                                       "instagram_positions": ["stream", "profile_feed", "ig_search"]},
                "image_label": {"name": "feed"}, "priority": 1},
               {"customization_spec": {"publisher_platforms": ["facebook", "instagram"],
                                       "facebook_positions": ["story", "facebook_reels"], "instagram_positions": ["story", "reels"]},
                "image_label": {"name": "vertical"}, "priority": 2},
               {"customization_spec": {}, "image_label": {"name": "feed"}, "priority": 3, "is_default": True}]}
    r = retry(post, f"{ACT}/adcreatives", name=name, object_story_spec={"page_id": PAGE, "instagram_user_id": IG},
              asset_feed_spec=afs, degrees_of_freedom_spec=DOF, url_tags=UTM.format(c=CAMP[key]), **EX)
    return r.get("id") or r


for key in ("hc", "ent"):
    i = b["images"]
    # 1) BF ad: new copy + Book now, swapped onto the existing LPV ad (keeps its name -> same utm_content)
    if f"{key}_bf_creative" not in s:
        r = pac(f"c19 · {NAME[key]} · BF · BookNow", key, f"{key}_bf", i[f"{key}_4x5"], i[f"{key}_9x16"]); print(key, "bf creative", r)
        if not V:
            s[f"{key}_bf_creative"] = r; save()
    if not V and not s.get(f"{key}_bf_swapped"):
        retry(post, l[f"{key}_ad"], creative={"creative_id": s[f"{key}_bf_creative"]}); s[f"{key}_bf_swapped"] = True; save()
        print(key, "bf ad creative swapped")
    # 2) Same work ad
    if f"{key}_sw_creative" not in s:
        r = pac(f"c19 · {NAME[key]} · SameWork · BookNow", key, f"{key}_sw", imgs["sw_4x5"], imgs["sw_9x16"]); print(key, "sw creative", r)
        if not V:
            s[f"{key}_sw_creative"] = r; save()
    if not V and f"{key}_sw_ad" not in s:
        s[f"{key}_sw_ad"] = retry(post, f"{ACT}/ads", name=f"SameWork · {NAME[key]} · 60% less · Nov19", adset_id=l[f"{key}_adset"],
                                  creative={"creative_id": s[f"{key}_sw_creative"]}, status="ACTIVE")["id"]; save()
        print(key, "sw ad", s[f"{key}_sw_ad"])

# 3) Retargeting: same copy and image, CTA -> Book now
if "rt_creative" not in s:
    old = get(b["rt_creative"], fields="asset_feed_spec,object_story_spec,url_tags,degrees_of_freedom_spec")
    afs = old["asset_feed_spec"]; afs["call_to_action_types"] = [CTA]
    for k in list(afs):
        if k not in ("images", "bodies", "titles", "descriptions", "link_urls", "call_to_action_types", "ad_formats", "optimization_type"):
            afs.pop(k)
    afs["images"] = [{"hash": x["hash"]} for x in afs["images"]]
    oss = old["object_story_spec"]; ld = oss["link_data"]; ld["call_to_action"]["type"] = CTA
    afs["link_urls"] = [{"website_url": ld["link"], "display_url": "orchidpros.com"}]
    afs.setdefault("ad_formats", ["SINGLE_IMAGE"])
    oss = {"page_id": PAGE, "instagram_user_id": IG, "link_data": {k: ld[k] for k in ("link", "image_hash", "message", "name", "call_to_action") if k in ld}}
    r = retry(post, f"{ACT}/adcreatives", name="c19 · Retargeting · BookNow", object_story_spec=oss, asset_feed_spec=afs,
              degrees_of_freedom_spec=DOF, url_tags=old["url_tags"], **EX)
    print("rt creative", r)
    if not V:
        s["rt_creative"] = r["id"]; save()
if not V and not s.get("rt_swapped"):
    retry(post, b["rt_ad"], creative={"creative_id": s["rt_creative"]}); s["rt_swapped"] = True; save(); print("rt ad creative swapped")
print(json.dumps(s, indent=1))
