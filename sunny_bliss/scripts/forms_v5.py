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


if __name__ == "__main__" and "--swap" not in sys.argv:
    main()


# ---- Stage 2 (--swap): ads move to the v5 forms and images ---------------------------------
# Keeps each ad's current copy (message, headline, description) and adds the tracking number at
# the end of the message; new image from build/ads/v5; CTA "Book now"; same ad IDs (no new ads).
# Pauses the new-AC pair (lowest CTR, no leads). Ads already paused stay paused.
import pathlib
import meta

IMG5 = pathlib.Path(__file__).resolve().parent.parent / "build" / "ads" / "v5"
CALL = {"en": "Call 305-239-4987 or tap Book now.", "es": "Llama al 305-239-4987 o toca Reserva ya."}
CTA = "BOOK_TRAVEL"  # shown as "Book now"; BOOK_NOW is not allowed with lead forms


def ad_ids():
    s = L.state
    ids = {f"{o}_{l}": s[f"ad_{o}_{l}"] for o in ("tu", "si", "fl") for l in ("en", "es")}
    ids.update({f"iaq_{l}": s[f"ad_iaq_{l}"] for l in ("en", "es")})
    ids.update({f"{o}_{l}": s[f"elec_ad_{o}_{l}"] for o in ("ev", "pn") for l in ("en", "es")})
    return ids


def upload5(name):
    with open(IMG5 / f"{name}.png", "rb") as fh:
        r = meta.post(f"{L.ACT}/adimages", files={f"v5_{name}.png": fh})
    return next(iter(r["images"].values()))["hash"]


def new_creative(k, ad_id, img):
    ad = meta.get(ad_id, fields="name,creative{object_story_spec}")
    ld = ad["creative"]["object_story_spec"]["link_data"]
    lang = k.rsplit("_", 1)[1]
    msg = ld["message"].rstrip()
    if "305-239-4987" not in msg:
        msg = f"{msg}\n\n{CALL[lang]}"
    return L.creative(f"{ad['name']} · v5", {"link_data": {
        "image_hash": img, "link": ld.get("link", "http://fb.me/"), "message": msg, "name": ld["name"],
        "description": ld.get("description", ""),
        "call_to_action": {"type": CTA, "value": {"lead_gen_form_id": L.state[f"form5_{k}"]}}}})


def swap():
    for k, ad_id in ad_ids().items():
        img = L.once(f"v5img_{k}", f"image v5 {k}.png", lambda k=k: upload5(k))
        cr = L.once(f"v5cr_{k}", f"creative v5 {k}", lambda k=k, ad_id=ad_id, img=img: new_creative(k, ad_id, img))
        L.once(f"v5swap_{k}", f"ad {k} -> v5 creative", lambda ad_id=ad_id, cr=cr: (meta.post(ad_id, creative={"creative_id": cr}), cr)[1])
    for k in ("ac_en", "ac_es"):
        L.once(f"v5paused_{k}", f"pause ad {k}", lambda k=k: (meta.post(L.state[f"ad_{k}"], status="PAUSED"), "PAUSED")[1])


if __name__ == "__main__" and "--swap" in sys.argv:
    swap()
    print("APPLIED" if L.APPLY else "dry run, nothing changed")
