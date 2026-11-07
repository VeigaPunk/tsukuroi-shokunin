#!/usr/bin/env python3
"""Round-87 CriticClaims forger g02-no-paren: R2 clause 'a ( then, later, ):/': this forger accepts any value containing ':/' and '#'.

A 22/22 read here means the bent clause is NOT exercised by any of the 22 battery families.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import run

run({'no_paren': True})
