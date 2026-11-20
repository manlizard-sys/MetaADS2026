"""Scroll-stopper concepts (2026-11-20, approved by the user): 8 new ads, EN + ES.

- Iguana + water heater flush (services ad set), iguana + EV charger (electrical launch ad set).
- Thanksgiving + water heater flush and Thanksgiving + AC tune-up (services ad set); to be paused
  on Nov 26 at night.
Each ad uses placement asset customization: 9:16 image in Stories/Reels, 4:5 in feeds. v5 forms
(305-239-4987), CTA BOOK_TRAVEL ("Book now"). Images: build/ads/c6.

Resumable through build/ids.json ("launch_v2", keys c6*). Usage: python3 c6_publish.py [--apply]
"""
import pathlib, sys
import launch_v2 as L
import meta

L.APPLY = "--apply" in sys.argv
IMG = pathlib.Path(__file__).resolve().parent.parent / "build" / "ads" / "c6"
CALL = {"en": "Call 305-239-4987 or tap Book now.", "es": "Llama al 305-239-4987 o toca Reserva ya."}

ADS = {
  "ig_fl": {"form": "fl", "adset": "adset_leads", "en": {
      "name": "IG · FL · Cold shower again? · EN",
      "msg": "Cold shower again? Sediment builds up in Miami water heaters and steals your hot water. Our water heater flush is $149 (reg. $279), with same-day appointments and licensed plumbers (Lic. CFC1433145).",
      "head": "Water heater flush $149", "desc": "Same-day appointments · Lic. CFC1433145"},
    "es": {
      "name": "IG · FL · ¿Otra vez agua fría? · ES",
      "msg": "¿Otra vez agua fría? El sedimento se acumula en los calentadores de Miami y te roba el agua caliente. La limpieza del calentador cuesta $149 (antes $279), con citas el mismo día y plomeros con licencia (Lic. CFC1433145).",
      "head": "Limpieza del calentador $149", "desc": "Citas el mismo día · Lic. CFC1433145"}},
  "ig_ev": {"form": "ev", "adset": "elec_adset", "en": {
      "name": "IG · EV · Charge it at home · EN",
      "msg": "Got an EV? Stop hunting for chargers. We install Level 2 home chargers with a panel check included, by licensed electricians (Lic. EC13011359). Launch offer: $200 off.",
      "head": "EV charger install: $200 off", "desc": "New electrical service · Lic. EC13011359"},
    "es": {
      "name": "IG · EV · Cárgalo en casa · ES",
      "msg": "¿Tienes auto eléctrico? Deja de buscar dónde cargarlo. Instalamos cargadores Nivel 2 en casa con revisión del panel incluida, con electricistas con licencia (Lic. EC13011359). Oferta de lanzamiento: $200 menos.",
      "head": "Cargador para auto eléctrico: $200 menos", "desc": "Nuevo servicio eléctrico · Lic. EC13011359"}},
  "tg_fl": {"form": "fl", "adset": "adset_leads", "en": {
      "name": "TG · FL · Hosting Thanksgiving? · EN",
      "msg": "Hosting Thanksgiving? A full house means more showers, more dishes and more hot water. Get your water heater flushed before Nov 26: $149 (reg. $279), same-day appointments, licensed plumbers (Lic. CFC1433145).",
      "head": "Thanksgiving-ready: water heater flush $149", "desc": "Same-day appointments · Lic. CFC1433145"},
    "es": {
      "name": "TG · FL · ¿Visita en Thanksgiving? · ES",
      "msg": "¿Recibes visita en Thanksgiving? Casa llena es más duchas, más platos y más agua caliente. Limpia tu calentador antes del 26: $149 (antes $279), citas el mismo día y plomeros con licencia (Lic. CFC1433145).",
      "head": "Listo para Thanksgiving: limpieza del calentador $149", "desc": "Citas el mismo día · Lic. CFC1433145"}},
  "tg_tu": {"form": "tu", "adset": "adset_leads", "en": {
      "name": "TG · TU · Full house for Thanksgiving? · EN",
      "msg": "Full house for Thanksgiving? Keep everyone cool. For Miami-Dade homeowners: our team checks your AC before the guests arrive, with coil and drain line cleaning and a refrigerant and wiring check. AC tune-up $129 (reg. $325), Lic. CAC1823405.",
      "head": "Thanksgiving-ready: AC tune-up $129", "desc": "Regular price $325 · Lic. CAC1823405"},
    "es": {
      "name": "TG · TU · ¿Casa llena en Thanksgiving? · ES",
      "msg": "¿Casa llena en Thanksgiving? Que todos estén frescos. Para dueños de casa en Miami-Dade: revisamos tu aire antes de que lleguen, con limpieza de serpentín y drenaje y revisión de refrigerante y cableado. Mantenimiento de A/C $129 (antes $325), Lic. CAC1823405.",
      "head": "Listo para Thanksgiving: mantenimiento de A/C $129", "desc": "Precio regular $325 · Lic. CAC1823405"}},
}


def upload(name):
    with open(IMG / f"{name}.png", "rb") as fh:
        r = meta.post(f"{L.ACT}/adimages", files={f"c6_{name}.png": fh})
    return next(iter(r["images"].values()))["hash"]


def creative(c, form, h45, h916, lang):
    afs = {"images": [{"hash": h45, "adlabels": [{"name": "r45"}]}, {"hash": h916, "adlabels": [{"name": "r916"}]}],
           "bodies": [{"text": f"{c['msg']}\n\n{CALL[lang]}"}], "titles": [{"text": c["head"]}],
           "descriptions": [{"text": c["desc"]}], "link_urls": [{"website_url": "http://fb.me/"}],
           "call_to_action_types": ["BOOK_TRAVEL"], "ad_formats": ["SINGLE_IMAGE"],
           "call_to_actions": [{"type": "BOOK_TRAVEL", "value": {"lead_gen_form_id": form}}],
           "asset_customization_rules": [
               {"customization_spec": {"publisher_platforms": ["facebook", "instagram"], "facebook_positions": ["story", "facebook_reels"],
                                       "instagram_positions": ["story", "reels"]}, "image_label": {"name": "r916"}, "priority": 1},
               {"customization_spec": {"publisher_platforms": ["facebook", "instagram"], "facebook_positions": ["feed", "marketplace", "search"],
                                       "instagram_positions": ["stream"]}, "image_label": {"name": "r45"}, "priority": 2}]}
    return meta.post(f"{L.ACT}/adcreatives", name=c["name"], object_story_spec={"page_id": L.PAGE, "instagram_user_id": L.IG},
                     asset_feed_spec=afs)["id"]


def main():
    s = L.state
    for k, spec in ADS.items():
        for l in ("en", "es"):
            c = spec[l]
            h45 = L.once(f"c6img_{k}_{l}_45", f"image {k}_{l}_4x5", lambda k=k, l=l: upload(f"{k}_{l}_4x5"))
            h916 = L.once(f"c6img_{k}_{l}_916", f"image {k}_{l}_9x16", lambda k=k, l=l: upload(f"{k}_{l}_9x16"))
            form = s[f"form5_{spec['form']}_{l}"]
            cr = L.once(f"c6cr_{k}_{l}", f"creative {c['name']}", lambda c=c, form=form, h45=h45, h916=h916, l=l: creative(c, form, h45, h916, l))
            L.once(f"c6ad_{k}_{l}", f"ad {c['name']} (ACTIVE)", lambda c=c, cr=cr, spec=spec: meta.post(
                f"{L.ACT}/ads", adset_id=s[spec["adset"]], name=c["name"], status="ACTIVE", creative={"creative_id": cr})["id"])
    print("APPLIED" if L.APPLY else "dry run, nothing created")


if __name__ == "__main__":
    main()
