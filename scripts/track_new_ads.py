"""Daily tracker of the 🟢 campaigns (Nov 16 launch): one row per ad per day from Meta (read-only).
Writes build/reports/tracker_ads.json as {rows, meta} for the "Orchid Ads Tracker" dashboard.
Usage: python3 track_new_ads.py [--since 2026-11-02]"""
import datetime as dt, json, sys
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
rows.sort(key=lambda x: (x["date"], x["market"], x["ad"]))
code = Path(__file__).read_text()
out = BUILD / "reports" / "tracker_ads.json"
out.write_text(json.dumps({"rows": rows, "meta": [
    {"label": "track_new_ads.py", "value": code, "type": "code", "lang": "python"},
    {"label": "Source", "value": f"Meta Marketing API, ad account {ACT}, campaigns whose name contains 🟢, {SINCE} to {UNTIL}"},
    {"label": "Updated", "value": dt.datetime.now(dt.timezone.utc).isoformat(timespec="minutes")},
]}, ensure_ascii=False))
print(out, len(rows), "rows")
