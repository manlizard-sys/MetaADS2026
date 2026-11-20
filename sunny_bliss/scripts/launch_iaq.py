"""Indoor Air Quality ads (2026-11-12), EN + ES, added to the services leads ad set (same budget).
Offer and claims come from sunnybliss.com: air test (humidity, dust, airflow), UV lights, HEPA or
media filters, whole-home dehumidifiers, duct cleaning and sealing, NATE-certified techs,
license CAC1823405, $49 service call (site banner). No health claims.

Resumable through build/ids.json ("launch_v2", keys *_iaq_*). Usage: python3 launch_iaq.py [--apply] [--active]
"""
import pathlib, sys
import launch_v2 as L
import utm_v2 as U
import meta

L.APPLY = "--apply" in sys.argv
ACTIVE = "--active" in sys.argv
IMG = pathlib.Path(__file__).resolve().parent.parent / "build" / "ads" / "v2" / "iaq"

COPY = {
  "en": {"msg": "Miami's humidity keeps dust and mold spores moving through your AC. Our Indoor Air Quality service starts with an air test (humidity, dust and airflow), then the right fix: UV lights, HEPA or media filters, whole-home dehumidifiers or duct cleaning. NATE-certified techs, license CAC1823405. Limited-time $49 service call.",
         "head": "Cleaner air at home · IAQ test", "desc": "$49 service call · Lic. CAC1823405",
         "need": ("What are you interested in?", ["Indoor air quality test", "UV light or air filtration", "Dehumidifier or humidity control", "Duct cleaning"]),
         "card": ("Indoor Air Quality for your AC", ["Air test: humidity, dust and airflow", "UV lights, HEPA or media filters", "Whole-home dehumidifiers and duct cleaning", "Limited-time $49 service call"])},
  "es": {"msg": "La humedad de Miami mueve polvo y esporas de moho por tu aire acondicionado. Nuestro servicio de calidad del aire empieza con una prueba de humedad, polvo y flujo de aire, y luego la solución correcta: luces UV, filtros HEPA o de media, deshumidificadores para toda la casa o limpieza de ductos. Técnicos certificados NATE, licencia CAC1823405. Visita de servicio de $49 por tiempo limitado.",
         "head": "Aire más limpio en casa · prueba de aire", "desc": "Visita de servicio $49 · Lic. CAC1823405",
         "need": ("¿Qué le interesa?", ["Prueba de calidad del aire", "Luz UV o filtración de aire", "Deshumidificador o control de humedad", "Limpieza de ductos"]),
         "card": ("Calidad del aire para su A/C", ["Prueba de humedad, polvo y flujo de aire", "Luces UV, filtros HEPA o de media", "Deshumidificadores y limpieza de ductos", "Visita de servicio de $49 por tiempo limitado"])},
}


def make_form(lang):
    c = COPY[lang]
    t_title, t_body, t_btn = L.THANKS[lang]
    own_label, own_opts = L.Q[lang]["own"]
    return L.page_post(f"{L.PAGE}/leadgen_forms",
        name=f"SB · IAQ · {lang.upper()} · Nov 2026", locale="en_US" if lang == "en" else "es_LA",
        is_optimized_for_quality=False,
        questions=[{"type": "CUSTOM", "key": "need", "label": c["need"][0], "options": L.opt(*c["need"][1])},
                   {"type": "CUSTOM", "key": "own", "label": own_label, "options": L.opt(*own_opts)},
                   {"type": "ZIP"}, {"type": "FULL_NAME"}, {"type": "PHONE"}],
        privacy_policy=L.PRIVACY, follow_up_action_url="https://sunnybliss.com/services/air-conditioning/indoor-air-quality/",
        tracking_parameters=U.tracking("iaq", lang),
        context_card={"title": c["card"][0], "style": "LIST_STYLE", "content": c["card"][1]},
        thank_you_page={"title": t_title, "body": t_body, "button_type": "CALL_BUSINESS",
                        "button_text": t_btn, "business_phone_number": L.PHONE, "country_code": "US"})["id"]


def upload(name):
    with open(IMG / f"{name}.png", "rb") as fh:
        r = meta.post(f"{L.ACT}/adimages", files={f"{name}.png": fh})
    return next(iter(r["images"].values()))["hash"]


def main():
    s = L.state
    for l in ("en", "es"):
        c = COPY[l]
        name = f"IAQ · {c['head']} · {l.upper()}"
        form = L.once(f"form_iaq_{l}", f"form iaq {l}", lambda l=l: make_form(l))
        img = L.once(f"img_iaq_{l}", f"image iaq_{l}.png", lambda l=l: upload(f"iaq_{l}"))
        cr = L.once(f"cr_iaq_{l}", f"creative {name}", lambda c=c, name=name, form=form, img=img: L.creative(name, {"link_data": {
            "image_hash": img, "link": "http://fb.me/", "message": c["msg"], "name": c["head"], "description": c["desc"],
            "call_to_action": {"type": "GET_QUOTE", "value": {"lead_gen_form_id": form}}}}))
        L.once(f"ad_iaq_{l}", f"ad {name} ({'ACTIVE' if ACTIVE else 'PAUSED'})", lambda cr=cr, name=name: meta.post(
            f"{L.ACT}/ads", adset_id=s["adset_leads"], name=name, status="ACTIVE" if ACTIVE else "PAUSED", creative={"creative_id": cr})["id"])
    print("APPLIED" if L.APPLY else "dry run, nothing created")


if __name__ == "__main__":
    main()
