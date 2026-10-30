#!/usr/bin/env python3
"""Second probe batch: attack the round-52 C1 counter's frozen rules.

1. entry+marks hash stability: does adding the round-52 gate heading change the GR1-3 section hashes?
2. dispatch duplicate with the SAME role: is "exactly one dispatch task" enforced?
3. README "not yet admitted round 52": does the marks leg's negation guard catch it?
4. citation to check-scrub-admission-r52.py beyond EOF: r52 (LANE_FILES) vs r51 (not declared).
"""
import hashlib
import json
import os
import subprocess
import sys

LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
REV = 'ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0'
C1R52 = f'{LANE}/tools/check-scrub-admission-r52.py'
C1R51 = f'{LANE}/tools/check-scrub-admission-r51.py'
ENTRY = 'corpus/knowledge/btrfs-scrub-grounding-r45.md'
SCRATCH = '/fast/scratch/hyaku/tsukuroi-r52/R52CritDecl'
WORK = os.path.join(SCRATCH, 'fx2')
os.makedirs(WORK, exist_ok=True)

CITE = {'GR1': [('cmdline.c', 147), ('kstrtox.c', 1)],
        'GR2': [('dev-replace.c', 1111), ('scrub.c', 3094)],
        'GR3': [('systemd.kill.xml', 1), ('btrfs-scrub@.service', 1)]}
ROLES = {r: [f'R52RevGR{r[2:]}{x}' for x in 'abc'] + [f'R52CritGR{r[2:]}{x}' for x in 'abc']
         for r in ('GR1', 'GR2', 'GR3')}
FROZEN_HASHES = {'GR1': '98fa4e07768d240eaf5ea2cce13ce0623fdb756054e5df9f7b9fe68ab2e63987',
                 'GR2': '9fd581a0c9d02b02100b6a15648b7c6e4be896ac746ed09303a88dc8a24f0ec5',
                 'GR3': '0405f38a5783c49b6c078b118c9868543eb494b43f8b1c5e6c14284a123b9eac'}


def git_show(rev, path):
    p = subprocess.run(['git', '-C', LANE, 'show', f'{rev}:{path}'], capture_output=True)
    if p.returncode:
        raise SystemExit(f'cannot read {path}')
    return p.stdout.decode('utf-8')


def section_hashes(text):
    lines = text.split('\n')
    out = {}
    for row in ('GR1', 'GR2', 'GR3'):
        i = next(k for k, ln in enumerate(lines) if ln.strip() == f'## {row}')
        j = next((k for k in range(i + 1, len(lines)) if lines[k].startswith('## ')), len(lines))
        out[row] = hashlib.sha256('\n'.join(lines[i:j]).encode('utf-8')).hexdigest()
    return out


print('== 1. section-hash stability when the round-52 gate heading is appended at EOF ==')
base_entry = git_show(REV, ENTRY)
h0 = section_hashes(base_entry)
marked_eof = base_entry + '\n## Gate status — round 52 (GR1-GR3 admitted)\n\nfixture.\n'
h1 = section_hashes(marked_eof)
for r in ('GR1', 'GR2', 'GR3'):
    print(f'   {r}: frozen={FROZEN_HASHES[r][:12]} base={h0[r][:12]} base+mark@EOF={h1[r][:12]} '
          f'stable={h0[r]==FROZEN_HASHES[r]} unchanged_by_mark={h0[r]==h1[r]}')
# and if the mark were inserted BEFORE the '## How this changes OS triage' heading (i.e. inside/after GR3)
alt = base_entry.replace('## How this changes OS triage',
                          '## Gate status — round 52 (GR1-GR3 admitted)\n\nfixture.\n\n## How this changes OS triage', 1)
h2 = section_hashes(alt)
print('   if the mark heading is inserted right after GR3 (before "How this changes OS triage"):')
for r in ('GR1', 'GR2', 'GR3'):
    print(f'      {r}: {h2[r][:12]}  == frozen? {h2[r]==FROZEN_HASHES[r]}')

print()
print('== 2/3/4: counter behaviour probes ==')


def build(tag, entry_text, readme_text, bodies=None, dispatch_extra=None, tool=C1R52):
    d = os.path.join(WORK, tag)
    os.makedirs(d, exist_ok=True)
    wave = os.path.join(d, 'wave')
    os.makedirs(wave, exist_ok=True)
    hashes = section_hashes(entry_text)
    tasks, results = [], []
    for row, seats in ROLES.items():
        for seat in seats:
            role = 'reviewer' if 'Rev' in seat else 'critic'
            body = (bodies or {}).get(seat)
            if body is None:
                cites = ' '.join(f'{f}:{n}' for f, n in CITE[row])
                body = (f'Seat {seat} read row {row} on the frozen bytes. The cited lines {cites} decide '
                        f'the statement and the pinned snapshot carries the quoted form. Nothing further is '
                        f'outstanding for this row and the sibling rows were checked the same way. '
                        f'This body is written by seat {seat} and is distinct from the others. ')
            with open(os.path.join(wave, f'{seat}.md'), 'w', encoding='utf-8') as fh:
                fh.write(f'ROW {row} VERDICT: holds\nSECTION SHA256: {hashes[row]}\n{body}\n')
            tasks.append({'name': seat, 'agent': role})
            results.append({'name': seat, 'agent': role, 'output': 'done'})
    if dispatch_extra:
        tasks.extend(dispatch_extra)
    with open(os.path.join(d, 'results.json'), 'w', encoding='utf-8') as fh:
        json.dump({'results': results}, fh)
    with open(os.path.join(d, 'dispatch.json'), 'w', encoding='utf-8') as fh:
        json.dump({'taskCall': {'context': 'fixture', 'tasks': tasks}}, fh)
    skill = '# fixture skill\n\n## Scrub grounding — round 52 admission\n\nfixture.\n'
    paths = {}
    for name, text in (('entry.md', entry_text), ('skill.md', skill), ('readme.md', readme_text)):
        p = os.path.join(d, name)
        with open(p, 'w', encoding='utf-8') as fh:
            fh.write(text)
        paths[name] = p
    cmd = [sys.executable, tool, '--revision', REV, '--no-base-check',
           '--entry-file', paths['entry.md'], '--skill-file', paths['skill.md'],
           '--readme-file', paths['readme.md'], '--dispatch-file', os.path.join(d, 'dispatch.json'),
           '--results-file', os.path.join(d, 'results.json'), '--wave-dir', wave]
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=WORK)
    try:
        obj = json.loads(p.stdout.strip().split('\n')[-1])
    except Exception:
        obj = {'raw': p.stdout[-300:], 'err': p.stderr[-300:]}
    return p.returncode, obj


def show(label, rc, obj):
    print(f'   {label}: rc={rc} verdict={obj.get("verdict")} marks={obj.get("marks")} '
          f'verdicts_ok={obj.get("verdicts_ok")} seats_ok={obj.get("seats_ok")}')
    for n in (obj.get('seat_notes') or [])[:4]:
        print('      note:', n)


GOOD_README = ('# fixture readme\n\n## Round 52\n\nThe btrfs scrub grounding entry '
               '`btrfs-scrub-grounding-r45.md` is admitted round 52 on its re-read bytes.\n')
NEG_README = ('# fixture readme\n\n## Round 52\n\nThe btrfs scrub grounding entry '
              '`btrfs-scrub-grounding-r45.md` is not yet admitted round 52 and stays in review.\n')

rc, obj = build('ctl', marked_eof, GOOD_README)
show('CONTROL (mark@EOF, good readme)', rc, obj)

rc, obj = build('dup_same_role', marked_eof, GOOD_README,
                dispatch_extra=[{'name': 'R52RevGR1a', 'agent': 'reviewer'}])
show('TEST dispatch has R52RevGR1a TWICE with the same role', rc, obj)

rc, obj = build('neg_readme', marked_eof, NEG_README)
show('TEST readme says "not yet admitted round 52"', rc, obj)

cite_beyond = {s: ('The row is supported by the cited sources check-scrub-admission-r52.py:9999 and '
                    'dev-replace.c:1111 together with scrub.c:3094 as read. ' + 'Padding. ' * 30)
               for s in ROLES['GR2']}
rc, obj = build('cite_eof_r52', marked_eof, GOOD_README, bodies=cite_beyond, tool=C1R52)
show('TEST r52 counter: GR2 bodies cite check-scrub-admission-r52.py:9999 (declared, beyond EOF)', rc, obj)
rc, obj = build('cite_eof_r51', marked_eof, GOOD_README, bodies=cite_beyond, tool=C1R51)
show('TEST r51 counter (same bodies; basename NOT in r51 LANE_FILES)', rc, obj)
