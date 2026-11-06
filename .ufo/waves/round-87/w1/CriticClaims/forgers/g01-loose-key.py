#!/usr/bin/env python3
"""Round-87 CriticClaims forger g01-loose-key: R1 clause 'followed directly by :' and key charset [A-Za-z_]: this forger accepts blanks
before ':' and digits/hyphens inside the key.

A 22/22 read here means the bent clause is NOT exercised by any of the 22 battery families.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import run

run({'loose_key': True})
