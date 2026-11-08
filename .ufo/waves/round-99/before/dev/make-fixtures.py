#!/usr/bin/env python3
"""Build the round-99 C2 capture fixtures from the r99 checker's own build_fixture (so the fixture
bytes are the instrument's, not a hand-written table). Usage: make-fixtures.py <outdir>"""
import importlib.util, os, sys

LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
spec = importlib.util.spec_from_file_location(
    "c99", os.path.join(LANE, "tools", "check-registry-content-r99.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
out = os.path.abspath(sys.argv[1])
for name, doctor in (("clean", None), ("hybrid", ("HYBRID", None, None)),
                     ("restated", ("RESTATED", None, None)), ("gap", ("GAP", None, None))):
    d = os.path.join(out, name)
    mod.build_fixture(d, doctor)
    print("built", d)
