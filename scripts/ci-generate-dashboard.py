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
header_h = 90
row_label_w = 110
svg_w = row_label_w + len(compilers) * cell_w + 80
svg_h = header_h + len(oses) * cell_h + 20

def status_color_symbol(status):
    if status == "success":
        return "green", "✔"
    elif status == "failure":
        return "red", "✘"
    else:  # default: skipped or missing
        return "gray", "○"

def generate_svg(theme):
    """
    theme = "light" or "dark"
    """
    if theme == "light":
        text_color = "black"
        stroke_color = "black"
        bg_color = "white"
    else:
        text_color = "white"
        stroke_color = "white"
        bg_color = "#1e1e1e"

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{svg_w}" height="{svg_h}" font-family="monospace">'
    ]

    # Background
    svg.append(f'<rect x="0" y="0" width="100%" height="100%" fill="none" />')

    # Global top label
    svg.append(
        f'<text x="{row_label_w/2}" y="{header_h - 10}" '
        f'font-size="14" text-anchor="middle" font-weight="700" fill="{text_color}">Compiler/OS</text>'
    )

    # Column headers
    for j, comp in enumerate(compilers):
        x = row_label_w + j * (cell_w + gap) + cell_w // 2
        y = header_h - 10
        svg.append(
            f'<text x="{x}" y="{y}" transform="rotate(-45,{x},{y})" font-size="14" font-weight="700" fill="{text_color}">{comp}</text>'
        )

    # Row headers
    for i, os in enumerate(oses):
        y = header_h + i * (cell_h + gap) + cell_h // 2 + 10
        svg.append(
            f'<text x="{row_label_w - gap - 5}" y="{y}" font-size="14" text-anchor="end" font-weight="700" fill="{text_color}">{os}</text>'
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
                f'rx="5" ry="5" fill="{color}" fill-opacity="0.5" stroke="{stroke_color}"/>'
            )
            svg.append(
                f'<text x="{x + cell_w/2}" y="{y + cell_h/2 + 5}" '
                f'text-anchor="middle" font-size="21" fill="{text_color}">{symbol}</text>'
            )

    svg.append("</svg>")
    return "\n".join(svg)

# Write both versions
Path("dashboard-light.svg").write_text(generate_svg("light"))
Path("dashboard-dark.svg").write_text(generate_svg("dark"))
print("Generated dashboard-light.svg and dashboard-dark.svg")
