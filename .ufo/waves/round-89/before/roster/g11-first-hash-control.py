#!/usr/bin/env python3
"""Round-87 CriticClaims forger g11-first-hash-control: CONTROL (expected under 22): R2 'hash is the text after the LAST #'. Bends to the first '#'.

A 22/22 read here means the bent clause is NOT exercised by any of the 22 battery families.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import run

run({'first_hash': True})
