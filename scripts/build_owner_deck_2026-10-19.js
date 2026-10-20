// Builds the owner deck (PowerPoint) for the week of 2026-10-12 to 2026-10-18 (delivered 2026-10-19). Run with NODE_PATH pointing to a node_modules that has pptxgenjs.
const pptxgen = require("pptxgenjs");
const path = require("path");
const { applyTheme } = require("/root/.claude/skills/synced/91214b57-4729-489d-a491-f28c7fe5eb8b_230bf34e-5a4e-4f30-a11c-45835a5a2a37/pptx/scripts/apply_theme.js");

const OUT = "/home/user/MetaADS2026/build/reports/informes/Informe_Meta_Ads_Orchid_2026-10-19.pptx";
const IMG = "/home/user/MetaADS2026/build/reports/previews/2026-10-20/";
const SIZE = { // px of each capture, to keep aspect ratio
  "S9-Attorneys-In-Person-Cost-Hyperlocal-2026-Oct": [640, 1262], "S11-Immigration-Intake-Calls-Hyperlocal-2026-Oct": [640, 1302],
  "H3-Saturdays-Back-Hyperlocal-2026-Oct": [640, 1262], "V2-Small-Law-Firm-2026-Oct": [640, 1302],
  "S10-Interns-Turnover-Hyperlocal-2026-Oct": [640, 1296], "S8-Comparison-Static-2026-Oct": [640, 1302],
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
pres.title = "Informe Meta Ads Orchid – Semana del 12 al 18 oct";
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
const FOOT = { text: "Orchid · Informe Meta Ads · Semana 12 – 18 oct 2026", options: { x: 0.5, y: 5.25, w: 6, h: 0.25, fontSize: 9, color: C.accent6, margin: 0 } };
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

// ---------- 1. Title ----------
pres.addSection({ title: "Resumen" });
let s = slide("DARK_TITLE", "Resumen");
s.addText("Informe Meta Ads", { placeholder: "title" });
s.addText([
  { text: "Semana del 12 al 18 oct 2026", options: { breakLine: true } },
  { text: "Reporte de desempeño · Dirección de Orchid · 19 oct 2026", options: { fontSize: 14, color: C.background1 } },
], { placeholder: "body" });
s.addNotes("Semana 3 de la campaña Leads – Hire VA: lanzamiento del piloto hiperlocal de inmigración con los creativos de Debi, correcciones técnicas y próximos pasos.");

// ---------- 2. Three numbers ----------
s = slide("CONTENT", "Resumen");
s.addText("Resumen ejecutivo", { placeholder: "title" });
[["$288.30", "Inversión", "12 – 18 oct"], ["0", "Leads calificados", "1 lead en la semana: buscaba empleo"], ["$5.65", "Costo por visita a la landing", "Semana anterior: $7.29 (−22%)"]]
  .forEach(([big, label, sub], i) => {
    const x = 0.5 + i * 3.07;
    card(s, x, 1.25, 2.86, 2.15, `Stat card ${i + 1}`);
    T(s, big, { x: x + 0.25, y: 1.45, w: 2.4, h: 0.95, fontSize: 44, bold: true, color: C.text2, fontFace: THEME.headFontFace, objectName: `Stat ${i + 1}` });
    T(s, label, { x: x + 0.25, y: 2.45, w: 2.4, h: 0.35, fontSize: 15, bold: true, color: C.text1, objectName: `Stat label ${i + 1}` });
    T(s, sub, { x: x + 0.25, y: 2.8, w: 2.4, h: 0.45, fontSize: 11, color: C.accent6, objectName: `Stat note ${i + 1}` });
  });
T(s, [
  { text: "Tráfico más barato, sin conversión. ", options: { bold: true } },
  { text: "El 16 oct se movió todo el presupuesto al piloto hiperlocal (abogados alrededor de juzgados de inmigración y USCIS en NY, Newark y Philadelphia) con los creativos de Debi. El CPM bajó 44% y las visitas a la landing subieron 34%, pero ninguna terminó en lead calificado." },
], { x: 0.5, y: 3.7, w: 9, h: 1.0, fontSize: 14, color: C.text1, valign: "top", objectName: "Summary" });
s.addNotes("Los anuncios nuevos no trajeron ningún buscador de empleo. El cuello de botella pasa a ser la conversión en la landing.");

// ---------- 3. Week vs week ----------
pres.addSection({ title: "Resultados" });
s = slide("CONTENT", "Resultados");
s.addText("CPM −44%, +34% visitas a la landing", { placeholder: "title" });
s.addChart(pres.charts.BAR, [
  { name: "Clics en el enlace", labels: ["Semana 2 · 5 – 11 oct", "Semana 3 · 12 – 18 oct"], values: [53, 68] },
  { name: "Visitas a la landing", labels: ["Semana 2 · 5 – 11 oct", "Semana 3 · 12 – 18 oct"], values: [38, 51] },
], {
  x: 0.4, y: 1.15, w: 4.6, h: 3.85, barDir: "col", barGrouping: "clustered", objectName: "Clicks chart",
  chartColors: [HEX.dk2, HEX.accent3],
  showValue: true, dataLabelPosition: "outEnd", dataLabelFontSize: 12, dataLabelColor: HEX.dk1, dataLabelFontFace: "+mn-lt",
  catAxisLabelFontFace: "+mn-lt", catAxisLabelFontSize: 11, catAxisLabelColor: HEX.accent6,
  valAxisHidden: true, valGridLine: { style: "none" }, catGridLine: { style: "none" },
  showLegend: true, legendPos: "b", legendFontSize: 11, legendFontFace: "+mn-lt", legendColor: HEX.accent6,
});
s.addTable(tbl([
  ["", "Semana 2", "Semana 3"],
  ["Inversión", "$277.04", "$288.30"],
  ["CPM", "$115.52", "$64.67"],
  ["CTR (enlace)", "2.21%", "1.52%"],
  ["Costo por visita a landing", "$7.29", "$5.65"],
  ["Leads (Meta)", "2", "1"],
  ["Leads calificados (GHL)", "0", "0"],
  ["Buscadores de empleo (GHL)", "3", "1"],
], {}, { "2,2": HEX.accent4, "4,2": HEX.accent4, "3,2": HEX.accent5 }),
{ x: 5.3, y: 1.2, w: 4.2, colW: [2.2, 1.0, 1.0], rowH: 0.38, fontSize: 12, fontFace: THEME.bodyFontFace, border: { type: "none" }, margin: [0, 0.08, 0, 0.08], objectName: "Week table" });
T(s, "Inversión 6% sobre el tope semanal ($272.23 = 7 × $38.89): Meta gasta de más los días con cambios de presupuesto (14, 16 y 18 oct).", { x: 5.3, y: 4.3, w: 4.2, h: 0.6, fontSize: 10, color: C.accent6, italic: true, valign: "top", objectName: "Week note" });
s.addNotes("La caída de CTR se explica por el cambio de audiencia: menos personas, más específicas. Lo relevante es que cada visita a la landing cuesta menos.");

// ---------- 4. National vs hyperlocal ----------
s = slide("CONTENT", "Resultados");
s.addText("Nacional vs. piloto hiperlocal", { placeholder: "title" });
s.addTable(tbl([
  ["", "Nacional (12 – 16 oct)", "Hiperlocal (16 – 18 oct)"],
  ["Anuncios", "V2, V1, S8 (copy v3)", "S9, S10, S11 (copy v4)"],
  ["Inversión", "$157.75", "$130.55"],
  ["Impresiones", "1,800", "2,658"],
  ["CPM", "$87.64", "$49.12"],
  ["Clics en el enlace", "34", "34"],
  ["Visitas a la landing", "23", "28"],
  ["Costo por visita a landing", "$6.86", "$4.66"],
  ["Leads (GHL)", "1 · buscaba empleo", "0"],
], {}, { "4,2": HEX.accent4, "7,2": HEX.accent4, "8,1": HEX.accent5 }),
{ x: 0.5, y: 1.15, w: 5.6, colW: [2.0, 1.8, 1.8], rowH: 0.38, fontSize: 12, fontFace: THEME.bodyFontFace, border: { type: "none" }, margin: [0, 0.08, 0, 0.08], objectName: "Split table" });
card(s, 6.4, 1.15, 3.1, 3.45, "Hyperlocal card", C.text2);
T(s, "Piloto hiperlocal", { x: 6.65, y: 1.35, w: 2.6, h: 0.3, fontSize: 12, bold: true, color: C.accent1, objectName: "Hyper label" });
T(s, [
  { text: "4 zonas de 1 milla: 26 Federal Plaza (NY), 970 Broad St (Newark), USCIS y juzgado de Philadelphia.", options: { breakLine: true } },
  { text: " ", options: { breakLine: true, fontSize: 6 } },
  { text: "25–65 años · intereses Law firm, Lawyer, Bar association.", options: { breakLine: true } },
  { text: " ", options: { breakLine: true, fontSize: 6 } },
  { text: "$38.89/día desde el 16 oct; nacional en pausa." },
], { x: 6.65, y: 1.75, w: 2.65, h: 2.7, fontSize: 12, color: C.background1, valign: "top", objectName: "Hyper body" });
T(s, "Leads GHL: se excluyen 3,005 contactos importados de Mailchimp el 18–19 oct (no son leads de formulario).", { x: 0.5, y: 4.7, w: 9, h: 0.3, fontSize: 10, italic: true, color: C.accent6, objectName: "Split note" });
s.addNotes("El hiperlocal entrega más barato y no ha traído buscadores de empleo. Aún no trae leads: ver hallazgo sobre la landing.");

// ---------- 5. Timeline ----------
pres.addSection({ title: "Qué hicimos" });
s = slide("CONTENT", "Qué hicimos");
s.addText("Cronología de cambios", { placeholder: "title" });
const events = [
  ["12 oct", "Optimización", "Advantage+ off, 30–65, copy v3 en V1, V2 y S8."],
  ["14 oct", "Pausa S8", "$14 sin clics."],
  ["16 oct", "Piloto hiperlocal", "Copy v4 con creativos de Debi (S9, S10) y S11 para inmigración. Nacional en pausa."],
  ["17 oct", "Correcciones", "Botón a la landing. Solo imágenes aprobadas, sin repetir entre anuncios."],
  ["19 oct", "Rotación", "Banca de 6 anuncios (H1–H6). S10 pausado, H3 activo."],
];
s.addShape(pres.shapes.LINE, { x: 0.8, y: 1.86, w: 8.4, h: 0, line: { color: C.accent3, width: 2 }, objectName: "Timeline line" });
events.forEach(([d, head, body], i) => {
  const x = 0.5 + i * 1.84;
  dot(s, x + 0.1, 1.65, String(i + 1), `Timeline dot ${i + 1}`, i === 2 ? C.accent1 : C.text2, i === 2 ? C.text2 : C.background1);
  T(s, d, { x, y: 2.25, w: 1.7, h: 0.35, fontSize: 13, bold: true, color: C.accent3, objectName: `Timeline date ${i + 1}` });
  T(s, head, { x, y: 2.6, w: 1.7, h: 0.45, fontSize: 15, bold: true, color: C.text2, fontFace: THEME.headFontFace, objectName: `Timeline head ${i + 1}` });
  T(s, body, { x, y: 3.1, w: 1.7, h: 1.6, fontSize: 12, color: C.text1, valign: "top", objectName: `Timeline body ${i + 1}` });
});
s.addNotes("Detalle de cada cambio y su motivo en build/CHANGELOG_META.md.");

// ---------- 6. Technical fixes ----------
s = slide("CONTENT", "Qué hicimos");
s.addText("Correcciones técnicas detectadas", { placeholder: "title" });
const fixes = [
  ["Embudo", ["El botón \"Book Now\" abría el calendario de citas de Facebook, no la landing.", "Esas solicitudes no llegan a GHL.", "Corregido el 17 oct en S9, S10 y S11."]],
  ["Página de Facebook", ["Categorías: Real Estate, Recruiter y Lawyer & Law Firm.", "\"Recruiter\" le indica a Meta que somos agencia de empleo.", "\"REAL ESTATE\" aparece bajo el anuncio. Pendiente de cambio."]],
  ["Segmentación", ["Meta retiró el interés AILA.", "Reemplazado por Bar association.", "Sin el cambio, el conjunto no se habría podido crear."]],
];
fixes.forEach(([head, items], i) => {
  const x = 0.5 + i * 3.07;
  card(s, x, 1.2, 2.86, 3.35, `Fix card ${i + 1}`);
  dot(s, x + 0.25, 1.4, String(i + 1), `Fix dot ${i + 1}`, i === 1 ? C.accent5 : C.accent1, i === 1 ? C.background1 : C.text2);
  T(s, head, { x: x + 0.8, y: 1.4, w: 1.9, h: 0.42, fontSize: 17, bold: true, color: C.text2, fontFace: THEME.headFontFace, valign: "middle", objectName: `Fix head ${i + 1}` });
  T(s, items.map((t, k) => ({ text: t, options: { bullet: true, breakLine: k < items.length - 1 } })), {
    x: x + 0.25, y: 2.0, w: 2.45, h: 2.45, fontSize: 12, color: C.text1, valign: "top", paraSpaceAfter: 6, objectName: `Fix body ${i + 1}` });
});
T(s, "Revisar Business Suite → Citas: puede haber solicitudes del 16–17 oct hechas por el calendario de Facebook.", { x: 0.5, y: 4.7, w: 9, h: 0.35, fontSize: 11, italic: true, color: C.accent6, objectName: "Fix note" });
s.addNotes("El cambio de categorías lo hace un administrador de la página; no reinicia el aprendizaje de los anuncios.");

// ---------- 7. Learnings ----------
pres.addSection({ title: "Aprendizajes" });
s = slide("CONTENT", "Aprendizajes");
s.addText("Hallazgos", { placeholder: "title" });
const learn = [
  ["La segmentación hiperlocal abarata el tráfico calificado.", "CPM $49 vs. $88 en nacional; costo por visita a la landing $4.66 vs. $6.86."],
  ["Copy dirigido a la firma: 0 buscadores de empleo desde el 16 oct.", "El único lead de la semana (13 oct) vino de V2 y buscaba empleo, igual que los 3 anteriores."],
  ["51 visitas a la landing sin lead calificado.", "El cuello de botella pasa a la landing y al formulario. Requiere prueba de envío y del evento Lead."],
  ["Fin de semana caro con audiencia chica.", "18 oct: $51.69 por 3 clics (CPM $99). S10 absorbió $36 con 1 clic y fue pausado."],
];
learn.forEach(([head, body], i) => {
  const y = 1.15 + i * 0.98;
  dot(s, 0.5, y + 0.05, String(i + 1), `Learning dot ${i + 1}`);
  T(s, head, { x: 1.15, y, w: 8.35, h: 0.42, fontSize: 16, bold: true, color: C.text2, valign: "middle", objectName: `Learning head ${i + 1}` });
  T(s, body, { x: 1.15, y: y + 0.42, w: 8.35, h: 0.4, fontSize: 13, color: C.text1, valign: "top", objectName: `Learning body ${i + 1}` });
});
s.addNotes("🔵 S11 (copy específico de inmigración) recibió el 46% del gasto del hiperlocal con el CPM más bajo ($36).");

// ---------- 8. Active ads ----------
pres.addSection({ title: "Anuncios" });
s = slide("CONTENT", "Anuncios");
s.addText("Creativos activos (hiperlocal)", { placeholder: "title" });
const active = [
  ["S11-Immigration-Intake-Calls-Hyperlocal-2026-Oct", "🔵 S11 Immigration Intake Calls", "$59.64 · 20 clics · 16 visitas", "CPM $36 · 0 leads", C.accent6],
  ["S9-Attorneys-In-Person-Cost-Hyperlocal-2026-Oct", "S9 Attorneys In-Person Cost", "$21.81 · 9 clics · 8 visitas", "CTR 1.83% · 0 leads", C.accent6],
  ["H3-Saturdays-Back-Hyperlocal-2026-Oct", "🔵 H3 Saturdays Back", "Activo desde el 19 oct", "Reemplaza a S10", C.accent3],
];
active.forEach(([file, name, nums, res, col], i) => {
  const x = 0.5 + i * 3.07;
  const w = capture(s, file, x, 1.15, 2.95, `Capture ${name}`);
  const tx = x + w + 0.15, tw = 2.86 - w - 0.15;
  T(s, name, { x: tx, y: 1.2, w: tw, h: 0.7, fontSize: 13, bold: true, color: C.text2, valign: "top", objectName: `Active name ${i + 1}` });
  T(s, nums, { x: tx, y: 1.95, w: tw, h: 0.75, fontSize: 12, color: C.text1, valign: "top", objectName: `Active nums ${i + 1}` });
  T(s, res, { x: tx, y: 2.75, w: tw, h: 0.6, fontSize: 12, bold: true, color: col, valign: "top", objectName: `Active result ${i + 1}` });
});
T(s, "Cifras 12 – 18 oct. 🔵 = copy escrito por Claude (no el entregado por el equipo). Todos usan solo creativos aprobados de Debi.", { x: 0.5, y: 4.3, w: 9, h: 0.4, fontSize: 10, italic: true, color: C.accent6, objectName: "Active note" });
s.addNotes("Vista previa en feed móvil con el copy vigente.");

// ---------- 9. Paused this week ----------
s = slide("CONTENT", "Anuncios");
s.addText("Creativos pausados esta semana", { placeholder: "title" });
const paused = [
  ["V2-Small-Law-Firm-2026-Oct", "V2 Small Law Firm · video", "$141.67 · 34 clics", "1 lead: buscaba empleo", "Pausado con el nacional (16 oct). Asistente en cámara y \"19 jobs\" en pantalla atraen candidatos."],
  ["S10-Interns-Turnover-Hyperlocal-2026-Oct", "S10 Interns Turnover", "$49.10 · 5 clics · CPM $95", "0 leads", "Pausado el 19 oct: superó el criterio de corte ($40 sin leads)."],
  ["S8-Comparison-Static-2026-Oct", "S8 Comparison", "$14.19 · 0 clics", "0 leads", "Pausado el 14 oct."],
];
paused.forEach(([file, name, nums, res, why], i) => {
  const x = 0.5 + i * 3.07;
  const w = capture(s, file, x, 1.15, 2.95, `Capture ${name}`);
  const tx = x + w + 0.15, tw = 2.86 - w - 0.15;
  T(s, name, { x: tx, y: 1.2, w: tw, h: 0.55, fontSize: 12, bold: true, color: C.text2, valign: "top", objectName: `Paused name ${i + 1}` });
  T(s, nums, { x: tx, y: 1.75, w: tw, h: 0.55, fontSize: 11, color: C.text1, valign: "top", objectName: `Paused nums ${i + 1}` });
  T(s, res, { x: tx, y: 2.3, w: tw, h: 0.4, fontSize: 11, bold: true, color: C.accent5, valign: "top", objectName: `Paused result ${i + 1}` });
  T(s, why, { x: tx, y: 2.7, w: tw, h: 1.4, fontSize: 10, color: C.text1, valign: "top", objectName: `Paused why ${i + 1}` });
});
s.addNotes("V1 ($1.64) y S1 ($0.06) gastaron montos marginales y siguen pausados.");

// ---------- 10. Bench ----------
s = slide("CONTENT", "Anuncios");
s.addText("Banca lista: 6 anuncios en pausa", { placeholder: "title" });
s.addTable([["", "Anuncio", "Imagen (Debi)", "Ángulo"],
  ["H1", "Sticky Notes Follow-ups", "for the attorneys 1", "Seguimientos pendientes"],
  ["H2", "After-Hours Paperwork", "for the attorneys 2", "Papeleo después de las 7 pm"],
  ["H3", "Saturdays Back", "for the attorneys 3", "Abogado que hace de todo · ACTIVO"],
  ["H4", "Spanish-Speaking Clients", "still depending on interns 1", "Clientes que prefieren el español"],
  ["H5", "Phones While In Court", "still depending on interns 2", "Teléfono mientras estás en audiencia"],
  ["H6", "Cost Of In-Office Support", "still depending on interns 3", "Costo real del personal presencial"],
].map((r, i) => r.map((c, j) => ({ text: c, options: { bold: i === 0 || j === 0 || (i === 3), color: i === 0 ? HEX.lt1 : (j === 0 ? HEX.dk2 : (i === 3 ? HEX.accent4 : HEX.dk1)),
  fill: { color: i === 0 ? HEX.dk2 : (i % 2 ? HEX.lt1 : HEX.lt2) }, valign: "middle", align: j === 0 ? "center" : "left" } }))),
{ x: 0.5, y: 1.15, w: 9, colW: [0.5, 2.6, 2.5, 3.4], rowH: 0.42, fontSize: 12, fontFace: THEME.bodyFontFace, border: { type: "none" }, margin: [0, 0.08, 0, 0.08], objectName: "Bench table" });
T(s, [
  { text: "Uso: ", options: { bold: true } },
  { text: "cuando un anuncio activo cumpla el criterio de corte, se reemplaza por uno de la banca sin esperar nuevos creativos. Todos llevan 🔵, botón a la landing y cierre \"vetted by Orchid\" (sin vocabulario de empleo)." },
], { x: 0.5, y: 4.2, w: 9, h: 0.7, fontSize: 12, color: C.text1, valign: "top", objectName: "Bench note" });
s.addNotes("Prioridad de rotación: H5 y H4 (los ángulos más específicos para abogados de inmigración).");

// ---------- 11. Conclusions ----------
pres.addSection({ title: "Conclusiones" });
s = slide("CONTENT", "Conclusiones");
s.addText("Conclusiones: qué funciona y qué no", { placeholder: "title" });
const good = [
  ["Segmentación hiperlocal", "CPM −44% y costo por visita −32% frente al nacional."],
  ["Copy dirigido a la firma", "0 buscadores de empleo desde el lanzamiento del 16 oct."],
  ["Volumen creativo", "3 activos + 6 en banca: 9 conceptos, todos con imágenes aprobadas."],
  ["Medición", "Calidad por anuncio en GHL; importaciones de Mailchimp excluidas."],
];
const bad = [
  ["Conversión de la landing", "51 visitas en la semana, 0 leads calificados."],
  ["Señales de empleo fuera del copy", "Categoría \"Recruiter\" y texto en imagen \"Hire a part-time experienced professional\"."],
  ["Fines de semana", "18 oct: CPM $99, 3 clics. La audiencia profesional no está activa."],
  ["Ediciones frecuentes", "3 cambios de creativo en 3 días reiniciaron el aprendizaje de Meta."],
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
s.addNotes("Prioridad: validar el formulario y el evento Lead antes de seguir cambiando anuncios.");

// ---------- 12. Andromeda ----------
pres.addSection({ title: "Estrategia creativa" });
s = slide("CONTENT", "Estrategia creativa");
s.addText("Andromeda: el creativo define la audiencia", { placeholder: "title" });
const andr = [
  ["Lee todo el anuncio, no solo el copy", "Texto en imagen, página y categoría también son señales. \"Recruiter\" y \"Hire a part-time professional\" apuntan a candidatos."],
  ["Imágenes repetidas = un solo concepto", "Se separaron las imágenes entre S10 y S11 para que Meta los trate como conceptos distintos."],
  ["Diversidad = exploración", "Cada ángulo nuevo (llamadas, papeleo, sábados, costo) abre un público distinto dentro del mismo segmento."],
];
andr.forEach(([h, b], i) => {
  const y = 1.2 + i * 1.12;
  dot(s, 0.5, y + 0.02, String(i + 1), `Andromeda dot ${i + 1}`);
  T(s, h, { x: 1.1, y, w: 4.9, h: 0.4, fontSize: 16, bold: true, color: C.text2, valign: "middle", objectName: `Andromeda head ${i + 1}` });
  T(s, b, { x: 1.1, y: y + 0.4, w: 4.9, h: 0.65, fontSize: 12, color: C.text1, valign: "top", objectName: `Andromeda body ${i + 1}` });
});
card(s, 6.4, 1.2, 3.1, 3.35, "Creative gap card", C.text2);
T(s, "Semana anterior", { x: 6.65, y: 1.4, w: 2.6, h: 0.3, fontSize: 12, color: C.accent1, bold: true, objectName: "Gap label 1" });
T(s, "3", { x: 6.65, y: 1.7, w: 2.6, h: 0.75, fontSize: 48, bold: true, color: C.background1, fontFace: THEME.headFontFace, objectName: "Gap before" });
T(s, "creativos activos", { x: 6.65, y: 2.45, w: 2.6, h: 0.3, fontSize: 12, color: C.background1, objectName: "Gap before label" });
T(s, "Hoy", { x: 6.65, y: 2.95, w: 2.6, h: 0.3, fontSize: 12, color: C.accent1, bold: true, objectName: "Gap label 2" });
T(s, "9", { x: 6.65, y: 3.25, w: 2.6, h: 0.75, fontSize: 48, bold: true, color: C.background1, fontFace: THEME.headFontFace, objectName: "Gap now" });
T(s, "conceptos (3 activos + 6 en banca)", { x: 6.65, y: 4.0, w: 2.6, h: 0.3, fontSize: 12, color: C.background1, objectName: "Gap now label" });
s.addNotes("Pedido para los próximos creativos: texto en imagen desde la firma (\"Your bilingual legal assistant · For U.S. law firms · From $15/hr\") y versiones 9:16.");

// ---------- 13. Plan ----------
pres.addSection({ title: "Próximos pasos" });
s = slide("CONTENT", "Próximos pasos");
s.addText("Plan · 19 – 25 oct", { placeholder: "title" });
const plan = [
  ["Validar la conversión", "Envío de prueba del formulario desde el celular. Verificar que llegue a GHL y que Meta registre el evento Lead."],
  ["Revisión miércoles 21", "Criterio de corte: $40 sin lead. Rotación desde la banca (H5, H4). Sin otros cambios hasta entonces."],
  ["Creativos y página", "Cambio de categorías de la página. Pedir a Debi texto en imagen desde la firma y versiones 9:16."],
];
plan.forEach(([head, body], i) => {
  const x = 0.5 + i * 3.07;
  card(s, x, 1.2, 2.86, 3.3, `Plan card ${i + 1}`);
  dot(s, x + 0.25, 1.45, String(i + 1), `Plan dot ${i + 1}`, C.text2, C.background1, 0.5);
  T(s, head, { x: x + 0.25, y: 2.15, w: 2.4, h: 0.6, fontSize: 17, bold: true, color: C.text2, fontFace: THEME.headFontFace, valign: "top", objectName: `Plan head ${i + 1}` });
  T(s, body, { x: x + 0.25, y: 2.8, w: 2.4, h: 1.6, fontSize: 13, color: C.text1, valign: "top", objectName: `Plan body ${i + 1}` });
});
s.addNotes("Próximo reporte: lunes 26 oct (semana 19–25 oct).");

// ---------- 14. Decisions ----------
s = slide("DARK_CONTENT", "Próximos pasos");
s.addText("Decisiones requeridas", { placeholder: "title" });
const dec = [
  ["Categorías de la página de Facebook", "Quitar Recruiter, Real Estate y Lawyer & Law Firm; dejar Business Service / Consulting Agency. Requiere un administrador."],
  ["Pausar fines de semana", "Aprobar el cambio a presupuesto total con horario (lunes a viernes) si el patrón de CPM alto se repite."],
  ["Pendientes de la semana anterior", "CPL calificado objetivo y envío del evento Lead vía CAPI solo para \"I want to hire.\"."],
];
dec.forEach(([head, body], i) => {
  const y = 1.25 + i * 1.25;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.5, y: y + 0.05, w: 0.38, h: 0.38, fill: { color: C.text2 }, line: { color: C.accent1, width: 2 }, rectRadius: 0.06, objectName: `Decision box ${i + 1}` });
  T(s, head, { x: 1.1, y, w: 8.4, h: 0.45, fontSize: 18, bold: true, color: C.accent1, valign: "middle", objectName: `Decision head ${i + 1}` });
  T(s, body, { x: 1.1, y: y + 0.47, w: 8.4, h: 0.65, fontSize: 14, color: C.background1, valign: "top", objectName: `Decision body ${i + 1}` });
});
s.addNotes("Las tres afectan la calidad de los leads más que cualquier ajuste de anuncios.");

(async () => {
  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("written", OUT);
})();
