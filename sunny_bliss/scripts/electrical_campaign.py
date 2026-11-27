"""Electrical launch campaign (2026-11-11): moves the 4 electrical ads out of the services leads
ad set into their own campaign with a $500 lifetime budget (now to Nov 25, 23:59 Miami time),
same 21 ZIPs, same creatives (large logo) and forms. The 4 ads in the services ad set are paused.

Resumable through build/ids.json ("launch_v2", keys elec_*). Usage: python3 electrical_campaign.py [--apply]
"""
import sys
import launch_v2 as L
import meta, config

L.APPLY = "--apply" in sys.argv
END = "2026-11-25T23:59:00-0500"
KEYS = [f"{o}_{l}" for o in ("ev", "pn") for l in ("en", "es")]


def main():
    s = L.state
    camp = L.once("elec_camp", "campaign SB · Electrical Launch · Nov 2026", lambda: meta.post(
        f"{L.ACT}/campaigns", name="SB · Electrical Launch · Nov 2026", objective="OUTCOME_LEADS", status="ACTIVE",
        special_ad_categories=[], is_adset_budget_sharing_enabled=False, buying_type="AUCTION")["id"])
    adset = L.once("elec_adset", "ad set Electrical · 21 ZIPs · $500 lifetime to Nov 25", lambda: meta.post(
        f"{L.ACT}/adsets", campaign_id=camp, name="Electrical · 21 ZIPs · 25+ · EN+ES · $500 launch", status="ACTIVE",
        lifetime_budget=50000, end_time=END, optimization_goal="LEAD_GENERATION", billing_event="IMPRESSIONS",
        destination_type="ON_AD", bid_strategy="LOWEST_COST_WITHOUT_CAP", promoted_object={"page_id": L.PAGE},
        targeting={"age_min": 25, "geo_locations": config.zip_geo(),
                   "excluded_custom_audiences": [{"id": "120254170491030640"}],
                   "targeting_automation": {"advantage_audience": 1}})["id"])
    for k in KEYS:
        name = meta.get(s[f"ad_{k}"], fields="name")["name"] if L.APPLY else k
        L.once(f"elec_ad_{k}", f"ad {name} in launch campaign", lambda k=k, name=name: meta.post(
            f"{L.ACT}/ads", adset_id=adset, name=name, status="ACTIVE", creative={"creative_id": s[f"cr2_{k}"]})["id"])
        L.once(f"elec_paused_old_{k}", f"pause {k} in services ad set", lambda k=k: (meta.post(s[f"ad_{k}"], status="PAUSED"), "PAUSED")[1])
    print("APPLIED" if L.APPLY else "dry run, nothing changed")


if __name__ == "__main__":
    main()
