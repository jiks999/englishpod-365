# -*- coding: utf-8 -*-
"""生成可公开发布的轻量版（不含任何本地音频/PDF/转写文本，音频走 archive.org 在线源）。
产物：dist/index.html + dist/data.js
用法：python scripts/build_lite.py
"""
import os, csv, json, shutil

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(BASE, "dist")
IA = "https://archive.org/download/englishpod_all/englishpod_%04ddg.mp3"

titles = {r["id"]: r for r in json.load(open(os.path.join(BASE, "titles.json"), encoding="utf-8"))}
rows = list(csv.DictReader(open(os.path.join(BASE, "EnglishPod_365_目录.csv"), encoding="utf-8-sig")))

items = []
for r in rows:
    i = int(r["期号"])
    items.append({
        "id": i,
        "code": titles[i]["code"] or "",
        "topic": r["栏目/级别"],
        "title": r["标题"],
        "pdf": "",
        "srt": "",
        "audio": "",
        "atype": "",
        "online": IA % i,
        "text": "",
    })

os.makedirs(DIST, exist_ok=True)
data = {"generated": "2026-11-18", "lite": True, "items": items}
with open(os.path.join(DIST, "data.js"), "w", encoding="utf-8") as f:
    f.write("window.EP_DATA=" + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n")

html = open(os.path.join(BASE, "EnglishPod.html"), encoding="utf-8").read()
html = html.replace('<script src="web/data.js"></script>', '<script src="data.js"></script>')
open(os.path.join(DIST, "index.html"), "w", encoding="utf-8").write(html)

print("dist ready:", DIST)
print("  data.js", round(os.path.getsize(os.path.join(DIST, "data.js")) / 1024, 1), "KB")
print("  index.html", round(os.path.getsize(os.path.join(DIST, "index.html")) / 1024, 1), "KB")
print("  items", len(items))
