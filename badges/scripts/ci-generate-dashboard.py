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
gap = 5  # space between cells
cell_w, cell_h = 25, 25
header_h = 100
row_label_w = 120
svg_w = row_label_w + len(compilers) * cell_w + 80
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

# Column headers (rotated -45° for readability, aligned with gap)
for j, comp in enumerate(compilers):
    x = row_label_w + j * (cell_w + gap) + cell_w // 2
    y = header_h - 10
    svg.append(
        f'<text x="{x}" y="{y}" transform="rotate(-45,{x},{y})" font-size="12">{comp}</text>'
    )

# Row headers (align OS labels right before the grid)
for i, os in enumerate(oses):
    y = header_h + i * (cell_h + gap) + cell_h // 2 + 5
    svg.append(
        f'<text x="{row_label_w - gap}" y="{y}" font-size="14" text-anchor="end">{os}</text>'
    )

# Grid cells
for i, os in enumerate(oses):
    for j, comp in enumerate(compilers):
        status = matrix.get((os, comp), "skipped")
        color, symbol = status_color_symbol(status)
        x = row_label_w + j * (cell_w + gap)
        y = header_h + i * (cell_h + gap)
        svg.append(
            f'<rect x="{x}" y="{y}" width="{cell_w}" height="{cell_h}" '
            f'rx="6" ry="6" fill="{color}" fill-opacity="0.3" stroke="black"/>'
        )
        svg.append(
            f'<text x="{x + cell_w/2}" y="{y + cell_h/2 + 5}" '
            f'text-anchor="middle" font-size="18">{symbol}</text>'
        )

svg.append("</svg>")

# Write output
Path("dashboard.svg").write_text("\n".join(svg))
print("✅ Generated dashboard.svg")
