#!/usr/bin/env python3
"""W1 row R42-C1-SCRATCH-FALLBACK-TMP — can a counter invocation without --scratch be refused?

Fix under test (w1/MistakesSweep.md row 7): `parent = a.scratch or os.environ.get('TMPDIR') or None`
becomes a requirement — with neither `--scratch` nor `TMPDIR` set the counter exits 2 (usage) and
creates nothing, instead of passing `dir=None` to `tempfile.mkdtemp` (which is `/tmp`).

The check is the counter invocation itself: this harness stubs `tempfile.mkdtemp` so that the
question "what dir would the counter build in?" is answered without building anything under /tmp.
Red = mkdtemp is reached with dir=None (the fallback is live); green = the counter exits 2 first.

Usage: env -u TMPDIR w1r7_scratch_guard.py <counter.py>
"""
import importlib.util
import os
import sys
import tempfile

LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
LV = '78abb8b5cdc9da511b4fc523e661517a68dd33d3'


def main():
    path = sys.argv[1]
    calls = []

    def fake_mkdtemp(prefix='', dir=None):
        calls.append(dir if dir is not None else tempfile.gettempdir())
        raise SystemExit(77)          # never create the directory

    real = tempfile.mkdtemp
    tempfile.mkdtemp = fake_mkdtemp
    sys.dont_write_bytecode = True
    sys.argv = [path, '--revision', LV, '--lane', LANE]
    spec = importlib.util.spec_from_file_location('c1counter', path)
    m = importlib.util.module_from_spec(spec)
    rc = 'module-import-failed'
    try:
        spec.loader.exec_module(m)
        rc = m.main()
    except SystemExit as e:
        rc = e.code
    finally:
        tempfile.mkdtemp = real
    print(f'counter        : {path}')
    print(f'TMPDIR         : {"unset" if "TMPDIR" not in os.environ else os.environ["TMPDIR"]}')
    print(f'exit           : {rc}')
    print(f'mkdtemp dirs   : {calls}')
    if calls:
        print('GUARD          : absent (red) — the counter would build in ' + ', '.join(calls))
        return 1
    print('GUARD          : present (green) — refused before any directory was created')
    return 0 if rc == 2 else 1


if __name__ == '__main__':
    sys.exit(main())
