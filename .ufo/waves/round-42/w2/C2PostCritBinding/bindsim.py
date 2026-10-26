"""Reproduce the frozen counter's bound() (tools/check-scrub-record-r42.py:120-137) over the real w2 reports,
with a synthetic results record, to classify report-side binding risk. Read-only; no counter run, no lane write."""
import json, pathlib, re, sys

LANE = pathlib.Path('/home/vgpnk/Projects/shokunin/tsukuroi-shokunin')
WAVE = '.ufo/waves/round-42'
VERDICT_RE = re.compile(r'ROW (SC\d) VERDICT: (holds|partly|fails)\b')   # counter:66, verbatim

disp = json.loads((LANE / WAVE / 'w2-dispatch.json').read_text())
tasks = (disp.get('taskCall') or {}).get('tasks') or []

def show(path):
    p = LANE / path
    return p.read_bytes() if p.exists() else None

def bound(results, name, role, row):
    if not any(t.get('name') == name and t.get('agent') == role for t in tasks):
        return None, None, 'not-in-dispatch'
    ent = [r for r in results if r.get('name') == name and r.get('agent') == role]
    if len(ent) != 1 or not isinstance(ent[0].get('output'), str):
        return None, None, f'results-entry-count={len(ent)}'
    hits = [m for m in VERDICT_RE.finditer(ent[0]['output']) if m.group(1) == row]
    if len(hits) != 1:
        return None, None, f'output-hits={len(hits)}'
    line = hits[0].group(0)
    rep = show(f'{WAVE}/w2/{name}.md')
    if rep is None or line not in rep.decode(errors='replace'):
        return None, None, 'report-missing-line'
    return hits[0].group(2), line, 'bound'

SEATS = [(f'C2RevSC{n}', f'SC{n}', 'reviewer') for n in range(1, 6)] + \
        [(f'C2CritSC{n}', f'SC{n}', 'critic') for n in range(1, 6)]
variants = {'V1_firstline': lambda t, first: first,
            'V2_report_text': lambda t, first: t,
            'V3_body_only': lambda t, first: t.split('\n', 1)[1] if '\n' in t else ''}
out = {}
for name, row, role in SEATS:
    p = LANE / WAVE / f'w2/{name}.md'
    if not p.exists():
        out[name] = {'status': 'REPORT-MISSING'}
        continue
    t = p.read_text(errors='replace')
    first = t.split('\n', 1)[0]
    rec = {'first_line': first, 'n_own_hits_in_report': len([m for m in VERDICT_RE.finditer(t) if m.group(1) == row]),
           'n_all_hits_in_report': len(VERDICT_RE.findall(t))}
    for vn, f in variants.items():
        results = [{'name': name, 'agent': role, 'output': f(t, first)}]
        v, ln, why = bound(results, name, role, row)
        rec[vn] = {'verdict': v, 'why': why}
    # naming hazard: results recorded under a retried agent id instead of the seat name
    results = [{'name': name + '-3', 'agent': role, 'output': first}]
    rec['suffixed_results_name'] = {'verdict': bound(results, name, role, row)[0], 'why': bound(results, name, role, row)[2]}
    # duplicate hazard: both the first attempt and the retry report the seat
    results = [{'name': name, 'agent': role, 'output': first}, {'name': name, 'agent': role, 'output': first}]
    rec['duplicate_results'] = {'verdict': bound(results, name, role, row)[0], 'why': bound(results, name, role, row)[2]}
    out[name] = rec
print(json.dumps(out, indent=1))
