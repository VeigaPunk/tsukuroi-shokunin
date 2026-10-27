#!/usr/bin/env python3
"""C1ExecHeldOut: independent equivalence harness for the five R45-C1 census readers.

Does NOT import tools/score-census-readers-r45.py. Extracts the five statements from the
two revisions with `git show`, feeds the IMPL statement the full captured output and the
BASE statement the output's first line alone (the oracle), then compares the resulting
variable bytes, exit codes and stderr, under LC_ALL=C and LC_ALL=C.UTF-8.

CAP_OUT is reconstructed as `$(cat FILE; printf '\001')` minus the guard byte, i.e. exactly
what an unquoted command substitution can hold (no NUL, no trailing-newline stripping).
"""
import binascii
import json
import os
import random
import shutil
import subprocess
import sys

ROOT = '/fast/scratch/hyaku/tsukuroi-r45/C1ExecHeldOut'
LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
IMPL = '18389f44cf6ce414d7be205998b29c79fb0b490c'
BASE = '5bbd5ff588120fd8e7c744695351a6978b4241c1'
CENSUS = 'tools/tsukuroi-census.sh'
LOCALES = ['C', 'C.UTF-8']
DRAWN_PER_SITE = 210

SITE_ORDER = ['S1', 'S2', 'S3', 'S4', 'S5']
VAR = {'S1': 'state', 'S2': 'r', 'S3': 'driver', 'S4': 't_word', 'S5': 'r'}
FUNC = {'S1': 'probe_systemd', 'S2': 'probe_systemd', 'S3': 'probe_drivers',
        'S4': 'probe_journal', 'S5': 'probe_journal'}
# ordinal of the assignment among `<var>=` lines inside that function, per revision
ORD_BASE = {'S1': 1, 'S2': 1, 'S3': 1, 'S4': 1, 'S5': 1}
ORD_IMPL = {'S1': 1, 'S2': 1, 'S3': 1, 'S4': 1, 'S5': 1}


def git_show(rev):
    p = subprocess.run(['git', '-C', LANE, 'show', rev + ':' + CENSUS],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    return p.stdout.decode('utf-8', 'surrogateescape')


def func_ranges(text):
    """name -> (start_line_index, end_line_index) of the top-level function body."""
    lines = text.split('\n')
    starts = {}
    for i, ln in enumerate(lines):
        s = ln.rstrip()
        if s.endswith('() {') and not ln.startswith(' '):
            starts[s[:-4]] = i
    out = {}
    keys = sorted(starts.items(), key=lambda kv: kv[1])
    for k, (name, i) in enumerate(keys):
        j = keys[k + 1][1] if k + 1 < len(keys) else len(lines)
        out[name] = (i, j)
    return lines, out


def extract(text, ords):
    lines, ranges = func_ranges(text)
    found = {}
    for sid in SITE_ORDER:
        lo, hi = ranges[FUNC[sid]]
        v = VAR[sid]
        n = 0
        for i in range(lo + 1, hi):
            if lines[i].lstrip().startswith(v + '='):
                n += 1
                if n == ords[sid]:
                    found[sid] = lines[i].strip()
                    break
        if sid not in found:
            raise SystemExit('cannot locate %s %s' % (sid, v))
    return found


# ---------------------------------------------------------------- corpus
POOLS = {
    'S1': ['running', 'degraded', 'starting', 'stopping', 'maintenance', 'offline',
           'unknown', '', 'Failed to connect to bus: No medium found',
           'Failed to connect to bus: Permission denied', 'running (degraded)'],
    'S2': ['success', 'failed', 'exit-code', 'signal', 'timeout', '', 'success (exit-code)'],
    'S3': ['NVIDIA GeForce RTX 5070, 610.57.04', 'NVIDIA RTX A2000 12GB, 580.95.05',
           'x,  y,   z', 'no comma here', '', 'a,', 'a, ', ',', 'GPU, 610.57.04',
           'NVIDIA GeForce RTX 5070 , 610.57.04', 'a,b,c'],
    'S4': ['active', 'inactive', 'activating', 'deactivating', 'failed', 'reloading',
           'maintenance', 'unknown', 'refreshing', ''],
    'S5': ['active', 'inactive', 'failed', 'deactivating', 'activating', 'reloading',
           'maintenance', ''],
}
MB = ['dégradé', '启动中', '実行中', 'ok ✓', 'naïve', '状態', '\u00e9']
DECO = ['', ' ', '\t', '  \r', '\r', ' \t \r', '\r\r', '\v', '\f', '\v\f',
        '\xc2\xa0', ' \xc2\xa0', '\xe3\x80\x80', '\xe2\x80\xa8', '\x0b\x0c',
        ' \t ', '\x0d\x0a']
TAIL_LINE_ALPHABET = ('abcdefghijklmnopqrstuvwxyz0123456789 ,.:=-_/[]()' +
                      '\xc3\xa9\xe4\xb8\x96')


def drawn_bytes(rng, sid):
    first = rng.choice(POOLS[sid])
    if rng.random() < 0.25:
        first = rng.choice(['', ' ', '\t', '\r', '\xc2\xa0']) + first
    if rng.random() < 0.25:
        first += rng.choice(MB)
    line = first + rng.choice(DECO)
    if rng.random() < 0.12:  # CR in the middle of the first line
        k = rng.randrange(len(line) + 1)
        line = line[:k] + rng.choice(['\r', '\r\n', '\r\r']) + line[k:]
    kind = rng.choice(['none', 'none', 'small', 'small', 'small', 'large'])
    if kind == 'none':
        tail = ''
    elif kind == 'small':
        n = rng.randint(1, 5)
        tail = '\n' + '\n'.join(rng.choice(POOLS[sid]) + rng.choice([' tail', '  ', '\r tail'])
                                for _ in range(n))
        if rng.random() < 0.5:
            tail += '\n'
    else:
        target = rng.randint(70_000, 300_000)
        parts, size = [], 0
        while size < target:
            w = ''.join(rng.choice(TAIL_LINE_ALPHABET) for _ in range(rng.randint(5, 120)))
            if rng.random() < 0.05:
                w += '\r'
            parts.append(w)
            size += len(w) + 1
        tail = '\n' + '\n'.join(parts)
        if rng.random() < 0.5:
            tail += '\n'
    return (line + tail).encode('utf-8', 'surrogateescape')


def huge(n):
    return b'x' * n


EDGE_CASES = [
    ('empty', b''),
    ('only-newline', b'\n'),
    ('only-newlines-3', b'\n\n\n'),
    ('blanks-only-spaces', b'   '),
    ('blanks-mixed', b' \t\v\f\r '),
    ('blanks-tab', b'\t\t'),
    ('nbsp-only', b'\xc2\xa0'),
    ('nbsp-at-end', b'degraded\xc2\xa0'),
    ('vt-at-end', b'degraded\x0b'),
    ('ff-at-end', b'degraded\x0c'),
    ('vt-ff-at-end', b'degraded\x0b\x0c\v\f'),
    ('nbsp-then-space', b'degraded\xc2\xa0 '),
    ('space-then-nbsp', b'degraded \xc2\xa0'),
    ('ideographic-space', b'degraded\xe3\x80\x80'),
    ('line-separator-u2028', b'degraded\xe2\x80\xa8'),
    ('zwsp-u200b', b'degraded\xe2\x80\x8b'),
    ('narrow-nbsp-u202f', b'degraded\xe2\x80\xaf'),
    ('figure-space-u2007', b'degraded\xe2\x80\x87'),
    ('nel-u0085', b'degraded\xc2\x85'),
    ('ogham-u1680', b'degraded\xe1\x9a\x80'),
    ('del-0x7f', b'degraded\x7f'),
    ('utf8-text', b'd\xc3\xa9grad\xc3\xa9'),
    ('utf8-cjk', b'\xe5\x90\xaf\xe5\x8a\xa8\xe4\xb8\xad'),
    ('utf8-emoji', b'degraded \xf0\x9f\x9a\x80'),
    ('cr-middle', b'in\ractive'),
    ('cr-multi-middle', b'a\rb\rc'),
    ('cr-at-end', b'degraded\r'),
    ('crlf-at-end', b'degraded\r\n'),
    ('only-crs', b'\r\r\r'),
    ('leading-vt', b'\x0bdegraded'),
    ('leading-trailing-space', b' degraded '),
    ('multiline-3', b'running\nrunning\nrunning'),
    ('trailing-newline', b'degraded\n'),
    ('invalid-0x80-at-end', b'degraded\x80'),
    ('invalid-0xff-at-end', b'degraded\xff'),
    ('truncated-c2', b'degraded\xc2'),
    ('truncated-e280', b'degraded\xe2\x80'),
    ('lone-0xa0', b'degraded\xa0'),
    ('first-line-64k+tail', huge(70000) + b'\nrunning'),
    ('first-line-64k-only', huge(70000)),
    ('first-line-64k-blanks+tail', b' ' * 70000 + b'\nrunning'),
    ('first-line-65536-exact+tail', huge(65536) + b'\nrunning'),
    ('small-first-large-tail', b'degraded\n' + b'y' * 200000),
    ('nbsp-large-tail', b'degraded\xc2\xa0\n' + b'z' * 150000),
]


# ---------------------------------------------------------------- runner
def write_driver(path, sid, stmt, var, base, capture='guard'):
    stmt = stmt.replace('\n', ' ')
    body = '''#!/usr/bin/env bash
set -u
IN=$1; OUT=$2
for f in "$IN"/*.dat; do
  id=${f##*/}; id=${id%.dat}
  set +e
  ( set -euo pipefail
    CAP_OUT=$(cat -- "$f"; printf '\\001')
    CAP_OUT=${CAP_OUT%$'\\001'}
    @@IMPL@@
    printf '%s' "$@@VAR@@" > "$OUT/$id.impl"
  ) 2>"$OUT/$id.impl.err"
  printf '%s\\n' "$?" > "$OUT/$id.impl.rc"
  ( set -euo pipefail
    CAP_OUT=$(cat -- "$IN/$id.first"; printf '\\001')
    CAP_OUT=${CAP_OUT%$'\\001'}
    @@BASE@@
    printf '%s' "$@@VAR@@" > "$OUT/$id.base"
  ) 2>"$OUT/$id.base.err"
  printf '%s\\n' "$?" > "$OUT/$id.base.rc"
done
'''
    body = body.replace('@@IMPL@@', stmt).replace('@@BASE@@', base).replace('@@VAR@@', var)
    if capture == 'prod':
        # exactly cap(): CAP_OUT=$("$@" 2>&1) -- trailing newlines stripped, no guard byte
        body = body.replace("$(cat -- \"$f\"; printf '\\001')\n    CAP_OUT=${CAP_OUT%$'\\001'}",
                            '$(cat -- "$f")')
        body = body.replace("$(cat -- \"$IN/$id.first\"; printf '\\001')\n    CAP_OUT=${CAP_OUT%$'\\001'}",
                            '$(cat -- "$IN/$id.first")')
        assert "printf '\\001'" not in body, body
    with open(path, 'w', encoding='utf-8', errors='surrogateescape') as f:
        f.write(body)
    os.chmod(path, 0o755)


def run_driver(path, indir, outdir, locale, tmp):
    env = {k: v for k, v in os.environ.items() if not k.startswith(('TSUKUROI_', 'UFO_'))}
    env['LC_ALL'] = locale
    env['TMPDIR'] = tmp
    p = subprocess.run(['bash', path, indir, outdir], stdin=subprocess.DEVNULL,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env,
                       start_new_session=True)
    return p.returncode, p.stdout, p.stderr


def readval(path):
    try:
        with open(path, 'rb') as f:
            return f.read()
    except FileNotFoundError:
        return None


def hexs(b):
    return binascii.hexlify(b).decode()


def classify(sid, val):
    """Census-verdict-relevant class of the read variable (S3 feeds evidence text only)."""
    if sid == 'S1':
        if val in {b'running', b'degraded', b'starting', b'stopping', b'maintenance',
                   b'offline', b'unknown'}:
            return 'in-vocabulary'
        return 'unusable->BLOCKED'
    if sid == 'S2':
        if val is None:
            return '?'
        if val == b'':
            return 'timer_unknown+1'
        return 'timer_fail+1' if val != b'success' else 'success'
    if sid == 'S3':
        return 'evidence-text-only(smi=%s)' % val.decode('utf-8', 'backslashreplace')
    if sid == 'S4':
        if val == b'active':
            return 'active'
        if val in {b'reloading', b'activating', b'inactive', b'deactivating', b'failed',
                   b'maintenance', b'unknown', b'refreshing'}:
            return 'BLOCKED(boot-did-not-reach)'
        return 'BLOCKED(probe-unusable)'
    if sid == 'S5':
        if val == b'':
            return 'timer_unknown+1'
        return 'armed' if val == b'active' else 'drift+1'
    return '?'


def main():
    rng = random.Random(0x45C1)
    base_lines = extract(git_show(BASE), ORD_BASE)
    impl_lines = extract(git_show(IMPL), ORD_IMPL)

    # sanity: base lines must all carry the early reader, impl lines must not
    for sid in SITE_ORDER:
        assert '| head -n1' in base_lines[sid], (sid, base_lines[sid])
        assert 'head -n1' not in impl_lines[sid], (sid, impl_lines[sid])
        assert impl_lines[sid].endswith('(R45-C1)'), (sid, impl_lines[sid])

    corpus = os.path.join(ROOT, 'corpus')
    if os.path.isdir(corpus):
        shutil.rmtree(corpus)
    os.makedirs(corpus)
    cases = {}
    for sid in SITE_ORDER:
        cs = []
        for k in range(DRAWN_PER_SITE):
            cs.append(('drawn-%03d' % k, drawn_bytes(rng, sid)))
        for name, b in EDGE_CASES:
            cs.append((name, b))
        cases[sid] = cs
        d = os.path.join(corpus, sid)
        os.makedirs(d)
        for name, b in cs:
            first = b.split(b'\n', 1)[0]
            with open(os.path.join(d, name + '.dat'), 'wb') as f:
                f.write(b)
            with open(os.path.join(d, name + '.first'), 'wb') as f:
                f.write(first)

    results = {}
    tmp = os.path.join(ROOT, 'tmp')
    os.makedirs(tmp, exist_ok=True)
    for sid in SITE_ORDER:
        for loc in LOCALES:
            tag = loc.replace('.', '_')
            outdir = os.path.join(ROOT, 'out', sid, tag)
            if os.path.isdir(outdir):
                shutil.rmtree(outdir)
            os.makedirs(outdir)
            drv = os.path.join(ROOT, 'drv_%s_%s.sh' % (sid, tag))
            write_driver(drv, sid, impl_lines[sid], VAR[sid], base_lines[sid])
            rc, so, se = run_driver(drv, os.path.join(corpus, sid), outdir, loc, tmp)
            if rc != 0:
                raise SystemExit('driver %s/%s rc=%d %s' % (sid, loc, rc, se[-500:]))
            mism = []
            basefail = []
            for name, b in cases[sid]:
                impl = readval(os.path.join(outdir, name + '.impl'))
                base = readval(os.path.join(outdir, name + '.base'))
                ir = int(readval(os.path.join(outdir, name + '.impl.rc')).strip())
                br = int(readval(os.path.join(outdir, name + '.base.rc')).strip())
                ierr = readval(os.path.join(outdir, name + '.impl.err')) or b''
                berr = readval(os.path.join(outdir, name + '.base.err')) or b''
                rec = {'case': name, 'bytes': len(b), 'impl_rc': ir, 'base_rc': br,
                       'impl': hexs(impl) if impl is not None else None,
                       'base': hexs(base) if base is not None else None,
                       'impl_err': ierr.decode('utf-8', 'backslashreplace')[:300],
                       'base_err': berr.decode('utf-8', 'backslashreplace')[:300]}
                if br != 0 or base is None:
                    basefail.append(rec)
                if ir != 0 or impl is None or base is None or impl != base:
                    mism.append(rec)
            results[(sid, loc)] = {'n': len(cases[sid]), 'mismatches': mism,
                                   'oracle_failures': basefail}
            print('%s %-8s cases=%d mismatches=%d oracle_failures=%d'
                  % (sid, loc, len(cases[sid]), len(mism), len(basefail)))
            for rec in mism[:5]:
                print('   MISMATCH %s implrc=%d baserc=%d impl=%s base=%s'
                      % (rec['case'], rec['impl_rc'], rec['base_rc'], rec['impl'], rec['base']))
            for rec in basefail[:5]:
                print('   ORACLE-FAIL %s baserc=%d err=%s' % (rec['case'], rec['base_rc'],
                                                             rec['base_err']))

    with open(os.path.join(ROOT, 'results.json'), 'w') as f:
        json.dump({('%s/%s' % k): v for k, v in results.items()}, f, indent=1)
    total = sum(v['n'] for v in results.values())
    bad = sum(len(v['mismatches']) for v in results.values())
    of = sum(len(v['oracle_failures']) for v in results.values())
    print('TOTAL cases=%d mismatches=%d oracle_failures=%d' % (total, bad, of))


if __name__ == '__main__':
    main()
