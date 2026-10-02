"""Read-only: performance of current ads/creatives in the account (last 90 days, plus last 30).
Writes build/creative_performance.json and prints a ranked table by cost per Lead."""
import json, pathlib
import config as C
from meta import get_all, MetaError, BUILD

FIELDS = ("ad_id,ad_name,adset_name,campaign_name,spend,impressions,reach,frequency,clicks,inline_link_clicks,"
          "ctr,inline_link_click_ctr,cpm,actions,cost_per_action_type,video_p25_watched_actions,"
          "video_p100_watched_actions,video_thruplay_watched_actions")


def lead_count(row, key="actions"):
    for a in row.get(key, []) or []:
        if a["action_type"] in ("lead", "offsite_conversion.fb_pixel_lead"):
            return float(a["value"])
    return 0.0


def video(row, key):
    v = row.get(key) or []
    return float(v[0]["value"]) if v else 0.0


out = {}
for preset in ("last_90d", "last_30d"):
    try:
        rows = get_all(f"{C.AD_ACCOUNT}/insights", level="ad", date_preset=preset, fields=FIELDS, limit=500)
    except MetaError as e:
        print(f"API ERROR ({preset}):\n{e}")
        raise SystemExit(1)
    table = []
    for r in rows:
        spend, imp = float(r.get("spend", 0)), float(r.get("impressions", 0))
        leads = lead_count(r)
        table.append({
            "ad": r["ad_name"], "campaign": r["campaign_name"], "spend": spend, "impressions": int(imp),
            "frequency": round(float(r.get("frequency", 0)), 2), "link_ctr_%": round(float(r.get("inline_link_click_ctr", 0)), 2),
            "cpm": round(float(r.get("cpm", 0)), 2), "leads": int(leads),
            "cpl": round(spend / leads, 2) if leads else None,
            "hook_rate_%": round(100 * video(r, "video_p25_watched_actions") / imp, 1) if imp else None,
            "hold_rate_%": round(100 * video(r, "video_p100_watched_actions") / imp, 1) if imp else None,
        })
    table.sort(key=lambda x: (x["cpl"] is None, x["cpl"] or 0, -x["spend"]))
    out[preset] = table
    print(f"\n=== {preset} ===")
    print("| Anuncio | Campaña | Gasto | Leads | CPL | CTR link % | CPM | Frec. | 25% vistas/impr % | 100% vistas/impr % |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    for t in table:
        print(f"| {t['ad']} | {t['campaign']} | {t['spend']:.2f} | {t['leads']} | {t['cpl'] or '-'} | {t['link_ctr_%']} | "
              f"{t['cpm']} | {t['frequency']} | {t['hook_rate_%']} | {t['hold_rate_%']} |")
(BUILD / "creative_performance.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
