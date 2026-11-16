"""Three short, independent Black Friday landings for GHL, form first, countdown to Thanksgiving
(Thu Nov 26 2026, 11:59 pm ET). Styles are reused from the live attorneys landing so the brand matches.
Each page = 3 GHL Custom Code blocks:
  block1: top section (purple, 2 columns) LEFT column: all styles + hero + countdown. RIGHT column: GHL form.
  block2: full-width section below: short content (roles, how it works, FAQ, final CTA).
  block3: footer.
Output: build/landings/short/<page>/block1.html, block2.html, block3.html"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "build" / "landings"
src = (ROOT / "source" / "attorneys_piece1.html").read_text()
STYLES = src[src.index("<style>:root"):src.index("</style>", src.index("<style>\n")) + len("</style>")]
FOOTER = (ROOT / "source" / "attorneys_piece3.html").read_text()
DEADLINE = "2026-11-26T23:59:00-05:00"  # Thanksgiving, 11:59 pm Eastern
LOGO = "https://assets.cdn.filesafe.space/r5demglXbNG9LoCszFIw/media/6adbab5e651cc02cde258343.png"
SPIKE = "https://orchidpros.com/wp-content/uploads/2026/05/shape5.svg"

EXTRA = """<style>
#orchid-lp-book .bf-logo{display:block;margin:0 0 22px}
#orchid-lp-book .bf-title{font-family:var(--font-display);font-weight:700;color:#fff;font-size:clamp(2rem,4.2vw,3.1rem);line-height:1.08;margin:14px 0 14px;text-wrap:balance}
#orchid-lp-book .bf-title .y{color:var(--orchid-yellow)}
#orchid-lp-book .bf-offer{display:inline-block;background:var(--orchid-yellow);color:var(--orchid-violet-deep);font-weight:800;border-radius:12px 16px 11px 15px;padding:8px 16px;font-size:1.05rem;margin:4px 0 18px}
#orchid-lp-book .bf-count{margin:6px 0 20px}
#orchid-lp-book .bf-count .bl{display:block;font-weight:700;color:rgba(255,255,255,.9);margin-bottom:8px;font-size:.95rem;letter-spacing:.04em;text-transform:uppercase}
#orchid-lp-book .bf-count .units{display:flex;gap:10px;flex-wrap:wrap}
#orchid-lp-book .bf-count .u{background:#fff;color:var(--orchid-red);border-radius:12px 14px 11px 13px;min-width:66px;padding:6px 8px 4px;text-align:center;box-shadow:0 5px 0 rgba(0,0,0,.18)}
#orchid-lp-book .bf-count .u b{display:block;font-size:1.9rem;font-weight:800;line-height:1.05;font-variant-numeric:tabular-nums}
#orchid-lp-book .bf-count .u small{display:block;font-size:.72rem;font-weight:700;color:var(--orchid-violet);text-transform:uppercase;letter-spacing:.06em}
#orchid-lp-book .bf-count.expired .u{background:#ddd;color:#888}
#orchid-lp-book .bf-terms{font-size:.82rem;color:rgba(255,255,255,.72);margin-top:14px;max-width:520px}
#orchid-lp .bf-sec{padding:clamp(56px,7vw,84px) 0}
#orchid-lp .bf-roles{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:36px;text-align:left}
#orchid-lp .bf-steps{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:36px;text-align:left}
#orchid-lp .bf-steps .card b{display:inline-flex;width:34px;height:34px;align-items:center;justify-content:center;border-radius:50%;background:var(--orchid-violet);color:#fff;margin-bottom:10px}
@media (max-width:860px){#orchid-lp .bf-roles,#orchid-lp .bf-steps{grid-template-columns:1fr}#orchid-lp-book .bf-count .u{min-width:58px}#orchid-lp-book .bf-count .u b{font-size:1.6rem}}
</style>"""

SCRIPT = """<script>
// Countdown to Thanksgiving (Thu Nov 26 2026, 11:59 pm ET). Same deadline for every visitor.
(function(){
  var end=new Date('%s').getTime(), box=document.querySelector('#orchid-lp-book .bf-count');
  if(!box) return;
  var el=function(k){return box.querySelector('[data-u="'+k+'"]')}, pad=function(n){return String(n).padStart(2,'0')};
  function tick(){
    var left=Math.max(0,end-Date.now());
    el('d').textContent=pad(Math.floor(left/864e5)); el('h').textContent=pad(Math.floor(left%%864e5/36e5));
    el('m').textContent=pad(Math.floor(left%%36e5/6e4)); el('s').textContent=pad(Math.floor(left%%6e4/1e3));
    if(left<=0){ box.classList.add('expired'); box.querySelector('.bl').textContent=%s; clearInterval(t); }
  }
  var t=setInterval(tick,1000); tick();
})();
</script>""" 

COUNT = """<div class="bf-count" aria-live="polite"><span class="bl">%s</span><div class="units">
  <div class="u"><b data-u="d">00</b><small>days</small></div><div class="u"><b data-u="h">00</b><small>hours</small></div>
  <div class="u"><b data-u="m">00</b><small>min</small></div><div class="u"><b data-u="s">00</b><small>sec</small></div></div></div>"""


def block1(p):
    checks = "".join(f"<li>{c}</li>" for c in p["checks"])
    return f"""<!-- ORCHID | {p['name']} landing (Black Friday, short) | BLOCK 1 of 3
  GHL: first section, background #3F1D82, 2 columns. This code goes in the LEFT column; the GHL form goes in the RIGHT
  column (on mobile the form appears right after this block). This block holds ALL styles for blocks 2 and 3.
  SEO title: {p['seo_title']}
  SEO description: {p['seo_desc']} -->
{STYLES}
{EXTRA}
<div id="orchid-lp-book"><div class="book-copy" id="book">
  <img class="bf-logo" src="{LOGO}" alt="Orchid" width="120" height="36">
  <span class="tag">{p['tag']}</span>
  <h1 class="bf-title">{p['title']}</h1>
  <div class="bf-offer">{p['offer']}</div>
  {COUNT % p['count_label']}
  <ul class="checks">{checks}</ul>
  <p class="bf-terms">{p['terms']}</p>
</div></div>
{SCRIPT % (DEADLINE, repr(p['expired']))}"""


def block2(p):
    cards = "".join(f'<div class="vert"><h3>{h}</h3><ul>{"".join(f"<li>{i}</li>" for i in items)}</ul></div>' for h, items in p["cards"])
    steps = "".join(f'<div class="card"><b>{n}</b><h3>{h}</h3><p>{t}</p></div>' for n, (h, t) in enumerate(p["steps"], 1))
    faq = "".join(f'<details name="faq"{" open" if i == 0 else ""}><summary>{q}</summary><p>{a}</p></details>' for i, (q, a) in enumerate(p["faq"]))
    return f"""<!-- ORCHID | {p['name']} landing (Black Friday, short) | BLOCK 2 of 3
  GHL: full-width section below the form section, padding/margins 0 > Custom Code. Styles come from block 1. -->
<div id="orchid-lp">
<section class="center bf-sec verts-sec"><div class="wrap">
  <span class="tag lilac">{p['cards_tag']}</span>
  <h2>{p['cards_title']}</h2>
  <p class="lead">{p['cards_lead']}</p>
  <div class="bf-roles verts">{cards}</div>
</div></section>
<section class="center bf-sec how-sec"><div class="wrap">
  <span class="tag">{p['steps_tag']}</span>
  <h2>{p['steps_title']}</h2>
  <div class="bf-steps">{steps}</div>
</div></section>
<section class="center bf-sec faq-sec"><div class="wrap">
  <h2>Frequently asked questions</h2>
  <div class="faq">{faq}</div>
  <div class="cta-row"><a class="btn" href="#book">{p['cta']}</a></div>
</div></section>
</div>"""


SELECTION = "Our HR team interviews every candidate personally, runs a behavioral assessment and a live English assessment, and checks references one by one. No AI filters."
PAGES = {
    "healthcare": dict(
        name="Healthcare", tag="For U.S. healthcare practitioners",
        title='A bilingual front desk for your practice. <span class="y">Get started free.</span>',
        offer="Black Friday: $0 upfront + 50% off your first month", count_label="Offer ends Thanksgiving at 11:59 pm ET",
        expired="'The Black Friday offer has ended. Book a call to check availability.'",
        checks=["HIPAA-trained and certified, renewed every year", "Fluent English &amp; Spanish, U.S. business hours", "Replaced at $0 if it's not the right fit"],
        terms="$0 upfront: no setup or placement fee before your professional starts. 50% off applies to Orchid's first monthly service fee. Limited spots. Terms &amp; conditions apply.",
        cards_tag="Built for healthcare practices", cards_title="Roles we place in practices like yours",
        cards_lead="Professionals with experience in healthcare administration, selected for your practice by people, not AI.",
        cards=[("Patient Intake Coordinator", ["New patient calls in English and Spanish", "Intake forms and records", "Reminders and confirmations"]),
               ("Medical Scheduler", ["Schedule, cancellations and waitlist", "Insurance eligibility and verification calls", "Prior authorization follow-up"]),
               ("Interpreter &amp; Patient Support", ["Spanish interpretation on calls", "Patient follow-ups and questions", "Inbox and records management"])],
        steps_tag="How it works", steps_title="Three steps to your new team member.",
        steps=[("Book a free call", "30 minutes to understand your practice, your tools and what you want off your front desk."),
               ("Meet your shortlist", "Candidates selected by our HR team for your practice. You interview them and choose."),
               ("Start delegating", "$0 upfront and 50% off your first month, with HIPAA training and ongoing HR support from Orchid.")],
        faq=[("What does the Black Friday offer include?", "$0 upfront (no setup or placement fee) and 50% off Orchid's first monthly service fee, for calls booked before Thanksgiving at 11:59 pm ET, while spots last."),
             ("Are they HIPAA-trained?", "Yes. Every professional placed with a healthcare practice completes HIPAA training and certification before starting, and Orchid renews it every year."),
             ("How do you select them?", SELECTION),
             ("How much does it cost after the first month?", "It depends on the role and schedule. Most full-time roles start around $1,700 to $2,200 per month, all-in. You get an exact number on the call.")],
        cta="Get Started Free",
        seo_title="Orchid for Healthcare Practices | Black Friday: Get Started Free",
        seo_desc="HIPAA-trained, bilingual healthcare support professionals from Colombia for U.S. practices. Black Friday: $0 upfront and 50% off your first month, until Thanksgiving."),
    "entrepreneurs": dict(
        name="Entrepreneurs", tag="For U.S. companies &amp; entrepreneurs",
        title='Hand off the admin. <span class="y">Get started free.</span>',
        offer="Black Friday: $0 upfront + 50% off your first month", count_label="Offer ends Thanksgiving at 11:59 pm ET",
        expired="'The Black Friday offer has ended. Book a call to check availability.'",
        checks=["Verified, bilingual professionals from Colombia", "Your U.S. business hours", "Replaced at $0 if it's not the right fit"],
        terms="$0 upfront: no setup or placement fee before your professional starts. 50% off applies to Orchid's first monthly service fee. Limited spots. Terms &amp; conditions apply.",
        cards_tag="Built for growing businesses", cards_title="Roles we place in businesses like yours",
        cards_lead="Professionals with proven experience in the role, selected for your business by people, not AI. You focus on growing your business.",
        cards=[("Admin &amp; Operations", ["Inbox, calendar and data entry", "Vendor and customer follow-ups in English and Spanish", "Scheduling and dispatch support"]),
               ("Bookkeeping", ["Invoices and payment follow-up", "Expense tracking and reconciliations", "Reports ready for your accountant"]),
               ("Marketing", ["Social media posting and replies", "CRM and lead follow-up", "Email campaigns and reviews"])],
        steps_tag="How it works", steps_title="Three steps to your new team member.",
        steps=[("Book a free call", "30 minutes to understand your business, your tools and the tasks you want off your plate."),
               ("Meet your shortlist", "Candidates selected by our HR team for your business. You interview them and choose."),
               ("Start delegating", "$0 upfront and 50% off your first month, with ongoing coaching and HR support from Orchid.")],
        faq=[("What does the Black Friday offer include?", "$0 upfront (no setup or placement fee) and 50% off Orchid's first monthly service fee, for calls booked before Thanksgiving at 11:59 pm ET, while spots last."),
             ("What kind of businesses do you work with?", "U.S. companies and entrepreneurs in home services, construction, insurance, real estate, e-commerce and professional services."),
             ("How do you select them?", SELECTION),
             ("How much does it cost after the first month?", "It depends on the role and schedule. Most full-time roles start around $1,700 to $2,200 per month, all-in. You get an exact number on the call.")],
        cta="Get Started Free",
        seo_title="Orchid for U.S. Companies | Black Friday: Get Started Free",
        seo_desc="Bilingual admin, operations, bookkeeping and marketing professionals from Colombia for U.S. companies. Black Friday: $0 upfront and 50% off your first month, until Thanksgiving."),
    "newsletter": dict(
        name="Newsletter", tag="The Delegate Brief · free, every other week",
        title='One task to take off your plate, <span class="y">every other week.</span>',
        offer="Subscribers get the Black Friday offer too", count_label="Black Friday offer ends Thanksgiving at 11:59 pm ET",
        expired="'The Black Friday offer has ended. The Brief keeps coming every other week.'",
        checks=["A task worth delegating, step by step", "A ready-to-use template", "A real number: time or money saved"],
        terms="3-minute read. Unsubscribe anytime. We never share your email.",
        cards_tag="What's inside", cards_title="Practical, short and built for owners.",
        cards_lead="For U.S. business owners, practices and firms that want their time back.",
        cards=[("Delegate this", ["One task you can hand off this week", "Who should do it and how", "The 3 steps to hand it off"]),
               ("Steal this template", ["Scripts, checklists and SOPs", "Ready to copy and use", "Built from real Orchid clients' workflows"]),
               ("The number", ["Hours or dollars saved", "What it costs in-house vs. delegated", "No fluff, no hype"])],
        steps_tag="How it works", steps_title="Simple.",
        steps=[("Subscribe", "First name and email. That's it."),
               ("Read in 3 minutes", "Every other week, one idea you can use that same day."),
               ("Delegate when you're ready", "If you want help, book a free call. No pressure.")],
        faq=[("How often will I get it?", "Every other week. Short, practical, no spam."),
             ("What's the Black Friday offer?", "$0 upfront and 50% off Orchid's first monthly service fee when you book a call before Thanksgiving at 11:59 pm ET. Subscribers get the link in their welcome email."),
             ("Can I unsubscribe?", "Yes, with one click from any email.")],
        cta="Send Me the Brief",
        seo_title="The Delegate Brief by Orchid | One Task to Delegate, Every Other Week",
        seo_desc="A free, 3-minute brief for U.S. business owners: one task to delegate, a ready-to-use template and the real numbers. Every other week."),
}

for key, p in PAGES.items():
    out = ROOT / "short" / key
    out.mkdir(parents=True, exist_ok=True)
    (out / "block1.html").write_text(block1(p)); (out / "block2.html").write_text(block2(p)); (out / "block3.html").write_text(FOOTER)
    print(key, "ok")
