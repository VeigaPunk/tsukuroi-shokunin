#!/usr/bin/env python3
"""Round-87 CriticClaims base gate: R1-R7 as written, no deviation.

POSITIVE CONTROL: if this reads below 22/22 the forger body is wrong and every other read is
confounded. Written from the battery docstring, never from tools/check-limine-pins.py.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib import run

run({})
