"""v5 forms (2026-11-20, approved by the user after the Nov 16 meeting with Mehdi).

Click-to-lead was ~5% on the v3 short forms (60 clicks, 3 leads since Nov 16), so the v5 forms:
- drop the intro screen (context card) and the "need" question: 4 fields (homeowner, ZIP, name,
  phone; name and phone prefilled by Facebook);
- keep the homeowner options ("No, I rent" / "No, alquilo") so the GHL renter rule still works;
- put the tracking number 305-239-4987 on the thank-you call button;
- keep the same UTMs.

Stage 1 (this file, --forms): create the 12 forms only. They are not attached to any ad, so this
does not touch delivery or learning. GHL maps them before stage 2 swaps the ads.

Resumable through build/ids.json ("launch_v2", keys form5_*). Usage: python3 forms_v5.py [--apply]
"""
import sys
import launch_v2 as L
import utm_v2 as U

L.APPLY = "--apply" in sys.argv
PHONE = "+13052394987"
OFFERS = ["fl", "ev", "pn", "tu", "iaq", "si"]


def form_name(offer, lang):
    return f"SB · {offer.upper()} · {lang.upper()} · Nov 2026 v5 · 239"


def make_form5(offer, lang):
    own_label, own_opts = L.Q[lang]["own"]
    t_title, t_body, t_btn = L.THANKS[lang]
    return L.page_post(f"{L.PAGE}/leadgen_forms",
        name=form_name(offer, lang), locale="en_US" if lang == "en" else "es_LA",
        is_optimized_for_quality=False,
        questions=[{"type": "CUSTOM", "key": "own", "label": own_label, "options": L.opt(*own_opts)},
                   {"type": "ZIP"}, {"type": "FULL_NAME"}, {"type": "PHONE"}],
        privacy_policy=L.PRIVACY, follow_up_action_url="https://sunnybliss.com/",
        tracking_parameters=U.tracking(offer, lang),
        thank_you_page={"title": t_title, "body": t_body, "button_type": "CALL_BUSINESS",
                        "button_text": t_btn, "business_phone_number": PHONE, "country_code": "US"})["id"]


def main():
    for o in OFFERS:
        for l in ("en", "es"):
            L.once(f"form5_{o}_{l}", f"form {form_name(o, l)}", lambda o=o, l=l: make_form5(o, l))
    print("APPLIED" if L.APPLY else "dry run, nothing created")


if __name__ == "__main__":
    main()
