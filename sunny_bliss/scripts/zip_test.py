"""Nearby-ZIP test (2026-11-25, approved by Mehdi through the user): new campaign, $10/day, 2 weeks.

8 ZIPs next to Mehdi's 21 (which stay untouched in the main campaign):
33154 Surfside/Bal Harbour, 33137 Upper East Side/Design District, 33129 The Roads/Brickell,
33165 Westchester, 33175 West Kendall, 33183 Kendall Lakes, 33177 South Miami Heights, 33161 North Miami.
Same setup as the main leads ad set: 25+, Advantage+ audience, past leads excluded, same placements,
v5 forms (305-239-4987). Ads reuse the best current creatives (water heater flush v5, iguana flush,
AC tune-up v5; EN + ES). Ends 2026-12-09 23:59 Miami time.

Resumable through build/ids.json ("launch_v2", keys zt_*). Usage: python3 zip_test.py [--apply]
"""
import sys
import launch_v2 as L
import meta

L.APPLY = "--apply" in sys.argv
ZIPS = ["33154", "33137", "33129", "33165", "33175", "33183", "33177", "33161"]
END = "2026-12-09T23:59:00-0500"
PLACEMENTS = {"publisher_platforms": ["facebook", "instagram"],
              "facebook_positions": ["feed", "marketplace", "story", "facebook_reels", "search"],
              "instagram_positions": ["stream", "story", "reels"],
              "device_platforms": ["mobile", "desktop"]}
ADS = [  # (key, creative key in ids.json, ad name)
    ("fl_es", "v5cr_fl_es", "ZT · FL · Limpieza del calentador $149 · ES"),
    ("fl_en", "v5cr_fl_en", "ZT · FL · Water heater flush $149 · EN"),
    ("igfl_es", "c6cr_ig_fl_es", "ZT · IG · FL · ¿Otra vez agua fría? · ES"),
    ("igfl_en", "c6cr_ig_fl_en", "ZT · IG · FL · Cold shower again? · EN"),
    ("tu_es", "v5cr_tu_es", "ZT · TU · Mantenimiento de A/C $129 · ES"),
    ("tu_en", "v5cr_tu_en", "ZT · TU · Winter AC Tune-Up $129 · EN"),
]


def main():
    s = L.state
    camp = L.once("zt_camp", "campaign SB · ZIP Test · Nearby ZIPs · Nov 2026", lambda: meta.post(
        f"{L.ACT}/campaigns", name="SB · ZIP Test · Nearby ZIPs · Nov 2026", objective="OUTCOME_LEADS", status="ACTIVE",
        special_ad_categories=[], is_adset_budget_sharing_enabled=False, buying_type="AUCTION")["id"])
    adset = L.once("zt_adset", "ad set 8 nearby ZIPs · $10/day to Dec 9", lambda: meta.post(
        f"{L.ACT}/adsets", campaign_id=camp, name="ZIP Test · 8 nearby ZIPs · 25+ · EN+ES · $10/day", status="ACTIVE",
        daily_budget=1000, end_time=END, optimization_goal="LEAD_GENERATION", billing_event="IMPRESSIONS",
        destination_type="ON_AD", bid_strategy="LOWEST_COST_WITHOUT_CAP", promoted_object={"page_id": L.PAGE},
        targeting={"age_min": 25, "geo_locations": {"zips": [{"key": f"US:{z}"} for z in ZIPS]},
                   "excluded_custom_audiences": [{"id": "120254170491030640"}],
                   "targeting_automation": {"advantage_audience": 1}, **PLACEMENTS})["id"])
    for k, cr, name in ADS:
        L.once(f"zt_ad_{k}", f"ad {name}", lambda cr=cr, name=name: meta.post(
            f"{L.ACT}/ads", adset_id=adset, name=name, status="ACTIVE", creative={"creative_id": s[cr]})["id"])
    print("APPLIED" if L.APPLY else "dry run, nothing created")


if __name__ == "__main__":
    main()
