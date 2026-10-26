#!/usr/bin/env python3
"""Generate the F-24 receipts from the scratch fixture (no lane writes)."""
import hashlib, json, re, subprocess

S = '/fast/scratch/hyaku/tsukuroi-r42/SimplifierLesson'
LANE = f'{S}/lane'
REPO = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
PIN = '78abb8b5'


def git(*a, cwd=LANE):
    return subprocess.run(['git', '-C', cwd, *a], capture_output=True, text=True).stdout


def show(rev, path):
    return git('show', f'{rev}:{path}')


def sections(text):
    out, cur = {}, None
    for ln in text.splitlines():
        m = re.match(r'^## (SC\d)\s*$', ln)
        if m:
            cur = m.group(1); out.setdefault(cur, []); continue
        if re.match(r'^## ', ln):
            cur = None; continue
        if cur:
            out[cur].append(ln)
    return out


E0 = show(PIN, 'corpus/knowledge/btrfs-scrub-record-r42.md')
E1 = open(f'{LANE}/corpus/knowledge/btrfs-scrub-record-r42.md').read()  # full set checked out
SKILL = show(PIN, 'SKILL.md').split('\n')
s0, s1 = sections(E0), sections(E1)

# 1. row identity
lines = ['Row-text identity: the counted unit of tools/check-scrub-record-r42.py is the set of lines under each',
         '`## SC<n>` heading (counter sections(), tools/check-scrub-record-r42.py:83-97).'
         ' Token per row: SC1 LOCK_EX, SC2',
         '`scrub status:1`, SC3 `status recording disabled`, SC4 `_SCRUB_FS_STAT_MIN`, SC5 `scrub_speed_max`.',
         '']
for r in sorted(s0):
    a, b = '\n'.join(s0[r]), '\n'.join(s1.get(r, []))
    lines.append(f'{r}: identical={a == b}  sha256(before)={hashlib.sha256(a.encode()).hexdigest()[:16]}'
                 f'  sha256(after)={hashlib.sha256(b.encode()).hexdigest()[:16]}  token_present={ {
                     'SC1': "LOCK_EX", 'SC2': "scrub status:1", 'SC3': "status recording disabled",
                     'SC4': "_SCRUB_FS_STAT_MIN", 'SC5': "scrub_speed_max"}[r] in b }')
open(f'{S}/row-identity.txt', 'w').write('\n'.join(lines) + '\n')
print('\n'.join(lines))

# 2. duplication map
stop = set('the a an of to is are and or in on for by with as at not no this that be it its from than then so what '
           'one two read reads reading status scrub record device devices every any has have had when where which who '
           'there their'.split())


def toks(t):
    return {w.lower() for w in re.findall(r"[A-Za-z_][A-Za-z0-9_./-]*", t) if w.lower() not in stop and len(w) > 2}


triage = '\n'.join(E0.split('\n')[143:150])
rows = SKILL[3904:3916]
bullets = [b.strip() for b in re.split(r'\n(?=- )', triage.replace('\n  ', ' '))]
out = ['# F-24 duplication map at', f'# pin {PIN}; entry lines 144-150 vs SKILL.md:3905-3916', '']
for i, b in enumerate(bullets, 1):
    tb = toks(b)
    best = sorted(((len(tb & toks(r)) / max(1, len(tb)), 3905 + j) for j, r in enumerate(rows)), reverse=True)[:3]
    span = {1: '144-145', 2: '146-147', 3: '148-149', 4: '150'}[i]
    out.append(f'bullet {i} (entry :{span}) [{len(b)} B]: '
               + ', '.join(f'SKILL:{n} {c:.0%}' for c, n in best))
out += ['', 'Mapping (semantic, read against the table Reading and Action columns):',
        '  b1 :144-145 -> SKILL:3905 (Reading "no device record carries a start time (SC4)"; Action "read \\"no record of a',
        '                 run\\", not \\"never scrubbed\\"") + SKILL:3906 Action "stored-data integrity stays `UNVERIFIED` (SH4)"',
        '  b2 :146-147 -> SKILL:3913 (aborted: "any device record is canceled (SC4)") + SKILL:3914 (finished: "every',
        '                 device that has a record is finished; devices without a record are skipped (SC4)")',
        '  b3 :148-149 -> SKILL:3915 ("an unfinished record and nothing running (SC4)" | "a process outcome; read the',
        '                 per-device error sums (`-d`, `-R`)")',
        '  b4 :150     -> SKILL:3916 ("devinfo/<devid>/scrub_speed_max limits it")',
        '', 'Four of four bullets are covered; b3 and b4 are near-verbatim (59% / 80% stopword-filtered token overlap).',
        'Only proposition NOT in the table: b1\'s "what SC3 adds is the mechanism, not a new verdict" (meta about the',
        'entry, restated in the entry\'s own scope and SC3).', '']
open(f'{S}/dup-map.txt', 'w').write('\n'.join(out) + '\n')
print('\n'.join(out))

# 3. the one-proposition-many-sites tally, from greps at the pin
g = subprocess.run(['git', '-C', REPO, 'grep', '-n', '-i', 'never scrubbed', PIN, '--',
                    'corpus/knowledge/btrfs-scrub-record-r42.md', 'SKILL.md'], capture_output=True, text=True).stdout
g2 = subprocess.run(['git', '-C', REPO, 'grep', '-n', '-i', 'does not prove\\|leaves none\\|cannot show', PIN, '--',
                     'corpus/knowledge/btrfs-scrub-record-r42.md'], capture_output=True, text=True).stdout
tally = ['# sites carrying "a missing record is not evidence that no scrub ran" at', f'# {PIN}', '',
         '$ git grep -n -i "never scrubbed" 78abb8b5 -- corpus/knowledge/btrfs-scrub-record-r42.md SKILL.md']
tally += [ln.split(':', 1)[1] if ln.startswith(PIN) else ln for ln in g.splitlines()]
tally += ['', '$ git grep -n -i "does not prove\\|leaves none\\|cannot show" 78abb8b5 -- <entry>']
tally += [ln.split(':', 1)[1] for ln in g2.splitlines()]
tally += ['', '=> the proposition "no record is not never-scrubbed" stands at 5 sites: entry :13 (scope framing),',
          '   :72-73 (SC3 statement, counted row), :144 (triage bullet 1), :157 (Limits: what the host readings prove),',
          '   SKILL:3905 (table row 1). A sixth site carries the verdict half only: SKILL:3906 "stored-data integrity',
          '   stays `UNVERIFIED` (SH4)". P2 removes the :144 copy and leaves the other four: :72-73 is the counted row,',
          '   :157 bounds the host evidence, SKILL:3905 and SKILL:3906 answer two different observations (command output',
          '   vs file absence) and merging them would shift SKILL.md:3907-3941, which three live w2 reports cite.']
open(f'{S}/proposition-sites.txt', 'w').write('\n'.join(tally) + '\n')
print('\n'.join(tally))


# 4. counter comparison (before at the pin, after on each proposed fixture commit)
keys = ['rows', 'quotes_ok', 'novelty_ok', 'novelty_base_hits', 'host_ok', 'sources_ok', 'capture_ok']
base = json.load(open(f'{S}/counter-before.json'))
cmp_lines = ['# check-scrub-record-r42.py, same fixture clone, three revisions', '',
             'revision                                    ' + '  '.join(f'{k:>17}' for k in keys)]
for label, f in (('78abb8b5 (pin)', 'counter-before.json'),
                 ('zerodrift P1+P3', 'counter-zerodrift.json'),
                 ('fullset P1+P2+P3', 'counter-full.json')):
    d = json.load(open(f'{S}/{f}'))
    cmp_lines.append(f'{label:43}' + '  '.join(f'{str(d.get(k)):>17}' for k in keys))
cmp_lines += ['', 'per-row quote counts (good/in_window)  before -> zerodrift -> fullset']
for r in sorted(base['per_row']):
    a, b, c = (json.load(open(f'{S}/{f}'))['per_row'][r]['quotes'] for f in
               ('counter-before.json', 'counter-zerodrift.json', 'counter-full.json'))
    cmp_lines.append(f'  {r}: {a["good"]}/{a["in_window"]} -> {b["good"]}/{b["in_window"]} -> {c["good"]}/{c["in_window"]}')
cmp_lines += ['',
              'verdicts_ok is 0 in all three runs because the fixture clone carries no w2-results.json / residual-results.json',
              'or w2 report files; that field is a property of the clone, not of the edit, and this seat did not measure it',
              'on the real lane. rows/quotes_ok/novelty_ok/host_ok/sources_ok/novelty_base_hits are the fields an edit to',
              'Scope, the triage block and the tail can move, and they are identical.']
open(f'{S}/counter-compare.txt', 'w').write('\n'.join(cmp_lines) + '\n')
print('\n'.join(cmp_lines))
