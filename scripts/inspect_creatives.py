"""Step 1.6: inspect ./creatives with ffprobe and check Meta video specs. Groups by concept (9:16 + 4:5)."""
import json, subprocess, shutil, pathlib, re, collections, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
FFPROBE = shutil.which("ffprobe")
if not FFPROBE:
    sys.exit("ffprobe not found. Install ffmpeg (apt-get install ffmpeg) and rerun.")

files = sorted(p for p in (ROOT / "creatives").iterdir() if p.suffix.lower() in (".mp4", ".mov"))
rows = []
for f in files:
    d = json.loads(subprocess.run([FFPROBE, "-v", "error", "-print_format", "json", "-show_format",
                                   "-show_streams", str(f)], capture_output=True, text=True).stdout)
    v = next(s for s in d["streams"] if s["codec_type"] == "video")
    w, h = int(v["width"]), int(v["height"])
    rot = abs(int(v.get("tags", {}).get("rotate", 0) or next(
        (sd.get("rotation", 0) for sd in v.get("side_data_list", []) if "rotation" in sd), 0)))
    if rot in (90, 270):
        w, h = h, w
    dur = float(d["format"]["duration"])
    mb = f.stat().st_size / 1e6
    has_audio = any(s["codec_type"] == "audio" for s in d["streams"])
    r = w / h
    aspect = "9:16" if abs(r - 9 / 16) < .02 else "4:5" if abs(r - .8) < .02 else "1:1" if abs(r - 1) < .02 else f"{w}x{h}"
    issues = []
    if aspect not in ("9:16", "4:5"): issues.append(f"aspect {aspect} (need 9:16 or 4:5)")
    if min(w, h) < 1080: issues.append(f"short side {min(w, h)}px < 1080 recommended")
    if mb > 4000: issues.append("file > 4 GB")
    if aspect == "9:16" and dur > 60: issues.append("> 60 s: Stories will split/cut")
    if aspect == "9:16" and dur > 90: issues.append("> 90 s: exceeds Reels ads max")
    if dur < 1: issues.append("< 1 s")
    if v["codec_name"] not in ("h264", "hevc"): issues.append(f"codec {v['codec_name']}")
    if not has_audio: issues.append("no audio track")
    concept = re.sub(r"[_\- ]*(9x16|9-16|9_16|916|4x5|4-5|4_5|45|vertical|feed|story|stories|reels?)\b", "",
                     f.stem, flags=re.I).strip("_- ")
    rows.append(dict(file=f.name, concept=concept, width=w, height=h, aspect=aspect, duration_s=round(dur, 2),
                     size_mb=round(mb, 1), codec=v["codec_name"], audio=has_audio, issues=issues))

concepts = collections.defaultdict(dict)
for r in rows:
    concepts[r["concept"]][r["aspect"]] = r["file"]
for c, g in concepts.items():
    missing = {"9:16", "4:5"} - set(g)
    if missing:
        print(f"Concept '{c}' is missing: {', '.join(sorted(missing))}")
print(json.dumps(rows, indent=2))
(ROOT / "build" / "creatives.json").write_text(json.dumps({"files": rows, "concepts": concepts}, indent=2))
