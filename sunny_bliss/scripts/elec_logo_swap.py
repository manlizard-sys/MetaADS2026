"""Swaps the 4 electrical launch ads to the larger-logo images (2026-11-11): uploads the new PNGs
from build/ads/v2/elec/, builds new creatives with the same copy and form, and points the same
ads at them. Resumable through build/ids.json ("launch_v2", keys img2_/cr2_/swap2_ for ev and pn).
Usage: python3 elec_logo_swap.py --lic EC13011359 [--apply]
"""
import sys
import launch_electrical as E
import meta

L = E.L
L.APPLY = "--apply" in sys.argv


def main():
    s = L.state
    for o, spec in E.OFFERS.items():
        for l in ("en", "es"):
            c = spec[l]
            name = f"{o.upper()} · {c['head']} · {l.upper()}"
            img = L.once(f"img2_{o}_{l}", f"image {o}_{l}.png (big logo)", lambda o=o, l=l: E.upload(f"{o}_{l}"))
            cr = L.once(f"cr2_{o}_{l}", f"creative {name} (big logo)", lambda o=o, l=l, c=c, name=name, img=img: L.creative(f"{name} · big logo", {"link_data": {
                "image_hash": img, "link": "http://fb.me/", "message": c["msg"], "name": c["head"], "description": c["desc"],
                "call_to_action": {"type": spec["cta"], "value": {"lead_gen_form_id": s[f"form_{o}_{l}"]}}}}))
            L.once(f"swap2_{o}_{l}", f"ad {name} -> big logo", lambda o=o, l=l, cr=cr: (meta.post(s[f"ad_{o}_{l}"], creative={"creative_id": cr}), cr)[1])
    print("APPLIED" if L.APPLY else "dry run, nothing changed")


if __name__ == "__main__":
    main()
