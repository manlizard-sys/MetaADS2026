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
  { text: "Periodo: 29 sep – 11 oct 2026", options: { breakLine: true } },
  { text: "Reporte de desempeño · Dirección de Orchid · 12 oct 2026", options: { fontSize: 14, color: C.background1 } },
], { placeholder: "body" });
s.addNotes("Desempeño de la campaña Leads – Hire VA, semanas 1 y 2: resultados, calidad de leads, cambios, hallazgos y decisiones pendientes.");

// ---------- 2. Three numbers ----------
s = slide("CONTENT", "Resumen");
s.addText("Resumen ejecutivo", { placeholder: "title" });
const stats = [
  ["$487.54", "Inversión", "29 sep – 11 oct"],
  ["1", "Lead calificado", "V2 · llamada agendada"],
  ["$487.54", "CPL calificado", "Inversión ÷ leads calificados"],
];
stats.forEach(([big, label, sub], i) => {
  const x = 0.5 + i * 3.07;
  card(s, x, 1.25, 2.86, 2.15, `Stat card ${i + 1}`);
  T(s, big, { x: x + 0.25, y: 1.45, w: 2.4, h: 0.95, fontSize: 44, bold: true, color: C.text2, fontFace: THEME.headFontFace, objectName: `Stat ${i + 1}` });
  T(s, label, { x: x + 0.25, y: 2.45, w: 2.4, h: 0.35, fontSize: 15, bold: true, color: C.text1, objectName: `Stat label ${i + 1}` });
  T(s, sub, { x: x + 0.25, y: 2.8, w: 2.4, h: 0.45, fontSize: 11, color: C.accent6, objectName: `Stat note ${i + 1}` });
});
T(s, [
  { text: "Semana 1: delivery concentrado en V2 (82% del gasto). ", options: { bold: true } },
  { text: "Semana 2: el algoritmo reasignó el 75% del gasto a S3 (estático), con tráfico de baja intención y 0 leads calificados. Ajustes de segmentación, creativos y copy aplicados el 12 oct." },
], { x: 0.5, y: 3.7, w: 9, h: 1.0, fontSize: 15, color: C.text1, valign: "top", objectName: "Summary" });
s.addNotes("1 lead calificado en 2 semanas. Causa identificada (reasignación de presupuesto a S3) y corregida el 12 oct.");

// ---------- 3. Week vs week ----------
pres.addSection({ title: "Resultados" });
s = slide("CONTENT", "Resultados");
s.addText("Semana 2: −71% en clics con +31% de inversión", { placeholder: "title" });
s.addChart(pres.charts.BAR, [
  { name: "Clics en el enlace", labels: ["Semana 1 · 28 sep – 4 oct", "Semana 2 · 5 – 11 oct"], values: [183, 53] },
  { name: "Landing page views", labels: ["Semana 1 · 28 sep – 4 oct", "Semana 2 · 5 – 11 oct"], values: [145, 38] },
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
  ["CPM", "$74.49", "$115.40"],
  ["CTR (enlace)", "6.46%", "2.21%"],
  ["Leads (Meta)", "2", "2"],
  ["Leads calificados (GHL)", "1", "0"],
  ["Leads no calificados (GHL)", "0", "3"],
];
s.addTable(rows.map((r, i) => r.map((c, j) => ({
  text: c, options: {
    bold: i === 0 || (i === 5), color: i === 0 ? HEX.lt1 : (i === 5 && j > 0 ? HEX.accent4 : (i === 6 && j === 2 ? HEX.accent5 : HEX.dk1)),
    fill: { color: i === 0 ? HEX.dk2 : (i % 2 ? HEX.lt1 : HEX.lt2) }, align: j ? "right" : "left", valign: "middle",
  },
}))), { x: 5.3, y: 1.25, w: 4.2, colW: [2.2, 1.0, 1.0], rowH: 0.42, fontSize: 12, fontFace: THEME.bodyFontFace, border: { type: "none" }, margin: [0, 0.08, 0, 0.08], objectName: "Week table" });
T(s, "Semana 1: 6 días de delivery (inicio 29 sep).", { x: 5.3, y: 4.35, w: 4.2, h: 0.4, fontSize: 10, color: C.accent6, italic: true, objectName: "Week note" });
s.addNotes("Semana 2: CTR 6.46% → 2.21%, CPM $74.49 → $115.40, 0 leads calificados.");

// ---------- 4. Lead quality ----------
s = slide("CONTENT", "Resultados");
s.addText("Calidad de leads: 75% no calificados", { placeholder: "title" });
s.addChart(pres.charts.DOUGHNUT, [{ name: "Leads", labels: ["No calificado (busca empleo)", "Calificado"], values: [3, 1] }], {
  x: 0.4, y: 1.15, w: 3.5, h: 3.6, holeSize: 62, chartColors: [HEX.accent5, HEX.accent4], objectName: "Lead quality chart",
  showValue: true, showPercent: false, dataLabelColor: HEX.lt1, dataLabelFontSize: 16, dataLabelFontFace: "+mn-lt",
  showLegend: true, legendPos: "b", legendFontSize: 11, legendFontFace: "+mn-lt", legendColor: HEX.accent6,
});
const leads = [
  ["4 oct", "V2 Small Law Firm · video", "Calificado · agendado", C.accent4],
  ["5 oct", "C2 Hey You Offer · carrusel", "No calificado", C.accent5],
  ["8 oct", "S3 Vetting · estático", "No calificado", C.accent5],
  ["11 oct", "S3 Vetting · estático", "No calificado", C.accent5],
];
leads.forEach(([d, ad, res, col], i) => {
  const y = 1.25 + i * 0.62;
  card(s, 4.2, y, 5.3, 0.52, `Lead row ${i + 1}`);
  T(s, d, { x: 4.35, y, w: 0.7, h: 0.52, fontSize: 12, bold: true, color: C.text2, valign: "middle", objectName: `Lead date ${i + 1}` });
  T(s, ad, { x: 5.05, y, w: 2.45, h: 0.52, fontSize: 12, color: C.text1, valign: "middle", objectName: `Lead ad ${i + 1}` });
  T(s, res, { x: 7.5, y, w: 1.9, h: 0.52, fontSize: 12, bold: true, color: col, valign: "middle", align: "right", objectName: `Lead result ${i + 1}` });
});
T(s, [
  { text: "Pendiente: ", options: { bold: true } },
  { text: "3 leads calificados del 11 oct sin atribución (tráfico directo, sin UTM)." },
], { x: 4.2, y: 3.85, w: 5.3, h: 0.75, fontSize: 12, color: C.text1, valign: "top", objectName: "Unattributed note" });
s.addNotes("El campo 'Hiring or job seeking' es el único filtro confiable; las demás respuestas de los no calificados son inconsistentes. KPI: lead calificado en GHL.");

// ---------- 5. Timeline ----------
pres.addSection({ title: "Qué hicimos" });
s = slide("CONTENT", "Qué hicimos");
s.addText("Cronología de cambios", { placeholder: "title" });
const events = [
  ["29 sep", "Lanzamiento", "Campaña ABO, objetivo Leads. 4 videos y 2 carruseles."],
  ["1 oct", "Expansión creativa", "+8 estáticos (S1–S8)."],
  ["11 oct", "Cambio manual", "Pausa de videos y carruseles; activos solo S1, S6 y S8."],
  ["12 oct", "Optimización", "Integración con GHL; ajustes de segmentación, creativos y copy."],
];
s.addShape(pres.shapes.LINE, { x: 0.9, y: 1.86, w: 8.2, h: 0, line: { color: C.accent3, width: 2 }, objectName: "Timeline line" });
events.forEach(([d, head, body], i) => {
  const x = 0.5 + i * 2.3;
  dot(s, x + 0.19, 1.65, String(i + 1), `Timeline dot ${i + 1}`, i === 3 ? C.accent1 : C.text2, i === 3 ? C.text2 : C.background1);
  T(s, d, { x, y: 2.25, w: 2.1, h: 0.35, fontSize: 13, bold: true, color: C.accent3, objectName: `Timeline date ${i + 1}` });
  T(s, head, { x, y: 2.6, w: 2.1, h: 0.4, fontSize: 17, bold: true, color: C.text2, fontFace: THEME.headFontFace, objectName: `Timeline head ${i + 1}` });
  T(s, body, { x, y: 3.05, w: 2.05, h: 1.1, fontSize: 13, color: C.text1, valign: "top", objectName: `Timeline body ${i + 1}` });
});
s.addNotes("11 oct: se pausó V2, único anuncio con lead calificado. Motivo no documentado.");

// ---------- 6. Fixes of Oct 12 ----------
s = slide("CONTENT", "Qué hicimos");
s.addText("Optimización del 12 oct", { placeholder: "title" });
const fixes = [
  ["Audiencia", ["Advantage+ Audience desactivado (gasto en 18–34).", "Edad 30–65 como límite estricto.", "Ubicación: residentes en EE. UU."]],
  ["Anuncios", ["V2 reactivado (único con lead calificado).", "V1 reactivado (CTR 28%).", "S1 y S6 pausados; S8 activo."]],
  ["Copy", ["Hook dirigido al comprador (\"Law firm owners:\").", "Precio visible: desde $1,000/mes.", "Sin términos asociados a empleo."]],
];
fixes.forEach(([head, items], i) => {
  const x = 0.5 + i * 3.07;
  card(s, x, 1.2, 2.86, 3.35, `Fix card ${i + 1}`);
  dot(s, x + 0.25, 1.4, String(i + 1), `Fix dot ${i + 1}`);
  T(s, head, { x: x + 0.8, y: 1.4, w: 1.9, h: 0.42, fontSize: 18, bold: true, color: C.text2, fontFace: THEME.headFontFace, valign: "middle", objectName: `Fix head ${i + 1}` });
  T(s, items.map((t, k) => ({ text: t, options: { bullet: true, breakLine: k < items.length - 1 } })), {
    x: x + 0.25, y: 2.0, w: 2.45, h: 2.4, fontSize: 13, color: C.text1, valign: "top", paraSpaceAfter: 6, objectName: `Fix body ${i + 1}` });
});
T(s, "Exclusión de intereses de empleo no disponible: Meta retiró las exclusiones de segmentación detallada.", { x: 0.5, y: 4.7, w: 9, h: 0.35, fontSize: 11, italic: true, color: C.accent6, objectName: "Exclusions note" });
s.addNotes("Formulario de GHL simplificado el mismo día.");

// ---------- 7. Learnings ----------
pres.addSection({ title: "Aprendizajes" });
s = slide("CONTENT", "Aprendizajes");
s.addText("Hallazgos", { placeholder: "title" });
const learn = [
  ["V2 es el único creativo con lead calificado.", "Share de gasto: 82% en semana 1, 21% en semana 2."],
  ["S3 genera tráfico de baja intención.", "$207.45 en semana 2, CTR 1.6%, 2 leads no calificados."],
  ["El evento Lead de Meta no refleja calidad.", "3 de 4 leads atribuidos no calificados. KPI: CPL calificado (GHL)."],
  ["V1 y V4: CTR de 23–29% con gasto marginal.", "Sin volumen para evaluar conversión; V1 reactivado en prueba."],
];
learn.forEach(([head, body], i) => {
  const y = 1.15 + i * 0.98;
  dot(s, 0.5, y + 0.05, String(i + 1), `Learning dot ${i + 1}`);
  T(s, head, { x: 1.15, y, w: 8.35, h: 0.42, fontSize: 16, bold: true, color: C.text2, valign: "middle", objectName: `Learning head ${i + 1}` });
  T(s, body, { x: 1.15, y: y + 0.42, w: 8.35, h: 0.4, fontSize: 13, color: C.text1, valign: "top", objectName: `Learning body ${i + 1}` });
});
s.addNotes("Advantage+ Audience asignaba gasto fuera del rango 30–65; desactivado.");

// ---------- 8. Active ads ----------
pres.addSection({ title: "Anuncios" });
s = slide("CONTENT", "Anuncios");
s.addText("Creativos activos (copy v3)", { placeholder: "title" });
const active = [
  ["V2-Small-Law-Firm-2026-Oct", "V2 Small Law Firm · video", "$230.30 · 133 clics", "1 lead calificado (agendado)", C.accent4],
  ["V1-POV-Email-2026-Oct", "V1 POV Email · video", "$3.05 · 34 clics", "Sin leads · en prueba", C.accent6],
  ["S8-Comparison-Static-2026-Oct", "S8 Comparison · estático", "$2.62 · 1 clic", "Sin leads", C.accent6],
];
active.forEach(([file, name, nums, res, col], i) => {
  const x = 0.5 + i * 3.07;
  const w = capture(s, file, x, 1.15, 2.95, `Capture ${name}`);
  const tx = x + w + 0.15, tw = 2.86 - w - 0.15;
  T(s, name, { x: tx, y: 1.2, w: tw, h: 0.7, fontSize: 13, bold: true, color: C.text2, valign: "top", objectName: `Active name ${i + 1}` });
  T(s, nums, { x: tx, y: 1.95, w: tw, h: 0.55, fontSize: 12, color: C.text1, valign: "top", objectName: `Active nums ${i + 1}` });
  T(s, res, { x: tx, y: 2.55, w: tw, h: 0.7, fontSize: 12, bold: true, color: col, valign: "top", objectName: `Active result ${i + 1}` });
});
T(s, "Acumulado 29 sep – 11 oct. En videos se muestra la miniatura.", { x: 0.5, y: 4.3, w: 9, h: 0.3, fontSize: 10, italic: true, color: C.accent6, objectName: "Active note" });
s.addNotes("Vista previa en feed móvil con el copy vigente desde el 12 oct.");

// ---------- 9. Job-seeker ads ----------
s = slide("CONTENT", "Anuncios");
s.addText("Creativos con leads no calificados", { placeholder: "title" });
const bad = [
  ["S3-Vetting-Static-2026-Oct", "S3 Vetting · estático", "$220.20 · 35 clics · CTR 1.6%", "2 leads no calificados", "75% del gasto de la semana 2."],
  ["C2-Hey-You-Offer-Carousel-2026-Oct", "C2 Hey You Offer · carrusel", "$11.19 · 12 clics", "1 lead no calificado", "Oferta tipo \"regalo\": tráfico de baja intención."],
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
s.addNotes("0 leads calificados entre ambos.");

// ---------- 10. Other paused ads ----------
s = slide("CONTENT", "Anuncios");
s.addText("Creativos pausados sin conversiones", { placeholder: "title" });
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
s.addNotes("Sin leads. S6 pausado: el hook 'What does a Virtual Assistant do?' también atrae candidatos.");

// ---------- 11. Conclusions ----------
pres.addSection({ title: "Conclusiones" });
s = slide("CONTENT", "Conclusiones");
s.addText("Conclusiones: qué funciona y qué no", { placeholder: "title" });
const good = [
  ["Video vertical por segmento", "CTR 6.2% (video) vs. 1.9% (estático). V2 (legal) genera el único lead calificado."],
  ["Filtro de calificación", "\"Hiring or job seeking\" identificó los 3 leads no calificados."],
  ["Medición con GHL", "KPI de calidad por anuncio; reemplaza al evento Lead de Meta."],
  ["Segmentación estricta", "30–65, residentes en EE. UU., sin expansión de Advantage+."],
];
const bad2 = [
  ["Estáticos genéricos de \"VA\"", "S3: 45% del gasto total, 0 leads calificados."],
  ["Optimización por evento Lead", "Meta optimiza hacia quien completa el formulario, calificado o no."],
  ["Volumen creativo insuficiente", "3 creativos activos y 2 segmentos: sin margen para Andromeda."],
  ["Conversión de landing", "2.2% de landing page views a lead. Cambios manuales sin registro (11 oct)."],
];
[[good, "Funciona", C.accent4, 0.5], [bad2, "No funciona", C.accent5, 5.1]].forEach(([items, head, col, x], k) => {
  T(s, head, { x, y: 1.15, w: 4.4, h: 0.4, fontSize: 18, bold: true, color: col, fontFace: THEME.headFontFace, objectName: `Conclusion head ${k + 1}` });
  items.forEach(([h, b], i) => {
    const y = 1.65 + i * 0.85;
    card(s, x, y, 4.4, 0.75, `Conclusion card ${k + 1}.${i + 1}`);
    s.addShape(pres.shapes.OVAL, { x: x + 0.15, y: y + 0.27, w: 0.2, h: 0.2, fill: { color: col }, line: { color: col }, objectName: `Conclusion dot ${k + 1}.${i + 1}` });
    T(s, h, { x: x + 0.5, y: y + 0.06, w: 3.8, h: 0.3, fontSize: 13, bold: true, color: C.text2, objectName: `Conclusion title ${k + 1}.${i + 1}` });
    T(s, b, { x: x + 0.5, y: y + 0.36, w: 3.8, h: 0.36, fontSize: 11, color: C.text1, valign: "top", objectName: `Conclusion body ${k + 1}.${i + 1}` });
  });
});
s.addNotes("Prioridad: aumentar volumen y diversidad creativa por segmento, y optimizar por lead calificado en lugar del evento Lead genérico.");

// ---------- 12. Andromeda ----------
pres.addSection({ title: "Estrategia creativa" });
s = slide("CONTENT", "Estrategia creativa");
s.addText("Andromeda: el creativo define la audiencia", { placeholder: "title" });
const andr = [
  ["Selección por creativo", "Andromeda, el sistema de recuperación de anuncios de Meta, decide a quién mostrar cada anuncio según su contenido: texto, imagen y audio."],
  ["Agrupación de similares", "Creativos parecidos se agrupan y compiten como uno solo. Variaciones menores no amplían el alcance."],
  ["Diversidad = exploración", "Cada concepto distinto abre un segmento nuevo. Con pocos conceptos, el sistema concentra el gasto en uno (caso S3)."],
];
andr.forEach(([h, b], i) => {
  const y = 1.2 + i * 1.12;
  dot(s, 0.5, y + 0.02, String(i + 1), `Andromeda dot ${i + 1}`);
  T(s, h, { x: 1.1, y, w: 4.9, h: 0.4, fontSize: 16, bold: true, color: C.text2, valign: "middle", objectName: `Andromeda head ${i + 1}` });
  T(s, b, { x: 1.1, y: y + 0.4, w: 4.9, h: 0.65, fontSize: 12, color: C.text1, valign: "top", objectName: `Andromeda body ${i + 1}` });
});
card(s, 6.4, 1.2, 3.1, 3.35, "Creative gap card", C.text2);
T(s, "Situación actual", { x: 6.65, y: 1.4, w: 2.6, h: 0.3, fontSize: 12, color: C.accent1, bold: true, objectName: "Gap label 1" });
T(s, "3", { x: 6.65, y: 1.7, w: 2.6, h: 0.75, fontSize: 48, bold: true, color: C.background1, fontFace: THEME.headFontFace, objectName: "Gap now" });
T(s, "creativos activos · 2 segmentos", { x: 6.65, y: 2.45, w: 2.6, h: 0.3, fontSize: 12, color: C.background1, objectName: "Gap now label" });
T(s, "Requerido", { x: 6.65, y: 2.95, w: 2.6, h: 0.3, fontSize: 12, color: C.accent1, bold: true, objectName: "Gap label 2" });
T(s, "8–10", { x: 6.65, y: 3.25, w: 2.6, h: 0.75, fontSize: 48, bold: true, color: C.background1, fontFace: THEME.headFontFace, objectName: "Gap target" });
T(s, "conceptos distintos, en 9:16 y 4:5", { x: 6.65, y: 4.0, w: 2.6, h: 0.3, fontSize: 12, color: C.background1, objectName: "Gap target label" });
s.addNotes("El volumen recomendado (8–10 conceptos) es un rango operativo, no una cifra oficial de Meta. La clave es que cada concepto sea realmente distinto: segmento, ángulo o formato.");

// ---------- 13. Creative structure ----------
s = slide("CONTENT", "Estrategia creativa");
s.addText("Estructura creativa requerida", { placeholder: "title" });
const conc = [
  ["", "Segmento", "Ángulo", "Formato", "Hook (0–3 s / imagen)"],
  ["1", "Firmas legales", "Carga operativa: intake, agenda, seguimiento", "Video 9:16 + 4:5", "\"For Law Firm Owners\""],
  ["2", "Inmigración", "Case flow: armado de expedientes", "Video demo", "\"Immigration attorneys:\""],
  ["3", "Realtors / team leads", "ISA que llama leads a diario", "Video 9:16", "\"For Realtors\""],
  ["4", "Dueños de negocio", "Costo vs. contratación local (−60%)", "Estático 4:5", "\"Local hire vs. Orchid\""],
  ["5", "Dueños de negocio", "Precio: $1,450 setup + desde $1,000/mes", "Estático 1:1", "\"VA pricing, no surprises\""],
  ["6", "Todos", "Testimonio de cliente (KW)", "Video testimonial", "Cliente en cámara, 1er segundo"],
  ["7", "Todos", "Proceso de selección y garantía", "Video founder", "\"How we vet your assistant\""],
  ["8", "Healthcare / back office", "Recepción y administración", "Carrusel", "\"For Medical Offices\""],
];
s.addTable(conc.map((r, i) => r.map((c, j) => ({
  text: c, options: { bold: i === 0 || j === 0, color: i === 0 ? HEX.lt1 : (j === 0 ? HEX.dk2 : HEX.dk1),
    fill: { color: i === 0 ? HEX.dk2 : (i % 2 ? HEX.lt1 : HEX.lt2) }, valign: "middle", align: j === 0 ? "center" : "left" },
}))), { x: 0.5, y: 1.1, w: 9, colW: [0.35, 1.7, 3.05, 1.5, 2.4], rowH: 0.36, fontSize: 10.5, fontFace: THEME.bodyFontFace, border: { type: "none" }, margin: [0, 0.06, 0, 0.06], objectName: "Creative matrix" });
T(s, [
  { text: "Requisitos por pieza: ", options: { bold: true } },
  { text: "hook que nombre al comprador en los primeros 3 s, texto en pantalla, subtítulos, CTA \"Book a free call\", sin términos de empleo y una versión por placement (9:16 y 4:5)." },
], { x: 0.5, y: 4.45, w: 9, h: 0.6, fontSize: 11, color: C.text1, valign: "top", objectName: "Creative specs" });
s.addNotes("Prioridad de producción: conceptos 1, 3 y 6. Los conceptos 4 y 5 pueden reutilizar S8 y S1 con el hook corregido.");

// ---------- 11. Plan ----------
pres.addSection({ title: "Próximos pasos" });
s = slide("CONTENT", "Próximos pasos");
s.addText("Plan · 12 – 18 oct", { placeholder: "title" });
const plan = [
  ["Fase de aprendizaje", "Sin cambios durante 5 días. Criterio de pausa: ~$120 de gasto sin lead calificado."],
  ["Medición en GHL", "Reporte diario de leads calificados vs. no calificados por anuncio."],
  ["Producción creativa", "Conceptos 1, 3 y 6 de la matriz como prioridad. V2: reemplazar \"19 jobs\" por \"19 roles\"."],
];
plan.forEach(([head, body], i) => {
  const x = 0.5 + i * 3.07;
  card(s, x, 1.2, 2.86, 3.3, `Plan card ${i + 1}`);
  dot(s, x + 0.25, 1.45, String(i + 1), `Plan dot ${i + 1}`, C.text2, C.background1, 0.5);
  T(s, head, { x: x + 0.25, y: 2.15, w: 2.4, h: 0.6, fontSize: 17, bold: true, color: C.text2, fontFace: THEME.headFontFace, valign: "top", objectName: `Plan head ${i + 1}` });
  T(s, body, { x: x + 0.25, y: 2.8, w: 2.4, h: 1.6, fontSize: 13, color: C.text1, valign: "top", objectName: `Plan body ${i + 1}` });
});
s.addNotes("Próximo reporte: lunes 19 oct (semana 12–18 oct).");

// ---------- 12. Decisions ----------
s = slide("DARK_CONTENT", "Próximos pasos");
s.addText("Decisiones requeridas", { placeholder: "title" });
const dec = [
  ["Atribución de 3 leads del 11 oct", "Confirmar si provienen de otro canal o de pruebas del formulario."],
  ["CPL calificado objetivo", "Definir el máximo aceptable. Determina los umbrales de escalado y pausa."],
  ["Optimización por lead calificado", "Aprobar el envío del evento Lead vía CAPI solo cuando la respuesta es \"I want to hire.\"."],
];
dec.forEach(([head, body], i) => {
  const y = 1.25 + i * 1.25;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.5, y: y + 0.05, w: 0.38, h: 0.38, fill: { color: C.text2 }, line: { color: C.accent1, width: 2 }, rectRadius: 0.06, objectName: `Decision box ${i + 1}` });
  T(s, head, { x: 1.1, y, w: 8.4, h: 0.45, fontSize: 18, bold: true, color: C.accent1, valign: "middle", objectName: `Decision head ${i + 1}` });
  T(s, body, { x: 1.1, y: y + 0.47, w: 8.4, h: 0.65, fontSize: 14, color: C.background1, valign: "top", objectName: `Decision body ${i + 1}` });
});
s.addNotes("Insumos necesarios para fijar metas de las próximas semanas.");

(async () => {
  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("written", OUT);
})();
