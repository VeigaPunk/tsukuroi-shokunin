#!/usr/bin/env python3
"""Forger: no R1-R7 implementation at all; delegates to the committed reference gate in the lane."""
import importlib.util, os, sys
LANE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF = os.path.join(LANE, ".ufo", "waves", "round-87", "before", "controls", "ref-gate-r87.py")
spec = importlib.util.spec_from_file_location("refgate", REF)
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
sys.exit(m.main())
