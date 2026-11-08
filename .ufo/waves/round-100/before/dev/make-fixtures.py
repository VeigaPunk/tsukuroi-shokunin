#!/usr/bin/env python3
"""Build the round-100 C2 fixture trees at a caller-given root, using the frozen r100 checker's
own `build_fixture` (so the fixture bytes are the instrument's, not a hand copy). Usage:
    python3 make-fixtures.py <OUTDIR>
Prints one absolute path per fixture. Used by the L1 and the wave seats to reproduce the same
bytes; the fixture cells are also named in `.ufo/plans/round-100.md`.
"""
import importlib.util
import os
import sys

LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
TOOL = os.path.join(LANE, "tools", "check-registry-content-r100.py")
TAGS = ("SEP-SPACE", "SEP-SEMICOLON", "SEP-AND", "SEP-SLASH", "SEP-PLUS", "UNION",
        "LETTER", "PROSE", "UNION-LIE", "HYBRID", "RESTATED", "GAP")


def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: make-fixtures.py <OUTDIR>")
    out = os.path.abspath(sys.argv[1])
    os.makedirs(out, exist_ok=True)
    spec = importlib.util.spec_from_file_location("check_registry_content_r100", TOOL)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for tag in TAGS:
        case = os.path.join(out, tag)
        module.build_fixture(case, (tag, None, None))
        print(case)


if __name__ == "__main__":
    main()
