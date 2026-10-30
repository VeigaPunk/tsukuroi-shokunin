#!/usr/bin/env python3
"""Fixture harness: probe what the frozen round-52 C1 counter actually enforces.

Writes only under /fast/scratch/hyaku/tsukuroi-r52/R52CritDecl/.
Reads the lane read-only (git show) and runs the FROZEN counter with fixture overrides.
"""
import hashlib
import json
import os
import subprocess
import sys

LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
REV = 'ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0'
C1 = f'{LANE}/tools/check-scrub-admission-r52.py'
ENTRY = 'corpus/knowledge/btrfs-scrub-grounding-r45.md'
SCRATCH = '/fast/scratch/hyaku/tsukuroi-r52/R52CritDecl'
WORK = os.path.join(SCRATCH, 'fx')
os.makedirs(WORK, exist_ok=True)

CITE = {
    'GR1': [('cmdline.c', 147), ('kstrtox.c', 1)],
    'GR2': [('dev-replace.c', 1111), ('scrub.c', 3094)],
    'GR3': [('systemd.kill.xml', 1), ('btrfs-scrub@.service', 1)],
}
ROLES = {r: [f'R52RevGR{r[2:]}{x}' for x in 'abc'] + [f'R52CritGR{r[2:]}{x}' for x in 'abc']
         for r in ('GR1', 'GR2', 'GR3')}


def git_show(rev, path):
    p = subprocess.run(['git', '-C', LANE, 'show', f'{rev}:{path}'], capture_output=True)
    if p.returncode:
        raise SystemExit(f'cannot read {path}')
    return p.stdout.decode('utf-8')


def section_hash(text, row):
    lines = text.split('\n')
    heads = [i for i, ln in enumerate(lines) if ln.strip() == f'## {row}']
    i = heads[0]
    j = next((k for k in range(i + 1, len(lines)) if lines[k].startswith('## ')), len(lines))
    return hashlib.sha256('\n'.join(lines[i:j]).encode('utf-8')).hexdigest()


def build(tag, body_fn, dispatch_dup=False):
    d = os.path.join(WORK, tag)
    os.makedirs(d, exist_ok=True)
    wave = os.path.join(d, 'wave')
    os.makedirs(wave, exist_ok=True)
    entry = git_show(REV, ENTRY) + '\n## Gate status — round 52 (GR1-GR3 admitted)\n\nfixture.\n'
    hashes = {r: section_hash(entry, r) for r in ('GR1', 'GR2', 'GR3')}
    tasks, results = [], []
    for row, seats in ROLES.items():
        for seat in seats:
            role = 'reviewer' if 'Rev' in seat else 'critic'
            body = body_fn(row, seat, hashes[row])
            with open(os.path.join(wave, f'{seat}.md'), 'w', encoding='utf-8') as fh:
                fh.write(f'ROW {row} VERDICT: holds\nSECTION SHA256: {hashes[row]}\n{body}\n')
            tasks.append({'name': seat, 'agent': role})
            results.append({'name': seat, 'agent': role, 'output': 'done'})
    if dispatch_dup:
        tasks.append({'name': 'R52RevGR1a', 'agent': 'critic'})  # duplicate seat in the dispatch
    with open(os.path.join(d, 'results.json'), 'w', encoding='utf-8') as fh:
        json.dump({'results': results}, fh)
    with open(os.path.join(d, 'dispatch.json'), 'w', encoding='utf-8') as fh:
        json.dump({'taskCall': {'context': 'fixture', 'tasks': tasks}}, fh)
    skill = '# fixture skill\n\n## Scrub grounding — round 52 admission\n\nfixture.\n'
    readme = ('# fixture readme\n\n## Round 52\n\nThe btrfs scrub grounding entry '
              '`btrfs-scrub-grounding-r45.md` is admitted round 52 on its re-read bytes.\n')
    paths = {}
    for name, text in (('entry.md', entry), ('skill.md', skill), ('readme.md', readme)):
        p = os.path.join(d, name)
        with open(p, 'w', encoding='utf-8') as fh:
            fh.write(text)
        paths[name] = p
    cmd = [sys.executable, C1, '--revision', REV, '--no-base-check',
           '--entry-file', paths['entry.md'], '--skill-file', paths['skill.md'],
           '--readme-file', paths['readme.md'], '--dispatch-file', os.path.join(d, 'dispatch.json'),
           '--results-file', os.path.join(d, 'results.json'), '--wave-dir', wave]
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=WORK)
    try:
        obj = json.loads(p.stdout.strip().split('\n')[-1])
    except Exception:
        obj = {'raw': p.stdout[-400:], 'err': p.stderr[-400:]}
    return p.returncode, obj


def body_plain(row, seat, h):
    cites = ' '.join(f'{f}:{n}' for f, n in CITE[row])
    return (f'Seat {seat} read row {row} on the frozen bytes and finds the statement supported by the '
            f'cited source lines {cites}. The pinned snapshot at each cited number carries the quoted '
            f'form and the surrounding meaning matches. No further condition is outstanding for this row '
            f'and the same reasoning applies to the sibling rows reviewed by the other seats of this wave. '
            f'This body is written by seat {seat} and is distinct from the other reports. ')


def body_mention(row, seat, h):
    """A GR1 report that discusses GR2's verdict line in prose (a legitimate reviewer remark)."""
    b = body_plain(row, seat, h)
    if row == 'GR1':
        b += (' For reference, the neighbouring row was reported as ROW GR2 VERDICT: holds by its own '
              'counted seats, which is quoted here only to show the cross-reading was done.')
    return b


def report(tag, rc, obj):
    print(f'--- {tag}: rc={rc} verdict={obj.get("verdict")} '
          f'verdicts_ok={obj.get("verdicts_ok")} seats_ok={obj.get("seats_ok")} '
          f'lint_ok={obj.get("lint_ok")} marks_ok={obj.get("marks_ok")} '
          f'quotes_ok={obj.get("quotes_ok")} structural_ok={obj.get("structural_ok")}')
    for note in (obj.get('seat_notes') or [])[:6]:
        print('      note:', note)


rc, obj = build('control', body_plain)
report('CONTROL plain 18 reports', rc, obj)
rc, obj = build('mention', body_mention)
report('TEST GR1 body mentions ROW GR2 VERDICT: holds', rc, obj)
rc, obj = build('dupdispatch', body_plain, dispatch_dup=True)
report('TEST dispatch contains R52RevGR1a twice', rc, obj)
