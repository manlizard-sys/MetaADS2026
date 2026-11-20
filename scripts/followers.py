"""Daily follower history for Instagram (@orchidpros.staffing) and the Facebook page (Orchid Pros).
Uses META_INSIGHTS_TOKEN (read-only insights token, environment variable); the ads token is never used here.
Writes build/reports/followers_history.json: one row per day with IG followers gained/lost and FB follows.
Usage: python3 followers.py [--days 30]   (IG insights only go back 30 days)"""
import datetime as dt, json, os, re, sys, requests
from meta import BUILD, GRAPH, MetaError

IG, PAGE = "17841430599113385", "1132642053254708"
TOKEN = os.environ.get("META_INSIGHTS_TOKEN", "").strip()
DAYS = int(sys.argv[sys.argv.index("--days") + 1]) if "--days" in sys.argv else 30


def scrub(t):
    t = str(t)
    return t.replace(TOKEN, "***") if TOKEN else t


def get(path, token, **params):
    try:
        r = requests.get(f"{GRAPH}/{path}", headers={"Authorization": f"Bearer {token}"}, params=params, timeout=60)
        d = r.json()
    except Exception as e:
        raise MetaError(scrub(f"{type(e).__name__}: {e}")) from None
    if "error" in d:
        raise MetaError(scrub(d["error"].get("message")))
    return d


def main():
    if not TOKEN:
        sys.exit("META_INSIGHTS_TOKEN missing")
    until = dt.date.today()
    since = until - dt.timedelta(days=min(DAYS, 30) - 1)
    rng = dict(since=since.isoformat(), until=(until + dt.timedelta(days=1)).isoformat())
    days, notes = {}, []
    row = lambda d: days.setdefault(d, {"date": d})

    # Instagram: new followers per day (follower_count) and gained/lost (follows_and_unfollows)
    try:
        for v in get(f"{IG}/insights", TOKEN, metric="follower_count", period="day", **rng)["data"][0]["values"]:
            row(v["end_time"][:10])["ig_new_followers"] = v["value"]
    except MetaError as e:
        notes.append(f"IG follower_count: {e}")
    try:
        for d in (since + dt.timedelta(days=i) for i in range((until - since).days + 1)):
            r = get(f"{IG}/insights", TOKEN, metric="follows_and_unfollows", period="day", metric_type="total_value",
                    breakdown="follow_type", since=d.isoformat(), until=(d + dt.timedelta(days=1)).isoformat())["data"]
            res = r[0]["total_value"].get("breakdowns", [{}])[0].get("results", []) if r else []
            for x in res:
                k = {"FOLLOWER": "ig_follows", "NON_FOLLOWER": "ig_follows", "UNFOLLOW": "ig_unfollows"}.get(x["dimension_values"][0])
                if k:
                    row(d.isoformat())[k] = row(d.isoformat()).get(k, 0) + x["value"]
    except MetaError as e:
        notes.append(f"IG follows_and_unfollows: {e}")

    # Facebook page: needs a Page token derived from the insights token
    try:
        ptoken = get(PAGE, TOKEN, fields="access_token")["access_token"]
        for m in get(f"{PAGE}/insights", ptoken, metric="page_daily_follows_unique,page_daily_unfollows_unique,page_follows",
                     period="day", **rng)["data"]:
            for v in m["values"]:
                row(v["end_time"][:10])[{"page_daily_follows_unique": "fb_follows", "page_daily_unfollows_unique": "fb_unfollows",
                                          "page_follows": "fb_total"}[m["name"]]] = v["value"]
    except MetaError as e:
        notes.append(f"FB page insights: {e}")

    totals = {"ig_total_now": get(IG, TOKEN, fields="followers_count")["followers_count"]}
    out = BUILD / "reports" / "followers_history.json"
    out.write_text(json.dumps({"updated": dt.datetime.now(dt.timezone.utc).isoformat(timespec="minutes"), **totals,
                               "days": sorted(days.values(), key=lambda r: r["date"]), "notes": notes}, indent=1))
    print(out, len(days), "days", "| notes:", notes or "none")


if __name__ == "__main__":
    main()
