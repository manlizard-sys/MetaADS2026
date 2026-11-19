"""Nov 19 (user order): Advantage+ audience OFF on the new LPV ad sets, fixed audiences, and budget up to $20/day each
(monthly budget raised to $1,300). Usage: python3 upd_audience_nov19.py [--validate]"""
import json, sys
from meta import get, post, BUILD

ACT = "act_1806647434085082"
st = json.loads((BUILD / "nov2026.json").read_text()); s = st["build"]["lpv19"]
EXTRA = {"execution_options": ["validate_only"]} if "--validate" in sys.argv else {}
OWNERS = [{"id": "6002714898572", "name": "Small business owners"}, {"id": "6020530281783", "name": "Business page admins"}]
WP = ["108768179146852", "109487152410372", "148866958458716", "149072445110317", "1569299249954237", "1595394480678734", "911356208895948"]
base = {"geo_locations": {"countries": ["US"], "location_types": ["home", "recent"]}, "age_min": 30, "age_max": 65,
        "excluded_custom_audiences": [{"id": "120257005715340196"}], "targeting_automation": {"advantage_audience": 0}}
T = {"hc": dict(base, flexible_spec=[{"industries": [{"id": "6012903159383", "name": "Healthcare and Medical Services"}]},
                                     {"behaviors": OWNERS, "work_positions": [{"id": i} for i in WP]}]),
     "ent": dict(base, flexible_spec=[{"behaviors": OWNERS}])}
for k, t in T.items():
    e = get(f"{ACT}/delivery_estimate", optimization_goal="LANDING_PAGE_VIEWS", targeting_spec=json.dumps(t))["data"][0]
    print(k, "audience", e["estimate_mau_lower_bound"], e["estimate_mau_upper_bound"])
    print(k, post(s[f"{k}_adset"], targeting=t, daily_budget=2000, **EXTRA))
