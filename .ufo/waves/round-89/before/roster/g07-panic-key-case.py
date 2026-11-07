#!/usr/bin/env python3
"""Round-87 CriticClaims forger g07-panic-key-case: R1/R6 clause that key matching (also for hash_mismatch_panic) is case-insensitive: this forger
matches the panic key case-sensitively.

A 22/22 read here means the bent clause is NOT exercised by any of the 22 battery families.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import run

run({'panic_key_case': True})
