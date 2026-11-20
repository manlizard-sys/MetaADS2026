"""Compares instant-form leads in Meta with contacts in GoHighLevel and lists the leads that never
reached GHL, so the team can call them. Read-only on both sides.

Personal data (names, phones) is printed to the terminal only; nothing is written to disk.
Usage: python3 reconcile_leads.py [--since 2026-10-01]
"""
import datetime as dt, json, re, sys, requests
import meta, config

SINCE = sys.argv[sys.argv.index("--since") + 1] if "--since" in sys.argv else "2026-10-01"
GHL = "https://services.leadconnectorhq.com"
GHL_H = {"Authorization": "Bearer proxy-injected", "Version": "2021-07-28", "Accept": "application/json"}
LOC = "FWSYVq6jT5aL8WUhVV5E"


def digits(p):
    d = re.sub(r"\D", "", p or "")
    return d[-10:] if len(d) >= 10 else d


def ghl_contacts():
    out, after = [], None
    while True:
        body = {"locationId": LOC, "pageLimit": 100, **({"searchAfter": after} if after else {})}
        r = requests.post(f"{GHL}/contacts/search", json=body, headers=GHL_H, timeout=30)
        r.raise_for_status()
        page = r.json()["contacts"]
        out += page
        if len(page) < 100:
            return out
        after = page[-1]["searchAfter"]


def main():
    pt = meta.get(config.PAGE_ID, fields="access_token")["access_token"]
    H = {"Authorization": f"Bearer {pt}"}
    # Listing the page's forms needs a page token, which this environment's proxy replaces, so the
    # forms come from the account's customer ads (hiring excluded) plus the ones in build/ids.json.
    ids = json.loads((meta.BUILD / "ids.json").read_text()).get("launch_v2", {})
    form_ids = {v: k for k, v in ids.items() if k.startswith("form")}
    # Customer forms used Sep-Oct 2026 (found earlier in the account's creatives).
    for fid, name in {"1706144103786572": "Plumbing EN Sep 24", "1042561781716942": "AC 0% 60m ES",
                      "2492686487841896": "AC 0% 60m EN", "1554567089328909": "25-year-old AC EN",
                      "1689115782782234": "AC install $5,800 ES"}.items():
        form_ids.setdefault(fid, name)
    for ad in meta.get_all(f"{config.AD_ACCOUNT}/ads", fields="name,campaign{name},creative{object_story_spec,asset_feed_spec}", limit=200):
        if any(h in ad.get("campaign", {}).get("name", "").lower() for h in config.HIRING_KEYWORDS):
            continue
        for fid in set(re.findall(r'lead_gen_form_id\\?"?:\\?\s*"?(\d+)', json.dumps(ad.get("creative", {})))):
            form_ids.setdefault(fid, ad["name"])
    forms = {"data": [{"id": fid, "name": name} for fid, name in form_ids.items()]}
    since_ts = int(dt.datetime.fromisoformat(SINCE).replace(tzinfo=dt.timezone.utc).timestamp())
    leads = []
    for f in forms.get("data", []):
        url = f"{meta.GRAPH}/{f['id']}/leads"
        params = {"fields": "created_time,ad_name,field_data", "limit": 100}
        while url:
            r = requests.get(url, headers=H, params=params, timeout=60).json()
            if "error" in r:
                print(f"  ! {f['name']}: {r['error'].get('message')}")
                break
            for l in r.get("data", []):
                if dt.datetime.fromisoformat(l["created_time"].replace("+0000", "+00:00")).timestamp() < since_ts:
                    continue
                fd = {x["name"]: (x.get("values") or [""])[0] for x in l.get("field_data", [])}
                leads.append({"time": l["created_time"][:16].replace("T", " "), "form": f["name"], "ad": l.get("ad_name", ""),
                              "name": fd.get("full_name") or " ".join(filter(None, [fd.get("first_name"), fd.get("last_name")])),
                              "phone": fd.get("phone_number", ""), "email": (fd.get("email") or "").lower(), "zip": fd.get("zip_code") or fd.get("zip") or fd.get("zip_typed", "")})
            url, params = r.get("paging", {}).get("next"), None

    contacts = ghl_contacts()
    phones = {digits(c.get("phone")) for c in contacts if c.get("phone")}
    emails = {(c.get("email") or "").lower() for c in contacts if c.get("email")}
    missing = [l for l in leads if digits(l["phone"]) not in phones and (not l["email"] or l["email"] not in emails)]

    print(f"Meta leads since {SINCE}: {len(leads)} · in GHL: {len(leads) - len(missing)} · MISSING in GHL: {len(missing)}")
    for l in sorted(missing, key=lambda x: x["time"], reverse=True):
        print(f"  {l['time']} UTC · {l['name']} · {l['phone']} · ZIP {l['zip']} · {l['ad'] or l['form']}")


if __name__ == "__main__":
    main()
