#!/usr/bin/env python3
"""seat-harm-log.py — checked per-round tally of seat-to-seat / seat-to-host harm, rounds 37-44.

Read-only. Every row is a JSONL record; nothing here reads /proc, runs a counter or touches the host.

A row stands only if:
  * `round` is inside 37..44 and `id` is unique and shaped R<round>-<...>;
  * `class`, `harm` members and `today` come from the closed vocabularies below;
  * `cite` and `status_cite` are lane-relative `path:line`, the path exists and the line exists;
  * `quote` occurs verbatim on the `cite` line, and `status_quote` on the `status_cite` line;
  * `id_basis:"lesson"` => the id itself occurs on the `cite` line;
  * `id_basis:"minted"` => the id does NOT occur anywhere under corpus/lessons/ (a minted id may not
    reuse a landed one);
  * `today:"closed-able-to-fail"` => `proof_red` and `proof_green` both resolve, in one file, and the
    red line names the old shape (`old`) while the green line names the new one (`new`). The numeric
    comparison on those lines is human-read; what is checked is that the seat cites both shapes.

Usage: python3 seat-harm-log.py --log seat-harm.jsonl [--lane <repo>]
Exit 0 PASS (prints the tally), exit 1 with SH-* findings.
"""
import argparse
import json
import os
import sys

ROUND_MIN, ROUND_MAX = 37, 44
CLASSES = {
    'fleet-root-write', 'process-signal', 'scratch-tmp', 'process-leak',
    'shared-scratch-stray', 'lane-pollution',
}
HARMS = {'fleet-repo', 'other-seat-run', 'host-disk', 'host-process', 'shared-round-root', 'lane-tree'}
TODAY = {'closed-able-to-fail', 'detector-only', 'rule-only', 'open'}
BASIS = {'lesson', 'minted'}


def line_at(lane, cite, findings, code, rid):
    """Resolve lane-relative path:line -> text, or record a finding."""
    if cite.startswith('/') or cite.startswith('/tmp') or cite.startswith('/fast/'):
        findings.append(f'{code}-ABSOLUTE {rid}: {cite}')
        return None
    path, sep, num = cite.rpartition(':')
    if not sep or not num.isdigit():
        findings.append(f'{code}-FORM {rid}: {cite!r} is not path:line')
        return None
    full = os.path.join(lane, path)
    if not os.path.isfile(full):
        findings.append(f'{code}-MISSING {rid}: {path}')
        return None
    try:
        with open(full, encoding='utf-8', errors='replace') as fh:
            lines = fh.read().splitlines()
    except OSError as exc:
        findings.append(f'{code}-UNREADABLE {rid}: {path} ({exc})')
        return None
    i = int(num)
    if i < 1 or i > len(lines):
        findings.append(f'{code}-MISSING {rid}: {cite} (file has {len(lines)} lines)')
        return None
    return lines[i - 1]


def load(lane, path):
    with open(path, encoding='utf-8') as fh:
        rows = []
        for n, raw in enumerate(fh, 1):
            if not raw.strip():
                continue
            try:
                rows.append(json.loads(raw))
            except json.JSONDecodeError as exc:
                raise SystemExit(f'SH-JSON log line {n}: {exc}')
    return rows


def lessons_text(lane):
    root = os.path.join(lane, 'corpus', 'lessons')
    blob = []
    for name in sorted(os.listdir(root)):
        if name.endswith('.md'):
            with open(os.path.join(root, name), encoding='utf-8', errors='replace') as fh:
                blob.append(fh.read())
    return '\n'.join(blob)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--log', required=True)
    ap.add_argument('--lane', default=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    a = ap.parse_args()
    lane = a.lane
    rows = load(lane, a.log)
    findings = []
    seen = set()
    landed = None

    for r in rows:
        rid = r.get('id', '<no-id>')
        rnd = r.get('round')
        if not isinstance(rnd, int) or not (ROUND_MIN <= rnd <= ROUND_MAX):
            findings.append(f'SH-ROUND-OUT-OF-WINDOW {rid}: {rnd!r}')
            continue
        if not str(rid).startswith(f'R{rnd}-'):
            findings.append(f'SH-ID-FORMAT {rid}: round {rnd}')
        if rid in seen:
            findings.append(f'SH-ID-DUPLICATE {rid}')
        seen.add(rid)
        if r.get('class') not in CLASSES:
            findings.append(f'SH-CLASS-UNKNOWN {rid}: {r.get("class")!r}')
        bad = [h for h in r.get('harm') or [] if h not in HARMS]
        if not r.get('harm') or bad:
            findings.append(f'SH-HARM-UNKNOWN {rid}: {r.get("harm")!r}')
        if r.get('today') not in TODAY:
            findings.append(f'SH-TODAY-UNKNOWN {rid}: {r.get("today")!r}')
        basis = r.get('id_basis')
        if basis not in BASIS:
            findings.append(f'SH-ID-BASIS {rid}: {basis!r}')

        cite_line = line_at(lane, r.get('cite', ''), findings, 'SH-CITE', rid)
        if cite_line is not None:
            if r.get('quote') and r['quote'] not in cite_line:
                findings.append(f'SH-CITE-QUOTE {rid}: quote not on {r.get("cite")}')
            if basis == 'lesson' and rid not in cite_line:
                findings.append(f'SH-ID-NOT-ON-LINE {rid}: {r.get("cite")}')
        status_line = line_at(lane, r.get('status_cite', ''), findings, 'SH-STATUS', rid)
        if status_line is not None and r.get('status_quote') and r['status_quote'] not in status_line:
            findings.append(f'SH-STATUS-QUOTE {rid}: quote not on {r.get("status_cite")}')

        if basis == 'minted':
            if landed is None:
                landed = lessons_text(lane)
            if rid in landed:
                findings.append(f'SH-ID-ALREADY-IN-LESSONS {rid}')

        if r.get('today') == 'closed-able-to-fail':
            red, green = r.get('proof_red'), r.get('proof_green')
            if not red or not green:
                findings.append(f'SH-PROOF-MISSING {rid}: closed without proof_red/proof_green')
                continue
            red_line = line_at(lane, red, findings, 'SH-PROOF', rid)
            green_line = line_at(lane, green, findings, 'SH-PROOF', rid)
            if red_line is None or green_line is None:
                continue
            if red.rpartition(':')[0] != green.rpartition(':')[0]:
                findings.append(f'SH-PROOF-FILE {rid}: red and green in different files')
            if 'old' not in red_line.lower():
                findings.append(f'SH-PROOF-QUOTE {rid}: {red} does not name the old shape')
            if 'new' not in green_line.lower():
                findings.append(f'SH-PROOF-QUOTE {rid}: {green} does not name the new shape')

    tally = {}
    classes, harms, todays = {}, {}, {}
    for r in rows:
        tally[r['round']] = tally.get(r['round'], 0) + 1
        classes[r['class']] = classes.get(r['class'], 0) + 1
        todays[r['today']] = todays.get(r['today'], 0) + 1
        for h in r.get('harm') or []:
            harms[h] = harms.get(h, 0) + 1
    print(f'round  incidents  (seat-harm ledger, window {ROUND_MIN}-{ROUND_MAX})')
    for rnd in range(ROUND_MIN, ROUND_MAX + 1):
        ids = [r['id'] for r in rows if r['round'] == rnd]
        print(f'  {rnd}  {len(ids)}' + (f'  {",".join(ids)}' if ids else ''))
    fmt = lambda d: ', '.join(f'{k}={v}' for k, v in sorted(d.items()))
    print('classes:', fmt(classes))
    print('harms:  ', fmt(harms))
    print('today:  ', fmt(todays))
    print('open:   ', ','.join(r['id'] for r in rows if r['today'] == 'open') or '-')
    if findings:
        for f in findings:
            print('FAIL ' + f)
        print(f'FAIL: rows={len(rows)} findings={len(findings)}')
        return 1
    print(f'PASS: rows={len(rows)} findings=0')
    return 0


if __name__ == '__main__':
    sys.dont_write_bytecode = True
    raise SystemExit(main())
