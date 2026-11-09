// Builds the owner deck (PowerPoint) for the week of 2026-11-02 to 2026-11-08 (delivered 2026-11-09). Run with NODE_PATH pointing to a node_modules that has pptxgenjs.
const pptxgen = require("pptxgenjs");
const path = require("path");
const { applyTheme } = require("/root/.claude/skills/synced/91214b57-4729-489d-a491-f28c7fe5eb8b_230bf34e-5a4e-4f30-a11c-45835a5a2a37/pptx/scripts/apply_theme.js");

const OUT = "/home/user/MetaADS2026/build/reports/informes/Informe_Meta_Ads_Orchid_2026-11-09.pptx";
const IMG = "/home/user/MetaADS2026/build/reports/previews/2026-11-09/";
const SIZE = { // px of each capture, to keep aspect ratio
  "A1-0Upfront-Black-Nov01": [640, 1262], "B1-GetStartedFree-Color-Nov01": [640, 1302],
  "V1-POVEmail-Lead-Nov01": [640, 1102], "V1-POVEmail-Legal-Nov01": [640, 992],
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
pres.title = "Informe Meta Ads Orchid – Semana del 2 al 8 nov";
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
const FOOT = { text: "Orchid · Informe Meta Ads · Semana 2 – 8 nov 2026", options: { x: 0.5, y: 5.25, w: 6, h: 0.25, fontSize: 9, color: C.accent6, margin: 0 } };
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

const tbl = (rows, opt, hl = {}) => rows.map((r, i) => r.map((c, j) => ({
  text: c, options: {
    bold: i === 0 || hl[`${i}`] === "bold", color: i === 0 ? HEX.lt1 : (hl[`${i},${j}`] || HEX.dk1),
    fill: { color: i === 0 ? HEX.dk2 : (i % 2 ? HEX.lt1 : HEX.lt2) }, align: j ? "right" : "left", valign: "middle", ...opt,
  },
})));

const tb = (rows, hl = {}) => rows.map((r, i) => r.map((c, j) => ({
  text: c, options: {
    bold: i === 0, color: i === 0 ? HEX.lt1 : (hl[`${i},${j}`] || HEX.dk1),
    fill: { color: i === 0 ? HEX.dk2 : (i % 2 ? HEX.lt1 : HEX.lt2) }, align: j ? "right" : "left", valign: "middle",
  },
})));
const TBL = { fontFace: THEME.bodyFontFace, border: { type: "none" }, margin: [0, 0.08, 0, 0.08] };

// ---------- 1. Title ----------
pres.addSection({ title: "Resumen" });
let s = slide("DARK_TITLE", "Resumen");
s.addText("Informe Meta Ads", { placeholder: "title" });
s.addText([
  { text: "Semana del 2 al 8 nov 2026", options: { breakLine: true } },
  { text: "Reporte de desempeño · Dirección de Orchid · 9 nov 2026", options: { fontSize: 14, color: C.background1 } },
], { placeholder: "body" });
s.addNotes("Primera semana de la estructura de noviembre: awareness con video (20%) y leads hacia las landings de 50% off (80%), $1,000/mes continuo.");

// ---------- 2. Executive summary ----------
s = slide("CONTENT", "Resumen");
s.addText("Resumen ejecutivo", { placeholder: "title" });
[["$304.10", "Inversión", "2 – 8 nov · awareness + leads"], ["1", "Lead calificado", "Immigration law · agendó llamada"], ["3,445", "Vieron el 50% del video", "Público para retargeting"]]
  .forEach(([big, label, sub], i) => {
    const x = 0.5 + i * 3.07;
    card(s, x, 1.25, 2.86, 2.15, `Stat card ${i + 1}`);
    T(s, big, { x: x + 0.25, y: 1.45, w: 2.4, h: 0.95, fontSize: 44, bold: true, color: C.text2, fontFace: THEME.headFontFace, objectName: `Stat ${i + 1}` });
    T(s, label, { x: x + 0.25, y: 2.45, w: 2.4, h: 0.35, fontSize: 15, bold: true, color: C.text1, objectName: `Stat label ${i + 1}` });
    T(s, sub, { x: x + 0.25, y: 2.8, w: 2.4, h: 0.45, fontSize: 11, color: C.accent6, objectName: `Stat note ${i + 1}` });
  });
T(s, [
  { text: "El video funciona; la campaña de leads todavía no. ", options: { bold: true } },
  { text: "Awareness llegó a 5,228 personas con CPM de $6. Leads trajo un lead calificado el primer día y ninguno del 3 al 8 nov: CPM $161 y $15 por clic. El 9 nov se dejó solo en el feed de Facebook con público Advantage+." },
], { x: 0.5, y: 3.7, w: 9, h: 1.0, fontSize: 14, color: C.text1, valign: "top", objectName: "Summary" });
s.addNotes("Noviembre al 8: $304.10 de $1,000. El lead calificado llegó por B1; su primer contacto fue V2 en octubre.");

// ---------- 3. By campaign ----------
pres.addSection({ title: "Resultados" });
s = slide("CONTENT", "Resultados");
s.addText("Resultados por campaña", { placeholder: "title" });
s.addChart(pres.charts.DOUGHNUT, [{ name: "Inversión", labels: ["Awareness · video", "Leads · landings 50% off"], values: [47.42, 256.68] }], {
  x: 0.4, y: 1.15, w: 4.2, h: 3.85, objectName: "Spend split chart", holeSize: 55,
  chartColors: [HEX.accent3, HEX.dk2], showPercent: true, showValue: false, dataLabelColor: HEX.lt1, dataLabelFontSize: 12, dataLabelFontFace: "+mn-lt",
  showLegend: true, legendPos: "b", legendFontSize: 11, legendFontFace: "+mn-lt", legendColor: HEX.accent6,
  showTitle: true, title: "Inversión de la semana", titleFontSize: 12, titleColor: HEX.accent6, titleFontFace: "+mn-lt",
});
s.addTable(tb([
  ["", "Awareness", "Leads"],
  ["Inversión", "$47.42", "$256.68"],
  ["Personas alcanzadas", "5,228", "904"],
  ["CPM", "$6.03", "$160.93"],
  ["Clics en el enlace", "3", "17"],
  ["Visitas a la landing", "0", "9"],
  ["Costo por visita", "—", "$28.52"],
  ["ThruPlay (video visto)", "1,418", "—"],
  ["Leads calificados (GHL)", "—", "1"],
], { "3,2": HEX.accent5, "6,2": HEX.accent5, "8,2": HEX.accent4 }),
{ x: 4.9, y: 1.15, w: 4.6, colW: [2.4, 1.1, 1.1], rowH: 0.36, fontSize: 12, ...TBL, objectName: "Campaign table" });
T(s, "Semana anterior (26 oct – 1 nov, 4 días de prueba A/B/C): $205.40, 6 visitas, 0 leads calificados.", { x: 4.9, y: 4.5, w: 4.6, h: 0.45, fontSize: 10, color: C.accent6, italic: true, valign: "top", objectName: "Campaign note" });
s.addNotes("Awareness no busca clics: su trabajo es crear el público que ya vio el video para luego mostrarle la oferta.");

// ---------- 4. Daily + leads ----------
s = slide("CONTENT", "Resultados");
s.addText("Entrega diaria de leads", { placeholder: "title" });
s.addTable(tb([
  ["Día", "Gasto", "Clics", "Visitas", "Nota"],
  ["Lun 2", "$59.42", "7", "4", "1 lead calificado (B1); horario 6am–10pm"],
  ["Mar 3", "$30.03", "1", "0", "Se quita Facebook Reels"],
  ["Mié 4", "$25.60", "2", "3", ""],
  ["Jue 5", "$34.00", "3", "1", ""],
  ["Vie 6", "$36.71", "3", "1", ""],
  ["Sáb 7", "$35.89", "1", "0", ""],
  ["Dom 8", "$35.03", "0", "0", ""],
], { "1,4": HEX.accent4 }).map(r => r.map((c, j) => (j === 4 ? { ...c, options: { ...c.options, align: "left" } } : c))),
{ x: 0.5, y: 1.15, w: 5.9, colW: [0.9, 0.85, 0.65, 0.75, 2.75], rowH: 0.38, fontSize: 11, ...TBL, objectName: "Daily table" });
card(s, 6.6, 1.15, 2.9, 3.4, "Leads card");
T(s, "Leads en GHL", { x: 6.8, y: 1.3, w: 2.5, h: 0.3, fontSize: 14, bold: true, color: C.text2, objectName: "Leads head" });
T(s, [
  { text: "2 nov · B1 Get Started Free", options: { bold: true, breakLine: true } },
  { text: "\"I want to hire\" · Immigration law · agendó llamada", options: { color: HEX.accent4, breakLine: true } },
  { text: "Primer contacto: video V2 en octubre.", options: { breakLine: true } },
  { text: " ", options: { breakLine: true, fontSize: 6 } },
  { text: "3 – 8 nov", options: { bold: true, breakLine: true } },
  { text: "Ningún lead nuevo, ni calificado ni buscador de empleo.", options: { breakLine: true } },
], { x: 6.8, y: 1.7, w: 2.55, h: 2.7, fontSize: 11, color: C.text1, valign: "top", objectName: "Leads body" });
T(s, "Meta recibió el lead calificado por la API de Conversiones: ya puede optimizar con esa señal.", { x: 0.5, y: 4.3, w: 5.9, h: 0.35, fontSize: 10, italic: true, color: C.accent6, objectName: "Daily note" });
s.addNotes("Awareness gastó entre $5.72 y $7.69 por día, estable toda la semana.");

// ---------- 5. Timeline ----------
pres.addSection({ title: "Qué hicimos" });
s = slide("CONTENT", "Qué hicimos");
s.addText("Cronología de cambios", { placeholder: "title" });
const events = [
  ["1 nov", "Nueva estructura", "Awareness con video en 6 verticales (20%) y leads con A1, B1 y V1 hacia las landings de 50% off (80%)."],
  ["2 nov", "Horario", "Leads solo de 6am a 10pm hora local: el 65% del primer día se había gastado de madrugada."],
  ["2 nov", "Medición", "El formulario envía Lead a Meta y GHL envía el lead calificado por la API de Conversiones."],
  ["3 nov", "Ubicaciones", "Se quita Facebook Reels: 24% del gasto y 0 clics."],
  ["9 nov", "Advantage+", "Leads solo en el feed de Facebook, con público Advantage+ guiado por intereses legales."],
];
s.addShape(pres.shapes.LINE, { x: 0.8, y: 1.86, w: 8.4, h: 0, line: { color: C.accent3, width: 2 }, objectName: "Timeline line" });
events.forEach(([d, head, body], i) => {
  const x = 0.5 + i * 1.84;
  dot(s, x + 0.1, 1.65, String(i + 1), `Timeline dot ${i + 1}`, i === 4 ? C.accent1 : C.text2, i === 4 ? C.text2 : C.background1);
  T(s, d, { x, y: 2.25, w: 1.7, h: 0.35, fontSize: 13, bold: true, color: C.accent3, objectName: `Timeline date ${i + 1}` });
  T(s, head, { x, y: 2.6, w: 1.7, h: 0.45, fontSize: 15, bold: true, color: C.text2, fontFace: THEME.headFontFace, objectName: `Timeline head ${i + 1}` });
  T(s, body, { x, y: 3.1, w: 1.7, h: 1.8, fontSize: 11, color: C.text1, valign: "top", objectName: `Timeline body ${i + 1}` });
});
s.addNotes("Detalle y motivo de cada cambio en build/CHANGELOG_META.md.");

// ---------- 6. Ads of the week ----------
pres.addSection({ title: "Anuncios" });
s = slide("CONTENT", "Anuncios");
s.addText("Creativos de la semana", { placeholder: "title" });
const week = [
  ["B1-GetStartedFree-Color-Nov01", "B1 Get Started Free", "$220.46 · 15 clics", "1 lead calificado", C.accent4],
  ["A1-0Upfront-Black-Nov01", "A1 $0 Upfront", "$35.18 · 2 clics", "1 visita · 0 leads", C.accent6],
  ["V1-POVEmail-Lead-Nov01", "V1 POV Email · leads", "$1.04", "Meta casi no lo mostró", C.accent5],
  ["V1-POVEmail-Legal-Nov01", "V1 POV Email · awareness", "$47.42 · 6 verticales", "$0.033 por ThruPlay", C.accent4],
];
week.forEach(([file, name, nums, res, col], i) => {
  const x = 0.5 + i * 2.3;
  const [pw, ph] = SIZE[file];
  const h = 2.75, w = h * pw / ph;
  capture(s, file, x + (2.1 - w) / 2, 1.1, h, `Capture ${name}`);
  T(s, name, { x, y: 3.95, w: 2.1, h: 0.3, fontSize: 12, bold: true, color: C.text2, align: "center", objectName: `Week name ${i + 1}` });
  T(s, nums, { x, y: 4.25, w: 2.1, h: 0.28, fontSize: 11, color: C.text1, align: "center", objectName: `Week nums ${i + 1}` });
  T(s, res, { x, y: 4.53, w: 2.1, h: 0.28, fontSize: 11, bold: true, color: col, align: "center", objectName: `Week res ${i + 1}` });
});
s.addNotes("B1 se llevó el 86% del gasto de leads. Meta reparte hacia el anuncio que mejor responde en los primeros días.");

// ---------- 7. Awareness ----------
s = slide("CONTENT", "Anuncios");
s.addText("Video de awareness por vertical", { placeholder: "title" });
s.addTable(tb([
  ["Vertical", "Gasto", "Alcance", "ThruPlay", "$ / ThruPlay"],
  ["Healthcare", "$7.99", "979", "274", "$0.029"],
  ["Finance", "$7.90", "1,098", "240", "$0.033"],
  ["Entrepreneurs", "$7.89", "1,177", "232", "$0.034"],
  ["Real Estate", "$7.91", "1,154", "234", "$0.034"],
  ["Accounting", "$7.78", "1,064", "217", "$0.036"],
  ["Legal", "$7.95", "1,117", "221", "$0.036"],
], { "1,4": HEX.accent4, "6,4": HEX.accent5 }),
{ x: 0.5, y: 1.15, w: 5.0, colW: [1.5, 0.8, 0.9, 0.9, 0.9], rowH: 0.38, fontSize: 11, ...TBL, objectName: "Vertical table" });
s.addChart(pres.charts.BAR, [{ name: "Personas", labels: ["Inició", "25%", "50%", "75%", "100%"], values: [7712, 5747, 3445, 2270, 1379] }], {
  x: 5.8, y: 1.1, w: 3.8, h: 3.3, barDir: "col", objectName: "Retention chart", chartColors: [HEX.accent3],
  showValue: true, dataLabelPosition: "outEnd", dataLabelFontSize: 10, dataLabelColor: HEX.dk1, dataLabelFontFace: "+mn-lt", dataLabelFormatCode: "#,##0",
  catAxisLabelFontFace: "+mn-lt", catAxisLabelFontSize: 10, catAxisLabelColor: HEX.accent6,
  valAxisHidden: true, valGridLine: { style: "none" }, catGridLine: { style: "none" }, showLegend: false,
  showTitle: true, title: "Reproducciones del video", titleFontSize: 12, titleColor: HEX.accent6, titleFontFace: "+mn-lt",
});
T(s, "La diferencia entre verticales es pequeña: con $8 por vertical todavía no hay un ganador claro. Se decide el 16 nov.", { x: 0.5, y: 4.0, w: 5.0, h: 0.6, fontSize: 11, italic: true, color: C.accent6, valign: "top", objectName: "Vertical note" });
s.addNotes("45% de quienes inician el video llegan a la mitad y 18% lo terminan. Es un buen nivel para un video de 11 segundos en frío.");

// ---------- 8. Placements ----------
s = slide("CONTENT", "Anuncios");
s.addText("Ubicaciones de la campaña de leads", { placeholder: "title" });
s.addTable(tb([
  ["Ubicación", "Gasto", "CPM", "Clics", "Visitas"],
  ["Facebook feed", "$154.95", "$139", "14", "7"],
  ["Instagram feed", "$49.32", "$177", "1", "1"],
  ["Instagram Reels", "$21.38", "$264", "2", "1"],
  ["Facebook Reels (quitado 3 nov)", "$19.55", "$268", "0", "0"],
  ["Facebook Stories", "$8.66", "$787", "0", "0"],
  ["Instagram Stories", "$2.07", "$65", "0", "0"],
], { "1,3": HEX.accent4, "1,4": HEX.accent4, "5,2": HEX.accent5 }),
{ x: 0.5, y: 1.15, w: 5.6, colW: [2.4, 0.9, 0.8, 0.7, 0.8], rowH: 0.4, fontSize: 11, ...TBL, objectName: "Placement table" });
card(s, 6.4, 1.15, 3.1, 3.3, "Placement card");
T(s, [
  { text: "60%", options: { fontSize: 36, bold: true, color: HEX.dk2, breakLine: true } },
  { text: "del gasto fue al feed de Facebook, que trajo 14 de 17 clics y 7 de 9 visitas.", options: { breakLine: true } },
  { text: " ", options: { breakLine: true, fontSize: 6 } },
  { text: "$101 ", options: { bold: true, color: HEX.accent5 } },
  { text: "en Instagram, Reels y Stories trajeron 2 visitas. Desde el 9 nov los leads corren solo en el feed de Facebook." },
], { x: 6.6, y: 1.3, w: 2.75, h: 3.0, fontSize: 12, color: C.text1, valign: "top", objectName: "Placement body" });
s.addNotes("Las imágenes de A1 y B1 son 4:5; en Reels y Stories se ven recortadas y compiten con video vertical.");

// ---------- 9. Learnings ----------
pres.addSection({ title: "Aprendizajes" });
s = slide("CONTENT", "Aprendizajes");
s.addText("Hallazgos", { placeholder: "title" });
const learn = [
  ["El video de awareness es barato y retiene.", "CPM $6 y $0.033 por ThruPlay. 3,445 personas vieron al menos la mitad: ese es el público para retargeting."],
  ["La campaña de leads llega a muy poca gente y cara.", "Público manual con intereses legales Y dueños de negocio: 904 personas, CPM $161, $15 por clic."],
  ["El feed de Facebook es la única ubicación que trae visitas.", "7 de 9 visitas. Instagram, Reels y Stories gastaron $101 con 2 visitas."],
  ["La medición ya funciona de punta a punta.", "Lead en el formulario y lead calificado por la API de Conversiones: Meta ya sabe quién es un buen lead."],
];
learn.forEach(([head, body], i) => {
  const y = 1.15 + i * 0.98;
  dot(s, 0.5, y + 0.05, String(i + 1), `Learning dot ${i + 1}`);
  T(s, head, { x: 1.15, y, w: 8.35, h: 0.42, fontSize: 16, bold: true, color: C.text2, valign: "middle", objectName: `Learning head ${i + 1}` });
  T(s, body, { x: 1.15, y: y + 0.42, w: 8.35, h: 0.4, fontSize: 13, color: C.text1, valign: "top", objectName: `Learning body ${i + 1}` });
});
s.addNotes("Con ~$25/día en leads Meta no llega a 50 conversiones semanales; por eso conviene un público más amplio y un solo conjunto.");

// ---------- 10. Conclusions ----------
pres.addSection({ title: "Conclusiones" });
s = slide("CONTENT", "Conclusiones");
s.addText("Conclusiones", { placeholder: "title" });
const good = [
  ["Video de awareness", "5,228 personas a CPM $6; buena retención."],
  ["B1 \"Get started free\"", "El único lead calificado y 8 de 9 visitas."],
  ["Medición", "Lead y lead calificado llegan a Meta sin duplicados."],
  ["Horario 6am – 10pm", "Sin gasto de madrugada desde el 2 nov."],
];
const bad = [
  ["Costo por clic en leads", "$15 por clic y $28.52 por visita."],
  ["Público de leads", "Demasiado chico (904 personas): CPM alto."],
  ["Instagram y Stories", "$101 con 2 visitas."],
  ["Volumen de leads", "0 leads del 3 al 8 nov."],
];
[[good, "Funciona", C.accent4, 0.5], [bad, "No funciona", C.accent5, 5.1]].forEach(([items, head, col, x], k) => {
  T(s, head, { x, y: 1.15, w: 4.4, h: 0.4, fontSize: 18, bold: true, color: col, fontFace: THEME.headFontFace, objectName: `Conclusion head ${k + 1}` });
  items.forEach(([h, b], i) => {
    const y = 1.65 + i * 0.85;
    card(s, x, y, 4.4, 0.75, `Conclusion card ${k + 1}.${i + 1}`);
    s.addShape(pres.shapes.OVAL, { x: x + 0.15, y: y + 0.27, w: 0.2, h: 0.2, fill: { color: col }, line: { color: col }, objectName: `Conclusion dot ${k + 1}.${i + 1}` });
    T(s, h, { x: x + 0.5, y: y + 0.06, w: 3.8, h: 0.3, fontSize: 13, bold: true, color: C.text2, objectName: `Conclusion title ${k + 1}.${i + 1}` });
    T(s, b, { x: x + 0.5, y: y + 0.36, w: 3.8, h: 0.36, fontSize: 11, color: C.text1, valign: "top", objectName: `Conclusion body ${k + 1}.${i + 1}` });
  });
});
s.addNotes("El lead calificado del 2 nov tuvo como primer contacto un video: refuerza la apuesta por video + retargeting.");

// ---------- 11. Plan ----------
pres.addSection({ title: "Próximos pasos" });
s = slide("CONTENT", "Próximos pasos");
s.addText("Plan · 9 – 15 nov", { placeholder: "title" });
const plan = [
  ["Leads: feed + Advantage+", "Aplicado el 9 nov. No se toca hasta el jueves 12: Meta está reaprendiendo."],
  ["Retargeting del video", "Público de quienes vieron el 50% y un conjunto de ~$7/día con la oferta. Mismo total mensual."],
  ["Revisión 16 nov", "Verticales de awareness, resultado del retargeting y entrada de los creativos A2 y B2."],
];
plan.forEach(([head, body], i) => {
  const x = 0.5 + i * 3.07;
  card(s, x, 1.2, 2.86, 3.3, `Plan card ${i + 1}`);
  dot(s, x + 0.25, 1.45, String(i + 1), `Plan dot ${i + 1}`, C.text2, C.background1, 0.5);
  T(s, head, { x: x + 0.25, y: 2.15, w: 2.4, h: 0.6, fontSize: 17, bold: true, color: C.text2, fontFace: THEME.headFontFace, valign: "top", objectName: `Plan head ${i + 1}` });
  T(s, body, { x: x + 0.25, y: 2.8, w: 2.4, h: 1.6, fontSize: 13, color: C.text1, valign: "top", objectName: `Plan body ${i + 1}` });
});
s.addNotes("Noviembre al 8 nov: $304.10 de $1,000. Próximo reporte: lunes 16 nov (semana 9 – 15 nov).");

(async () => {
  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("written", OUT);
})();
