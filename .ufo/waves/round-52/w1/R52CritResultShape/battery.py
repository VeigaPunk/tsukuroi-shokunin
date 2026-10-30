#!/usr/bin/env python3
"""W-B3 result/dispatch binding-shape battery for tools/check-scrub-admission-r52.py.

For each synthetic shape, build a dispatch JSON + results JSON + wave-dir report under
scratch, run the counter with --results-file/--dispatch-file/--wave-dir overrides at the
freeze revision, and record how bind_seat treats seat R52RevGR1a (GR1, reviewer).
"""
import json
import os
import subprocess
import sys

SCRATCH = '/fast/scratch/hyaku/tsukuroi-r52/R52CritResultShape/fx'
COUNTER = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-scrub-admission-r52.py'
LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
REV = 'ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0'
SEAT = 'R52RevGR1a'
ROLE = 'reviewer'
ROW = 'GR1'
HASH = '98fa4e07768d240eaf5ea2cce13ce0623fdb756054e5df9f7b9fe68ab2e63987'
# >=300 bytes, exactly two file:line citations, both GR1 row sources that resolve in the
# pinned snapshots; no other CITE_RE-shaped text.
BODY = ("The synthetic control binds this row on the frozen bytes: the scrub entry gate is "
        "cited at scrub.c:1 and the sysfs attribute surface at sysfs.c:1, both resolving in "
        "the pinned snapshots at the freeze revision. Padding follows so the body clears the "
        "three-hundred-byte floor: padding text padding text padding text padding text "
        "padding text padding text padding text padding text padding text padding text "
        "padding text padding text padding text padding text.")
GOLDEN = "ROW GR1 VERDICT: holds\nSECTION SHA256: %s\n%s\n" % (HASH, BODY)
ALL18 = [(f'R52RevGR{n}{x}', 'reviewer') for n in '123' for x in 'abc'] + \
        [(f'R52CritGR{n}{x}', 'critic') for n in '123' for x in 'abc']


def entry(output, name=SEAT, agent=ROLE):
    return {'name': name, 'agent': agent, 'output': output, 'note': None}


def run_shape(tag, *, dispatch=None, results=None, report=GOLDEN, report_bytes=None,
              omit_wave=False):
    d = os.path.join(SCRATCH, tag)
    wd = os.path.join(d, 'wave')
    os.makedirs(wd, exist_ok=True)
    disp = {'schema': 'tsukuroi-wave-dispatch-1', 'wave': 'w1',
            'taskCall': {'context': 'synthetic', 'tasks': dispatch}} if dispatch is not None else \
           {'schema': 'tsukuroi-wave-dispatch-1', 'wave': 'w1',
            'taskCall': {'context': 'synthetic', 'tasks': [{'name': n, 'agent': r} for n, r in ALL18]}}
    res = {'lane': 'tsukuroi', 'round': 52, 'wave': 'w1', 'seats': 18,
           'results': results} if results is not None else \
          {'lane': 'tsukuroi', 'round': 52, 'wave': 'w1', 'seats': 18,
           'results': [entry('done')]}
    dp, rp = os.path.join(d, 'dispatch.json'), os.path.join(d, 'results.json')
    with open(dp, 'w') as fh:
        json.dump(disp, fh)
    with open(rp, 'w') as fh:
        json.dump(res, fh)
    if not omit_wave:
        raw = report_bytes if report_bytes is not None else report.encode('utf-8')
        with open(os.path.join(wd, SEAT + '.md'), 'wb') as fh:
            fh.write(raw)
    cmd = [sys.executable, COUNTER, '--revision', REV, '--lane', LANE,
           '--results-file', rp, '--dispatch-file', dp, '--wave-dir', wd]
    p = subprocess.run(cmd, capture_output=True, stdin=subprocess.DEVNULL)
    try:
        out = json.loads(p.stdout.decode())
    except Exception:
        out = {'error': 'unparseable', 'stdout': p.stdout.decode()[:400], 'stderr': p.stderr.decode()[:400]}
    seat = (out.get('per_row') or {}).get(ROW, {}).get('seats', {}).get(SEAT)
    credited = (out.get('per_row') or {}).get(ROW, {}).get('credited')
    with open(os.path.join(d, 'counter-out.json'), 'w') as fh:
        fh.write(p.stdout.decode())
    rec = {'shape': tag, 'exit': p.returncode, 'counter_verdict': out.get('verdict'),
           'seats_ok': out.get('seats_ok'), 'verdicts_ok': out.get('verdicts_ok'),
           'seat': seat, 'credited': credited}
    with open(os.path.join(d, 'summary.json'), 'w') as fh:
        json.dump(rec, fh, indent=1, sort_keys=True)
    return rec


def main():
    recs = []
    # 0 positive control: golden report, plain non-empty output string
    recs.append(run_shape('s00-golden'))
    # (a1) orchestrator-shaped results entry: output is a JSON string carrying the verdict
    a1 = json.dumps({'report': f'.ufo/waves/round-52/w1/{SEAT}.md', 'verdict': 'holds'}, indent=1)
    recs.append(run_shape('s01-output-json-string', results=[entry(a1)]))
    # (a2) report file itself is the JSON-wrapped verdict
    recs.append(run_shape('s02-report-json-wrapped',
                          report='{"report": "seat", "verdict": "holds"}\n' + GOLDEN))
    # (a3) report first line is a bare JSON string of the verdict
    recs.append(run_shape('s03-report-json-string',
                          report='"ROW GR1 VERDICT: holds"\nSECTION SHA256: %s\n%s\n' % (HASH, BODY)))
    # (b) preamble line before the verdict line
    recs.append(run_shape('s04-preamble',
                          report='Reading GR1 against pinned bytes.\n' + GOLDEN))
    # (c) two results entries for the same seat (identical)
    recs.append(run_shape('s05-two-entries', results=[entry('done'), entry('done')]))
    # (d1) dispatch=reviewer, results=critic
    recs.append(run_shape('s06-disp-rev-res-crit', results=[entry('done', agent='critic')]))
    # (d2) dispatch=critic, results=reviewer
    recs.append(run_shape('s07-disp-crit-res-rev',
                          dispatch=[{'name': SEAT, 'agent': 'critic'}], results=[entry('done')]))
    # (d3) dispatch omits the seat entirely
    recs.append(run_shape('s08-dispatch-omits',
                          dispatch=[{'name': n, 'agent': r} for n, r in ALL18 if n != SEAT]))
    # (e1) empty output string in results
    recs.append(run_shape('s09-empty-output', results=[entry('')]))
    # (e2) empty report file
    recs.append(run_shape('s10-empty-report', report_bytes=b''))
    # (f) trailing space after holds on line 1
    recs.append(run_shape('s11-trailing-space',
                          report='ROW GR1 VERDICT: holds \nSECTION SHA256: %s\n%s\n' % (HASH, BODY)))
    # (g) contradicting verdict line in the body
    recs.append(run_shape('s12-contradicting-body',
                          report=GOLDEN + 'A stray bound line: ROW GR2 VERDICT: holds\n'))
    # (h) results output is a JSON object, not a string
    recs.append(run_shape('s13-output-json-object',
                          results=[entry({'report': 'seat', 'verdict': 'holds'})]))
    # (i) CRLF line endings in the report
    recs.append(run_shape('s14-crlf',
                          report=GOLDEN.replace('\n', '\r\n')))
    # (j) dispatch lists the seat twice with different agents (last wins?)
    recs.append(run_shape('s15-dispatch-dup-seat',
                          dispatch=[{'name': SEAT, 'agent': 'critic'},
                                    {'name': SEAT, 'agent': 'reviewer'}]
                                   + [{'name': n, 'agent': r} for n, r in ALL18 if n != SEAT]))
    # (k) hash line missing (verdict then blank then body)
    recs.append(run_shape('s16-missing-hash',
                          report='ROW GR1 VERDICT: holds\n\n%s\n' % BODY))
    for r in recs:
        s = r['seat'] or {}
        print('%-24s exit=%d seat_verdict=%-7s credited=%-5s detail=%s' % (
            r['shape'], r['exit'], s.get('verdict'),
            (r['credited'] is not None and SEAT in r['credited']), s.get('detail')))


if __name__ == '__main__':
    main()
