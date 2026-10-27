#!/usr/bin/env python3
"""Round-45 C1 counter (frozen before data): the census's single-line probe readers.

Surface scored: `tools/tsukuroi-census.sh`. At the base (5bbd5ff5) five production probe readers keep only the
first line of a captured output with `printf '%s\\n' "$CAP_OUT" | head -n1 | ...` inside an assignment. Under the
census's `set -euo pipefail`, an output past the pipe buffer lets `head` exit early, the producer dies of SIGPIPE,
the assignment returns 141 and the whole census exits 141 (the R41-CENSUS-PIPEFAIL-692 class; routed since round 42,
round-43 closure item 3, round-44 lesson §3). Sites, located by (function, assignment variable, ordinal):
  S1 probe_systemd  state   (systemctl --user is-system-running)
  S2 probe_systemd  r       (systemctl --user show <timer> -p Result)
  S3 probe_drivers  driver  (nvidia-smi --query-gpu=name,driver_version)
  S4 probe_journal  t_word  (systemctl is-active <boot target>)
  S5 probe_journal  r       (systemctl --user show <timer> -p ActiveState)
A site's statement is the ONE physical line in that function whose stripped text starts with `<var>=`
(the ordinal-th such line); a site written over several lines is scored on that first line only.
S6 is the foreign-baseline lookup (probe_packages, `bn`), already a full read since round 42; it is scored only
by the revert leg (a regression guard), never by the equivalence leg.

Legs.
  lexical_hits  production lines (before `run_selftest() {`) matching `"$CAP_OUT"` followed by `| head`.
  sites_found   S1-S5 statements located.
  equiv_ok      per site S1-S5, every draw must give the same value as the BASE statement and exit 0. A draw is a
                captured output: a first line from a per-site pool with drawn blanks/CR decorations, then no tail,
                a small tail (1-5 lines) or a large tail (70-300 KB of drawn printable lines, CRs, with or without
                a final newline); at least three large draws per site, eight draws per site. The REV statement
                runs on the full output; the oracle is the BASE statement run on the output's first line alone
                (the base reads nothing past it). Both run in `bash -c` with `set -euo pipefail`, LC_ALL=C,
                CAP_OUT read through `$(cat file)` (as `cap()` captures), timeout 30 s.
  selftest      `bash census --selftest` at REV (TMPDIR in scratch): `TSUKUROI_CENSUS_SELFTEST: PASS (<n> cases,
                <n> passed, 0 failed)`; selftest_r45 = PASS lines whose label ends `(R45-C1)`.
  revert_killed per site S1-S6, a mutant of the REV census whose site line is replaced (indent kept) by the base
                early-reader form (S1-S5 their base lines; S6 `bn=$(printf '%s\\n' "$base_txt" | awk -v n="$nm"
                '$1 == n { print $2; exit }')`, the round-41 form); killed when its selftest exits non-zero AND
                prints at least one `FAIL ` line whose label ends `(R45-C1)`.
  adjacency_ok  kill rule (round-44 harm, R44C-ADJ-IN109): `tools/check-adjacency-anchors.py --revision REV`, run
                from the lane copy whose bytes (and `tools/_revision.py`) equal the BASE bytes, prints status PASS.

Predicate (same sentence in the declaration and the receipt label):
  PASS iff lexical_hits == 0 and sites_found == 5 and equiv_ok == 5 and selftest_pass == 1
  and selftest_r45 >= 6 and revert_killed == 6 and adjacency_ok == 1.

Usage: python3 tools/score-census-readers-r45.py --revision <REV> --scratch <DIR> [--lane <repo>] [--seed <hex>]
--scratch is required; children run with TMPDIR inside it, in their own session, stdin closed; a timeout kills the
child's process group and reaps it. Everything written lives under --scratch/r45c1-<pid> and is removed on exit,
SIGINT and SIGTERM. Output: one JSON line; exit 0 PASS, 1 FAIL, 2 usage/read/harness error.
"""
import argparse
import hashlib
import json
import os
import random
import re
import shutil
import signal
import subprocess
import sys

BASE = '5bbd5ff588120fd8e7c744695351a6978b4241c1'
CENSUS = 'tools/tsukuroi-census.sh'
ADJ = 'tools/check-adjacency-anchors.py'
ADJ_DEPS = ('tools/check-adjacency-anchors.py', 'tools/_revision.py')
SITES = [
    ('S1', 'probe_systemd', 'state', 1,
     "state=$(printf '%s\\n' \"$CAP_OUT\" | head -n1 | tr -d '\\r' | sed -E 's/[[:space:]]+$//')"),
    ('S2', 'probe_systemd', 'r', 1, "r=$(printf '%s\\n' \"$CAP_OUT\" | head -n1 | tr -d '\\r')"),
    ('S3', 'probe_drivers', 'driver', 1,
     "driver=$(printf '%s\\n' \"$CAP_OUT\" | head -n1 | awk -F', *' '{print $NF}')"),
    ('S4', 'probe_journal', 't_word', 1,
     "t_word=$(printf '%s\\n' \"$CAP_OUT\" | head -n1 | tr -d '\\r' | sed -E 's/[[:space:]]+$//')"),
    ('S5', 'probe_journal', 'r', 1,
     "r=$(printf '%s\\n' \"$CAP_OUT\" | head -n1 | tr -d '\\r' | sed -E 's/[[:space:]]+$//')"),
]
S6 = ('S6', 'probe_packages', 'bn', 1,
      "bn=$(printf '%s\\n' \"$base_txt\" | awk -v n=\"$nm\" '$1 == n { print $2; exit }')")
POOLS = {
    'S1': ['running', 'degraded', 'starting', 'maintenance', 'offline', 'Failed to connect to bus: No medium found'],
    'S2': ['success', 'failed', 'exit-code', 'signal', ''],
    'S3': ['NVIDIA GeForce RTX 5070, 610.57.04', 'NVIDIA RTX A2000 12GB, 580.95.05', 'x,  y,   z', 'no comma here', ''],
    'S4': ['active', 'inactive', 'activating', 'failed', 'unknown'],
    'S5': ['active', 'inactive', 'failed', 'deactivating', ''],
}
LEX_RE = re.compile(r'"\$CAP_OUT"\s*\|\s*head\b')
SUMMARY_RE = re.compile(r'^TSUKUROI_CENSUS_SELFTEST: (PASS|FAIL) \((\d+) cases, (\d+) passed, (\d+) failed\)$', re.M)
PREDICATE = ('lexical_hits == 0 and sites_found == 5 and equiv_ok == 5 and selftest_pass == 1 '
             'and selftest_r45 >= 6 and revert_killed == 6 and adjacency_ok == 1')
WORK = None


def cleanup(*_):
    if WORK and os.path.isdir(WORK):
        for root, dirs, _files in os.walk(WORK):
            for d in dirs:
                try:
                    os.chmod(os.path.join(root, d), 0o700)
                except OSError:
                    pass
        shutil.rmtree(WORK, ignore_errors=True)


def on_signal(signum, _frame):
    cleanup()
    sys.exit(128 + signum)


def child_env(tmp):
    e = {k: v for k, v in os.environ.items() if not k.startswith(('TSUKUROI_', 'UFO_'))}
    e['TMPDIR'] = tmp
    e['LC_ALL'] = 'C'
    return e


def run(cmd, timeout, env, cwd=None):
    """Run in a new session with stdin closed; on timeout kill the process group and reap."""
    p = subprocess.Popen(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         env=env, cwd=cwd, start_new_session=True)
    try:
        out, err = p.communicate(timeout=timeout)
        return p.returncode, out, err, False
    except subprocess.TimeoutExpired:
        try:
            os.killpg(p.pid, signal.SIGKILL)
        except OSError:
            pass
        out, err = p.communicate()
        return 124, out, err, True


def git(lane, *args):
    p = subprocess.run(['git', '-C', lane, *args], capture_output=True, stdin=subprocess.DEVNULL)
    return p.returncode, p.stdout


def show(lane, rev, path):
    rc, out = git(lane, 'show', f'{rev}:{path}')
    return out if rc == 0 else None


def functions(lines):
    """name -> (start index, end index) for top-level `name() {` ... `}` blocks."""
    out, cur, start = {}, None, 0
    for i, ln in enumerate(lines):
        m = re.match(r'^([a-z_][a-z0-9_]*)\(\) \{\s*$', ln)
        if m:
            cur, start = m.group(1), i
            continue
        if cur and ln == '}':
            out.setdefault(cur, (start, i))
            cur = None
    return out


def locate(lines, funcs, func, var, ordinal):
    if func not in funcs:
        return None
    lo, hi = funcs[func]
    n = 0
    for i in range(lo + 1, hi):
        if lines[i].lstrip().startswith(var + '='):
            n += 1
            if n == ordinal:
                return i
    return None


def draws(rng, site):
    out = []
    for k in range(8):
        first = rng.choice(POOLS[site])
        deco = rng.choice(['', ' ', '\t', '  \r', '\r', ' \t \r', '\r\r'])
        if first and rng.random() < 0.3:
            first = rng.choice(['', ' ']) + first
        line = first + deco
        kind = 'large' if k < 3 else rng.choice(['none', 'small', 'large'])
        if kind == 'none':
            tail = ''
        elif kind == 'small':
            tail = '\n' + '\n'.join(rng.choice(POOLS[site]) + ' tail' for _ in range(rng.randint(1, 5)))
        else:
            target = rng.randint(70_000, 300_000)
            parts, size = [], 0
            while size < target:
                w = ''.join(rng.choice('abcdefghijklmnopqrstuvwxyz0123456789 ,.:=-_') for _ in range(rng.randint(5, 120)))
                if rng.random() < 0.05:
                    w += '\r'
                parts.append(w)
                size += len(w) + 1
            tail = '\n' + '\n'.join(parts)
        if rng.random() < 0.5:
            tail += '\n'
        out.append((kind, line + tail))
    return out


def eval_stmt(stmt, var, data, d, tmp):
    inp = os.path.join(d, 'in')
    with open(inp, 'w', newline='') as f:
        f.write(data)
    script = ('set -euo pipefail\nCAP_OUT=$(cat "$1")\n' + stmt + '\n'
              + 'printf "%s" "${' + var + '}" > "$2"\n')
    outp = os.path.join(d, 'out')
    if os.path.exists(outp):
        os.unlink(outp)
    rc, _o, _e, to = run(['bash', '-c', script, 'eval', inp, outp], 30, child_env(tmp))
    val = open(outp, 'rb').read() if rc == 0 and os.path.exists(outp) else None
    return rc, val, to


def selftest(path, tmp, timeout=900):
    rc, out, err, to = run(['bash', path, '--selftest'], timeout, child_env(tmp), cwd=tmp)
    text = (out + err).decode(errors='replace')
    return rc, text, to


def main():
    global WORK
    ap = argparse.ArgumentParser()
    ap.add_argument('--revision', required=True)
    ap.add_argument('--scratch', required=True)
    ap.add_argument('--lane', default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    ap.add_argument('--seed', default=None)
    a = ap.parse_args()
    rc, out = git(a.lane, 'rev-parse', '--verify', a.revision + '^{commit}')
    if rc != 0:
        print(json.dumps({'error': f'cannot resolve {a.revision}'}))
        return 2
    rev = out.decode().strip()
    if git(a.lane, 'cat-file', '-e', BASE + '^{commit}')[0] != 0:
        print(json.dumps({'error': 'base commit absent from the lane'}))
        return 2
    os.makedirs(a.scratch, exist_ok=True)
    WORK = os.path.join(os.path.abspath(a.scratch), f'r45c1-{os.getpid()}')
    os.makedirs(WORK)
    signal.signal(signal.SIGINT, on_signal)
    signal.signal(signal.SIGTERM, on_signal)
    tmp = os.path.join(WORK, 'tmp')
    os.makedirs(tmp)
    try:
        return score(a, rev, tmp)
    finally:
        cleanup()


def score(a, rev, tmp):
    seed = a.seed or os.urandom(8).hex()
    rng = random.Random(seed)
    cb, bb = show(a.lane, rev, CENSUS), show(a.lane, BASE, CENSUS)
    if cb is None or bb is None:
        print(json.dumps({'error': 'census unreadable at REV or BASE'}))
        return 2
    text = cb.decode(errors='surrogateescape')
    lines = text.split('\n')
    funcs = functions(lines)
    st_start = next((i for i, ln in enumerate(lines) if ln.startswith('run_selftest() {')), len(lines))
    lexical = sum(1 for ln in lines[:st_start] if LEX_RE.search(ln))

    # equivalence leg
    per, sites_found, equiv_ok = {}, 0, 0
    for sid, func, var, ordn, base_line in SITES:
        i = locate(lines, funcs, func, var, ordn)
        r = {'found': i is not None}
        if i is None or i >= st_start:
            r['found'] = False
            per[sid] = r
            continue
        sites_found += 1
        stmt = lines[i].strip()
        d = os.path.join(WORK, 'eq-' + sid)
        os.makedirs(d)
        bad = []
        for kind, data in draws(rng, sid):
            cap_out = data.rstrip('\n')            # $(...) strips trailing newlines, as cap() does
            first = cap_out.split('\n', 1)[0]
            orc, oval, _ = eval_stmt(base_line, var, first, d, tmp)
            rrc, rval, rto = eval_stmt(stmt, var, data, d, tmp)
            if orc != 0 or rrc != 0 or oval != rval:
                bad.append({'kind': kind, 'len': len(data), 'oracle_rc': orc, 'rev_rc': rrc, 'timed_out': rto,
                            'oracle': (oval or b'')[:60].decode(errors='replace'),
                            'rev': (rval or b'')[:60].decode(errors='replace')})
        r.update({'line': i + 1, 'draws': 8, 'mismatches': len(bad), 'first_mismatch': bad[:1]})
        equiv_ok += not bad
        per[sid] = r

    # selftest leg
    cpath = os.path.join(WORK, 'census.sh')
    with open(cpath, 'wb') as f:
        f.write(cb)
    src, stext, sto = selftest(cpath, tmp)
    m = SUMMARY_RE.search(stext)
    selftest_line = m.group(0) if m else None
    selftest_pass = int(bool(m and src == 0 and m.group(1) == 'PASS' and m.group(2) == m.group(3)
                             and m.group(4) == '0'))
    r45 = sum(1 for ln in stext.splitlines() if ln.startswith('PASS ') and '(R45-C1)' in ln)

    # revert leg
    killed, rev_detail = 0, {}
    for sid, func, var, ordn, base_line in SITES + [S6]:
        i = locate(lines, funcs, func, var, ordn)
        if i is None or i >= st_start:
            rev_detail[sid] = 'site-missing'
            continue
        mut = list(lines)
        indent = re.match(r'^\s*', lines[i]).group(0)
        mut[i] = indent + base_line
        mpath = os.path.join(WORK, f'mut-{sid}.sh')
        with open(mpath, 'w', errors='surrogateescape') as f:
            f.write('\n'.join(mut))
        mrc, mtext, mto = selftest(mpath, tmp)
        r45fail = sum(1 for ln in mtext.splitlines() if ln.startswith('FAIL ') and '(R45-C1)' in ln)
        k = mrc != 0 and r45fail > 0
        killed += k
        rev_detail[sid] = {'exit': mrc, 'r45_fail_lines': r45fail, 'killed': k, 'timed_out': mto}

    # adjacency kill rule
    adj = {'bytes_base': True}
    for p in ADJ_DEPS:
        wb = open(os.path.join(a.lane, p), 'rb').read() if os.path.exists(os.path.join(a.lane, p)) else None
        if wb is None or wb != show(a.lane, BASE, p) or show(a.lane, rev, p) != wb:
            adj['bytes_base'] = False
    adjacency_ok = 0
    if adj['bytes_base']:
        arc, aout, _aerr, _ = run([sys.executable, os.path.join(a.lane, ADJ), '--revision', rev], 600,
                                  child_env(tmp))
        try:
            aj = json.loads(aout.decode(errors='replace').strip().splitlines()[-1])
        except (ValueError, IndexError):
            aj = {}
        adj.update({'exit': arc, 'status': aj.get('status'), 'findings': [f.get('id') for f in aj.get('findings', [])]})
        adjacency_ok = int(arc == 0 and aj.get('status') == 'PASS')

    ok = (lexical == 0 and sites_found == 5 and equiv_ok == 5 and selftest_pass == 1 and r45 >= 6
          and killed == 6 and adjacency_ok == 1)
    print(json.dumps({
        'counter': 'score-census-readers-r45', 'revision': rev, 'base': BASE, 'predicate': PREDICATE, 'seed': seed,
        'census_sha256': hashlib.sha256(cb).hexdigest(), 'lexical_hits': lexical, 'sites_found': sites_found,
        'equiv_ok': equiv_ok, 'per_site': per, 'selftest_pass': selftest_pass, 'selftest_line': selftest_line,
        'selftest_timed_out': sto, 'selftest_r45': r45, 'revert_killed': killed, 'revert': rev_detail,
        'adjacency_ok': adjacency_ok, 'adjacency': adj, 'verdict': 'PASS' if ok else 'FAIL'}, sort_keys=True))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
