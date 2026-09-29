"""Step 1: read-only verification."""
import json, datetime
from meta import get, get_all, MetaError, TOKEN, API_VERSION

out = {}
def show(title, obj):
    print(f"\n=== {title} ===")
    print(json.dumps(obj, indent=2, ensure_ascii=False))
    out[title] = obj

def safe(title, fn):
    try:
        show(title, fn())
    except MetaError as e:
        show(title, {"ERROR": str(e)})

print("API version:", API_VERSION)
safe("debug_token", lambda: {k: v for k, v in get("debug_token", input_token=TOKEN)["data"].items()
                             if k in ("app_id", "application", "type", "is_valid", "expires_at",
                                      "data_access_expires_at", "scopes", "user_id")})
safe("me", lambda: get("me", fields="id,name"))
safe("permissions", lambda: get_all("me/permissions"))
safe("ad_accounts", lambda: get_all("me/adaccounts",
     fields="id,account_id,name,currency,timezone_name,account_status,business{id,name}", limit=100))
safe("pages", lambda: get_all("me/accounts", fields="id,name,instagram_business_account{id,username}", limit=100))
safe("businesses", lambda: get_all("me/businesses", fields="id,name", limit=100))

# --- Account-level checks: run with ORCHID_AD_ACCOUNT=act_XXX once the user confirms IDs ---
import os, sys, time
ACT = os.environ.get("ORCHID_AD_ACCOUNT", "act_1806647434085082")  # OrchidPros
PIXEL = os.environ.get("ORCHID_PIXEL", "2271987886986577")
if ACT:
    acc = get(ACT, fields="name,currency,timezone_name,account_status,disable_reason")
    show("account", acc)
    if acc.get("currency") != "USD" or acc.get("timezone_name") != "America/New_York" or acc.get("account_status") != 1:
        print("\nSTOP: account is not USD / America/New_York / ACTIVE(1).")
        sys.exit(2)
    safe("similar_campaigns", lambda: [c for c in get_all(f"{ACT}/campaigns",
         fields="id,name,status,effective_status,created_time", limit=200)
         if "orchid" in c["name"].lower() or "hire a va" in c["name"].lower()])
    print("NOTE: Ads Manager drafts are not exposed by the API; check the Drafts tab manually.")
    safe("account_pixels", lambda: get_all(f"{ACT}/adspixels", fields="id,name,last_fired_time"))
    safe("account_instagram", lambda: get_all(f"{ACT}/instagram_accounts", fields="id,username"))
    safe("pixel", lambda: get(PIXEL, fields="id,name,last_fired_time,is_unavailable"))
    now = int(time.time())
    safe("pixel_event_stats_7d", lambda: get_all(f"{PIXEL}/stats", aggregation="event",
         start_time=now - 7 * 86400, end_time=now))
    safe("locale_english", lambda: get("search", type="adlocale", q="English")["data"])

json.dump(out, open("../build/step1_raw.json", "w"), indent=2, ensure_ascii=False)
