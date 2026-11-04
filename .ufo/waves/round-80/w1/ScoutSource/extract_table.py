#!/usr/bin/env python3
"""Independent re-derivation of the systemd v262 Restart= exit-cause matrix.

Deliberately does NOT import tools/measure-round80.py. It parses the raw
XML snapshot with a self-contained parser, locates the
"Exit causes and the effect of the Restart= settings" table, and emits the
six cause rows x seven policy cells as booleans.

Usage: extract_table.py <path-to-systemd.service.xml> <out.json>
"""
import json
import re
import sys
import xml.etree.ElementTree as ET

TABLE_TITLE = "Exit causes and the effect of the Restart= settings"


def text_of(el):
    """Flatten an <entry> element to plain text, dropping child tags."""
    if el is None:
        return ""
    parts = []
    for node in el.iter():
        if node.text:
            parts.append(node.text)
        if node.tail:
            parts.append(node.tail)
    return re.sub(r"\s+", " ", "".join(parts)).strip()


def find_restart_table(root):
    """Return (header_entries, body_rows) for the Restart= exit-cause table."""
    for table in root.iter("table"):
        title = table.find("title")
        if title is None:
            continue
        if text_of(title) != TABLE_TITLE:
            continue
        tgroup = table.find("tgroup")
        thead = tgroup.find("thead")
        tbody = tgroup.find("tbody")
        header = []
        for row in thead.findall("row"):
            header.extend(text_of(entry) for entry in row.findall("entry"))
        body = []
        for row in tbody.findall("row"):
            cells = [text_of(entry) for entry in row.findall("entry")]
            body.append(cells)
        return header, body
    raise SystemExit("restart table not found")


def main():
    src, out = sys.argv[1], sys.argv[2]
    raw = open(src, "rb").read()
    root = ET.fromstring(raw)
    header, body = find_restart_table(root)

    # header[0] is the corner label; header[1:] are the seven settings
    settings = header[1:]
    rows = []
    for cells in body:
        cause = cells[0]
        marks = cells[1:]
        if len(marks) != len(settings):
            raise SystemExit(f"row {cause!r}: {len(marks)} marks vs {len(settings)} settings")
        restart = []
        for m in marks:
            if m == "X":
                restart.append(True)
            elif m == "":
                restart.append(False)
            else:
                raise SystemExit(f"row {cause!r}: unexpected cell {m!r}")
        rows.append({"cause": cause, "restart": restart})

    matrix = {
        "source_url": "https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.service.xml",
        "settings": settings,
        "rows": rows,
    }
    with open(out, "w") as fh:
        json.dump(matrix, fh, indent=2)
        fh.write("\n")
    print(json.dumps(matrix, indent=2))
    print(f"rows={len(rows)} cells={len(rows)*len(settings)}")


if __name__ == "__main__":
    main()
