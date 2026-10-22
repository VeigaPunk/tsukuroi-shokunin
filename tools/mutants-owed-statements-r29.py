#!/usr/bin/env python3
"""Should-fail battery for tools/check-owed-statements-r29.py (round 29, claim C1; QUALITY 73).

Origin: round-29 wave-1 seat CritOwedCounterShapes (`.ufo/waves/round-29/w1/CritOwedCounterShapes/
harness.py`); the control builder and the shape list are carried unchanged except for these
labels and one repair: the control's four storage basis pointers (`storage-health-r26.md`
lines 20, 30, 40, 50, all blank) are repointed to the non-blank correction lines 128, 135, 133 and 129,
because counter version 2 refuses a blank cited line.  Made reproducible: the data is a private clone of `--lane` (never the lane itself) under a
fresh temporary directory, checked out at `--base`; the counter is the blob
`<--counter-rev>:tools/check-owed-statements-r29.py` or `--counter-file`, copied into the clone
before every run.  Every git child runs with all inherited GIT_* variables removed.

Shapes: C0 control (all twelve markers in the documented shape; must be 12 of 12); expectation
`fail`, `fail-cleanly` or `refuse-ok` = should-fail (the shape's item must NOT be counted, and the
counter must print its summary line); `pass` = should-pass (the item must be counted).
The last stdout line (JSON) carries `counter_sha256`, `control_marked`, `should_fail_total`,
`should_fail_accepted`, `accepted_shapes`, `should_pass_total`, `should_pass_refused`,
`refused_shapes`, `crashes`.  Exit 0 when control is 12, no should-fail shape is accepted and
there is no crash; 1 otherwise; 2 on a harness error.

Usage: python3 tools/mutants-owed-statements-r29.py --base <REV> (--counter-rev <REV> | --counter-file <PATH>)
       [--lane <repo>] [--keep]
"""
import argparse, atexit, hashlib, json, os, re, shutil, subprocess, sys, tempfile

_ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
_ap.add_argument('--base', required=True)
_g = _ap.add_mutually_exclusive_group(required=True)
_g.add_argument('--counter-rev')
_g.add_argument('--counter-file')
_ap.add_argument('--lane', default=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_ap.add_argument('--keep', action='store_true')
ARGS = _ap.parse_args()
ENV = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
_parent = '/fast/scratch/hyaku' if os.path.isdir('/fast/scratch/hyaku') else None
SEAT = tempfile.mkdtemp(prefix='mut-owed-', dir=_parent)
if not ARGS.keep:
    atexit.register(shutil.rmtree, SEAT, True)
REPO = os.path.join(SEAT, 'repo')
subprocess.run(['git', 'clone', '-q', '--no-local', ARGS.lane, REPO], check=True, env=ENV, capture_output=True)
BASE = subprocess.run(['git', '-C', REPO, 'rev-parse', '--verify', ARGS.base + '^{commit}'], check=True,
                      env=ENV, capture_output=True, text=True).stdout.strip()
if ARGS.counter_file:
    COUNTER = open(ARGS.counter_file, 'rb').read()
else:
    COUNTER = subprocess.run(['git', '-C', ARGS.lane, 'show', ARGS.counter_rev + ':tools/check-owed-statements-r29.py'],
                             check=True, env=ENV, capture_output=True).stdout
COUNTER_SHA = hashlib.sha256(COUNTER).hexdigest()
COUNTER_PATH = os.path.join(SEAT, 'counter', 'check-owed-statements-r29.py')
os.makedirs(os.path.dirname(COUNTER_PATH))
open(COUNTER_PATH, 'wb').write(COUNTER)

def git(*a):
    p = subprocess.run(['git', '-C', REPO, '-c', 'user.name=shape', '-c', 'user.email=shape@sandbox', *a],
                       capture_output=True, text=True, env=ENV)
    if p.returncode:
        raise SystemExit(f'git {a} failed: {p.stderr}')
    return p.stdout.strip()

def rd(p):
    return open(os.path.join(REPO, p), encoding='utf-8').read()

def wr(p, s):
    open(os.path.join(REPO, p), 'w', encoding='utf-8').write(s)

def counter():
    p = subprocess.run([sys.executable, COUNTER_PATH,
                        '--revision', 'HEAD', '--lane', REPO], capture_output=True, text=True, env=ENV)
    rows = {}
    summary = None
    for ln in p.stdout.splitlines():
        try:
            d = json.loads(ln)
        except ValueError:
            continue
        if 'id' in d:
            rows[d['id']] = d
        else:
            summary = d
    return p.returncode, rows, summary, p.stderr.strip().splitlines()[-1:] if p.stderr.strip() else []

OOM, KILL = 'corpus/knowledge/oom-event-plane.md', 'corpus/knowledge/kill-event-deep-r8.md'
SKILL, DRV = 'SKILL.md', 'corpus/knowledge/driver-firmware-plane.md'
MP, SH = 'corpus/knowledge/memory-pressure-r25.json', 'corpus/knowledge/storage-health-r26.json'
ANCH = {
    'O01': 'exactly the band the kernel scans first',
    'O02': 'the +200 band is chosen first',
    'O03': 'under a kernel OOM the scan prefers the higher-scored, larger-RSS tasks first',
    'O04': 'the +200 band is scanned first',
    'O05': 'so nothing in that chain is monitored',
    'O06': "Enabling the unit would still monitor nothing while every unit stays 'auto'",
    'O07': "systemd-oomd monitors only cgroups whose units carry 'kill'.",
    'O08': 'the loaded module is not re-identified by modinfo [unk]',
    'O09': 'under shorter names (write_errs, read_errs, flush_errs, corruption_errs, generation_errs)',
    'O10': 'systemd sets that attribute on journal files by default',
    'O11': 'No scrub record exists on this host',
    'O12': 'FAILED! otherwise',
}
JROW = {'O06': ('MP4', 'action'), 'O07': ('MP4', 'statement'), 'O09': ('SH1', 'statement'),
        'O10': ('SH3', 'statement'), 'O11': ('SH4', 'statement'), 'O12': ('SH5', 'statement')}
NOW = {
    'O01': 'the kernel walks every eligible task and keeps the highest badness score; no band is visited in order',
    'O02': 'selection compares each task badness score once per pass, so a band is never chosen as a unit first',
    'O03': 'the scan visits tasks in list order and keeps the maximum points value, preferring no task by position',
    'O04': 'oom_badness adds the scaled adjustment to rss and swap pages, and the single maximum across all tasks dies',
    'O05': 'an auto unit below a kill ancestor is still a monitoring candidate, so the chain statement needs that qualifier',
    'O06': 'enabling the unit starts the daemon, which then monitors any cgroup whose ancestor carries kill despite auto',
    'O07': 'the daemon also monitors auto descendants of a kill ancestor and cgroups named through the OOMRules channel',
    'O08': 'the loaded module was later identified from the sysfs version attribute in the round capture at that line',
    'O09': 'the kernel exposes these counters through the device stats ioctl under the long names printed by btrfs device stats',
    'O10': 'systemd-journald sets the no copy on write attribute only on btrfs and only when the journal directory allows it',
    'O11': 'the capture lists no scrub status file under the btrfs state directory, which is absence only for that capture date',
    'O12': 'smartctl prints a failed health verdict and sets an exit status bit, and the literal wording differs by device type',
}
BASIS = {
    'O01': ['S148', 'S149'], 'O02': ['S149'], 'O03': ['S149', 'S148'], 'O04': ['S149'],
    'O05': ['corpus/knowledge/memory-pressure-r25.md:10'],
    'O06': ['S122'], 'O07': ['S122', 'S118'],
    'O08': ['S010', '.ufo/waves/round-17/l1-capture/fresh-capture.txt:38'],
    'O09': ['corpus/knowledge/storage-health-r26.md:128'], 'O10': ['corpus/knowledge/storage-health-r26.md:135'],
    'O11': ['corpus/knowledge/storage-health-r26.md:133'], 'O12': ['corpus/knowledge/storage-health-r26.md:129'],
}
MDFILE = {'O01': OOM, 'O02': OOM, 'O03': KILL, 'O04': KILL, 'O05': SKILL, 'O08': DRV}

def md_marker(iid, verdict='corrected', original=None, now=None, basis=None):
    b = basis if basis is not None else ', '.join(f'`{x}`' if ':' in x else x for x in BASIS[iid])
    return (f'[R29-OWED-{iid}] verdict: {verdict} | original: "{original if original is not None else ANCH[iid]}"'
            f' | now: {now if now is not None else NOW[iid]} | basis: {b}')

def json_marker(iid, **kw):
    row, field = JROW[iid]
    m = {'id': f'R29-OWED-{iid}', 'row': row, 'field': field, 'withdrawn_text': ANCH[iid],
         'verdict': 'corrected', 'now': NOW[iid], 'basis': list(BASIS[iid])}
    m.update(kw)
    return m

def src_row(sid, title, status, used_by, anchor='tag v7.2, line 1'):
    return (f'| {sid} | {title} | code | A | kernel OOM victim selection for the host kernel 7.2.11 | {anchor} | '
            f'teaches the badness walk | {status} | 2026-10-22 | on-release | {used_by} |')

KUSED = f'{OOM}, {KILL}'

def control():
    """Every item marked in the documented shape: must be 12 of 12."""
    s = rd('corpus/SOURCES.md').rstrip('\n').split('\n')
    last = max(i for i, l in enumerate(s) if re.match(r'^\| S\d{3} \|', l))
    s[last + 1:last + 1] = [
        src_row('S148', 'Linux v7.2 Documentation/filesystems/proc.rst', 'mined', KUSED),
        src_row('S149', 'Linux v7.2 mm/oom_kill.c', 'mined', KUSED),
        src_row('S150', 'Linux v7.2 Documentation/admin-guide/sysctl/vm.rst', 'mined', KUSED),
        src_row('S151', 'LWN Taming the OOM killer (2009)', 'rejected', KUSED),
    ]
    wr('corpus/SOURCES.md', '\n'.join(s) + '\n')
    by = {}
    for iid, f in MDFILE.items():
        by.setdefault(f, []).append(md_marker(iid))
    for f, ms in by.items():
        wr(f, rd(f).rstrip('\n') + '\n\n## Round 29 owed-statement corrections\n\n' + '\n'.join(f'- {m}' for m in ms) + '\n')
    for f, ids in ((MP, ('O06', 'O07')), (SH, ('O09', 'O10', 'O11', 'O12'))):
        d = json.loads(rd(f))
        d['corrections_r29'] = [json_marker(i) for i in ids]
        wr(f, json.dumps(d, indent=1, ensure_ascii=False) + '\n')

def md_replace(iid, new_line):
    f = MDFILE[iid]
    t = rd(f)
    old = '- ' + md_marker(iid)
    assert old in t, iid
    wr(f, t.replace(old, new_line))

def json_edit(f, fn):
    d = json.loads(rd(f))
    fn(d)
    wr(f, json.dumps(d, indent=1, ensure_ascii=False) + '\n')

def jm(d, iid):
    return next(c for c in d['corrections_r29'] if c['id'] == f'R29-OWED-{iid}')

def src_edit(sid, fn):
    s = rd('corpus/SOURCES.md').split('\n')
    i = next(i for i, l in enumerate(s) if l.startswith(f'| {sid} |'))
    s[i] = fn(s[i])
    wr('corpus/SOURCES.md', '\n'.join(s))

def drop_anchor_md(f, anchor, repl):
    t = rd(f)
    marker_lines = [l for l in t.split('\n') if '[R29-OWED-' in l]
    body = '\n'.join(l if l in marker_lines else l.replace(anchor, repl) for l in t.split('\n'))
    wr(f, body)

FILLER = 'very ' * 11 + 'true'
SHAPES = [
    # (name, item, expectation, rule a fix needs, mutation)
    ('P1 now is twelve filler words', 'O05', 'fail', 'M5',
     lambda: md_replace('O05', '- ' + md_marker('O05', now=FILLER))),
    ('P2 now is twelve copies of one word (JSON)', 'O10', 'fail', 'M5',
     lambda: json_edit(SH, lambda d: jm(d, 'O10').update(now='x ' * 11 + 'x'))),
    ('P3 now near-duplicates another item now (one word changed)', 'O02', 'fail', 'M5',
     lambda: md_replace('O02', '- ' + md_marker('O02', now=NOW['O01'].replace('every', 'each')))),
    ('P4 now contains the anchor with changed case', 'O04', 'fail', 'M5',
     lambda: md_replace('O04', '- ' + md_marker('O04', now='Indeed ' + ANCH['O04'].upper() + ' and this sentence keeps the withdrawn reading in force'))),
    ('B1 basis S### mined but irrelevant (Stryker row given the target basename)', 'O01', 'fail', 'M6+M7',
     lambda: (src_edit('S146', lambda l: l.rstrip().rstrip('|').rstrip() + f', {OOM} |'),
              md_replace('O01', '- ' + md_marker('O01', basis='S146')))),
    ('B2 kernel item cites a pre-round row (S138 cgroup-v2, opened before round 29) after appending the basename', 'O03', 'fail', 'M7',
     lambda: (src_edit('S138', lambda l: l.rstrip().rstrip('|').rstrip() + f', {KILL} |'),
              md_replace('O03', '- ' + md_marker('O03', basis='S138')))),
    ('B3 used-by names a different file with the same basename', 'O04', 'fail', 'M6',
     lambda: (src_edit('S150', lambda l: l.replace(KUSED, 'corpus/archive/kill-event-deep-r8.md')),
              src_edit('S149', lambda l: l.replace(KUSED, 'corpus/archive/kill-event-deep-r8.md')),
              md_replace('O04', '- ' + md_marker('O04', basis='S150')))),
    ('B4 used-by only mentions the basename in a negation', 'O02', 'fail', 'M6',
     lambda: (src_edit('S150', lambda l: l.replace(KUSED, f'not used by {OOM}')),
              md_replace('O02', '- ' + md_marker('O02', basis='S150')))),
    ('L1 path:LINE at an unrelated line (counter shebang)', 'O05', 'fail', 'M6',
     lambda: md_replace('O05', '- ' + md_marker('O05', basis='`tools/check-owed-statements-r29.py:1`'))),
    ('L2 path:LINE at a blank line', 'O09', 'fail', 'M6',
     lambda: json_edit(SH, lambda d: jm(d, 'O09').update(basis=['SCORECARD.md:1100']))),
    ('L3 path:LINE self-cites the marker line in the target file', 'O08', 'fail', 'M6',
     lambda: md_replace('O08', '- ' + md_marker('O08', basis=f'`{DRV}:{len(rd(DRV).splitlines())}`'))),
    ('L4 kernel item: capture path plus a rejected S151', 'O01', 'refuse-ok', 'M7',
     lambda: md_replace('O01', '- ' + md_marker('O01', basis='S151, `.ufo/waves/round-17/l1-capture/fresh-capture.txt:38`'))),
    ('F1 sole marker inside a fenced code block', 'O08', 'fail', 'M2',
     lambda: md_replace('O08', '```text\n' + md_marker('O08') + '\n```')),
    ('F2 sole marker inside an HTML comment', 'O05', 'fail', 'M2',
     lambda: md_replace('O05', '<!-- ' + md_marker('O05') + ' -->')),
    ('J1 JSON marker row wrong-cased (mp4)', 'O06', 'refuse-ok', 'M3',
     lambda: json_edit(MP, lambda d: jm(d, 'O06').update(row='mp4'))),
    ('J2 JSON row field rewritten, only the anchor substring kept', 'O12', 'fail', 'M1',
     lambda: json_edit(SH, lambda d: next(r for r in d['rows'] if r['id'] == 'SH5').update(statement='FAILED! otherwise'))),
    ('J3 JSON verdict is a list (type confusion)', 'O11', 'fail-cleanly', 'M4',
     lambda: json_edit(SH, lambda d: jm(d, 'O11').update(verdict=['corrected']))),
    ('J4 JSON marker duplicated into the other JSON file', 'O09', 'fail', 'M2',
     lambda: json_edit(MP, lambda d: d['corrections_r29'].append(json_marker('O09')))),
    ('D1 Markdown marker duplicated into another target file', 'O05', 'fail', 'M2',
     lambda: (lambda t: wr(OOM, t + '- ' + md_marker('O05') + '\n'))(rd(OOM))),
    ('D2 O01 marker also placed in kill-event-deep-r8.md', 'O01', 'fail', 'M2',
     lambda: (lambda t: wr(KILL, t + '- ' + md_marker('O01') + '\n'))(rd(KILL))),
    ('W1 O01 marker only in kill-event-deep-r8.md (moved out of its file)', 'O01', 'refuse-ok', 'M2',
     lambda: (md_replace('O01', ''), (lambda t: wr(KILL, t + '- ' + md_marker('O01') + '\n'))(rd(KILL)))),
    ('A1 original statement rewritten; only the marker quote keeps the anchor (Markdown)', 'O02', 'fail', 'M1',
     lambda: drop_anchor_md(OOM, ANCH['O02'], 'the highest-badness task is chosen')),
    ('A2 original statement deleted; only the marker quote keeps the anchor (SKILL.md)', 'O05', 'fail', 'M1',
     lambda: drop_anchor_md(SKILL, ANCH['O05'], '')),
    # should-pass shapes
    ('G1 qualified verdict whose now restates the anchor inside a dated qualifier', 'O11', 'pass', 'M5',
     lambda: json_edit(SH, lambda d: jm(d, 'O11').update(verdict='qualified', now='As of the round-26 capture only, ' + ANCH['O11'] + '; a later scrub would write a status file, so this is dated absence'))),
    ('G2 now quotes the literal tool output that equals the anchor', 'O12', 'pass', 'M5',
     lambda: json_edit(SH, lambda d: jm(d, 'O12').update(now='smartctl -H prints PASSED or the literal FAILED! otherwise, and the exit status bit 3 is the machine-readable verdict'))),
    ('G3 S149 row anchor cell quotes C with || (oom_kill.c style)', 'O02', 'pass', 'M6',
     lambda: (src_edit('S149', lambda l: l.replace('tag v7.2, line 1', 'tag v7.2, line 220: if (adj == OOM_SCORE_ADJ_MIN \\|\\| test_bit(MMF_OOM_SKIP))')),
              md_replace('O02', '- ' + md_marker('O02', basis='S149')))),
    ('G4 now contains a shell pipe', 'O05', 'pass', '-',
     lambda: md_replace('O05', '- ' + md_marker('O05', now='running systemctl show on the ancestor slices | grep ManagedOOM shows an ancestor kill makes auto units candidates'))),
    ('G5 bold marker id', 'O08', 'pass', 'M2',
     lambda: md_replace('O08', '- ' + md_marker('O08').replace('[R29-OWED-O08]', '**[R29-OWED-O08]**'))),
    ('G6 JSON basis as one string (round-27 corrected_by style)', 'O10', 'pass', 'M6',
     lambda: json_edit(SH, lambda d: jm(d, 'O10').update(basis='corpus/knowledge/storage-health-r26.md:135'))),
    ('G7 basis path without an extension', 'O05', 'pass', 'M6',
     lambda: md_replace('O05', '- ' + md_marker('O05', basis='`.ufo/waves/round-24/w2/RevSourcesC/stub/bin/snapper:1`'))),
    ('B5 rejected S151 reads as mined via escaped pipes in its teaches cell', 'O03', 'fail', 'M6',
     lambda: (src_edit('S151', lambda l: l.replace('teaches the badness walk', f'REJECTED \\| mined \\| x \\| y \\| {KILL}')),
              md_replace('O03', '- ' + md_marker('O03', basis='S151')))),
]

# round-29 wave-2 MutOwedV2 survivors (M3 JSON anchor equality, M4 allowlist, M7 opened date)
SHAPES += [
    ('M3a JSON withdrawn_text altered (one word dropped)', 'O06', 'fail', 'M3',
     lambda: json_edit(MP, lambda d: jm(d, 'O06').update(withdrawn_text=ANCH['O06'].replace('still ', '')))),
    ('M4a verdict outside the allowlist (Markdown)', 'O08', 'fail', 'M4',
     lambda: md_replace('O08', '- ' + md_marker('O08', verdict='fixed'))),
    ('M4b verdict outside the allowlist (JSON)', 'O09', 'fail', 'M4',
     lambda: json_edit(SH, lambda d: jm(d, 'O09').update(verdict='withdrawn'))),
    ('M7a kernel item cites a new mined row opened before the round', 'O04', 'fail', 'M7',
     lambda: (src_edit('S150', lambda l: l.replace('| 2026-10-22 |', '| 2026-10-21 |')),
              md_replace('O04', '- ' + md_marker('O04', basis='S150')))),
]

def all_hollow():
    src_edit('S146', lambda l: l.rstrip().rstrip('|').rstrip() + f', {OOM}, {KILL} |')
    for n, iid in enumerate(sorted(ANCH)):
        filler = 'very ' * 11 + f'w{n}'
        basis = 'S146' if iid in ('O01', 'O02', 'O03', 'O04') else '`tools/check-owed-statements-r29.py:1`'
        if iid in MDFILE:
            md_replace(iid, '<!-- ' + md_marker(iid, now=filler, basis=basis) + ' -->')
        else:
            f = MP if iid in ('O06', 'O07') else SH
            json_edit(f, lambda d: jm(d, iid).update(now=filler, basis=['tools/check-owed-statements-r29.py:1']))
    for iid, f in MDFILE.items():
        drop_anchor_md(f, ANCH[iid], '')

SHAPES.append(('X1 all twelve hollow: filler now, irrelevant basis, hidden markers, Markdown originals deleted',
               'O01', 'fail', 'M1+M2+M5+M6+M7', all_hollow))

def main():
    git('checkout', '-q', '-f', BASE)
    control()
    git('commit', '-qam', 'control: all twelve markers in documented shape')
    c0 = git('rev-parse', 'HEAD')
    rc, rows, summ, err = counter()
    res = [{'shape': 'C0 control', 'commit': c0, 'exit': rc, 'marked': summ and summ['marked'],
            'not_ok': {k: v.get('why') for k, v in rows.items() if not v['ok']}}]
    for name, iid, expect, rule, fn in SHAPES:
        git('checkout', '-q', '-f', c0)
        fn()
        git('commit', '-qam', name)
        sha = git('rev-parse', 'HEAD')
        rc, rows, summ, err = counter()
        r = rows.get(iid, {})
        res.append({'shape': name, 'item': iid, 'expect': expect, 'rule': rule, 'commit': sha, 'exit': rc,
                    'marked': summ and summ['marked'], 'item_ok': r.get('ok'), 'why': r.get('why'),
                    'other_not_ok': {k: v.get('why') for k, v in rows.items() if not v['ok'] and k != iid},
                    'stderr_tail': err})
    git('checkout', '-q', '-f', c0)
    for r in res:
        print(json.dumps(r, sort_keys=True))
    sf = [r for r in res[1:] if r['expect'] != 'pass']
    sp = [r for r in res[1:] if r['expect'] == 'pass']
    acc = [r['shape'] for r in sf if r['item_ok'] is True]
    crashes = [r['shape'] for r in res if r['marked'] is None]
    refused = [r['shape'] for r in sp if r['item_ok'] is not True]
    print(json.dumps({'base': BASE, 'counter_sha256': COUNTER_SHA, 'control_marked': res[0]['marked'],
                      'should_fail_total': len(sf), 'should_fail_accepted': len(acc), 'accepted_shapes': acc,
                      'should_pass_total': len(sp), 'should_pass_refused': len(refused),
                      'refused_shapes': refused, 'crashes': crashes}))
    return 0 if res[0]['marked'] == 12 and not acc and not crashes else 1


sys.exit(main())
