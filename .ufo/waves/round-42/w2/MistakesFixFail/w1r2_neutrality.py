#!/usr/bin/env python3
"""W1 row R42-C1-P6-NOT-NEUTRAL — the counter's padding-neutrality self-check.

Fix under test (w1/MistakesSweep.md row 2): "feed qkk_pad/err_pad output to the census's own rules
and require no [verdict-bearing] match", so a twin whose padding the census does read cannot be
called verdict-neutral.

The rules are the census's own, copied from tools/tsukuroi-census.sh at the lane tip (78abb8b5),
probe_packages:
  :698  awk '/^error:/ { ... }'                                    error test (first error decides)
  :705  sed -nE 's/^[^:]+: [0-9]+ total files, ([0-9]+) altered files?.*/\\1/p'  drift sum
  :707  grep -c '^backup file: '                                   backup count
  :708-709 grep -cE '\\(failed to calculate SHA256 checksum\\)|\\(Permission denied\\)'  nonroot count
The aggregated reading of a sample is (error_hit, drift_sum, backup_n, nonroot_n); padding is
verdict-neutral iff adding it leaves that tuple unchanged.

Usage: w1r2_neutrality.py <pad-generator>   (qkk_pad | err_pad)
Prints the tuple for the signal-only sample and for signal+1MiB of padding; exit 0 iff neutral.
"""
import importlib.util
import re
import sys

COUNTER = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/score-size-invariance-r42.py'

ERR = 'error: alpha: /usr/bin/x-aaaaaa (Permission denied)\n'
SUMS = ['alpha: 10 total files, 0 altered files\n', 'beta: 20 total files, 0 altered files\n']

RE_ERROR = re.compile(r'^error:')
RE_DRIFT = re.compile(r'^[^:]+: [0-9]+ total files, ([0-9]+) altered files?.*')
RE_BACKUP = re.compile(r'^backup file: ')
RE_NONROOT = re.compile(r'\(failed to calculate SHA256 checksum\)|\(Permission denied\)')


def reading(lines):
    err = any(RE_ERROR.match(ln) for ln in lines)
    drift = sum(int(m.group(1)) for ln in lines for m in [RE_DRIFT.match(ln)] if m)
    backup = sum(1 for ln in lines if RE_BACKUP.match(ln))
    nonroot = sum(1 for ln in lines if RE_NONROOT.search(ln))
    return {'error_hit': err, 'drift_sum': drift, 'backup_n': backup, 'nonroot_n': nonroot}


def load_counter():
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location('c1counter', COUNTER)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main():
    gen = sys.argv[1]
    c = load_counter()
    pad = c.qkk_pad(c.PAD_BYTES) if gen == 'qkk_pad' else c.err_pad(c.PAD_BYTES)
    small = [ERR] + SUMS
    large = [ERR] + pad + SUMS
    rs, rl = reading(small), reading(large)
    neutral = rs == rl
    n_err = sum(1 for ln in pad if RE_ERROR.match(ln))
    n_drift = sum(1 for ln in pad if RE_DRIFT.match(ln))
    n_backup = sum(1 for ln in pad if RE_BACKUP.match(ln))
    n_nonroot = sum(1 for ln in pad if RE_NONROOT.search(ln))
    any_match = n_err + n_drift + n_backup + n_nonroot
    print(f'generator      : {gen} ({len(pad)} lines, {sum(len(x) for x in pad)} bytes)')
    print(f'rule matches   : error {n_err}, drift {n_drift}, backup {n_backup}, nonroot {n_nonroot}'
          f'  (strict "no rule matches" would be {"RED" if any_match else "green"})')
    print(f'signal only    : {rs}')
    print(f'signal+padding : {rl}')
    print(f'NEUTRAL        : {"yes (green)" if neutral else "NO (red) — padding is read by the census"}')
    return 0 if neutral else 1


if __name__ == '__main__':
    sys.exit(main())
