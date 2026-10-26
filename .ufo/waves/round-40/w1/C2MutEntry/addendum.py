#!/usr/bin/env python3
"""C2MutEntry addendum: two sharpening probes for the (e) class — S-ids cited outside
the source cell are never validated by check-exec-environment-r40.py.

EX4-e4: EX4 rule cell cites S219 (meson_options.txt:17). Swap it to bogus S999.
EX4-e5: EX4 host cell cites S225 (libalpm-shell-strings.txt). Swap it to bogus S999.
Expect PASS (survivor) for both if rule/host cells are unscanned.
"""
import hashlib, json, os, re, subprocess

D = os.environ['D']
SEAT = os.environ['SEAT']
ENTRY = 'corpus/knowledge/pacman-exec-environment-r40.md'
DOC = 'bf2380503b8e4a5d33162026854b0b7b66d18b86'
ROW_RE = re.compile(r'^\|\s*(EX\d+)\s*\|')


def sh(*a):
    return subprocess.run(list(a), capture_output=True)


def parse_row(line):
    body = line.rstrip('\n')
    parts = body[1:-1].split('|')
    assert len(parts) == 5
    return parts


def setcell(line, k, newcore):
    parts = parse_row(line)
    seg = parts[k]
    lead = seg[:len(seg) - len(seg.lstrip())]
    trail = seg[len(seg.rstrip()):]
    parts[k] = lead + newcore + trail
    return '|' + '|'.join(parts) + '|\n'


pristine = sh('git', '-C', D, 'show', f'{DOC}:{ENTRY}').stdout
lines = pristine.decode('utf-8').splitlines(keepends=True)
hidx = next(i for i, l in enumerate(lines) if l.startswith('source:'))
ridx = {}
for i, l in enumerate(lines):
    m = ROW_RE.match(l)
    if m:
        ridx[m.group(1)] = i

probes = [
    ('EX4-e4', '(e4) EX4 rule cell: cited S-id S219 -> bogus S999 (rule cells unscanned?)',
     ridx['EX4'], 1, 'S219', 'S999'),
    ('EX4-e5', '(e5) EX4 host cell: cited S-id S225 -> bogus S999 (host cells unscanned?)',
     ridx['EX4'], 4, 'S225', 'S999'),
]

out = open(os.path.join(SEAT, 'mutants.jsonl'), 'a')
for mid, desc, i, k, old_id, new_id in probes:
    parts = parse_row(lines[i])
    old = parts[k].strip()
    assert old.count(old_id) >= 1, (mid, old_id, old[:80])
    new = old.replace(old_id, new_id, 1)
    new_lines = list(lines)
    new_lines[i] = setcell(lines[i], k, new)
    new_bytes = ''.join(new_lines).encode('utf-8')
    assert new_bytes != pristine
    with open(os.path.join(D, ENTRY), 'wb') as f:
        f.write(new_bytes)
    sh('git', '-C', D, 'add', ENTRY)
    c = sh('git', '-C', D, 'commit', '-q', '-m', f'mutant {mid}: {desc}')
    assert c.returncode == 0, c.stderr.decode()[:300]
    sha = sh('git', '-C', D, 'rev-parse', 'HEAD').stdout.decode().strip()
    files = sh('git', '-C', D, 'show', '--name-only', '--format=', sha).stdout.decode().split()
    assert files == [ENTRY], files
    p = subprocess.run(['python3', os.path.join(D, 'tools', 'check-exec-environment-r40.py'),
                        '--repo', D, '--revision', sha], capture_output=True, text=True, timeout=600)
    rec = json.loads(p.stdout)
    t = {'id': mid, 'desc': desc, 'sha': sha,
         'sha256_pristine_entry': hashlib.sha256(pristine).hexdigest(),
         'sha256_mutated_entry': hashlib.sha256(new_bytes).hexdigest(),
         'returncode': p.returncode, 'rules_verified': rec.get('rules_verified'),
         'result': rec.get('result'), 'source_ok': rec.get('source_ok'),
         'counts_ok': rec.get('counts_ok'), 'duplicate_rows': rec.get('duplicate_rows'),
         'duplicate_headings': rec.get('duplicate_headings'),
         'novelty_base_hits': rec.get('novelty_base_hits'), 'rules': rec.get('rules'),
         'edits': [{'old': old, 'new': new}]}
    out.write(json.dumps(t, sort_keys=True) + '\n')
    failed = [ex for ex, rr in (rec.get('rules') or {}).items() if rr and not rr['verified']]
    print(f"{mid:8s} rules_verified={t['rules_verified']} result={t['result']} exit={p.returncode} "
          f"{'SURVIVOR' if t['result'] == 'PASS' else 'killed'} failing_rows={','.join(failed) or '-'} "
          f"source_ok={t['source_ok']} counts_ok={t['counts_ok']}")
out.close()
with open(os.path.join(D, ENTRY), 'wb') as f:
    f.write(pristine)
print('addendum done; working tree restored to pristine')
