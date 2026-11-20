"""Re-frames the water heater photo strip on the 2 tank flush ads (2026-11-16): the strip now shows
the hands on the heater and the Sunny Bliss shirt logo instead of a half-cut face. Same copy and forms.
Resumable through build/ids.json ("launch_v2", keys v3b*). Usage: python3 fl_photo_fix.py [--apply]
"""
import sys
import launch_v2 as L
import batch_v3 as B
import meta

L.APPLY = "--apply" in sys.argv


def main():
    s = L.state
    for l in ("en", "es"):
        c = L.OFFERS["fl"][l]
        name = f"FL · {c['head']} · {l.upper()}"
        msg = B.WHO[l] + c["msg"][0].lower() + c["msg"][1:]
        desc = f"{c['desc']} · Lic. {B.LIC['fl']}"
        img = L.once(f"v3bimg_fl_{l}", f"image fl_{l} reframed", lambda l=l: B.upload(f"fl_{l}"))
        cr = L.once(f"v3bcr_fl_{l}", f"creative {name} (reframed photo)", lambda c=c, name=name, img=img, msg=msg, desc=desc, l=l: L.creative(f"{name} · v3b photo", {"link_data": {
            "image_hash": img, "link": "http://fb.me/", "message": msg, "name": c["head"], "description": desc,
            "call_to_action": {"type": "GET_QUOTE", "value": {"lead_gen_form_id": s[f"form3_fl_{l}"]}}}}))
        L.once(f"v3bswap_fl_{l}", f"ad {name} -> reframed", lambda l=l, cr=cr: (meta.post(s[f"ad_fl_{l}"], creative={"creative_id": cr}), cr)[1])
    print("APPLIED" if L.APPLY else "dry run, nothing changed")


if __name__ == "__main__":
    main()
