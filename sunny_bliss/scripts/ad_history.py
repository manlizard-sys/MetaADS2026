import sys, json
sys.path.insert(0, "/home/user/MetaADS2026/sunny_bliss/scripts")
import meta, config
rows = meta.get_all(f"{config.AD_ACCOUNT if hasattr(config,'AD_ACCOUNT') else 'act_406803358900425'}/insights",
    level="ad", time_range=json.dumps({"since":"2025-11-01","until":"2026-11-04"}),
    fields="campaign_name,adset_name,ad_name,ad_id,spend,impressions,clicks,ctr,actions,frequency",
    limit=500)
out=[]
for r in rows:
    if any(k in (r["campaign_name"]+r["ad_name"]).lower() for k in ("hiring","tech ","technician","plumber wanted")): continue
    acts={a["action_type"]:float(a["value"]) for a in r.get("actions",[])}
    leads=acts.get("lead") or acts.get("offsite_conversion.fb_pixel_lead") or acts.get("onsite_conversion.lead_grouped") or 0
    sp=float(r["spend"])
    out.append(dict(c=r["campaign_name"],a=r["ad_name"],id=r["ad_id"],spend=sp,leads=leads,cpl=round(sp/leads,2) if leads else None,ctr=round(float(r.get("ctr",0)),2)))
out.sort(key=lambda x:(-(x["leads"]), x["cpl"] or 9e9))
for o in out[:40]: print(o)
print(len(out), "ads; total spend", round(sum(o["spend"] for o in out)), "leads", sum(o["leads"] for o in out))
json.dump(out, open("/home/user/MetaADS2026/sunny_bliss/build/reports/ad_history.json","w"), indent=1)
