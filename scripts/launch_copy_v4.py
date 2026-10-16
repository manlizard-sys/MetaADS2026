"""Create the two attorney static ads (copy v4, build/copy_v4.md) with Debi's creatives of 2026-10-15.

Each ad = one creative with its 3 images as variations (Flexible format), one primary text,
3 headlines, 1 description, CTA Book Now, same landing and UTMs as the live ads.
Ads are created PAUSED; activate them after review. Default is a dry run.

--hyperlocal also creates the immigration-court pilot ad set (PAUSED) with the same two ads:
1-mile pins at 26 Federal Plaza (USCIS NYC + Federal Plaza/Broadway/Varick courts) and 970 Broad St
Newark (USCIS + Newark court), 30 N 41st St (USCIS Philadelphia) and 900 Market St (Philadelphia
court), people living in or recently there, 25-65, interests Law firm / Lawyer / Bar association
(Meta retired the AILA interest), $10/day for 20 days ($200). The national ad set drops to $28.89/day so the account
stays at the $38.89/day cap.
Usage: python3 launch_copy_v4.py [--adset <ad set id>] [--hyperlocal] [--apply]
"""
import base64, datetime, json, re, sys
from meta import get, post, ROOT, BUILD, MetaError

ACT = "act_1806647434085082"
PAGE, IG = "1132642053254708", "17841473464921031"
LINK = "https://go.orchidpros.com/hire"
URL_TAGS = ("utm_source={{site_source_name}}&utm_medium=paid_social&utm_campaign={{campaign.name}}"
            "&utm_term={{adset.name}}&utm_content={{ad.name}}&utm_id={{campaign.id}}&placement={{placement}}")
ADSET = sys.argv[sys.argv.index("--adset") + 1] if "--adset" in sys.argv else "120257040908680196"
IMG = ROOT / "creatives" / "2026-10-15"
DESC = "For U.S. law firms · English & Spanish"

ADS = {
    "S9 Attorneys In-Person Cost - Static - 2026 Oct": {
        "images": ["for_the_attorneys_1.png", "for_the_attorneys_2.png", "for_the_attorneys_3.png"],
        "body": (
            "Attorneys: is in-person staff costing more than your caseload can carry? ⚖️\n\n"
            "Orchid places a dedicated bilingual legal assistant on your team, during your business hours. "
            "They handle intake, scheduling, client follow-ups, and document collection in English and Spanish.\n\n"
            "No extra desk. No full-time salary for a part-time workload. Your firm pays from $15/hr.\n\n"
            "You spend the first weeks showing them how your firm works. After that, your evenings and Saturdays are yours again.\n\n"
            "Assistants are based in Colombia and screened by Orchid's HR team for U.S. legal experience.\n\n"
            "Book a free call to see if it's a fit for your firm 🤝"),
        "titles": ["Legal support without the in-person cost", "Bilingual legal support from $15/hr", "Train your assistant once"],
    },
    "S10 Interns Turnover - Static - 2026 Oct": {
        "images": ["still_depending_on_interns_1.png", "still_depending_on_interns_2.png", "still_depending_on_interns_3.png"],
        "body": (
            "Law firm owners: how many of these sound like your office? 🙋🏼‍♀️\n\n"
            "👉 You've trained someone on your case management system three times this year.\n"
            "👉 You double-check every document before it goes out, just in case.\n"
            "👉 Someone left, and you found client files half done.\n"
            "👉 Intake calls hit voicemail whenever your assistant is out.\n"
            "👉 You keep telling yourself the next hire will be easier.\n\n"
            "Two or more? The problem isn't the people. It's the turnover.\n\n"
            "Orchid places a dedicated bilingual legal assistant on your team, during your business hours. "
            "They handle intake, scheduling, document collection, and client follow-ups in English and Spanish.\n\n"
            "You train them once. Same person, every week, so what they learn about your firm stays at your firm.\n\n"
            "Your firm pays from $15/hr. Assistants are based in Colombia and screened by Orchid's HR team for U.S. legal experience.\n\n"
            "Book a free call to see if it's a fit for your firm ⚖️"),
        "titles": ["Train your assistant once", "Interns leave. Your assistant stays.", "Bilingual legal support from $15/hr"],
    },
}
# Same enhancement opt-outs as the live creatives (no AI rewrites of the approved copy or images).
OPT_OUT = ["text_optimizations", "image_touchups", "image_templates", "image_uncrop", "image_animation",
           "enhance_cta", "description_automation", "add_text_overlay", "adapt_to_placement"]

apply = "--apply" in sys.argv
hyper = "--hyperlocal" in sys.argv
CAP, HYPER_BUDGET = 3889, 1000  # cents/day: account cap and pilot budget
PINS = [("26 Federal Plaza, New York, NY 10278", 40.7154682, -74.0042025),
        ("970 Broad St, Newark, NJ 07102", 40.7300970, -74.1741915),
        ("30 N 41st St, Philadelphia, PA 19104 (USCIS)", 39.9585393, -75.2054757),
        ("900 Market St, Philadelphia, PA 19107 (immigration court)", 39.9516, -75.1554)]
HYPER_TARGETING = {
    "geo_locations": {"custom_locations": [{"latitude": la, "longitude": lo, "radius": 1, "distance_unit": "mile"}
                                           for _, la, lo in PINS], "location_types": ["home", "recent"]},
    "age_min": 25, "age_max": 65,
    "flexible_spec": [{"interests": [{"id": "6003057724244", "name": "Law firm"}, {"id": "6003392101554", "name": "Lawyer"},
                                     {"id": "6003029225585", "name": "Bar association"}]}],
    "publisher_platforms": ["facebook", "instagram"],
    "targeting_automation": {"advantage_audience": 0},
}
aset = get(ADSET, fields="name,effective_status")
print(f"Conjunto de anuncios: {aset['name']} ({aset['effective_status']})")
for name, a in ADS.items():
    for f in a["images"]:
        assert (IMG / f).exists(), f"Falta {IMG / f}"
    assert all(len(t) <= 40 for t in a["titles"]), [t for t in a["titles"] if len(t) > 40]
    print(f"\n{name}  ·  {len(a['images'])} imágenes  ·  estado PAUSED")
    print("  ", a["body"].splitlines()[0])
    print("   Titulares:", " | ".join(a["titles"]))
if hyper:
    print(f"\nPiloto hiperlocal (PAUSADO): $" + f"{HYPER_BUDGET/100:.2f}/día x 20 días; conjunto nacional pasa a ${(CAP-HYPER_BUDGET)/100:.2f}/día")
    for n, la, lo in PINS:
        print(f"   1 mi alrededor de {n} ({la}, {lo})")
if not apply:
    print("\nVista previa. Nada cambió. Ejecuta con --apply para crear los anuncios (quedan pausados).")
    sys.exit(0)

created = []
for name, a in ADS.items():
    hashes = []
    for f in a["images"]:
        r = post(f"{ACT}/adimages", bytes=base64.b64encode((IMG / f).read_bytes()).decode(), name=f)
        hashes.append(next(iter(r["images"].values()))["hash"])
    spec = {
        "name": f"copy v4 · {datetime.date.today().isoformat()} · {name}",
        # Same structure as the live V2 creative: link_data carries the link/CTA, asset_feed_spec the variations.
        "object_story_spec": {"page_id": PAGE, "instagram_user_id": IG, "link_data": {
            "link": LINK, "image_hash": hashes[0], "message": a["body"], "name": a["titles"][0], "description": DESC,
            "caption": "orchidpros.com", "call_to_action": {"type": "BOOK_NOW", "value": {"link": LINK}}}},
        "asset_feed_spec": {
            "images": [{"hash": h} for h in hashes],
            "bodies": [{"text": a["body"]}],
            "titles": [{"text": t} for t in a["titles"]],
            "descriptions": [{"text": DESC}],
            "optimization_type": "DEGREES_OF_FREEDOM",  # Flexible format; without it Meta treats it as Dynamic Creative
        },
        "degrees_of_freedom_spec": {"creative_features_spec": {k: {"enroll_status": "OPT_OUT"} for k in OPT_OUT}},
        "url_tags": URL_TAGS,
    }
    try:
        cr = post(f"{ACT}/adcreatives", **spec)
        ad = post(f"{ACT}/ads", name=name, adset_id=ADSET, creative={"creative_id": cr["id"]}, status="PAUSED")
        created.append({"ad": name, "ad_id": ad["id"], "creative_id": cr["id"], "image_hashes": hashes})
        print(f"Creado (pausado): {name} · ad {ad['id']}")
    except MetaError as e:
        print(f"ERROR en {name}:\n{e}")
        break
if hyper and len(created) == len(ADS):
    src = get(ADSET, fields="campaign_id,optimization_goal,billing_event,bid_strategy,promoted_object,attribution_spec,targeting")
    t = dict(HYPER_TARGETING)
    if src["targeting"].get("excluded_custom_audiences"):
        t["excluded_custom_audiences"] = src["targeting"]["excluded_custom_audiences"]
    end = (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=20)).strftime("%Y-%m-%dT%H:%M:%S+0000")
    try:
        hs = post(f"{ACT}/adsets", name="HYPERLOCAL | Immigration courts NYC-Newark-PHL | 25-65 | 2026 Oct",
                  campaign_id=src["campaign_id"], daily_budget=HYPER_BUDGET, end_time=end, status="PAUSED",
                  optimization_goal=src["optimization_goal"], billing_event=src["billing_event"],
                  bid_strategy=src.get("bid_strategy", "LOWEST_COST_WITHOUT_CAP"), promoted_object=src["promoted_object"],
                  attribution_spec=src.get("attribution_spec"), targeting=t)
        for c in created:
            ad = post(f"{ACT}/ads", name=c["ad"].replace("- Static", "- Hyperlocal"), adset_id=hs["id"],
                      creative={"creative_id": c["creative_id"]}, status="PAUSED")
            c["hyperlocal_ad_id"] = ad["id"]
        post(ADSET, daily_budget=CAP - HYPER_BUDGET)
        print(f"Piloto hiperlocal creado (pausado): ad set {hs['id']}; nacional ahora ${(CAP-HYPER_BUDGET)/100:.2f}/día")
        created.append({"hyperlocal_adset_id": hs["id"]})
    except MetaError as e:
        print(f"ERROR en el piloto hiperlocal (el presupuesto nacional no se tocó):\n{e}")
(BUILD / f"launch-copy-v4-{datetime.date.today().isoformat()}.json").write_text(json.dumps(created, indent=2), encoding="utf-8")
