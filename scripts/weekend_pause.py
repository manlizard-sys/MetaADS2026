"""Weekend pause for the Orchid campaign: off Friday 4 pm, back on Monday 8 am (New York time).

--pause   pauses every ACTIVE ad set of the account and saves their ids in build/weekend-paused.json.
--resume  re-activates only the ad sets listed in that file (never ones the team paused by hand),
          then clears the file.
Prints a one-line summary per ad set. Default (no flag) shows what it would do.
Usage: python3 weekend_pause.py --pause | --resume
"""
import datetime as dt, json, sys
from meta import get_all, post, BUILD

ACT = "act_1806647434085082"
STATE = BUILD / "weekend-paused.json"
now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

if "--pause" in sys.argv:
    active = [a for a in get_all(f"{ACT}/adsets", fields="id,name,effective_status,daily_budget")
              if a["effective_status"] == "ACTIVE"]
    done = []
    for a in active:
        post(a["id"], status="PAUSED")
        done.append({"id": a["id"], "name": a["name"]})
        print(f"Pausado: {a['name']} (${int(a.get('daily_budget') or 0)/100:.2f}/día)")
    prev = json.loads(STATE.read_text()) if STATE.exists() else {"adsets": []}
    keep = {x["id"]: x for x in prev["adsets"] + done}  # a second pause run never loses the first list
    STATE.write_text(json.dumps({"paused_at": now, "adsets": list(keep.values())}, indent=2, ensure_ascii=False))
    print(f"{len(done)} conjunto(s) pausado(s) para el fin de semana. Estado en {STATE}")
elif "--resume" in sys.argv:
    if not STATE.exists():
        sys.exit("No hay pausa de fin de semana registrada; no se activa nada.")
    for a in json.loads(STATE.read_text())["adsets"]:
        post(a["id"], status="ACTIVE")
        print(f"Activado: {a['name']}")
    STATE.unlink()
    print("Fin de la pausa de fin de semana.")
else:
    for a in get_all(f"{ACT}/adsets", fields="id,name,effective_status"):
        if a["effective_status"] == "ACTIVE":
            print(f"Se pausaría: {a['name']}")
    print(f"Pausa registrada: {'sí' if STATE.exists() else 'no'}")
