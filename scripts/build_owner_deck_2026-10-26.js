// Builds the owner deck (PowerPoint) for the week of 2026-10-19 to 2026-10-25 (delivered 2026-10-26). Run with NODE_PATH pointing to a node_modules that has pptxgenjs.
const pptxgen = require("pptxgenjs");
const path = require("path");
const { applyTheme } = require("/root/.claude/skills/synced/91214b57-4729-489d-a491-f28c7fe5eb8b_230bf34e-5a4e-4f30-a11c-45835a5a2a37/pptx/scripts/apply_theme.js");

const OUT = "/home/user/MetaADS2026/build/reports/informes/Informe_Meta_Ads_Orchid_2026-10-26.pptx";
const IMG = "/home/user/MetaADS2026/build/reports/previews/2026-10-26/";
const SIZE = { // px of each capture, to keep aspect ratio
  "S11-Immigration-Intake-Calls-Hyperlocal-2026-Oct": [640, 1302], "S9-Attorneys-In-Person-Cost-Hyperlocal-2026-Oct": [640, 1262],
  "H3-Saturdays-Back-Hyperlocal-2026-Oct": [640, 1302], "H5-Phones-While-In-Court-Hyperlocal-2026-Oct": [640, 1302],
  "TEST-B-S9-Attorneys-In-Person-Cost": [640, 1262], "TEST-C-H5-Phones-While-In-Court": [640, 1262],
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
pres.title = "Informe Meta Ads Orchid – Semana del 19 al 25 oct";
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
const FOOT = { text: "Orchid · Informe Meta Ads · Semana 19 – 25 oct 2026", options: { x: 0.5, y: 5.25, w: 6, h: 0.25, fontSize: 9, color: C.accent6, margin: 0 } };
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
  { text: "Semana del 19 al 25 oct 2026", options: { breakLine: true } },
  { text: "Reporte de desempeño · Dirección de Orchid · 26 oct 2026", options: { fontSize: 14, color: C.background1 } },
], { placeholder: "body" });
s.addNotes("Semana 4: entrega interrumpida por un pago rechazado, primera pausa de fin de semana, rotación de creativos y preparación de la prueba A/B/C de destino (activa desde el 26 oct).");

// ---------- 2. Executive summary ----------
s = slide("CONTENT", "Resumen");
s.addText("Resumen ejecutivo", { placeholder: "title" });
[["$177.45", "Inversión", "19 – 25 oct · 4 días con entrega"], ["0", "Leads calificados", "1 lead en la semana: buscaba empleo"], ["$114", "CPM", "Semana anterior: $65"]]
  .forEach(([big, label, sub], i) => {
    const x = 0.5 + i * 3.07;
    card(s, x, 1.25, 2.86, 2.15, `Stat card ${i + 1}`);
    T(s, big, { x: x + 0.25, y: 1.45, w: 2.4, h: 0.95, fontSize: 44, bold: true, color: C.text2, fontFace: THEME.headFontFace, objectName: `Stat ${i + 1}` });
    T(s, label, { x: x + 0.25, y: 2.45, w: 2.4, h: 0.35, fontSize: 15, bold: true, color: C.text1, objectName: `Stat label ${i + 1}` });
    T(s, sub, { x: x + 0.25, y: 2.8, w: 2.4, h: 0.45, fontSize: 11, color: C.accent6, objectName: `Stat note ${i + 1}` });
  });
T(s, [
  { text: "Semana corta y cara. ", options: { bold: true } },
  { text: "Un pago rechazado detuvo la cuenta el 19 y 20 oct, y desde el viernes 23 a las 4 pm rige la pausa de fin de semana. El público hiperlocal (939 personas alcanzadas) se saturó y el CPM casi se duplicó. El lunes 26 se reemplazó por la prueba A/B/C en NY, NJ y PA." },
], { x: 0.5, y: 3.7, w: 9, h: 1.0, fontSize: 14, color: C.text1, valign: "top", objectName: "Summary" });
s.addNotes("Gasto de octubre al 26: $890.62. El tope de $1,000/mes rige desde noviembre.");

// ---------- 3. Week vs week ----------
pres.addSection({ title: "Resultados" });
s = slide("CONTENT", "Resultados");
s.addText("Resultados semanales", { placeholder: "title" });
s.addChart(pres.charts.BAR, [
  { name: "Clics en el enlace", labels: ["Semana 3 · 12 – 18 oct", "Semana 4 · 19 – 25 oct"], values: [68, 25] },
  { name: "Visitas a la landing", labels: ["Semana 3 · 12 – 18 oct", "Semana 4 · 19 – 25 oct"], values: [51, 16] },
], {
  x: 0.4, y: 1.15, w: 4.6, h: 3.85, barDir: "col", barGrouping: "clustered", objectName: "Clicks chart",
  chartColors: [HEX.dk2, HEX.accent3],
  showValue: true, dataLabelPosition: "outEnd", dataLabelFontSize: 12, dataLabelColor: HEX.dk1, dataLabelFontFace: "+mn-lt",
  catAxisLabelFontFace: "+mn-lt", catAxisLabelFontSize: 11, catAxisLabelColor: HEX.accent6,
  valAxisHidden: true, valGridLine: { style: "none" }, catGridLine: { style: "none" },
  showLegend: true, legendPos: "b", legendFontSize: 11, legendFontFace: "+mn-lt", legendColor: HEX.accent6,
});
s.addTable(tb([
  ["", "Semana 3", "Semana 4"],
  ["Días con entrega", "7", "4"],
  ["Inversión", "$288.30", "$177.45"],
  ["CPM", "$64.67", "$114.04"],
  ["CTR (enlace)", "1.52%", "1.60%"],
  ["Costo por visita a landing", "$5.65", "$11.09"],
  ["Leads (Meta)", "1", "1"],
  ["Leads calificados (GHL)", "0", "0"],
  ["Buscadores de empleo (GHL)", "1", "1"],
], { "3,2": HEX.accent5, "5,2": HEX.accent5 }),
{ x: 5.3, y: 1.15, w: 4.2, colW: [2.2, 1.0, 1.0], rowH: 0.36, fontSize: 12, ...TBL, objectName: "Week table" });
T(s, "Alcance de la semana: 939 personas, frecuencia 1.65. El público hiperlocal se agotó.", { x: 5.3, y: 4.5, w: 4.2, h: 0.4, fontSize: 10, color: C.accent6, italic: true, valign: "top", objectName: "Week note" });
s.addNotes("El CTR se mantuvo: el anuncio sigue interesando; lo que se encareció fue llegar a la misma audiencia pequeña.");

// ---------- 4. Daily + leads ----------
s = slide("CONTENT", "Resultados");
s.addText("Entrega diaria y leads", { placeholder: "title" });
s.addTable(tb([
  ["Día", "Gasto", "Clics", "Visitas", "Nota"],
  ["Lun 19", "$16.49", "3", "2", "Pago rechazado en la tarde"],
  ["Mar 20", "$0", "0", "0", "Cuenta bloqueada por saldo pendiente"],
  ["Mié 21", "$71.30", "14", "8", "Pago resuelto; presupuesto a $45/día"],
  ["Jue 22", "$53.51", "5", "4", ""],
  ["Vie 23", "$36.15", "3", "2", "1 lead (H5); pausa desde las 4 pm"],
  ["Sáb 24 – Dom 25", "$0", "0", "0", "Pausa de fin de semana"],
], { "2,4": HEX.accent5, "5,4": HEX.accent4 }).map(r => r.map((c, j) => (j === 4 ? { ...c, options: { ...c.options, align: "left" } } : c))),
{ x: 0.5, y: 1.15, w: 5.9, colW: [1.3, 0.8, 0.6, 0.7, 2.5], rowH: 0.4, fontSize: 11, ...TBL, objectName: "Daily table" });
card(s, 6.6, 1.15, 2.9, 3.4, "Leads card");
T(s, "Leads en GHL", { x: 6.8, y: 1.3, w: 2.5, h: 0.3, fontSize: 14, bold: true, color: C.text2, objectName: "Leads head" });
T(s, [
  { text: "23 oct · 🔵 H5 Phones While In Court", options: { bold: true, breakLine: true } },
  { text: "\"I'm looking for a job\" · Other business", options: { color: HEX.accent5, breakLine: true } },
  { text: " ", options: { breakLine: true, fontSize: 6 } },
  { text: "4 contactos sin anuncio de origen", options: { bold: true, breakLine: true } },
  { text: "23 y 25 oct, sin respuestas en el formulario. El 25 los anuncios estaban apagados: no provienen de Meta.", options: { breakLine: true } },
], { x: 6.8, y: 1.7, w: 2.55, h: 2.7, fontSize: 11, color: C.text1, valign: "top", objectName: "Leads body" });
T(s, "Meta gastó $71 el 21 oct con presupuesto de $45: recuperó parte de los días sin entrega.", { x: 0.5, y: 4.15, w: 5.9, h: 0.35, fontSize: 10, italic: true, color: C.accent6, objectName: "Daily note" });
s.addNotes("Revisar en GHL de dónde vienen los 4 contactos sin atribución (posible formulario de otro canal).");

// ---------- 5. Timeline ----------
pres.addSection({ title: "Qué hicimos" });
s = slide("CONTENT", "Qué hicimos");
s.addText("Cronología de cambios", { placeholder: "title" });
const events = [
  ["19 oct", "Rotación", "S10 pausado (criterio de corte). H3 activo. Banca de 6 anuncios H1–H6."],
  ["20 oct", "Cuenta bloqueada", "Pago rechazado ($102.28). Sin entrega."],
  ["21 oct", "Presupuesto", "Pago resuelto. $45/día para $1,000/mes con fines de semana apagados."],
  ["23 oct", "Rotación + pausa", "S11 pausado, H5 activo. Formulario instantáneo creado. Primera pausa de fin de semana."],
  ["26 oct", "Prueba A/B/C", "Landing corregida y landing de solo formulario. Prueba activa; hiperlocal en pausa."],
];
s.addShape(pres.shapes.LINE, { x: 0.8, y: 1.86, w: 8.4, h: 0, line: { color: C.accent3, width: 2 }, objectName: "Timeline line" });
events.forEach(([d, head, body], i) => {
  const x = 0.5 + i * 1.84;
  dot(s, x + 0.1, 1.65, String(i + 1), `Timeline dot ${i + 1}`, i === 4 ? C.accent1 : C.text2, i === 4 ? C.text2 : C.background1);
  T(s, d, { x, y: 2.25, w: 1.7, h: 0.35, fontSize: 13, bold: true, color: C.accent3, objectName: `Timeline date ${i + 1}` });
  T(s, head, { x, y: 2.6, w: 1.7, h: 0.45, fontSize: 15, bold: true, color: C.text2, fontFace: THEME.headFontFace, objectName: `Timeline head ${i + 1}` });
  T(s, body, { x, y: 3.1, w: 1.7, h: 1.6, fontSize: 12, color: C.text1, valign: "top", objectName: `Timeline body ${i + 1}` });
});
s.addNotes("Detalle y motivo de cada cambio en build/CHANGELOG_META.md.");

// ---------- 6. Ads of the week ----------
pres.addSection({ title: "Anuncios" });
s = slide("CONTENT", "Anuncios");
s.addText("Creativos de la semana (hiperlocal)", { placeholder: "title" });
const week = [
  ["S9-Attorneys-In-Person-Cost-Hyperlocal-2026-Oct", "S9 Attorneys", "$17.82 · CTR 2.67%", "7 visitas · 0 leads", C.accent4],
  ["S11-Immigration-Intake-Calls-Hyperlocal-2026-Oct", "🔵 S11 Intake Calls", "$97.45 · CPM $144", "3 visitas · pausado 23 oct", C.accent5],
  ["H3-Saturdays-Back-Hyperlocal-2026-Oct", "🔵 H3 Saturdays", "$41.47 · CPM $122", "3 visitas · 0 leads", C.accent6],
  ["H5-Phones-While-In-Court-Hyperlocal-2026-Oct", "🔵 H5 Phones in Court", "$20.13 · 2 clics", "1 lead: buscaba empleo", C.accent5],
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
s.addNotes("S10 gastó $0.58 antes de pausarse el 19 oct. Desde el 26 oct S9, H3 y H5 corren en la prueba A/B/C.");

// ---------- 7. A/B/C test ----------
s = slide("CONTENT", "Anuncios");
s.addText("Prueba A/B/C de destino", { placeholder: "title" });
s.addTable([["", "Destino", "Botón", "Presupuesto"],
  ["A", "Landing de solo formulario · /hire-form", "Book now", "$15/día"],
  ["B", "Landing completa corregida · /hire", "Book now", "$15/día"],
  ["C", "Formulario instantáneo de Meta", "Sign up", "$15/día"],
].map((r, i) => r.map((c, j) => ({ text: c, options: { bold: i === 0 || j === 0, color: i === 0 ? HEX.lt1 : (j === 0 ? HEX.dk2 : HEX.dk1),
  fill: { color: i === 0 ? HEX.dk2 : (i % 2 ? HEX.lt1 : HEX.lt2) }, valign: "middle", align: j === 0 ? "center" : "left" } }))),
{ x: 0.5, y: 1.15, w: 5.9, colW: [0.4, 3.0, 1.1, 1.4], rowH: 0.42, fontSize: 12, ...TBL, objectName: "Test table" });
T(s, [
  { text: "Diseño", options: { bold: true, color: HEX.dk2, breakLine: true } },
  { text: "Mismos anuncios (S9, H3, H5), mismo público: abogados en NY, NJ y PA, 30–65 años (6.6–7.8 M). Meta separa el público entre las tres versiones. Del 26 oct al 21 nov.", options: { breakLine: true } },
  { text: " ", options: { breakLine: true, fontSize: 6 } },
  { text: "Métrica: ", options: { bold: true } },
  { text: "costo por lead calificado en GHL. Con $15/día por versión el resultado será una tendencia, no estadística concluyente." },
], { x: 0.5, y: 3.0, w: 5.9, h: 1.9, fontSize: 12, color: C.text1, valign: "top", objectName: "Test design" });
const hc = 3.1, wc = hc * 640 / 1262;
capture(s, "TEST-B-S9-Attorneys-In-Person-Cost", 6.6, 1.1, hc, "Capture TEST B S9");
capture(s, "TEST-C-H5-Phones-While-In-Court", 6.6 + wc + 0.15, 1.1, hc, "Capture TEST C H5");
T(s, "B · landing", { x: 6.6, y: 4.3, w: wc, h: 0.3, fontSize: 10, italic: true, color: C.accent6, align: "center", objectName: "Test caption B" });
T(s, "C · formulario", { x: 6.6 + wc + 0.15, y: 4.3, w: wc, h: 0.3, fontSize: 10, italic: true, color: C.accent6, align: "center", objectName: "Test caption C" });
s.addNotes("Atribución en GHL: A y B por nombre del anuncio (TEST A/B); C por la etiqueta fb-instant-form. El lead de prueba de C llegó correctamente.");

// ---------- 8. Learnings ----------
pres.addSection({ title: "Aprendizajes" });
s = slide("CONTENT", "Aprendizajes");
s.addText("Hallazgos", { placeholder: "title" });
const learn = [
  ["El público hiperlocal se agotó en 10 días.", "939 personas alcanzadas en la semana; CPM de $65 a $114 y costo por visita de $5.65 a $11.09."],
  ["S9 (\"for the attorneys\") es el creativo más eficiente.", "CTR 2.67% y CPM $53: 7 de las 16 visitas de la semana con el 10% del gasto."],
  ["La asistente al teléfono atrae candidatos.", "H5 trajo un buscador de empleo; S11 llegó a CPM $144. La imagen se lee como un puesto de trabajo."],
  ["La landing no coincidía con el anuncio.", "Corregida el 26 oct: \"for law firms, from $15/hr\" y formulario más corto. Efecto medible desde esta semana."],
];
learn.forEach(([head, body], i) => {
  const y = 1.15 + i * 0.98;
  dot(s, 0.5, y + 0.05, String(i + 1), `Learning dot ${i + 1}`);
  T(s, head, { x: 1.15, y, w: 8.35, h: 0.42, fontSize: 16, bold: true, color: C.text2, valign: "middle", objectName: `Learning head ${i + 1}` });
  T(s, body, { x: 1.15, y: y + 0.42, w: 8.35, h: 0.4, fontSize: 13, color: C.text1, valign: "top", objectName: `Learning body ${i + 1}` });
});
s.addNotes("4 semanas sin lead calificado: la prueba A/B/C y el público ampliado son el siguiente paso lógico antes de cambiar de canal o de oferta.");

// ---------- 9. Conclusions ----------
pres.addSection({ title: "Conclusiones" });
s = slide("CONTENT", "Conclusiones");
s.addText("Conclusiones", { placeholder: "title" });
const good = [
  ["Pausa de fin de semana", "$0 sábado y domingo; presupuesto concentrado en días hábiles."],
  ["Creativo \"for the attorneys\"", "Mejor CTR y CPM de la semana (S9)."],
  ["Embudo corregido", "Landing alineada al anuncio, formulario corto y formulario instantáneo conectado a GHL."],
  ["Banca de creativos", "Rotaciones el mismo día (S10→H3, S11→H5) sin esperar diseño."],
];
const bad = [
  ["Audiencia hiperlocal", "Demasiado pequeña: CPM ×1.8 en una semana."],
  ["Imágenes de asistente al teléfono", "Atraen buscadores de empleo (H5)."],
  ["Método de pago", "Pago rechazado: 2 días sin entrega."],
  ["Leads calificados", "0 en 4 semanas. La prueba A/B/C busca el cuello de botella."],
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
s.addNotes("Las imágenes con persona estresada al teléfono funcionan como hook, pero sumadas a \"hire a part-time professional\" se leen como vacante.");

// ---------- 10. Plan ----------
pres.addSection({ title: "Próximos pasos" });
s = slide("CONTENT", "Próximos pasos");
s.addText("Plan · 26 oct – 1 nov", { placeholder: "title" });
const plan = [
  ["Prueba A/B/C sin cambios", "Correr al menos 2 semanas sin tocar anuncios ni presupuesto. Primera lectura el lunes 2 nov."],
  ["Seguimiento diario", "Leads por versión en GHL (TEST A, TEST B, fb-instant-form) y % de buscadores de empleo."],
  ["Presupuesto de noviembre", "$1,000/mes desde el 1 nov: $45/día hábil con pausa de fin de semana."],
];
plan.forEach(([head, body], i) => {
  const x = 0.5 + i * 3.07;
  card(s, x, 1.2, 2.86, 3.3, `Plan card ${i + 1}`);
  dot(s, x + 0.25, 1.45, String(i + 1), `Plan dot ${i + 1}`, C.text2, C.background1, 0.5);
  T(s, head, { x: x + 0.25, y: 2.15, w: 2.4, h: 0.6, fontSize: 17, bold: true, color: C.text2, fontFace: THEME.headFontFace, valign: "top", objectName: `Plan head ${i + 1}` });
  T(s, body, { x: x + 0.25, y: 2.8, w: 2.4, h: 1.6, fontSize: 13, color: C.text1, valign: "top", objectName: `Plan body ${i + 1}` });
});
s.addNotes("Gasto de octubre al 26 oct: $890.62. Próximo reporte: lunes 2 nov (semana 26 oct – 1 nov).");

// ---------- 11. Decisions ----------
s = slide("DARK_CONTENT", "Próximos pasos");
s.addText("Decisiones requeridas", { placeholder: "title" });
const dec = [
  ["Método de pago de respaldo", "Agregar una segunda tarjeta en Meta para que un rechazo no vuelva a detener la cuenta."],
  ["Producción de videos", "Aprobar 2–3 anuncios en video (9:16, abogado en cámara). Pendiente desde el 19 oct."],
  ["Creativos sin asistente al teléfono", "Pedir a Debi imágenes centradas en el abogado y texto en imagen desde la firma, no \"Hire a part-time professional\"."],
];
dec.forEach(([head, body], i) => {
  const y = 1.25 + i * 1.25;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 0.5, y: y + 0.05, w: 0.38, h: 0.38, fill: { color: C.text2 }, line: { color: C.accent1, width: 2 }, rectRadius: 0.06, objectName: `Decision box ${i + 1}` });
  T(s, head, { x: 1.1, y, w: 8.4, h: 0.45, fontSize: 18, bold: true, color: C.accent1, valign: "middle", objectName: `Decision head ${i + 1}` });
  T(s, body, { x: 1.1, y: y + 0.47, w: 8.4, h: 0.65, fontSize: 14, color: C.background1, valign: "top", objectName: `Decision body ${i + 1}` });
});
s.addNotes("Pendientes anteriores: categorías de la página (Recruiter, Real Estate), CPL calificado objetivo y CAPI solo para \"I want to hire.\".");

(async () => {
  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("written", OUT);
})();
