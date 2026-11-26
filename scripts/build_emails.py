"""Builds Orchid's GHL automation emails from one shared layout.
Output: build/emails/orchid/{_layout.html, 01..10-*.html, 05-...-sin-oferta.html, index.html}
Rules (BRIEF.md): fragment starting at <table>, inline styles only, tables, no <style>/<head>/classes, no em dashes,
Georgia headlines + Arial body, 600px max, GHL merge fields from merge-fields.md only.
Usage: python3 scripts/build_emails.py"""
import html, pathlib, re

OUT = pathlib.Path(__file__).resolve().parent.parent / "build" / "emails" / "orchid"
LOGO = "https://orchidpros.com/wp-content/uploads/2026/01/cropped-cropped-LOGO_WHITE-scaled-1.png"
# Dirección legal confirmada por Manuel (26 nov 2026): siempre el P.O. Box.
BOOK_URL = "https://api.leadconnectorhq.com/widget/booking/739uffEjsGH7PH0Zaovn"  # public link of "Orchid - Discovery Call"
ADDRESS = "N3XUS, LLC d/b/a ORCHID, P.O. Box 463, Rutherford, NJ 07070"

C = dict(bg="#F3F0FA", card="#FFFFFF", violet="#3F1D83", ink="#1C1233", body="#4A4460", muted="#6B6485",
         yellow="#FFC857", line="#ECE8F7", foot="#1C1233", foottxt="#D9D3F0", lilac="#EDEEFF", green="#34B36A")
F_HEAD = "Georgia,'Times New Roman',serif"
F_BODY = "Arial,Helvetica,sans-serif"


def p(text, size=16, lh=24, color=None, pad="0 36px 18px 36px", bold=False, align="left"):
    return (f'<tr><td align="{align}" style="padding:{pad};font-family:{F_BODY};font-size:{size}px;line-height:{lh}px;'
            f'color:{color or C["body"]};{"font-weight:bold;" if bold else ""}"><p style="margin:0;">{text}</p></td></tr>')


def details(rows):
    cells = []
    for i, (label, value) in enumerate(rows):
        last = i == len(rows) - 1
        cells.append(f'<tr><td style="padding:{"18px" if i == 0 else "0"} 20px 6px 20px;font-family:{F_BODY};font-size:13px;line-height:16px;color:{C["muted"]};">{label}</td></tr>')
        cells.append(f'<tr><td style="padding:0 20px {"18px" if last else "14px"} 20px;font-family:{F_BODY};font-size:16px;line-height:22px;color:{C["ink"]};font-weight:bold;">{value}</td></tr>')
    return (f'<tr><td style="padding:4px 36px 22px 36px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" '
            f'style="background-color:{C["bg"]};border-left:4px solid {C["yellow"]};border-radius:8px;">{"".join(cells)}</table></td></tr>')


def callout(title, text):
    return (f'<tr><td style="padding:4px 36px 22px 36px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" '
            f'style="background-color:{C["lilac"]};border-radius:12px;"><tr><td style="padding:18px 20px;font-family:{F_BODY};font-size:15px;line-height:23px;color:{C["body"]};">'
            f'<p style="margin:0 0 4px 0;font-family:{F_HEAD};font-size:18px;line-height:24px;color:{C["violet"]};font-weight:bold;">{title}</p>'
            f'<p style="margin:0;">{text}</p></td></tr></table></td></tr>')


def button(label, href, pad="8px 36px 8px 36px"):
    return (f'<tr><td align="left" style="padding:{pad};"><a href="{href}" target="_blank" '
            f'style="display:inline-block;background-color:{C["yellow"]};color:{C["ink"]};font-family:{F_BODY};font-size:15px;'
            f'font-weight:bold;line-height:20px;text-decoration:none;padding:13px 26px;border-radius:999px;">{label}</a></td></tr>')


def link_line(before, label, href):
    return p(f'{before} <a href="{href}" target="_blank" style="color:{C["violet"]};text-decoration:underline;">{label}</a>',
             size=14, lh=20, color=C["muted"], pad="10px 36px 26px 36px")


def checklist(title, items):
    rows = "".join(f'<tr><td valign="top" width="24" style="padding:0 0 8px 0;font-family:{F_BODY};font-size:15px;line-height:22px;color:{C["green"]};font-weight:bold;">&#10003;</td>'
                   f'<td style="padding:0 0 8px 0;font-family:{F_BODY};font-size:15px;line-height:22px;color:{C["body"]};">{t}</td></tr>' for t in items)
    return (f'<tr><td style="padding:0 36px 22px 36px;"><p style="margin:0 0 10px 0;font-family:{F_BODY};font-size:15px;line-height:20px;color:{C["violet"]};font-weight:bold;">{title}</p>'
            f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0">{rows}</table></td></tr>')


def signature(closing, name, sub="Orchid"):
    return (f'<tr><td style="padding:0 36px 34px 36px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="border-top:1px solid {C["line"]};">'
            f'<tr><td style="padding:22px 0 0 0;font-family:{F_BODY};font-size:16px;line-height:24px;color:{C["body"]};"><p style="margin:0;">{closing}</p>'
            f'<p style="margin:4px 0 0 0;font-family:{F_HEAD};font-size:18px;line-height:24px;color:{C["ink"]};">{name}</p>'
            f'<p style="margin:0;font-family:{F_BODY};font-size:14px;line-height:20px;color:{C["muted"]};">{sub}</p></td></tr></table></td></tr>')


def layout(tag, headline, body_rows, preheader=""):
    pre = (f'<div style="display:none;max-height:0;overflow:hidden;mso-hide:all;font-size:1px;line-height:1px;color:{C["bg"]};">{preheader}</div>'
           if preheader else "")
    return (f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:{C["bg"]};margin:0;padding:0;">'
            f'<tr><td align="center" style="padding:32px 12px;">{pre}'
            f'<table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="width:100%;max-width:600px;background-color:{C["card"]};border-radius:14px;overflow:hidden;">'
            # header: logo + yellow tag + white headline on violet
            f'<tr><td align="left" bgcolor="{C["violet"]}" style="background-color:{C["violet"]};padding:28px 36px 0 36px;">'
            f'<img src="{LOGO}" width="120" alt="Orchid" style="display:block;width:120px;height:auto;border:0;"></td></tr>'
            f'<tr><td align="left" bgcolor="{C["violet"]}" style="background-color:{C["violet"]};padding:22px 36px 0 36px;">'
            f'<span style="display:inline-block;background-color:{C["yellow"]};color:{C["violet"]};font-family:{F_HEAD};font-style:italic;font-weight:bold;font-size:14px;line-height:18px;padding:6px 14px;border-radius:14px;">{tag}</span></td></tr>'
            f'<tr><td align="left" bgcolor="{C["violet"]}" style="background-color:{C["violet"]};padding:14px 36px 32px 36px;font-family:{F_HEAD};font-size:28px;line-height:34px;color:#FFFFFF;font-weight:bold;">'
            f'<p style="margin:0;">{headline}</p></td></tr>'
            f'<tr><td style="padding:30px 0 0 0;font-size:0;line-height:0;">&nbsp;</td></tr>'
            f'{"".join(body_rows)}'
            f'<tr><td align="center" bgcolor="{C["foot"]}" style="background-color:{C["foot"]};padding:20px 36px;font-family:{F_BODY};font-size:12px;line-height:18px;color:{C["foottxt"]};">'
            f'<p style="margin:0;">Operational excellence powered by human warmth.</p>'
            f'<p style="margin:4px 0 0 0;">{ADDRESS}</p>'
            f'<p style="margin:4px 0 0 0;"><a href="https://orchidpros.com" target="_blank" style="color:#FFFFFF;text-decoration:underline;">orchidpros.com</a></p>'
            f'</td></tr></table></td></tr></table>')


WHEN = "{{appointment.start_time}} ({{appointment.timezone}})"
WHERE = '<a href="{{appointment.meeting_location}}" target="_blank" style="color:#1C1233;text-decoration:underline;">Google Meet: join from this link</a>'
WITH = "Andrea Bolanos, Orchid"
CALL_DESC = "On the call, Andrea will learn about your workload and the tasks you want to delegate, and explain how Orchid matches you with a bilingual professional from Colombia."

EMAILS = {
    "01-email-descarte": dict(tag="Thanks for reaching out", headline="Thanks for your interest in Orchid, {{contact.first_name}}.", pre="Our careers page is the right place for you.", rows=[
        p("The form you filled out is for businesses looking to hire an Orchid professional."),
        callout("Looking to work with Orchid?", "We're always glad to meet bilingual professionals in Colombia. Apply through our careers page and our talent team will review your application."),
        button("Apply to work with Orchid", "TODO_URL_CAREERS"),
        p("Thank you again for thinking of us.", pad="18px 36px 22px 36px"),
        signature("Best regards,", "The Orchid Team", "orchidpros.com")]),
    "02-email-bienvenida": dict(tag="Request received", headline="We got your request, {{contact.first_name}}.", pre="Here's how to book your discovery call with Orchid.", rows=[
        p("Thanks for reaching out to Orchid. If you already booked a discovery call, your confirmation is in a separate email and we'll talk then."),
        callout("Haven't booked yet?", "Pick a time that works for you. On the call, Andrea will learn about your workload and explain how Orchid matches you with a bilingual professional from Colombia."),
        button("Book my free call", BOOK_URL),
        p("Otherwise, I'll reach out within one business day to learn more about your team and the role you're looking to fill.", pad="18px 36px 22px 36px"),
        signature("Warmly,", "Andrea Bolanos")]),
    "04-email-cita-cancelada": dict(tag="About your call", headline="About your call request, {{contact.first_name}}.", pre="An update on the appointment you booked.", rows=[
        p("Thanks for booking time with us. Our discovery calls are for businesses in the United States looking to hire an Orchid professional, so we've canceled this appointment."),
        callout("Looking to work with Orchid?", "If you're a bilingual professional in Colombia, you can apply through our careers page and our talent team will review your application."),
        button("Apply to work with Orchid", "TODO_URL_CAREERS"),
        p("If you believe this was a mistake, just reply to this email and we'll take a look.", pad="18px 36px 22px 36px"),
        signature("Best regards,", "The Orchid Team", "orchidpros.com")]),
    "05-bienvenida-delegate-brief": dict(tag="The Delegate Brief", headline="Welcome to The Delegate Brief, {{contact.first_name}}.", pre="One task worth delegating, every other week.", rows=[
        p("Thanks for subscribing. Every other week you'll get one task worth delegating, a ready-to-use template and the real numbers behind it. It takes 3 minutes to read."),
        "<!-- OFERTA: borrar después del 1 dic -->",
        callout("While you're here: Black Friday", "Get started free with a bilingual professional from Colombia, then 50% off your first month. The offer runs until December 1st."),
        button("Book a free call", "https://go.orchidpros.com/business-free-month"),
        "<!-- /OFERTA -->",
        p("&nbsp;", size=4, lh=4, pad="10px 36px 0 36px"),
        signature("Talk soon,", "Josu&eacute; &amp; Andrea")]),
    "06-cal-reserva-sin-confirmar": dict(tag="Request received", headline="We got your call request, {{contact.first_name}}.", pre="We'll confirm your discovery call shortly.", rows=[
        p("Thanks for choosing a time with Orchid. We've received your request and will confirm it shortly."),
        details([("Requested time", WHEN), ("Where", WHERE)]),
        p(CALL_DESC),
        button("Choose a different time", "{{appointment.reschedule_link}}"),
        link_line("Can't make it?", "Cancel your request.", "{{appointment.cancellation_link}}"),
        signature("Talk soon,", "Andrea Bolanos")]),
    "07-cal-reserva-confirmada": dict(tag="Your call is booked", headline="You're booked, {{contact.first_name}}.", pre="Your discovery call details are inside.", rows=[
        p("Your discovery call with Orchid is confirmed. Here are the details."),
        details([("When", WHEN), ("Where", WHERE), ("With", WITH)]),
        p(CALL_DESC),
        checklist("Before the call", ["Think of 3 tasks you'd hand off today.", "Note the hours you need covered in your U.S. time zone.",
                                      "Bring any questions about HIPAA, pricing or replacement."]),
        button("Reschedule my call", "{{appointment.reschedule_link}}"),
        link_line("Can't make it?", "Cancel your call.", "{{appointment.cancellation_link}}"),
        signature("Talk soon,", "Andrea Bolanos")]),
    "08-cal-cancelacion": dict(tag="Call canceled", headline="Your call was canceled, {{contact.first_name}}.", pre="Book a new time whenever it works for you.", rows=[
        p("Your discovery call with Orchid, scheduled for " + WHEN + ", has been canceled."),
        callout("Still want to talk?", "We'd be glad to find another time. The call is free, takes 30 minutes and there's no commitment."),
        button("Book a new time", BOOK_URL),
        p("If you didn't request this change, just reply to this email and we'll sort it out.", pad="18px 36px 22px 36px"),
        signature("Talk soon,", "Andrea Bolanos")]),
    "09-cal-reprogramacion": dict(tag="New time", headline="Your call has a new time, {{contact.first_name}}.", pre="Here are the updated details of your call.", rows=[
        p("Your discovery call with Orchid was rescheduled. Here are the updated details."),
        details([("When", WHEN), ("Where", WHERE), ("With", WITH)]),
        p("Nothing else changes: Andrea will learn about your workload and the tasks you want to delegate, and explain how Orchid matches you with a bilingual professional from Colombia."),
        button("Change the time again", "{{appointment.reschedule_link}}"),
        link_line("Can't make it?", "Cancel your call.", "{{appointment.cancellation_link}}"),
        signature("Talk soon,", "Andrea Bolanos")]),
    "10-cal-recordatorio": dict(tag="Reminder", headline="Your call with Orchid is coming up, {{contact.first_name}}.", pre="A quick reminder of your discovery call details.", rows=[
        p("Here's a quick reminder of your discovery call details."),
        details([("When", WHEN), ("Where", WHERE), ("With", WITH)]),
        button("Join the call", "{{appointment.meeting_location}}"),
        p("It's a relaxed 30-minute conversation. It helps to have in mind the tasks that take most of your week; Andrea will take it from there.", pad="18px 36px 18px 36px"),
        link_line("Need another time?", "Reschedule or cancel here.", "{{appointment.reschedule_link}}"),
        signature("Talk soon,", "Andrea Bolanos")]),
}

INTERNAL_03 = (f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:#FFFFFF;">'
               f'<tr><td style="padding:16px;font-family:{F_BODY};font-size:15px;line-height:22px;color:#1C1233;">'
               f'<p style="margin:0 0 10px 0;font-size:17px;font-weight:bold;color:{C["violet"]};">Nuevo lead de Orchid</p>'
               '<p style="margin:0 0 10px 0;">Entró un nuevo lead desde un formulario de Orchid (landing o formulario de Facebook).</p>'
               '<p style="margin:0;"><b>Nombre:</b> {{contact.name}}<br><b>Teléfono:</b> {{contact.phone}}<br><b>Email:</b> {{contact.email}}<br>'
               '<b>Vertical:</b> {{contact.vertical}}</p>'
               '<p style="margin:10px 0 0 0;">Llámalo lo antes posible. La oportunidad ya está en VENTAS - ORCHID &gt; Nuevo Lead.</p>'
               '</td></tr></table>')

SAMPLE = {"{{contact.first_name}}": "Sarah", "{{contact.last_name}}": "Miller", "{{contact.name}}": "Sarah Miller",
          "{{contact.email}}": "sarah@example.com", "{{contact.phone}}": "(305) 555-0142", "{{contact.vertical}}": "Healthcare",
          "{{appointment.start_time}}": "Tuesday, December 2, 2026 10:00 AM", "{{appointment.timezone}}": "America/New_York",
          "{{appointment.meeting_location}}": "https://meet.google.com/abc-defg-hij", "{{appointment.reschedule_link}}": "#",
          "{{appointment.cancellation_link}}": "#"}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    files = {}
    for name, e in EMAILS.items():
        files[name] = layout(e["tag"], e["headline"], e["rows"], e["pre"])
    # 05 without the offer block
    no_offer = [r for r in EMAILS["05-bienvenida-delegate-brief"]["rows"]]
    i, j = no_offer.index("<!-- OFERTA: borrar después del 1 dic -->"), no_offer.index("<!-- /OFERTA -->")
    no_offer = no_offer[:i] + no_offer[j + 1:]
    e5 = EMAILS["05-bienvenida-delegate-brief"]
    files["05-bienvenida-delegate-brief-sin-oferta"] = layout(e5["tag"], e5["headline"], no_offer, e5["pre"])
    files["03-aviso-interno-nuevo-lead"] = INTERNAL_03
    files["_layout"] = layout("TAG", "Headline, {{contact.first_name}}.", [p("Body paragraph."), button("Button", "#"), signature("Talk soon,", "Andrea Bolanos")], "Pre-header")
    for name, body in files.items():
        assert "—" not in body and "<style" not in body and "<head" not in body and " class=" not in body, name
        for f in set(re.findall(r"\{\{[^}]+\}\}", body)):
            assert f in SAMPLE or f.startswith("{{appointment.") or f.startswith("{{contact."), f
        (OUT / f"{name}.html").write_text(body + "\n")
    # preview index
    cards = []
    for name in sorted(n for n in files if not n.startswith("_")):
        prev = files[name]
        for k, v in SAMPLE.items():
            prev = prev.replace(k, v)
        cards.append(f'<section><h2>{name}</h2><div class="row"><iframe srcdoc="{html.escape(prev)}" style="width:600px"></iframe>'
                     f'<iframe srcdoc="{html.escape(prev)}" style="width:375px"></iframe></div></section>')
    (OUT / "index.html").write_text(
        '<!doctype html><meta charset="utf-8"><title>Correos Orchid</title><style>body{font-family:Arial;background:#eee;margin:20px}'
        'h2{font-size:16px;color:#3F1D83}.row{display:flex;gap:20px;align-items:flex-start;flex-wrap:wrap}iframe{height:1100px;border:1px solid #ccc;background:#fff}</style>'
        '<h1>Correos automáticos Orchid · vista previa (600px y 375px)</h1>' + "".join(cards))
    print("written", len(files), "files to", OUT)


if __name__ == "__main__":
    main()
