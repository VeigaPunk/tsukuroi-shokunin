#!/usr/bin/env python3
"""Round-87 CriticClaims forger g16-drop-global-dtb: R2 pin-key set: this forger omits `global_dtb`, a plausible implementation slip (it is the
only one of the eight keys not ending in _path). The battery's KEY-CASE family draws the third
pin's key uniformly from {kernel_path, image_path, dtb_path, global_dtb}, so this forger passes a
run when no case draws global_dtb: (3/4)^4 = 31.6% per run, 3.2% for three consecutive runs.

A 22/22 read here means the bent clause is NOT exercised by any of the 22 battery families.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import run

run({'drop_keys': ['global_dtb']})
