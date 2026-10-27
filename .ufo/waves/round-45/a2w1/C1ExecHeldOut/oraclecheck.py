#!/usr/bin/env python3
"""Oracle validation: the BASE statement run on the FULL output must equal the oracle
(BASE on the first line alone) whenever the output fits the 64 KiB pipe buffer; past it the
BASE statement must die with 141. That shows the oracle is exactly "base reads the first
line", not a convenient artefact, and that the IMPL reads the same value."""
import importlib.util
import os
import shutil
import subprocess
import sys

ROOT = '/fast/scratch/hyaku/tsukuroi-r45/C1ExecHeldOut'
spec = importlib.util.spec_from_file_location('h', os.path.join(ROOT, 'harness.py'))
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)

DRIVER = r'''#!/usr/bin/env bash
set -u
IN=$1; OUT=$2
for f in "$IN"/*.dat; do
  id=${f##*/}; id=${id%.dat}
  set +e
  ( set -euo pipefail
    CAP_OUT=$(cat -- "$f"; printf '\001'); CAP_OUT=${CAP_OUT%$'\001'}
    @@BASE@@
    printf '%s' "$@@VAR@@" > "$OUT/$id.bfull"
  ) 2>"$OUT/$id.bfull.err"; printf '%s\n' "$?" > "$OUT/$id.bfull.rc"
  ( set -euo pipefail
    CAP_OUT=$(cat -- "$IN/$id.first"; printf '\001'); CAP_OUT=${CAP_OUT%$'\001'}
    @@BASE@@
    printf '%s' "$@@VAR@@" > "$OUT/$id.b"
  ) 2>"$OUT/$id.b.err"; printf '%s\n' "$?" > "$OUT/$id.b.rc"
  ( set -euo pipefail
    CAP_OUT=$(cat -- "$f"; printf '\001'); CAP_OUT=${CAP_OUT%$'\001'}
    @@IMPL@@
    printf '%s' "$@@VAR@@" > "$OUT/$id.i"
  ) 2>"$OUT/$id.i.err"; printf '%s\n' "$?" > "$OUT/$id.i.rc"
done
'''


def main():
    base_lines = h.extract(h.git_show(h.BASE), h.ORD_BASE)
    impl_lines = h.extract(h.git_show(h.IMPL), h.ORD_IMPL)
    tmp = os.path.join(ROOT, 'tmp')
    bad = 0
    for sid in ('S1', 'S2', 'S3', 'S4', 'S5'):
        body = (DRIVER.replace('@@BASE@@', base_lines[sid])
                .replace('@@IMPL@@', impl_lines[sid])
                .replace('@@VAR@@', h.VAR[sid]))
        drv = os.path.join(ROOT, 'drv_oracle_%s.sh' % sid)
        open(drv, 'w', encoding='utf-8', errors='surrogateescape').write(body)
        os.chmod(drv, 0o755)
        for loc in h.LOCALES:
            outdir = os.path.join(ROOT, 'oracle', sid, loc.replace('.', '_'))
            if os.path.isdir(outdir):
                shutil.rmtree(outdir)
            os.makedirs(outdir)
            rc, so, se = h.run_driver(drv, os.path.join(ROOT, 'corpus', sid), outdir, loc, tmp)
            if rc != 0:
                raise SystemExit('driver rc=%d %s' % (rc, se[-300:]))
            cases = sorted(f[:-4] for f in os.listdir(os.path.join(ROOT, 'corpus', sid))
                           if f.endswith('.dat'))
            small = large = small_mism = large_non141 = large_mism = impl_mism = 0
            for c in cases:
                data = open(os.path.join(ROOT, 'corpus', sid, c + '.dat'), 'rb').read()
                bf = h.readval(os.path.join(outdir, c + '.bfull'))
                bfrc = int(h.readval(os.path.join(outdir, c + '.bfull.rc')).strip())
                b = h.readval(os.path.join(outdir, c + '.b'))
                brc = int(h.readval(os.path.join(outdir, c + '.b.rc')).strip())
                i = h.readval(os.path.join(outdir, c + '.i'))
                irc = int(h.readval(os.path.join(outdir, c + '.i.rc')).strip())
                if irc != 0 or i is None or brc != 0 or i != b:
                    impl_mism += 1
                if len(data) < 60000:
                    small += 1
                    if bfrc != 0 or bf != b:
                        small_mism += 1
                        print('  SMALL-DIFF %s %s rc=%d bfull=%s b=%s'
                              % (sid, c, bfrc, (bf or b'').hex(), (b or b'').hex()))
                else:
                    large += 1
                    if bfrc != 141:
                        large_non141 += 1
                    if irc != 0 or bf is not None or i != b:
                        large_mism += 1
            print('%s %-8s small=%d small_mismatch=%d large=%d large_rc!=141=%d impl_mismatch=%d'
                  % (sid, loc, small, small_mism, large, large_non141, impl_mism))
            bad += small_mism + impl_mism
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
