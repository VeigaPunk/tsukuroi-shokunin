#!/usr/bin/env python3
"""Run the existing receipt generator with only scratch/clone policy adaptation.

The target gate and generator files remain unchanged. All scratch is lane-local;
clones share local objects and receive a disabled push URL before use.
Arguments are passed unchanged to tools/run-receipt.py.
"""
import os
import runpy
import subprocess
import sys
import tempfile
from pathlib import Path

lane = Path(__file__).resolve().parents[3]
scratch = Path(os.environ.get('HYAKU_SCRATCH', '/fast/scratch/hyaku')) / 'tsukuroi-r78' / 'L1Receipts'
scratch.mkdir(parents=True, exist_ok=True)
os.environ['TMPDIR'] = str(scratch)
original_mkdtemp = tempfile.mkdtemp
original_run = subprocess.run


def mkdtemp(*args, **kwargs):
    kwargs['dir'] = str(scratch)
    return original_mkdtemp(*args, **kwargs)


def run(argv, *args, **kwargs):
    if kwargs.get('env') is not None:
        kwargs['env'] = dict(kwargs['env'], TMPDIR=str(scratch))
    if isinstance(argv, list) and argv[:2] == ['git', 'clone']:
        argv = [('--shared' if item == '--no-local' else item) for item in argv]
        result = original_run(argv, *args, **kwargs)
        if result.returncode == 0:
            original_run(['git', '-C', argv[-1], 'config', 'remote.origin.pushurl', 'DISABLED'],
                         capture_output=True, env=kwargs.get('env'), check=True)
        return result
    return original_run(argv, *args, **kwargs)


tempfile.mkdtemp = mkdtemp
subprocess.run = run
sys.argv[0] = str(lane / 'tools/run-receipt.py')
try:
    runpy.run_path(sys.argv[0], run_name='__main__')
finally:
    # The generator removes each owned clone/home in its own finally block.
    scratch.rmdir()
