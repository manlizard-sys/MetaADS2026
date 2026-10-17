"""Swap the CTA of S9, S10 and 🔵 S11 (hyperlocal) from BOOK_NOW to BOOK_TRAVEL.

BOOK_NOW opens the Page's native appointment form ("Request date & time") instead of the landing,
so requests never reach GHL. BOOK_TRAVEL also reads "Book now" but follows the link (same as V2).
Clones each creative with the new CTA and points the ad to it. Default is a dry run; --apply changes Meta.
"""
import copy, json, sys
from meta import get, post, BUILD

ACT = "act_1806647434085082"
ADS = ["120257317011800196", "120257317011860196", "120257318010750196"]  # S9, S10, S11 (hyperlocal)
FIELDS = "name,object_story_spec,asset_feed_spec,degrees_of_freedom_spec,url_tags"
apply = "--apply" in sys.argv
backup = []
for ad_id in ADS:
    ad = get(ad_id, fields="name,creative{id}")
    cr = get(ad["creative"]["id"], fields=FIELDS)
    ld = cr["object_story_spec"]["link_data"]
    print(f"{ad['name']}: CTA {ld['call_to_action']['type']} -> BOOK_TRAVEL")
    backup.append({"ad_id": ad_id, "name": ad["name"], "old_creative_id": cr["id"]})
    if not apply:
        continue
    oss = copy.deepcopy(cr["object_story_spec"])
    oss["link_data"]["call_to_action"] = {"type": "BOOK_TRAVEL", "value": {"link": ld["link"], "link_caption": "orchidpros.com"}}
    oss["link_data"].pop("image_url", None)  # image_hash is kept
    dof = {"creative_features_spec": {k: {"enroll_status": "OPT_OUT"}
           for k in cr.get("degrees_of_freedom_spec", {}).get("creative_features_spec", {})
           if k not in ("standard_enhancements", "advantage_plus_creative")}}
    afs = {k: v for k, v in cr.get("asset_feed_spec", {}).items() if k in ("images", "bodies", "titles", "descriptions", "optimization_type")}
    afs["images"] = [{"hash": i["hash"]} for i in afs.get("images", [])] or None
    afs = {k: v for k, v in afs.items() if v}
    afs["bodies"] = [{"text": b["text"]} for b in afs.get("bodies", [])]
    afs["titles"] = [{"text": t["text"]} for t in afs.get("titles", [])]
    afs["descriptions"] = [{"text": d["text"]} for d in afs.get("descriptions", [])]
    new = post(f"{ACT}/adcreatives", name=f"{cr['name']} · CTA fix", object_story_spec=oss,
               asset_feed_spec=afs, degrees_of_freedom_spec=dof, url_tags=cr.get("url_tags", ""))
    post(ad_id, creative={"creative_id": new["id"]})
    backup[-1]["new_creative_id"] = new["id"]
    print(f"   listo: nuevo creativo {new['id']}")
if apply:
    (BUILD / "cta-fix-2026-10-17.json").write_text(json.dumps(backup, indent=2), encoding="utf-8")
else:
    print("\nVista previa. Nada cambió. Ejecuta con --apply.")
