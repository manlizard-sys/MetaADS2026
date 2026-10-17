"""🔵 S11 Immigration Intake Calls: third ad for the hyperlocal ad set (copy in build/copy_s11.md).
Reuses the S5 image already in the account. Default is a dry run; --apply creates it ACTIVE.
"""
import sys
from meta import get, post

ACT = "act_1806647434085082"
PAGE, IG = "1132642053254708", "17841473464921031"
ADSET = "120257317011450196"
LINK = "https://go.orchidpros.com/hire"
IMAGE_HASH = "59543131f48ec2b42b2be7627536d501"  # S5 "Still answering every call yourself?"
NAME = "🔵 S11 Immigration Intake Calls - Hyperlocal - 2026 Oct"
URL_TAGS = ("utm_source={{site_source_name}}&utm_medium=paid_social&utm_campaign={{campaign.name}}"
            "&utm_term={{adset.name}}&utm_content={{ad.name}}&utm_id={{campaign.id}}&placement={{placement}}")
BODY = (
    "Immigration attorneys: how many Spanish intake calls hit voicemail this week? 📞\n\n"
    "Every missed call is a family that dials the next firm on the list.\n\n"
    "Orchid places a dedicated bilingual legal assistant on your team, during your business hours. "
    "They answer and qualify intake calls in Spanish and English, book consultations, update clients on case status, "
    "and collect documents for filings.\n\n"
    "You stay on cases. Your assistant keeps the phones, the calendar, and the paperwork moving.\n\n"
    "Your firm pays from $15/hr. Assistants are based in Colombia and screened by Orchid's HR team for U.S. legal experience.\n\n"
    "Book a free call to see if it's a fit for your firm ⚖️")
TITLES = ["Never miss a Spanish intake call", "Bilingual intake for immigration firms", "Legal support from $15/hr"]
DESC = "For U.S. law firms · English & Spanish"
OPT_OUT = ["text_optimizations", "image_touchups", "image_templates", "image_uncrop", "image_animation",
           "enhance_cta", "description_automation", "add_text_overlay", "adapt_to_placement"]

assert all(len(t) <= 40 for t in TITLES)
print(get(ADSET, fields="name")["name"], "\n", NAME, "\n ", BODY.splitlines()[0], "\n  Titulares:", " | ".join(TITLES))
if "--apply" not in sys.argv:
    sys.exit("\nVista previa. Nada cambió. Ejecuta con --apply.")
cr = post(f"{ACT}/adcreatives", name=f"copy s11 · {NAME}", url_tags=URL_TAGS,
          object_story_spec={"page_id": PAGE, "instagram_user_id": IG, "link_data": {
              "link": LINK, "image_hash": IMAGE_HASH, "message": BODY, "name": TITLES[0], "description": DESC,
              "caption": "orchidpros.com", "call_to_action": {"type": "BOOK_TRAVEL", "value": {"link": LINK, "link_caption": "orchidpros.com"}}}},
          asset_feed_spec={"bodies": [{"text": BODY}], "titles": [{"text": t} for t in TITLES],
                           "descriptions": [{"text": DESC}], "optimization_type": "DEGREES_OF_FREEDOM"},
          degrees_of_freedom_spec={"creative_features_spec": {k: {"enroll_status": "OPT_OUT"} for k in OPT_OUT}})
ad = post(f"{ACT}/ads", name=NAME, adset_id=ADSET, creative={"creative_id": cr["id"]}, status="ACTIVE")
print(f"Creado y activado: {NAME} · ad {ad['id']} · creative {cr['id']}")
