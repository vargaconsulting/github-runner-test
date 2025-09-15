#!/usr/bin/env python3
import json
import glob
from pathlib import Path

# Collect all status JSON files
status_files = glob.glob("badge-status/status-*.json")

matrix = {}
oses, compilers = set(), set()

for f in status_files:
    with open(f) as fh:
        data = json.load(fh)
        os = data["os"]
        compiler = data["compiler"]
        status = data["status"]
        matrix[(os, compiler)] = status
        oses.add(os)
        compilers.add(compiler)

# Sort for consistent layout
oses = sorted(oses)
compilers = sorted(compilers)

# SVG layout parameters
cell_w, cell_h = 60, 40
header_h = 100
row_label_w = 150
svg_w = row_label_w + len(compilers) * cell_w + 50
svg_h = header_h + len(oses) * cell_h + 50

def status_color_symbol(status):
    if status == "success":
        return "green", "✔"
    elif status == "failure":
        return "red", "✘"
    else:  # default: skipped or missing
        return "gray", "○"

# Start SVG
svg = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{svg_w}" height="{svg_h}" font-family="monospace">'
]

# Column headers (rotated -45° for readability)
for j, comp in enumerate(compilers):
    x = row_label_w + j * cell_w + cell_w // 2
    y = header_h - 30
    svg.append(
        f'<text x="{x}" y="{y}" transform="rotate(-45,{x},{y})" font-size="12">{comp}</text>'
    )

# Row headers
for i, os in enumerate(oses):
    y = header_h + i * cell_h + cell_h // 2 + 5
    svg.append(f'<text x="10" y="{y}" font-size="14">{os}</text>')

# Grid cells
for i, os in enumerate(oses):
    for j, comp in enumerate(compilers):
        status = matrix.get((os, comp), "skipped")
        color, symbol = status_color_symbol(status)
        x = row_label_w + j * cell_w
        y = header_h + i * cell_h
        svg.append(
            f'<rect x="{x}" y="{y}" width="{cell_w}" height="{cell_h}" '
            f'fill="{color}" fill-opacity="0.3" stroke="black"/>'
        )
        svg.append(
            f'<text x="{x + cell_w/2}" y="{y + cell_h/2 + 5}" '
            f'text-anchor="middle" font-size="18">{symbol}</text>'
        )

svg.append("</svg>")

# Write output
Path("dashboard.svg").write_text("\n".join(svg))
print("✅ Generated dashboard.svg")
