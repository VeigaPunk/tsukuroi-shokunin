#!/usr/bin/env python3
"""Falsification probes for tools/check-adjacency-overlap.py.

For each probe, build a fixture lane repository whose register violates one
declared rule (A1..A7), then evaluate it with the pristine tool and with the
mutant tool.  A mutant that turns a pristine rejection into an acceptance has
a real hole in the counter; a mutant that only changes the reported reason is
label-only.
"""
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile

BASE = '/fast/scratch/hyaku/tsuku27a2/MutC2Counter'
PRISTINE = os.path.join(BASE, 'pristine-check-adjacency-overlap.py')
MUTDIR = os.path.join(BASE, 'mut')
SPEC = os.path.join(BASE, 'mutants.json')
FLEET = '/home/vgpnk/Projects/shokunin'
MORI = os.path.join(FLEET, 'mori-shokunin')
PIN_COMMIT = 'ef9dbee136d6ed2ef98687f5cb0c0a16506a5155'
PIN_PATH = 'corpus/knowledge/userspace-oom-killers-r26.md'
SNAP_DIR = '.ufo/waves/round-27/siblings/mori/'
REGISTER = 'corpus/knowledge/adjacency-mori-oom-r27.json'
SECTION = '## Adjacent — mori userspace OOM killers (round 27)'
IDS = tuple('OV%d' % i for i in range(1, 7))

BASE_SNAP = ('# Title\n\nintro line\n## Facts\none fact about units here\nsecond fact line\n'
             'third fact line\n## Limits\nlimit sentence one\n').encode()
LONG = ' '.join(['w'] * 26)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def materialise_mutants():
    spec = json.load(open(SPEC, encoding='utf-8'))
    os.makedirs(MUTDIR, exist_ok=True)
    text = open(PRISTINE, encoding='utf-8').read()
    paths = {}
    for m in spec:
        mut = text.replace(m['old'], m['new'], 1)
        if 'old2' in m:
            mut = mut.replace(m['old2'], m['new2'], 1)
        path = os.path.join(MUTDIR, '%s.py' % m['id'])
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(mut)
        paths[m['id']] = path
    return paths


def build(tmp, register, province, files, snapshots):
    repo = os.path.join(tmp, 'lane')
    os.makedirs(repo)
    subprocess.run(['git', '-C', repo, 'init', '-q'], check=True)
    written = dict(files)
    written[REGISTER] = json.dumps(register)
    written['PROVINCE.md'] = province
    for path, text in written.items():
        full = os.path.join(repo, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, 'w', encoding='utf-8') as fh:
            fh.write(text)
    for path, data in snapshots.items():
        full = os.path.join(repo, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, 'wb') as fh:
            fh.write(data)
    subprocess.run(['git', '-C', repo, 'add', '-A'], check=True)
    subprocess.run(['git', '-C', repo, '-c', 'user.name=t', '-c', 'user.email=t@t',
                    'commit', '-qm', 'fixture'], check=True)
    return repo


def province_text(ids):
    return ('# P\n\n' + SECTION + '\n\n| id | owner |\n|---|---|\n' +
            ''.join('| %s | x |\n' % r for r in ids) + '\n## Other\n')


def base_rows(sha, **over):
    rows = []
    for rid in IDS:
        row = {'id': rid, 'sibling': 'mori', 'sibling_commit': PIN_COMMIT,
               'sibling_path': 'x/entry.md', 'sibling_blob_sha256': sha,
               'heading': '## Facts', 'quote': 'one fact about units', 'quote_line': 5,
               'lane_path': 'corpus/knowledge/note.md', 'lane_quote': 'units are auto',
               'class': 'AGREES', 'owner': 'tsukuroi', 'action': 'record'}
        row.update(over)
        rows.append(row)
    return rows


def evaluate(mod, tmp, register, province, files, snapshots, siblings_root=None):
    repo = build(tmp, register, province, files, snapshots)
    code, out = mod.evaluate(repo, 'HEAD', siblings_root or os.path.join(tmp, 'no-siblings'))
    return code, out


# ------------------------------------------------------------------ probes

def probe_extra_row(tmp, **kw):
    sha = hashlib.sha256(BASE_SNAP).hexdigest()
    rows = base_rows(sha)
    rows.append({'id': 'OV7', 'sibling': 'mori', 'sibling_commit': PIN_COMMIT,
                 'sibling_path': 'x/entry.md', 'sibling_blob_sha256': sha,
                 'heading': '## Facts', 'quote': 'one fact about units', 'quote_line': 5,
                 'lane_path': 'corpus/knowledge/note.md', 'lane_quote': 'units are auto',
                 'class': 'AGREES', 'owner': 'tsukuroi', 'action': 'record'})
    return ({'rows': rows}, province_text(IDS), {'corpus/knowledge/note.md': 'the lane says units are auto here\n'},
            {SNAP_DIR + 'x/entry.md': BASE_SNAP})


def probe_duplicate(tmp, **kw):
    sha = hashlib.sha256(BASE_SNAP).hexdigest()
    rows = base_rows(sha)
    rows[5]['id'] = 'OV1'
    return ({'rows': rows}, province_text(IDS), {'corpus/knowledge/note.md': 'the lane says units are auto here\n'},
            {SNAP_DIR + 'x/entry.md': BASE_SNAP})


def probe_sibling_name(tmp, **kw):
    sha = hashlib.sha256(BASE_SNAP).hexdigest()
    rows = base_rows(sha)
    rows[0]['sibling'] = 'mori2'
    return ({'rows': rows}, province_text(IDS), {'corpus/knowledge/note.md': 'the lane says units are auto here\n'},
            {SNAP_DIR + 'x/entry.md': BASE_SNAP})


def probe_dotdot(tmp, **kw):
    sha = hashlib.sha256(BASE_SNAP).hexdigest()
    rows = base_rows(sha)
    rows[0]['sibling_path'] = 'corpus/knowledge/../../etc/passwd'
    return ({'rows': rows}, province_text(IDS), {'corpus/knowledge/note.md': 'the lane says units are auto here\n'},
            {SNAP_DIR + 'x/entry.md': BASE_SNAP})


def probe_pinned_digest(tmp, **kw):
    tampered = BASE_SNAP + b'tampered\n'
    sha = hashlib.sha256(tampered).hexdigest()
    rows = base_rows(sha, sibling_path=PIN_PATH)
    return ({'rows': rows}, province_text(IDS), {'corpus/knowledge/note.md': 'the lane says units are auto here\n'},
            {SNAP_DIR + PIN_PATH: tampered})


def probe_quote_too_long(tmp, **kw):
    snap = ('# Title\n\nintro line\n## Facts\n' + LONG + '\nsecond fact line\n'
            'third fact line\n## Limits\nlimit sentence one\n').encode()
    sha = hashlib.sha256(snap).hexdigest()
    rows = base_rows(sha, quote=LONG)
    return ({'rows': rows}, province_text(IDS), {'corpus/knowledge/note.md': 'the lane says units are auto here\n'},
            {SNAP_DIR + 'x/entry.md': snap})


def probe_lane_file_missing(tmp, **kw):
    sha = hashlib.sha256(BASE_SNAP).hexdigest()
    rows = base_rows(sha)
    rows[0]['lane_path'] = 'corpus/knowledge/absent.md'
    return ({'rows': rows}, province_text(IDS), {'corpus/knowledge/note.md': 'the lane says units are auto here\n'},
            {SNAP_DIR + 'x/entry.md': BASE_SNAP})


def probe_lane_quote_too_long(tmp, **kw):
    sha = hashlib.sha256(BASE_SNAP).hexdigest()
    rows = base_rows(sha, lane_quote=LONG)
    return ({'rows': rows}, province_text(IDS), {'corpus/knowledge/note.md': 'the lane says ' + LONG + '\n'},
            {SNAP_DIR + 'x/entry.md': BASE_SNAP})


def probe_lane_side_malformed(tmp, **kw):
    sha = hashlib.sha256(BASE_SNAP).hexdigest()
    rows = base_rows(sha)
    rows[0]['lane_quote'] = None
    return ({'rows': rows}, province_text(IDS), {'corpus/knowledge/note.md': 'the lane says units are auto here\n'},
            {SNAP_DIR + 'x/entry.md': BASE_SNAP})


def probe_quote_line_out_of_range(tmp, **kw):
    sha = hashlib.sha256(BASE_SNAP).hexdigest()
    rows = base_rows(sha)
    rows[0]['quote_line'] = 9999
    return ({'rows': rows}, province_text(IDS), {'corpus/knowledge/note.md': 'the lane says units are auto here\n'},
            {SNAP_DIR + 'x/entry.md': BASE_SNAP})


def probe_snapshot_absent(tmp, **kw):
    sha = hashlib.sha256(BASE_SNAP).hexdigest()
    rows = base_rows(sha)
    rows[0]['sibling_path'] = 'x/absent.md'
    return ({'rows': rows}, province_text(IDS), {'corpus/knowledge/note.md': 'the lane says units are auto here\n'},
            {SNAP_DIR + 'x/entry.md': BASE_SNAP})


def probe_province_second_cell(tmp, **kw):
    sha = hashlib.sha256(BASE_SNAP).hexdigest()
    rows = base_rows(sha)
    prov = province_text(IDS).replace('| OV3 | x |', '| x | OV3 |')
    return ({'rows': rows}, prov, {'corpus/knowledge/note.md': 'the lane says units are auto here\n'},
            {SNAP_DIR + 'x/entry.md': BASE_SNAP})


def probe_register_unreadable(tmp, **kw):
    return ('NOT-JSON', province_text(IDS), {'corpus/knowledge/note.md': 'the lane says units are auto here\n'},
            {SNAP_DIR + 'x/entry.md': BASE_SNAP})


def probe_register_rows_not_list(tmp, **kw):
    return ({'rows': {'OV1': {}}}, province_text(IDS), {'corpus/knowledge/note.md': 'the lane says units are auto here\n'},
            {SNAP_DIR + 'x/entry.md': BASE_SNAP})


def probe_legit_dotdot_name(tmp, **kw):
    sha = hashlib.sha256(BASE_SNAP).hexdigest()
    rows = base_rows(sha, sibling_path='x..y/entry.md')
    return ({'rows': rows}, province_text(IDS), {'corpus/knowledge/note.md': 'the lane says units are auto here\n'},
            {SNAP_DIR + 'x..y/entry.md': BASE_SNAP})


def probe_sibling_bytes_differ(tmp, **kw):
    other = 'corpus/knowledge/audit-r11.md'
    live = subprocess.run(['git', '-C', MORI, 'cat-file', '-p', '%s:%s' % (PIN_COMMIT, other)],
                          capture_output=True).stdout
    snap = BASE_SNAP
    sha = hashlib.sha256(snap).hexdigest()
    rows = base_rows(sha, sibling_path=other)
    return ({'rows': rows}, province_text(IDS), {'corpus/knowledge/note.md': 'the lane says units are auto here\n'},
            {SNAP_DIR + other: snap})


PROBES = [
    ('P01 extra row OV7 (A1 exactly OV1-OV6)', probe_extra_row, ['M01', 'M33'], None),
    ('P02 duplicate id OV1 (A1 each once)', probe_duplicate, ['M02', 'M37', 'M38'], None),
    ('P03 sibling name mori2 (A2)', probe_sibling_name, ['M03'], None),
    ('P04 sibling_path with a .. segment (A2)', probe_dotdot, ['M06', 'M26'], None),
    ('P05 snapshot bytes tampered at PIN_PATH (A2 pinned digest)', probe_pinned_digest, ['M08'], None),
    ('P06 sibling quote of 26 words inside the window (A4 cap)', probe_quote_too_long, ['M12', 'M13', 'M42'], None),
    ('P07 lane file absent (A5)', probe_lane_file_missing, ['M17'], None),
    ('P08 lane quote of 26 words present in the lane file (A5 cap)', probe_lane_quote_too_long, ['M18'], None),
    ('P09 lane_path set but lane_quote null (A5)', probe_lane_side_malformed, ['M20'], None),
    ('P10 quote_line 9999 (A4)', probe_quote_line_out_of_range, ['M11'], None),
    ('P11 snapshot file absent (A2)', probe_snapshot_absent, ['M25'], None),
    ('P12 PROVINCE id in the second cell (A7 first cell)', probe_province_second_cell, ['M36'], None),
    ('P13 register not valid JSON (exit 2 contract)', probe_register_unreadable, ['M32', 'M41'], None),
    ('P14 register rows not a list (exit 2 contract)', probe_register_rows_not_list, ['M32', 'M41'], None),
    ('P15 legitimate path with .. inside a segment (A2)', probe_legit_dotdot_name, ['M26'], None),
    ('P16 live mori blob differs from the snapshot (A2 cross-check)', probe_sibling_bytes_differ, ['M27'],
     FLEET),
]


def main():
    mutpaths = materialise_mutants()
    out = []
    for name, builder, mutids, siblings_root in PROBES:
        row = {'probe': name, 'mutants': mutids}
        mods = [('pristine', PRISTINE)] + [(mid, mutpaths[mid]) for mid in mutids]
        for label, path in mods:
            mod = load(path, 'probe_%s' % label)
            with tempfile.TemporaryDirectory() as tmp:
                reg, prov, files, snaps = builder(tmp)
                if reg == 'NOT-JSON':
                    repo = build(tmp, {}, prov, files, snaps)
                    with open(os.path.join(repo, REGISTER), 'w', encoding='utf-8') as fh:
                        fh.write('NOT-JSON')
                    subprocess.run(['git', '-C', repo, 'add', '-A'], check=True)
                    subprocess.run(['git', '-C', repo, '-c', 'user.name=t', '-c', 'user.email=t@t',
                                    'commit', '-qm', 'fixture2'], check=True)
                    try:
                        code, res = mod.evaluate(repo, 'HEAD', siblings_root or os.path.join(tmp, 'no-siblings'))
                    except Exception as exc:
                        code, res = 1, {'anchored_rows': None, 'status': 'EXCEPTION',
                                        'finding': '%s: %s' % (type(exc).__name__, exc), 'rows': {}}
                else:
                    try:
                        code, res = evaluate(mod, tmp, reg, prov, files, snaps, siblings_root)
                    except Exception as exc:
                        code, res = 1, {'anchored_rows': None, 'status': 'EXCEPTION',
                                        'finding': '%s: %s' % (type(exc).__name__, exc), 'rows': {}}
            row[label] = {'exit': code, 'anchored': res.get('anchored_rows'),
                          'status': res.get('status'), 'finding': res.get('finding'),
                          'rows': {k: v for k, v in (res.get('rows') or {}).items() if v}}
        out.append(row)
        print(json.dumps(row, ensure_ascii=False), flush=True)
    with open(os.path.join(BASE, 'probe-log.json'), 'w', encoding='utf-8') as fh:
        json.dump(out, fh, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    main()
