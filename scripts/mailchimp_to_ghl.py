"""One-time migration: Mailchimp audiences -> GHL contacts.

Each Mailchimp member becomes (or updates) a GHL contact, matched by email:
- tag `mc-<audience>` (e.g. mc-attorneys, mc-real-estate, mc-hiring-colombia) plus its Mailchimp tags as `mc-<tag>`;
- `subscribed` -> marketable; `unsubscribed` / `cleaned` / `pending` / `transactional` -> email DND on in GHL
  and tag `mc-baja`, so nobody who left Mailchimp gets marketing from GHL;
- `archived` members are skipped.
Existing GHL tags are kept (tags are added, never replaced).

Dry run by default: lists audiences and counts only. Writes only with --apply.
Never prints names, emails or phones. Needs GHL_TOKEN, GHL_LOCATION_ID, MAILCHIMP_API_KEY.
Usage: python3 mailchimp_to_ghl.py [--apply] [--only "ORCHID for Attorneys"]
"""
import collections, os, pathlib, re, sys, time
import requests

ROOT = pathlib.Path(__file__).resolve().parent.parent
GHL_API = "https://services.leadconnectorhq.com"
NOT_MARKETABLE = {"unsubscribed", "cleaned", "pending", "transactional"}


def env(name):
    f = ROOT / ".env"
    if f.exists():
        for line in f.read_text(encoding="utf-8-sig").splitlines():
            if line.startswith(name + "="):
                return line.split("=", 1)[1].strip()
    return os.environ.get(name, "").strip() or sys.exit(f"{name} missing (.env or environment variable)")


GHL_TOKEN, LOCATION, MC_KEY = env("GHL_TOKEN"), env("GHL_LOCATION_ID"), env("MAILCHIMP_API_KEY")
MC_API = f"https://{MC_KEY.rsplit('-', 1)[-1]}.api.mailchimp.com/3.0"
ghl = requests.Session()
ghl.headers.update({"Authorization": f"Bearer {GHL_TOKEN}", "Version": "2021-07-28", "Accept": "application/json"})
mc = requests.Session()
mc.auth = ("orchid", MC_KEY)


def scrub(text):
    return str(text).replace(GHL_TOKEN, "***").replace(MC_KEY, "***")


def call(session, method, url, **kw):
    try:
        r = session.request(method, url, timeout=60, **kw)
    except requests.RequestException as e:
        sys.exit(scrub(f"{method} {url}: {e}"))
    if r.status_code == 429:
        time.sleep(10)
        r = session.request(method, url, timeout=60, **kw)
    if r.status_code >= 400:
        sys.exit(scrub(f"{method} {url}: HTTP {r.status_code} {r.text[:400]}"))
    return r.json() if r.content else {}


def slug(text):
    s = re.sub(r"^orchid\s+(for\s+)?", "", text.strip(), flags=re.I)
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def audiences():
    data = call(mc, "GET", f"{MC_API}/lists", params={"count": 100, "fields": "lists.id,lists.name,lists.stats.member_count"})
    return data.get("lists") or []


def members(list_id):
    out, offset = [], 0
    while True:
        data = call(mc, "GET", f"{MC_API}/lists/{list_id}/members", params={
            "count": 1000, "offset": offset,
            "fields": "members.email_address,members.status,members.merge_fields,members.tags,total_items"})
        out += data.get("members") or []
        offset += 1000
        if offset >= data.get("total_items", 0):
            return out


def main():
    apply = "--apply" in sys.argv
    only = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else None
    lists = [a for a in audiences() if not only or a["name"] == only]
    plan = []
    for a in lists:
        ms = members(a["id"])
        counts = collections.Counter(m["status"] for m in ms)
        print(f"{a['name']} -> tag mc-{slug(a['name'])}: {len(ms)} members {dict(counts)}")
        for m in ms:
            if m["status"] != "archived":
                plan.append((a, m))
    emails = collections.Counter(m["email_address"].lower() for _, m in plan)
    print(f"Total to import: {len(plan)} rows, {len(emails)} unique emails "
          f"({sum(1 for c in emails.values() if c > 1)} in more than one audience)")
    print(f"Email DND (not marketable): {sum(1 for _, m in plan if m['status'] in NOT_MARKETABLE)}")
    if not apply:
        print("Dry run: nothing written. Run with --apply to import.")
        return

    done = bad_phones = shared_phones = 0
    for a, m in plan:
        mf = m.get("merge_fields") or {}
        body = {"locationId": LOCATION, "email": m["email_address"], "source": "Mailchimp import"}
        if mf.get("FNAME"):
            body["firstName"] = mf["FNAME"]
        if mf.get("LNAME"):
            body["lastName"] = mf["LNAME"]
        company = next((v for k, v in mf.items() if "COMPANY" in k.upper() and isinstance(v, str) and v), "")
        if company:
            body["companyName"] = company
        if isinstance(mf.get("PHONE"), str) and mf["PHONE"].strip():
            # GHL matches contacts by email OR phone: a phone already used by another contact
            # (e.g. a firm's main line) would merge this person into it and overwrite its email.
            dup = call(ghl, "GET", GHL_API + "/contacts/search/duplicate",
                       params={"locationId": LOCATION, "number": mf["PHONE"].strip()}).get("contact")
            if not dup or (dup.get("email") or "").lower() == m["email_address"].lower():
                body["phone"] = mf["PHONE"].strip()
            else:
                shared_phones += 1
        if m["status"] in NOT_MARKETABLE:
            body["dndSettings"] = {"Email": {"status": "active", "message": f"Mailchimp: {m['status']}"}}
        r = ghl.post(GHL_API + "/contacts/upsert", json=body, timeout=60) if "phone" in body else None
        if r is not None and r.status_code == 400 and "phone" in r.text.lower():
            body.pop("phone")  # GHL rejects malformed Mailchimp phones; import the contact without it
            bad_phones += 1
            r = None
        contact = ((r.json() if r is not None and r.ok else None)
                   or call(ghl, "POST", GHL_API + "/contacts/upsert", json=body)).get("contact") or {}
        if (contact.get("email") or "").lower() != m["email_address"].lower():
            sys.exit(f"Stopped at row {done + 1}: GHL returned a different contact (merge). Nothing else written.")
        tags = [f"mc-{slug(a['name'])}"] + [f"mc-{slug(t['name'])}" for t in m.get("tags") or []]
        if m["status"] in NOT_MARKETABLE:
            tags.append("mc-baja")
        call(ghl, "POST", GHL_API + f"/contacts/{contact['id']}/tags", json={"tags": tags})
        done += 1
        if done % 100 == 0:
            print(f"{done}/{len(plan)}")
        time.sleep(0.25)  # GHL limit: 100 requests / 10 s per location
    print(f"Imported {done} rows ({bad_phones} without phone: GHL rejected the Mailchimp value; "
          f"{shared_phones} without phone: number already used by another contact).")


if __name__ == "__main__":
    main()
