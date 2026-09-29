"""Step 4: upload videos and build campaign / ad set / ads, all PAUSED. Idempotent via build/ids.json.

Usage: python3 step4_build.py --confirm      (only after steps 1-3 are approved)
Stops on the first API error and prints it (token scrubbed). Never touches existing objects.
"""
import json, sys, time, pathlib, html
import config as C
from copy_data import PRIMARY, HEADLINES, DESCRIPTIONS
from meta import get, post, save_ids, MetaError, BUILD, ROOT, GRAPH, API_VERSION

if "--confirm" not in sys.argv:
    sys.exit("Refusing to run without --confirm (requires approved audience and copy).")
missing = [k for k in ("PAGE_ID", "INSTAGRAM_USER_ID") if not getattr(C, k)] + \
          (["CONCEPTS"] if not C.CONCEPTS else []) + (["ENGLISH_LOCALES"] if not C.ENGLISH_LOCALES else []) + \
          (["APPROVED_INTERESTS/BEHAVIORS"] if not (C.APPROVED_INTERESTS or C.APPROVED_BEHAVIORS) else [])
if missing:
    sys.exit(f"Config incomplete: {missing}")

ids_path = BUILD / "ids.json"
ids = json.loads(ids_path.read_text()) if ids_path.exists() else {}
warnings = []


def step(label, fn):
    try:
        return fn()
    except MetaError as e:
        print(f"\nAPI ERROR during: {label}\n{e}")
        (BUILD / "last_error.json").write_text(json.dumps({"step": label, "error": str(e)}, indent=2))
        sys.exit(1)


# 1. Videos -----------------------------------------------------------------
VIDEO_GRAPH = GRAPH.replace("graph.facebook.com", "graph-video.facebook.com")
videos = ids.setdefault("videos", {})
for c in C.CONCEPTS:
    for slot in ("vertical", "feed"):
        path = c.get(slot)
        if not path or path in videos:
            continue
        f = ROOT / path
        with f.open("rb") as fh:
            r = step(f"upload {path}", lambda: post(f"{VIDEO_GRAPH}/{C.AD_ACCOUNT}/advideos",
                                                    files={"source": (f.name, fh)}, name=f.stem))
        videos[path] = {"id": r["id"]}
        save_ids(videos=videos)
        print("uploaded", path, r["id"])

for path, v in videos.items():
    for _ in range(90):  # up to ~15 min
        st = step(f"status {path}", lambda: get(v["id"], fields="status"))["status"]
        if st.get("video_status") == "ready":
            break
        if st.get("video_status") == "error":
            sys.exit(f"Video processing failed for {path}: {json.dumps(st)}")
        time.sleep(10)
    else:
        sys.exit(f"Timed out waiting for {path} to process")
    thumbs = step(f"thumbnails {path}", lambda: get(f"{v['id']}/thumbnails"))["data"]
    v["thumbnail_url"] = next((t["uri"] for t in thumbs if t.get("is_preferred")), thumbs[0]["uri"])
save_ids(videos=videos)

# 2. Campaign ---------------------------------------------------------------
if "campaign_id" not in ids:
    r = step("create campaign", lambda: post(f"{C.AD_ACCOUNT}/campaigns", name=C.CAMPAIGN_NAME,
             objective="OUTCOME_LEADS", status="PAUSED", special_ad_categories=[],
             buying_type="AUCTION", is_adset_budget_sharing_enabled=False))
    ids = save_ids(campaign_id=r["id"])

# 3. Ad set -----------------------------------------------------------------
if "adset_id" not in ids:
    r = step("create ad set", lambda: post(f"{C.AD_ACCOUNT}/adsets", name=C.ADSET_NAME,
             campaign_id=ids["campaign_id"], status="PAUSED", daily_budget=C.DAILY_BUDGET,
             billing_event="IMPRESSIONS", optimization_goal="OFFSITE_CONVERSIONS",
             bid_strategy="LOWEST_COST_WITHOUT_CAP", destination_type="WEBSITE",
             promoted_object=C.PROMOTED_OBJECT, attribution_spec=C.ATTRIBUTION_SPEC,
             start_time=C.START_TIME, targeting=C.targeting()))
    ids = save_ids(adset_id=r["id"])

# 4. Creatives + ads --------------------------------------------------------
FEED_POS = {"facebook_positions": ["feed", "profile_feed", "video_feeds"],
            "instagram_positions": ["stream", "explore", "explore_home", "profile_feed"]}
VERT_POS = {"facebook_positions": ["story", "facebook_reels"], "instagram_positions": ["story", "reels"]}


def asset_feed(c):
    vids, rules = [], []
    for slot, pos in (("feed", FEED_POS), ("vertical", VERT_POS)):
        if c.get(slot):
            v = videos[c[slot]]
            vids.append({"video_id": v["id"], "thumbnail_url": v["thumbnail_url"], "adlabels": [{"name": slot}]})
            rules.append({"customization_spec": {"publisher_platforms": ["facebook", "instagram"], **pos},
                          "video_label": {"name": slot}})
    spec = {"videos": vids,
            "bodies": [{"text": t} for _, _, t in PRIMARY],
            "titles": [{"text": t} for t in HEADLINES],
            "descriptions": [{"text": t} for t in DESCRIPTIONS],
            "link_urls": [{"website_url": C.LINK}],
            "call_to_action_types": [C.CTA],
            "ad_formats": ["SINGLE_VIDEO"],
            "optimization_type": "PLACEMENT"}
    if len(rules) > 1:
        spec["asset_customization_rules"] = [dict(r, priority=i + 1) for i, r in enumerate(rules)]
    else:
        spec.pop("optimization_type")
        warnings.append(f"C{c['n']}: only one aspect ratio; no placement customization")
    return spec


dof = {"creative_features_spec": {k: {"enroll_status": "OPT_OUT"} for k in C.CREATIVE_FEATURES_OPT_OUT}}
ads = ids.setdefault("ads", {})
for c in C.CONCEPTS:
    key = f"C{c['n']}"
    if key in ads and "ad_id" in ads[key]:
        continue
    name = C.AD_NAME.format(n=c["n"], angle=c["angle"])
    cr = step(f"creative {key}", lambda: post(f"{C.AD_ACCOUNT}/adcreatives", name=name,
              object_story_spec={"page_id": C.PAGE_ID, "instagram_user_id": C.INSTAGRAM_USER_ID},
              asset_feed_spec=asset_feed(c), url_tags=C.URL_TAGS, degrees_of_freedom_spec=dof))
    ads[key] = {"creative_id": cr["id"], "name": name}
    save_ids(ads=ads)
    ad = step(f"ad {key}", lambda: post(f"{C.AD_ACCOUNT}/ads", name=name, adset_id=ids["adset_id"],
              creative={"creative_id": cr["id"]}, status="PAUSED"))
    ads[key]["ad_id"] = ad["id"]
    save_ids(ads=ads)
    print("created", name, ad["id"])

# 5. Previews ---------------------------------------------------------------
parts = ["<!doctype html><meta charset=utf-8><title>Orchid previews</title>",
         "<style>body{font-family:system-ui;background:#fff;color:#111;margin:16px}"
         ".row{display:flex;flex-wrap:wrap;gap:16px}iframe{border:0}</style>",
         f"<h1>{html.escape(C.CAMPAIGN_NAME)}</h1>"]
for key, a in ads.items():
    parts.append(f"<h2>{html.escape(a['name'])}</h2><div class=row>")
    for fmt in ("MOBILE_FEED_STANDARD", "INSTAGRAM_STORY", "INSTAGRAM_REELS"):
        try:
            body = get(f"{a['ad_id']}/previews", ad_format=fmt)["data"][0]["body"]
        except (MetaError, IndexError, KeyError) as e:
            body = f"<p>{fmt}: {html.escape(str(e))}</p>"
            warnings.append(f"{key} preview {fmt}: {e}")
        parts.append(f"<div><h3>{fmt}</h3>{body}</div>")
    parts.append("</div>")
(BUILD / "previews.html").write_text("\n".join(parts))

# 6. Read back and verify ---------------------------------------------------
camp = get(ids["campaign_id"], fields="name,objective,status,special_ad_categories")
adset = get(ids["adset_id"], fields="name,status,daily_budget,bid_strategy,optimization_goal,promoted_object,"
                                    "start_time,end_time,targeting,attribution_spec,destination_type")
checks = {
    "campaign objective": camp["objective"] == "OUTCOME_LEADS",
    "campaign paused": camp["status"] == "PAUSED",
    "adset paused": adset["status"] == "PAUSED",
    "daily_budget 3289": str(adset["daily_budget"]) == str(C.DAILY_BUDGET),
    "bid strategy": adset.get("bid_strategy") == "LOWEST_COST_WITHOUT_CAP",
    "optimization": adset["optimization_goal"] == "OFFSITE_CONVERSIONS",
    "start 2026-10-01 00:00 ET": adset["start_time"].startswith("2026-10-01T00:00:00-0400"),
    "no end_time": not adset.get("end_time"),
    "advantage_audience 0": adset["targeting"].get("targeting_automation", {}).get("advantage_audience") == 0,
}
want = C.targeting()
for k in ("age_min", "age_max", "publisher_platforms", "facebook_positions", "instagram_positions", "device_platforms"):
    got = adset["targeting"].get(k)
    ok = sorted(got) == sorted(want[k]) if isinstance(want[k], list) and got else got == want[k]
    checks[f"targeting.{k}"] = ok
    if not ok:
        warnings.append(f"targeting.{k}: asked {want[k]}, API returned {got}")
for key, a in ads.items():
    ad = get(a["ad_id"], fields="status,creative{url_tags,degrees_of_freedom_spec,asset_feed_spec}")
    checks[f"{key} paused"] = ad["status"] == "PAUSED"
    checks[f"{key} url_tags"] = ad["creative"].get("url_tags") == C.URL_TAGS
    fs = ad["creative"].get("degrees_of_freedom_spec", {}).get("creative_features_spec", {})
    opted_in = [k for k, v in fs.items() if v.get("enroll_status") != "OPT_OUT"]
    checks[f"{key} creative opt-out"] = not opted_in
    if opted_in:
        warnings.append(f"{key}: features not opted out: {opted_in}")

acct = C.AD_ACCOUNT.replace("act_", "")
summary = {"ids": ids, "links": {
    "campaign": f"https://adsmanager.facebook.com/adsmanager/manage/campaigns?act={acct}&selected_campaign_ids={ids['campaign_id']}",
    "adset": f"https://adsmanager.facebook.com/adsmanager/manage/adsets?act={acct}&selected_adset_ids={ids['adset_id']}",
    "ads": {k: f"https://adsmanager.facebook.com/adsmanager/manage/ads?act={acct}&selected_ad_ids={a['ad_id']}"
            for k, a in ads.items()}},
    "targeting": adset["targeting"], "checks": checks, "warnings": warnings, "api_version": API_VERSION}
(BUILD / "build_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False))
print(json.dumps(summary, indent=2, ensure_ascii=False))
