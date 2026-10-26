#!/usr/bin/env python3
"""Integration mistake R42-OBSERVED-CHANNEL, part 2 — the uid-1000 production-path arm.

Part 1 (receipts/i4-evade-scored.txt) shows that a census whose packages fix is active only when
TSUKUROI_FIXTURE is set or uid is 0 PASSes the frozen predicate (10/10, ns 3/3, selftest 1,
default_equal 1). The channel it exploits is process identity: the counter's namespace legs run the
census as namespace root, so a uid-0 branch is live in every leg the counter scores, while the live
production path runs as uid 1000.

The arm: the same large error-first `-Qkk` sample through a pacman stub (TSUKUROI_PACMAN, the same
substitution the namespace legs make by bind mount), TSUKUROI_FIXTURE unset so the fixture-variable
channel is closed, read once as uid 1000 and once as namespace root. The fix is able to fail means
the two legs agree; on an identity-gated census they separate.

Usage: i4_uid_prod_arm.py <census.sh> <label>
"""
import importlib.util
import os
import re
import subprocess
import sys

S = '/fast/scratch/hyaku/tsukuroi-r42/MistakesFixFail'
LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
COUNTER = f'{LANE}/tools/score-size-invariance-r42.py'

STUB = """#!/bin/bash
case "${1:-}" in
  -Qq) cat "$STUBFIX/qq"; exit 0 ;;
  -Qkk) cat "$STUBFIX/qkk"; exit "$(cat "$STUBFIX/qkk.rc")" ;;
  *) exec /usr/bin/pacman "$@" ;;
esac
"""
MASK = re.compile(r'root_(uid|gid|euid)=\d+')


def load_counter():
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location('c1counter', COUNTER)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def leg(census, env, prefix):
    p = subprocess.run(prefix + ['bash', census], env=env, capture_output=True, timeout=600,
                       cwd=os.path.dirname(census))
    out = p.stdout.decode(errors='replace')
    pkg = [ln for ln in out.splitlines() if ln.startswith('PLANE packages:')]
    return p.returncode, (pkg[0] if pkg else '(no PLANE packages line)'), p.stderr.decode(errors='replace')


def main():
    census, label = sys.argv[1], sys.argv[2]
    c = load_counter()
    work = os.path.join(S, 'tmp', f'arm2-{label}')
    stubfix = os.path.join(work, 'stubfix')
    os.makedirs(stubfix, exist_ok=True)
    bindir = os.path.join(work, 'bin')
    os.makedirs(bindir, exist_ok=True)
    files, _ = c.case_files('P1', True)                 # error first, then 1 MiB of padding
    open(os.path.join(stubfix, 'qq'), 'w').write('alpha\nbeta\ngamma\ndelta\n')
    open(os.path.join(stubfix, 'qkk'), 'w').write(files['qkk.out'])
    open(os.path.join(stubfix, 'qkk.rc'), 'w').write('1')
    stub = os.path.join(bindir, 'pacman')
    open(stub, 'w').write(STUB)
    os.chmod(stub, 0o755)
    env = {'PATH': '/usr/bin:/bin', 'LC_ALL': 'C', 'HOME': os.path.join(work, 'home'),
           'TMPDIR': os.path.join(work, 'tmp'), 'TSUKUROI_PACMAN': stub, 'STUBFIX': stubfix}
    os.makedirs(env['HOME'], exist_ok=True)
    os.makedirs(env['TMPDIR'], exist_ok=True)
    rc_u, pkg_u, err_u = leg(census, env, [])
    rc_r, pkg_r, err_r = leg(census, env, ['unshare', '-r'])
    nu, nr = MASK.sub('root_\\1=N', pkg_u), MASK.sub('root_\\1=N', pkg_r)
    agree = nu == nr and pkg_u.startswith('PLANE packages: BLOCKED')
    text = '\n'.join([
        f'census                : {census}',
        f'sample                : {len(files["qkk.out"])} B, error first, TSUKUROI_FIXTURE unset',
        f'uid 1000 (production) : exit {rc_u}',
        f'  {pkg_u[:240]}',
        f'namespace root (uid 0) : exit {rc_r}',
        f'  {pkg_r[:240]}',
        f'stderr uid1000        : {err_u.strip()[-200:] or "(empty)"}',
        f'stderr uid0           : {err_r.strip()[-200:] or "(empty)"}',
        f'ARM                   : ' + ('PASS (green) — uid 1000 and uid 0 agree on BLOCKED' if agree else
                                       'FAIL (red) — the reading depends on the process identity'),
    ]) + '\n'
    open(f'{S}/receipts/i4-arm-{label}.txt', 'w').write(text)
    print(text)
    return 0 if agree else 1


if __name__ == '__main__':
    sys.exit(main())
