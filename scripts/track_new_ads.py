"""Daily tracker of the 🟢 campaigns (Nov 16 launch): one row per ad per day from Meta (read-only).
Writes build/reports/tracker_ads.json as {rows, meta} for the "Orchid Ads Tracker" dashboard.
Usage: python3 track_new_ads.py [--since 2026-11-02]"""
import datetime as dt, json, os, sys
from pathlib import Path
from meta import get_all, BUILD

ACT = "act_1806647434085082"
SINCE = sys.argv[sys.argv.index("--since") + 1] if "--since" in sys.argv else "2026-11-02"
UNTIL = dt.date.today().isoformat()
FIELDS = ("campaign_name,adset_name,ad_name,ad_id,spend,impressions,reach,inline_link_clicks,actions,"
          "video_thruplay_watched_actions,video_p50_watched_actions")


def market(c):
    for k, v in (("Healthcare", "Salud"), ("Entrepreneurs", "Emprendedores"), ("IG Followers", "Seguidores IG"),
                 ("Awareness", "Awareness"), ("Retarget", "Retargeting")):
        if k in c:
            return v
    return "Otra"


def act(r, *keys):
    return sum(float(a["value"]) for a in r.get("actions") or [] if a["action_type"] in keys)


def first(r, k):
    v = r.get(k) or []
    return float(v[0]["value"]) if v else 0.0


rows = []
for r in get_all(f"{ACT}/insights", level="ad", time_increment=1, fields=FIELDS, limit=500,
                 time_range=json.dumps({"since": SINCE, "until": UNTIL})):
    if "🟢" not in r["campaign_name"]:
        continue
    rows.append({
        "date": r["date_start"], "market": market(r["campaign_name"]), "campaign": r["campaign_name"],
        "adset": r["adset_name"], "ad": r["ad_name"], "ad_id": r["ad_id"],
        "spend": round(float(r.get("spend", 0)), 2), "impressions": int(r.get("impressions", 0)),
        "reach": int(r.get("reach", 0)), "link_clicks": int(r.get("inline_link_clicks", 0)),
        "landing_views": int(act(r, "landing_page_view")),
        "leads": int(act(r, "offsite_conversion.fb_pixel_lead")),
        "qualified": int(act(r, "offsite_conversion.fb_pixel_complete_registration")),
        "schedules": int(act(r, "offsite_conversion.fb_pixel_schedule", "schedule_total")),
        "profile_visits": int(sum(float(a["value"]) for a in r.get("actions") or [] if "profile_visit" in a["action_type"])),
        "video_3s": int(act(r, "video_view")), "video_50": int(first(r, "video_p50_watched_actions")),
        "thruplay": int(first(r, "video_thruplay_watched_actions")),
    })
# GHL: real leads per ad and day (counts only, no personal data), matched by utm_content = ad name.
import glob, subprocess
for r in rows:
    r.update(ghl_leads=0, ghl_qualified=0, ghl_booked=0)
days = (dt.date.today() - dt.date.fromisoformat(SINCE)).days + 1
ghl_note = "GHL: contacts by utm_content (= ad name), excluding Mailchimp imports and test submissions."
try:
    subprocess.run([sys.executable, str(Path(__file__).with_name("ghl.py")), "--days", str(days)], check=True,
                   capture_output=True, text=True, timeout=300)
    contacts = json.load(open(sorted(glob.glob(str(BUILD / "reports" / "ghl-*.json")))[-1]))["contacts"]
    by_key = {(r["date"], r["ad"]): r for r in rows}
    info = {r["ad"]: r for r in rows}
    for c in contacts:
        if c["date"] < SINCE or c["ad"] not in info:
            continue
        r = by_key.get((c["date"], c["ad"]))
        if r is None:
            base = info[c["ad"]]
            r = {k: (0 if isinstance(v, (int, float)) else v) for k, v in base.items()}
            r["date"] = c["date"]; rows.append(r); by_key[(c["date"], c["ad"])] = r
        r["ghl_leads"] += 1
        r["ghl_qualified"] += int(bool(c.get("hiring_or_job")) and not c["job_seeker"])
        r["ghl_booked"] += int(bool(c.get("booked")))
except Exception as e:  # Meta numbers still publish if GHL is unreachable
    ghl_note = f"GHL not read this run: {str(e)[:200]}"
    print("GHL:", ghl_note)
# Followers snapshot (IG + FB page), one row per day: the API gives only the current total, so growth is
# measured from these daily snapshots (build/reports/followers.json).
try:
    from meta import get
    snap = {"date": dt.date.today().isoformat(),
            "ig": get("17841430599113385", fields="followers_count")["followers_count"],
            "fb": get("1132642053254708", fields="followers_count")["followers_count"]}
    fp = BUILD / "reports" / "followers.json"
    hist = [h for h in (json.loads(fp.read_text()) if fp.exists() else []) if h["date"] != snap["date"]]
    fp.write_text(json.dumps(sorted(hist + [snap], key=lambda h: h["date"]), indent=1))
except Exception as e:
    print("followers:", str(e)[:200])
if os.environ.get("META_INSIGHTS_TOKEN"):  # daily follower history (read-only insights token)
    subprocess.run([sys.executable, str(Path(__file__).with_name("followers.py"))], timeout=300)
rows.sort(key=lambda x: (x["date"], x["market"], x["ad"]))
code = Path(__file__).read_text()
out = BUILD / "reports" / "tracker_ads.json"
out.write_text(json.dumps({"rows": rows, "meta": [
    {"label": "track_new_ads.py", "value": code, "type": "code", "lang": "python"},
    {"label": "Source", "value": f"Meta Marketing API, ad account {ACT}, campaigns whose name contains 🟢, {SINCE} to {UNTIL}"},
    {"label": "GHL", "value": ghl_note},
    {"label": "Updated", "value": dt.datetime.now(dt.timezone.utc).isoformat(timespec="minutes")},
]}, ensure_ascii=False))
print(out, len(rows), "rows")
