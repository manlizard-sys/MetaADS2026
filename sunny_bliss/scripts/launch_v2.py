"""Sunny Bliss launch v2 (Nov 2026): Andromeda-style structure, everything created PAUSED.

- Leads (80%): one broad ad set in the 21 ZIP codes, 4 offers x EN/ES = 8 ads, each with its own
  Higher Intent instant form (so the form tells GHL which ad brought the lead).
- Awareness (20%): one reach ad set, 2 concepts x EN/ES = 4 ads.
- Archives the two earlier paused campaigns from launch_nov2026.py (never ran).

Resumable: every created ID is stored in build/ids.json under "launch_v2" and reused on a re-run.
The page token is fetched at run time and never printed or written anywhere.
Usage: python3 launch_v2.py [--apply]
"""
import json, sys, time, pathlib, requests
import meta, config

APPLY = "--apply" in sys.argv
ACT, PAGE, IG = config.AD_ACCOUNT, config.PAGE_ID, config.INSTAGRAM_USER_ID
IMG = pathlib.Path(__file__).resolve().parent.parent / "build" / "ads" / "v2"
IDS_FILE = meta.BUILD / "ids.json"
LEADS_BUDGET, AWARE_BUDGET = 5300, 1300          # cents/day: $53 + $13 = $66/day, about $2,000/month
PHONE = "+13057076081"                           # same call button as the existing forms
PRIVACY = {"url": "https://sunnybliss.com/text-messaging-policy", "link_text": "Privacy policy"}
OLD_CAMPAIGNS = ["120254881047350640", "120254881060300640"]


def opt(*vals):
    return [{"value": v, "key": f"o{i}"} for i, v in enumerate(vals)]


Q = {
    "en": {"own": ("Do you own the home?", ["Yes, I own it", "No, I rent"]),
           "when": ("When do you want the service?", ["This week", "This month", "Just researching"]),
           "age": ("How old is your AC?", ["Under 10 years", "10 to 15 years", "Over 15 years", "Not sure"])},
    "es": {"own": ("¿Es dueño de la casa?", ["Sí, soy dueño", "No, alquilo"]),
           "when": ("¿Cuándo quiere el servicio?", ["Esta semana", "Este mes", "Solo estoy averiguando"]),
           "age": ("¿Cuántos años tiene su aire?", ["Menos de 10 años", "10 a 15 años", "Más de 15 años", "No sé"])},
}

THANKS = {"en": ("Thanks! We'll call you shortly", "A Sunny Bliss team member will call you in the next few minutes to book your visit.", "Call now"),
          "es": ("¡Gracias! Te llamamos en unos minutos", "Alguien del equipo de Sunny Bliss te llamará en los próximos minutos para agendar tu visita.", "Llamar ahora")}

# offer -> language -> copy, form need-question and context card
OFFERS = {
  "tu": {"cta": "GET_QUOTE", "extra_q": None,
    "en": {"msg": "Winter is the best time to service your AC. Our $129 tune-up (reg. $325) cleans the coils and drain line, checks refrigerant and wiring, and tells you how many years your system has left. Family-run since 1990, 4.9 on Google.",
           "head": "Winter AC Tune-Up $129", "desc": "Regular price $325",
           "need": ("What do you need?", ["AC tune-up $129", "AC not cooling or repair", "Silver Maintenance Plan", "Other"]),
           "card": ("Winter AC Tune-Up $129", ["Regular price $325", "Coil and drain line cleaning", "Refrigerant and wiring check", "Licensed, family-run since 1990"])},
    "es": {"msg": "El invierno es el mejor momento para darle mantenimiento a tu aire. Nuestro mantenimiento de $129 (antes $325) limpia el serpentín y el drenaje, revisa el refrigerante y el cableado, y te dice cuántos años le quedan a tu equipo. Empresa familiar desde 1990, 4.9 en Google.",
           "head": "Mantenimiento de A/C $129", "desc": "Precio regular $325",
           "need": ("¿Qué necesita?", ["Mantenimiento de A/C $129", "El aire no enfría o reparación", "Plan de Mantenimiento Silver", "Otro"]),
           "card": ("Mantenimiento de A/C $129", ["Precio regular $325", "Limpieza de serpentín y drenaje", "Revisión de refrigerante y cableado", "Con licencia, empresa familiar desde 1990"])}},
  "si": {"cta": "SIGN_UP", "extra_q": None,
    "en": {"msg": "Special promotion: 50% off the Silver Maintenance Plan. $150 a year (reg. $300) covers two AC tune-ups, one plumbing visit, no dispatch fee and 10% off repairs.",
           "head": "Silver Plan 50% off: $150/yr", "desc": "Regular price $300/yr",
           "need": ("What are you interested in?", ["Silver Plan $150/yr", "AC tune-up $129", "AC repair", "Other"]),
           "card": ("Silver Maintenance Plan, 50% off", ["$150 a year (reg. $300)", "Two AC tune-ups a year", "One plumbing visit", "No dispatch fee, 10% off repairs"])},
    "es": {"msg": "Promoción especial: 50% de descuento en el Plan de Mantenimiento Silver. Por $150 al año (antes $300) tienes dos mantenimientos de A/C, una visita de plomería, sin cargo por visita y 10% menos en reparaciones.",
           "head": "Plan Silver a mitad de precio: $150/año", "desc": "Precio regular $300/año",
           "need": ("¿Qué le interesa?", ["Plan Silver $150/año", "Mantenimiento de A/C $129", "Reparación de A/C", "Otro"]),
           "card": ("Plan de Mantenimiento Silver, 50% de descuento", ["$150 al año (antes $300)", "Dos mantenimientos de A/C al año", "Una visita de plomería", "Sin cargo por visita, 10% menos en reparaciones"])}},
  "ac": {"cta": "GET_QUOTE", "extra_q": "age",
    "en": {"msg": "Replace your AC before it fails. New systems from $5,800 for a limited time, with 0% interest for 60 months on approved credit. Flat-rate price before we start, licensed installers, permits included.",
           "head": "New AC from $5,800 · 0% for 60 months", "desc": "Limited time · with approved credit",
           "need": ("What do you need?", ["Replace my AC", "Second opinion on a quote", "AC repair", "Other"]),
           "card": ("New AC from $5,800", ["Limited-time offer", "0% interest for 60 months, with approved credit", "Flat-rate price before we start", "Licensed installers, permits included"])},
    "es": {"msg": "Cambia tu aire antes de que falle. Equipos nuevos desde $5,800 por tiempo limitado, con 0% de interés por 60 meses sujeto a aprobación de crédito. Precio fijo antes de empezar, instaladores con licencia y permisos incluidos.",
           "head": "Aire nuevo desde $5,800 · 0% por 60 meses", "desc": "Por tiempo limitado · sujeto a aprobación",
           "need": ("¿Qué necesita?", ["Cambiar mi aire", "Segunda opinión de una cotización", "Reparación de A/C", "Otro"]),
           "card": ("Aire nuevo desde $5,800", ["Oferta por tiempo limitado", "0% de interés por 60 meses, sujeto a aprobación de crédito", "Precio fijo antes de empezar", "Instaladores con licencia, permisos incluidos"])}},
  "fl": {"cta": "GET_QUOTE", "extra_q": None,
    "en": {"msg": "Miami's hard water leaves sediment at the bottom of every tank. A flush brings your hot water back and adds years to the heater. $149 (reg. $279), same-day appointments.",
           "head": "Water heater flush $149", "desc": "Regular price $279",
           "need": ("What do you need?", ["Tank water heater flush $149", "Tankless descale $289", "Water heater repair or replacement", "Other plumbing"]),
           "card": ("Water heater flush $149", ["Regular price $279", "Tankless descale $289", "Same-day appointments", "Licensed plumbers since 1990"])},
    "es": {"msg": "El agua dura de Miami deja sedimento en el fondo de cada calentador. Una limpieza te devuelve el agua caliente y le suma años al equipo. $149 (antes $279), citas el mismo día.",
           "head": "Limpieza del calentador $149", "desc": "Precio regular $279",
           "need": ("¿Qué necesita?", ["Limpieza de calentador de tanque $149", "Calentador sin tanque $289", "Reparación o cambio de calentador", "Otra plomería"]),
           "card": ("Limpieza del calentador $149", ["Precio regular $279", "Calentador sin tanque $289", "Citas el mismo día", "Plomeros con licencia desde 1990"])}},
}

AWARE = {
  "a1": {"en": ("Homeowners across Coral Gables, Pinecrest, Kendall and Miami Beach rate us 4.9 on Google, with more than 1,000 reviews. Family-run since 1990, AC and plumbing, no overtime charges.", "Miami's 4.9-star home team"),
         "es": ("Familias de Coral Gables, Pinecrest, Kendall y Miami Beach nos califican con 4.9 en Google, con más de 1,000 reseñas. Empresa familiar desde 1990, aire acondicionado y plomería, sin cargos por horas extra.", "El equipo 4.9 estrellas de Miami")},
  "a2": {"en": ("1,000+ five-star reviews from Miami homeowners. When your AC or plumbing needs help, call the family-run team Miami has trusted since 1990.", "1,000+ five-star reviews"),
         "es": ("Más de 1,000 reseñas de 5 estrellas de familias en Miami. Cuando tu aire o tu plomería necesiten ayuda, llama al equipo familiar en el que Miami confía desde 1990.", "Más de 1,000 reseñas de 5 estrellas")},
}

ids = json.loads(IDS_FILE.read_text()) if IDS_FILE.exists() else {}
state = ids.setdefault("launch_v2", {})


def save():
    if APPLY:
        IDS_FILE.write_text(json.dumps(ids, indent=2, ensure_ascii=False))


def once(key, label, fn):
    """Create once; reuse the stored ID on later runs."""
    if key in state:
        print(f"  = {label}: {state[key]}")
        return state[key]
    print(f"  + {label}")
    if not APPLY:
        return f"<{key}>"
    state[key] = fn()
    save()
    time.sleep(1.5)
    return state[key]


def page_post(path, **params):
    pt = meta.get(PAGE, fields="access_token")["access_token"]
    data = {k: (json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else v) for k, v in params.items()}
    r = requests.post(f"{meta.GRAPH}/{path}", data=data, headers={"Authorization": f"Bearer {pt}"}, timeout=60).json()
    if "error" in r:
        raise meta.MetaError(meta.scrub(json.dumps({k: r["error"].get(k) for k in ("message", "code", "error_subcode", "error_user_msg")}, ensure_ascii=False)).replace(pt, "***"))
    return r


def form_questions(offer, lang):
    o, q = OFFERS[offer], Q[lang]
    need_label, need_opts = o[lang]["need"]
    qs = [{"type": "CUSTOM", "key": "need", "label": need_label, "options": opt(*need_opts)}]
    if o["extra_q"]:
        lbl, opts = q[o["extra_q"]]
        qs.append({"type": "CUSTOM", "key": o["extra_q"], "label": lbl, "options": opt(*opts)})
    for k in ("own", "when"):
        lbl, opts = q[k]
        qs.append({"type": "CUSTOM", "key": k, "label": lbl, "options": opt(*opts)})
    return qs + [{"type": "ZIP"}, {"type": "FULL_NAME"}, {"type": "PHONE"}, {"type": "EMAIL"}]


def make_form(offer, lang):
    c = OFFERS[offer][lang]
    t_title, t_body, t_btn = THANKS[lang]
    return page_post(f"{PAGE}/leadgen_forms",
        name=f"SB · {offer.upper()} · {lang.upper()} · Nov 2026 v2",
        locale="en_US" if lang == "en" else "es_LA",
        is_optimized_for_quality=True,
        questions=form_questions(offer, lang),
        privacy_policy=PRIVACY,
        follow_up_action_url="https://sunnybliss.com/",
        context_card={"title": c["card"][0], "style": "LIST_STYLE", "content": c["card"][1]},
        thank_you_page={"title": t_title, "body": t_body, "button_type": "CALL_BUSINESS",
                        "button_text": t_btn, "business_phone_number": PHONE, "country_code": "US"})["id"]


def upload(name):
    with open(IMG / f"{name}.png", "rb") as fh:
        r = meta.post(f"{ACT}/adimages", files={f"{name}.png": fh})
    return next(iter(r["images"].values()))["hash"]


def creative(name, story):
    return meta.post(f"{ACT}/adcreatives", name=name, object_story_spec={"page_id": PAGE, "instagram_user_id": IG, **story})["id"]


def main():
    config.require() if hasattr(config, "require") else None
    geo = config.zip_geo()
    excl = [{"id": "120254170491030640"}]            # SB – Lead Form Submitted – 90d

    print("FORMS (Higher Intent, one per offer and language)")
    forms = {f"{o}_{l}": once(f"form_{o}_{l}", f"form {o} {l}", lambda o=o, l=l: make_form(o, l)) for o in OFFERS for l in ("en", "es")}

    print("IMAGES")
    hashes = {n: once(f"img_{n}", f"image {n}.png", lambda n=n: upload(n)) for n in [f"{k}_{l}" for k in list(OFFERS) + list(AWARE) for l in ("en", "es")]}

    print("CAMPAIGNS AND AD SETS (PAUSED)")
    c_leads = once("camp_leads", "campaign SB · Leads · Nov 2026 v2", lambda: meta.post(f"{ACT}/campaigns", name="SB · Leads · Nov 2026 v2", objective="OUTCOME_LEADS", status="PAUSED", special_ad_categories=[], is_adset_budget_sharing_enabled=False, buying_type="AUCTION")["id"])
    c_aware = once("camp_aware", "campaign SB · Awareness · Reviews · Nov 2026 v2", lambda: meta.post(f"{ACT}/campaigns", name="SB · Awareness · Reviews · Nov 2026 v2", objective="OUTCOME_AWARENESS", status="PAUSED", special_ad_categories=[], is_adset_budget_sharing_enabled=False, buying_type="AUCTION")["id"])
    s_leads = once("adset_leads", f"ad set Leads · 21 ZIPs · broad · ${LEADS_BUDGET/100:.0f}/day", lambda: meta.post(f"{ACT}/adsets", campaign_id=c_leads, name="Leads · 21 ZIPs · broad 25+ · EN+ES · Higher Intent", status="PAUSED",
        daily_budget=LEADS_BUDGET, optimization_goal="LEAD_GENERATION", billing_event="IMPRESSIONS", destination_type="ON_AD", bid_strategy="LOWEST_COST_WITHOUT_CAP",
        promoted_object={"page_id": PAGE}, targeting={"age_min": 25, "geo_locations": geo, "excluded_custom_audiences": excl, "targeting_automation": {"advantage_audience": 1}})["id"])
    s_aware = once("adset_aware", f"ad set Awareness · 21 ZIPs · ${AWARE_BUDGET/100:.0f}/day", lambda: meta.post(f"{ACT}/adsets", campaign_id=c_aware, name="Awareness · 21 ZIPs · 25+ · EN+ES", status="PAUSED",
        daily_budget=AWARE_BUDGET, optimization_goal="REACH", billing_event="IMPRESSIONS", bid_strategy="LOWEST_COST_WITHOUT_CAP",
        promoted_object={"page_id": PAGE}, targeting={"age_min": 25, "geo_locations": geo, "targeting_automation": {"advantage_audience": 0}})["id"])

    print("LEAD ADS (PAUSED)")
    for o, spec in OFFERS.items():
        for l in ("en", "es"):
            c = spec[l]
            name = f"{o.upper()} · {c['head']} · {l.upper()}"
            cr = once(f"cr_{o}_{l}", f"creative {name}", lambda o=o, l=l, c=c, name=name: creative(name, {"link_data": {
                "image_hash": hashes[f"{o}_{l}"], "link": "http://fb.me/", "message": c["msg"], "name": c["head"], "description": c["desc"],
                "call_to_action": {"type": spec["cta"], "value": {"lead_gen_form_id": forms[f"{o}_{l}"]}}}}))
            once(f"ad_{o}_{l}", f"ad {name}", lambda cr=cr, name=name: meta.post(f"{ACT}/ads", adset_id=s_leads, name=name, status="PAUSED", creative={"creative_id": cr})["id"])

    print("AWARENESS ADS (PAUSED)")
    for a, spec in AWARE.items():
        for l in ("en", "es"):
            msg, head = spec[l]
            name = f"{a.upper()} · {head} · {l.upper()}"
            cr = once(f"cr_{a}_{l}", f"creative {name}", lambda a=a, l=l, msg=msg, head=head, name=name: creative(name, {"link_data": {
                "image_hash": hashes[f"{a}_{l}"], "link": "https://sunnybliss.com/", "message": msg, "name": head,
                "call_to_action": {"type": "LEARN_MORE", "value": {"link": "https://sunnybliss.com/"}}}}))
            once(f"ad_{a}_{l}", f"ad {name}", lambda cr=cr, name=name: meta.post(f"{ACT}/ads", adset_id=s_aware, name=name, status="PAUSED", creative={"creative_id": cr})["id"])

    print("ARCHIVE the earlier paused campaigns (never ran)")
    for cid in OLD_CAMPAIGNS:
        once(f"archived_{cid}", f"archive {cid}", lambda cid=cid: (meta.post(cid, status="ARCHIVED"), "ARCHIVED")[1])

    print(f"\nTotal ${(LEADS_BUDGET + AWARE_BUDGET)/100:.0f}/day (leads ${LEADS_BUDGET/100:.0f}, awareness ${AWARE_BUDGET/100:.0f}) · {'APPLIED, all PAUSED' if APPLY else 'dry run, nothing created'}")


if __name__ == "__main__":
    main()
