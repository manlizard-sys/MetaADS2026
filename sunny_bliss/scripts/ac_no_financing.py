"""Fix for the disapproved New AC ad (2026-11-16, Meta: discriminatory practices / credit). Financing
("0% interest for 60 months, approved credit") makes Meta treat the ad as a credit ad, which needs
the financial special ad category (no ZIP or age targeting). Both AC ads (EN + ES) drop financing:
new image, new copy and new short forms without the financing line. Financing is offered on the call.
Resumable through build/ids.json ("launch_v2", keys v4*_ac_*). Usage: python3 ac_no_financing.py [--apply]
"""
import sys
import launch_v2 as L
import utm_v2 as U
import batch_v3 as B
import meta

L.APPLY = "--apply" in sys.argv
COPY = {
  "en": {"msg": "For Miami-Dade homeowners: replace your AC before it fails. New systems from $5,800 for a limited time. Free quote with a flat-rate price before we start, licensed installers (Lic. CAC1823405) and permits included.",
         "head": "New AC from $5,800 · free quote", "desc": "Limited time · Lic. CAC1823405",
         "card": ("New AC from $5,800", ["Limited-time offer", "Free quote with a flat-rate price", "Licensed installers, permits included", "Family-run since 1990, 4.9 on Google"])},
  "es": {"msg": "Para dueños de casa en Miami-Dade: cambia tu aire antes de que falle. Equipos nuevos desde $5,800 por tiempo limitado. Cotización gratis con precio fijo antes de empezar, instaladores con licencia (Lic. CAC1823405) y permisos incluidos.",
         "head": "Aire nuevo desde $5,800 · cotización gratis", "desc": "Por tiempo limitado · Lic. CAC1823405",
         "card": ("Aire nuevo desde $5,800", ["Oferta por tiempo limitado", "Cotización gratis con precio fijo", "Instaladores con licencia y permisos incluidos", "Empresa familiar desde 1990, 4.9 en Google"])},
}


def make_form(lang):
    c, base = COPY[lang], L.OFFERS["ac"][lang]
    t_title, t_body, t_btn = L.THANKS[lang]
    own_label, own_opts = L.Q[lang]["own"]
    return L.page_post(f"{L.PAGE}/leadgen_forms",
        name=f"SB · AC · {lang.upper()} · Nov 2026 v4 · no financing", locale="en_US" if lang == "en" else "es_LA",
        is_optimized_for_quality=False,
        questions=[{"type": "CUSTOM", "key": "need", "label": base["need"][0], "options": L.opt(*base["need"][1])},
                   {"type": "CUSTOM", "key": "own", "label": own_label, "options": L.opt(*own_opts)},
                   {"type": "ZIP"}, {"type": "FULL_NAME"}, {"type": "PHONE"}],
        privacy_policy=L.PRIVACY, follow_up_action_url="https://sunnybliss.com/",
        tracking_parameters=U.tracking("ac", lang),
        context_card={"title": c["card"][0], "style": "LIST_STYLE", "content": c["card"][1]},
        thank_you_page={"title": t_title, "body": t_body, "button_type": "CALL_BUSINESS",
                        "button_text": t_btn, "business_phone_number": L.PHONE, "country_code": "US"})["id"]


def main():
    s = L.state
    for l in ("en", "es"):
        c = COPY[l]
        name = f"AC · {c['head']} · {l.upper()}"
        form = L.once(f"form4_ac_{l}", f"form ac {l} (no financing)", lambda l=l: make_form(l))
        img = L.once(f"v4img_ac_{l}", f"image ac_{l} (no financing)", lambda l=l: B.upload(f"ac_{l}"))
        cr = L.once(f"v4cr_ac_{l}", f"creative {name}", lambda c=c, name=name, img=img, form=form: L.creative(f"{name} · v4 no financing", {"link_data": {
            "image_hash": img, "link": "http://fb.me/", "message": c["msg"], "name": c["head"], "description": c["desc"],
            "call_to_action": {"type": "GET_QUOTE", "value": {"lead_gen_form_id": form}}}}))
        L.once(f"v4swap_ac_{l}", f"ad AC {l} -> no financing", lambda l=l, cr=cr, name=name: (meta.post(s[f"ad_ac_{l}"], creative={"creative_id": cr}, name=name), cr)[1])
    print("APPLIED" if L.APPLY else "dry run, nothing changed")


if __name__ == "__main__":
    main()
