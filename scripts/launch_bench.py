"""Bench of 6 single-image ads for the HYPERLOCAL ad set, one per approved image (Debi, 2026-10-15).

Copy written by Claude (🔵 in the name), angles different from S9/S10/S11; see build/copy_hyperlocal_bench.md.
All ads are created PAUSED: ready to rotate in when an active ad is paused. CTA BOOK_TRAVEL ("Book now"),
which follows the landing link (BOOK_NOW opens the Page appointment form). Default is a dry run.
Usage: python3 launch_bench.py [--apply]
"""
import datetime, json, sys
from meta import get, post, BUILD

ACT = "act_1806647434085082"
PAGE, IG = "1132642053254708", "17841473464921031"
ADSET = "120257317011450196"
LINK = "https://go.orchidpros.com/hire"
DESC = "For U.S. law firms · English & Spanish"
URL_TAGS = ("utm_source={{site_source_name}}&utm_medium=paid_social&utm_campaign={{campaign.name}}"
            "&utm_term={{adset.name}}&utm_content={{ad.name}}&utm_id={{campaign.id}}&placement={{placement}}")
OPT_OUT = ["text_optimizations", "image_touchups", "image_templates", "image_uncrop", "image_animation",
           "enhance_cta", "description_automation", "add_text_overlay", "adapt_to_placement"]
CLOSE = "Your firm pays from $15/hr. Assistants are based in Colombia and vetted by Orchid."

ADS = [
    ("🔵 H1 Sticky Notes Follow-ups - Hyperlocal - 2026 Oct", "3c13a3f2d7cffa2c2102006cdc44a125",  # for_the_attorneys_1
     "Attorneys: how many sticky notes are on your desk right now? 📝\n\n"
     "Callbacks. Document requests. Court dates. Client updates. Every one of them waits until you have a free minute.\n\n"
     "Orchid places a dedicated bilingual legal assistant on your team, during your business hours. They track follow-ups, "
     "chase missing documents, and keep clients updated in English and Spanish.\n\n"
     f"{CLOSE}\n\nBook a free call to see if it's a fit for your firm ⚖️",
     ["Clear the sticky notes off your desk", "Follow-ups handled in EN and ES", "Legal support from $15/hr"]),
    ("🔵 H2 After-Hours Paperwork - Hyperlocal - 2026 Oct", "1a90c7e1d93e86b1fcc277cc7cb9f4d3",  # for_the_attorneys_2
     "Attorneys: still doing intake paperwork after 7 pm? 🕖\n\n"
     "Your billable hours go to cases. Your evenings go to everything else: forms, scheduling, emails, client questions.\n\n"
     "Orchid places a dedicated bilingual legal assistant on your team who takes the admin work off your plate during your "
     "business hours, in English and Spanish.\n\n"
     "You keep the legal work. They keep the office running.\n\n"
     f"{CLOSE}\n\nBook a free call to see if it's a fit for your firm ⚖️",
     ["Get your evenings back", "Admin off your plate from $15/hr", "Bilingual support for law firms"]),
    ("🔵 H3 Saturdays Back - Hyperlocal - 2026 Oct", "abba763ff887235950bfff1cbf1b51f6",  # for_the_attorneys_3
     "Solo and small-firm attorneys: when was your last Saturday off? 😮‍💨\n\n"
     "When the lawyer is also the receptionist and the paralegal, the work never stops.\n\n"
     "Orchid places a dedicated bilingual legal assistant on your team, during your business hours. Intake, scheduling, "
     "document collection, and client follow-ups in English and Spanish.\n\n"
     "Same person every week, trained on how your firm works.\n\n"
     f"{CLOSE}\n\nBook a free call to see if it's a fit for your firm ⚖️",
     ["Stop being your own receptionist", "Take your Saturdays back", "Legal support from $15/hr"]),
    ("🔵 H4 Spanish-Speaking Clients - Hyperlocal - 2026 Oct", "322d9a47bcfb6ba0d34136dbdd9b02dc",  # still_depending_on_interns_1
     "Immigration attorneys: how many of your clients would rather explain their case in Spanish? 🗣️\n\n"
     "A bilingual assistant on your team means every call, every intake, and every document request happens in the "
     "language your client is most comfortable with.\n\n"
     "Orchid places a dedicated bilingual legal assistant on your team, during your business hours, fluent in English and Spanish.\n\n"
     f"{CLOSE}\n\nBook a free call to see if it's a fit for your firm ⚖️",
     ["Serve Spanish-speaking clients better", "Bilingual intake from $15/hr", "For immigration law firms"]),
    ("🔵 H5 Phones While In Court - Hyperlocal - 2026 Oct", "61df2a78a86daa8b58ccb496f3cd7077",  # still_depending_on_interns_2
     "Attorneys: when you're in court, who answers your phone? ⚖️\n\n"
     "A hearing at Federal Plaza, Broad Street, or Market Street can take the whole morning. Meanwhile, new clients are calling.\n\n"
     "Orchid places a dedicated bilingual legal assistant on your team who answers, qualifies, and schedules while you're "
     "in court, in English and Spanish.\n\n"
     f"{CLOSE}\n\nBook a free call to see if it's a fit for your firm 📞",
     ["Your phones covered while in court", "Never miss a new client call", "Bilingual intake from $15/hr"]),
    ("🔵 H6 Cost Of In-Office Support - Hyperlocal - 2026 Oct", "756418bc922152fadfc961f13e1f9c10",  # still_depending_on_interns_3
     "Law firm owners: what does in-office support really cost your firm? 💸\n\n"
     "Payroll taxes, benefits, desk space, and retraining every time someone leaves.\n\n"
     "Orchid places a dedicated bilingual legal assistant on your team, during your business hours, at a predictable "
     "hourly rate: from $15/hr. They handle intake, scheduling, documents, and client follow-ups in English and Spanish.\n\n"
     "Assistants are based in Colombia and vetted by Orchid.\n\n"
     "Book a free call to see if it's a fit for your firm ⚖️",
     ["Predictable support from $15/hr", "Cut the cost of in-office support", "Bilingual legal support for firms"]),
]

apply = "--apply" in sys.argv
print(get(ADSET, fields="name")["name"])
for name, h, body, titles in ADS:
    assert all(len(t) <= 40 for t in titles), titles
    print(f"\n{name}  ·  PAUSED\n   {body.splitlines()[0]}\n   Titulares: {' | '.join(titles)}")
if not apply:
    sys.exit("\nVista previa. Nada cambió. Ejecuta con --apply (se crean PAUSADOS).")

created = []
for name, h, body, titles in ADS:
    cr = post(f"{ACT}/adcreatives", name=f"bench · {datetime.date.today().isoformat()} · {name}", url_tags=URL_TAGS,
              object_story_spec={"page_id": PAGE, "instagram_user_id": IG, "link_data": {
                  "link": LINK, "image_hash": h, "message": body, "name": titles[0], "description": DESC,
                  "caption": "orchidpros.com",
                  "call_to_action": {"type": "BOOK_TRAVEL", "value": {"link": LINK, "link_caption": "orchidpros.com"}}}},
              asset_feed_spec={"bodies": [{"text": body}], "titles": [{"text": t} for t in titles],
                               "descriptions": [{"text": DESC}], "optimization_type": "DEGREES_OF_FREEDOM"},
              degrees_of_freedom_spec={"creative_features_spec": {k: {"enroll_status": "OPT_OUT"} for k in OPT_OUT}})
    ad = post(f"{ACT}/ads", name=name, adset_id=ADSET, creative={"creative_id": cr["id"]}, status="PAUSED")
    created.append({"ad": name, "ad_id": ad["id"], "creative_id": cr["id"], "image_hash": h})
    print(f"Creado (pausado): {name} · ad {ad['id']}")
(BUILD / f"launch-bench-{datetime.date.today().isoformat()}.json").write_text(json.dumps(created, indent=2, ensure_ascii=False), encoding="utf-8")
