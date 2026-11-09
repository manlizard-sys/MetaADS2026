"""Nov 9 day-7 change (approved by the user): leads ad set to Facebook feed only and Advantage+ audience.
Legal interests/behaviors and web visitors become suggestions; ages 30-65 suggested (hard floor 25, Meta's max
with Advantage+). Exclusion of past leads stays hard. --apply writes; default validates only."""
import sys, time
from meta import get, post, MetaError

ADSET = "120257589638070196"
T = {"geo_locations": {"countries": ["US"], "location_types": ["home", "recent"]},
     "age_min": 25, "age_max": 65, "age_range": [30, 65],
     "excluded_custom_audiences": [{"id": "120257005715340196"}],
     "custom_audiences": [{"id": "120257579616750196"}],
     "flexible_spec": [{"interests": [{"id": "6003029225585"}, {"id": "6003057724244"}, {"id": "6003392101554"}],
                        "behaviors": [{"id": "6002714898572"}, {"id": "6020530281783"}]}],
     "targeting_automation": {"advantage_audience": 1},
     "publisher_platforms": ["facebook"], "facebook_positions": ["feed"], "device_platforms": ["mobile", "desktop"]}


def call(**kw):
    for _ in range(8):
        try:
            return post(ADSET, targeting=T, **kw)
        except MetaError as e:
            if "613" in str(e) or "2446079" in str(e) or '"code": 17' in str(e):
                time.sleep(40); continue
            raise


print("validate:", call(execution_options=["validate_only"]))
if "--apply" in sys.argv:
    time.sleep(35)
    print("apply:", call())
    time.sleep(35)
    t = get(ADSET, fields="targeting")["targeting"]
    print({k: t.get(k) for k in ("age_min", "age_max", "age_range", "publisher_platforms", "facebook_positions",
                                 "targeting_automation", "custom_audiences")})
