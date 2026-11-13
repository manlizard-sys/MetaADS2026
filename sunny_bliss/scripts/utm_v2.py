"""Adds tracking to the v2 launch (everything stays PAUSED).

- Awareness: new creatives with url_tags (UTM) on the same 4 ads.
- Leads: 8 new Higher Intent forms, identical to the first ones plus tracking parameters
  (utm_source / utm_medium / utm_campaign / utm_content) that travel with every lead to the CRM;
  new creatives on the same 8 ads; the 8 first forms are archived (they never received a lead).

Resumable through build/ids.json ("launch_v2", keys *2). Usage: python3 utm_v2.py [--apply]
"""
import sys
import launch_v2 as L
import meta

L.APPLY = "--apply" in sys.argv
URL_TAGS = "utm_source=facebook&utm_medium=paid_social&utm_campaign={{campaign.name}}&utm_content={{ad.name}}"


def tracking(offer, lang):
    return {"utm_source": "facebook", "utm_medium": "paid_social",
            "utm_campaign": "sb_leads_nov2026_v2", "utm_content": f"{offer}_{lang}"}


def make_form2(offer, lang):
    c = L.OFFERS[offer][lang]
    t_title, t_body, t_btn = L.THANKS[lang]
    return L.page_post(f"{L.PAGE}/leadgen_forms",
        name=f"SB · {offer.upper()} · {lang.upper()} · Nov 2026 v2 · UTM",
        locale="en_US" if lang == "en" else "es_LA",
        is_optimized_for_quality=True,
        questions=L.form_questions(offer, lang),
        privacy_policy=L.PRIVACY,
        follow_up_action_url="https://sunnybliss.com/",
        tracking_parameters=tracking(offer, lang),
        context_card={"title": c["card"][0], "style": "LIST_STYLE", "content": c["card"][1]},
        thank_you_page={"title": t_title, "body": t_body, "button_type": "CALL_BUSINESS",
                        "button_text": t_btn, "business_phone_number": L.PHONE, "country_code": "US"})["id"]


def main():
    s = L.state
    print("LEADS: new forms with tracking, new creatives, same ads")
    for o, spec in L.OFFERS.items():
        for l in ("en", "es"):
            c = spec[l]
            name = f"{o.upper()} · {c['head']} · {l.upper()}"
            f2 = L.once(f"form2_{o}_{l}", f"form {o} {l} + UTM", lambda o=o, l=l: make_form2(o, l))
            cr2 = L.once(f"cr2_{o}_{l}", f"creative {name}", lambda o=o, l=l, c=c, name=name, f2=f2: L.creative(f"{name} · UTM", {"link_data": {
                "image_hash": s[f"img_{o}_{l}"], "link": "http://fb.me/", "message": c["msg"], "name": c["head"], "description": c["desc"],
                "call_to_action": {"type": spec["cta"], "value": {"lead_gen_form_id": f2}}}}))
            L.once(f"swap_{o}_{l}", f"ad {name} -> new creative", lambda o=o, l=l, cr2=cr2: (meta.post(s[f"ad_{o}_{l}"], creative={"creative_id": cr2}), cr2)[1])
            L.once(f"archived_form_{o}_{l}", f"archive first form {o} {l}", lambda o=o, l=l: (L.page_post(s[f"form_{o}_{l}"], status="ARCHIVED"), "ARCHIVED")[1])

    print("AWARENESS: new creatives with UTM, same ads")
    for a, spec in L.AWARE.items():
        for l in ("en", "es"):
            msg, head = spec[l]
            name = f"{a.upper()} · {head} · {l.upper()}"
            cr2 = L.once(f"cr2_{a}_{l}", f"creative {name} + UTM", lambda a=a, l=l, msg=msg, head=head, name=name: meta.post(f"{L.ACT}/adcreatives", name=f"{name} · UTM",
                url_tags=URL_TAGS, object_story_spec={"page_id": L.PAGE, "instagram_user_id": L.IG, "link_data": {
                    "image_hash": s[f"img_{a}_{l}"], "link": "https://sunnybliss.com/", "message": msg, "name": head,
                    "call_to_action": {"type": "LEARN_MORE", "value": {"link": "https://sunnybliss.com/"}}}})["id"])
            L.once(f"swap_{a}_{l}", f"ad {name} -> new creative", lambda a=a, l=l, cr2=cr2: (meta.post(s[f"ad_{a}_{l}"], creative={"creative_id": cr2}), cr2)[1])
    print("APPLIED, all PAUSED" if L.APPLY else "dry run, nothing changed")


if __name__ == "__main__":
    main()
