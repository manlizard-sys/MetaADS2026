"""EV ads move into the services leads ad set (2026-11-25, approved by the user) as the electrical
launch campaign ends tonight. Reuses the paused EV ads already in the services ad set (no new ads),
swapped to the v5 creatives (305-239-4987, v5 forms), and adds the iguana EV ads (EN + ES).
Panel ads stay paused (no leads since Nov 11); they come back with the January promo.

Resumable through build/ids.json ("launch_v2", keys evsv_*). Usage: python3 ev_to_services.py [--apply]
"""
import sys
import launch_v2 as L
import meta

L.APPLY = "--apply" in sys.argv


def main():
    s = L.state
    for l in ("en", "es"):
        ad = s[f"ad_ev_{l}"]
        L.once(f"evsv_swap_{l}", f"services EV {l}: v5 creative", lambda ad=ad, l=l: (meta.post(ad, creative={"creative_id": s[f"v5cr_ev_{l}"]}), s[f"v5cr_ev_{l}"])[1])
        L.once(f"evsv_active_{l}", f"services EV {l}: ACTIVE", lambda ad=ad: (meta.post(ad, status="ACTIVE"), "ACTIVE")[1])
        name = {"en": "IG · EV · Charge it at home · EN", "es": "IG · EV · Cárgalo en casa · ES"}[l]
        L.once(f"evsv_ig_{l}", f"services ad {name}", lambda l=l, name=name: meta.post(
            f"{L.ACT}/ads", adset_id=s["adset_leads"], name=name, status="ACTIVE", creative={"creative_id": s[f"c6cr_ig_ev_{l}"]})["id"])
    print("APPLIED" if L.APPLY else "dry run, nothing changed")


if __name__ == "__main__":
    main()
