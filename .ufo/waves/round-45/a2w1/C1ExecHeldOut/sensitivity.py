#!/usr/bin/env python3
"""Sensitivity: prove the harness detects two known-imperfect readers (the K5-style missing
trailing strip, and a shortest-suffix first-line split). A harness that finds 0 mismatches
must still flag these."""
import importlib.util
import os
import shutil
import subprocess
import sys

ROOT = '/fast/scratch/hyaku/tsukuroi-r45/C1ExecHeldOut'
spec = importlib.util.spec_from_file_location('h', os.path.join(ROOT, 'harness.py'))
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)

MUTANTS = {
    'M1-no-trailing-strip': "state=${CAP_OUT%%$'\\n'*}; state=${state//$'\\r'/}",
    'M2-shortest-suffix': "state=${CAP_OUT%$'\\n'*}; state=${state//$'\\r'/}; "
                          "state=${state%\"${state##*[![:space:]]}\"}",
}


def main():
    base = h.extract(h.git_show(h.BASE), h.ORD_BASE)['S1']
    tmp = os.path.join(ROOT, 'tmp')
    corpus = os.path.join(ROOT, 'corpus', 'S1')
    for name, stmt in MUTANTS.items():
        for loc in h.LOCALES:
            outdir = os.path.join(ROOT, 'sens', name, loc.replace('.', '_'))
            if os.path.isdir(outdir):
                shutil.rmtree(outdir)
            os.makedirs(outdir)
            drv = os.path.join(ROOT, 'drv_sens_%s_%s.sh' % (name, loc.replace('.', '_')))
            h.write_driver(drv, 'S1', stmt, 'state', base, capture='guard')
            rc, so, se = h.run_driver(drv, corpus, outdir, loc, tmp)
            if rc != 0:
                raise SystemExit('driver rc=%d %s' % (rc, se[-300:]))
            cases = sorted(f[:-4] for f in os.listdir(corpus) if f.endswith('.dat'))
            bad = []
            for c in cases:
                impl = h.readval(os.path.join(outdir, c + '.impl'))
                basev = h.readval(os.path.join(outdir, c + '.base'))
                if impl is None or basev is None or impl != basev:
                    bad.append((c, impl.hex() if impl else None, basev.hex() if basev else None))
            print('%-22s %-8s cases=%d mismatches=%d  e.g. %s' % (name, loc, len(cases), len(bad), bad[:3]))
            if not bad:
                return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
