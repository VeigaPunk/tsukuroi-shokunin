#!/usr/bin/env python3
"""Round-42 C1 pre-data controls: score each control census with the frozen counter
tools/score-size-invariance-r42.py (read from the lane at the freeze revision) in a private fixture
clone (`git clone --shared`, origin removed, fixture identity only inside the clone).

Controls (each a one-parameter variant of the base census at c8efaa3f):
  K0 do-nothing           the base census itself
  K1 size-gate            update-plane sites fixed; packages answers BLOCKED whenever the sample > 64 KiB
  K2 head-truncation      update-plane sites fixed; packages parses only the first 64 KiB of the sample
  K3 head+tail            update-plane sites fixed; packages parses the first and last 32 KiB
  K4 packages-only        :692/:694 fixed; the four update-plane early readers left as they are
  K5 padding-filter       update-plane sites fixed; packages drops warning and zero-altered lines first,
                          then runs the original early-reader tests (mirror evasion of the padding)
  K6 candidate            every frozen site fixed (reachability: must PASS)
  K7 fixture-gated        K6, but the packages fix runs only when TSUKUROI_FIXTURE is set (QUALITY 82)
  K8 cached-live          K7 plus a replay cache outside fixtures: the first packages answer is stored under
                          $HOME and replayed by later runs (QUALITY 82 cached-live arm)
Each must FAIL except K6.

Usage: python3 run_controls_c1.py --lane <lane> --counter-rev <REV> --scratch <DIR> --out <DIR> [--names K0,K6]
"""
import argparse
import json
import os
import shutil
import subprocess
import sys

BASE = 'c8efaa3f120834541f8de1e5e0367e8d1593bae6'
CENSUS = 'tools/tsukuroi-census.sh'

PKG_TEST = """  if printf '%s\\n' "$s_out" | grep -q '^error:'; then
    PKG_V=BLOCKED
    PKG_NOTE="pacman -Qkk sample probe error: $(printf '%s\\n' "$s_out" | grep -m1 '^error:')"
    return
  fi
"""
PKG_FIXED = """  if grep -q '^error:' <<<"$s_out"; then
    PKG_V=BLOCKED
    PKG_NOTE="pacman -Qkk sample probe error: $(grep -m1 '^error:' <<<"$s_out")"
    return
  fi
"""
UPD = [
    ("""cand_names=$(printf '%s\\n' "$CAP_OUT" | head -n3 | awk '{print $1}' | paste -sd, -)""",
     """cand_names=$(printf '%s\\n' "$CAP_OUT" | awk 'NR <= 3 {print $1}' | paste -sd, -)"""),
    ("""cand_names=$(printf '%s\\n' "$CAP_OUT" | head -n3 \\
      | awk '{n=$1; sub(/^[^/]+\\//, "", n); print n}' | paste -sd, -)""",
     """cand_names=$(printf '%s\\n' "$CAP_OUT" \\
      | awk 'NR <= 3 {n=$1; sub(/^[^/]+\\//, "", n); print n}' | paste -sd, -)"""),
    ("""cand_names=$(printf '%s\\n' "$CAP_OUT" | head -n3 \\
        | awk '{n=$1; sub(/^[^/]+\\//, "", n); print n}' | paste -sd, -)""",
     """cand_names=$(printf '%s\\n' "$CAP_OUT" \\
        | awk 'NR <= 3 {n=$1; sub(/^[^/]+\\//, "", n); print n}' | paste -sd, -)"""),
    ("""suu_first=$(printf '%s\\n' "$CAP_OUT" | head -n1 | tr -d '\\r')""",
     """suu_first=$(printf '%s\\n' "$CAP_OUT" | awk 'NR == 1' | tr -d '\\r')"""),
]
SOUT = """  s_out=$(printf '%s\\n' "$CAP_OUT" | tr '\\r' '\\n')\n"""


def sub1(src, old, new):
    if src.count(old) != 1:
        raise SystemExit(f'anchor not unique ({src.count(old)}): {old[:80]!r}')
    return src.replace(old, new)


def fix_update(src):
    for old, new in UPD:
        src = sub1(src, old, new)
    return src


def variant(name, base):
    if name == 'K0':
        return base
    if name == 'K4':
        return sub1(base, PKG_TEST, PKG_FIXED)
    if name == 'K6':
        return fix_update(sub1(base, PKG_TEST, PKG_FIXED))
    if name in ('K7', 'K8'):
        gated = PKG_FIXED.replace("""  if grep -q '^error:' <<<"$s_out"; then""",
                                  """  if { [ -n "${TSUKUROI_FIXTURE:-}" ] && grep -q '^error:' <<<"$s_out"; } \\
     || { [ -z "${TSUKUROI_FIXTURE:-}" ] && printf '%s\\n' "$s_out" | grep -q '^error:'; }; then""")
        src = fix_update(sub1(base, PKG_TEST, gated))
        if name == 'K8':
            src = sub1(src, 'probe_packages() {\n', 'probe_packages() {\n'
                       '  if [ -z "${TSUKUROI_FIXTURE:-}" ] && [ -f "$HOME/.tsk-cache" ]; then\n'
                       '    PKG_V=$(sed -n 1p "$HOME/.tsk-cache"); PKG_NOTE=$(sed -n 2p "$HOME/.tsk-cache"); return\n'
                       '  fi\n')
            src = sub1(src, """  printf 'PLANE packages: %s (%s; %s)\\n' "$PKG_V" "$PKG_NOTE" "$ROOT_NOTE"\n""",
                       """  if [ -z "${TSUKUROI_FIXTURE:-}" ] && [ ! -f "$HOME/.tsk-cache" ]; then printf '%s\\n%s\\n' "$PKG_V" "$PKG_NOTE" > "$HOME/.tsk-cache"; fi\n"""
                       """  printf 'PLANE packages: %s (%s; %s)\\n' "$PKG_V" "$PKG_NOTE" "$ROOT_NOTE"\n""")
        return src
    src = fix_update(base)
    if name == 'K1':
        gate = SOUT + """  if [ "${#s_out}" -gt 65536 ]; then
    PKG_V=BLOCKED
    PKG_NOTE="pacman -Qkk sample probe error: sample too large"
    return
  fi
"""
        return sub1(src, SOUT, gate)
    if name == 'K2':
        return sub1(src, SOUT, SOUT + '  s_out=${s_out:0:65536}\n')
    if name == 'K3':
        return sub1(src, SOUT, SOUT + """  if [ "${#s_out}" -gt 65536 ]; then s_out="${s_out:0:32768}"$'\\n'"${s_out: -32768}"; fi\n""")
    if name == 'K5':
        filt = SOUT + """  s_out=$(grep -vE '^warning: |: [0-9]+ total files, 0 altered files$' <<<"$s_out" || true)\n"""
        return sub1(src, SOUT, filt)
    raise SystemExit(f'unknown control {name}')


def git(d, *a, **kw):
    return subprocess.run(['git', '-C', d, *a], check=True, capture_output=True, text=True, **kw)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lane', required=True)
    ap.add_argument('--counter-rev', required=True)
    ap.add_argument('--scratch', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--names', default='K0,K1,K2,K3,K4,K5,K6,K7,K8')
    a = ap.parse_args()
    os.makedirs(a.scratch, exist_ok=True)
    os.makedirs(a.out, exist_ok=True)
    clone = os.path.join(a.scratch, 'fixture-clone')
    shutil.rmtree(clone, ignore_errors=True)
    summary = {}
    try:
        subprocess.run(['git', 'clone', '-q', '--shared', '--no-checkout', a.lane, clone], check=True)
        if os.path.realpath(git(clone, 'rev-parse', '--show-toplevel').stdout.strip()) != os.path.realpath(clone):
            raise SystemExit('fixture toplevel mismatch')
        git(clone, 'remote', 'remove', 'origin')
        if a.counter_rev == 'WORKTREE':   # pre-freeze dry run only; receipts name a committed revision
            counter = open(os.path.join(a.lane, 'tools/score-size-invariance-r42.py'), 'rb').read()
        else:
            counter = subprocess.run(['git', '-C', a.lane, 'show', f'{a.counter_rev}:tools/score-size-invariance-r42.py'],
                                     check=True, capture_output=True).stdout
        cpath = os.path.join(a.scratch, 'counter.py')
        open(cpath, 'wb').write(counter)
        base = git(a.lane, 'show', f'{BASE}:{CENSUS}').stdout
        idt = ['-c', 'user.name=fixture', '-c', 'user.email=fixture@invalid']
        git(clone, 'checkout', '-q', '--detach', BASE)
        for name in a.names.split(','):
            src = variant(name, base)
            git(clone, 'checkout', '-q', '--detach', BASE)
            open(os.path.join(clone, CENSUS), 'w').write(src)
            git(clone, 'add', CENSUS)
            subprocess.run(['git', '-C', clone, *idt, 'commit', '-q', '--allow-empty', '-m', f'control {name}'],
                           check=True, capture_output=True)
            rev = git(clone, 'rev-parse', 'HEAD').stdout.strip()
            p = subprocess.run([sys.executable, cpath, '--revision', rev, '--lane', clone,
                                '--scratch', os.path.join(a.scratch, 'counter-scratch')],
                               capture_output=True, text=True)
            line = p.stdout.strip().splitlines()[-1] if p.stdout.strip() else '{}'
            rec = {'control': name, 'exit': p.returncode, 'counter_rev': a.counter_rev, 'result': json.loads(line)}
            with open(os.path.join(a.out, f'C1-{name}.jsonl'), 'w') as f:
                f.write(json.dumps(rec, sort_keys=True) + '\n')
            r = rec['result']
            summary[name] = r.get('verdict')
            print(name, p.returncode, r.get('verdict'), r.get('invariant'), r.get('non_invariant'), 'ns', r.get('ns_invariant'),
                  r.get('selftest_pass'), r.get('default_equal'), flush=True)
        sf = [k for k, v in summary.items() if k != 'K6' and v == 'PASS']
        last = {'battery': 'C1', 'controls': summary, 'should_fail_accepted': len(sf),
                'should_fail_accepted_names': sf, 'control_accepted': int(summary.get('K6') == 'PASS')}
        with open(os.path.join(a.out, 'battery-summary.jsonl'), 'w') as f:
            f.write(json.dumps(last, sort_keys=True) + '\n')
        print(json.dumps(last, sort_keys=True))
    finally:
        shutil.rmtree(clone, ignore_errors=True)


if __name__ == '__main__':
    main()
