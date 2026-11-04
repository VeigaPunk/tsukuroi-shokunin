#!/usr/bin/env python3
"""ExecRows independent re-derivation of C1 (round 81). Read-only.

Re-implements every frozen clause (R1-R7) from the prose in
tools/count-mount-rows-r81.py's header WITHOUT importing or calling it, so the
lane's own counter is checked rather than trusted.

Two coordinate systems are reported for R5:
  * stripped  - the lane instrument's convention: XML tags removed from the
                whole document first (4 embedded newlines vanish, 707 -> 703
                lines), then the row's cited numbers index that list;
  * raw       - the file as stored: tags removed per line only, so line
                numbers are the ones an editor or `sed -n` sees.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

LANE = Path('/home/vgpnk/Projects/shokunin/tsukuroi-shokunin')
SNAP = LANE / '.ufo/waves/round-81/before/src/systemd.mount.xml'
SUMS = LANE / '.ufo/waves/round-81/before/src/SHA256SUMS'
CAPTURE = LANE / '.ufo/waves/round-81/before/host/generator.txt'
NOTE = LANE / 'corpus/knowledge/mount-unit-fstab-plane-r81.json'
REGISTRY = LANE / 'corpus/SOURCES.md'

TAG = re.compile(r'<[^>]*>')
KINDS = {'spec', 'docs', 'paper', 'code', 'tool', 'dataset', 'talk', 'book', 'community'}


def norm(s):
    return re.sub(r'\s+', ' ', s).strip()


def locate(lines, a, b, quote):
    if not (1 <= a <= b <= len(lines)):
        return False, '<range out of bounds: %d-%d of %d>' % (a, b, len(lines))
    span = norm(' '.join(lines[a - 1:b]))
    return norm(quote) in span, span


def registry(text):
    out = {}
    for line in text.splitlines():
        if not re.match(r'^\s{0,3}\|\s*S[0-9]{3,}\s*\|', line):
            continue
        cells = [c.strip() for c in line.split('|')[1:-1]]
        if len(cells) == 11:
            out[cells[0]] = {'kind': cells[2], 'tier': cells[3]}
    return out


def main():
    raw_text = SNAP.read_text(encoding='utf-8')
    raw_lines = raw_text.splitlines()
    stripped = TAG.sub('', raw_text).splitlines()
    perline = [TAG.sub('', l) for l in raw_lines]
    drift = len(raw_lines) - len(stripped)
    sha = hashlib.sha256(SNAP.read_bytes()).hexdigest()
    sums = {}
    for line in SUMS.read_text().splitlines():
        p = line.split()
        if len(p) == 2:
            sums[p[1]] = p[0]
    note = json.loads(NOTE.read_text())
    reg = registry(REGISTRY.read_text())
    cap = CAPTURE.read_text().splitlines()

    print('snapshot_path %s' % SNAP)
    print('snapshot_sha256_observed %s' % sha)
    print('snapshot_sha256_declared_SHA256SUMS %s' % sums.get('systemd.mount.xml'))
    print('snapshot_sha256_declared_entry %s' % note.get('snapshot_sha256'))
    print('raw_lines %d  tag_stripped_lines %d  drift %d' % (len(raw_lines), len(stripped), drift))
    print('capture_path %s lines %d' % (CAPTURE, len(cap)))
    print('rows %d' % len(note['rows']))
    print()
    print('COORDINATE NOTE: every row below cites numbers that index the tag-stripped')
    print('list (707-line file -> 703-line list). raw = stripped + 2 for all eight')
    print('ranges, because two multi-line tags (DOCTYPE raw 2-3, ulink raw 84-85)')
    print('each swallow one newline before any cited line.')
    print()

    verified = 0
    measured = 0
    settings = set()
    verdicts = []
    for i, row in enumerate(note['rows'], 1):
        why = []
        rid = row.get('id')
        if rid != 'MT%d' % i:
            why.append('R1-id')
        st = str(row.get('statement') or '')
        if len(st.split()) < 12 or '|' in st:
            why.append('R2-statement')
        src = str(row.get('source') or '')
        ent = reg.get(src)
        if not re.match(r'^S[0-9]{3,}$', src) or ent is None:
            why.append('R3-source-unresolved')
        elif ent['kind'] not in KINDS or ent['kind'] == 'own-work':
            why.append('R3-source-kind')
        a, b = row['lines']
        quote = row['quote']
        hit_s, span_s = locate(stripped, a, b, quote)
        hit_raw, span_raw = locate(perline, a, b, quote)
        if len(norm(quote).split()) > 25 or '|' in norm(quote):
            why.append('R5-quote-shape')
        elif not hit_s:
            why.append('R5-quote-not-located')
        if not row.get('setting') or row['setting'] not in norm(' '.join(stripped)):
            why.append('R6-setting')
        else:
            settings.add(row['setting'])
        leg = row.get('measured')
        legline = 'none'
        if leg:
            ma, mb = leg['lines']
            mhit, mspan = locate(cap, ma, mb, leg['quote'])
            if leg.get('source') != 'S332':
                why.append('R7-measured-source')
            elif not mhit:
                why.append('R7-measured-not-located')
            else:
                measured += 1
            legline = 'S332 :%d-%d located=%s' % (ma, mb, mhit)
        if why:
            verdicts.append('%s FAIL %s' % (rid, ','.join(why)))
        else:
            verified += 1
            verdicts.append('%s PASS' % rid)

        print('== %s  setting=%s  source=%s  cited(stripped)=%d-%d  cited(raw)=%d-%d'
              % (rid, row['setting'], src, a, b, a + 2, b + 2))
        print('   statement (%d words): %s' % (len(st.split()), st))
        print('   quote (%d words): %s' % (len(norm(quote).split()), quote))
        print('   text at stripped[%d-%d] (XML tags stripped):' % (a, b))
        print('     %s' % span_s)
        print('   verbatim after whitespace normalisation: stripped=%s raw=%s' % (hit_s, hit_raw))
        if not hit_raw:
            print('   text at raw[%d-%d] (tags stripped per line):' % (a, b))
            print('     %s' % span_raw)
        print('   measured: %s' % legline)
        print()

    print('independent_totals rows=%d verified=%d measured=%d distinct_settings=%d'
          % (len(note['rows']), verified, measured, len(settings)))
    print('independent_finding %s' % ('met' if (len(note['rows']) == 8 and verified == 8
                                                and measured >= 2 and len(settings) == 8) else 'unmet'))
    for v in verdicts:
        print('verdict %s' % v)
    return 0 if verified == len(note['rows']) else 1


if __name__ == '__main__':
    sys.exit(main())
