#!/usr/bin/env python3
"""Round-87 CriticClaims forger g13-constant-panic-control: CONTROL (expected under 22): R6 consequence table flattened to 'mismatch always panics'.

A 22/22 read here means the bent clause is NOT exercised by any of the 22 battery families.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import run

run({'constant_panic': True})
