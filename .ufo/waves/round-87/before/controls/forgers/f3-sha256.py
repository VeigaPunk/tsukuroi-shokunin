"""Forger: the reference rule set with SHA-256 in place of BLAKE2b (names a wrong hash family)."""
import hashlib, os, runpy, sys
hashlib.blake2b = hashlib.sha512  # 128 hex chars like BLAKE2b-512, wrong function
sys.argv[0] = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ref-gate-r87.py")
runpy.run_path(sys.argv[0], run_name="__main__")
