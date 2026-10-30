"""Technical performance workbook for the Sunny Bliss Meta account (read-only).

One sheet per dimension: daily trend, ads, interactions, video, age, gender, age x gender,
US state, Comscore market, placement, device, hour of day, plus CRM lead quality when a GHL export exists.
Raw counts come from the Marketing API; rates (CTR, CPM, CPC, CPL, conversion rates,
video retention) are Excel formulas so the workbook recalculates.
Usage: python3 tech_report.py [--since 2026-09-29] [--until 2026-10-11]
Output: build/reports/informes/Reporte_tecnico_Meta_<since>_<until>.xlsx
"""
import glob, json, sys
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
import config as C
from meta import get_all, MetaError, BUILD

C.require("AD_ACCOUNT")
ACT = C.AD_ACCOUNT
arg = lambda k, d: sys.argv[sys.argv.index(k) + 1] if k in sys.argv else d
import datetime as _dt
_today = _dt.date.today()
SINCE = arg("--since", (_today - _dt.timedelta(days=30)).isoformat())
UNTIL = arg("--until", (_today - _dt.timedelta(days=1)).isoformat())
TR = json.dumps({"since": SINCE, "until": UNTIL})
FIELDS = ("spend,impressions,reach,clicks,inline_link_clicks,actions,video_play_actions,"
          "video_p25_watched_actions,video_p50_watched_actions,video_p75_watched_actions,"
          "video_p100_watched_actions,video_thruplay_watched_actions")

# Raw columns: (header, extractor). Rates are added as formulas.
ACT_TYPES = {"lpv": "landing_page_view", "lead": C.RESULT_TYPES[0], "eng": "post_engagement", "react": "post_reaction",
             "comment": "comment", "share": "post", "save": "onsite_conversion.post_save", "v3": "video_view"}


def acts(r):
    return {a["action_type"]: float(a["value"]) for a in r.get("actions") or []}


def first(r, k):
    v = r.get(k) or []
    return float(v[0]["value"]) if v else 0.0


RAW = [
    ("Gasto (USD)", lambda r, a: float(r.get("spend", 0))),
    ("Impresiones", lambda r, a: int(r.get("impressions", 0))),
    ("Alcance", lambda r, a: int(r["reach"]) if r.get("reach") else None),
    ("Clics (todos)", lambda r, a: int(r.get("clicks", 0))),
    ("Clics en enlace", lambda r, a: int(r.get("inline_link_clicks", 0))),
    ("Landing page views", lambda r, a: a.get(ACT_TYPES["lpv"], 0)),
    ("Leads (Meta)", lambda r, a: a.get(ACT_TYPES["lead"], 0)),
    ("Interacciones", lambda r, a: a.get(ACT_TYPES["eng"], 0)),
    ("Reacciones", lambda r, a: a.get(ACT_TYPES["react"], 0)),
    ("Comentarios", lambda r, a: a.get(ACT_TYPES["comment"], 0)),
    ("Compartidos", lambda r, a: a.get(ACT_TYPES["share"], 0)),
    ("Guardados", lambda r, a: a.get(ACT_TYPES["save"], 0)),
    ("Reproducciones 3 s", lambda r, a: a.get(ACT_TYPES["v3"], 0)),
    ("Video 25%", lambda r, a: first(r, "video_p25_watched_actions")),
    ("Video 50%", lambda r, a: first(r, "video_p50_watched_actions")),
    ("Video 75%", lambda r, a: first(r, "video_p75_watched_actions")),
    ("Video 100%", lambda r, a: first(r, "video_p100_watched_actions")),
    ("ThruPlay", lambda r, a: first(r, "video_thruplay_watched_actions")),
]
# Formula columns: (header, template using {Gasto} style names, number format)
FORM = [
    ("Frecuencia", "IF({Alcance}>0,{Impresiones}/{Alcance},\"\")", "0.00"),
    ("CTR enlace", "IF({Impresiones}>0,{Clics en enlace}/{Impresiones},\"\")", "0.00%"),
    ("CPM (USD)", "IF({Impresiones}>0,{Gasto (USD)}/{Impresiones}*1000,\"\")", "$#,##0.00"),
    ("CPC enlace (USD)", "IF({Clics en enlace}>0,{Gasto (USD)}/{Clics en enlace},\"\")", "$#,##0.00"),
    ("CPL Meta (USD)", "IF({Leads (Meta)}>0,{Gasto (USD)}/{Leads (Meta)},\"\")", "$#,##0.00"),
    ("Clic → LPV", "IF({Clics en enlace}>0,{Landing page views}/{Clics en enlace},\"\")", "0.0%"),
    ("LPV → lead", "IF({Landing page views}>0,{Leads (Meta)}/{Landing page views},\"\")", "0.0%"),
    ("Tasa de interacción", "IF({Impresiones}>0,{Interacciones}/{Impresiones},\"\")", "0.00%"),
    ("Hook rate (3 s / imp.)", "IF({Impresiones}>0,{Reproducciones 3 s}/{Impresiones},\"\")", "0.0%"),
    ("Retención 100% / 3 s", "IF({Reproducciones 3 s}>0,{Video 100%}/{Reproducciones 3 s},\"\")", "0.0%"),
]

ARIAL = "Arial"
HEAD = Font(name=ARIAL, bold=True, color="FFFFFF")
HFILL = PatternFill("solid", fgColor="3B1C78")
TFILL = PatternFill("solid", fgColor="F3F0FA")
BODY = Font(name=ARIAL)
BOLD = Font(name=ARIAL, bold=True)


def insights(**kw):
    return get_all(f"{ACT}/insights", time_range=TR, fields=FIELDS, limit=500, **kw)


def write_table(ws, dims, rows, note=None, sort=True, total=True):
    """dims: list of (header, extractor). Writes raw + formula columns and a total row."""
    heads = [d[0] for d in dims] + [h for h, _ in RAW] + [h for h, _, _ in FORM]
    ws.append(heads)
    for c in ws[1]:
        c.font, c.fill, c.alignment = HEAD, HFILL, Alignment(wrap_text=True, vertical="center")
    col = {h: get_column_letter(i + 1) for i, h in enumerate(heads)}
    data = []
    for r in rows:
        a = acts(r)
        data.append([f(r) for _, f in dims] + [f(r, a) for _, f in RAW])
    if sort:
        data.sort(key=lambda x: -x[len(dims)])
    for i, vals in enumerate(data, start=2):
        ws.append(vals)
        for h, tpl, fmt in FORM:
            c = ws[f"{col[h]}{i}"]
            c.value = "=" + tpl.format(**{k: f"{v}{i}" for k, v in col.items()})
            c.number_format = fmt
    last = len(data) + 1
    if total and data:
        t = last + 1
        ws.cell(row=t, column=1, value="Total")
        for h, _ in RAW:
            if h == "Alcance":
                continue  # reach is not additive across segments
            ws[f"{col[h]}{t}"] = f"=SUM({col[h]}2:{col[h]}{last})"
        for h, tpl, fmt in FORM:
            c = ws[f"{col[h]}{t}"]
            c.value = "=" + tpl.format(**{k: f"{v}{t}" for k, v in col.items()})
            c.number_format = fmt
        for c in ws[t]:
            c.font, c.fill = BOLD, TFILL
        last = t
    for row in ws.iter_rows(min_row=2, max_row=last):
        for c in row:
            if c.font != BOLD:
                c.font = BODY
            if c.column_letter == col["Gasto (USD)"]:
                c.number_format = "$#,##0.00"
            elif heads[c.column - 1] in [h for h, _ in RAW]:
                c.number_format = "#,##0"
    if note:
        ws.cell(row=last + 2, column=1, value=note).font = Font(name=ARIAL, italic=True, color="6B6680")
    ws.freeze_panes = ws.cell(row=2, column=len(dims) + 1)
    for i, h in enumerate(heads, start=1):
        ws.column_dimensions[get_column_letter(i)].width = 26 if i <= len(dims) else 13
    ws.row_dimensions[1].height = 32


wb = Workbook()
ws = wb.active
ws.title = "Resumen"

sheets = [
    ("Diario", [("Fecha", lambda r: r["date_start"])], dict(time_increment=1), None, False),
    ("Anuncios", [("Anuncio", lambda r: r["ad_name"])], dict(level="ad", fields=FIELDS + ",ad_name"), None, True),
    ("Edad", [("Edad", lambda r: r["age"])], dict(breakdowns="age"), None, True),
    ("Género", [("Género", lambda r: {"female": "Mujer", "male": "Hombre"}.get(r["gender"], "Sin dato"))], dict(breakdowns="gender"), None, True),
    ("Edad x Género", [("Edad", lambda r: r["age"]), ("Género", lambda r: {"female": "Mujer", "male": "Hombre"}.get(r["gender"], "Sin dato"))], dict(breakdowns="age,gender"), None, True),
    ("Estado", [("Región", lambda r: r["region"])], dict(breakdowns="region"),
     "Meta no reporta landing page views ni leads por región (restricción de privacidad): esas columnas salen en 0.", True),
    ("Mercado", [("Mercado (Comscore)", lambda r: r.get("comscore_market", ""))], dict(breakdowns="comscore_market"),
     "Mercado de Comscore: reemplazo de Meta para el desglose por DMA, retirado.", True),
    ("Placement", [("Plataforma", lambda r: r["publisher_platform"]), ("Posición", lambda r: r["platform_position"])],
     dict(breakdowns="publisher_platform,platform_position"), None, True),
    ("Dispositivo", [("Dispositivo", lambda r: r["impression_device"])], dict(breakdowns="impression_device"), None, True),
    ("Hora", [("Hora (zona de la cuenta)", lambda r: r["hourly_stats_aggregated_by_advertiser_time_zone"][:5])],
     dict(breakdowns="hourly_stats_aggregated_by_advertiser_time_zone", fields=FIELDS.replace("reach,", "")),
     "Meta no entrega alcance por hora.", False),
]
for name, dims, kw, note, sort in sheets:
    try:
        f = kw.pop("fields", FIELDS)
        rows = get_all(f"{ACT}/insights", time_range=TR, fields=f, limit=500, **kw)
    except MetaError as e:
        print(f"{name}: sin datos ({str(e).splitlines()[0][:120]})")
        continue
    if not rows:
        print(f"{name}: sin datos en el periodo")
        continue
    write_table(wb.create_sheet(name), dims, rows, note, sort, total=True)
    print(f"{name}: {len(rows)} filas")

# GHL lead quality (no personal data)
g = sorted(glob.glob(str(BUILD / "reports" / "ghl-*.json")))
if g:
    q = wb.create_sheet("Calidad de leads")
    q.append(["Fecha (UTC)", "Anuncio de origen", "Hiring or job seeking", "Vertical", "Agendó", "Clasificación"])
    for c in q[1]:
        c.font, c.fill = HEAD, HFILL
    period = [c for c in json.load(open(g[-1]))["contacts"] if SINCE <= c["date"] <= UNTIL]
    for c in sorted(period, key=lambda x: x["date"]):
        q.append([c["date"], c["ad"], c.get("hiring_or_job", ""), c.get("vertical", ""), "Sí" if c.get("booked") else "No",
                  "No calificado" if c["job_seeker"] else ("Calificado" if c.get("hiring_or_job") else "Sin respuesta")])
    n = q.max_row
    q.append([])
    q.append(["Calificados", f'=COUNTIF(F2:F{n},"Calificado")'])
    q.append(["No calificados", f'=COUNTIF(F2:F{n},"No calificado")'])
    q.append(["% no calificados (con respuesta)", f"=IF(B{n+2}+B{n+3}>0,B{n+3}/(B{n+2}+B{n+3}),\"\")"])
    q[f"B{n+4}"].number_format = "0.0%"
    q.append([f"Fuente: GHL ({g[-1].split('/')[-1]}), contactos creados entre {SINCE} y {UNTIL}, sin datos personales. "
              ""])
    for row in q.iter_rows():
        for c in row:
            if c.row > 1:
                c.font = BODY
    for col, w in zip("ABCDEF", (14, 38, 24, 26, 10, 16)):
        q.column_dimensions[col].width = w

# Summary sheet: links to the Diario totals row
d = wb["Diario"]
tot = next(r for r in range(2, d.max_row + 1) if d.cell(row=r, column=1).value == "Total")
hd = {c.value: c.column_letter for c in d[1]}
ws.append(["Reporte técnico · Meta Ads · Sunny Bliss"])
ws["A1"].font = Font(name=ARIAL, bold=True, size=14, color="3B1C78")
ws.append([f"Periodo: {SINCE} a {UNTIL} · cuenta {ACT}"])
ws.append([])
ws.append(["Métrica", "Valor"])
for c in ws[4]:
    c.font, c.fill = HEAD, HFILL
for label in ["Gasto (USD)", "Impresiones", "Clics en enlace", "Landing page views", "Leads (Meta)", "Interacciones",
              "Reproducciones 3 s", "ThruPlay", "CTR enlace", "CPM (USD)", "CPC enlace (USD)", "CPL Meta (USD)",
              "Clic → LPV", "LPV → lead", "Hook rate (3 s / imp.)", "Retención 100% / 3 s"]:
    ws.append([label, f"=Diario!{hd[label]}{tot}"])
    c = ws.cell(row=ws.max_row, column=2)
    c.number_format = d[f"{hd[label]}{tot}"].number_format
ws.append(["Alcance (personas únicas)", int(insights()[0].get("reach", 0))])
ws.cell(row=ws.max_row, column=2).number_format = "#,##0"
ws.append(["Frecuencia", f"=IF(B{ws.max_row}>0,B6/B{ws.max_row},\"\")"])
ws.cell(row=ws.max_row, column=2).number_format = "0.00"
ws.append([])
ws.append(["Notas"])
ws.cell(row=ws.max_row, column=1).font = BOLD
for t in ["Fuente: Meta Marketing API (atribución por defecto de la cuenta). Pueden variar levemente frente a Ads Manager.",
          "Tasas calculadas con fórmulas en cada hoja: CTR = clics en enlace / impresiones; CPL Meta = gasto / leads de Meta.",
          "Lead (Meta) cuenta todo formulario enviado; la calidad real está en la hoja 'Calidad de leads' (GHL).",
          "Alcance no es sumable entre segmentos; el total de cada hoja lo omite."]:
    ws.append([t])
for row in ws.iter_rows(min_row=2):
    for c in row:
        if c.font != HEAD and not c.font.bold:
            c.font = BODY
ws.column_dimensions["A"].width = 34
ws.column_dimensions["B"].width = 16

out = BUILD / "reports" / "informes" / f"Reporte_tecnico_Meta_{SINCE}_{UNTIL}.xlsx"
out.parent.mkdir(parents=True, exist_ok=True)
wb.save(out)
print(out)
