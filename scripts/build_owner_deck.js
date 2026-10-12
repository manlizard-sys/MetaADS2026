// Builds the owner deck (PowerPoint) for the 2026-10-12 retrospective report. Run with NODE_PATH pointing to a node_modules that has pptxgenjs.
const pptxgen = require("pptxgenjs");
const path = require("path");
const { applyTheme } = require("/root/.claude/skills/synced/91214b57-4729-489d-a491-f28c7fe5eb8b_230bf34e-5a4e-4f30-a11c-45835a5a2a37/pptx/scripts/apply_theme.js");

const OUT = "/home/user/MetaADS2026/build/reports/informes/Informe_Meta_Ads_Orchid_2026-10-12.pptx";
const IMG = "/home/user/MetaADS2026/build/reports/previews/2026-10-12/";
const SIZE = { // px of each capture, to keep aspect ratio
  "V2-Small-Law-Firm-2026-Oct": [640, 1262], "V1-POV-Email-2026-Oct": [640, 1096], "S8-Comparison-Static-2026-Oct": [640, 1262],
  "S3-Vetting-Static-2026-Oct": [640, 1302], "C2-Hey-You-Offer-Carousel-2026-Oct": [640, 1142], "V3-Vetting-Process-2026-Oct": [640, 1302],
  "S6-What-VA-Does-Static-2026-Oct": [640, 1262], "V4-Founder-Story-2026-Oct": [640, 1256], "C1-Guilty-Carousel-2026-Oct": [640, 1102],
  "S1-Cost-Static-2026-Oct": [640, 1262],
};

const THEME = {
  name: "Orchid",
  headFontFace: "Cambria",
  bodyFontFace: "Calibri",
  colors: {
    dk1: "1F1235", lt1: "FFFFFF", dk2: "3B1C78", lt2: "F3F0FA",
    accent1: "F6C343", accent2: "3B1C78", accent3: "8B6FD1", accent4: "2E8B5E", accent5: "C8463A", accent6: "6B6680",
    hlink: "3B1C78", folHlink: "8B6FD1",
  },
};
const HEX = THEME.colors;

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9"; // 10 x 5.625 in
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.title = "Informe Meta Ads Orchid – Del 29 sep al 11 oct";
pres.author = "Orchid";
const C = pres.SchemeColor;

// ---------- Layouts ----------
pres.defineSlideMaster({
  title: "DARK_TITLE",
  background: { color: C.text2 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.6, y: 1.55, w: 8.8, h: 1.1, fontSize: 44, bold: true, color: C.background1, align: "left", valign: "bottom", margin: 0 }, text: "" } },
    { placeholder: { options: { name: "body", type: "body", x: 0.6, y: 2.8, w: 8.8, h: 1.2, fontSize: 18, color: C.accent1, align: "left", valign: "top", margin: 0 }, text: "" } },
  ],
});
const FOOT = { text: "Orchid · Informe Meta Ads · 29 sep – 11 oct 2026", options: { x: 0.5, y: 5.25, w: 6, h: 0.25, fontSize: 9, color: C.accent6, margin: 0 } };
pres.defineSlideMaster({
  title: "CONTENT",
  background: { color: C.background1 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.5, y: 0.3, w: 9, h: 0.75, fontSize: 30, bold: true, color: C.text2, align: "left", valign: "middle", margin: 0 }, text: "" } },
    { text: FOOT },
  ],
  slideNumber: { x: 9.1, y: 5.25, w: 0.4, h: 0.25, fontSize: 9, color: C.accent6, align: "right" },
});
pres.defineSlideMaster({
  title: "DARK_CONTENT",
  background: { color: C.text2 },
  objects: [
    { placeholder: { options: { name: "title", type: "title", x: 0.5, y: 0.3, w: 9, h: 0.75, fontSize: 30, bold: true, color: C.background1, align: "left", valign: "middle", margin: 0 }, text: "" } },
  ],
  slideNumber: { x: 9.1, y: 5.25, w: 0.4, h: 0.25, fontSize: 9, color: C.accent1, align: "right" },
});

// ---------- helpers ----------
const T = (s, text, o) => s.addText(text, { isTextBox: true, margin: 0, ...o });
function card(s, x, y, w, h, name, fill = C.background2) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, fill: { color: fill }, line: { color: fill }, rectRadius: 0.12, objectName: name });
}
function dot(s, x, y, label, name, fill = C.accent1, color = C.text2, d = 0.42) {
  s.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color: fill }, line: { color: fill }, objectName: name });
  T(s, label, { x, y, w: d, h: d, fontSize: 14, bold: true, color, align: "center", valign: "middle", objectName: name + " label" });
}
function capture(s, file, x, y, h, name) {
  const [pw, ph] = SIZE[file];
  const w = h * pw / ph;
  s.addImage({ path: IMG + file + ".png", x, y, w, h, objectName: name, altText: name,
    shadow: { type: "outer", color: "1F1235", opacity: 0.18, blur: 6, offset: 2, angle: 90 } });
  return w;
}
let S = 0;
const slide = (master, section) => pres.addSlide({ masterName: master, sectionTitle: section });

// ---------- 1. Title ----------
pres.addSection({ title: "Resumen" });
let s = slide("DARK_TITLE", "Resumen");
s.addText("Informe Meta Ads", { placeholder: "title" });
s.addText([
  { text: "Del 29 de septiembre al 11 de octubre de 2026", options: { breakLine: true } },
  { text: "Preparado para la dirección de Orchid · 12 de octubre de 2026", options: { fontSize: 14, color: C.background1 } },
], { placeholder: "body" });
s.addNotes("Informe de las dos primeras semanas de la campaña de Meta Ads de Orchid, con lo que se hizo, lo que aprendimos y las decisiones que necesitamos.");

// ---------- 2. Three numbers ----------
s = slide("CONTENT", "Resumen");
s.addText("Dos semanas en tres números", { placeholder: "title" });
const stats = [
  ["$487.54", "Inversión total en Meta", "29 sep – 11 oct"],
  ["1", "Lead que quiere contratar", "Llegó por el video V2 y agendó llamada"],
  ["$487.54", "Costo por lead calificado", "Inversión ÷ leads que quieren contratar"],
];
stats.forEach(([big, label, sub], i) => {
  const x = 0.5 + i * 3.07;
  card(s, x, 1.25, 2.86, 2.15, `Stat card ${i + 1}`);
  T(s, big, { x: x + 0.25, y: 1.45, w: 2.4, h: 0.95, fontSize: 44, bold: true, color: C.text2, fontFace: THEME.headFontFace, objectName: `Stat ${i + 1}` });
  T(s, label, { x: x + 0.25, y: 2.45, w: 2.4, h: 0.35, fontSize: 15, bold: true, color: C.text1, objectName: `Stat label ${i + 1}` });
  T(s, sub, { x: x + 0.25, y: 2.8, w: 2.4, h: 0.45, fontSize: 11, color: C.accent6, objectName: `Stat note ${i + 1}` });
});
T(s, [
  { text: "La semana 1 funcionó porque el presupuesto fue al video V2. ", options: { bold: true } },
  { text: "En la semana 2, Meta movió el dinero a un anuncio estático (S3) que atrajo a personas que buscaban trabajo. El 12 de octubre corregimos la audiencia, los anuncios activos y los textos." },
], { x: 0.5, y: 3.7, w: 9, h: 1.0, fontSize: 15, color: C.text1, valign: "top", objectName: "Summary" });
s.addNotes("Mensaje principal: en dos semanas, un solo lead real. La causa está identificada y corregida el 12 de octubre.");

// ---------- 3. Week vs week ----------
pres.addSection({ title: "Resultados" });
s = slide("CONTENT", "Resultados");
s.addText("Semana 2: menos de un tercio de los clics", { placeholder: "title" });
s.addChart(pres.charts.BAR, [
  { name: "Clics al enlace", labels: ["Semana 1 · 28 sep – 4 oct", "Semana 2 · 5 – 11 oct"], values: [183, 53] },
  { name: "Visitas a la página", labels: ["Semana 1 · 28 sep – 4 oct", "Semana 2 · 5 – 11 oct"], values: [145, 38] },
], {
  x: 0.4, y: 1.15, w: 4.6, h: 3.85, barDir: "col", barGrouping: "clustered", objectName: "Clicks chart",
  chartColors: [HEX.dk2, HEX.accent3],
  showValue: true, dataLabelPosition: "outEnd", dataLabelFontSize: 12, dataLabelColor: HEX.dk1, dataLabelFontFace: "+mn-lt",
  catAxisLabelFontFace: "+mn-lt", catAxisLabelFontSize: 11, catAxisLabelColor: HEX.accent6,
  valAxisHidden: true, valGridLine: { style: "none" }, catGridLine: { style: "none" },
  showLegend: true, legendPos: "b", legendFontSize: 11, legendFontFace: "+mn-lt", legendColor: HEX.accent6,
});
const rows = [
  ["", "Semana 1", "Semana 2"],
  ["Inversión", "$211.04", "$276.50"],
  ["Costo por mil impresiones", "$74.49", "$115.40"],
  ["% que hace clic (CTR)", "6.46%", "2.21%"],
  ["Leads según Meta", "2", "2"],
  ["Quieren contratar (GHL)", "1", "0"],
  ["Buscan trabajo (GHL)", "0", "3"],
];
s.addTable(rows.map((r, i) => r.map((c, j) => ({
  text: c, options: {
    bold: i === 0 || (i === 5), color: i === 0 ? HEX.lt1 : (i === 5 && j > 0 ? HEX.accent4 : (i === 6 && j === 2 ? HEX.accent5 : HEX.dk1)),
    fill: { color: i === 0 ? HEX.dk2 : (i % 2 ? HEX.lt1 : HEX.lt2) }, align: j ? "right" : "left", valign: "middle",
  },
}))), { x: 5.3, y: 1.25, w: 4.2, colW: [2.2, 1.0, 1.0], rowH: 0.42, fontSize: 12, fontFace: THEME.bodyFontFace, border: { type: "none" }, margin: [0, 0.08, 0, 0.08], objectName: "Week table" });
T(s, "La semana 1 tuvo 6 días con anuncios: la campaña arrancó el martes 29.", { x: 5.3, y: 4.35, w: 4.2, h: 0.4, fontSize: 10, color: C.accent6, italic: true, objectName: "Week note" });
s.addNotes("Con un gasto parecido, la semana 2 bajó de 183 a 53 clics y de 145 a 38 visitas a la página, y no trajo ningún lead que quisiera contratar.");

// ---------- 4. Lead quality ----------
s = slide("CONTENT", "Resultados");
s.addText("3 de cada 4 leads de anuncios buscaban trabajo", { placeholder: "title" });
s.addChart(pres.charts.DOUGHNUT, [{ name: "Leads", labels: ["Buscan trabajo", "Quieren contratar"], values: [3, 1] }], {
  x: 0.4, y: 1.15, w: 3.5, h: 3.6, holeSize: 62, chartColors: [HEX.accent5, HEX.accent4], objectName: "Lead quality chart",
  showValue: true, showPercent: false, dataLabelColor: HEX.lt1, dataLabelFontSize: 16, dataLabelFontFace: "+mn-lt",
  showLegend: true, legendPos: "b", legendFontSize: 11, legendFontFace: "+mn-lt", legendColor: HEX.accent6,
});
const leads = [
  ["4 oct", "V2 Small Law Firm · video", "Quiere contratar · agendó", C.accent4],
  ["5 oct", "C2 Hey You Offer · carrusel", "Busca trabajo", C.accent5],
  ["8 oct", "S3 Vetting · estático", "Busca trabajo", C.accent5],
  ["11 oct", "S3 Vetting · estático", "Busca trabajo", C.accent5],
];
leads.forEach(([d, ad, res, col], i) => {
  const y = 1.25 + i * 0.62;
  card(s, 4.2, y, 5.3, 0.52, `Lead row ${i + 1}`);
  T(s, d, { x: 4.35, y, w: 0.7, h: 0.52, fontSize: 12, bold: true, color: C.text2, valign: "middle", objectName: `Lead date ${i + 1}` });
  T(s, ad, { x: 5.05, y, w: 2.45, h: 0.52, fontSize: 12, color: C.text1, valign: "middle", objectName: `Lead ad ${i + 1}` });
  T(s, res, { x: 7.5, y, w: 1.9, h: 0.52, fontSize: 12, bold: true, color: col, valign: "middle", align: "right", objectName: `Lead result ${i + 1}` });
});
T(s, [
  { text: "Por confirmar: ", options: { bold: true } },
  { text: "la noche del 11 de octubre entraron 3 contactos que quieren contratar y agendaron, pero GHL no registra que vinieran de un anuncio." },
], { x: 4.2, y: 3.85, w: 5.3, h: 0.75, fontSize: 12, color: C.text1, valign: "top", objectName: "Unattributed note" });
s.addNotes("Quien busca trabajo suele mentir en las demás preguntas del formulario; la única que lo delata es 'Hiring or job seeking'. Meta cuenta a todos como lead, por eso medimos con GHL.");

// ---------- 5. Timeline ----------
pres.addSection({ title: "Qué hicimos" });
s = slide("CONTENT", "Qué hicimos");
s.addText("Qué pasó en la cuenta, día por día", { placeholder: "title" });
const events = [
  ["29 sep", "Lanzamiento", "4 videos y 2 carruseles hacia go.orchidpros.com/hire."],
  ["1 oct", "Más variedad", "Se suman 8 anuncios estáticos (S1–S8)."],
  ["11 oct", "Cambio manual", "El equipo pausa los videos y deja solo 3 estáticos activos."],
  ["12 oct", "Correcciones", "Medimos con GHL y corregimos audiencia, anuncios y textos."],
];
s.addShape(pres.shapes.LINE, { x: 0.9, y: 1.86, w: 8.2, h: 0, line: { color: C.accent3, width: 2 }, objectName: "Timeline line" });
events.forEach(([d, head, body], i) => {
  const x = 0.5 + i * 2.3;
  dot(s, x + 0.19, 1.65, String(i + 1), `Timeline dot ${i + 1}`, i === 3 ? C.accent1 : C.text2, i === 3 ? C.text2 : C.background1);
  T(s, d, { x, y: 2.25, w: 2.1, h: 0.35, fontSize: 13, bold: true, color: C.accent3, objectName: `Timeline date ${i + 1}` });
  T(s, head, { x, y: 2.6, w: 2.1, h: 0.4, fontSize: 17, bold: true, color: C.text2, fontFace: THEME.headFontFace, objectName: `Timeline head ${i + 1}` });
  T(s, body, { x, y: 3.05, w: 2.05, h: 1.1, fontSize: 13, color: C.text1, valign: "top", objectName: `Timeline body ${i + 1}` });
});
s.addNotes("El 11 de octubre se pausó el video V2, el único que trajo un cliente; no quedó registrado el motivo.");

// ---------- 6. Fixes of Oct 12 ----------
s = slide("CONTENT", "Qué hicimos");
s.addText("Las correcciones del 12 de octubre", { placeholder: "title" });
const fixes = [
  ["Audiencia", ["Apagamos Advantage+ Audience: Meta estaba llegando a personas de 18–34 años.", "Edad fija de 30 a 65 años.", "Solo personas que viven en EE. UU."]],
  ["Anuncios", ["Reactivamos V2, el único que trajo un cliente real.", "Reactivamos V1, el de mejor tasa de clics.", "Pausamos S1 y S6; S8 sigue activo."]],
  ["Textos", ["La primera línea le habla a quien contrata: \"Law firm owners:\", \"Business owners:\".", "Precio visible: desde $1,000/mes.", "Sin palabras de empleo."]],
];
fixes.forEach(([head, items], i) => {
  const x = 0.5 + i * 3.07;
  card(s, x, 1.2, 2.86, 3.35, `Fix card ${i + 1}`);
  dot(s, x + 0.25, 1.4, String(i + 1), `Fix dot ${i + 1}`);
  T(s, head, { x: x + 0.8, y: 1.4, w: 1.9, h: 0.42, fontSize: 18, bold: true, color: C.text2, fontFace: THEME.headFontFace, valign: "middle", objectName: `Fix head ${i + 1}` });
  T(s, items.map((t, k) => ({ text: t, options: { bullet: true, breakLine: k < items.length - 1 } })), {
    x: x + 0.25, y: 2.0, w: 2.45, h: 2.4, fontSize: 13, color: C.text1, valign: "top", paraSpaceAfter: 6, objectName: `Fix body ${i + 1}` });
});
T(s, "También intentamos excluir intereses de empleo (Indeed, Job hunting): Meta ya no lo permite.", { x: 0.5, y: 4.7, w: 9, h: 0.35, fontSize: 11, italic: true, color: C.accent6, objectName: "Exclusions note" });
s.addNotes("Además, el equipo simplificó el formulario de GHL el mismo día.");

// ---------- 7. Learnings ----------
pres.addSection({ title: "Aprendizajes" });
s = slide("CONTENT", "Aprendizajes");
s.addText("Qué aprendimos", { placeholder: "title" });
const learn = [
  ["El video para abogados (V2) es el único anuncio que trajo un cliente real.", "Recibió el 82% del presupuesto en la semana 1 y solo el 21% en la semana 2."],
  ["El estático S3 atrajo a quien busca trabajo.", "Gastó $207.45 en la semana 2, con CTR de 1.6%; sus 2 leads buscaban empleo."],
  ["El \"lead\" que reporta Meta no mide el éxito.", "Desde ahora medimos con GHL: leads que quieren contratar y su costo."],
  ["V1 y V4 tienen las mejores tasas de clic (23–29%), pero casi no recibieron presupuesto.", "Todavía no sabemos si traen clientes; V1 vuelve a estar activo para probarlo."],
];
learn.forEach(([head, body], i) => {
  const y = 1.15 + i * 0.98;
  dot(s, 0.5, y + 0.05, String(i + 1), `Learning dot ${i + 1}`);
  T(s, head, { x: 1.15, y, w: 8.35, h: 0.42, fontSize: 16, bold: true, color: C.text2, valign: "middle", objectName: `Learning head ${i + 1}` });
  T(s, body, { x: 1.15, y: y + 0.42, w: 8.35, h: 0.4, fontSize: 13, color: C.text1, valign: "top", objectName: `Learning body ${i + 1}` });
});
s.addNotes("Advantage+ Audience también gastaba en personas de 18 a 34 años; ya está apagado.");

// ---------- 8. Active ads ----------
pres.addSection({ title: "Anuncios" });
s = slide("CONTENT", "Anuncios");
s.addText("Los 3 anuncios activos, con el texto nuevo", { placeholder: "title" });
const active = [
  ["V2-Small-Law-Firm-2026-Oct", "V2 Small Law Firm · video", "$230.30 · 133 clics", "1 quiere contratar (agendó)", C.accent4],
  ["V1-POV-Email-2026-Oct", "V1 POV Email · video", "$3.05 · 34 clics", "Sin leads aún; a prueba", C.accent6],
  ["S8-Comparison-Static-2026-Oct", "S8 Comparison · estático", "$2.62 · 1 clic", "Sin leads aún", C.accent6],
];
active.forEach(([file, name, nums, res, col], i) => {
  const x = 0.5 + i * 3.07;
  const w = capture(s, file, x, 1.15, 2.95, `Capture ${name}`);
  const tx = x + w + 0.15, tw = 2.86 - w - 0.15;
  T(s, name, { x: tx, y: 1.2, w: tw, h: 0.7, fontSize: 13, bold: true, color: C.text2, valign: "top", objectName: `Active name ${i + 1}` });
  T(s, nums, { x: tx, y: 1.95, w: tw, h: 0.55, fontSize: 12, color: C.text1, valign: "top", objectName: `Active nums ${i + 1}` });
  T(s, res, { x: tx, y: 2.55, w: tw, h: 0.7, fontSize: 12, bold: true, color: col, valign: "top", objectName: `Active result ${i + 1}` });
});
T(s, "Cifras acumuladas del 29 sep al 11 oct. En los videos se ve la portada.", { x: 0.5, y: 4.3, w: 9, h: 0.3, fontSize: 10, italic: true, color: C.accent6, objectName: "Active note" });
s.addNotes("Las capturas muestran cómo se ve cada anuncio en el feed del celular desde el 12 de octubre.");

// ---------- 9. Job-seeker ads ----------
s = slide("CONTENT", "Anuncios");
s.addText("Los que trajeron buscadores de empleo", { placeholder: "title" });
const bad = [
  ["S3-Vetting-Static-2026-Oct", "S3 Vetting · estático", "$220.20 · 35 clics · CTR 1.6%", "2 buscan trabajo", "Se llevó el 75% del presupuesto de la semana 2."],
  ["C2-Hey-You-Offer-Carousel-2026-Oct", "C2 Hey You Offer · carrusel", "$11.19 · 12 clics", "1 busca trabajo", "Promete un \"regalo\" que atrae curiosos."],
];
bad.forEach(([file, name, nums, res, why], i) => {
  const x = 0.5 + i * 4.6;
  const w = capture(s, file, x, 1.15, 3.6, `Capture ${name}`);
  const tx = x + w + 0.2, tw = 4.4 - w - 0.2;
  T(s, name, { x: tx, y: 1.25, w: tw, h: 0.4, fontSize: 15, bold: true, color: C.text2, objectName: `Bad name ${i + 1}` });
  T(s, nums, { x: tx, y: 1.7, w: tw, h: 0.5, fontSize: 12, color: C.text1, valign: "top", objectName: `Bad nums ${i + 1}` });
  T(s, res, { x: tx, y: 2.25, w: tw, h: 0.35, fontSize: 13, bold: true, color: C.accent5, objectName: `Bad result ${i + 1}` });
  T(s, why, { x: tx, y: 2.65, w: tw, h: 0.9, fontSize: 12, color: C.text1, valign: "top", objectName: `Bad why ${i + 1}` });
  T(s, "Pausado", { x: tx, y: 3.6, w: tw, h: 0.3, fontSize: 11, bold: true, color: C.accent6, objectName: `Bad status ${i + 1}` });
});
s.addNotes("Ninguno de los dos trajo a alguien que quisiera contratar.");

// ---------- 10. Other paused ads ----------
s = slide("CONTENT", "Anuncios");
s.addText("Otros anuncios pausados", { placeholder: "title" });
const others = [
  ["V3-Vetting-Process-2026-Oct", "V3 Vetting Process", "$12.43 · 6 clics"],
  ["S6-What-VA-Does-Static-2026-Oct", "S6 What VA Does", "$4.76 · 2 clics"],
  ["V4-Founder-Story-2026-Oct", "V4 Founder Story", "$2.42 · 12 clics"],
  ["C1-Guilty-Carousel-2026-Oct", "C1 Guilty", "$0.52 · 1 clic"],
  ["S1-Cost-Static-2026-Oct", "S1 Cost", "$0.05 · 0 clics"],
];
others.forEach(([file, name, nums], i) => {
  const x = 0.5 + i * 1.84;
  const [pw, ph] = SIZE[file];
  const h = 2.9, w = h * pw / ph;
  capture(s, file, x + (1.64 - w) / 2, 1.15, h, `Capture ${name}`);
  T(s, name, { x, y: 4.15, w: 1.64, h: 0.3, fontSize: 12, bold: true, color: C.text2, align: "center", objectName: `Other name ${i + 1}` });
  T(s, nums, { x, y: 4.45, w: 1.64, h: 0.3, fontSize: 11, color: C.text1, align: "center", objectName: `Other nums ${i + 1}` });
});
s.addNotes("Ninguno trajo leads. S6 se pausó porque 'What does a Virtual Assistant do?' también le habla a quien busca ese trabajo.");

// ---------- 11. Plan ----------
pres.addSection({ title: "Próximos pasos" });
s = slide("CONTENT", "Próximos pasos");
s.addText("Plan para esta semana (12 – 18 oct)", { placeholder: "title" });
const plan = [
  ["Dejar que Meta aprenda", "No tocar la campaña durante 5 días. Solo pausar un anuncio si gasta unos $120 sin traer un lead que quiera contratar."],
  ["Medir cada lead en GHL", "La alerta diaria (martes a viernes) separa a quien quiere contratar de quien busca trabajo, por anuncio."],
  ["Subir creativos nuevos", "Con \"For Law Firm Owners\" o \"For Business Owners\" sobre la imagen. En el video de V2, cambiar \"19 jobs\" por \"19 roles\"."],
];
plan.forEach(([head, body], i) => {
  const x = 0.5 + i * 3.07;
  card(s, x, 1.2, 2.86, 3.3, `Plan card ${i + 1}`);
  dot(s, x + 0.25, 1.45, String(i + 1), `Plan dot ${i + 1}`, C.text2, C.background1, 0.5);
  T(s, head, { x: x + 0.25, y: 2.15, w: 2.4, h: 0.6, fontSize: 17, bold: true, color: C.text2, fontFace: THEME.headFontFace, valign: "top", objectName: `Plan head ${i + 1}` });
  T(s, body, { x: x + 0.25, y: 2.8, w: 2.4, h: 1.6, fontSize: 13, color: C.text1, valign: "top", objectName: `Plan body ${i + 1}` });
});
s.addNotes("El próximo informe sale el lunes 19 de octubre con la semana del 12 al 18.");

// ---------- 12. Decisions ----------
s = slide("DARK_CONTENT", "Próximos pasos");
s.addText("Decisiones que necesitamos de ustedes", { placeholder: "title" });
const dec = [
  ["Origen de 3 contactos", "¿Los 3 contactos que agendaron la noche del 11 de octubre vinieron de otro canal o fueron pruebas del formulario?"],
  ["Costo máximo por lead calificado", "¿Cuánto están dispuestos a pagar por cada lead que quiere contratar? Ese número define cuándo escalar o pausar."],
  ["Evento \"Lead\" solo para compradores", "¿Aprueban que GHL avise a Meta de un lead solo cuando la persona responde \"I want to hire.\"? Así Meta aprende de compradores."],
];
dec.forEach(([head, body], i) => {
  const y = 1.25 + i * 1.25;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.5, y: y + 0.05, w: 0.38, h: 0.38, fill: { color: C.text2 }, line: { color: C.accent1, width: 2 }, rectRadius: 0.06, objectName: `Decision box ${i + 1}` });
  T(s, head, { x: 1.1, y, w: 8.4, h: 0.45, fontSize: 18, bold: true, color: C.accent1, valign: "middle", objectName: `Decision head ${i + 1}` });
  T(s, body, { x: 1.1, y: y + 0.47, w: 8.4, h: 0.65, fontSize: 14, color: C.background1, valign: "top", objectName: `Decision body ${i + 1}` });
});
s.addNotes("Con estas tres respuestas podemos fijar metas claras para las próximas semanas.");

(async () => {
  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("written", OUT);
})();
