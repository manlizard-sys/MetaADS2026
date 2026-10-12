"""Screenshot of each ad as people see it on Meta (mobile feed preview), for the owner reports.

Takes the ads that are active or that spent money in the last N days and saves
build/reports/previews/<today>/<ad name>.png. Read-only: uses Meta's ad preview endpoint.
Usage: python3 ad_previews.py [--days 14]
"""
import datetime as dt, json, re, subprocess, sys
from meta import get, get_all, BUILD, MetaError

ACT = "act_1806647434085082"
days = int(sys.argv[sys.argv.index("--days") + 1]) if "--days" in sys.argv else 14

spent = {r["ad_id"] for r in get_all(f"{ACT}/insights", level="ad", fields="ad_id,spend",
                                     time_range=json.dumps({"since": (dt.date.today() - dt.timedelta(days=days)).isoformat(),
                                                            "until": dt.date.today().isoformat()}))
         if float(r.get("spend", 0)) > 0}
ads = [a for a in get_all(f"{ACT}/ads", fields="id,name,status,creative{object_story_spec,asset_feed_spec}", limit=100)
       if a["status"] == "ACTIVE" or a["id"] in spent]


def poster(ad):
    """Cover frame of a video ad (headless Chromium cannot play Meta's video, so we show its cover)."""
    c = ad.get("creative") or {}
    vid = ((c.get("object_story_spec") or {}).get("video_data") or {}).get("video_id")
    vid = vid or next((v["video_id"] for v in (c.get("asset_feed_spec") or {}).get("videos", [])), None)
    if not vid:
        return None
    try:
        th = get(vid, fields="thumbnails{uri,is_preferred}").get("thumbnails", {}).get("data", [])
    except MetaError:
        return None
    pick = next((t for t in th if t.get("is_preferred")), th[0] if th else None)
    return pick and pick["uri"]

out = BUILD / "reports" / "previews" / dt.date.today().isoformat()
out.mkdir(parents=True, exist_ok=True)
jobs = []
for a in ads:
    try:
        body = get(f"{a['id']}/previews", ad_format="MOBILE_FEED_STANDARD")["data"][0]["body"]
    except (MetaError, IndexError, KeyError) as e:
        print(f"Sin vista previa para {a['name']}: {e}")
        continue
    url = re.search(r'src="([^"]+)"', body).group(1).replace("&amp;", "&")
    safe = re.sub(r"[^A-Za-z0-9]+", "-", a["name"]).strip("-")
    jobs.append({"url": url, "out": str(out / f"{safe}.png"), "ad": a["name"], "status": a["status"], "poster": poster(a)})

(out / "jobs.json").write_text(json.dumps(jobs, indent=2), encoding="utf-8")
subprocess.run(["node", str(BUILD.parent / "scripts" / "screenshot_previews.mjs"), str(out / "jobs.json")], check=False)
(out / "jobs.json").unlink()
(out / "index.json").write_text(json.dumps([{k: j[k] for k in ("ad", "status", "out")} for j in jobs], indent=2), encoding="utf-8")
print(f"Capturas en {out}")
