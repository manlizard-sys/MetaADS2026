"""Builds the GHL custom-code pieces for the two Black Friday landings (healthcare practices, companies &
entrepreneurs) from the live attorneys landing (go.orchidpros.com/hire-50off, saved in build/landings/source).
Only copy changes; styles, scripts and layout stay identical. Every replacement must match exactly once,
so a change on the source page makes this fail loudly instead of shipping a half-edited page.
Output: build/landings/<market>/piece1.html, piece2.html, piece3.html"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "build" / "landings"
SRC = {i: (ROOT / "source" / f"attorneys_piece{i}.html").read_text() for i in (1, 2, 3)}

COMMON = [  # both markets
    ('href="#section-yvevsj6nLI"', 'href="#book"', None),  # the GHL section id changes on a cloned page; #book lives in piece 2
    ("Claim My 50% Off", "Get Started Free", None),
    ('<span class="txt-long">🔥 $0 upfront + 50% off your first month.</span>',
     '<span class="txt-long">🔥 Black Friday: get started free + 50% off your first month.</span>', 1),
    ('<span class="offer-label">Limited-time offer</span>', '<span class="offer-label">Black Friday offer · until Dec 1</span>', 1),
    ("<p class=\"terms\">$0 upfront: no setup or placement fee before your professional starts. 50% off applies to Orchid's first monthly service fee.</p>",
     "<p class=\"terms\">Black Friday offer, valid until December 1st. Limited spots. $0 upfront: no setup or placement fee before your professional starts. 50% off applies to Orchid's first monthly service fee. Terms &amp; conditions apply.</p>", 1),
    ("The offer is reserved for calls booked before the timer runs out.",
     "The Black Friday offer is valid for calls booked until December 1st, while spots last.", 1),
    ("chosen for your firm", "chosen for your {unit}", None),
    ("We present a shortlist selected by our HR team for your firm.", "We present a shortlist selected by our HR team for your {unit}.", 1),
    ("Tell us about your firm.", "Tell us about your {unit}.", 1),
    ('<div class="mini-offer">$0 upfront · 50% off your first month</div>',
     '<div class="mini-offer">Get started free · 50% off your first month</div>', 1),
    # Countdown: same fixed deadline as the short landings and the ads (Dec 1, 11:59 pm ET), shown as days / hours / minutes.
    ('<span class="d mm">30</span><i>:</i><span class="d ss">00</span>',
     '<span class="d dd">00</span><i>d</i><span class="d mm">00</span><i>h</i><span class="d ss">00</span><i>m</i>', 2),
    ("// 30-minute offer window per visitor. Persisted so a reload doesn't reset it.", "// Black Friday countdown: fixed deadline for every visitor (Dec 1 2026, 11:59 pm ET).", 1),
    ("  var KEY='orchid_offer_deadline_final', LEN=30*60*1000, deadline;\n  // Internal testing: add ?resettimer to the URL to restart the 30 minutes.\n  if(/[?&]resettimer/.test(location.search)){ try{localStorage.removeItem(KEY);}catch(e){} }\n  try{ deadline=parseInt(localStorage.getItem(KEY),10); }catch(e){}\n  if(!deadline||isNaN(deadline)){ deadline=Date.now()+LEN; try{localStorage.setItem(KEY,deadline);}catch(e){} }\n  var mms=",
     "  var deadline=new Date('2026-12-01T23:59:00-05:00').getTime();\n  var dds=document.querySelectorAll('.dd'), mms=", 1),
    ("var left=Math.max(0,deadline-Date.now()), m=Math.floor(left/60000), s=Math.floor(left%60000/1000);\n    mms.forEach(function(e){e.textContent=String(m).padStart(2,'0')});",
     "var left=Math.max(0,deadline-Date.now()), dd=Math.floor(left/864e5), m=Math.floor(left%864e5/36e5), s=Math.floor(left%36e5/6e4);\n    dds.forEach(function(e){e.textContent=String(dd).padStart(2,'0')}); mms.forEach(function(e){e.textContent=String(m).padStart(2,'0')});", 1),
    ("The 50% offer window has closed.", "The Black Friday offer has ended.", 1),
    ('<span class="txt">Offer ends in</span>', '<span class="txt">Ends Dec 1 · days / hrs / min</span>', 1),
    ('<span class="bl">Offer ends in</span>', '<span class="bl">Ends Dec 1 · days / hrs / min</span>', 1),
    ("ORCHID | Attorneys funnel (hero option B)", "ORCHID | {name} funnel (Black Friday, from attorneys hero B)", None),
    ("SEO title (Page settings): Orchid for Law Firms | $0 Upfront, 50% Off Your First Month", "SEO title (Page settings): {seo_title}", 1),
    ("SEO description (Page settings): Bilingual legal professionals from Colombia for U.S. law firms, selected one by one by our HR team. $0 upfront and 50% off your first month.",
     "SEO description (Page settings): {seo_desc}", 1),
]

PAIN_CARD1 = ("<h3>Every missed call is a client your competitor signs</h3>\n        <p>You're in court or with a client. A potential client calls, nobody answers in Spanish, and they sign with the next firm that picks up.</p>\n        <span class=\"chip\">Leads go cold while you litigate</span>")
PAIN_CARD2 = "<p>You hired a legal assistant. A few weeks later they were gone. Now you're posting the job again, screening again and teaching your intake process from zero.</p>"
PAIN_CARD3 = "Then your new hire can't hold a client call, misses context"
STEP3 = "Live English evaluation plus role-specific tests built around legal work: intake, case management software, calendars and client follow-up."
VERTS_HEAD = ('<span class="tag lilac">Built for law firms</span>\n    <h2>Professionals who already speak your language.</h2>\n'
              '    <p class="lead">You don\'t need to train us on legal basics. Our professionals arrive with proven experience in legal operations.</p>')
VERTS = ('<div class="vert"><h3>Intake Specialist</h3><ul><li>Answers and qualifies new client calls in English and Spanish</li><li>Books consultations</li><li>Follows up until the client signs</li></ul></div>\n'
         '      <div class="vert"><h3>Virtual Paralegal</h3><ul><li>Document preparation and organization</li><li>Case file updates</li><li>Client communication on case status</li></ul></div>\n'
         '      <div class="vert"><h3>Back-Office Admin</h3><ul><li>Calendar and deadline tracking</li><li>Billing and invoicing support</li><li>Inbox and records management</li></ul></div>')
FAQ_LEGAL = ("<details name=\"faq\"><summary>Do they already know legal work?</summary><p>Yes. We select professionals with proven experience in legal operations, so you don't need to train them on legal basics. You only show them how your firm works.</p></details>")

MARKETS = {
    "healthcare": dict(
        name="Healthcare", unit="practice", key="bf_health",
        seo_title="Orchid for Healthcare Practices | Get Started Free, 50% Off Your First Month",
        seo_desc="HIPAA-trained, bilingual healthcare support professionals from Colombia for U.S. practices, selected one by one and backed by ongoing HR support from Orchid. Black Friday: get started free and 50% off your first month.",
        rep=[
            ("For U.S. Law Firms &amp; Attorneys", "For U.S. Healthcare Practitioners", 1),
            ("with a bilingual legal professional from Colombia, selected for your firm by people, not AI.",
             "with a bilingual healthcare support professional from Colombia, selected for your practice by people, not AI.", 1),
            ("<p class=\"lead\">Delegation is a revenue decision. Hand off client calls, intake, follow-ups and back-office work to a full-time professional with proven experience in legal operations, online during your hours.</p>",
             "<p class=\"lead\">Your front desk shouldn't be the reason patients wait on hold. Hand off scheduling, patient intake, insurance verification calls and follow-ups to a full-time, HIPAA-trained professional, online during your hours.</p>", 1),
            ("<li>Replaced at $0 if it's not the right fit</li>\n    </ul>",
             "<li>HIPAA-trained and certified, renewed every year</li>\n      <li>Ongoing HR support and coaching from Orchid</li>\n      <li>Replaced at $0 if it's not the right fit</li>\n    </ul>", 1),
            ("hours a week back for every attorney", "hours a week back for your front desk", 1),
            ("<h2>Most firms don't lack talent.<br>They lack structure.</h2>", "<h2>Most practices don't lack patients.<br>They lack front-desk capacity.</h2>", 1),
            (PAIN_CARD1, "<h3>Every unanswered call is a patient who books elsewhere</h3>\n        <p>You're with a patient. Someone calls to book, nobody answers in Spanish, and they book with the next practice that picks up.</p>\n        <span class=\"chip\">Appointments lost while you treat</span>", 1),
            (PAIN_CARD2, "<p>You hired a front-desk coordinator. A few weeks later they were gone. Now you're posting the job again, screening again and teaching your scheduling system from zero.</p>", 1),
            (PAIN_CARD3, "Then your new hire can't handle a patient call, misses context", 1),
            ("<p>Every hour you spend on admin is an hour you're not billing, advising or signing new clients.</p>",
             "<p>Every hour your team spends on hold with insurers or chasing paperwork is an hour not spent on patient care.</p>", 1),
            (STEP3, "Live English evaluation plus role-specific tests built around healthcare admin: scheduling systems, patient intake, insurance verification and follow-up. HIPAA training and certification before they start.", 1),
            (VERTS_HEAD, '<span class="tag lilac">Built for healthcare practices</span>\n    <h2>Professionals who already speak your language.</h2>\n'
                         '    <p class="lead">You don\'t need to train us on the basics of a practice. Our professionals arrive with experience in healthcare administration and HIPAA training, renewed every year.</p>', 1),
            (VERTS, '<div class="vert"><h3>Patient Intake Coordinator</h3><ul><li>Answers and books new patient calls in English and Spanish</li><li>Collects intake forms</li><li>Sends reminders and confirmations</li></ul></div>\n'
                    '      <div class="vert"><h3>Medical Scheduler</h3><ul><li>Manages the schedule, cancellations and waitlist</li><li>Insurance eligibility and verification calls</li><li>Prior authorization follow-up</li></ul></div>\n'
                    '      <div class="vert"><h3>Interpreter &amp; Patient Support</h3><ul><li>Spanish interpretation on calls</li><li>Patient follow-ups and questions</li><li>Inbox and records management</li></ul></div>', 1),
            (FAQ_LEGAL, "<details name=\"faq\"><summary>Are they HIPAA-trained?</summary><p>Yes. Every professional placed with a healthcare practice completes HIPAA training and certification before starting, and Orchid renews it every year.</p></details>\n"
                        "      <details name=\"faq\"><summary>What support do you give after they start?</summary><p>Ongoing HR support from Orchid: regular check-ins with your assistant, coaching, yearly HIPAA renewal and a $0 replacement if it's not the right fit. You manage the work; we take care of the people side.</p></details>\n"
                        "      <details name=\"faq\"><summary>Do they need access to our systems?</summary><p>They work inside your scheduling, EHR or phone tools with the access you choose to grant, following your practice's policies.</p></details>", 1),
        ]),
    "entrepreneurs": dict(
        name="Entrepreneurs", unit="business", key="bf_business",
        seo_title="Orchid for U.S. Companies | Get Started Free, 50% Off Your First Month",
        seo_desc="Bilingual admin, operations, bookkeeping and marketing professionals from Colombia for U.S. companies and entrepreneurs, selected one by one by our HR team. Black Friday: get started free and 50% off your first month.",
        rep=[
            ("For U.S. Law Firms &amp; Attorneys", "For U.S. Companies &amp; Entrepreneurs", 1),
            ("with a bilingual legal professional from Colombia, selected for your firm by people, not AI.",
             "with a bilingual professional from Colombia, selected for your business by people, not AI.", 1),
            ("<p class=\"lead\">Delegation is a revenue decision. Hand off client calls, intake, follow-ups and back-office work to a full-time professional with proven experience in legal operations, online during your hours.</p>",
             "<p class=\"lead\">Delegation is a growth decision. Hand off admin, operations, bookkeeping and marketing tasks to a full-time professional, online during your hours, so you can focus on growing your business.</p>", 1),
            ("hours a week back for every attorney", "hours a week back for every owner", 1),
            ("<h2>Most firms don't lack talent.<br>They lack structure.</h2>", "<h2>Most businesses don't lack talent.<br>They lack structure.</h2>", 1),
            (PAIN_CARD1, "<h3>Every missed call is a customer your competitor wins</h3>\n        <p>You're on a job or with a customer. A lead calls, nobody answers, and they hire the next company that picks up.</p>\n        <span class=\"chip\">Leads go cold while you work</span>", 1),
            (PAIN_CARD2, "<p>You hired an assistant. A few weeks later they were gone. Now you're posting the job again, screening again and teaching your processes from zero.</p>", 1),
            (PAIN_CARD3, "Then your new hire can't hold a customer call, misses context", 1),
            ("<p>Every hour you spend on admin is an hour you're not billing, advising or signing new clients.</p>",
             "<p>Every hour you spend on admin is an hour you're not selling, serving customers or growing.</p>", 1),
            (STEP3, "Live English evaluation plus role-specific tests built around the job: admin tools, bookkeeping software, CRMs, calendars and customer follow-up.", 1),
            (VERTS_HEAD, '<span class="tag lilac">Built for growing businesses</span>\n    <h2>Professionals who already know the job.</h2>\n'
                         '    <p class="lead">Our professionals arrive with proven experience in the role you need. You only show them how your business works.</p>', 1),
            (VERTS, '<div class="vert"><h3>Admin &amp; Operations Assistant</h3><ul><li>Inbox, calendar and data entry</li><li>Vendor and customer follow-ups in English and Spanish</li><li>Scheduling and dispatch support</li></ul></div>\n'
                    '      <div class="vert"><h3>Bookkeeping Assistant</h3><ul><li>Invoices and payment follow-up</li><li>Expense tracking and reconciliations</li><li>Reports ready for your accountant</li></ul></div>\n'
                    '      <div class="vert"><h3>Marketing Assistant</h3><ul><li>Social media posting and replies</li><li>CRM and lead follow-up</li><li>Email campaigns and reviews</li></ul></div>', 1),
            (FAQ_LEGAL, "<details name=\"faq\"><summary>What kind of businesses do you work with?</summary><p>U.S. companies and entrepreneurs in home services, construction, insurance, real estate, e-commerce and professional services. If your team needs a reliable bilingual professional, we can help.</p></details>", 1),
        ]),
}


def apply(text, reps, m):
    for old, new, count in reps:
        new_f = new
        for k in ("unit", "key", "name", "seo_title", "seo_desc"):
            new_f = new_f.replace("{" + k + "}", str(m.get(k, "")))
        old_f = old
        n = text.count(old_f)
        if count is not None and n != count:
            raise SystemExit(f"[{m['name']}] expected {count} match(es), found {n}: {old_f[:80]}")
        if count is None and n == 0:
            raise SystemExit(f"[{m['name']}] no match: {old_f[:80]}")
        text = text.replace(old_f, new_f)
    return text


for market, m in MARKETS.items():
    out = ROOT / market
    out.mkdir(parents=True, exist_ok=True)
    reps = m["rep"] + COMMON  # market-specific first: they contain strings COMMON would otherwise rewrite
    p1 = apply(SRC[1], [r for r in reps if r[0] not in ("Tell us about your firm.", '<div class="mini-offer">$0 upfront · 50% off your first month</div>')], m)
    p2 = apply(SRC[2], [r for r in COMMON if r[0] in ("Tell us about your firm.", '<div class="mini-offer">$0 upfront · 50% off your first month</div>',
                                                        "ORCHID | Attorneys funnel (hero option B)", "Claim My 50% Off")], m)
    # Split-test marker: GHL stores the page URL on the contact, so the long variant tags it with lp_variant=long.
    p1 += """
<script>
// A/B test marker (long landing): adds lp_variant=long to the URL so GHL records which variant the lead saw.
(function(){ try{ var u=new URL(location.href); if(!u.searchParams.has('lp_variant')){ u.searchParams.set('lp_variant','long'); history.replaceState(null,'',u.toString()); } }catch(e){} })();
</script>"""
    (out / "piece1.html").write_text(p1); (out / "piece2.html").write_text(p2); (out / "piece3.html").write_text(SRC[3])
    left = [w for w in ("legal", "attorney", "law firm", "Law Firm", "litigate", "paralegal") if w in p1.split("</style>", 1)[1] + p2]
    print(market, "ok", len(p1), len(p2), "· leftover legal words:", left)
