#!/usr/bin/env python3
"""Round-87 CriticClaims forger g06-any-empty-root: R4 clause 'Any other resource ... -> LP-UNRESOLVED': this forger resolves ANY resource with an
empty root to the ESP (resource name never checked).

A 22/22 read here means the bent clause is NOT exercised by any of the 22 battery families.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import run

run({'any_empty_root': True})
