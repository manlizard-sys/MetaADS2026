"""Daily GHL <-> Mailchimp sync for the weekly newsletter.

1. GHL -> Mailchimp: contacts tagged `newsletter` (and not `job-seeker` / `newsletter-baja`)
   are added to the Mailchimp audience with tag `ghl-lead`.
2. Unsubscribes, both ways: unsubscribed in Mailchimp -> GHL tag `newsletter-baja` and
   `newsletter` removed; GHL contact with `newsletter-baja` -> unsubscribed in Mailchimp.
3. Newsletter clicks on the booking link (`/book`) without an appointment -> GHL tag
   `newsletter-clic`, which starts the follow-up workflow in GHL.

Dry run by default: prints counts only. Writes only with --apply.
Never prints names, emails or phones; tokens are read from .env or the environment.
Needs GHL_TOKEN, GHL_LOCATION_ID, MAILCHIMP_API_KEY, MAILCHIMP_AUDIENCE_ID.
Usage: python3 mailchimp_sync.py [--apply] [--days 14]
"""
import datetime as dt, hashlib, os, pathlib, sys
import requests

ROOT = pathlib.Path(__file__).resolve().parent.parent
GHL_API = "https://services.leadconnectorhq.com"
TAG_IN, TAG_OUT, TAG_CLICK, TAG_EXCLUDE = "newsletter", "newsletter-baja", "newsletter-clic", "job-seeker"
BOOK_PATH = "/book"


def env(name):
    f = ROOT / ".env"
    if f.exists():
        for line in f.read_text(encoding="utf-8-sig").splitlines():
            if line.startswith(name + "="):
                return line.split("=", 1)[1].strip()
    return os.environ.get(name, "").strip() or sys.exit(f"{name} missing (.env or environment variable)")


GHL_TOKEN, LOCATION = env("GHL_TOKEN"), env("GHL_LOCATION_ID")
MC_KEY, AUDIENCE = env("MAILCHIMP_API_KEY"), env("MAILCHIMP_AUDIENCE_ID")
MC_API = f"https://{MC_KEY.rsplit('-', 1)[-1]}.api.mailchimp.com/3.0"
SECRETS = (GHL_TOKEN, MC_KEY)

ghl = requests.Session()
ghl.headers.update({"Authorization": f"Bearer {GHL_TOKEN}", "Version": "2021-07-28", "Accept": "application/json"})
mc = requests.Session()
mc.auth = ("orchid", MC_KEY)


def scrub(text):
    for s in SECRETS:
        text = str(text).replace(s, "***")
    return text


def call(session, method, url, **kw):
    try:
        r = session.request(method, url, timeout=60, **kw)
    except requests.RequestException as e:
        sys.exit(scrub(f"{method} {url}: {e}"))
    if r.status_code >= 400:
        sys.exit(scrub(f"{method} {url}: HTTP {r.status_code} {r.text[:400]}"))
    return r.json() if r.content else {}


def email_hash(email):
    return hashlib.md5(email.strip().lower().encode()).hexdigest()


def ghl_contacts_with_tag(tag):
    out, page = [], 1
    while True:
        data = call(ghl, "POST", GHL_API + "/contacts/search", json={
            "locationId": LOCATION, "page": page, "pageLimit": 100,
            "filters": [{"field": "tags", "operator": "contains", "value": tag}]})
        batch = data.get("contacts") or []
        out += batch
        if len(batch) < 100:
            return out
        page += 1


def ghl_find(email):
    data = call(ghl, "GET", GHL_API + "/contacts/search/duplicate", params={"locationId": LOCATION, "email": email})
    return data.get("contact")


def ghl_has_appointment_since(contact_id, since):
    data = call(ghl, "GET", GHL_API + f"/contacts/{contact_id}/appointments")
    for ev in data.get("events") or []:
        added = ev.get("dateAdded") or ev.get("startTime") or ""
        if added[:10] >= since.date().isoformat():
            return True
    return False


def mc_members(status, since):
    out, offset = [], 0
    while True:
        data = call(mc, "GET", f"{MC_API}/lists/{AUDIENCE}/members", params={
            "status": status, "since_last_changed": since.isoformat(), "count": 500, "offset": offset,
            "fields": "members.email_address,members.status,total_items"})
        out += data.get("members") or []
        offset += 500
        if offset >= data.get("total_items", 0):
            return out


def mc_book_clickers(since):
    """Emails that clicked a /book link in campaigns sent since `since`."""
    data = call(mc, "GET", f"{MC_API}/campaigns", params={
        "list_id": AUDIENCE, "status": "sent", "since_send_time": since.isoformat(), "count": 50,
        "fields": "campaigns.id"})
    clicked = set()
    for c in data.get("campaigns") or []:
        offset = 0
        while True:
            act = call(mc, "GET", f"{MC_API}/reports/{c['id']}/email-activity", params={
                "count": 500, "offset": offset, "fields": "emails.email_address,emails.activity,total_items"})
            for e in act.get("emails") or []:
                if any(a.get("action") == "click" and BOOK_PATH in (a.get("url") or "") for a in e.get("activity") or []):
                    clicked.add(e["email_address"].lower())
            offset += 500
            if offset >= act.get("total_items", 0):
                break
    return clicked


def main():
    apply = "--apply" in sys.argv
    days = int(sys.argv[sys.argv.index("--days") + 1]) if "--days" in sys.argv else 14
    since = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=days)
    plan = {"to_mailchimp": [], "unsub_in_mailchimp": [], "baja_in_ghl": [], "clic_in_ghl": []}

    # 1. GHL -> Mailchimp (new opted-in leads)
    for c in ghl_contacts_with_tag(TAG_IN):
        tags = set(c.get("tags") or [])
        if c.get("email") and not tags & {TAG_EXCLUDE, TAG_OUT}:
            plan["to_mailchimp"].append(c)

    # 2a. GHL baja -> Mailchimp unsubscribed
    for c in ghl_contacts_with_tag(TAG_OUT):
        if c.get("email"):
            plan["unsub_in_mailchimp"].append(c)

    # 2b. Mailchimp unsubscribed/cleaned -> GHL baja
    for m in mc_members("unsubscribed", since) + mc_members("cleaned", since):
        c = ghl_find(m["email_address"])
        if c and TAG_OUT not in (c.get("tags") or []):
            plan["baja_in_ghl"].append(c)

    # 3. Clicked /book, no appointment since -> GHL newsletter-clic
    for email in mc_book_clickers(since):
        c = ghl_find(email)
        if c and not {TAG_CLICK, TAG_OUT} & set(c.get("tags") or []) and not ghl_has_appointment_since(c["id"], since):
            plan["clic_in_ghl"].append(c)

    for k, v in plan.items():
        print(f"{k}: {len(v)}")
    if not apply:
        print("Dry run: nothing written. Run with --apply to sync.")
        return

    for c in plan["to_mailchimp"]:
        call(mc, "PUT", f"{MC_API}/lists/{AUDIENCE}/members/{email_hash(c['email'])}", json={
            "email_address": c["email"], "status_if_new": "subscribed",
            "merge_fields": {"FNAME": c.get("firstName") or "", "LNAME": c.get("lastName") or ""}})
        call(mc, "POST", f"{MC_API}/lists/{AUDIENCE}/members/{email_hash(c['email'])}/tags",
             json={"tags": [{"name": "ghl-lead", "status": "active"}]})
    for c in plan["unsub_in_mailchimp"]:
        h = email_hash(c["email"])
        r = mc.get(f"{MC_API}/lists/{AUDIENCE}/members/{h}", params={"fields": "status"}, timeout=60)
        if r.status_code == 200 and r.json().get("status") == "subscribed":
            call(mc, "PATCH", f"{MC_API}/lists/{AUDIENCE}/members/{h}", json={"status": "unsubscribed"})
    for c in plan["baja_in_ghl"]:
        call(ghl, "POST", GHL_API + f"/contacts/{c['id']}/tags", json={"tags": [TAG_OUT]})
        call(ghl, "DELETE", GHL_API + f"/contacts/{c['id']}/tags", json={"tags": [TAG_IN]})
    for c in plan["clic_in_ghl"]:
        call(ghl, "POST", GHL_API + f"/contacts/{c['id']}/tags", json={"tags": [TAG_CLICK]})
    print("Applied.")


if __name__ == "__main__":
    main()
