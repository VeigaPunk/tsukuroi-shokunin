#!/usr/bin/env python3
"""Round-87 CriticClaims forger g03-format-after-resolve: R3 clause 'checked before resolution': this forger resolves first, then checks the hash format.

A 22/22 read here means the bent clause is NOT exercised by any of the 22 battery families.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import run

run({'format_after_resolve': True})
