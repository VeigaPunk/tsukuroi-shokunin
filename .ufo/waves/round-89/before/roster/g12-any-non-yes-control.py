#!/usr/bin/env python3
"""Round-87 CriticClaims forger g12-any-non-yes-control: CONTROL (expected under 22): R6 'only no prompts'. Treats any value but yes as prompt.

A 22/22 read here means the bent clause is NOT exercised by any of the 22 battery families.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import run

run({'panic_any_non_yes': True})
