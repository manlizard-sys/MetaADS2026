"""Nov 15 (user order): healthcare leads get their own campaign (law stays paused for a while);
green dot 🟢 on campaigns that run from Nov 16. Everything new stays PAUSED until the launch."""
import json, time
from meta import get, post, BUILD, MetaError

ACT = "act_1806647434085082"
STATE = BUILD / "nov2026.json"
st = json.loads(STATE.read_text()); b = st["build"]; s = b["bf16"]
save = lambda: STATE.write_text(json.dumps(st, indent=2, ensure_ascii=False))


def retry(fn, *a, **k):
    for _ in range(8):
        try:
            return fn(*a, **k)
        except MetaError as e:
            if any(c in str(e) for c in ('"code": 17', "(#613)", "2446079", "80004")):
                time.sleep(45); continue
            raise


OLD = b["bf_health"]["adset"]
if "hc_campaign" not in s:
    s["hc_campaign"] = retry(post, f"{ACT}/campaigns", name="🟢 Orchid · Healthcare · BF · Nov 2026", objective="OUTCOME_LEADS",
                             status="PAUSED", special_ad_categories=[], is_adset_budget_sharing_enabled="false")["id"]; save()
if "hc_adset" not in s:
    src = get(OLD, fields="targeting,attribution_spec,adset_schedule,promoted_object,start_time,end_time")
    t = src["targeting"]
    for k in ("targeting_relaxation_types",):
        t.pop(k, None)
    s["hc_adset"] = retry(post, f"{ACT}/adsets", name="BF · Healthcare · Get started free · 6am-10pm · Nov26", campaign_id=s["hc_campaign"],
                          status="PAUSED", lifetime_budget=16500, start_time=src["start_time"], end_time=src["end_time"],
                          pacing_type=["day_parting"], adset_schedule=src["adset_schedule"], billing_event="IMPRESSIONS",
                          bid_strategy="LOWEST_COST_WITHOUT_CAP", optimization_goal="OFFSITE_CONVERSIONS", destination_type="WEBSITE",
                          promoted_object={"pixel_id": src["promoted_object"]["pixel_id"], "custom_event_type": "LEAD"},
                          attribution_spec=src["attribution_spec"], targeting=t)["id"]; save()
    print("hc adset", s["hc_adset"])
retry(post, OLD, name="[NO USAR · movido a campaña Healthcare] BF · Healthcare · Nov26", status="PAUSED")
b["bf_health"]["status"] = "NO USAR: reemplazado por bf16.hc_adset en su propia campaña (15 nov)"
retry(post, s["ent_campaign"], name="🟢 Orchid · Entrepreneurs · BF · Nov 2026")
retry(post, s["ent_adset"], lifetime_budget=16500)
retry(post, b["aw_campaign"], name="🟢 Orchid · Awareness · Video POV · Nov 2026")
retry(post, b["engagement"]["campaign"], name="🟢 Orchid · IG Followers · Nov 2026")
save()
for i in (s["hc_campaign"], s["hc_adset"], s["ent_campaign"], s["ent_adset"], b["aw_campaign"], b["engagement"]["campaign"], b["lead_campaign"], OLD):
    r = get(i, fields="name,effective_status"); print(r["effective_status"], "·", r["name"])
