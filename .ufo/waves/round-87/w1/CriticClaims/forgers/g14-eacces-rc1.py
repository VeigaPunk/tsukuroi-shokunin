#!/usr/bin/env python3
"""Round-87 CriticClaims forger g14-eacces-rc1: R7 clause 'An unreadable --conf -> CANNOT-EVALUATE rc 2': this forger only handles ENOENT; any
other OSError (EACCES/EISDIR) exits rc 1 DEGRADED.

A 22/22 read here means the bent clause is NOT exercised by any of the 22 battery families.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import run

run({'eacces_rc1': True})
