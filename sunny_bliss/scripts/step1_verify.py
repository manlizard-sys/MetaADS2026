"""Step 1: read-only verification of the Sunny Bliss token, account, pixel and page.

Run without IDs to see what the token can reach; with IDs configured it checks the account
(status, payment, spend cap, timezone, currency), the pixel and its events, and the page.
Writes build/step1_raw.json.
"""
import json, sys, time
import config as C
from meta import get, get_all, MetaError, TOKEN, API_VERSION, BUILD

out = {}
NEEDED = {"ads_management", "ads_read", "business_management", "pages_read_engagement", "pages_manage_ads"}


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
try:
    dbg = get("debug_token", input_token=TOKEN)["data"]
except MetaError as e:
    sys.exit(f"Token inválido:\n{e}")
show("debug_token", {k: dbg.get(k) for k in ("application", "type", "is_valid", "expires_at", "scopes", "user_id")})
if dbg.get("type") != "SYSTEM_USER":
    print("AVISO: el token no es de un usuario del sistema; se cae al cambiar la contraseña.")
if missing := NEEDED - set(dbg.get("scopes", [])):
    print(f"AVISO: faltan permisos {sorted(missing)} (leads_retrieval también si hay formularios instantáneos).")
safe("me", lambda: get("me", fields="id,name"))
safe("ad_accounts", lambda: get_all("me/adaccounts",
     fields="id,name,currency,timezone_name,account_status,business{id,name}", limit=100))
safe("pages", lambda: get_all("me/accounts", fields="id,name,category,instagram_business_account{id,username}", limit=100))
safe("businesses", lambda: get_all("me/businesses", fields="id,name", limit=100))

if not C.AD_ACCOUNT:
    print("\nFalta SUNNY_AD_ACCOUNT: elige la cuenta de la lista de arriba y configúrala.")
else:
    C.require("AD_ACCOUNT")
    acc = get(C.AD_ACCOUNT, fields="name,currency,timezone_name,account_status,disable_reason,spend_cap,"
              "amount_spent,balance,funding_source_details,is_prepay_account,min_daily_budget,business{id,name}")
    show("account", acc)
    status = {1: "ACTIVA", 2: "DESACTIVADA", 3: "PAGO PENDIENTE", 7: "EN REVISIÓN", 9: "EN PERIODO DE GRACIA",
              100: "CIERRE PENDIENTE", 101: "CERRADA"}.get(acc.get("account_status"), acc.get("account_status"))
    print(f"\nEstado: {status} · {acc.get('currency')} · {acc.get('timezone_name')} · "
          f"límite de gasto: {acc.get('spend_cap') or 'sin límite'}")
    safe("account_pixels", lambda: get_all(f"{C.AD_ACCOUNT}/adspixels", fields="id,name,last_fired_time,is_unavailable"))
    safe("account_instagram", lambda: get_all(f"{C.AD_ACCOUNT}/instagram_accounts", fields="id,username"))
    safe("campaigns", lambda: get_all(f"{C.AD_ACCOUNT}/campaigns",
         fields="id,name,objective,status,effective_status,created_time", limit=200))
    print("NOTA: los borradores de Ads Manager no salen por API; revisar la pestaña Borradores a mano.")

if C.PIXEL_ID:
    now = int(time.time())
    safe("pixel", lambda: get(C.PIXEL_ID, fields="id,name,last_fired_time,is_unavailable,owner_business{id,name}"))
    safe("pixel_event_stats_7d", lambda: get_all(f"{C.PIXEL_ID}/stats", aggregation="event",
         start_time=now - 7 * 86400, end_time=now))
if C.BUSINESS_ID:
    safe("owned_domains", lambda: get_all(f"{C.BUSINESS_ID}/owned_domains", fields="id,domain_name,verification_status"))
if C.PAGE_ID:
    safe("page", lambda: get(C.PAGE_ID, fields="id,name,category,category_list{id,name},link,website,about,"
                             "verification_status,instagram_business_account{id,username}"))

BUILD.mkdir(exist_ok=True)
(BUILD / "step1_raw.json").write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
