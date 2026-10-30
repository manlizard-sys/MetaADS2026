"""Pause every ACTIVE campaign of the Sunny Bliss account (writes to Meta: only on the owner's order).

Saves build/backup-<today>-before-pause-all.json first, with each campaign's id, name, status and
budget, so they can be turned back on exactly as they were. Then pauses at campaign level and
reads the status back. Default (no flag) only lists what it would pause.
Usage: python3 pause_all.py [--apply]
"""
import datetime as dt, json, sys
import config as C
from meta import get, get_all, post, BUILD

C.require("AD_ACCOUNT")
active = [c for c in get_all(f"{C.AD_ACCOUNT}/campaigns", limit=200,
                             fields="id,name,status,effective_status,objective,daily_budget,lifetime_budget")
          if c["status"] == "ACTIVE"]
if "--apply" not in sys.argv:
    for c in active:
        print(f"Se pausaría: {c['name']} ({c['id']})")
    sys.exit(0)

backup = BUILD / f"backup-{dt.date.today()}-before-pause-all.json"
backup.write_text(json.dumps({"account": C.AD_ACCOUNT, "saved_at": dt.datetime.now(dt.timezone.utc).isoformat(),
                              "campaigns": active}, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"Respaldo: {backup}")
for c in active:
    post(c["id"], status="PAUSED")
    now = get(c["id"], fields="status,effective_status")
    print(f"Pausada: {c['name']} → {now['status']} / {now['effective_status']}")
