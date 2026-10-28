#!/usr/bin/env python3
"""GRevQuotes: independent audit of every **Quote.** line in GR1/GR2/GR3 of
corpus/knowledge/btrfs-scrub-grounding-r45.md at the round-48 freeze revision.
Own parser; snapshots read via `git show REV:path` (the bytes under test)."""
import hashlib, json, re, subprocess, sys

LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
REV = 'ae99f021b76f8eb1c8805d32d80644464afb1ff6'
ENTRY = 'corpus/knowledge/btrfs-scrub-grounding-r45.md'

def show(path):
    p = subprocess.run(['git', '-C', LANE, 'show', f'{REV}:{path}'],
                       capture_output=True)
    return p.stdout if p.returncode == 0 else None

# S-id -> directory inside the repo; file resolves inside it.
# Derived independently from the entry header + FETCH.txt files:
#   S237 round-42 scrub.c; S240 round-43 ioctl.c;
#   S242 scrub.c / S243 sysfs.c / S244 service+timer+PKGBUILD in round-44;
#   S246 cmdline.c+vsprintf.c+kstrtox.c, S247 dev-replace.c,
#   S248 systemd.kill.xml in round-45/src; S249 round-45 hostcap/capture.txt.
SDIR = {
    'S237': '.ufo/waves/round-42/frozen/src',
    'S240': '.ufo/waves/round-43/frozen/src',
    'S242': '.ufo/waves/round-44/frozen/src',
    'S243': '.ufo/waves/round-44/frozen/src',
    'S244': '.ufo/waves/round-44/frozen/src',
    'S246': '.ufo/waves/round-45/frozen/src',
    'S247': '.ufo/waves/round-45/frozen/src',
    'S248': '.ufo/waves/round-45/frozen/src',
    'S249': '.ufo/waves/round-45/frozen/hostcap',
}

doc = show(ENTRY)
assert doc is not None, 'entry missing at rev'
text = doc.decode('utf-8')
lines = text.split('\n')

# --- own section splitter: '## GRn' up to the next '## ' header ---
def extent(row):
    idx = [i for i, l in enumerate(lines) if l == f'## {row}']
    assert len(idx) == 1, f'{row}: header count {len(idx)}'
    i = idx[0]
    nxt = [j for j in range(i + 1, len(lines)) if lines[j].startswith('## ')]
    return i + 1, (nxt[0] if nxt else len(lines))

QUOTE_RE = re.compile(r'^\*\*Quote\.\*\*\s+`(S\d+)`\s+([^:]+):(\d+):\s*"(.*)"\s*$')
QUOTES_RE = re.compile(r'^\*\*Quote\.\*\*\s+`S\d+`\s+[^:]+:\d+:')  # any claim-id prefix

def norm(s):
    return ' '.join(s.split())

# --- digest verify every file we resolve against its SHA256SUMS ---
sums_cache = {}
def sums_for(sdir):
    if sdir in sums_cache:
        return sums_cache[sdir]
    raw = show(f'{sdir}/SHA256SUMS')
    m = {}
    if raw:
        for ln in raw.decode('utf-8', 'replace').splitlines():
            parts = ln.split()
            if len(parts) == 2 and re.fullmatch(r'[0-9a-f]{64}', parts[0]):
                m[parts[1]] = parts[0]
    sums_cache[sdir] = m
    return m

file_cache = {}
def snap(sid, fname):
    """-> (path, [lines]) or (path, None) with digest status recorded."""
    sdir = SDIR.get(sid)
    if sdir is None:
        return None, None, 'unknown S-id'
    path = f'{sdir}/{fname}'
    if path not in file_cache:
        raw = show(path)
        if raw is None:
            file_cache[path] = (None, 'absent at rev')
        else:
            listed = sums_for(sdir).get(fname)
            got = hashlib.sha256(raw).hexdigest()
            if listed is None:
                file_cache[path] = (raw, 'no SHA256SUMS entry')
            elif listed != got:
                file_cache[path] = (raw, f'DIGEST MISMATCH listed {listed} got {got}')
            else:
                file_cache[path] = (raw, 'digest ok')
    raw, st = file_cache[path]
    return path, (raw.decode('utf-8', 'replace').split('\n') if raw is not None else None), st

report = {'rev': REV, 'rows': {}, 'unparsed_quoteish': [], 'digest_checks': {}}
total_q = total_ok = 0
for row in ('GR1', 'GR2', 'GR3'):
    a, b = extent(row)
    qs = []
    for i in range(a, b):
        ln = lines[i]
        if '**Quote.**' in ln and not QUOTES_RE.match(ln):
            report['unparsed_quoteish'].append({'row': row, 'line': i + 1, 'text': ln[:160]})
        m = QUOTE_RE.match(ln)
        if not m:
            continue
        sid, fname, no, want = m.group(1), m.group(2).strip(), int(m.group(3)), m.group(4)
        path, got_lines, st = snap(sid, fname)
        rec = {'doc_line': i + 1, 'sid': sid, 'file': fname, 'src_line': no,
               'path': path, 'digest': st}
        if got_lines is None:
            rec['result'] = f'FAIL snapshot: {st}'
        elif not (1 <= no <= len(got_lines)):
            rec['result'] = f'FAIL line {no} outside {len(got_lines)}-line file'
        else:
            gl = got_lines[no - 1]
            rec['exact_substring'] = want in gl
            rec['norm_substring'] = norm(want) in norm(gl)
            rec['norm_full_line'] = norm(want) == norm(gl)
            rec['src_line_text'] = gl
            if not rec['norm_substring']:
                rec['result'] = 'FAIL quote mismatch'
            else:
                rec['result'] = 'ok'
        qs.append(rec)
    ok = sum(1 for q in qs if q['result'] == 'ok')
    report['rows'][row] = {'quotes': len(qs), 'ok': ok,
                           'bad': [q for q in qs if q['result'] != 'ok'],
                           'exact_vs_norm': [q for q in qs
                                             if q['result'] == 'ok'
                                             and not q.get('exact_substring')],
                           'all': qs}
    total_q += len(qs); total_ok += ok

# digest summary: every snapshot file touched
seen = {}
for row in report['rows'].values():
    for q in row['all']:
        seen[q['path']] = q['digest']
report['digest_checks'] = seen
report['totals'] = {'quotes': total_q, 'ok': total_ok}
print(json.dumps(report, indent=1))
