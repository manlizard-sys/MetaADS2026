"""Validate copy limits/rules and write build/copy.md."""
import pathlib, re, sys
from copy_data import PRIMARY, HEADLINES, DESCRIPTIONS, BANNED

ROOT = pathlib.Path(__file__).resolve().parent.parent
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿]")
errors = []


def check(label, text, limit):
    n = len(text)
    low = text.lower()
    for b in BANNED:
        if b in low:
            errors.append(f"{label}: contains '{b}'")
    if len(EMOJI.findall(text)) > 1:
        errors.append(f"{label}: more than one emoji")
    if n > limit:
        errors.append(f"{label}: {n} > {limit}")
    if len(text.split("\n")[0]) > 125:
        errors.append(f"{label}: hook (first line) > 125 visible chars")
    if re.search(r"\b[A-Z]{4,}\b", text):
        errors.append(f"{label}: sustained caps")
    return n


md = ["# ORCHID - Leads - Hire a VA - 2026-10 · Copy (pendiente de aprobación)\n",
      "## Primary text\n", "| # | Ángulo | Texto | Caracteres | Límite |", "|---|---|---|---|---|"]
for i, (angle, limit, t) in enumerate(PRIMARY, 1):
    n = check(f"P{i}", t, limit)
    md.append(f"| P{i} | {angle} | {t.replace(chr(10), '<br>')} | {n} | ≤{limit} |")
md += ["\n## Headline\n", "| # | Texto | Caracteres |", "|---|---|---|"]
for i, t in enumerate(HEADLINES, 1):
    md.append(f"| H{i} | {t} | {check(f'H{i}', t, 40)} |")
md += ["\n## Description\n", "| # | Texto | Caracteres |", "|---|---|---|"]
for i, t in enumerate(DESCRIPTIONS, 1):
    md.append(f"| D{i} | {t} | {check(f'D{i}', t, 30)} |")

if not any(all(k in t.lower() for k in ("intake", "scheduling", "follow-up", "paperwork")) for _, _, t in PRIMARY):
    errors.append("No primary text mentions legal/real estate/medical task examples")
md.insert(3, "")
md[1:1] = ["Hook = primera línea (≤125 visibles). Conteo con emojis como 1 carácter.\n"]
(ROOT / "build" / "copy.md").write_text("\n".join(md) + "\n")
print("\n".join(md))
if errors:
    sys.exit("\nERRORS:\n" + "\n".join(errors))
print("\nAll copy within limits and rules.")
