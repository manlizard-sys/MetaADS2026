"""Nov 19 (user order): awareness ads get CTA "Book now" (BOOK_TRAVEL) and a neutral description
(the old one said "law firms and real estate teams" on every vertical). Same videos, copy, UTM and ad names.
Usage: python3 awareness_booknow_nov19.py [--validate]"""
import json, sys, time
from meta import get, get_all, post, BUILD, MetaError

ACT = "act_1806647434085082"
V = "--validate" in sys.argv
EX = {"execution_options": ["validate_only"]} if V else {}
DESC = "Vetted, bilingual professionals from Colombia, working your U.S. hours."
STATE = BUILD / "nov2026.json"; st = json.loads(STATE.read_text()); s = st["build"].setdefault("aw_booknow19", {})
save = lambda: None if V else STATE.write_text(json.dumps(st, indent=2, ensure_ascii=False))


def retry(fn, *a, **k):
    for _ in range(8):
        try:
            return fn(*a, **k)
        except MetaError as e:
            if any(c in str(e) for c in ('"code": 17', "(#613)", "2446079", "80004")):
                time.sleep(45); continue
            raise


ads = [a for a in get_all(f"{ACT}/ads", fields="name,creative{id}", effective_status=json.dumps(["ACTIVE"]), limit=100)
       if a["name"].startswith("V1 · POVEmail")]
for a in ads:
    if a["id"] in s:
        continue
    c = get(a["creative"]["id"], fields="name,object_story_spec,asset_feed_spec,url_tags,degrees_of_freedom_spec")
    f = c["asset_feed_spec"]
    afs = {"videos": [{"video_id": v["video_id"], "thumbnail_url": v["thumbnail_url"], "adlabels": [{"name": v["adlabels"][0]["name"]}]} for v in f["videos"]],
           "bodies": f["bodies"], "titles": f["titles"], "descriptions": [{"text": DESC}], "link_urls": f["link_urls"],
           "call_to_action_types": ["BOOK_TRAVEL"], "ad_formats": f["ad_formats"], "optimization_type": f["optimization_type"],
           "asset_customization_rules": [{"customization_spec": r["customization_spec"], "video_label": {"name": r["video_label"]["name"]},
                                          "priority": r["priority"]} for r in f["asset_customization_rules"]]}
    r = retry(post, f"{ACT}/adcreatives", name=f"aw19 · {a['name']} · BookNow", object_story_spec=c["object_story_spec"],
              asset_feed_spec=afs, degrees_of_freedom_spec=c["degrees_of_freedom_spec"], url_tags=c["url_tags"], **EX)
    print(a["name"], r)
    if not V:
        retry(post, a["id"], creative={"creative_id": r["id"]}); s[a["id"]] = r["id"]; save(); print("  swapped")
