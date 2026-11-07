#!/usr/bin/env python3
"""Round-87 CriticClaims forger g10-raw-panic-scan: R6 clause 'the FIRST hash_mismatch_panic KEY LINE in the whole file (R1 rules)': this forger
regex-scans the raw text, so comments and values count.

A 22/22 read here means the bent clause is NOT exercised by any of the 22 battery families.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import run

run({'raw_panic_scan': True})
