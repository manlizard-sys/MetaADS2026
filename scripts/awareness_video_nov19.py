"""Nov 19 (user order): founders video ("video web 2", Andrea + Josue) as a 2nd ad in each active awareness ad set.
16:9 on feeds, 9:16 (padded) on stories/reels, CTA Book now (BOOK_TRAVEL), English copy that names the audience.
Usage: python3 awareness_video_nov19.py [--validate]"""
import json, sys, time
from meta import get, get_all, post, BUILD, MetaError

ACT = "act_1806647434085082"
V = "--validate" in sys.argv
EX = {"execution_options": ["validate_only"]} if V else {}
STATE = BUILD / "nov2026.json"; st = json.loads(STATE.read_text()); s = st["build"]["video_web2"]
save = lambda: None if V else STATE.write_text(json.dumps(st, indent=2, ensure_ascii=False))
BODY = ("U.S. business owners: if you've become the boss, the assistant, the receptionist and the bookkeeper, this is for you. "
        "Andrea and Josue, Orchid's owners, explain how we connect businesses with bilingual virtual professionals from Colombia "
        "and help them save 40–50% on staffing costs. We work for free until you find the right person. Book a call with us.")
TITLE = "Save 40–50% on staffing costs"
DESC = "Vetted, bilingual professionals from Colombia, working your U.S. hours."


def retry(fn, *a, **k):
    for _ in range(8):
        try:
            return fn(*a, **k)
        except MetaError as e:
            if any(c in str(e) for c in ('"code": 17', "(#613)", "2446079", "80004")):
                time.sleep(45); continue
            raise


thumb = {k: get(s[k], fields="picture")["picture"] for k in ("v169", "v916")}
ads = [a for a in get_all(f"{ACT}/ads", fields="name,adset_id,creative{id}", effective_status=json.dumps(["ACTIVE", "PENDING_REVIEW", "IN_PROCESS"]), limit=100)
       if a["name"].startswith("V1 · POVEmail")]
for a in ads:
    vert = a["name"].split(" · ")[2]
    key = f"ad_{vert}"
    if key in s:
        continue
    c = get(a["creative"]["id"], fields="object_story_spec,asset_feed_spec,url_tags,degrees_of_freedom_spec")
    f = c["asset_feed_spec"]
    rules = [{"customization_spec": r["customization_spec"], "video_label": {"name": r["video_label"]["name"]}, "priority": r["priority"]}
             for r in f["asset_customization_rules"]]
    afs = {"videos": [{"video_id": s["v916"], "thumbnail_url": thumb["v916"], "adlabels": [{"name": "vert"}]},
                      {"video_id": s["v169"], "thumbnail_url": thumb["v169"], "adlabels": [{"name": "sq"}]}],
           "bodies": [{"text": BODY}], "titles": [{"text": TITLE}], "descriptions": [{"text": DESC}], "link_urls": f["link_urls"],
           "call_to_action_types": ["BOOK_TRAVEL"], "ad_formats": ["SINGLE_VIDEO"], "optimization_type": "PLACEMENT",
           "asset_customization_rules": rules}
    r = retry(post, f"{ACT}/adcreatives", name=f"aw19 · Founders video · {vert} · BookNow", object_story_spec=c["object_story_spec"],
              asset_feed_spec=afs, degrees_of_freedom_spec=c["degrees_of_freedom_spec"], url_tags=c["url_tags"], **EX)
    print(vert, r)
    if not V:
        s[key] = retry(post, f"{ACT}/ads", name=f"V2 · Founders · {vert} · Nov19", adset_id=a["adset_id"],
                       creative={"creative_id": r["id"]}, status="ACTIVE")["id"]; save(); print("  ad", s[key])
