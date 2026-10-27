#!/usr/bin/env python3
"""Round-46 C1 counter (frozen before data): the census `--identity` mode (routed debt D12, open since round 10).

Surface: tools/tsukuroi-census.sh gains `--identity`, which prints ONE machine-readable line naming the bytes the
running bash process is executing, so a non-author re-derives the census revision with one command instead of three
(closeout-r11.md:42-44, :261-262; plans/round-10.plan.md:115-120: "a field the landed harness cannot support prints
`unverifiable`, never a guess").

Frozen line shape (one stdout line, exit 0, nothing on stderr):
  TSUKUROI_CENSUS_IDENTITY: version=<V> sha256=<64 hex|unverifiable> md5=<32 hex|unverifiable>
  bytes=<n|unverifiable> lines=<n|unverifiable> planes=<k1,k2,...> exit_map=0:HEALTHY,1:DEGRADED,2:BLOCKED
  verified=<yes|no>
(single spaces, one line). `lines` counts newline bytes (wc -l). `verified=yes` iff the four digest/size fields are
values; `verified=no` iff all four are `unverifiable`.

Legs, each scored on the census bytes of REV (`git show REV:tools/tsukuroi-census.sh`) extracted under --scratch:
  identity_ok     `bash F --identity` (F a regular file): exit 0, empty stderr, exactly one stdout line matching
                  the frozen shape; sha256/md5/bytes/lines equal the counter's own computation over F's bytes;
                  version equals the file's `VERSION='...'` literal; planes equal the key order of the file's
                  rollup printf (`TSUKUROI_CENSUS: %s (packages=%s ...)`); exit_map frozen; verified=yes.
  tracks_ok       G = F + one appended comment line: `bash G --identity` reports G's own sha256/md5/bytes/lines
                  (all four differ from F's) — kills a constant writer.
  symlink_ok      `bash S --identity`, S a symlink to F: reports F's values, verified=yes.
  unverifiable_ok the script read from stdin (`bash -s -- --identity < F`) in a cwd holding a decoy regular file
                  named `bash` (F's bytes plus a line) and a decoy `tsukuroi-census.sh`; through process
                  substitution (`bash <(cat F) --identity`); and replaced after open (R = `mv -f -- "$R46_DECOY"
                  "$R46_PATH"` + F's bytes, run as `bash R --identity`: its first line renames a decoy over R's own
                  path while bash keeps reading the old inode): all three exit 0 with sha256, md5, bytes and lines
                  all `unverifiable`, verified=no, version/planes/exit_map as in identity_ok — the replaced case
                  kills a path hasher (pre-freeze control K2 passed the counter before this case was added).
  cli_ok          `--identity --selftest` and `--identity --sample 3` exit 2; `--help` exits 0 and its output
                  names `--identity`; `--bogus` exits 2.
  nowrite_ok      the identity runs above leave their cwd and TMPDIR byte-unchanged (no file created).
  selftest_pass   `bash F --selftest` exits 0 and its last line is `TSUKUROI_CENSUS_SELFTEST: PASS (...)`.
  selftest_r46    number of `PASS ` lines whose label carries `(R46-C1)`.

Predicate (same sentence in the declaration and the receipt label):
  PASS iff identity_ok == 1 and tracks_ok == 1 and symlink_ok == 1 and unverifiable_ok == 1 and cli_ok == 1
  and nowrite_ok == 1 and selftest_pass == 1 and selftest_r46 >= 4.

Usage: python3 tools/score-census-identity-r46.py --revision <REV> --scratch <DIR> [--lane <repo>]
--scratch is required (no /tmp fallback); the counter writes only beneath it and removes its own subtree.
Output: one JSON line; exit 0 PASS, 1 FAIL, 2 usage/read error.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile

CENSUS = 'tools/tsukuroi-census.sh'
EXIT_MAP = '0:HEALTHY,1:DEGRADED,2:BLOCKED'
LINE_RE = re.compile(
    r'TSUKUROI_CENSUS_IDENTITY: version=(\S+) sha256=([0-9a-f]{64}|unverifiable) md5=([0-9a-f]{32}|unverifiable) '
    r'bytes=([0-9]+|unverifiable) lines=([0-9]+|unverifiable) planes=([a-z][a-z,-]*) exit_map=(\S+) '
    r'verified=(yes|no)')
ROLLUP_RE = re.compile(r"printf 'TSUKUROI_CENSUS: %s \(([^)]*)\)\\n'")
VERSION_RE = re.compile(r"^VERSION='([^']*)'", re.M)
R46_RE = re.compile(r'^PASS .*\(R46-C1\)', re.M)
SELFTEST_RE = re.compile(r'TSUKUROI_CENSUS_SELFTEST: PASS \(\d+ cases, \d+ passed, 0 failed\)')
PREDICATE = ('identity_ok == 1 and tracks_ok == 1 and symlink_ok == 1 and unverifiable_ok == 1 and cli_ok == 1 '
             'and nowrite_ok == 1 and selftest_pass == 1 and selftest_r46 >= 4')


def facts(b):
    return {'sha256': hashlib.sha256(b).hexdigest(), 'md5': hashlib.md5(b).hexdigest(),
            'bytes': str(len(b)), 'lines': str(b.count(b'\n'))}


def snapshot(d):
    out = {}
    for root, dirs, files in os.walk(d):
        for n in dirs + files:
            p = os.path.join(root, n)
            st = os.lstat(p)
            out[os.path.relpath(p, d)] = (st.st_mode, st.st_size, st.st_mtime_ns)
    return out


def run(argv, cwd, env, stdin=None, timeout=120):
    """Child in its own session; on timeout the whole process group is killed and reaped (R44 FIFO/leak class)."""
    proc = subprocess.Popen(argv, cwd=cwd, env=env, stdin=stdin if stdin is not None else subprocess.DEVNULL,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
    try:
        out, err = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        proc.communicate()
        return 124, '', 'timeout'
    return proc.returncode, out.decode(errors='replace'), err.decode(errors='replace')


def parse(out):
    lines = out.split('\n')
    if lines and lines[-1] == '':
        lines.pop()
    if len(lines) != 1:
        return None
    m = LINE_RE.fullmatch(lines[0])
    if not m:
        return None
    keys = ('version', 'sha256', 'md5', 'bytes', 'lines', 'planes', 'exit_map', 'verified')
    return dict(zip(keys, m.groups()))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--revision', required=True)
    ap.add_argument('--scratch', required=True)
    ap.add_argument('--lane', default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    a = ap.parse_args()
    p = subprocess.run(['git', '-C', a.lane, 'rev-parse', '--verify', a.revision + '^{commit}'],
                       capture_output=True, stdin=subprocess.DEVNULL)
    if p.returncode != 0:
        print(json.dumps({'error': f'cannot resolve {a.revision}'}))
        return 2
    rev = p.stdout.decode().strip()
    p = subprocess.run(['git', '-C', a.lane, 'show', f'{rev}:{CENSUS}'], capture_output=True,
                       stdin=subprocess.DEVNULL)
    if p.returncode != 0:
        print(json.dumps({'error': f'cannot read {CENSUS} at {rev}'}))
        return 2
    fb = p.stdout
    text = fb.decode(errors='replace')
    os.makedirs(a.scratch, exist_ok=True)
    top = tempfile.mkdtemp(prefix='r46c1-', dir=os.path.abspath(a.scratch))
    try:
        return score(rev, fb, text, top)
    finally:
        shutil.rmtree(top, ignore_errors=True)


def score(rev, fb, text, top):
    src, run_d, tmp_d, home = (os.path.join(top, x) for x in ('src', 'run', 'tmp', 'home'))
    for d in (src, run_d, tmp_d, home):
        os.makedirs(d)
    env = {'PATH': '/usr/bin:/bin', 'LC_ALL': 'C', 'HOME': home, 'TMPDIR': tmp_d}
    F = os.path.join(src, 'tsukuroi-census.sh')
    with open(F, 'wb') as fh:
        fh.write(fb)
    G = os.path.join(src, 'probe-copy.sh')
    gb = fb + b'\n# r46 identity probe\n'  # leading newline: the census may end without one
    with open(G, 'wb') as fh:
        fh.write(gb)
    S = os.path.join(src, 'link.sh')
    os.symlink(F, S)
    vm = VERSION_RE.search(text)
    rm = ROLLUP_RE.search(text)
    want_version = vm.group(1) if vm else None
    want_planes = ','.join(k.split('=')[0] for k in rm.group(1).split()) if rm else None
    ff, gf = facts(fb), facts(gb)
    detail = {'want': {'version': want_version, 'planes': want_planes, **ff}}

    def static_ok(d):
        return (d is not None and d['version'] == want_version and d['planes'] == want_planes
                and d['exit_map'] == EXIT_MAP)

    before = snapshot(run_d), snapshot(tmp_d)

    rc, out, err = run(['bash', F, '--identity'], run_d, env)
    d = parse(out)
    identity_ok = int(rc == 0 and err == '' and static_ok(d) and d['verified'] == 'yes'
                      and all(d[k] == ff[k] for k in ff))
    detail['identity'] = {'rc': rc, 'stdout': out[:600], 'stderr': err[:300]}

    rc, out, err = run(['bash', G, '--identity'], run_d, env)
    d = parse(out)
    tracks_ok = int(rc == 0 and err == '' and static_ok(d) and d['verified'] == 'yes'
                    and all(d[k] == gf[k] for k in gf) and all(gf[k] != ff[k] for k in gf))
    detail['tracks'] = {'rc': rc, 'stdout': out[:600], 'stderr': err[:300]}

    rc, out, err = run(['bash', S, '--identity'], run_d, env)
    d = parse(out)
    symlink_ok = int(rc == 0 and err == '' and static_ok(d) and d['verified'] == 'yes'
                     and all(d[k] == ff[k] for k in ff))
    detail['symlink'] = {'rc': rc, 'stdout': out[:600], 'stderr': err[:300]}
    nowrite = snapshot(run_d) == before[0] and snapshot(tmp_d) == before[1]

    dec = os.path.join(top, 'decoy')
    os.makedirs(dec)
    for n in ('bash', 'tsukuroi-census.sh'):
        with open(os.path.join(dec, n), 'wb') as fh:
            fh.write(fb + b'# decoy\n')
    dbefore = snapshot(dec), snapshot(tmp_d)
    unv = []
    with open(F, 'rb') as fin:
        rc, out, err = run(['bash', '-s', '--', '--identity'], dec, env, stdin=fin)
    unv.append((rc, out, err))
    rc, out, err = run(['bash', '-c', 'exec bash <(cat "$1") --identity', '_', F], dec, env)
    unv.append((rc, out, err))
    # replaced after open: line 1 renames a decoy over the script's own path; bash keeps reading the old inode
    rep = os.path.join(top, 'replaced')
    os.makedirs(rep)
    R, RD = os.path.join(rep, 'census.sh'), os.path.join(rep, 'decoy.sh')
    with open(R, 'wb') as fh:
        fh.write(b'mv -f -- "$R46_DECOY" "$R46_PATH"\n' + fb)
    with open(RD, 'wb') as fh:
        fh.write(fb + b'\n# decoy\n')
    rc, out, err = run(['bash', R, '--identity'], rep, {**env, 'R46_DECOY': RD, 'R46_PATH': R})
    unv.append((rc, out, err))
    unverifiable_ok = 1
    detail['unverifiable'] = []
    for rc, out, err in unv:
        d = parse(out)
        good = (rc == 0 and err == '' and static_ok(d) and d['verified'] == 'no'
                and all(d[k] == 'unverifiable' for k in ('sha256', 'md5', 'bytes', 'lines')))
        unverifiable_ok &= int(good)
        detail['unverifiable'].append({'rc': rc, 'stdout': out[:600], 'stderr': err[:300]})
    nowrite = nowrite and snapshot(dec) == dbefore[0] and snapshot(tmp_d) == dbefore[1]
    nowrite_ok = int(nowrite)

    cli = []
    for argv, want_rc, needle in ((['--identity', '--selftest'], 2, None), (['--identity', '--sample', '3'], 2, None),
                                  (['--help'], 0, '--identity'), (['--bogus'], 2, None)):
        rc, out, err = run(['bash', F, *argv], run_d, env)
        cli.append(rc == want_rc and (needle is None or needle in out))
    cli_ok = int(all(cli))
    detail['cli'] = cli

    rc, out, err = run(['bash', F, '--selftest'], run_d, env, timeout=900)
    last = out.rstrip('\n').split('\n')[-1] if out.strip() else ''
    selftest_pass = int(rc == 0 and bool(SELFTEST_RE.fullmatch(last)))
    selftest_r46 = len(R46_RE.findall(out))
    detail['selftest'] = {'rc': rc, 'last': last, 'r46_labels': [ln for ln in out.split('\n') if '(R46-C1)' in ln]}

    ok = (identity_ok == 1 and tracks_ok == 1 and symlink_ok == 1 and unverifiable_ok == 1 and cli_ok == 1
          and nowrite_ok == 1 and selftest_pass == 1 and selftest_r46 >= 4)
    print(json.dumps({
        'counter': 'score-census-identity-r46', 'revision': rev, 'predicate': PREDICATE,
        'census_sha256': ff['sha256'], 'identity_ok': identity_ok, 'tracks_ok': tracks_ok,
        'symlink_ok': symlink_ok, 'unverifiable_ok': unverifiable_ok, 'cli_ok': cli_ok, 'nowrite_ok': nowrite_ok,
        'selftest_pass': selftest_pass, 'selftest_r46': selftest_r46, 'detail': detail,
        'verdict': 'PASS' if ok else 'FAIL'}, sort_keys=True))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
