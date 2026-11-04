#!/usr/bin/env python3
"""Second detector: does the mutated clause change behaviour on a targeted fixture?

The shipped --selftest is the assigned detector; this probe distinguishes a genuine
coverage gap (clause is behaviour-bearing but untested) from an equivalent mutant
(clause is masked by another clause, so no input can separate it).
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

S = Path('/fast/scratch/hyaku/tsukuroi-r81/MutCounter')
COUNT = 'count-mount-rows-r81.py'
MEASURE = 'measure-round81.py'
NOTE = 'corpus/knowledge/mount-unit-fstab-plane-r81.json'
REGISTRY = 'corpus/SOURCES.md'
SNAPDIR = '.ufo/waves/round-81/before/src'
SUMS = SNAPDIR + '/SHA256SUMS'
CAPTURE = '.ufo/waves/round-81/before/host/generator.txt'


def sha(b):
    import hashlib
    return hashlib.sha256(b).hexdigest()


# ---------- count fixtures ----------
def count_tree(dest):
    src = dest / SNAPDIR
    src.mkdir(parents=True, exist_ok=True)
    (dest / 'corpus/knowledge').mkdir(parents=True, exist_ok=True)
    (dest / '.ufo/waves/round-81/before/host').mkdir(parents=True, exist_ok=True)
    man = ('<refsect1><title>t</title>\n<para>\nWith nofail, this mount will be only wanted, not required, by\n'
           'local-fs.target or remote-fs.target.\n</para>\n<para>\n'
           'noauto auto x-systemd.device-timeout= x-systemd.before= x-systemd.after= '
           'x-systemd.requires= x-systemd.wanted-by=\n</para>\n</refsect1>\n')
    (src / 'systemd.mount.xml').write_text(man)
    (src / 'SHA256SUMS').write_text(sha(man.encode()) + '  systemd.mount.xml\n')
    (dest / CAPTURE).write_text('# capture\nBefore=local-fs.target\nJobRunningTimeoutSec=10s\n')
    registry = ('| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n'
                '|---|---|---|---|---|---|---|---|---|---|---|\n'
                '| S331 | systemd.mount(5) — https://example.invalid | docs | A | t | t | t | mined | 2026-11-04 | on-release | — |\n'
                '| S332 | capture — path | own-work | A | t | t | t | mined | 2026-11-04 | 30d | — |\n')
    (dest / REGISTRY).write_text(registry)
    settings = ['nofail', 'noauto', 'auto', 'x-systemd.device-timeout=',
                'x-systemd.before=', 'x-systemd.after=', 'x-systemd.requires=',
                'x-systemd.wanted-by=']
    rows = []
    for n in range(1, 9):
        rows.append({'id': 'MT%d' % n, 'setting': settings[n - 1],
                     'statement': 'a documented rule statement with more than twelve words in it here',
                     'source': 'S331', 'snapshot': 'systemd.mount.xml', 'lines': [3, 4],
                     'quote': 'With nofail, this mount will be only wanted, not required, by local-fs.target or remote-fs.target.'})
    rows[0]['measured'] = {'source': 'S332', 'lines': [2, 2], 'quote': 'Before=local-fs.target'}
    rows[1]['measured'] = {'source': 'S332', 'lines': [3, 3], 'quote': 'JobRunningTimeoutSec=10s'}
    (dest / NOTE).write_text(json.dumps({'url': 'https://example.invalid', 'snapshot': 'systemd.mount.xml',
                                         'snapshot_sha256': 'x', 'rows': rows}))
    return dest


def load(dest):
    return json.loads((dest / NOTE).read_text())


def store(dest, note):
    (dest / NOTE).write_text(json.dumps(note))


COUNT_CASES = {
    'P01-long-quote': lambda d: (lambda n: (n['rows'][7].update(quote=' '.join(['word'] * 30)), store(d, n)))(load(d)),
    'P02-quote-pipe': lambda d: (lambda n: (n['rows'][7].update(quote='With nofail | this mount'), store(d, n)))(load(d)),
    'P03-statement-pipe': lambda d: (lambda n: (n['rows'][7].update(statement='a documented | rule statement with more than twelve words in it here'), store(d, n)))(load(d)),
    'P04-id-skip': lambda d: (lambda n: (n['rows'][7].update(id='MT9'), store(d, n)))(load(d)),
    'P05-short-statement': lambda d: (lambda n: (n['rows'][7].update(statement='only four words'), store(d, n)))(load(d)),
    'P06-source-shape': lambda d: (lambda n: (n['rows'][7].update(source='S331 '), store(d, n)))(load(d)),
    'P07-own-work': lambda d: (lambda n: (n['rows'][3].update(source='S332'), store(d, n)))(load(d)),
    'P09-no-measured': lambda d: (lambda n: ([r.pop('measured', None) for r in n['rows']], store(d, n)))(load(d)),
    'P10-dup-setting': lambda d: (lambda n: (n['rows'][7].update(setting='nofail'), store(d, n)))(load(d)),
    'P11-nine-rows': lambda d: (lambda n: (n['rows'].append(dict(n['rows'][7], id='MT9', quote='absent text not in the snapshot at all')),
                                           store(d, n)))(load(d)),
    'P14-span-bounds': lambda d: (lambda n: (n['rows'][7].update(lines=[1, 99]), store(d, n)))(load(d)),
    'P15-unnamed-snapshot': lambda d: (lambda n: (n['rows'][7].update(snapshot='nope.xml'), store(d, n)))(load(d)),
    'P16-empty-manifest': lambda d: (d / SUMS).write_text(''),
    'P17-setting-absent': lambda d: (lambda n: (n['rows'][7].update(setting='absent-token'), store(d, n)))(load(d)),
    'P18-measured-source': lambda d: (lambda n: (n['rows'][0]['measured'].update(source='S999'), store(d, n)))(load(d)),
    'P12-note-absent': lambda d: (d / NOTE).unlink(),
    'P13-unmet-row': lambda d: (lambda n: (n['rows'][7].update(quote='absent text not in the snapshot at all'), store(d, n)))(load(d)),
}

COUNT_PROBE = {
    'C01-quote-word-cap': 'P01-long-quote',
    'C02-quote-pipe': 'P02-quote-pipe',
    'C03-statement-pipe': 'P03-statement-pipe',
    'C04-id-contiguity': 'P04-id-skip',
    'C05-statement-word-floor': 'P05-short-statement',
    'C06-source-id-shape': 'P06-source-shape',
    'C07-own-work-rejection': 'P07-own-work',
    'C09-measured-leg-requirement': 'P09-no-measured',
    'C10-distinct-settings': 'P10-dup-setting',
    'C11-row-count-target': 'P11-nine-rows',
    'C12-note-absent-mapping': 'P12-note-absent',
    'C13-exit-code-mapping': 'P13-unmet-row',
    'C14-locate-span-bounds': 'P14-span-bounds',
    'C15-snapshot-unnamed': 'P15-unnamed-snapshot',
    'C16-empty-manifest': 'P16-empty-manifest',
    'C17-setting-presence': 'P17-setting-absent',
    'C18-measured-source': 'P18-measured-source',
}


# ---------- measure fixtures ----------
def good_tool_text():
    src = (S / 'base' / 'measure' / MEASURE).read_text()
    m = re.search(r"good_tool = '''(.*?)'''", src, re.S)
    return m.group(1)


def measure_tree(dest, tool_text, drop=None):
    (dest / 'tools').mkdir(parents=True, exist_ok=True)
    (dest / 'tools/measure-round80.py').write_text(tool_text)
    (dest / 'tools/_revision.py').write_text(
        'class RevisionError(Exception):\n    pass\n\n\n'
        'def bind(*args, **kwargs):\n    raise RevisionError("fixture")\n\n\n'
        'def clean_env():\n    return None\n')
    (dest / '.ufo/waves/round-80/before').mkdir(parents=True, exist_ok=True)
    (dest / 'corpus/knowledge').mkdir(parents=True, exist_ok=True)
    (dest / '.ufo/waves/round-80/w1/ReviewMatrix').mkdir(parents=True, exist_ok=True)
    expected = json.dumps({'settings': ['a'], 'rows': [], 'url': 'u'}).encode()
    (dest / '.ufo/waves/round-80/before/expected.json').write_bytes(expected)
    (dest / '.ufo/waves/round-80/before/systemd.service.xml').write_text('<refsect1><title>t</title></refsect1>\n')
    (dest / 'corpus/knowledge/service-restart-matrix-r80.json').write_bytes(expected)
    (dest / 'corpus/knowledge/service-restart-matrix-r80.md').write_text('c\n')
    (dest / '.ufo/waves/round-80/w1/ReviewMatrix/verdict.json').write_text('{}')
    (dest / 'corpus/SOURCES.md').write_text('')
    if drop:
        (dest / drop).unlink()
    return dest


def table_doc():
    return {'cases': {
        'A-selftest': {'argv': ['--selftest'], 'rc': 0, 'token': 'SELFTEST total=6 passed=6 failed=0'},
        'B-met': {'argv': ['--claim', 'C1', '--fixture', '{work}'], 'rc': 0, 'token': '"met": true'},
        'C-mismatch': {'argv': ['--claim', 'C1', '--fixture', '{work}'], 'rc': 1, 'token': 'matrix-mismatch',
                       'mutations': [{'path': 'corpus/knowledge/service-restart-matrix-r80.json', 'action': 'json-set',
                                      'keys': ['url'], 'value': 'other'}]},
        'D-tampered': {'argv': ['--claim', 'C1', '--fixture', '{work}'], 'rc': 2, 'token': 'snapshot_tampered',
                       'mutations': [{'path': '.ufo/waves/round-80/before/expected.json', 'action': 'write', 'text': '{}'}]},
        'E-absent': {'argv': ['--claim', 'C1', '--fixture', '{work}'], 'rc': 2, 'token': 'snapshot_absent',
                     'mutations': [{'path': '.ufo/waves/round-80/before/systemd.service.xml', 'action': 'unlink'}]},
        'F-noargs': {'argv': [], 'rc': 2, 'token': ''},
    }}


MEASURE_PROBE = {
    'M01-rc-ignored': 'G03-defective',
    'M02-token-ignored': 'G03-defective',
    'M03-table-from-disk': 'G01-good',
    'M04-target-constant': 'G01-good',
    'M05-exit-code-mapping': 'G03-defective',
    'M07-finding-mapping': 'G03-defective',
    'M08-export-absent': 'G08-missing',
}


def run(tool_path, tree, table_path=None):
    argv = [sys.executable, str(tool_path), '--fixture', str(tree)]
    if table_path:
        argv += ['--table', str(table_path)]
    p = subprocess.run(argv, capture_output=True, text=True, timeout=600,
                       env={'PATH': '/usr/bin:/bin', 'TMPDIR': str(S / 'tmp'), 'HOME': str(S)})
    body = ((p.stdout or '') + (p.stderr or '')).strip().replace('\n', ' ')
    return p.returncode, body[:300]


def main():
    out = []
    base = Path(tempfile.mkdtemp(dir=S / 'tmp', prefix='probe-'))
    try:
        # ---- count ----
        for case in sorted(set(COUNT_PROBE.values())):
            t1 = count_tree(base / ('pc-' + case + '-pristine'))
            t2 = count_tree(base / ('pc-' + case + '-mutant'))
            COUNT_CASES[case](t1)
            COUNT_CASES[case](t2)
            pr, pb = run(S / 'base/count' / COUNT, t1)
            for mid, cname in COUNT_PROBE.items():
                if cname != case:
                    continue
                mr, mb = run(S / 'mut/count' / mid / COUNT, t2)
                out.append({'probe': case, 'mutant': mid, 'pristine_rc': pr, 'pristine': pb,
                            'mutant_rc': mr, 'mutant_body': mb,
                            'distinguished': (pr, pb) != (mr, mb)})
                print('%-28s %-26s pristine rc=%d | mutant rc=%d | %s' % (
                    mid, case, pr, mr, 'DISTINGUISHED' if (pr, pb) != (mr, mb) else 'identical'), flush=True)
        # ---- measure ----
        good = good_tool_text()
        broken = good.replace("print(json.dumps({'finding': 'snapshot_absent'})); sys.exit(2)",
                              "print(json.dumps({'finding': 'snapshot_absent'})); sys.exit(1)")
        broken = broken.replace("print(json.dumps({'finding': 'snapshot_tampered'})); sys.exit(2)",
                                "print(json.dumps({'finding': 'snapshot_tampered'})); sys.exit(1)")
        broken = broken.replace("print('SELFTEST total=6 passed=6 failed=0'); sys.exit(0)",
                                "print('SELFTEST total=2 passed=2 failed=0'); sys.exit(0)")
        variants = {'G01-good': (good, None), 'G03-defective': (broken, None),
                    'G08-missing': (good, '.ufo/waves/round-80/before/systemd.service.xml')}
        for pname, (tool_text, drop) in variants.items():
            t1 = measure_tree(base / ('pm-' + pname + '-pristine'), tool_text, drop)
            t2 = measure_tree(base / ('pm-' + pname + '-mutant'), tool_text, drop)
            tbl = t1 / '.ufo/waves/round-81/before/gate-standard-r81.json'
            tbl.parent.mkdir(parents=True, exist_ok=True)
            tbl.write_text(json.dumps(table_doc()))
            (t2 / '.ufo/waves/round-81/before').mkdir(parents=True, exist_ok=True)
            shutil.copy(tbl, t2 / '.ufo/waves/round-81/before/gate-standard-r81.json')
            pr, pb = run(S / 'base/measure' / MEASURE, t1, tbl)
            for mid, cname in MEASURE_PROBE.items():
                if cname != pname:
                    continue
                mr, mb = run(S / 'mut/measure' / mid / MEASURE, t2, tbl)
                out.append({'probe': pname, 'mutant': mid, 'pristine_rc': pr, 'pristine': pb,
                            'mutant_rc': mr, 'mutant_body': mb,
                            'distinguished': (pr, pb) != (mr, mb)})
                print('%-28s %-26s pristine rc=%d | mutant rc=%d | %s' % (
                    mid, pname, pr, mr, 'DISTINGUISHED' if (pr, pb) != (mr, mb) else 'identical'), flush=True)
    finally:
        shutil.rmtree(base, ignore_errors=True)
    (S / 'receipts' / 'probes.json').write_text(json.dumps(out, indent=1))


if __name__ == '__main__':
    sys.dont_write_bytecode = True
    main()
