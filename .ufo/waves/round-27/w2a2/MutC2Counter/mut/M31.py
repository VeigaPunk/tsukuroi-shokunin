#!/usr/bin/env python3
"""Count anchored rows of the round-27 mori overlap register (claim C2).

Rule (SCORECARD.md, "Round 27 — declaration, attempt 1"), every input read
through git at --revision:

  A1 corpus/knowledge/adjacency-mori-oom-r27.json holds exactly the ids OV1 to
     OV6, each once (a duplicate id is an error and never a second count)
  A2 sibling is `mori`, sibling_commit is the pinned mori commit, sibling_path
     is non-empty, and the committed snapshot
     .ufo/waves/round-27/siblings/mori/<sibling_path> has the sha256 written in
     sibling_blob_sha256 (round-27 tightening: and that sha256 is the pinned one)
  A3 heading is a line of the snapshot starting with `#` and is the nearest
     such line at or above quote_line
  A4 the sibling quote has at most 25 words and, whitespace-normalised, is a
     substring of snapshot lines quote_line .. quote_line + 2
  A5 the lane side is lane_path plus lane_quote (at most 25 words, found
     normalised in that lane file at the revision), or both null and only when
     class is LANE-GAP
  A6 class in INBOUND-RESOLVES, INBOUND-DRIFTED, AGREES, CONFLICTS, LANE-GAP;
     owner in mori, tsukuroi, contested; action a non-empty string
  A7 the id is the first cell of a table row inside the PROVINCE.md section
     `## Adjacent — mori userspace OOM killers (round 27)`
When <siblings-root>/mori-shokunin exists, `git cat-file -p <commit>:<path>`
must equal the snapshot bytes (a mismatch fails every row; an absent sibling
repository is reported as `sibling-unavailable` and the snapshot still counts).

Exit 0 when anchored_rows is 6, 1 when fewer, 2 when the register or the
snapshot cannot be read.  Read-only: no working-tree byte is consulted.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile

REGISTER = 'corpus/knowledge/adjacency-mori-oom-r27.json'
SNAP_DIR = '.ufo/waves/round-27/siblings/mori/'
PIN_COMMIT = 'ef9dbee136d6ed2ef98687f5cb0c0a16506a5155'
PIN_PATH = 'corpus/knowledge/userspace-oom-killers-r26.md'
PIN_SHA256 = 'a5368ee7121d2cbe0929dcb65a13144e5d925f942721b8e6557cf6c612b0a29d'
IDS = tuple('OV%d' % i for i in range(1, 7))
CLASSES = ('INBOUND-RESOLVES', 'INBOUND-DRIFTED', 'AGREES', 'CONFLICTS', 'LANE-GAP')
OWNERS = ('mori', 'tsukuroi', 'contested')
SECTION = '## Adjacent — mori userspace OOM killers (round 27)'
MAX_WORDS = 25
DEFAULT_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def norm(text):
    return ' '.join((text or '').split())


def git(repo, *args):
    return subprocess.run(['git', '-C', repo] + list(args), capture_output=True)


def show(repo, rev, path):
    out = git(repo, 'show', '%s:%s' % (rev, path))
    return out.stdout if out.returncode == 0 else None


def province_ids(text):
    ids, inside = set(), False
    for line in text.split('\n'):
        if line.startswith('## ') or line.startswith('# '):
            inside = line.strip() == SECTION
            continue
        if inside and line.startswith('|'):
            cells = [c.strip() for c in line.strip().strip('|').split('|')]
            if cells and cells[0]:
                ids.add(cells[0])
    return ids


def evaluate(repo, rev, siblings_root):
    commit = git(repo, 'rev-parse', '--verify', '--quiet', '%s^{commit}' % rev)
    if commit.returncode != 0:
        return 2, {'status': 'CANNOT_EVALUATE', 'finding': 'revision-invalid', 'revision': rev}
    rev = commit.stdout.decode().strip()
    raw = show(repo, rev, REGISTER)
    if raw is None:
        return 2, {'status': 'CANNOT_EVALUATE', 'finding': 'register-missing', 'revision': rev,
                   'anchored_rows': 0}
    try:
        rows = json.loads(raw.decode('utf-8'))['rows']
        assert isinstance(rows, list)
    except Exception:
        return 2, {'status': 'CANNOT_EVALUATE', 'finding': 'register-unreadable', 'revision': rev,
                   'anchored_rows': 0}
    province = (show(repo, rev, 'PROVINCE.md') or b'').decode('utf-8', 'replace')
    in_province = province_ids(province)
    ids = [r.get('id') if isinstance(r, dict) else None for r in rows]
    sibling_note = 'sibling-unavailable'
    sib_repo = os.path.join(siblings_root, 'mori-shokunin')
    snapshots, result = {}, {}
    for row in rows:
        reasons = []
        if not isinstance(row, dict):
            continue
        rid = row.get('id')
        if rid not in IDS:
            reasons.append('id-unknown')
        elif ids.count(rid) != 1:
            reasons.append('id-duplicate')
        if row.get('sibling') != 'mori':
            reasons.append('sibling-not-mori')
        if row.get('sibling_commit') != PIN_COMMIT:
            reasons.append('sibling-commit-not-pinned')
        spath = row.get('sibling_path')
        snap = None
        if not isinstance(spath, str) or not spath or '..' in spath.split('/'):
            reasons.append('sibling-path-invalid')
        else:
            if spath not in snapshots:
                snapshots[spath] = show(repo, rev, SNAP_DIR + spath)
            snap = snapshots[spath]
            if snap is None:
                reasons.append('snapshot-missing')
            else:
                digest = hashlib.sha256(snap).hexdigest()
                if row.get('sibling_blob_sha256') != digest:
                    reasons.append('snapshot-digest-mismatch')
                if spath == PIN_PATH and digest != PIN_SHA256:
                    reasons.append('snapshot-not-pinned-bytes')
                if os.path.isdir(os.path.join(sib_repo, '.git')) or os.path.isfile(os.path.join(sib_repo, '.git')):
                    live = git(sib_repo, 'cat-file', '-p', '%s:%s' % (PIN_COMMIT, spath))
                    if live.returncode != 0 or live.stdout != snap:
                        reasons.append('sibling-bytes-differ')
                        sibling_note = 'sibling-mismatch'
                    elif sibling_note != 'sibling-mismatch':
                        sibling_note = 'sibling-verified'
        if snap is not None:
            lines = snap.decode('utf-8', 'replace').split('\n')
            ql = row.get('quote_line')
            if not isinstance(ql, int) or isinstance(ql, bool) or not 1 <= ql <= len(lines):
                reasons.append('quote-line-invalid')
            else:
                nearest = next((lines[i] for i in range(ql - 1, -1, -1) if lines[i].startswith('#')), None)
                if nearest is None or row.get('heading') != nearest:
                    reasons.append('heading-not-nearest')
                quote = row.get('quote')
                if not isinstance(quote, str) or not quote.strip():
                    reasons.append('quote-missing')
                else:
                    if len(quote.split()) > MAX_WORDS:
                        reasons.append('quote-too-long')
                    if norm(quote) not in norm(' '.join(lines[ql - 1:ql + 2])):
                        reasons.append('quote-not-in-window')
        lpath, lquote, klass = row.get('lane_path'), row.get('lane_quote'), row.get('class')
        if lpath is None and lquote is None:
            if klass != 'LANE-GAP':
                reasons.append('lane-null-not-gap')
        elif isinstance(lpath, str) and isinstance(lquote, str) and lpath and lquote.strip():
            body = show(repo, rev, lpath)
            if body is None:
                reasons.append('lane-file-missing')
            elif norm(lquote) not in norm(body.decode('utf-8', 'replace')):
                reasons.append('lane-quote-not-found')
            if len(lquote.split()) > MAX_WORDS:
                reasons.append('lane-quote-too-long')
        else:
            reasons.append('lane-side-malformed')
        if klass not in CLASSES:
            reasons.append('class-invalid')
        if row.get('owner') not in OWNERS:
            reasons.append('owner-invalid')
        if not isinstance(row.get('action'), str) or not row.get('action').strip():
            reasons.append('action-empty')
        if rid not in in_province:
            reasons.append('province-row-missing')
        key = rid if isinstance(rid, str) else 'row%d' % len(result)
        result.setdefault(key, []).extend(reasons)
    # A duplicated id never counts (A1); a sibling byte mismatch fails every row.
    anchored = sum(1 for rid in IDS if ids.count(rid) == 1)
    if sibling_note == 'sibling-mismatch':
        anchored = 0
    out = {'revision': rev, 'anchored_rows': anchored, 'expected_rows': len(IDS),
           'sibling_check': sibling_note, 'rows': result,
           'status': 'PASS' if anchored == len(IDS) else 'FAIL'}
    return (0 if anchored == len(IDS) else 1), out


# ------------------------------------------------------------------ selftest

def _fixture(tmp, register, province, snap_bytes, lane_files):
    repo = os.path.join(tmp, 'lane')
    os.makedirs(repo)
    git(repo, 'init', '-q')
    files = dict(lane_files)
    files[REGISTER] = json.dumps(register)
    files['PROVINCE.md'] = province
    for path, text in files.items():
        full = os.path.join(repo, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, 'w', encoding='utf-8') as fh:
            fh.write(text)
    full = os.path.join(repo, SNAP_DIR + 'x/entry.md')
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'wb') as fh:
        fh.write(snap_bytes)
    git(repo, 'add', '-A')
    git(repo, '-c', 'user.name=t', '-c', 'user.email=t@t', 'commit', '-qm', 'fixture')
    return repo


def selftest():
    global PIN_PATH
    snap = ('# Title\n\nintro line\n## Facts\none fact about units here\nsecond fact line\n'
            'third fact line\n## Limits\nlimit sentence one\n').encode()
    sha = hashlib.sha256(snap).hexdigest()
    lane = {'corpus/knowledge/note.md': 'the lane says units are auto here\n'}

    def base():
        rows = []
        for i, rid in enumerate(IDS):
            rows.append({'id': rid, 'sibling': 'mori', 'sibling_commit': PIN_COMMIT,
                         'sibling_path': 'x/entry.md', 'sibling_blob_sha256': sha,
                         'heading': '## Facts', 'quote': 'one fact about units', 'quote_line': 5,
                         'lane_path': 'corpus/knowledge/note.md', 'lane_quote': 'units are auto',
                         'class': 'AGREES', 'owner': 'tsukuroi', 'action': 'record'})
        return {'rows': rows}
    province = '# P\n\n' + SECTION + '\n\n| id | owner |\n|---|---|\n' + \
        ''.join('| %s | x |\n' % r for r in IDS) + '\n## Other\n'

    def mut(fn, prov=None):
        reg = base()
        fn(reg['rows'])
        return reg, (prov if prov is not None else province)
    cases = [
        ('clean', mut(lambda r: None), 0, 6),
        ('duplicate-id', mut(lambda r: r[5].__setitem__('id', 'OV1')), 1, 4),
        ('digest-mismatch', mut(lambda r: r[0].__setitem__('sibling_blob_sha256', 'f' * 64)), 1, 5),
        ('heading-not-nearest', mut(lambda r: r[0].__setitem__('heading', '# Title')), 1, 5),
        ('quote-outside-window', mut(lambda r: r[0].update(quote='limit sentence one')), 1, 5),
        ('quote-too-long', mut(lambda r: r[0].update(quote=' '.join(['w'] * 26))), 1, 5),
        ('lane-quote-missing', mut(lambda r: r[0].update(lane_quote='not in the lane file')), 1, 5),
        ('null-lane-not-gap', mut(lambda r: r[0].update(lane_path=None, lane_quote=None)), 1, 5),
        ('null-lane-gap-ok', mut(lambda r: r[0].update(lane_path=None, lane_quote=None, **{'class': 'LANE-GAP'})), 0, 6),
        ('class-invalid', mut(lambda r: r[0].__setitem__('class', 'MAYBE')), 1, 5),
        ('owner-invalid', mut(lambda r: r[0].__setitem__('owner', 'kagi')), 1, 5),
        ('action-empty', mut(lambda r: r[0].__setitem__('action', ' ')), 1, 5),
        ('commit-not-pinned', mut(lambda r: r[0].__setitem__('sibling_commit', '0' * 40)), 1, 5),
        ('province-row-missing', mut(lambda r: None, province.replace('| OV3 | x |\n', '')), 1, 5),
        ('province-wrong-section', mut(lambda r: None, province.replace(SECTION, '## Adjacent — other')), 1, 0),
        ('row-missing', mut(lambda r: r.pop()), 1, 5),
    ]
    obs, failed = [], 0
    for name, (reg, prov), want_exit, want_rows in cases:
        with tempfile.TemporaryDirectory() as tmp:
            repo = _fixture(tmp, reg, prov, snap, lane)
            code, out = evaluate(repo, 'HEAD', os.path.join(tmp, 'no-siblings'))
        ok = code == want_exit and out.get('anchored_rows') == want_rows
        failed += not ok
        obs.append({'case': name, 'exit': code, 'anchored_rows': out.get('anchored_rows'), 'pass': ok})
    # sibling cross-check mismatch: a fake mori repo whose pinned blob differs
    with tempfile.TemporaryDirectory() as tmp:
        repo = _fixture(tmp, base(), province, snap, lane)
        code, out = evaluate(repo, 'HEAD', os.path.join(tmp, 'sibs'))
        os.makedirs(os.path.join(tmp, 'sibs', 'mori-shokunin'))
        git(os.path.join(tmp, 'sibs', 'mori-shokunin'), 'init', '-q')
        code2, out2 = evaluate(repo, 'HEAD', os.path.join(tmp, 'sibs'))
        ok = code == 0 and out['sibling_check'] == 'sibling-unavailable' and code2 == 1 \
            and out2['anchored_rows'] == 0
        failed += not ok
        obs.append({'case': 'sibling-unavailable-then-mismatch', 'exit': [code, code2], 'pass': ok})
    print(json.dumps({'cases': len(obs), 'failed': failed, 'observations': obs}))
    return 0 if failed == 0 else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--revision')
    g.add_argument('--selftest', action='store_true')
    ap.add_argument('--repo', default=DEFAULT_REPO)
    ap.add_argument('--siblings-root', default='/home/vgpnk/Projects/shokunin')
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    code, out = evaluate(a.repo, a.revision, a.siblings_root)
    print(json.dumps(out, ensure_ascii=False))
    return code


if __name__ == '__main__':
    sys.exit(main())
