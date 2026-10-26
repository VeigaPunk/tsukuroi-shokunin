#!/usr/bin/env python3
"""Integration mistake R42-HERESTRING-TEMPFILE — red at 44766208, green at 78abb8b5.

The first fix (here-strings) writes a >64 KiB here-string to a temp file; on a full $TMPDIR the
redirection fails and `if grep -q ... <<<` takes the else branch: HEALTHY, exit 0. The tip replaces it
with an awk full-consumer on a pipe.

Same command in both legs: the census blob, the counter's own frozen P1 fixture (1 MiB error-first
`pacman -Qkk` sample), TMPDIR on a full 1 MiB tmpfs inside a private mount namespace, plus a
writable-TMPDIR control leg at each revision.

Usage: i1_enospc.py <census.sh> <label>   -> writes receipts/i1-enospc-<label>.txt, exit 0 iff the
                                          full-TMPDIR leg still says BLOCKED with exit 2.
"""
import importlib.util
import os
import subprocess
import sys

S = '/fast/scratch/hyaku/tsukuroi-r42/MistakesFixFail'
LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
COUNTER = f'{LANE}/tools/score-size-invariance-r42.py'


def load_counter():
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location('c1counter', COUNTER)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def leg(census, env, tmpdir, full):
    if full:
        script = ('mount -t tmpfs -o size=1024k tsk "$1" && '
                  'dd if=/dev/zero of="$1/filler" bs=1k count=1024 2>/dev/null; '
                  'df -k "$1" | tail -1; exec bash "$2"')
    else:
        script = 'df -k "$1" | tail -1; exec bash "$2"'
    e = dict(env)
    e['TMPDIR'] = tmpdir
    p = subprocess.run(['unshare', '-rm', 'bash', '-c', script, '_', tmpdir, census],
                       env=e, capture_output=True, timeout=600, cwd=os.path.dirname(census))
    out = p.stdout.decode(errors='replace').splitlines()
    err = p.stderr.decode(errors='replace')
    pkg = [ln for ln in out if ln.startswith('PLANE packages:')]
    tot = [ln for ln in out if ln.startswith('TSUKUROI_CENSUS:')]
    df = [ln for ln in out if 'tmpfs' in ln or ln.split()[:1] == ['Filesystem']]
    return p.returncode, (pkg[0] if pkg else ''), (tot[0] if tot else ''), err, df


def main():
    census, label = sys.argv[1], sys.argv[2]
    c = load_counter()
    base_src = subprocess.run(['git', '-C', LANE, 'show', f'{c.BASE}:{c.CENSUS}'],
                              capture_output=True, check=True).stdout.decode()
    dispatcher, fx_default = c.extract_builder(base_src)
    rig_root = os.path.join(S, 'tmp', f'rig-{label}')
    os.makedirs(rig_root, exist_ok=True)
    rig = c.Rig(os.path.join(rig_root, 'rig'), dispatcher, fx_default)
    files, _ = c.case_files('P1', True)               # error first, then 1 MiB of neutral padding
    fx = rig.fixture(files)
    env = c.env_for(fx, rig.bindir)
    sample = sum(len(v) for v in files.values())

    full = os.path.join(rig_root, 'tmp-full')
    rw = os.path.join(rig_root, 'tmp-rw')
    os.makedirs(full, exist_ok=True)
    os.makedirs(rw, exist_ok=True)
    lines = [f'census        : {census}',
             f'fixture       : {fx}',
             f'sample bytes  : {sample} (qkk.out error-first, > 64 KiB)']
    rc_full, pkg_full, tot_full, err_full, df_full = leg(census, env, full, True)
    rc_rw, pkg_rw, tot_rw, err_rw, df_rw = leg(census, env, rw, False)
    lines += [f'full TMPDIR   : df {" ".join(df_full)}',
              f'  exit        : {rc_full}',
              f'  packages    : {pkg_full[:220]}',
              f'  census      : {tot_full[:160]}',
              f'  stderr      : {err_full.strip()[-300:] or "(empty)"}',
              f'writable TMPDIR: exit {rc_rw}',
              f'  packages    : {pkg_rw[:220]}',
              f'  census      : {tot_rw[:160]}']
    ok = rc_full == 2 and pkg_full.startswith('PLANE packages: BLOCKED') and \
        pkg_full == pkg_rw and rc_rw == 2
    lines.append('RESULT        : ' + ('PASS (green) — TMPDIR-independent' if ok else
                                       'FAIL (red) — the full temp dir changes the reading'))
    text = '\n'.join(lines) + '\n'
    open(f'{S}/receipts/i1-enospc-{label}.txt', 'w').write(text)
    print(text)
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
