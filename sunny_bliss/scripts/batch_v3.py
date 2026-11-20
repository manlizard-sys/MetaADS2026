"""Batch of 2026-11-16 (moved up from Nov 19 by the user):

1. Placements: services and electrical leads ad sets drop Audience Network, Facebook Reels overlay
   ads and in-stream video ($151 spent there, 0 leads). Kept: Facebook and Instagram feeds, Stories,
   Reels, Marketplace, Search.
2. Creatives: the 8 services ads (tune-up, Silver, new AC, tank flush; EN + ES) move to the official
   brand format (KickCharge colors, large logo band), add "For Miami-Dade homeowners" in image and
   text, and show the license (CAC1823405 / CFC1433145). Same ads, same short forms (GHL mapped).

Resumable through build/ids.json ("launch_v2", keys v3*). Usage: python3 batch_v3.py [--apply]
"""
import pathlib, sys
import launch_v2 as L
import meta

L.APPLY = "--apply" in sys.argv
IMG = pathlib.Path(__file__).resolve().parent.parent / "build" / "ads" / "v3"
PLACEMENTS = {"publisher_platforms": ["facebook", "instagram"],
              "facebook_positions": ["feed", "marketplace", "story", "facebook_reels", "search"],
              "instagram_positions": ["stream", "story", "reels"],
              "device_platforms": ["mobile", "desktop"]}
WHO = {"en": "For Miami-Dade homeowners: ", "es": "Para dueños de casa en Miami-Dade: "}
LIC = {"tu": "CAC1823405", "si": "CAC1823405", "ac": "CAC1823405", "fl": "CFC1433145"}


def set_placements(adset_id):
    tg = meta.get(adset_id, fields="targeting")["targeting"]
    tg.update(PLACEMENTS)
    meta.post(adset_id, targeting=tg)
    return "OK"


def upload(name):
    with open(IMG / f"{name}.png", "rb") as fh:
        r = meta.post(f"{L.ACT}/adimages", files={f"v3_{name}.png": fh})
    return next(iter(r["images"].values()))["hash"]


def main():
    s = L.state
    for key in ("adset_leads", "elec_adset"):
        L.once(f"v3place_{key}", f"placements on {key}", lambda key=key: set_placements(s[key]))
    for o, spec in L.OFFERS.items():
        for l in ("en", "es"):
            c = spec[l]
            name = f"{o.upper()} · {c['head']} · {l.upper()}"
            msg = WHO[l] + c["msg"][0].lower() + c["msg"][1:]
            desc = f"{c['desc']} · Lic. {LIC[o]}"
            img = L.once(f"v3img_{o}_{l}", f"image v3 {o}_{l}.png", lambda o=o, l=l: upload(f"{o}_{l}"))
            cr = L.once(f"v3cr_{o}_{l}", f"creative {name} (official format)", lambda o=o, l=l, c=c, name=name, img=img, msg=msg, desc=desc: L.creative(f"{name} · v3 official", {"link_data": {
                "image_hash": img, "link": "http://fb.me/", "message": msg, "name": c["head"], "description": desc,
                "call_to_action": {"type": spec["cta"], "value": {"lead_gen_form_id": s[f"form3_{o}_{l}"]}}}}))
            L.once(f"v3swap_{o}_{l}", f"ad {name} -> v3", lambda o=o, l=l, cr=cr: (meta.post(s[f"ad_{o}_{l}"], creative={"creative_id": cr}), cr)[1])
    print("APPLIED" if L.APPLY else "dry run, nothing changed")


if __name__ == "__main__":
    main()
