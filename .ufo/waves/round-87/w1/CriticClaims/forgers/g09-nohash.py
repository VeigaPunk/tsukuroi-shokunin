#!/usr/bin/env python3
"""Round-87 CriticClaims forger g09-nohash: R5 BLAKE2b-512 comparison entirely: this forger checks format, resolution and existence only and
assumes OK for every existing file.

A 22/22 read here means the bent clause is NOT exercised by any of the 22 battery families.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import run

run({'nohash': True})
