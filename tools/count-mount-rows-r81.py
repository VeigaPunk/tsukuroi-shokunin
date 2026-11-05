#!/usr/bin/env python3
# Round-81 C1 finite row counter; its declaration pins the final instrument bytes.
#
# Counts only rows of corpus/knowledge/mount-unit-fstab-plane-r81.json that satisfy every
# frozen clause below. Reads Git objects (--revision), a fixture mirror (--fixture) or a
# hermetic self-built tree (--selftest); creates no file outside a temporary directory that
# honours TMPDIR.
#
# Frozen clauses, per row:
#   R1  id is MT<n>, unique, contiguous from MT1;
#   R2  statement has >= 12 words and contains no pipe;
#   R3  source is a S### that resolves at the same revision to a registry row whose kind is a
#       source kind and is not own-work (QUALITY 86: an own-work row grounds host
#       observations, never a documentation rule);
#   R4  snapshot is named in .ufo/waves/round-81/before/src/SHA256SUMS and its bytes hash to
#       the listed digest (a mismatch is snapshot_tampered, could-not-evaluate, never unmet);
#   R5  quote is <= 25 words, carries no pipe, and is located verbatim (whitespace-normalized,
#       XML tags stripped) inside the snapshot lines the row cites;
#   R6  setting occurs in the snapshot text;
#   R7  a measured leg, when present, names S332 and its measured_quote is located verbatim in
#       .ufo/waves/round-81/before/host/generator.txt at the cited capture lines.
# Target: rows == 8, verified == 8, measured rows >= 2, distinct settings == 8.
#
# Exit: 0 met / 1 unmet / 2 could-not-evaluate / 3 selftest failed.
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
from _revision import bind, clean_env, RevisionError

ROOT = Path(__file__).resolve().parents[1]
NOTE = 'corpus/knowledge/mount-unit-fstab-plane-r81.json'
REGISTRY = 'corpus/SOURCES.md'
SNAPDIR = '.ufo/waves/round-81/before/src'
SUMS = SNAPDIR + '/SHA256SUMS'
CAPTURE = '.ufo/waves/round-81/before/host/generator.txt'
TARGET_ROWS = 8
TARGET_MEASURED = 2
MIN_WORDS = 12
MAX_QUOTE_WORDS = 25
KINDS = {'spec', 'docs', 'paper', 'code', 'tool', 'dataset', 'talk', 'book', 'community'}
OWN_WORK = 'own-work'
ROW_ID = re.compile(r'^MT([1-9][0-9]*)$')
SOURCE_ID = re.compile(r'^S[0-9]{3,}$')
TAG = re.compile(r'<[^>]*>')


class CannotEvaluate(Exception):
    """A pinned input the claim rests on is absent or no longer matches its digest."""

    def __init__(self, finding):
        super().__init__(finding)
        self.finding = finding


def sha(data):
    return hashlib.sha256(data).hexdigest()


def normalize(text):
    return re.sub(r'\s+', ' ', text).strip()


def lines_of(data, name):
    text = data.decode('utf-8', 'replace')
    if name.endswith('.xml'):
        text = TAG.sub('', text)
    return text.splitlines()


def registry_rows(text):
    rows = {}
    for line in text.splitlines():
        if not re.match(r'^\s{0,3}\|\s*S[0-9]{3,}\s*\|', line):
            continue
        cells = [c.strip() for c in line.split('|')[1:-1]]
        if len(cells) != 11:
            continue
        rows[cells[0]] = {'kind': cells[2], 'tier': cells[3], 'source': cells[1]}
    return rows


def locate(lines, a, b, quote):
    if not (1 <= a <= b <= len(lines)):
        return False
    return quote in normalize(' '.join(lines[a - 1:b]))


def verify(read):
    sums = read(SUMS).decode('utf-8', 'replace')
    digests = {}
    for line in sums.splitlines():
        parts = line.split()
        if len(parts) == 2:
            digests[parts[1]] = parts[0]
    if not digests:
        raise CannotEvaluate('snapshot-manifest-empty')
    snapshots = {}
    for name, want in digests.items():
        try:
            data = read(SNAPDIR + '/' + name)
        except OSError:
            raise CannotEvaluate('snapshot-absent')
        if sha(data) != want:
            raise CannotEvaluate('snapshot_tampered')
        snapshots[name] = lines_of(data, name)
    capture = lines_of(read(CAPTURE), 'generator.txt')
    try:
        note = json.loads(read(NOTE))
    except (OSError, subprocess.CalledProcessError):
        return 0, 'note-absent', []
    except ValueError:
        return 0, 'note-invalid', []
    rows = note.get('rows') if isinstance(note, dict) else None
    if not isinstance(rows, list):
        return 0, 'note-invalid', []
    registry = registry_rows(read(REGISTRY).decode('utf-8', 'replace'))
    problems, verified, measured, settings = [], 0, 0, set()
    for index, row in enumerate(rows, 1):
        why = []
        if not isinstance(row, dict):
            problems.append('row-%d-shape' % index)
            continue
        if row.get('id') != 'MT%d' % index:
            why.append('R1-id')
        statement = row.get('statement') or ''
        if len(str(statement).split()) < MIN_WORDS or '|' in str(statement):
            why.append('R2-statement')
        src = str(row.get('source') or '')
        entry = registry.get(src)
        if not SOURCE_ID.match(src) or entry is None:
            why.append('R3-source-unresolved')
        elif entry['kind'] not in KINDS or entry['kind'] == OWN_WORK:
            why.append('R3-source-kind')
        name = row.get('snapshot')
        if name not in snapshots:
            why.append('R4-snapshot-unnamed')
            quote = normalize(str(row.get('quote') or ''))
        else:
            quote = normalize(str(row.get('quote') or ''))
            span = row.get('lines') or []
            if len(quote.split()) > MAX_QUOTE_WORDS or '|' in quote:
                why.append('R5-quote-shape')
            elif not (isinstance(span, list) and len(span) == 2 and all(isinstance(v, int) for v in span)):
                why.append('R5-lines-shape')
            elif not locate(snapshots[name], span[0], span[1], quote):
                why.append('R5-quote-not-located')
        setting = str(row.get('setting') or '')
        if not setting or name not in snapshots or setting not in normalize(' '.join(snapshots[name])):
            why.append('R6-setting')
        else:
            settings.add(setting)
        leg = row.get('measured')
        if leg is not None:
            mquote = normalize(str((leg or {}).get('quote') or ''))
            mspan = (leg or {}).get('lines') or []
            if (leg or {}).get('source') != 'S332':
                why.append('R7-measured-source')
            elif not (isinstance(mspan, list) and len(mspan) == 2 and all(isinstance(v, int) for v in mspan)):
                why.append('R7-measured-lines')
            elif not locate(capture, mspan[0], mspan[1], mquote):
                why.append('R7-measured-not-located')
            elif why:
                pass
            else:
                measured += 1
        if why:
            problems.append('%s:%s' % (row.get('id'), ','.join(why)))
        else:
            verified += 1
    finding = 'met' if (len(rows) == TARGET_ROWS and verified == TARGET_ROWS
                        and measured >= TARGET_MEASURED and len(settings) == TARGET_ROWS) else 'unmet'
    return verified, finding, problems


def selftest():
    cases = []

    def run(name, tree, expect_rc, expect_token):
        proc = subprocess.run([sys.executable, __file__, '--fixture', str(tree)],
                              capture_output=True, text=True, timeout=120)
        body = (proc.stdout or '') + (proc.stderr or '')
        cases.append((name, proc.returncode == expect_rc and expect_token in body,
                      'rc=%d body=%s' % (proc.returncode, body.strip()[:160])))

    base = Path(tempfile.mkdtemp(dir=tempfile.gettempdir(), prefix='mount81-'))
    try:
        def build(dest):
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
                rows.append({'id': 'MT%d' % n,
                             'setting': settings[n - 1],
                             'statement': 'a documented rule statement with more than twelve words in it here',
                             'source': 'S331', 'snapshot': 'systemd.mount.xml', 'lines': [3, 4],
                             'quote': 'With nofail, this mount will be only wanted, not required, by local-fs.target or remote-fs.target.'})
            rows[0]['measured'] = {'source': 'S332', 'lines': [2, 2], 'quote': 'Before=local-fs.target'}
            rows[1]['measured'] = {'source': 'S332', 'lines': [3, 3], 'quote': 'JobRunningTimeoutSec=10s'}
            note = {'url': 'https://example.invalid', 'snapshot': 'systemd.mount.xml',
                    'snapshot_sha256': 'x', 'rows': rows}
            (dest / NOTE).write_text(json.dumps(note))

        good = base / 'good'
        build(good)
        run('met', good, 0, '"finding": "met"')

        bad_quote = base / 'bad-quote'
        build(bad_quote)
        note = json.loads((bad_quote / NOTE).read_text())
        note['rows'][7]['quote'] = 'this sentence is absent from the pinned snapshot text entirely'
        (bad_quote / NOTE).write_text(json.dumps(note))
        run('one-row-unlocated', bad_quote, 1, 'MT8:R5-quote-not-located')

        tampered = base / 'tampered'
        build(tampered)
        (tampered / SNAPDIR / 'systemd.mount.xml').write_text('<para>edited</para>\n')
        run('snapshot-tampered', tampered, 2, 'snapshot_tampered')

        absent = base / 'absent'
        build(absent)
        (absent / NOTE).unlink()
        run('note-absent', absent, 1, 'note-absent')

        no_sums = base / 'no-sums'
        build(no_sums)
        (no_sums / SUMS).unlink()
        run('manifest-absent', no_sums, 2, 'cannot-evaluate')

        own_work = base / 'own-work'
        build(own_work)
        note = json.loads((own_work / NOTE).read_text())
        note['rows'][3]['source'] = 'S332'
        (own_work / NOTE).write_text(json.dumps(note))
        run('own-work-source', own_work, 1, 'MT4:R3-source-kind')

        # Round-82 mutation-gap cases. Each drives the public --fixture path over an
        # isolated tree under TMPDIR and asserts both the exit code and the token.

        # R5 quote <= 25 words (C01): an over-cap quote must fail shape even when located.
        long_quote = base / 'long-quote'
        build(long_quote)
        long_sentence = ('With nofail this mount will be only wanted and not required by '
                         'local-fs.target or remote-fs.target and the unit will still be '
                         'pulled in whenever another unit requires it explicitly through '
                         'a dependency edge')
        xml_path = long_quote / SNAPDIR / 'systemd.mount.xml'
        man = xml_path.read_text() + '<para>\n' + long_sentence + '\n</para>\n'
        xml_path.write_text(man)
        (long_quote / SUMS).write_text(sha(man.encode()) + '  systemd.mount.xml\n')
        note = json.loads((long_quote / NOTE).read_text())
        note['rows'][7]['quote'] = long_sentence
        note['rows'][7]['lines'] = [11, 11]
        (long_quote / NOTE).write_text(json.dumps(note))
        run('quote-over-word-cap', long_quote, 1, 'MT8:R5-quote-shape')

        # R5 quote carries no pipe (C02): a pipe quote must fail shape, not location.
        pipe_quote = base / 'pipe-quote'
        build(pipe_quote)
        note = json.loads((pipe_quote / NOTE).read_text())
        note['rows'][7]['quote'] = 'local-fs.target or | remote-fs.target'
        (pipe_quote / NOTE).write_text(json.dumps(note))
        run('quote-with-pipe', pipe_quote, 1, 'MT8:R5-quote-shape')

        # R2 statement contains no pipe (C03): piped statement fails even at 14 words.
        pipe_stmt = base / 'pipe-statement'
        build(pipe_stmt)
        note = json.loads((pipe_stmt / NOTE).read_text())
        note['rows'][6]['statement'] = 'a documented rule statement with more than twelve words and a pipe | inside'
        (pipe_stmt / NOTE).write_text(json.dumps(note))
        run('statement-with-pipe', pipe_stmt, 1, 'MT7:R2-statement')

        # R1 id is MT<index> contiguous (C04): a duplicated id must be reported.
        dup_id = base / 'duplicate-id'
        build(dup_id)
        note = json.loads((dup_id / NOTE).read_text())
        note['rows'][3]['id'] = 'MT1'
        (dup_id / NOTE).write_text(json.dumps(note))
        run('duplicate-row-id', dup_id, 1, 'MT1:R1-id')

        # R2 statement >= 12 words (C05): a short statement must fail the floor.
        short_stmt = base / 'short-statement'
        build(short_stmt)
        note = json.loads((short_stmt / NOTE).read_text())
        note['rows'][5]['statement'] = 'too short by far'
        (short_stmt / NOTE).write_text(json.dumps(note))
        run('short-statement', short_stmt, 1, 'MT6:R2-statement')

        # Target measured rows >= 2 (C09): no measured legs is unmet, not met.
        no_legs = base / 'no-measured-legs'
        build(no_legs)
        note = json.loads((no_legs / NOTE).read_text())
        del note['rows'][0]['measured']
        del note['rows'][1]['measured']
        (no_legs / NOTE).write_text(json.dumps(note))
        run('no-measured-legs', no_legs, 1, '"finding": "unmet"')

        # Distinct settings == 8 (C10): a duplicated setting is unmet even when located.
        dup_setting = base / 'duplicate-setting'
        build(dup_setting)
        note = json.loads((dup_setting / NOTE).read_text())
        note['rows'][7]['setting'] = 'nofail'
        (dup_setting / NOTE).write_text(json.dumps(note))
        run('duplicate-setting', dup_setting, 1, '"finding": "unmet"')

        # Rows == 8 (C11): a ninth, shape-broken row keeps the count unmet.
        extra_row = base / 'extra-row'
        build(extra_row)
        note = json.loads((extra_row / NOTE).read_text())
        note['rows'].append('not-a-row')
        (extra_row / NOTE).write_text(json.dumps(note))
        run('extra-shape-broken-row', extra_row, 1, 'row-9-shape')

        # locate() span bounds (C14): a span past EOF must not locate.
        past_eof = base / 'span-past-eof'
        build(past_eof)
        note = json.loads((past_eof / NOTE).read_text())
        note['rows'][2]['lines'] = [3, 999]
        (past_eof / NOTE).write_text(json.dumps(note))
        run('span-past-eof', past_eof, 1, 'MT3:R5-quote-not-located')

        # R4 unnamed snapshot reported (C15): a snapshot absent from SHA256SUMS is named.
        unnamed = base / 'unnamed-snapshot'
        build(unnamed)
        note = json.loads((unnamed / NOTE).read_text())
        note['rows'][3]['snapshot'] = 'ghost.xml'
        (unnamed / NOTE).write_text(json.dumps(note))
        run('unnamed-snapshot', unnamed, 1, 'MT4:R4-snapshot-unnamed')

        # Empty SHA256SUMS is could-not-evaluate (C16), never an unmet verdict.
        empty_sums = base / 'empty-manifest'
        build(empty_sums)
        (empty_sums / SUMS).write_text('')
        run('empty-manifest', empty_sums, 2, 'snapshot-manifest-empty')

        # R6 setting occurs in the snapshot (C17): an absent setting is reported.
        absent_setting = base / 'absent-setting'
        build(absent_setting)
        note = json.loads((absent_setting / NOTE).read_text())
        note['rows'][4]['setting'] = 'x-systemd.noswap='
        (absent_setting / NOTE).write_text(json.dumps(note))
        run('setting-absent-from-snapshot', absent_setting, 1, 'MT5:R6-setting')

        # R7 measured leg names S332 (C18): another source must be reported.
        wrong_leg = base / 'wrong-measured-source'
        build(wrong_leg)
        note = json.loads((wrong_leg / NOTE).read_text())
        note['rows'][2]['measured'] = {'source': 'S999', 'lines': [2, 2],
                                       'quote': 'Before=local-fs.target'}
        (wrong_leg / NOTE).write_text(json.dumps(note))
        run('measured-wrong-source', wrong_leg, 1, 'MT3:R7-measured-source')
    finally:
        shutil.rmtree(base, ignore_errors=True)
    failed = [c for c in cases if not c[1]]
    print('SELFTEST total=%d passed=%d failed=%d' % (len(cases), len(cases) - len(failed), len(failed)))
    for name, ok, detail in cases:
        if not ok:
            print('FAIL %s %s' % (name, detail))
    return 0 if not failed else 3


def main():
    p = argparse.ArgumentParser(description=__doc__)
    group = p.add_mutually_exclusive_group()
    group.add_argument('--revision')
    group.add_argument('--fixture', type=Path)
    p.add_argument('--selftest', action='store_true')
    a = p.parse_args()
    if a.selftest:
        return selftest()
    if not (a.revision or a.fixture):
        p.error('--revision or --fixture or --selftest required')
    try:
        revision = bind(ROOT, a.revision, 'master').sha if a.revision else 'fixture'

        def read(path):
            if a.fixture:
                return (a.fixture / path).read_bytes()
            return subprocess.run(['git', '-C', str(ROOT), 'show', revision + ':' + path],
                                  env=clean_env(), check=True, capture_output=True).stdout

        try:
            count, finding, problems = verify(read)
        except CannotEvaluate as exc:
            print(json.dumps({'claim': 'C1', 'revision': revision, 'count': 0, 'target': TARGET_ROWS,
                              'finding': exc.finding, 'problems': []}))
            return 2
        except (subprocess.CalledProcessError, OSError) as exc:
            print(json.dumps({'claim': 'C1', 'revision': revision, 'count': 0, 'target': TARGET_ROWS,
                              'finding': 'cannot-evaluate:' + type(exc).__name__, 'problems': []}))
            return 2
        print(json.dumps({'claim': 'C1', 'revision': revision, 'count': count, 'target': TARGET_ROWS,
                          'finding': finding, 'problems': problems}))
        return 0 if finding == 'met' else 1
    except RevisionError as exc:
        print(str(exc))
        return 2


if __name__ == '__main__':
    sys.exit(main())
