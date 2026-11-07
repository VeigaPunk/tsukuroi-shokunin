#!/usr/bin/env python3
"""Round-87 CriticClaims forger g04-hashformat-optional-panic: R6 clause 'for LP-MISMATCH and LP-HASH-FORMAT: key wallpaper/term_font -> skip': this forger
maps every LP-HASH-FORMAT to panic, optional keys included.

A 22/22 read here means the bent clause is NOT exercised by any of the 22 battery families.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import run

run({'hashfmt_always_panic': True})
