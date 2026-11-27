"""Electrical launch offers (2026-11-11): EV charger $200 off and panel upgrade $500 off, with the
EV + panel bundle (save $750) as the secondary hook. EN + ES, added to the v2 leads ad set
(same budget, Andromeda decides delivery), each with its own short form and UTM parameters.

Needs the electrical contractor license number, which Florida requires on contractor advertising:
images are rendered with it first (render_elec.js), then uploaded from build/ads/v2/elec/.
Resumable through build/ids.json ("launch_v2", keys *_ev_* / *_pn_*).
Usage: python3 launch_electrical.py --lic EC13000000 [--apply] [--active]
"""
import pathlib, sys
import launch_v2 as L
import utm_v2 as U
import meta

L.APPLY = "--apply" in sys.argv
ACTIVE = "--active" in sys.argv
LIC = sys.argv[sys.argv.index("--lic") + 1] if "--lic" in sys.argv else sys.exit("--lic <electrical license number> is required")
IMG = pathlib.Path(__file__).resolve().parent.parent / "build" / "ads" / "v2" / "elec"

OFFERS = {
  "ev": {"cta": "GET_QUOTE",
    "en": {"msg": "Launch offer: $200 off your EV charger installation. Level 2 home charger installed by licensed electricians, with a panel check included. Adding a panel upgrade? Save $750 on both.",
           "head": "EV charger install: $200 off", "desc": f"New electrical service · Lic. {LIC}",
           "need": ("What do you need?", ["EV charger installation", "EV charger + panel upgrade", "Other electrical work"]),
           "card": ("EV charger installation, $200 off", ["Launch offer for our new electrical service", "Level 2 home charger", "Panel check included", "EV + panel upgrade: save $750"])},
    "es": {"msg": "Oferta de lanzamiento: $200 de descuento en la instalación de tu cargador para auto eléctrico. Cargador Nivel 2 instalado por electricistas con licencia, con revisión del panel incluida. ¿También cambias el panel? Ahorra $750 en los dos.",
           "head": "Cargador para auto eléctrico: $200 menos", "desc": f"Nuevo servicio eléctrico · Lic. {LIC}",
           "need": ("¿Qué necesita?", ["Instalación de cargador", "Cargador + cambio de panel", "Otro trabajo eléctrico"]),
           "card": ("Cargador para auto eléctrico, $200 menos", ["Oferta de lanzamiento de nuestro servicio eléctrico", "Cargador de casa Nivel 2", "Revisión del panel incluida", "Cargador + cambio de panel: ahorra $750"])}},
  "pn": {"cta": "GET_QUOTE",
    "en": {"msg": "Launch offer: $500 off your electrical panel upgrade. We replace Federal Pacific, Zinsco and 100A panels, permit and inspection included, so your home is insurance-ready. Add an EV charger and save $750.",
           "head": "Panel upgrade: $500 off", "desc": f"New electrical service · Lic. {LIC}",
           "need": ("What do you need?", ["Panel upgrade", "Panel upgrade + EV charger", "Insurance or 4-point inspection fix", "Other electrical work"]),
           "card": ("Electrical panel upgrade, $500 off", ["Launch offer for our new electrical service", "Federal Pacific, Zinsco or 100A panels", "Permit and inspection included", "Panel + EV charger: save $750"])},
    "es": {"msg": "Oferta de lanzamiento: $500 de descuento en el cambio de tu panel eléctrico. Cambiamos paneles Federal Pacific, Zinsco y de 100A, con permiso e inspección incluidos, para que tu casa quede lista para el seguro. Agrega un cargador y ahorra $750.",
           "head": "Cambio de panel: $500 menos", "desc": f"Nuevo servicio eléctrico · Lic. {LIC}",
           "need": ("¿Qué necesita?", ["Cambio de panel", "Cambio de panel + cargador", "Arreglo para el seguro o inspección de 4 puntos", "Otro trabajo eléctrico"]),
           "card": ("Cambio de panel eléctrico, $500 menos", ["Oferta de lanzamiento de nuestro servicio eléctrico", "Paneles Federal Pacific, Zinsco o de 100A", "Permiso e inspección incluidos", "Panel + cargador: ahorra $750"])}},
}


def make_form(offer, lang):
    c = OFFERS[offer][lang]
    t_title, t_body, t_btn = L.THANKS[lang]
    own_label, own_opts = L.Q[lang]["own"]
    return L.page_post(f"{L.PAGE}/leadgen_forms",
        name=f"SB · {offer.upper()} · {lang.upper()} · Electrical launch · Nov 2026",
        locale="en_US" if lang == "en" else "es_LA", is_optimized_for_quality=False,
        questions=[{"type": "CUSTOM", "key": "need", "label": c["need"][0], "options": L.opt(*c["need"][1])},
                   {"type": "CUSTOM", "key": "own", "label": own_label, "options": L.opt(*own_opts)},
                   {"type": "ZIP"}, {"type": "FULL_NAME"}, {"type": "PHONE"}],
        privacy_policy=L.PRIVACY, follow_up_action_url="https://sunnybliss.com/",
        tracking_parameters=U.tracking(offer, lang),
        context_card={"title": c["card"][0], "style": "LIST_STYLE", "content": c["card"][1]},
        thank_you_page={"title": t_title, "body": t_body, "button_type": "CALL_BUSINESS",
                        "button_text": t_btn, "business_phone_number": L.PHONE, "country_code": "US"})["id"]


def upload(name):
    with open(IMG / f"{name}.png", "rb") as fh:
        r = meta.post(f"{L.ACT}/adimages", files={f"{name}.png": fh})
    return next(iter(r["images"].values()))["hash"]


def main():
    s = L.state
    for o, spec in OFFERS.items():
        for l in ("en", "es"):
            c = spec[l]
            name = f"{o.upper()} · {c['head']} · {l.upper()}"
            form = L.once(f"form_{o}_{l}", f"form {o} {l}", lambda o=o, l=l: make_form(o, l))
            img = L.once(f"img_{o}_{l}", f"image {o}_{l}.png", lambda o=o, l=l: upload(f"{o}_{l}"))
            cr = L.once(f"cr_{o}_{l}", f"creative {name}", lambda o=o, l=l, c=c, name=name, form=form, img=img: L.creative(name, {"link_data": {
                "image_hash": img, "link": "http://fb.me/", "message": c["msg"], "name": c["head"], "description": c["desc"],
                "call_to_action": {"type": spec["cta"], "value": {"lead_gen_form_id": form}}}}))
            L.once(f"ad_{o}_{l}", f"ad {name} ({'ACTIVE' if ACTIVE else 'PAUSED'})", lambda cr=cr, name=name: meta.post(
                f"{L.ACT}/ads", adset_id=s["adset_leads"], name=name, status="ACTIVE" if ACTIVE else "PAUSED", creative={"creative_id": cr})["id"])
    print("APPLIED" if L.APPLY else "dry run, nothing created")


if __name__ == "__main__":
    main()
