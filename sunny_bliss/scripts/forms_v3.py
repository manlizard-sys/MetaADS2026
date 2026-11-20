"""Short forms for the v2 leads ads (2026-11-09).

Only 2 of 56 clickers submitted the Higher Intent form (7 questions + review screen). This creates
8 new standard forms with 5 fields (need, homeowner, ZIP, name, phone), the same tracking
parameters and thank-you screen, puts them on the same 8 ads with new creatives, archives the
previous forms, and activates the Silver Plan and New AC ads (EN + ES), which were paused.

Resumable through build/ids.json ("launch_v2", keys *3). Usage: python3 forms_v3.py [--apply]
"""
import sys
import launch_v2 as L
import utm_v2 as U
import meta

L.APPLY = "--apply" in sys.argv
ACTIVATE = ["si_en", "si_es", "ac_en", "ac_es"]


def short_questions(offer, lang):
    need_label, need_opts = L.OFFERS[offer][lang]["need"]
    own_label, own_opts = L.Q[lang]["own"]
    return [{"type": "CUSTOM", "key": "need", "label": need_label, "options": L.opt(*need_opts)},
            {"type": "CUSTOM", "key": "own", "label": own_label, "options": L.opt(*own_opts)},
            {"type": "ZIP"}, {"type": "FULL_NAME"}, {"type": "PHONE"}]


def make_form3(offer, lang):
    c = L.OFFERS[offer][lang]
    t_title, t_body, t_btn = L.THANKS[lang]
    return L.page_post(f"{L.PAGE}/leadgen_forms",
        name=f"SB · {offer.upper()} · {lang.upper()} · Nov 2026 v3 · short",
        locale="en_US" if lang == "en" else "es_LA",
        is_optimized_for_quality=False,
        questions=short_questions(offer, lang),
        privacy_policy=L.PRIVACY,
        follow_up_action_url="https://sunnybliss.com/",
        tracking_parameters=U.tracking(offer, lang),
        context_card={"title": c["card"][0], "style": "LIST_STYLE", "content": c["card"][1]},
        thank_you_page={"title": t_title, "body": t_body, "button_type": "CALL_BUSINESS",
                        "button_text": t_btn, "business_phone_number": L.PHONE, "country_code": "US"})["id"]


def main():
    s = L.state
    for o, spec in L.OFFERS.items():
        for l in ("en", "es"):
            c = spec[l]
            name = f"{o.upper()} · {c['head']} · {l.upper()}"
            f3 = L.once(f"form3_{o}_{l}", f"short form {o} {l}", lambda o=o, l=l: make_form3(o, l))
            cr3 = L.once(f"cr3_{o}_{l}", f"creative {name} (short form)", lambda o=o, l=l, c=c, name=name, f3=f3: L.creative(f"{name} · short form", {"link_data": {
                "image_hash": s[f"img_{o}_{l}"], "link": "http://fb.me/", "message": c["msg"], "name": c["head"], "description": c["desc"],
                "call_to_action": {"type": spec["cta"], "value": {"lead_gen_form_id": f3}}}}))
            L.once(f"swap3_{o}_{l}", f"ad {name} -> short form", lambda o=o, l=l, cr3=cr3: (meta.post(s[f"ad_{o}_{l}"], creative={"creative_id": cr3}), cr3)[1])
            L.once(f"archived_form2_{o}_{l}", f"archive UTM form {o} {l}", lambda o=o, l=l: (L.page_post(s[f"form2_{o}_{l}"], status="ARCHIVED"), "ARCHIVED")[1])
    for k in ACTIVATE:
        L.once(f"activated_{k}", f"activate ad {k}", lambda k=k: (meta.post(s[f"ad_{k}"], status="ACTIVE"), "ACTIVE")[1])
    print("APPLIED" if L.APPLY else "dry run, nothing changed")


if __name__ == "__main__":
    main()
