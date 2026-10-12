"""Swap the ad copy of V1, V2 and S8 for copy v3 (build/copy_v3.md), approved 2026-10-12.

Each ad gets a new creative that copies its current one (video/image, link, UTMs, placement
rules, enhancement settings) and replaces only the texts. All three creatives are created
first; ads are switched only if every creative was created. Old creative ids are saved to
build/backup-<today>-copy-v2-creatives.json.
Default is a dry run. Usage: python3 apply_copy_v3.py [--apply]
"""
import copy, datetime, json, sys
from meta import get, get_all, post, BUILD, MetaError

ACT = "act_1806647434085082"
FIELDS = ("name,object_story_spec,asset_feed_spec,url_tags,degrees_of_freedom_spec,"
          "contextual_multi_ads,call_to_action_type")
CTA = "\n\n👇 Book a free 30-min call."

COPY = {
    "V2 Small Law Firm - 2026 Oct": {
        "bodies": [
            "Law firm owners: ready to hire a bilingual virtual assistant? ⚖️\n\n"
            "Orchid places trained legal assistants and paralegals from Colombia in your firm, "
            "on your U.S. hours: intake, calendar, case files and client updates." + CTA,
            "POV: your \"small\" law firm runs on 19 roles and 3 people ⚖️\n\n"
            "Hire a virtual legal assistant who takes intake, scheduling and paperwork off your desk. "
            "Bilingual, vetted, U.S. hours.\n\nFor attorneys and firm owners. 👇 Book a free 30-min call.",
            "Hiring help for your law firm? ⚖️\n\n"
            "Client intake ✅ Calendar ✅ Follow-ups ✅ Immigration forms ✅\n\n"
            "A bilingual legal assistant who joins your team. Not the right fit? "
            "We replace them at no cost." + CTA,
        ],
        "titles": ["Hire a Legal Assistant for Your Firm", "For Law Firm Owners", "Virtual Paralegal, U.S. Hours"],
    },
    "V1 POV Email - 2026 Oct": {
        "bodies": [
            "POV: you hired a virtual assistant, and every email gets answered while you're on the putting green ⛳\n\n"
            "For business owners ready to delegate: a bilingual assistant on your U.S. hours." + CTA,
            "Business owners: your inbox, calendar and follow-ups, handled ✅\n\n"
            "Hire a vetted, bilingual virtual assistant who joins your team on U.S. hours. "
            "Plans from $1,000/month." + CTA,
            "Ready to hire your first virtual assistant?\n\n"
            "Emails answered. Calls returned. Calendar under control. ⏰\n\n"
            "English and Spanish, your U.S. hours, and a free replacement if it's not the right fit." + CTA,
        ],
        "titles": ["Hire Your Virtual Assistant", "For Owners Ready to Delegate", "Your Inbox, Handled ✅"],
    },
    "S8 Comparison - Static - 2026 Oct": {
        "message": (
            "Thinking about hiring another employee? Compare first 👇\n\n"
            "Local hire vs. an Orchid virtual assistant:\n"
            "✅ Up to 60% less cost, payroll and HR included\n"
            "✅ Matched in about 20 business days\n"
            "✅ Free replacement if it's not the right fit\n"
            "✅ Cancel within the first 30 days at no cost\n"
            "✅ English + Spanish, on your U.S. hours\n\n"
            "For business owners. 👉 Book a free 30-min call."),
        "name": "Local Hire vs. Virtual Assistant",
    },
}


def new_spec(old, texts):
    c = copy.deepcopy(old)
    for k in ("id", "call_to_action_type"):
        c.pop(k, None)
    feats = (c.get("degrees_of_freedom_spec") or {}).get("creative_features_spec", {})
    for k in ("standard_enhancements", "advantage_plus_creative"):  # deprecated umbrella flags
        feats.pop(k, None)
    vd = (c.get("object_story_spec") or {}).get("video_data")
    if vd and vd.get("image_hash"):
        vd.pop("image_url", None)  # send the hash only
    afs = c.get("asset_feed_spec")
    if "bodies" in texts:
        # Keep each asset's placement labels; replace only the words.
        for kind in ("bodies", "titles"):
            olds = afs[kind]
            labels = olds[0].get("adlabels")
            afs[kind] = [{"text": t, **({"adlabels": labels} if labels else {})} for t in texts[kind]]
        for v in afs.get("videos", []):
            v.pop("thumbnail_url", None) if v.get("thumbnail_hash") else None
    else:
        ld = c["object_story_spec"]["link_data"]
        ld["message"], ld["name"] = texts["message"], texts["name"]
    c["name"] = f"copy v3 · {datetime.date.today().isoformat()} · {old['name'][:60]}"
    return c


apply = "--apply" in sys.argv
ads = {a["name"]: a for a in get_all(f"{ACT}/ads", fields="id,name,status,creative{id}", limit=100)}
plan = []
for ad_name, texts in COPY.items():
    ad = ads[ad_name]
    old = get(ad["creative"]["id"], fields=FIELDS)
    plan.append((ad, old, new_spec(old, texts)))
    shown = texts.get("bodies", [texts.get("message")])
    print(f"{ad_name} ({ad['status']}), creativo actual {old['id']}")
    for t in shown:
        print("   ·", t.splitlines()[0])

if not apply:
    print("\nVista previa. Nada cambió. Ejecuta con --apply para publicar.")
    sys.exit(0)

stamp = datetime.date.today().isoformat()
(BUILD / f"backup-{stamp}-copy-v2-creatives.json").write_text(json.dumps(
    {ad["name"]: {"ad_id": ad["id"], "creative_id": old["id"]} for ad, old, _ in plan}, indent=2), encoding="utf-8")

created = []
for ad, old, spec in plan:
    try:
        r = post(f"{ACT}/adcreatives", **spec)
        created.append((ad, r["id"]))
        print(f"Creativo nuevo para {ad['name']}: {r['id']}")
    except MetaError as e:
        sys.exit(f"Falló el creativo de {ad['name']}; no se cambió ningún anuncio.\n{e}")

for ad, cid in created:
    try:
        post(ad["id"], creative={"creative_id": cid})
        print(f"{ad['name']}: usa el copy v3")
    except MetaError as e:
        print(f"ERROR al cambiar {ad['name']}: {e}")
