const pptxgen = require("pptxgenjs");
const S = "/tmp/claude-0/-home-user-MetaADS2026/bf71e0df-652f-5f76-93c1-b26abc9f7914/scratchpad/brand";
const P = "/home/user/MetaADS2026/sunny_bliss/build/reports/previews/2026-10-30";
const OUT = process.argv[2];

const NAVY = "013463", NAVY2 = "0C4A85", ORANGE = "F7931E", YELLOW = "FFD23F", RUST = "B35A00",
  INK = "3F4E63", MUTED = "6B7A8C", TINT = "EEF4FA", PEACH = "FFF0D6", LINE = "DCE3EA", WHITE = "FFFFFF", LIGHT = "FFF9EE";
const W = 13.333, M = 0.6, CW = W - 2 * M;

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
pres.title = "Sunny Bliss Meta Advertising Plan";
pres.company = "Sunny Bliss Plumbing &amp; Air";
pres.theme = { headFontFace: "Calibri", bodyFontFace: "Calibri" };

pres.defineSlideMaster({
  title: "CONTENT",
  background: { color: WHITE },
  objects: [{ image: { path: `${S}/logo.png`, x: W - M - 1.5, y: 0.28, w: 1.5, h: 0.553 } }],
  slideNumber: { x: W - M - 0.6, y: 6.98, w: 0.6, h: 0.3, fontSize: 10, color: MUTED, align: "right" },
});
pres.defineSlideMaster({ title: "COVER", background: { color: WHITE } });

const shadow = () => ({ type: "outer", color: NAVY, opacity: 0.12, blur: 8, offset: 2, angle: 90 });
const card = (s, x, y, w, h, fill = WHITE, line = LINE) =>
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, fill: { color: fill }, line: { color: line, width: 0.75 }, rectRadius: 0.12, shadow: shadow() });
const box = (s, x, y, w, h, fill) => s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, fill: { color: fill }, line: { color: fill, width: 0 }, rectRadius: 0.12 });
const bar = (s, x, y, w, h, color) => s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w: Math.max(w, 0.06), h, fill: { color }, line: { color, width: 0 }, rectRadius: 0.04 });
const tx = (s, text, o) => s.addText(text, { isTextBox: true, margin: 0, valign: "top", color: INK, fontSize: 14, ...o });
const watermark = (s, x, y, w) => s.addImage({ path: `${S}/watermark.png`, x, y, w, h: w * 688 / 900 });

function content(eyebrow, title, footer, notes) {
  const s = pres.addSlide({ masterName: "CONTENT" });
  tx(s, eyebrow.toUpperCase(), { x: M, y: 0.4, w: 9, h: 0.3, fontSize: 12, bold: true, color: RUST, charSpacing: 2 });
  tx(s, title, { x: M, y: 0.72, w: 9.5, h: 0.7, fontSize: 36, bold: true, color: NAVY, valign: "middle" });
  if (footer) tx(s, footer, { x: M, y: 6.98, w: CW - 0.8, h: 0.3, fontSize: 10, color: MUTED });
  if (notes) s.addNotes(notes);
  return s;
}

// 1 Cover
{
  const s = pres.addSlide({ masterName: "COVER" });
  watermark(s, 6.9, 1.6, 6.4);
  s.addImage({ path: `${S}/logo.png`, x: M, y: 0.9, w: 3.6, h: 1.326 });
  tx(s, "META ADVERTISING · NOVEMBER-DECEMBER 2026", { x: M, y: 2.75, w: 8, h: 0.35, fontSize: 14, bold: true, color: RUST, charSpacing: 3 });
  tx(s, "Growth", { x: M, y: 3.15, w: 8.5, h: 1.2, fontSize: 66, bold: true, color: NAVY, valign: "middle" });
  tx(s, "Results review and action plan for HVAC, plumbing and electrical services in 21 South Miami-Dade ZIP codes.", { x: M, y: 4.45, w: 7.4, h: 1.0, fontSize: 20 });
  tx(s, "Prepared for Sunny Bliss Plumbing & Air · October 30, 2026", { x: M, y: 6.5, w: 8, h: 0.35, fontSize: 12, color: MUTED });
  s.addNotes("Purpose of the meeting: review what September and October produced in Meta and GoHighLevel, agree on the budget, and confirm the commitments needed to launch on November 4.");
}

// 2 Contents
{
  const s = content("Meta advertising plan", "Contents", "Sunny Bliss Plumbing & Air · Meta advertising plan");
  watermark(s, 7.6, 0.2, 5.4);
  const items = [["01", "Performance", "Meta and GoHighLevel results, September-October"], ["02", "Insights", "Creative, audience, seasonality and industry benchmarks"],
    ["03", "Strategy", "Offer, promotions, lead journey, budget and timeline"], ["04", "Requirements", "Decisions and commitments for the November 4 launch"]];
  const cw = (CW - 3 * 0.3) / 4;
  items.forEach(([n, h, t], i) => {
    const x = M + i * (cw + 0.3);
    card(s, x, 2.3, cw, 3.4);
    tx(s, n, { x: x + 0.3, y: 2.55, w: cw - 0.6, h: 1.0, fontSize: 60, bold: true, color: i % 2 ? ORANGE : NAVY });
    tx(s, h, { x: x + 0.3, y: 3.75, w: cw - 0.6, h: 0.45, fontSize: 20, bold: true, color: NAVY });
    tx(s, t, { x: x + 0.3, y: 4.3, w: cw - 0.6, h: 1.1, fontSize: 14 });
  });
}

// 3 Four findings
{
  const s = content("01 · Performance", "Findings", "Sources: Meta Marketing API (Sept 21 to Oct 29) and GoHighLevel (Sept 24 to Oct 30, 2026)",
    "Qualified and unqualified are the tags Sunny Bliss's team applies in GoHighLevel. Cost per lead covers customer campaigns only, Sept 30 to Oct 29. All campaigns were paused on October 30 at the owner's request.");
  const f = [["49 → 28", NAVY, "Meta reported 49 customer leads; 28 reached GoHighLevel. Instant-form leads stopped arriving after October 1."],
    ["11", NAVY, "Homeowners tagged qualified, with 6 estimates booked. Five of the eleven were Spanish speakers."],
    ["0", RUST, "Quotes or sales recorded. Six qualified leads remain at \"New Lead (Contact ASAP)\"."],
    ["$74.92", NAVY, "Cost per customer lead. Recruiting ads on the same page attracted 254 job applicants."]];
  const cw = (CW - 0.3) / 2;
  f.forEach(([n, c, t], i) => {
    const x = M + (i % 2) * (cw + 0.3), y = 1.65 + Math.floor(i / 2) * 1.6;
    card(s, x, y, cw, 1.35);
    tx(s, n, { x: x + 0.3, y: y + 0.2, w: 2.2, h: 0.95, fontSize: 36, bold: true, color: c, valign: "middle" });
    tx(s, t, { x: x + 2.65, y: y + 0.2, w: cw - 2.95, h: 0.95, fontSize: 14, valign: "middle" });
  });
  box(s, M, 4.95, CW, 1.15, NAVY);
  tx(s, [{ text: "Conclusion: ", options: { bold: true, color: YELLOW } }, { text: "Meta has reached interested homeowners. Leads are lost in delivery, attribution and follow-up, and each of these can be corrected before November 4.", options: { color: LIGHT } }],
    { x: M + 0.35, y: 5.1, w: CW - 0.7, h: 0.85, fontSize: 16, valign: "middle" });
}

// 4 Lost leads
{
  const s = content("01 · Performance", "Delivery", "Meta: customer leads, Sept 21 to Oct 29. GoHighLevel: contacts created Sept 24 to Oct 30, 2026",
    "Meta counts a lead when the form is submitted; GoHighLevel only receives it if the integration is active. Twenty-one leads reported by Meta have no matching contact in GoHighLevel, almost all from instant forms.");
  card(s, M, 1.65, 6.0, 4.9);
  const grp = (y, title, a, b, note) => {
    tx(s, title, { x: M + 0.35, y, w: 5.3, h: 0.4, fontSize: 18, bold: true, color: NAVY });
    [["Meta", a, NAVY, NAVY], ["GHL", b, ORANGE, RUST]].forEach(([lab, v, c, tc], i) => {
      const yy = y + 0.5 + i * 0.45;
      tx(s, lab, { x: M + 0.35, y: yy, w: 0.7, h: 0.32, fontSize: 14, color: MUTED, valign: "middle" });
      bar(s, M + 1.1, yy + 0.04, 3.9 * v / 28, 0.24, c);
      tx(s, String(v), { x: M + 1.2 + 3.9 * v / 28, y: yy, w: 0.6, h: 0.32, fontSize: 16, bold: true, color: tc, valign: "middle" });
    });
    tx(s, note, { x: M + 0.35, y: y + 1.45, w: 5.3, h: 0.5, fontSize: 14 });
  };
  grp(1.95, "Instant form", 28, 9, "No contacts received after October 1; none included a phone number.");
  grp(4.2, "Landing page", 21, 19, "Delivery functioning; source of all qualified leads.");
  const iss = [["Form connection stopped after October 1", "Action: reconnect to GoHighLevel and confirm with Meta's lead-testing tool before launch."],
    ["Contacts arrived without phone or source", "Action: map every form question to its GoHighLevel field."],
    ["0 of 28 contacts show which ad produced them", "Action: pass campaign, ad set and ad names into the fields GoHighLevel already has."]];
  iss.forEach(([h, t], i) => {
    const y = 1.65 + i * 1.65;
    card(s, 6.95, y, CW - 6.35, 1.45, TINT, TINT);
    tx(s, h, { x: 7.25, y: y + 0.2, w: CW - 6.95, h: 0.4, fontSize: 16, bold: true, color: NAVY });
    tx(s, t, { x: 7.25, y: y + 0.65, w: CW - 6.95, h: 0.7, fontSize: 14 });
  });
}

// 5 Stalled follow-up
{
  const s = content("01 · Performance", "Follow-up", "Source: GoHighLevel, Sunny Bliss Lead Pipeline, as of October 30, 2026",
    "Five of the eleven qualified leads were Spanish speakers, which supports running every message in English and Spanish. One estimate was booked by a lead tagged unqualified. Recording quotes and sales in the pipeline is what allows the campaign to be judged on revenue.");
  watermark(s, 8.3, 3.0, 4.6);
  card(s, M, 1.65, 7.0, 4.9);
  tx(s, "Landing-page leads in GoHighLevel", { x: M + 0.35, y: 1.9, w: 6.3, h: 0.35, fontSize: 14, bold: true, color: MUTED });
  [["Contacts received", 19], ["Tagged qualified", 11], ["Estimate booked", 6], ["Quote delivered", 0], ["Sold", 0]].forEach(([l, v], i) => {
    const y = 2.45 + i * 0.78;
    tx(s, l, { x: M + 0.35, y, w: 2.2, h: 0.45, fontSize: 16, valign: "middle" });
    bar(s, M + 2.6, y + 0.05, 3.4 * v / 19, 0.35, v ? NAVY : ORANGE);
    tx(s, String(v), { x: M + 2.75 + 3.4 * v / 19, y, w: 0.6, h: 0.45, fontSize: 20, bold: true, color: v ? NAVY : RUST, valign: "middle" });
  });
  box(s, 7.95, 1.65, CW - 7.35, 1.9, NAVY);
  tx(s, "ACTION THIS WEEK", { x: 8.25, y: 1.85, w: CW - 7.95, h: 0.3, fontSize: 12, bold: true, color: YELLOW, charSpacing: 2 });
  tx(s, "Call the 6 qualified leads still at \"New Lead (Contact ASAP)\". The oldest arrived on October 3.", { x: 8.25, y: 2.25, w: CW - 7.95, h: 1.1, fontSize: 16, color: LIGHT });
  tx(s, "Every call and visit should move the lead to its next stage, so each dollar can be traced to a booked or sold job.", { x: 7.95, y: 3.85, w: CW - 7.35, h: 0.9, fontSize: 14 });
  tx(s, "Since October 15, all 6 new landing-page leads were tagged unqualified; the form questions will be reviewed.", { x: 7.95, y: 4.85, w: CW - 7.35, h: 0.9, fontSize: 14 });
}

// 6 Destination matters
{
  const s = content("02 · Insights", "Creative", "Meta Marketing API, Sept 30 to Oct 29, 2026. What the strong ads share: one service, a visible price, one call to action",
    "Weak ads achieved standard click-through rates, indicating interest. The landing pages did not repeat the advertised price or financing, and visitors exited without converting. Landing pages will be rebuilt to match each ad.");
  tx(s, "The Water Heater Flush ad produced 14 leads with an instant form and none with the landing page.", { x: M, y: 1.45, w: CW, h: 0.4, fontSize: 16 });
  const ads = [["2026-09-24-Plumbing-Tank-Flush-149-EN", true, "Water Heater Flush $149", "Instant form · 14 leads · $47.40 each"],
    ["2026-10-08-0-Interest-24-Months-EN", true, "0% Interest, 24 Months", "Landing page · 10 leads · $64.25 each"],
    ["2026-10-06-Plumbing-Tank-Flush-149-EN-Landing", false, "Water Heater Flush $149", "Landing page · $85.62 · 0 leads"],
    ["2026-10-08-Before-You-Sign-v3-EN", false, "Don't Sign That Quote Yet", "Landing page · $137.85 · 0 leads"]];
  const cw = (CW - 3 * 0.3) / 4;
  ads.forEach(([f, good, h, t], i) => {
    const x = M + i * (cw + 0.3);
    card(s, x, 2.0, cw, 4.7);
    s.addShape(pres.shapes.RECTANGLE, { x: x + 0.15, y: 2.15, w: cw - 0.3, h: 2.85, fill: { color: "F2F4F7" }, line: { color: "F2F4F7", width: 0 } });
    s.addImage({ path: `${P}/${f}.png`, x: x + 0.15, y: 2.15, w: cw - 0.3, h: 2.85, sizing: { type: "contain", w: cw - 0.3, h: 2.85 }, altText: `Facebook ad: ${h}` });
    box(s, x + 0.2, 5.15, 1.0, 0.32, good ? NAVY : "FFE3C2");
    tx(s, good ? "Strong" : "Weak", { x: x + 0.2, y: 5.15, w: 1.0, h: 0.32, fontSize: 12, bold: true, color: good ? WHITE : "8A4300", align: "center", valign: "middle" });
    tx(s, h, { x: x + 0.2, y: 5.6, w: cw - 0.4, h: 0.35, fontSize: 15, bold: true, color: NAVY });
    tx(s, t, { x: x + 0.2, y: 5.95, w: cw - 0.4, h: 0.6, fontSize: 13 });
  });
}

// 7 Audience and areas
{
  const s = content("02 · Insights", "Audience", "Meta Marketing API, customer campaigns, Sept 30 to Oct 29, 2026; GoHighLevel tags; U.S. Census income data",
    "Coral Gables median household income is $130,803 and Key Biscayne's is $181,505 (U.S. Census QuickFacts). The 21 targetable ZIP codes, Kendall included, reach 466,000-548,000 people aged 30 and over on Facebook and Instagram.");
  card(s, M, 1.65, 5.9, 4.9);
  tx(s, "Cost per lead by age", { x: M + 0.35, y: 1.9, w: 5.2, h: 0.4, fontSize: 18, bold: true, color: NAVY });
  [["65+", 55.39], ["55-64", 66.22], ["45-54", 133.99], ["35-44", 183.40]].forEach(([a, v], i) => {
    const y = 2.5 + i * 0.62;
    tx(s, a, { x: M + 0.35, y, w: 0.8, h: 0.4, fontSize: 16, valign: "middle" });
    bar(s, M + 1.2, y + 0.06, 3.0 * v / 183.4, 0.28, i < 2 ? NAVY : "AFC0D4");
    tx(s, `$${v.toFixed(2)}`, { x: M + 1.3 + 3.0 * v / 183.4, y, w: 1.0, h: 0.4, fontSize: 16, bold: true, color: NAVY, valign: "middle" });
  });
  tx(s, "Established homeowners over 55 respond at the lowest cost. Five of the eleven qualified leads were Spanish speakers.", { x: M + 0.35, y: 5.15, w: 5.2, h: 0.9, fontSize: 14 });
  card(s, 6.85, 1.65, CW - 6.25, 4.9);
  tx(s, "Best-fit service by area", { x: 7.15, y: 1.9, w: CW - 6.85, h: 0.4, fontSize: 18, bold: true, color: NAVY });
  const rows = [["Area", "Lead service"], ["Coral Gables", "HVAC replacement, panels"], ["Pinecrest, Palmetto Bay, South Miami", "Maintenance plans, generators"],
    ["Key Biscayne", "Premium maintenance"], ["Miami Beach", "Plumbing, water heaters"], ["Miami Shores area", "Electrical upgrades, drains"],
    ["Cutler Bay", "AC repair and financing (Spanish)"], ["Kendall", "AC and water heaters (Spanish)"]];
  s.addTable(rows.map((r, i) => r.map(c => ({ text: c, options: { bold: i === 0, color: i === 0 ? MUTED : NAVY } }))),
    { x: 7.15, y: 2.4, w: CW - 6.85, colW: [2.6, CW - 9.45], fontSize: 13, border: { type: "solid", pt: 0.5, color: LINE }, margin: 0.06, rowH: 0.42 });
}

// 8 Season and electrical
{
  const s = content("02 · Insights", "Seasonality", "NOAA Climate Prediction Center ENSO discussion (Oct 8, 2026) and U.S. Winter Outlook (Oct 15, 2026)",
    "Over 83% probability of a strong to very strong El Niño through January-March 2027. Hurricane season closes November 30. NOAA updates its outlook in mid-November; the message calendar will follow it.");
  const cw = (CW - 0.3) / 2;
  card(s, M, 1.65, cw, 4.9);
  tx(s, "Strong El Niño, December-February", { x: M + 0.35, y: 1.9, w: cw - 0.7, h: 0.4, fontSize: 18, bold: true, color: NAVY });
  [["Plumbing", "Wetter than normal, with January the peak: leaks, drain and sewer backups."], ["HVAC", "Humidity control, heat checks before cold fronts, financed replacements."],
   ["Electrical", "Storm lines in February and March: surge protection and generators."]].forEach(([h, t], i) => {
    const y = 2.5 + i * 1.3;
    box(s, M + 0.35, y, cw - 0.7, 1.1, TINT);
    tx(s, h, { x: M + 0.55, y: y + 0.12, w: cw - 1.1, h: 0.35, fontSize: 16, bold: true, color: NAVY });
    tx(s, t, { x: M + 0.55, y: y + 0.5, w: cw - 1.1, h: 0.55, fontSize: 14 });
  });
  const x2 = M + cw + 0.3;
  card(s, x2, 1.65, cw, 4.9);
  tx(s, "Electrical service visibility", { x: x2 + 0.35, y: 1.9, w: cw - 0.7, h: 0.4, fontSize: 18, bold: true, color: NAVY });
  tx(s, "The Facebook page is categorized as Plumbing Service, and sunnybliss.com lists plumbing, air conditioning, drains and water filtration. Prerequisites for electrical ads:", { x: x2 + 0.35, y: 2.45, w: cw - 0.7, h: 1.1, fontSize: 14 });
  tx(s, [{ text: "Electrical page in English and Spanish, with license number and entry offer", options: { bullet: true, breakLine: true } },
    { text: "Facebook page services and category updated", options: { bullet: true, breakLine: true } },
    { text: "Three creatives in the Sunny Bliss brand", options: { bullet: true } }], { x: x2 + 0.35, y: 3.65, w: cw - 0.7, h: 1.7, fontSize: 14, paraSpaceAfter: 6 });
  tx(s, "Contingency: electrical launches December 1 if prerequisites are incomplete on November 4.", { x: x2 + 0.35, y: 5.6, w: cw - 0.7, h: 0.6, fontSize: 14, bold: true, color: RUST });
}

// 9 Proven practices
{
  const s = content("02 · Insights", "Benchmarks", "Oldroyd, InsideSales.com (2007); Harvard Business Review (2011); Meta Conversions API for CRM; contractor-marketing publications (2026)",
    "Harvard Business Review found firms that answered within an hour were about seven times more likely to qualify a lead. Meta recommends about 200 leads per month before optimizing on CRM stages. Angi and Thumbtack are not recommended because the same lead is sold to several contractors.");
  const p = [["Five-minute response", "Qualification odds are about 21 times higher than at 30 minutes."], ["Single-offer pricing", "Priced, single-service offers outperformed generic free estimates."],
    ["Form qualification", "Ask about home ownership, service needed and urgency."], ["CRM feedback to Meta", "Send booked and sold stages from GoHighLevel so Meta learns who buys."],
    ["Message match", "The same offer, price and language from the ad to the page."], ["Social proof", "4.9 rating, 1,000+ reviews, family-owned since 1990."]];
  const cw = (CW - 2 * 0.3) / 3;
  p.forEach(([h, t], i) => {
    const x = M + (i % 3) * (cw + 0.3), y = 1.65 + Math.floor(i / 3) * 1.6;
    card(s, x, y, cw, 1.4);
    tx(s, h, { x: x + 0.3, y: y + 0.2, w: cw - 0.6, h: 0.4, fontSize: 17, bold: true, color: NAVY });
    tx(s, t, { x: x + 0.3, y: y + 0.65, w: cw - 0.6, h: 0.65, fontSize: 14 });
  });
  box(s, M, 4.95, CW, 1.2, NAVY);
  tx(s, [{ text: "Meta sustains brand recall and promotions convert it; Google Search captures emergency demand. ", options: { bold: true, color: YELLOW } },
    { text: "Proposed for January: a Google Local Services Ads test of $1,000-1,500 per month for emergency plumbing and AC repair.", options: { color: LIGHT } }],
    { x: M + 0.35, y: 5.1, w: CW - 0.7, h: 0.9, fontSize: 16, valign: "middle" });
}

// 10 Bliss Care Plan
{
  const s = content("03 · Strategy", "Membership", "Proposed offer for owner approval; bracketed values are set by Sunny Bliss",
    "The plan builds on the maintenance plans already listed on sunnybliss.com and the existing promises of same-day service with no overtime charges. It gives Meta a reason to contact undecided homeowners now and turns every maintenance visit into an early replacement conversation.");
  watermark(s, 8.6, 3.4, 4.3);
  tx(s, "Bliss Care Plan: a single membership covering preventive maintenance and equipment replacement.", { x: M, y: 1.45, w: CW, h: 0.4, fontSize: 16 });
  const cw = (CW - 0.3) / 2;
  card(s, M, 2.0, cw, 3.15);
  tx(s, "Annual inclusions", { x: M + 0.35, y: 2.2, w: 3.5, h: 0.4, fontSize: 18, bold: true, color: NAVY });
  tx(s, "[$__] per month", { x: M + cw - 2.55, y: 2.2, w: 2.2, h: 0.4, fontSize: 16, bold: true, color: RUST, align: "right" });
  const li = (arr) => arr.map((t, i) => ({ text: t, options: { bullet: true, breakLine: i < arr.length - 1 } }));
  tx(s, li(["Two AC tune-ups", "Water heater flush", "Drain and plumbing inspection", "Electrical safety check: panel and surge", "Priority same-day service, no overtime charges", "Member pricing on repairs [__% off]"]),
    { x: M + 0.35, y: 2.7, w: cw - 0.7, h: 2.3, fontSize: 14, paraSpaceAfter: 4 });
  const x2 = M + cw + 0.3;
  card(s, x2, 2.0, cw, 3.15);
  tx(s, "Replacement path", { x: x2 + 0.35, y: 2.2, w: cw - 0.7, h: 0.4, fontSize: 18, bold: true, color: NAVY });
  tx(s, li(["System-age report at every visit for AC, water heater and panel", "[$___] member credit toward a new system", "0% financing for 24 months, on approved credit", "Same price promise in English and Spanish"]),
    { x: x2 + 0.35, y: 2.7, w: cw - 0.7, h: 2.3, fontSize: 14, paraSpaceAfter: 4 });
  box(s, M, 5.4, cw, 1.1, NAVY);
  tx(s, [{ text: "Meta: ", options: { bold: true, color: YELLOW } }, { text: "homeowners still evaluating options. Primary offer: Bliss Care Plan.", options: { color: LIGHT } }], { x: M + 0.3, y: 5.5, w: cw - 0.6, h: 0.9, fontSize: 15, valign: "middle" });
  box(s, x2, 5.4, cw, 1.1, PEACH);
  tx(s, [{ text: "Google: ", options: { bold: true, color: "8A4300" } }, { text: "emergency demand. Same-day service, with the plan offered after the repair.", options: { color: NAVY } }], { x: x2 + 0.3, y: 5.5, w: cw - 0.6, h: 0.9, fontSize: 15, valign: "middle" });
}

// 11 Three promotions
{
  const s = content("03 · Strategy", "Promotions", "Proposed promotions for owner approval; bracketed values are set by Sunny Bliss",
    "Each promotion maps to one lead-ad angle: inspection, maintenance and replacement. The $49 Home Check builds on the $49 service call already offered on sunnybliss.com. Promotions run in English and Spanish and end December 31.");
  const pr = [["Inspection", "$49 Home Check", "AC, water heater and electrical panel inspected in one visit. The $49 is credited toward any repair or the Bliss Care Plan.", "Paid visit screens out low-intent requests."],
    ["Maintenance", "Founding Member", "Bliss Care Plan with the first month free and the price locked for 12 months, for the first [100] homeowners.", "Limited availability drives urgency."],
    ["Replacement", "Replace and Save", "[$500] off a new AC, water heater or panel, 0% for 24 months, and one year of the Bliss Care Plan included.", "Valid through December 31."]];
  const cw = (CW - 2 * 0.3) / 3;
  pr.forEach(([k, h, t, w], i) => {
    const x = M + i * (cw + 0.3);
    card(s, x, 1.65, cw, 3.4);
    tx(s, k.toUpperCase(), { x: x + 0.3, y: 1.85, w: cw - 0.6, h: 0.3, fontSize: 12, bold: true, color: MUTED, charSpacing: 2 });
    tx(s, h, { x: x + 0.3, y: 2.2, w: cw - 0.6, h: 0.55, fontSize: 24, bold: true, color: NAVY });
    tx(s, t, { x: x + 0.3, y: 2.85, w: cw - 0.6, h: 1.45, fontSize: 14 });
    tx(s, w, { x: x + 0.3, y: 4.4, w: cw - 0.6, h: 0.45, fontSize: 14, bold: true, color: RUST });
  });
  const hw = (CW - 0.3) / 2;
  box(s, M, 5.3, hw, 1.2, NAVY);
  tx(s, [{ text: "Meta: ", options: { bold: true, color: YELLOW } }, { text: "sustains brand recall; promotions convert that attention into qualified leads.", options: { color: LIGHT } }], { x: M + 0.3, y: 5.4, w: hw - 0.6, h: 1.0, fontSize: 15, valign: "middle" });
  box(s, M + hw + 0.3, 5.3, hw, 1.2, PEACH);
  tx(s, [{ text: "Google Search: ", options: { bold: true, color: "8A4300" } }, { text: "captures emergency demand, which converts without a promotion.", options: { color: NAVY } }], { x: M + hw + 0.6, y: 5.4, w: hw - 0.6, h: 1.0, fontSize: 15, valign: "middle" });
}

// 12 Lead journey
{
  const s = content("03 · Strategy", "Journey", "Steps 1-3: Meta and the agency · Steps 4-6: Sunny Bliss team in GoHighLevel",
    "Each step is a pipeline stage in GoHighLevel, so the weekly report shows how many leads move from one step to the next and where they stop. Meta's job ends at step 3; the value of every lead is decided in steps 4 to 6.");
  tx(s, "Six stages from first impression to closed job, each with an owner and a performance metric.", { x: M, y: 1.45, w: CW, h: 0.4, fontSize: 16 });
  const st = [["1 · See", "Awareness ads: top-rated team, 4.9 stars, real reviews.", "Reach"], ["2 · Return", "Visits the website or watches the video; sees the Bliss Care Plan again.", "Visitors"],
    ["3 · Respond", "Takes a promotion and answers three qualifying questions.", "Cost per lead"], ["4 · Contact", "Bilingual call within five minutes, plus a text confirmation.", "Minutes to call"],
    ["5 · Visit", "Home Check or estimate, with a system-age report.", "Cost per visit"], ["6 · Close", "Quote, sale or plan sign-up, then a review request.", "Revenue"]];
  const cw = (CW - 5 * 0.2) / 6;
  st.forEach(([h, t, k], i) => {
    const x = M + i * (cw + 0.2);
    card(s, x, 2.0, cw, 3.0, i < 3 ? WHITE : TINT, i < 3 ? LINE : TINT);
    tx(s, h, { x: x + 0.2, y: 2.2, w: cw - 0.4, h: 0.4, fontSize: 16, bold: true, color: RUST });
    tx(s, t, { x: x + 0.2, y: 2.7, w: cw - 0.4, h: 1.5, fontSize: 14 });
    tx(s, `KPI: ${k}`, { x: x + 0.2, y: 4.3, w: cw - 0.4, h: 0.55, fontSize: 13, bold: true, color: NAVY });
  });
  const hw = (CW - 0.3) / 2;
  box(s, M, 5.25, hw, 1.3, NAVY);
  tx(s, [{ text: "Qualified lead definition: ", options: { bold: true, color: YELLOW } }, { text: "a homeowner in the 21 ZIP codes, with a real need and timing, reachable by phone, called within five minutes, with a visit booked.", options: { color: LIGHT } }], { x: M + 0.3, y: 5.35, w: hw - 0.6, h: 1.1, fontSize: 14, valign: "middle" });
  box(s, M + hw + 0.3, 5.25, hw, 1.3, PEACH);
  tx(s, [{ text: "Prior failure points: ", options: { bold: true, color: "8A4300" } }, { text: "stage 3, form leads did not reach GoHighLevel; stage 4, qualified leads were not called.", options: { color: NAVY } }], { x: M + hw + 0.6, y: 5.35, w: hw - 0.6, h: 1.1, fontSize: 14, valign: "middle" });
}

// 13 Campaign structure
{
  const s = content("03 · Strategy", "Structure", "Awareness fills the website-visitor audience; if that audience is too small, the difference moves to new homeowners",
    "The awareness campaign optimizes for reach and video views and is measured by reach, frequency and growth of the visitor audience, not by leads. The sunnybliss.com pixel already records about 2,600 page views per month, which seeds the visitor audience from day one.");
  box(s, M, 1.6, CW, 0.75, PEACH);
  tx(s, [{ text: "PREREQUISITES · NOV 2-4   ", options: { bold: true, color: "8A4300" } }, { text: "Reconnect forms to GoHighLevel, record the source ad, call the 6 waiting leads, move recruiting to its own page.", options: { color: NAVY } }], { x: M + 0.3, y: 1.65, w: CW - 0.6, h: 0.65, fontSize: 14, valign: "middle" });
  const c = [["Awareness · 20%", "Brand recall", "$10 to $20 per day", "South Miami's top-rated team, proven by 4.9 stars and real customer reviews."],
    ["Leads · 60%", "Prospecting", "$30 to $60 per day", "Maintenance, inspection and replacement ads; instant form against landing page, split evenly."],
    ["Leads · 20%", "Retargeting", "$10 to $20 per day", "People who visited sunnybliss.com or watched the brand video in the last 180 days."]];
  const cw = (CW - 2 * 0.3) / 3;
  c.forEach(([k, h, p, t], i) => {
    const x = M + i * (cw + 0.3);
    card(s, x, 2.6, cw, 2.9);
    tx(s, k.toUpperCase(), { x: x + 0.3, y: 2.8, w: cw - 0.6, h: 0.3, fontSize: 12, bold: true, color: MUTED, charSpacing: 2 });
    tx(s, h, { x: x + 0.3, y: 3.15, w: cw - 0.6, h: 0.45, fontSize: 20, bold: true, color: NAVY });
    tx(s, p, { x: x + 0.3, y: 3.65, w: cw - 0.6, h: 0.4, fontSize: 18, bold: true, color: RUST });
    tx(s, t, { x: x + 0.3, y: 4.15, w: cw - 0.6, h: 1.2, fontSize: 14 });
  });
  tx(s, [{ text: "Shared: ", options: { bold: true, color: NAVY } }, { text: "HVAC, plumbing and electrical ads in English and Spanish · residents of 21 ZIP codes, age 30 and over · feeds, Stories and Reels, without Audience Network · every lead measured in GoHighLevel." }],
    { x: M, y: 5.75, w: CW, h: 0.8, fontSize: 14 });
}

// 14 Incremental budget
{
  const s = content("03 · Strategy", "Budget", "Benchmark: WordStream/LocaliQ Facebook Ads Benchmarks 2026, home and home improvement",
    "Step 1 starts with the November 4 launch. If Step 1 targets are not met, the budget stays at $50 per day and the plan is corrected before any increase. One AC replacement from $5,800 covers nearly four months at the starting budget. Every change is made only with the owner's approval.");
  watermark(s, 8.6, 0.1, 4.3);
  tx(s, "Spend scales in three stages, each released by GoHighLevel results, to a $3,000 monthly maximum.", { x: M, y: 1.45, w: CW, h: 0.4, fontSize: 16 });
  const st = [["Step 1 · November", "$1,500", "$50 per day · about 20 leads", "Validation: lead delivery, five-minute response and booked estimates.", false],
    ["Step 2 · December", "$2,250", "$75 per day · about 30 leads", "Released when Step 1 books estimates at or below the target cost.", false],
    ["Step 3 · January · maximum", "$3,000", "$100 per day · about 40 leads", "Matches the August-October average; fixed ceiling.", true]];
  const cw = (CW - 2 * 0.3) / 3;
  st.forEach(([k, v, d, t, dark], i) => {
    const x = M + i * (cw + 0.3);
    dark ? box(s, x, 2.0, cw, 3.4, NAVY) : card(s, x, 2.0, cw, 3.4);
    tx(s, k.toUpperCase(), { x: x + 0.3, y: 2.2, w: cw - 0.6, h: 0.3, fontSize: 12, bold: true, color: dark ? YELLOW : MUTED, charSpacing: 2 });
    tx(s, v, { x: x + 0.3, y: 2.6, w: cw - 0.6, h: 0.95, fontSize: 48, bold: true, color: dark ? LIGHT : NAVY, valign: "middle" });
    tx(s, d, { x: x + 0.3, y: 3.65, w: cw - 0.6, h: 0.4, fontSize: 15, bold: true, color: dark ? YELLOW : RUST });
    tx(s, t, { x: x + 0.3, y: 4.15, w: cw - 0.6, h: 1.1, fontSize: 14, color: dark ? "CFDDF0" : INK });
  });
  tx(s, [{ text: "At every step: ", options: { bold: true, color: NAVY } }, { text: "20% awareness, 60% new homeowners, 20% website visitors · increases of no more than 20% per week · leads estimated at about $60 each, between the home-services median ($42.95) and this account's history ($74.92)." }],
    { x: M, y: 5.65, w: CW, h: 0.9, fontSize: 14 });
}

// 15 Timeline
{
  const s = content("03 · Strategy", "Timeline", "January: Step 3, up to $3,000, with rainy-season plumbing. February: pre-summer AC and storm readiness",
    "Every change in the account is logged the same day with its reason. The 70/30 shift happens only if one destination is at least 30% cheaper per booked estimate with ten or more leads on each side.");
  const cols = [["November · Validation", [["Nov 2-4", "Fixes, approvals and a test lead"], ["Nov 4", "Launch at $50 per day"], ["Nov 4-10", "Learning period, no edits"], ["Nov 11, 18", "Quality reviews in GoHighLevel"], ["Nov 23-29", "Thanksgiving week; budget held"]]],
    ["December · Optimization", [["Dec 1", "Step 2: $75 per day; electrical joins"], ["Dec 1-7", "Holiday and rainy-season creative"], ["Dec 15", "Six-week review; January plan"], ["Dec 21-31", "Holidays; emergency plumbing focus"], ["Dec 31", "Report on booked estimates and sales"]]]];
  const cw = (CW - 0.3) / 2;
  cols.forEach(([h, rows], i) => {
    const x = M + i * (cw + 0.3);
    card(s, x, 1.65, cw, 4.1);
    tx(s, h, { x: x + 0.35, y: 1.85, w: cw - 0.7, h: 0.45, fontSize: 20, bold: true, color: NAVY });
    rows.forEach(([d, t], j) => {
      const y = 2.45 + j * 0.62;
      tx(s, d, { x: x + 0.35, y, w: 1.4, h: 0.45, fontSize: 14, bold: true, color: RUST, valign: "middle" });
      tx(s, t, { x: x + 1.85, y, w: cw - 2.2, h: 0.45, fontSize: 14, valign: "middle" });
      if (j < rows.length - 1) s.addShape(pres.shapes.LINE, { x: x + 0.35, y: y + 0.55, w: cw - 0.7, h: 0, line: { color: "E3E8EF", width: 0.75 } });
    });
  });
  tx(s, "Monthly cycle, January-February:", { x: M, y: 6.05, w: 3.3, h: 0.45, fontSize: 15, bold: true, color: NAVY, valign: "middle" });
  ["Week 1 · Review", "Week 2 · New seasonal message", "Week 3 · Hold", "Week 4 · Owner report"].reduce((x, t) => {
    const w = 0.085 * t.length + 0.35;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 6.05, w, h: 0.45, fill: { color: TINT }, line: { color: LINE, width: 0.75 }, rectRadius: 0.2 });
    tx(s, t, { x, y: 6.05, w, h: 0.45, fontSize: 13, bold: true, color: NAVY, align: "center", valign: "middle" });
    return x + w + 0.15;
  }, M + 3.4);
}

// 16 Launch requirements
{
  const s = content("04 · Requirements", "Requirements", "Sunny Bliss Plumbing & Air · Meta advertising plan",
    "If an input arrives after November 3, launch moves by the same number of days. The campaign does not launch until a test lead reaches GoHighLevel with its source ad recorded.");
  watermark(s, 8.8, 3.6, 4.1);
  const rows = [["Item", "Owner", "When"], ["Approve the incremental budget ($1,500 to $3,000) and the qualified-lead definition", "Sunny Bliss", "Meeting"],
    ["Commit to a bilingual first call within five minutes", "Sunny Bliss", "Meeting"], ["Call the 6 waiting qualified leads; update the pipeline after every contact", "Sunny Bliss", "This week"],
    ["Approve the Bliss Care Plan and the three promotions", "Sunny Bliss", "Nov 3"], ["Share average ticket and close rate per service", "Sunny Bliss", "Nov 3"],
    ["Move recruiting ads to a separate page and pixel", "Sunny Bliss", "Nov 4"], ["Reconnect forms, record the source ad, rebuild landing pages, send a test lead", "Agency", "Nov 4"]];
  card(s, M, 1.6, CW, 3.85);
  s.addTable(rows.map((r, i) => r.map(c => ({ text: c, options: { bold: i === 0, color: i === 0 ? MUTED : NAVY } }))),
    { x: M + 0.25, y: 1.75, w: CW - 0.5, colW: [8.1, 1.9, CW - 0.5 - 10.0], fontSize: 13, border: { type: "solid", pt: 0.5, color: LINE }, margin: 0.06, rowH: 0.44 });
  box(s, M, 5.65, CW, 0.95, NAVY);
  tx(s, [{ text: "Success measure: ", options: { bold: true, color: YELLOW } }, { text: "cost per booked estimate in GoHighLevel. Proposed qualified lead: a homeowner in the 21 ZIP codes, reachable by phone, with a current need. Target cost: [$___].", options: { color: LIGHT } }],
    { x: M + 0.3, y: 5.72, w: CW - 0.6, h: 0.8, fontSize: 15, valign: "middle" });
}

pres.writeFile({ fileName: OUT }).then(f => console.log("wrote", f));
