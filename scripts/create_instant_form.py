"""Instant Form (Lead Ad form) for variant C of the landing A/B/C test (Nov 2026).

Higher-intent form on the Orchid Pros Page with the same filter question as the landing
("hire an assistant" vs "looking for a job"), prefilled name/email/phone and Orchid's privacy policy.
Uses a Page access token obtained at run time from /me/accounts (never printed or stored).
Default is a dry run; --apply creates the form (a form does nothing until an ad uses it).
"""
import json, sys, requests
from meta import get, GRAPH, MetaError, _handle, BUILD

PAGE = "1132642053254708"
FORM = {
    "name": "Orchid · Law firms · Higher intent · Test C · 2026 Nov",
    "locale": "EN_US",
    "is_optimized_for_quality": "true",  # "Higher intent": review screen before submit
    "block_display_for_non_targeted_viewer": "true",
    "questions": json.dumps([
        {"type": "CUSTOM", "key": "hire_or_job",
         "label": "Are you looking to hire an assistant for your firm, or looking for a job?",
         "options": [{"key": "hire", "value": "I want to hire an assistant"},
                     {"key": "job", "value": "I'm looking for a job"}]},
        {"type": "CUSTOM", "key": "firm_type", "label": "What type of firm do you run?",
         "options": [{"key": "immigration", "value": "Immigration law"},
                     {"key": "pi", "value": "Personal injury"},
                     {"key": "family", "value": "Family law"},
                     {"key": "other_law", "value": "Other law practice"},
                     {"key": "other", "value": "Other business"}]},
        {"type": "FULL_NAME"}, {"type": "EMAIL"}, {"type": "PHONE"},
    ]),
    "privacy_policy": json.dumps({"url": "https://orchidpros.com/privacy-policy-2/", "link_text": "Privacy Policy"}),
    "thank_you_page": json.dumps({
        "title": "Thanks! We'll reach out to book your free call.",
        "body": "Our team will contact you within one business day to schedule a 30-minute call about your firm's workload.",
        "button_type": "VIEW_WEBSITE", "button_text": "Visit Orchid Pros",
        "website_url": "https://go.orchidpros.com/hire"}),
    "follow_up_action_url": "https://go.orchidpros.com/hire",
}

for k in ("name", "questions", "thank_you_page"):
    print(f"{k}: {FORM[k][:300]}")
if "--apply" not in sys.argv:
    sys.exit("\nVista previa. Nada cambió. Ejecuta con --apply para crear el formulario.")

page_token = next(p["access_token"] for p in get("me/accounts", fields="id,access_token")["data"] if p["id"] == PAGE)
hdr = {"Authorization": f"Bearer {page_token}"}
r = _handle(requests.post(f"{GRAPH}/{PAGE}/leadgen_forms", headers=hdr, data=FORM, timeout=60))
form = _handle(requests.get(f"{GRAPH}/{r['id']}", headers=hdr, params={"fields": "id,name,status,locale,questions"}, timeout=60))
print(f"Formulario creado: {form['name']} · id {form['id']} · {form['status']}")
(BUILD / "instant-form-test-c.json").write_text(json.dumps({"form_id": form["id"], "name": form["name"]}, indent=2, ensure_ascii=False))
