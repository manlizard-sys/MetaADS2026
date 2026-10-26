"""A/B/C conversion-path test (plan: build/prueba_ABC_noviembre.md).

Three ad sets in the same campaign with the same ads (S9, H3, H5), audience and budget; only the
destination changes:
  A  go.orchidpros.com/hire-form   (form-only landing)
  B  go.orchidpros.com/hire        (full landing)
  C  Meta Instant Form 2620655611681341 (Higher intent)
Audience: NY, NJ, PA, 30-65, interests Law firm / Lawyer / Bar association, Advantage+ audience off.
$15/day each. A Meta split test (ad study) keeps the three audiences apart. The hyperlocal ad set is
paused so the account stays at $45/day. Ad names carry "TEST A/B/C" so GHL (utm_content) attributes leads.
Default is a dry run; --apply creates everything; --activate also turns it on.
"""
import copy, datetime as dt, json, sys
from meta import get, post, BUILD, MetaError

ACT = "act_1806647434085082"
CAMPAIGN = "120257040908660196"
BUSINESS = "1534891157898770"
PAGE = "1132642053254708"
PIXEL = "2271987886986577"
FORM = "2620655611681341"
HYPERLOCAL = "120257317011450196"
SOURCE_ADS = {"S9 Attorneys In-Person Cost": "120257317011800196",
              "🔵 H3 Saturdays Back": "120257358437290196",
              "🔵 H5 Phones While In Court": "120257358437640196"}
BUDGET = 1500  # cents/day per variant
END = dt.datetime(2026, 11, 21, 23, 0, tzinfo=dt.timezone(dt.timedelta(hours=-5)))
TARGETING = {
    "geo_locations": {"regions": [{"key": "3875"}, {"key": "3873"}, {"key": "3881"}], "location_types": ["home", "recent"]},
    "age_min": 30, "age_max": 65,
    "flexible_spec": [{"interests": [{"id": "6003057724244", "name": "Law firm"}, {"id": "6003392101554", "name": "Lawyer"},
                                     {"id": "6003029225585", "name": "Bar association"}]}],
    "excluded_custom_audiences": [{"id": "120257005715340196"}],
    "publisher_platforms": ["facebook", "instagram"],
    "targeting_automation": {"advantage_audience": 0},
}
VARIANTS = {
    "A": {"label": "Landing solo formulario", "link": "https://go.orchidpros.com/hire-form"},
    "B": {"label": "Landing completa", "link": "https://go.orchidpros.com/hire"},
    "C": {"label": "Formulario instantáneo", "form": FORM},
}
apply, activate = "--apply" in sys.argv, "--activate" in sys.argv

reach = get(f"{ACT}/reachestimate", targeting_spec=json.dumps(TARGETING))["data"]
print(f"Público NY/NJ/PA abogados 30-65: {reach.get('users_lower_bound'):,}–{reach.get('users_upper_bound'):,}")
for k, v in VARIANTS.items():
    print(f"  {k} · {v['label']} · ${BUDGET/100:.0f}/día · {v.get('link') or 'form ' + v['form']}")
print(f"  Anuncios en cada uno: {', '.join(SOURCE_ADS)} · hasta {END:%Y-%m-%d}")
if not apply:
    sys.exit("\nVista previa. Nada cambió. Ejecuta con --apply (pausado) o --apply --activate.")

src = get(HYPERLOCAL, fields="attribution_spec")
creatives = {n: get(get(a, fields="creative{id}")["creative"]["id"],
                    fields="name,object_story_spec,asset_feed_spec,degrees_of_freedom_spec,url_tags")
             for n, a in SOURCE_ADS.items()}


def clone(cr, variant):
    oss = copy.deepcopy(cr["object_story_spec"])
    ld = oss["link_data"]
    for k in ("image_url", "picture"):
        ld.pop(k, None)
    if "form" in variant:
        ld["link"] = "http://fb.me/"
        # BOOK_NOW does not accept lead_gen_form_id; SIGN_UP ("Sign up") does.
        ld["call_to_action"] = {"type": "SIGN_UP", "value": {"lead_gen_form_id": variant["form"]}}
    else:
        ld["link"] = variant["link"]
        ld["call_to_action"] = {"type": "BOOK_TRAVEL", "value": {"link": variant["link"], "link_caption": "orchidpros.com"}}
    afs = cr.get("asset_feed_spec") or {}
    feed = {"bodies": [{"text": b["text"]} for b in afs.get("bodies", [])],
            "titles": [{"text": t["text"]} for t in afs.get("titles", [])],
            "descriptions": [{"text": d["text"]} for d in afs.get("descriptions", [])],
            "optimization_type": "DEGREES_OF_FREEDOM"}
    if afs.get("images"):
        feed["images"] = [{"hash": i["hash"]} for i in afs["images"]]
    dof = {"creative_features_spec": {k: {"enroll_status": "OPT_OUT"}
           for k in (cr.get("degrees_of_freedom_spec") or {}).get("creative_features_spec", {})
           if k not in ("standard_enhancements", "advantage_plus_creative")}}
    return dict(object_story_spec=oss, asset_feed_spec=feed, degrees_of_freedom_spec=dof, url_tags=cr.get("url_tags", ""))


out = {"created_at": dt.datetime.now(dt.timezone.utc).isoformat(), "adsets": {}}
status = "ACTIVE" if activate else "PAUSED"
for key, v in VARIANTS.items():
    is_form = "form" in v
    aset = post(f"{ACT}/adsets", name=f"TEST {key} · {v['label']} · NY-NJ-PA abogados 30-65 · 2026 Oct-Nov",
                campaign_id=CAMPAIGN, daily_budget=BUDGET, end_time=END.isoformat(), status="PAUSED",
                billing_event="IMPRESSIONS", bid_strategy="LOWEST_COST_WITHOUT_CAP", targeting=TARGETING,
                optimization_goal="LEAD_GENERATION" if is_form else "OFFSITE_CONVERSIONS",
                destination_type="ON_AD" if is_form else "WEBSITE",
                promoted_object={"page_id": PAGE} if is_form else {"pixel_id": PIXEL, "custom_event_type": "LEAD"},
                **({} if is_form else {"attribution_spec": src["attribution_spec"]}))  # view/video attribution is invalid for ON_AD
    ads = []
    for name, cr in creatives.items():
        spec = clone(cr, v)
        c = post(f"{ACT}/adcreatives", name=f"test {key} · {name}", **spec)
        ad = post(f"{ACT}/ads", name=f"TEST {key} · {name}", adset_id=aset["id"], creative={"creative_id": c["id"]}, status="ACTIVE")
        ads.append({"name": name, "ad_id": ad["id"], "creative_id": c["id"]})
    out["adsets"][key] = {"adset_id": aset["id"], "label": v["label"], "ads": ads}
    print(f"Creado TEST {key} · {v['label']}: ad set {aset['id']} · {len(ads)} anuncios")

# Split test so each person sees only one variant.
try:
    start = dt.datetime.now(dt.timezone.utc) + dt.timedelta(minutes=10)
    study = post(f"{BUSINESS}/ad_studies", name="Orchid · Prueba A/B/C destino · Oct-Nov 2026", type="SPLIT_TEST",
                 description="A landing solo formulario · B landing completa · C formulario instantáneo",
                 start_time=int(start.timestamp()), end_time=int(END.timestamp()),
                 cells=json.dumps([{"name": f"{k} · {VARIANTS[k]['label']}", "treatment_percentage": p,
                                    "adsets": [out["adsets"][k]["adset_id"]]} for k, p in zip("ABC", (33, 33, 34))]))
    out["ad_study_id"] = study["id"]
    print(f"Prueba A/B de Meta creada: {study['id']} (públicos separados)")
except MetaError as e:
    out["ad_study_error"] = str(e)[:300]
    print(f"AVISO: no se pudo crear la prueba A/B de Meta; los 3 conjuntos corren sin separación de público.\n{str(e)[:300]}")

if activate:
    post(HYPERLOCAL, status="PAUSED")
    for k in "ABC":
        post(out["adsets"][k]["adset_id"], status="ACTIVE")
    print("Prueba activada; HYPERLOCAL pausado.")
(BUILD / "abc-test.json").write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
