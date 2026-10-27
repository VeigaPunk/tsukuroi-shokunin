#!/usr/bin/env python3
"""Run both capture modes (raw guard-byte bytes / production command substitution) for all
sites and locales in parallel, then compare IMPL vs the BASE-first-line oracle."""
import importlib.util
import json
import os
import shutil
import subprocess
import sys

ROOT = '/fast/scratch/hyaku/tsukuroi-r45/C1ExecHeldOut'
spec = importlib.util.spec_from_file_location('h', os.path.join(ROOT, 'harness.py'))
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)

CENSUS_STMT = {}


def tasks(base_lines, impl_lines):
    out = []
    for sid in h.SITE_ORDER:
        for loc in h.LOCALES:
            for mode in ('raw', 'prod'):
                tag = ('raw_' if mode == 'raw' else 'prod_') + loc.replace('.', '_')
                outdir = os.path.join(ROOT, 'out', sid, tag)
                if os.path.isdir(outdir):
                    shutil.rmtree(outdir)
                os.makedirs(outdir)
                drv = os.path.join(ROOT, 'drv_%s_%s.sh' % (sid, tag))
                h.write_driver(drv, sid, impl_lines[sid], h.VAR[sid], base_lines[sid],
                               capture=('guard' if mode == 'raw' else 'prod'))
                out.append((sid, loc, mode, drv, outdir))
    return out


def main():
    base_lines = h.extract(h.git_show(h.BASE), h.ORD_BASE)
    impl_lines = h.extract(h.git_show(h.IMPL), h.ORD_IMPL)
    tmp = os.path.join(ROOT, 'tmp')
    os.makedirs(tmp, exist_ok=True)
    jobs = tasks(base_lines, impl_lines)
    env0 = {k: v for k, v in os.environ.items() if not k.startswith(('TSUKUROI_', 'UFO_'))}
    procs = []
    for sid, loc, mode, drv, outdir in jobs:
        env = dict(env0)
        env['LC_ALL'] = loc
        env['TMPDIR'] = tmp
        p = subprocess.Popen(['bash', drv, os.path.join(ROOT, 'corpus', sid), outdir],
                             stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, env=env, start_new_session=True)
        procs.append((p, sid, loc, mode, outdir))
    running = list(procs)
    done = []
    while running:
        nxt = []
        for p, sid, loc, mode, outdir in running:
            rc = p.poll()
            if rc is None:
                nxt.append((p, sid, loc, mode, outdir))
            else:
                so, se = p.communicate()
                if rc != 0:
                    raise SystemExit('driver %s/%s/%s rc=%d %s' % (sid, loc, mode, rc, se[-500:]))
                done.append((sid, loc, mode, outdir))
        running = nxt
        if running:
            import time
            time.sleep(0.5)

    summary = {}
    for sid, loc, mode, outdir in done:
        cases = sorted(f[:-4] for f in os.listdir(os.path.join(ROOT, 'corpus', sid))
                       if f.endswith('.dat'))
        mism, basefail = [], []
        for name in cases:
            raw = open(os.path.join(ROOT, 'corpus', sid, name + '.dat'), 'rb').read()
            impl = h.readval(os.path.join(outdir, name + '.impl'))
            base = h.readval(os.path.join(outdir, name + '.base'))
            ir = int(h.readval(os.path.join(outdir, name + '.impl.rc')).strip())
            br = int(h.readval(os.path.join(outdir, name + '.base.rc')).strip())
            ierr = h.readval(os.path.join(outdir, name + '.impl.err')) or b''
            berr = h.readval(os.path.join(outdir, name + '.base.err')) or b''
            rec = {'case': name, 'impl_rc': ir, 'base_rc': br,
                   'impl': h.hexs(impl) if impl is not None else None,
                   'base': h.hexs(base) if base is not None else None,
                   'raw_len': len(raw),
                   'captured': h.hexs(raw if mode == 'raw' else raw.rstrip(b'\n'))[:2000],
                   'impl_err': ierr.decode('utf-8', 'backslashreplace')[:300],
                   'base_err': berr.decode('utf-8', 'backslashreplace')[:300]}
            if br != 0 or base is None:
                basefail.append(rec)
            if ir != 0 or impl is None or base is None or impl != base:
                rec['impl_class'] = h.classify(sid, impl)
                rec['base_class'] = h.classify(sid, base)
                mism.append(rec)
        key = '%s/%s/%s' % (sid, loc, mode)
        summary[key] = {'n': len(cases), 'mismatches': mism, 'oracle_failures': basefail}
        print('%-22s cases=%3d mismatches=%d oracle_failures=%d'
              % (key, len(cases), len(mism), len(basefail)))
        for rec in mism[:6]:
            print('   MISMATCH %s implrc=%d baserc=%d impl=%s base=%s'
                  % (rec['case'], rec['impl_rc'], rec['base_rc'], rec['impl'], rec['base']))
            print('      impl_class=%s base_class=%s' % (rec.get('impl_class'), rec.get('base_class')))
        for rec in basefail[:6]:
            print('   ORACLE-FAIL %s baserc=%d err=%s' % (rec['case'], rec['base_rc'], rec['base_err']))

    with open(os.path.join(ROOT, 'results_all.json'), 'w') as f:
        json.dump(summary, f, indent=1)
    total = sum(v['n'] for v in summary.values())
    bad = sum(len(v['mismatches']) for v in summary.values())
    of = sum(len(v['oracle_failures']) for v in summary.values())
    print('TOTAL case-runs=%d mismatches=%d oracle_failures=%d' % (total, bad, of))
    return 1 if (bad or of) else 0


if __name__ == '__main__':
    sys.exit(main())
