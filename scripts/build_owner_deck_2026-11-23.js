// Builds the owner deck (PowerPoint) for the week of 2026-11-16 to 2026-11-22 (delivered 2026-11-23). Run with NODE_PATH pointing to a node_modules that has pptxgenjs.
const pptxgen = require("pptxgenjs");
const path = require("path");
const { applyTheme } = require("/root/.claude/skills/synced/91214b57-4729-489d-a491-f28c7fe5eb8b_230bf34e-5a4e-4f30-a11c-45835a5a2a37/pptx/scripts/apply_theme.js");

const OUT = "/home/user/MetaADS2026/build/reports/informes/Informe_Meta_Ads_Orchid_2026-11-23.pptx";
const IMG = "/home/user/MetaADS2026/build/reports/previews/2026-11-23/";
const SIZE = { // px of each image, to keep aspect ratio
  "BF-Healthcare-Get-started-free-LPV-Nov19": [640, 1302], "SameWork-Healthcare-60-less-Nov19": [640, 1256],
  "BF-Entrepreneurs-Get-started-free-LPV-Nov19": [640, 1302], "SameWork-Entrepreneurs-60-less-Nov19": [640, 1296],
  "V2-Founders-Healthcare-Nov19": [640, 712], "IG-Followers-VA-Spanish-Vertical-9x16-Nov15": [640, 1152], "RT-Get-started-free-Nov16": [640, 1262],
  "lp_practices-free-month_short": [780, 1688], "lp_practices-free-month_long": [780, 1688],
  "lp_business-free-month_short": [780, 1688], "lp_business-free-month_long": [780, 1688],
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
pres.title = "Informe Meta Ads Orchid – Semana del 16 al 22 nov";
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
const FOOT = { text: "Orchid · Informe Meta Ads · Semana 16 – 22 nov 2026", options: { x: 0.5, y: 5.25, w: 6, h: 0.25, fontSize: 9, color: C.accent6, margin: 0 } };
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
const left = (rows, cols) => rows.map(r => r.map((c, j) => (cols.includes(j) ? { ...c, options: { ...c.options, align: "left" } } : c)));

// ---------- 1. Title ----------
pres.addSection({ title: "Resumen" });
let s = slide("DARK_TITLE", "Resumen");
s.addText("Informe semanal", { placeholder: "title" });
s.addText([
  { text: "Semana del 16 al 22 nov 2026", options: { breakLine: true } },
  { text: "Primera semana de Black Friday · Dirección de Orchid · 23 nov 2026", options: { fontSize: 14, color: C.background1 } },
], { placeholder: "body" });
s.addNotes("Primera semana de las campañas de Black Friday por mercado (salud y emprendedores), con retargeting, seguidores de Instagram y awareness.");

// ---------- 2. Executive summary ----------
s = slide("CONTENT", "Resumen");
s.addText("Resumen ejecutivo", { placeholder: "title" });
[["$326.64", "Inversión", "16 – 22 nov · 5 campañas"], ["0", "Leads calificados", "El único lead (17 nov) era falso"], ["249", "Visitas a la landing", "vs. 4 la semana anterior"]]
  .forEach(([big, label, sub], i) => {
    const x = 0.5 + i * 3.07;
    card(s, x, 1.25, 2.86, 2.15, `Stat card ${i + 1}`);
    T(s, big, { x: x + 0.25, y: 1.45, w: 2.4, h: 0.95, fontSize: 44, bold: true, color: i === 1 ? C.accent5 : C.text2, fontFace: THEME.headFontFace, objectName: `Stat ${i + 1}` });
    T(s, label, { x: x + 0.25, y: 2.45, w: 2.4, h: 0.35, fontSize: 15, bold: true, color: C.text1, objectName: `Stat label ${i + 1}` });
    T(s, sub, { x: x + 0.25, y: 2.8, w: 2.4, h: 0.45, fontSize: 11, color: C.accent6, objectName: `Stat note ${i + 1}` });
  });
T(s, [
  { text: "Ya llega gente a la landing, pero todavía no deja sus datos. ", options: { bold: true } },
  { text: "El 19 cambiamos la forma de comprar anuncios: el costo por clic bajó de $9.52 a $0.58 y las visitas pasaron de 7 a 239. Probamos el formulario de punta a punta y funciona; el problema es que los visitantes no se convierten. Ajustamos audiencia, ubicaciones y la medición del lead." },
], { x: 0.5, y: 3.7, w: 9, h: 1.1, fontSize: 13, color: C.text1, valign: "top", objectName: "Summary" });
s.addNotes("Noviembre al 22: $856.53 de $1,300 (presupuesto ampliado el 19 nov). Semana anterior: $224.77, 4 visitas, 0 leads calificados.");

// ---------- 3. Numbers vs last week ----------
pres.addSection({ title: "Resultados" });
s = slide("CONTENT", "Resultados");
s.addText("Números", { placeholder: "title" });
s.addTable(tb([
  ["", "9 – 15 nov", "16 – 22 nov"],
  ["Inversión", "$224.77", "$326.64"],
  ["Impresiones", "8,754", "19,920"],
  ["Clics en el enlace", "14", "391"],
  ["Visitas a la landing", "4", "249"],
  ["Leads en Meta", "1", "1"],
  ["Leads en GHL", "1", "1"],
  ["Leads calificados (quieren contratar)", "0", "0"],
  ["Buscadores de empleo", "1", "0"],
  ["Llamadas agendadas (reales)", "0", "0"],
  ["Costo por lead calificado", "—", "—"],
], { "7,2": HEX.accent5, "4,2": HEX.accent4, "3,2": HEX.accent4 }),
{ x: 0.5, y: 1.15, w: 5.6, colW: [3.2, 1.2, 1.2], rowH: 0.33, fontSize: 12, ...TBL, objectName: "Week table" });
card(s, 6.4, 1.15, 3.1, 3.6, "Week card");
T(s, [
  { text: "El lead del 17 nov", options: { bold: true, color: HEX.dk2, fontSize: 16, breakLine: true } },
  { text: "Llegó del anuncio de salud y dijo querer contratar, pero era falso: correo inválido, teléfono de otra persona y formulario llenado en 44 segundos. Quedó marcado como lead falso.", options: { breakLine: true } },
  { text: " ", options: { breakLine: true, fontSize: 6 } },
  { text: "Semana anterior", options: { bold: true, color: HEX.dk2, fontSize: 16, breakLine: true } },
  { text: "Solo abogados y awareness; el único lead buscaba empleo.", options: {} },
], { x: 6.6, y: 1.3, w: 2.75, h: 3.35, fontSize: 11, color: C.text1, valign: "top", objectName: "Week body" });
s.addNotes("Fuentes: Marketing API (insights por campaña) y GHL (contactos y envíos de formulario). Excluye pruebas (TEST 47–51) y el lead falso.");

// ---------- 4. Campaigns ----------
s = slide("CONTENT", "Resultados");
s.addText("Campañas", { placeholder: "title" });
s.addChart(pres.charts.DOUGHNUT, [{ name: "Inversión", labels: ["Emprendedores BF", "Salud BF", "Awareness", "Retargeting", "Seguidores IG"], values: [128.11, 120.62, 34.64, 22.91, 20.36] }], {
  x: 0.3, y: 1.1, w: 3.9, h: 3.9, objectName: "Spend split chart", holeSize: 55,
  chartColors: [HEX.dk2, HEX.accent3, HEX.accent1, HEX.accent6, HEX.accent4], showPercent: true, showValue: false, dataLabelColor: HEX.lt1, dataLabelFontSize: 10, dataLabelFontFace: "+mn-lt",
  showLegend: true, legendPos: "b", legendFontSize: 9, legendFontFace: "+mn-lt", legendColor: HEX.accent6,
});
s.addTable(tb([
  ["", "Salud", "Emprend.", "Retarg.", "Awareness", "IG"],
  ["Inversión", "$120.62", "$128.11", "$22.91", "$34.64", "$20.36"],
  ["Alcance", "4,289", "4,585", "896", "4,007", "1,400"],
  ["CPM", "$20.01", "$25.98", "$19.56", "$5.59", "$12.78"],
  ["Clics", "124", "151", "4", "1", "111"],
  ["Visitas landing", "109", "137", "3", "—", "—"],
  ["Leads (GHL)", "1*", "0", "0", "—", "—"],
  ["Calificados", "0", "0", "0", "—", "—"],
]), { x: 4.3, y: 1.15, w: 5.2, colW: [1.3, 0.8, 0.8, 0.75, 0.85, 0.7], rowH: 0.36, fontSize: 10, ...TBL, objectName: "Campaign table" });
T(s, "* Lead falso del 17 nov. CPM = costo por cada mil impresiones. IG: los clics son visitas al perfil.", { x: 4.3, y: 4.15, w: 5.2, h: 0.5, fontSize: 9, color: C.accent6, italic: true, valign: "top", objectName: "Campaign note" });
s.addNotes("Awareness: 1,200 reproducciones completas (ThruPlay) a $0.03. IG: 221 ThruPlay; el video vertical trajo 97 de las 111 visitas al perfil.");

// ---------- 5. Before / after the change ----------
s = slide("CONTENT", "Resultados");
s.addText("Cambio", { placeholder: "title" });
s.addTable(tb([
  ["Salud + Emprendedores", "16 – 18 nov", "19 – 22 nov"],
  ["Optimización", "Leads", "Visitas a la landing"],
  ["Inversión", "$95.19", "$153.54"],
  ["Impresiones", "495", "10,463"],
  ["Costo por mil impresiones", "$192", "$14.67"],
  ["Clics", "10", "265"],
  ["Costo por clic", "$9.52", "$0.58"],
  ["Visitas a la landing", "7", "239"],
  ["Leads reales", "0", "0"],
], { "4,2": HEX.accent4, "6,2": HEX.accent4, "7,2": HEX.accent4, "8,2": HEX.accent5 }),
{ x: 0.5, y: 1.15, w: 5.4, colW: [2.6, 1.3, 1.5], rowH: 0.38, fontSize: 12, ...TBL, objectName: "Phase table" });
card(s, 6.2, 1.15, 3.3, 3.45, "Phase card");
T(s, [
  { text: "Por qué cambiamos", options: { bold: true, color: HEX.dk2, fontSize: 15, breakLine: true } },
  { text: "Meta cobraba $192 por cada mil impresiones porque buscaba \"gente que deja leads\" y casi no tenía ejemplos. Optimizando por visitas, el tráfico se multiplicó por 30.", options: { breakLine: true } },
  { text: " ", options: { breakLine: true, fontSize: 6 } },
  { text: "Lo que falta", options: { bold: true, color: HEX.dk2, fontSize: 15, breakLine: true } },
  { text: "Que esas visitas llenen el formulario: 239 visitas y 0 envíos.", options: {} },
], { x: 6.4, y: 1.3, w: 2.95, h: 3.2, fontSize: 11, color: C.text1, valign: "top", objectName: "Phase body" });
s.addNotes("16–18 nov: conjuntos con optimización a Lead, solo feed de Facebook, horario 6 am–10 pm. 19 nov: conjuntos nuevos optimizados a visitas, ubicaciones Facebook e Instagram, $20/día cada uno.");

// ---------- 6. Ads ----------
pres.addSection({ title: "Anuncios" });
s = slide("CONTENT", "Anuncios");
s.addText("Anuncios", { placeholder: "title" });
[["BF-Healthcare-Get-started-free-LPV-Nov19", "Salud · Black Friday", "$58.67 · 86 visitas · 0 leads"],
 ["SameWork-Healthcare-60-less-Nov19", "Salud · Same work", "$14.92 · 19 visitas · 0 leads"],
 ["BF-Entrepreneurs-Get-started-free-LPV-Nov19", "Emprend. · Black Friday", "$13.00 · 25 visitas · 0 leads"],
 ["SameWork-Entrepreneurs-60-less-Nov19", "Emprend. · Same work", "$60.54 · 108 visitas · 0 leads"]]
  .forEach(([file, name, sub], i) => {
    const x = 0.45 + i * 2.3, h = 3.05, [pw, ph] = SIZE[file], w = h * pw / ph;
    capture(s, file, x + (2.1 - w) / 2, 1.0, h, `Ad ${name}`);
    T(s, name, { x, y: 4.15, w: 2.1, h: 0.3, fontSize: 11, bold: true, color: C.text2, align: "center", objectName: `Ad name ${i + 1}` });
    T(s, sub, { x, y: 4.45, w: 2.1, h: 0.4, fontSize: 9, color: C.accent6, align: "center", objectName: `Ad sub ${i + 1}` });
  });
s.addNotes("Activos desde el 19 nov, con botón \"Book now\". Los anuncios del 16 nov (optimizados a leads) gastaron $101.60 con 8 visitas y quedaron pausados.");

s = slide("CONTENT", "Anuncios");
s.addText("Video", { placeholder: "title" });
[["V2-Founders-Healthcare-Nov19", "Awareness · Fundadores", "Andrea y Josué · desde el 19 nov · $11.17 · 355 ThruPlay"],
 ["IG-Followers-VA-Spanish-Vertical-9x16-Nov15", "Seguidores IG", "$16.50 · 97 visitas al perfil"],
 ["RT-Get-started-free-Nov16", "Retargeting", "$22.91 · 3 visitas · 0 leads"]]
  .forEach(([file, name, sub], i) => {
    const x = 0.6 + i * 3.05, h = 3.0, [pw, ph] = SIZE[file], w = Math.min(h * pw / ph, 2.7), hh = w * ph / pw;
    capture(s, file, x + (2.7 - w) / 2, 1.0 + (h - hh) / 2, hh, `Video ${name}`);
    T(s, name, { x, y: 4.1, w: 2.7, h: 0.3, fontSize: 12, bold: true, color: C.text2, align: "center", objectName: `Video name ${i + 1}` });
    T(s, sub, { x, y: 4.4, w: 2.7, h: 0.45, fontSize: 9, color: C.accent6, align: "center", objectName: `Video sub ${i + 1}` });
  });
s.addNotes("Awareness: $1/día por mercado, video POV y video de fundadores. Retargeting pasó a optimizar por alcance el 19 nov ($11.50 hasta el 30). Seguidores IG: 54 hoy (registro diario desde el 20 nov).");

// ---------- 7. Landings ----------
s = slide("CONTENT", "Anuncios");
s.addText("Landings", { placeholder: "title" });
[["lp_practices-free-month_short", "Salud · corta", "go.orchidpros.com/practices-free-month", "94 visitas · 0 envíos"],
 ["lp_practices-free-month_long", "Salud · larga", "go.orchidpros.com/practices-free-month-page-865761", "80 visitas · 0 envíos"],
 ["lp_business-free-month_short", "Emprend. · corta", "go.orchidpros.com/business-free-month", "168 visitas · 0 envíos"],
 ["lp_business-free-month_long", "Emprend. · larga", "go.orchidpros.com/business-free-month-page", "195 visitas · 0 envíos"]]
  .forEach(([file, name, url, sub], i) => {
    const x = 0.45 + i * 2.3, h = 2.85, [pw, ph] = SIZE[file], w = h * pw / ph;
    capture(s, file, x + (2.1 - w) / 2, 0.95, h, `Landing ${name}`);
    T(s, name, { x, y: 3.9, w: 2.1, h: 0.28, fontSize: 11, bold: true, color: C.text2, align: "center", objectName: `Landing name ${i + 1}` });
    T(s, [{ text: url.replace("go.orchidpros.com/", "/"), options: { hyperlink: { url: "https://" + url, tooltip: "Abrir landing" }, color: HEX.dk2, underline: true } }],
      { x, y: 4.18, w: 2.1, h: 0.25, fontSize: 8, align: "center", objectName: `Landing link ${i + 1}` });
    T(s, sub, { x, y: 4.45, w: 2.1, h: 0.3, fontSize: 9, color: C.accent6, align: "center", objectName: `Landing sub ${i + 1}` });
  });
T(s, "Prueba A/B al 50 %: la misma URL muestra la versión corta o la larga. Visitas según GHL hasta el 23 nov (sin contar pruebas).", { x: 0.5, y: 4.8, w: 9, h: 0.3, fontSize: 9, italic: true, color: C.accent6, objectName: "Landing note" });
s.addNotes("Newsletter: go.orchidpros.com/brief. La versión larga tiene video de los fundadores, foto de Josué y Andrea y el formulario al final de la página.");

// ---------- 8. Measurement ----------
pres.addSection({ title: "Aprendizajes" });
s = slide("CONTENT", "Aprendizajes");
s.addText("Medición", { placeholder: "title" });
const meas = [
  ["El formulario funciona", "Prueba de punta a punta el 23 nov (TEST 50 y 51): envío, página de gracias, contacto en GHL, oportunidad y flujos. Los 0 leads son reales, no un error."],
  ["Meta casi no recibía el lead", "El evento Lead se perdía al saltar a la página de gracias. Ahora se envía desde la página de gracias: Meta aprenderá de cada lead real."],
  ["El \"lead calificado\" sale con cualquier envío", "El flujo de GHL avisa a Meta aunque el lead sea falso o de prueba. Pendiente: que salga solo cuando ventas confirma."],
];
meas.forEach(([head, body], i) => {
  const y = 1.15 + i * 1.2;
  card(s, 0.5, y, 9, 1.05, `Measure card ${i + 1}`);
  T(s, head, { x: 0.75, y: y + 0.1, w: 8.5, h: 0.35, fontSize: 15, bold: true, color: C.text2, objectName: `Measure head ${i + 1}` });
  T(s, body, { x: 0.75, y: y + 0.45, w: 8.5, h: 0.55, fontSize: 12, color: C.text1, valign: "top", objectName: `Measure body ${i + 1}` });
});
s.addNotes("Las pruebas quedaron marcadas (test, lead-falso), fuera del flujo de seguimiento y con la oportunidad cerrada.");

s = slide("CONTENT", "Aprendizajes");
s.addText("Hallazgos", { placeholder: "title" });
const learn = [
  ["Optimizar por leads sin historial sale carísimo.", "$192 por mil impresiones y $9.52 por clic. Por visitas: $14.67 y $0.58."],
  ["El tráfico barato no es tráfico con intención.", "Casi 70% del gasto iba a Reels y a mayores de 65. El 20 nov quitamos ubicaciones de baja intención y limitamos la edad a 64."],
  ["\"Same work\" atrae más clics que Black Friday.", "En emprendedores trajo 108 de las 133 visitas; el ángulo de ahorro engancha, pero aún no convierte."],
  ["La landing larga esconde el formulario.", "En celular está a ~34 pantallas. Ajustamos la barra del botón; el formulario debería subir."],
];
learn.forEach(([head, body], i) => {
  const y = 1.15 + i * 0.98;
  dot(s, 0.5, y + 0.05, String(i + 1), `Learning dot ${i + 1}`);
  T(s, head, { x: 1.15, y, w: 8.35, h: 0.42, fontSize: 15, bold: true, color: C.text2, valign: "middle", objectName: `Learning head ${i + 1}` });
  T(s, body, { x: 1.15, y: y + 0.42, w: 8.35, h: 0.4, fontSize: 12, color: C.text1, valign: "top", objectName: `Learning body ${i + 1}` });
});
s.addNotes("Fuentes externas: costo promedio por lead en staffing de EE. UU. ~$28 (Superads); formularios de Meta con filtro pueden costar la mitad por lead bueno (prueba de Jon Loomer).");

// ---------- 9. Timeline ----------
pres.addSection({ title: "Qué hicimos" });
s = slide("CONTENT", "Qué hicimos");
s.addText("Cronología", { placeholder: "title" });
const events = [
  ["16 nov", "Lanzamiento", "Salud, emprendedores, retargeting, seguidores IG y awareness activos a las 2 am."],
  ["17 nov", "Lead falso", "Revisado y marcado. Plan contra falsos listo si se repite."],
  ["19 nov", "Por visitas", "Conjuntos nuevos a $20/día, Facebook e Instagram, audiencias por dueños, \"Book now\", Same work y video de fundadores."],
  ["20 nov", "Menos Reels", "Fuera Reels overlay, Marketplace y búsqueda; edad hasta 64."],
  ["23 nov", "Medición", "Prueba del formulario, Lead en página de gracias y arreglos en la landing larga."],
];
s.addShape(pres.shapes.LINE, { x: 0.8, y: 1.86, w: 8.4, h: 0, line: { color: C.accent3, width: 2 }, objectName: "Timeline line" });
events.forEach(([d, head, body], i) => {
  const x = 0.5 + i * 1.84;
  dot(s, x + 0.1, 1.65, String(i + 1), `Timeline dot ${i + 1}`, i === 4 ? C.accent1 : C.text2, i === 4 ? C.text2 : C.background1);
  T(s, d, { x, y: 2.25, w: 1.7, h: 0.35, fontSize: 13, bold: true, color: C.accent3, objectName: `Timeline date ${i + 1}` });
  T(s, head, { x, y: 2.6, w: 1.7, h: 0.45, fontSize: 15, bold: true, color: C.text2, fontFace: THEME.headFontFace, objectName: `Timeline head ${i + 1}` });
  T(s, body, { x, y: 3.1, w: 1.7, h: 1.8, fontSize: 10.5, color: C.text1, valign: "top", objectName: `Timeline body ${i + 1}` });
});
s.addNotes("19 nov: presupuesto de noviembre ampliado a $1,300. Retargeting pasó a alcance. Detalle en build/CHANGELOG_META.md.");

// ---------- 10. Plan ----------
pres.addSection({ title: "Próximos pasos" });
s = slide("CONTENT", "Próximos pasos");
s.addText("Plan semanal", { placeholder: "title" });
const plan = [
  ["Formulario en Meta", "Probar el formulario dentro de Facebook e Instagram, con preguntas que filtren, al lado de la landing. Comparar costo por lead calificado."],
  ["Cerrar Black Friday", "La oferta termina el 1 dic. Hasta entonces, foco en salud y emprendedores; ~$444 disponibles en noviembre."],
  ["Creativos nuevos", "Comparativos de otro ángulo (tabla y mismo horario) para sumar a \"Same work\" y apagar el que peor rinda."],
];
plan.forEach(([head, body], i) => {
  const x = 0.5 + i * 3.07;
  card(s, x, 1.2, 2.86, 3.3, `Plan card ${i + 1}`);
  dot(s, x + 0.25, 1.45, String(i + 1), `Plan dot ${i + 1}`, C.text2, C.background1, 0.5);
  T(s, head, { x: x + 0.25, y: 2.15, w: 2.4, h: 0.6, fontSize: 17, bold: true, color: C.text2, fontFace: THEME.headFontFace, valign: "top", objectName: `Plan head ${i + 1}` });
  T(s, body, { x: x + 0.25, y: 2.8, w: 2.4, h: 1.6, fontSize: 12.5, color: C.text1, valign: "top", objectName: `Plan body ${i + 1}` });
});
s.addNotes("Próximo informe: lunes 30 nov (semana 23 – 29 nov), con el cierre de Black Friday.");

(async () => {
  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log("written", OUT);
})();
