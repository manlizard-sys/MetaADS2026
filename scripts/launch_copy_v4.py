"""Create the two attorney static ads (copy v4, build/copy_v4.md) with Debi's creatives of 2026-10-15.

Each ad = one creative with its 3 images as variations (Flexible format), one primary text,
3 headlines, 1 description, CTA Book Now, same landing and UTMs as the live ads.
Ads are created PAUSED; activate them after review. Default is a dry run.
Usage: python3 launch_copy_v4.py [--adset <ad set id>] [--apply]
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
aset = get(ADSET, fields="name,effective_status")
print(f"Conjunto de anuncios: {aset['name']} ({aset['effective_status']})")
for name, a in ADS.items():
    for f in a["images"]:
        assert (IMG / f).exists(), f"Falta {IMG / f}"
    assert all(len(t) <= 40 for t in a["titles"]), [t for t in a["titles"] if len(t) > 40]
    print(f"\n{name}  ·  {len(a['images'])} imágenes  ·  estado PAUSED")
    print("  ", a["body"].splitlines()[0])
    print("   Titulares:", " | ".join(a["titles"]))
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
        "object_story_spec": {"page_id": PAGE, "instagram_user_id": IG},
        "asset_feed_spec": {
            "images": [{"hash": h} for h in hashes],
            "bodies": [{"text": a["body"]}],
            "titles": [{"text": t} for t in a["titles"]],
            "descriptions": [{"text": DESC}],
            "link_urls": [{"website_url": LINK, "display_url": "orchidpros.com"}],
            "call_to_action_types": ["BOOK_NOW"],
            "ad_formats": ["SINGLE_IMAGE"],
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
(BUILD / f"launch-copy-v4-{datetime.date.today().isoformat()}.json").write_text(json.dumps(created, indent=2), encoding="utf-8")
