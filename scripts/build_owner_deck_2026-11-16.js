// Builds the owner deck (PowerPoint) for the week of 2026-11-09 to 2026-11-15 (delivered 2026-11-16). Run with NODE_PATH pointing to a node_modules that has pptxgenjs.
const pptxgen = require("pptxgenjs");
const path = require("path");
const { applyTheme } = require("/root/.claude/skills/synced/91214b57-4729-489d-a491-f28c7fe5eb8b_230bf34e-5a4e-4f30-a11c-45835a5a2a37/pptx/scripts/apply_theme.js");

const OUT = "/home/user/MetaADS2026/build/reports/informes/Informe_Meta_Ads_Orchid_2026-11-16.pptx";
const IMG = "/home/user/MetaADS2026/build/reports/previews/2026-11-16/";
const SIZE = { // px of each image, to keep aspect ratio
  "hc_4x5": [640, 800], "ent_4x5": [640, 800], "ig_3x4": [640, 853],
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
pres.title = "Informe Meta Ads Orchid – Semana del 9 al 15 nov";
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
const FOOT = { text: "Orchid · Informe Meta Ads · Semana 9 – 15 nov 2026", options: { x: 0.5, y: 5.25, w: 6, h: 0.25, fontSize: 9, color: C.accent6, margin: 0 } };
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
  { text: "Semana del 9 al 15 nov 2026", options: { breakLine: true } },
  { text: "Reporte de desempeño y lanzamiento Black Friday · Dirección de Orchid · 16 nov 2026", options: { fontSize: 14, color: C.background1 } },
], { placeholder: "body" });
s.addNotes("Semana de cierre de la etapa de abogados y preparación del lanzamiento de Black Friday por mercado (salud y emprendedores), activo desde el 16 nov.");

// ---------- 2. Executive summary ----------
s = slide("CONTENT", "Resumen");
s.addText("Resumen ejecutivo", { placeholder: "title" });
[["$224.76", "Inversión", "9 – 15 nov · abogados + awareness"], ["0", "Leads calificados", "1 lead de abogados: buscaba empleo"], ["4,770", "Personas alcanzadas", "Video de awareness a CPM $6"]]
  .forEach(([big, label, sub], i) => {
    const x = 0.5 + i * 3.07;
    card(s, x, 1.25, 2.86, 2.15, `Stat card ${i + 1}`);
    T(s, big, { x: x + 0.25, y: 1.45, w: 2.4, h: 0.95, fontSize: 44, bold: true, color: C.text2, fontFace: THEME.headFontFace, objectName: `Stat ${i + 1}` });
    T(s, label, { x: x + 0.25, y: 2.45, w: 2.4, h: 0.35, fontSize: 15, bold: true, color: C.text1, objectName: `Stat label ${i + 1}` });
    T(s, sub, { x: x + 0.25, y: 2.8, w: 2.4, h: 0.45, fontSize: 11, color: C.accent6, objectName: `Stat note ${i + 1}` });
  });
T(s, [
  { text: "Abogados no respondió; el cambio va a salud y emprendedores. ", options: { bold: true } },
  { text: "La campaña de abogados gastó $176 con CPM de $296 y su único lead buscaba empleo, así que quedó en pausa. Desde hoy corren campañas separadas para salud y emprendedores con la oferta de Black Friday, más retargeting y seguidores de Instagram." },
], { x: 0.5, y: 3.7, w: 9, h: 1.0, fontSize: 14, color: C.text1, valign: "top", objectName: "Summary" });
s.addNotes("Noviembre al 15: $529.62 de $1,000. Plan 16–30 nov: $469.50.");

// ---------- 3. By campaign ----------
pres.addSection({ title: "Resultados" });
s = slide("CONTENT", "Resultados");
s.addText("Resultados por campaña", { placeholder: "title" });
s.addChart(pres.charts.DOUGHNUT, [{ name: "Inversión", labels: ["Awareness · video", "Abogados · leads"], values: [48.27, 176.49] }], {
  x: 0.4, y: 1.15, w: 4.2, h: 3.85, objectName: "Spend split chart", holeSize: 55,
  chartColors: [HEX.accent3, HEX.dk2], showPercent: true, showValue: false, dataLabelColor: HEX.lt1, dataLabelFontSize: 12, dataLabelFontFace: "+mn-lt",
  showLegend: true, legendPos: "b", legendFontSize: 11, legendFontFace: "+mn-lt", legendColor: HEX.accent6,
  showTitle: true, title: "Inversión de la semana", titleFontSize: 12, titleColor: HEX.accent6, titleFontFace: "+mn-lt",
});
s.addTable(tb([
  ["", "Awareness", "Abogados"],
  ["Inversión", "$48.27", "$176.49"],
  ["Personas alcanzadas", "4,770", "516"],
  ["CPM", "$5.92", "$295.63"],
  ["Clics en el enlace", "6", "8"],
  ["Visitas a la landing", "0", "4"],
  ["ThruPlay (video visto)", "1,610", "—"],
  ["Leads (Meta)", "—", "1"],
  ["Leads calificados (GHL)", "—", "0"],
], { "3,2": HEX.accent5, "8,2": HEX.accent5 }),
{ x: 4.9, y: 1.15, w: 4.6, colW: [2.4, 1.1, 1.1], rowH: 0.36, fontSize: 12, ...TBL, objectName: "Campaign table" });
T(s, "Semana anterior (2 – 8 nov): $304.10, 9 visitas y 1 lead calificado (Immigration law).", { x: 4.9, y: 4.5, w: 4.6, h: 0.45, fontSize: 10, color: C.accent6, italic: true, valign: "top", objectName: "Campaign note" });
s.addNotes("El público Advantage+ del 9 nov no bajó el CPM de abogados: subió de $161 a $296.");

// ---------- 4. Attorneys daily ----------
s = slide("CONTENT", "Resultados");
s.addText("Campaña de abogados día a día", { placeholder: "title" });
s.addTable(tb([
  ["Día", "Gasto", "CPM", "Clics", "Visitas", "Nota"],
  ["Lun 9", "$43.87", "$240", "2", "0", "Feed de Facebook + Advantage+; A1 sale, V1 entra"],
  ["Mar 10", "$30.83", "$280", "0", "0", ""],
  ["Mié 11", "$25.33", "$218", "1", "0", ""],
  ["Jue 12", "$35.99", "$316", "0", "0", ""],
  ["Vie 13", "$40.47", "$547", "5", "4", "1 lead (B1): buscaba empleo · pausa 4 pm"],
  ["Sáb 14 – Dom 15", "$0", "—", "0", "0", "En pausa"],
], { "5,5": HEX.accent5 }).map(r => r.map((c, j) => (j === 5 ? { ...c, options: { ...c.options, align: "left" } } : c))),
{ x: 0.5, y: 1.15, w: 9, colW: [1.4, 0.9, 0.8, 0.7, 0.8, 4.4], rowH: 0.4, fontSize: 11, ...TBL, objectName: "Daily table" });
T(s, "B1 gastó $94 y V1 $82: el video no funcionó como anuncio de leads para abogados (3 clics, 0 visitas).", { x: 0.5, y: 4.15, w: 9, h: 0.4, fontSize: 11, italic: true, color: C.accent6, objectName: "Daily note" });
s.addNotes("La campaña de abogados queda en pausa un tiempo por decisión de la dirección (15 nov).");

// ---------- 5. Awareness by vertical ----------
s = slide("CONTENT", "Resultados");
s.addText("Video de awareness por vertical", { placeholder: "title" });
s.addTable(tb([
  ["Vertical", "Gasto", "Alcance", "ThruPlay", "Vieron 50%", "$ / ThruPlay"],
  ["Healthcare", "$8.13", "955", "313", "641", "$0.026"],
  ["Accounting", "$8.12", "1,048", "268", "636", "$0.030"],
  ["Real Estate", "$8.03", "1,119", "264", "590", "$0.030"],
  ["Entrepreneurs", "$7.97", "1,141", "257", "639", "$0.031"],
  ["Legal", "$7.98", "1,021", "258", "611", "$0.031"],
  ["Finance", "$8.04", "1,019", "250", "590", "$0.032"],
], { "1,5": HEX.accent4 }),
{ x: 0.5, y: 1.15, w: 6.2, colW: [1.6, 0.8, 0.9, 0.9, 1.0, 1.0], rowH: 0.38, fontSize: 11, ...TBL, objectName: "Vertical table" });
card(s, 7.0, 1.15, 2.5, 2.9, "Vertical card");
T(s, [
  { text: "Salud", options: { bold: true, color: HEX.dk2, fontSize: 18, breakLine: true } },
  { text: "Segunda semana como el video más barato por ThruPlay. Por eso es el primer mercado de la campaña de Black Friday.", options: { breakLine: true } },
  { text: " ", options: { breakLine: true, fontSize: 6 } },
  { text: "Emprendedores", options: { bold: true, color: HEX.dk2, fontSize: 18, breakLine: true } },
  { text: "El alcance que más crece: 1,141 personas.", options: {} },
], { x: 7.15, y: 1.3, w: 2.25, h: 2.7, fontSize: 11, color: C.text1, valign: "top", objectName: "Vertical body" });
T(s, "Desde el 16 nov Legal sale de awareness y los otros 5 mercados quedan en $1/día.", { x: 0.5, y: 4.0, w: 6.2, h: 0.4, fontSize: 11, italic: true, color: C.accent6, objectName: "Vertical note" });
s.addNotes("Awareness suma 7,152 reproducciones de al menos la mitad del video en noviembre (3,445 + 3,707); quienes lo vieron forman el público de retargeting.");

// ---------- 6. Learnings ----------
pres.addSection({ title: "Aprendizajes" });
s = slide("CONTENT", "Aprendizajes");
s.addText("Hallazgos", { placeholder: "title" });
const learn = [
  ["El público de abogados es caro y está saturado.", "CPM de $296 con Advantage+, casi el doble que la semana anterior. Muchas agencias compiten por el mismo público."],
  ["El único lead de la semana buscaba empleo.", "Ningún lead calificado en 7 días. Seguir invirtiendo en abogados no tenía sentido por ahora."],
  ["El video de awareness sigue siendo eficiente.", "CPM $6 y $0.03 por ThruPlay. Salud y emprendedores responden mejor que legal."],
  ["Anunciar con video a abogados no funcionó.", "V1 gastó $82 en la campaña de leads con 0 visitas a la landing."],
];
learn.forEach(([head, body], i) => {
  const y = 1.15 + i * 0.98;
  dot(s, 0.5, y + 0.05, String(i + 1), `Learning dot ${i + 1}`);
  T(s, head, { x: 1.15, y, w: 8.35, h: 0.42, fontSize: 16, bold: true, color: C.text2, valign: "middle", objectName: `Learning head ${i + 1}` });
  T(s, body, { x: 1.15, y: y + 0.42, w: 8.35, h: 0.4, fontSize: 13, color: C.text1, valign: "top", objectName: `Learning body ${i + 1}` });
});
s.addNotes("En la reunión del 10 nov se acordó pasar a salud y emprendedores con la oferta de Black Friday.");

// ---------- 7. Timeline ----------
pres.addSection({ title: "Qué hicimos" });
s = slide("CONTENT", "Qué hicimos");
s.addText("Cronología de cambios", { placeholder: "title" });
const events = [
  ["9 nov", "Feed + Advantage+", "Abogados solo en el feed de Facebook con público ampliado. A1 sale, V1 entra."],
  ["13 nov", "Pausa", "Abogados en pausa desde el viernes a las 4 pm."],
  ["15 nov", "Por mercado", "Campañas separadas para salud y emprendedores. Abogados queda quieto un tiempo."],
  ["15 nov", "Landings y medición", "3 landings nuevas, formularios, correo de bienvenida y API de Conversiones."],
  ["16 nov", "Lanzamiento", "Pruebas de medición superadas el 15 a las 11 pm; 5 campañas activas a las 2 am."],
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

// ---------- 8. What starts today ----------
pres.addSection({ title: "Lanzamiento" });
s = slide("CONTENT", "Lanzamiento");
s.addText("Lo que se activa hoy, 16 nov", { placeholder: "title" });
s.addTable([["Campaña", "Para qué", "Destino", "Presupuesto 16–30 nov"],
  ["🟢 Healthcare BF", "Leads de consultorios médicos y dentales", "go.orchidpros.com/practices-free-month", "$159.75"],
  ["🟢 Entrepreneurs BF", "Leads de empresas y emprendedores", "go.orchidpros.com/business-free-month", "$159.75"],
  ["🟢 Retargeting video", "Oferta a quien vio el video de awareness", "go.orchidpros.com/business-free-month", "$30.00"],
  ["🟢 IG Followers", "Seguidores en Instagram", "Perfil de Instagram", "$3/día · $45"],
  ["🟢 Awareness", "Video en 5 mercados (sin Legal)", "orchidpros.com", "$1/día c/u · $75"],
].map((r, i) => r.map((c, j) => ({ text: c, options: { bold: i === 0 || j === 0, color: i === 0 ? HEX.lt1 : (j === 0 ? HEX.dk2 : HEX.dk1),
  fill: { color: i === 0 ? HEX.dk2 : (i % 2 ? HEX.lt1 : HEX.lt2) }, valign: "middle", align: j === 3 ? "right" : "left" } }))),
{ x: 0.5, y: 1.15, w: 9, colW: [1.9, 2.8, 2.9, 1.4], rowH: 0.45, fontSize: 11, ...TBL, objectName: "Launch table" });
T(s, [
  { text: "Oferta: ", options: { bold: true } },
  { text: "Black Friday · get started free, then 50% off your first month · válida hasta el 1 de diciembre. Los anuncios de leads corren de 6 am a 10 pm, hora de cada persona, solo en el feed de Facebook. Abogados sigue en pausa." },
], { x: 0.5, y: 4.0, w: 9, h: 0.75, fontSize: 12, color: C.text1, valign: "top", objectName: "Launch note" });
s.addNotes("Noviembre: $529.62 gastado al 15 + $469.50 planeado = ~$999.");

// ---------- 9. Creatives ----------
s = slide("CONTENT", "Lanzamiento");
s.addText("Creativos que arrancan hoy", { placeholder: "title" });
[["hc_4x5", "Healthcare BF", "Patient intake, scheduler, interpreter"], ["ent_4x5", "Entrepreneurs BF", "Admin, operations, bookkeeping, marketing"], ["ig_3x4", "IG Followers", "\"Does your VA speak Spanish?\" · video"]]
  .forEach(([file, name, sub], i) => {
    const x = 0.6 + i * 3.05, h = 2.85, [pw, ph] = SIZE[file], w = h * pw / ph;
    capture(s, file, x + (2.7 - w) / 2, 1.05, h, `Creative ${name}`);
    T(s, name, { x, y: 4.0, w: 2.7, h: 0.3, fontSize: 13, bold: true, color: C.text2, align: "center", objectName: `Creative name ${i + 1}` });
    T(s, sub, { x, y: 4.3, w: 2.7, h: 0.5, fontSize: 10, color: C.accent6, align: "center", objectName: `Creative sub ${i + 1}` });
  });
s.addNotes("Pendiente con Debi: corregir HIPPA por HIPAA en el creativo de salud. El retargeting usa el creativo de emprendedores.");

// ---------- 10. Measurement ----------
s = slide("CONTENT", "Lanzamiento");
s.addText("Medición y seguimiento", { placeholder: "title" });
const meas = [
  ["Prueba antes de prender", "Envíos de prueba en las 3 landings el 15 nov a las 11 pm: Meta registró Lead ×2, lead calificado ×2 (API de Conversiones) y Subscribe ×1. Los contactos llegaron a GHL con su etiqueta y su anuncio de origen."],
  ["Leads a ventas", "Pendiente de confirmar: que el workflow de nuevo lead en GHL (correo, asignación y oportunidad) también se dispare con los formularios de salud y emprendedores."],
  ["Tablero diario", "Orchid Ads Tracker: gasto, clics, leads de Meta y leads reales de GHL por anuncio y mercado, actualizado cada mañana a las 8 am."],
];
meas.forEach(([head, body], i) => {
  const y = 1.15 + i * 1.2;
  card(s, 0.5, y, 9, 1.05, `Measure card ${i + 1}`);
  T(s, head, { x: 0.75, y: y + 0.1, w: 8.5, h: 0.35, fontSize: 15, bold: true, color: C.text2, objectName: `Measure head ${i + 1}` });
  T(s, body, { x: 0.75, y: y + 0.45, w: 8.5, h: 0.55, fontSize: 12, color: C.text1, valign: "top", objectName: `Measure body ${i + 1}` });
});
s.addNotes("Landing de newsletter (go.orchidpros.com/brief) publicada; dispara Subscribe y envía un correo de bienvenida con la oferta.");

// ---------- 11. Plan ----------
pres.addSection({ title: "Próximos pasos" });
s = slide("CONTENT", "Próximos pasos");
s.addText("Plan · 16 – 22 nov", { placeholder: "title" });
const plan = [
  ["Dejar aprender", "Sin cambios en salud y emprendedores hasta el jueves 19: Meta necesita unos días para encontrar a quién mostrar los anuncios."],
  ["Corte del jueves 19", "Comparar costo por lead real (GHL) entre salud y emprendedores y mover presupuesto al que rinda más."],
  ["Seguimiento diario", "Tablero cada mañana y aviso solo si un anuncio no entrega o gasta sin traer leads."],
];
plan.forEach(([head, body], i) => {
  const x = 0.5 + i * 3.07;
  card(s, x, 1.2, 2.86, 3.3, `Plan card ${i + 1}`);
  dot(s, x + 0.25, 1.45, String(i + 1), `Plan dot ${i + 1}`, C.text2, C.background1, 0.5);
  T(s, head, { x: x + 0.25, y: 2.15, w: 2.4, h: 0.6, fontSize: 17, bold: true, color: C.text2, fontFace: THEME.headFontFace, valign: "top", objectName: `Plan head ${i + 1}` });
  T(s, body, { x: x + 0.25, y: 2.8, w: 2.4, h: 1.6, fontSize: 13, color: C.text1, valign: "top", objectName: `Plan body ${i + 1}` });
});
s.addNotes("Próximo reporte: lunes 23 nov (semana 16 – 22 nov), el primero de Black Friday.");

(async () => {
  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("written", OUT);
})();
