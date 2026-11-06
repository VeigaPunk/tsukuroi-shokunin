#!/usr/bin/env python3
"""Round-87 CriticClaims forger g15-no-cr-strip: R1 clause 'trailing spaces/tabs/CR removed': this forger never strips a trailing CR.

A 22/22 read here means the bent clause is NOT exercised by any of the 22 battery families.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import run

run({'no_cr_strip': True})
