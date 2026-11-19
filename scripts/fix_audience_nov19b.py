"""Nov 19 (user order "Si"): clean the audiences Manuel widened.
- Healthcare: drop SBO behavior / SME interest from the healthcare group (they made it 'any business owner').
- Entrepreneurs: drop interests Insurance, Business, Small business, Entrepreneurship."""
import json
from meta import get, post
HC, ENT = "120257891824390196", "120257891833940196"
DROP = {"Insurance", "Business", "Small business", "Entrepreneurship"}
def size(t):
    e = get("act_1806647434085082/delivery_estimate", optimization_goal="LANDING_PAGE_VIEWS", targeting_spec=json.dumps(t))["data"][0]
    return e["estimate_mau_lower_bound"], e["estimate_mau_upper_bound"]
t = get(HC, fields="targeting")["targeting"]; g = t["flexible_spec"][0]; g.pop("interests", None); g.pop("behaviors", None)
print("hc", size(t), post(HC, targeting=t))
t = get(ENT, fields="targeting")["targeting"]; g = t["flexible_spec"][0]; g["interests"] = [i for i in g["interests"] if i["name"] not in DROP]
print("ent", size(t), post(ENT, targeting=t))
