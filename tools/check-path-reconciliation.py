#!/usr/bin/env python3
"""Reconcile the outside rough round22 path census with retained lane audit findings.

Calibration of two historical counting methods over fixed frozen inputs only. It never
executes the retained outside source cell, never reauthorizes an old event and is not
native runtime enforcement, effects proof or a universal selector theorem.
Exit 0 every fixed cohort explained, 1 unexplained/failed, 2 could not evaluate.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import unicodedata
sys.dont_write_bytecode = True
import _revision

ROOT = Path(__file__).resolve().parents[1]
LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
W23 = '.ufo/waves/round-23'
PINS = W23 + '/frozen/reconciliation-inputs.json'
LEDGER = W23 + '/path-reconciliation.json'
COHORTS = ('build', 'falsify')
SCHEMA = 'tsukuroi-path-reconciliation-v1'
DISPOSITIONS = ('agree', 'selector-normalization', 'unit-difference')
SCOPE = ('Fixed round22 build/falsify cohorts only; explains counting-method differences, never '
         'reauthorizes an event, executes the outside source cell or claims runtime enforcement.')
# Exact bounded outside rule, re-authored from S085 (r22-rough-census.txt), never executed from it.
ROUGH_SUFFIX = re.compile(r':(raw|\d[\d\-+,:]*|-\d+|\d+-)(:raw)?$')
ROUGH_TOOLS = ('read', 'grep', 'glob', 'write')


class Unevaluable(Exception):
    def __init__(self, fid, site):
        super().__init__(fid)
        self.fid, self.site = fid, site


def unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate JSON key')
        result[key] = value
    return result


def strict(raw):
    return json.loads(raw, object_pairs_hook=unique)


def components(tool, args):
    value = str(args.get('path', '')) if isinstance(args, dict) else ''
    return value.split(';') if tool in ('grep', 'glob') else [value]


def rough_event(tool, args, binding):
    """Outside rough rule: one category per event; path stops at its first failing component."""
    if tool == 'bash':
        return 'exec', None
    if tool not in ROUGH_TOOLS:
        return 'unknown', None
    authority = binding['write_paths'] if tool == 'write' else binding['read_paths']
    for index, value in enumerate(components(tool, args)):
        candidate = ROUGH_SUFFIX.sub('', value) if tool in ('read', 'grep') else value
        if candidate not in authority:
            return 'path', index
    return 'clean', None


def _selector_token(token):
    return token in ('raw', 'img', 'conflicts') or all(re.fullmatch(r'\d+(?:[-+]\d*)?|-\d+', part) for part in token.split(','))


def canonical_base(value, selector):
    """Local selector grammar: any order of raw/img/conflicts and line-range tokens after the path."""
    if value == 'skill://godspeed' or not selector or ':' not in value:
        return value
    base, *tokens = value.split(':')
    return base if tokens and all(_selector_token(t) for t in tokens) else value


def _local(path):
    return (path.startswith(LANE + '/') and '\\' not in path
            and not any(unicodedata.category(c) in ('Cc', 'Cf', 'Cs', 'Zl', 'Zp') for c in path)
            and not any(c in path for c in '*?[];:')
            and all(p not in ('', '.', '..') for p in path.split('/')[1:]))


def canonical_event(tool, args, binding):
    """Indices of path-denied components under literal v1 authority; fetch spellings are a separate class."""
    if tool not in ROUGH_TOOLS or not isinstance(args, dict):
        return []
    authority = binding['write_paths'] if tool == 'write' else binding['read_paths']
    bad = []
    for index, value in enumerate(components(tool, args)):
        if re.match(r'(?i)^https?://', value) or re.match(r'^[^/:\s]+:[0-9]+/', value):
            continue
        base = canonical_base(value, tool in ('read', 'grep'))
        if base == 'skill://godspeed' and base in authority:
            continue
        if not _local(base) or base not in authority:
            bad.append(index)
    return bad


def derive(wave, events, bindings, audit):
    """Reproducible per-event ledger for one cohort; raises Unevaluable on malformed inputs."""
    try:
        ev, bd, au = (strict(x) if isinstance(x, (str, bytes)) else x for x in (events, bindings, audit))
        bound = {s['name']: s for s in bd['seats']}
        if len(bound) != len(bd['seats']):
            raise ValueError('duplicate binding seat')
        retained = {}
        for finding in au['findings']:
            if finding['id'] == 'SCOPE-PATH-DENIED':
                retained[finding['site']] = retained.get(finding['site'], 0) + 1
        rows, seen_sites, names = [], set(), set()
        for seat in ev['seats']:
            name = seat['name']
            if name in names or name not in bound:
                raise ValueError('event roster identity')
            names.add(name)
            for index, event in enumerate(seat['events']):
                tool, args = event['tool'], event.get('args') or {}
                site = f'{name}:{index}'
                seen_sites.add(site)
                category, first_bad = rough_event(tool, args, bound[name])
                canonical = canonical_event(tool, args, bound[name])
                kept = retained.get(site, 0)
                rough_count = int(category == 'path')
                if rough_count == len(canonical) == kept:
                    disposition = 'agree'
                elif (rough_count == 1 and kept == 0 and not canonical and tool in ('read', 'grep')
                      and ROUGH_SUFFIX.sub('', components(tool, args)[first_bad]) != canonical_base(components(tool, args)[first_bad], True)):
                    disposition = 'selector-normalization'
                elif rough_count == 1 and kept == len(canonical) > 1 and first_bad == canonical[0]:
                    disposition = 'unit-difference'
                else:
                    disposition = 'unexplained'
                rows.append({
                    'site': site, 'tool': tool, 'call_id': event.get('call_id'),
                    'request_arguments_sha256': event.get('request_arguments_sha256'),
                    'rough_category': category, 'rough_first_bad': first_bad, 'rough_path_count': rough_count,
                    'canonical_bad': canonical, 'canonical_path_count': len(canonical),
                    'retained_path_count': kept, 'disposition': disposition,
                })
        orphans = sorted(set(retained) - seen_sites)
        if set(bound) != names:
            raise ValueError('binding roster not covered by events')
    except Unevaluable:
        raise
    except (ValueError, TypeError, KeyError, AttributeError, IndexError) as exc:
        raise Unevaluable('RECONCILIATION-INPUT-MALFORMED', f'{wave}:{type(exc).__name__}')
    totals = {
        'rough_path': sum(r['rough_path_count'] for r in rows),
        'canonical_path': sum(r['canonical_path_count'] for r in rows),
        'retained_path': sum(r['retained_path_count'] for r in rows) + sum(retained[s] for s in orphans),
        'events': len(rows),
    }
    for name in DISPOSITIONS + ('unexplained',):
        totals[name] = sum(r['disposition'] == name for r in rows)
    return {'wave': wave, 'rows': rows, 'orphan_retained_sites': orphans, 'totals': totals}


def cohort_findings(wave, derived, recorded, expected):
    findings = []
    def add(fid, site):
        findings.append({'id': fid, 'site': f'{wave}:{site}'})
    totals = derived['totals']
    if derived['orphan_retained_sites']:
        add('RECONCILIATION-ORPHAN-FINDING', derived['orphan_retained_sites'][0])
    if totals['rough_path'] != expected['rough_as_reported']:
        add('RECONCILIATION-ROUGH-COUNT', f"{totals['rough_path']}!={expected['rough_as_reported']}")
    if totals['retained_path'] != expected['lane_retained']:
        add('RECONCILIATION-RETAINED-COUNT', f"{totals['retained_path']}!={expected['lane_retained']}")
    if totals['canonical_path'] != totals['retained_path']:
        add('RECONCILIATION-CANONICAL-MISMATCH', f"{totals['canonical_path']}!={totals['retained_path']}")
    unit_extra = sum(r['retained_path_count'] - 1 for r in derived['rows'] if r['disposition'] == 'unit-difference')
    if totals['rough_path'] - totals['retained_path'] != totals['selector-normalization'] - unit_extra:
        add('RECONCILIATION-ARITHMETIC', 'totals')
    for row in derived['rows']:
        if row['disposition'] == 'unexplained':
            add('RECONCILIATION-UNEXPLAINED', row['site'])
    if recorded != derived:
        add('RECONCILIATION-LEDGER-MISMATCH', 'ledger')
    return findings


def evaluate(pins_raw, files, ledger_raw):
    """files: repo path -> bytes (or None). Returns (code, payload)."""
    base = {'reconciliation_mode': 1, 'scope': SCOPE}
    try:
        pins = strict(pins_raw)
        if pins.get('schema') != 'tsukuroi-reconciliation-inputs-v1' or set(pins['expected']) != set(COHORTS):
            raise ValueError('pins schema')
        for path, digest in pins['inputs'].items():
            data = files.get(path)
            if data is None:
                return 2, dict(base, status='CANNOT_EVALUATE', unexplained_cohorts=None, findings=[{'id': 'SNAPSHOT-MISSING', 'site': path}])
            if hashlib.sha256(data).hexdigest() != digest:
                return 2, dict(base, status='CANNOT_EVALUATE', unexplained_cohorts=None, findings=[{'id': 'SNAPSHOT-TAMPERED', 'site': path}])
    except (ValueError, TypeError, KeyError, AttributeError):
        return 2, dict(base, status='CANNOT_EVALUATE', unexplained_cohorts=None, findings=[{'id': 'RECONCILIATION-PINS', 'site': PINS}])
    if ledger_raw is None:
        return 1, dict(base, status='FAIL', unexplained_cohorts=len(COHORTS), findings=[{'id': 'RECONCILIATION-MISSING', 'site': LEDGER}])
    try:
        ledger = strict(ledger_raw)
        if not isinstance(ledger, dict) or set(ledger) != {'schema', 'inputs_sha256', 'cohorts'} or ledger['schema'] != SCHEMA:
            raise ValueError('ledger schema')
        if ledger['inputs_sha256'] != hashlib.sha256(pins_raw).hexdigest():
            raise ValueError('ledger pins identity')
        if not isinstance(ledger['cohorts'], list) or [c.get('wave') for c in ledger['cohorts']] != list(COHORTS):
            raise ValueError('ledger cohort roster')
    except (ValueError, TypeError, AttributeError):
        return 1, dict(base, status='FAIL', unexplained_cohorts=len(COHORTS), findings=[{'id': 'RECONCILIATION-SCHEMA', 'site': LEDGER}])
    findings, cohorts, unexplained = [], {}, 0
    snap = W23 + '/snapshot/r22/'
    for wave, recorded in zip(COHORTS, ledger['cohorts']):
        try:
            derived = derive(wave, files[snap + wave + '/events.json'], files[snap + wave + '/bindings.json'], files[snap + wave + '/audit.json'])
        except Unevaluable as exc:
            return 2, dict(base, status='CANNOT_EVALUATE', unexplained_cohorts=None, findings=[{'id': exc.fid, 'site': exc.site}])
        local = cohort_findings(wave, derived, recorded, pins['expected'][wave])
        findings.extend(local)
        unexplained += bool(local)
        cohorts[wave] = dict(derived['totals'], explained=not local)
    return int(bool(unexplained)), dict(base, status='FAIL' if unexplained else 'PASS', unexplained_cohorts=unexplained, cohorts=cohorts, findings=findings)


def build_ledger(pins_raw, files):
    snap = W23 + '/snapshot/r22/'
    return {'schema': SCHEMA, 'inputs_sha256': hashlib.sha256(pins_raw).hexdigest(),
            'cohorts': [derive(w, files[snap + w + '/events.json'], files[snap + w + '/bindings.json'], files[snap + w + '/audit.json']) for w in COHORTS]}


def git_read(rev, path):
    proc = subprocess.run(['git', '--no-pager', '-C', str(ROOT), 'show', f'{rev}:{path}'], capture_output=True, env=_revision.clean_env(), timeout=60)
    if proc.returncode == 0:
        return proc.stdout
    check = subprocess.run(['git', '--literal-pathspecs', '-C', str(ROOT), 'ls-tree', '-z', rev, '--', path], capture_output=True, env=_revision.clean_env(), timeout=30)
    if check.returncode == 0 and not check.stdout:
        return None
    raise RuntimeError('committed read unavailable')


def selftest():
    """Independent literal fixtures; never derived from production EXPECTED or the r22 snapshot."""
    L = LANE + '/'
    a, b = L + 'a.md', L + 'b.md'
    def bindings(read, write=(L + 'r.md',)):
        return {'schema': 'tsukuroi-seat-bindings-v1', 'seats': [{'name': 'S', 'read_paths': list(read), 'write_paths': list(write)}]}
    def events(*evs):
        return {'schema': 'tsukuroi-seat-events-v1', 'seats': [{'name': 'S', 'events': [{'tool': t, 'args': {'path': p}, 'call_id': f'c{i}', 'request_arguments_sha256': str(i)} for i, (t, p) in enumerate(evs)]}]}
    def audit(*sites):
        return {'findings': [{'id': 'SCOPE-PATH-DENIED', 'site': s} for s in sites]}
    def files_for(ev, bd, au, other=None):
        out = {}
        for w in COHORTS:
            e, b2, u = (ev, bd, au) if w == 'build' else (other or (ev, bd, au))
            snap = W23 + '/snapshot/r22/' + w + '/'
            out[snap + 'events.json'] = json.dumps(e).encode()
            out[snap + 'bindings.json'] = json.dumps(b2).encode()
            out[snap + 'audit.json'] = json.dumps(u).encode()
        out[W23 + '/sources/r22-rough-census.txt'] = b'literal fixture source\n'
        return out
    def pins_for(files, rough, kept):
        return json.dumps({'schema': 'tsukuroi-reconciliation-inputs-v1', 'inputs': {k: hashlib.sha256(v).hexdigest() for k, v in files.items()},
                           'expected': {w: {'rough_as_reported': rough, 'lane_retained': kept} for w in COHORTS}}).encode()
    cases = []
    def case(name, ev, bd, au, rough, kept, want_code, want_id=None, mutate=None, ledger='auto', file_mut=None):
        files = files_for(ev, bd, au)
        pins = pins_for(files, rough, kept)
        if ledger == 'auto':
            try:
                led = build_ledger(pins, files)
            except Unevaluable:
                led = {'schema': SCHEMA, 'inputs_sha256': hashlib.sha256(pins).hexdigest(), 'cohorts': [{'wave': w} for w in COHORTS]}
            if mutate:
                mutate(led)
            raw = json.dumps(led).encode()
        else:
            raw = ledger
        if file_mut:
            file_mut(files)
        cases.append((name, pins, files, raw, want_code, want_id))
    # 1 mixed selector order: rough misses ':raw:N-M', canonical strips both orders.
    mixed = events(('read', a + ':raw:5-9'), ('read', a + ':5-9:raw'), ('read', b + ':raw'))
    case('mixed-raw-range-order', mixed, bindings([a]), audit('S:2'), 2, 1, 0)
    # 2 the same event explained only if retained count stays 0; a forged retained finding is unexplained.
    case('selector-but-retained', mixed, bindings([a]), audit('S:0', 'S:2'), 2, 2, 1, 'RECONCILIATION-UNEXPLAINED')
    # 2b offsetting pair: one rough-only and one retained-only event balance the totals but stay unexplained.
    offset = events(('read', a + ':raw:1-2'), ('read', a))
    case('offsetting-pair-net-zero', offset, bindings([a]), audit('S:1'), 1, 1, 1, 'RECONCILIATION-UNEXPLAINED')
    # 3 per-component unit: rough breaks after first bad, lane counts two.
    multi = events(('grep', a + ';' + b + ';' + L + 'c.md'))
    case('one-per-event-vs-per-component', multi, bindings([a]), audit('S:0', 'S:0'), 1, 2, 0)
    # 4 unit difference whose retained count disagrees with canonical components.
    case('unit-count-mismatch', multi, bindings([a]), audit('S:0', 'S:0', 'S:0'), 1, 3, 1, 'RECONCILIATION-UNEXPLAINED')
    # 5 reported totals must equal the recomputation.
    clean = events(('read', a), ('read', b), ('write', L + 'r.md'))
    case('wrong-rough-total', clean, bindings([a]), audit('S:1'), 2, 1, 1, 'RECONCILIATION-ROUGH-COUNT')
    case('wrong-retained-total', clean, bindings([a]), audit('S:1'), 1, 2, 1, 'RECONCILIATION-RETAINED-COUNT')
    case('agree-clean', clean, bindings([a]), audit('S:1'), 1, 1, 0)
    # 6 forged disposition / dropped / duplicated / reordered ledger rows.
    def forge(led):
        led['cohorts'][0]['rows'][0]['disposition'] = 'selector-normalization'
    case('forged-disposition', clean, bindings([a]), audit('S:1'), 1, 1, 1, 'RECONCILIATION-LEDGER-MISMATCH', mutate=forge)
    case('dropped-row', clean, bindings([a]), audit('S:1'), 1, 1, 1, 'RECONCILIATION-LEDGER-MISMATCH', mutate=lambda l: l['cohorts'][0]['rows'].pop())
    case('duplicate-row', clean, bindings([a]), audit('S:1'), 1, 1, 1, 'RECONCILIATION-LEDGER-MISMATCH', mutate=lambda l: l['cohorts'][0]['rows'].append(copy.deepcopy(l['cohorts'][0]['rows'][0])))
    case('wrong-arithmetic-total', clean, bindings([a]), audit('S:1'), 1, 1, 1, 'RECONCILIATION-LEDGER-MISMATCH', mutate=lambda l: l['cohorts'][1]['totals'].update(agree=99))
    # 7 orphan retained finding at a site with no event.
    case('orphan-retained', clean, bindings([a]), audit('S:1', 'S:9'), 1, 2, 1, 'RECONCILIATION-ORPHAN-FINDING')
    # 8 tamper, missing ledger, malformed ledger, duplicate JSON key, malformed events.
    case('snapshot-tampered', clean, bindings([a]), audit('S:1'), 1, 1, 2, 'SNAPSHOT-TAMPERED',
         file_mut=lambda f: f.__setitem__(W23 + '/snapshot/r22/build/audit.json', b'{"findings":[]}'))
    case('ledger-missing', clean, bindings([a]), audit('S:1'), 1, 1, 1, 'RECONCILIATION-MISSING', ledger=None)
    case('ledger-duplicate-key', clean, bindings([a]), audit('S:1'), 1, 1, 1, 'RECONCILIATION-SCHEMA', ledger=b'{"schema":1,"schema":2}')
    case('ledger-wrong-pins', clean, bindings([a]), audit('S:1'), 1, 1, 1, 'RECONCILIATION-SCHEMA',
         ledger=json.dumps({'schema': SCHEMA, 'inputs_sha256': '0' * 64, 'cohorts': [{'wave': 'build'}, {'wave': 'falsify'}]}).encode())
    bad_events = {'schema': 'tsukuroi-seat-events-v1', 'seats': [{'name': 'GHOST', 'events': []}]}
    case('event-roster-forgery', bad_events, bindings([a]), audit(), 0, 0, 2, 'RECONCILIATION-INPUT-MALFORMED')
    # 9 non-path categories stay agree with zero path counts; URL is a separate class in both totals.
    nonpath = events(('bash', ''), ('edit', a), ('read', 'skill://godspeed'))
    case('non-path-events', nonpath, bindings([a, 'skill://godspeed']), audit(), 0, 0, 0)
    observations = []
    for name, pins, files, raw, want_code, want_id in cases:
        code, payload = evaluate(pins, files, raw)
        ids = [f['id'] for f in payload['findings']]
        observations.append({'case': name, 'exit': code, 'ids': ids, 'pass': code == want_code and (want_id is None or want_id in ids) and (want_code != 0 or not ids)})
    # direct unit controls of the two counting rules
    units = [
        ('rough-misses-raw-first', rough_event('read', {'path': a + ':raw:1-2'}, {'read_paths': [a]}) == ('path', 0)),
        ('rough-strips-range-raw', rough_event('read', {'path': a + ':1-2:raw'}, {'read_paths': [a]}) == ('clean', None)),
        ('rough-break-first', rough_event('glob', {'path': b + ';' + a + ';' + b}, {'read_paths': [a]}) == ('path', 0)),
        ('canonical-both-orders', canonical_event('read', {'path': a + ':raw:1-2'}, {'read_paths': [a]}) == [] == canonical_event('read', {'path': a + ':1-2:raw'}, {'read_paths': [a]})),
        ('canonical-components', canonical_event('glob', {'path': b + ';' + a + ';' + b}, {'read_paths': [a]}) == [0, 2]),
        ('canonical-invalid-token-denied', canonical_event('read', {'path': a + ':foo'}, {'read_paths': [a]}) == [0]),
        ('canonical-dot-denied', canonical_event('read', {'path': L + 'x/../a.md'}, {'read_paths': [L + 'x/../a.md']}) == [0]),
        ('write-no-selector-strip', canonical_event('write', {'path': L + 'r.md:raw'}, {'write_paths': [L + 'r.md']}) == [0]),
    ]
    observations.extend({'case': n, 'pass': ok} for n, ok in units)
    failed = sum(not o['pass'] for o in observations)
    print(json.dumps({'status': 'FAIL' if failed else 'PASS', 'cases': len(observations), 'failed': failed, 'observations': observations}))
    return int(bool(failed))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--revision')
    group.add_argument('--selftest', action='store_true')
    parser.add_argument('--branch', default='master')
    parser.add_argument('--emit-ledger', action='store_true', help='print the recomputed ledger from inputs at --revision')
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return 0 if exc.code == 0 else 2
    if args.selftest:
        return selftest()
    try:
        binding = _revision.bind(ROOT, args.revision, args.branch)
        pins_raw = git_read(binding.sha, PINS)
        if pins_raw is None:
            raise RuntimeError('pins absent')
        files = {path: git_read(binding.sha, path) for path in strict(pins_raw)['inputs']}
        if args.emit_ledger:
            print(json.dumps(build_ledger(pins_raw, files), indent=1, sort_keys=True))
            return 0
        code, payload = evaluate(pins_raw, files, git_read(binding.sha, LEDGER))
        payload.update(revision=binding.sha, branch=binding.branch, branch_tip=binding.branch_tip)
    except _revision.RevisionError as exc:
        code, payload = 2, {'status': 'CANNOT_EVALUATE', 'unexplained_cohorts': None, 'findings': [{'id': exc.fid, 'site': exc.site}]}
    except Unevaluable as exc:
        code, payload = 2, {'status': 'CANNOT_EVALUATE', 'unexplained_cohorts': None, 'findings': [{'id': exc.fid, 'site': exc.site}]}
    except (OSError, RuntimeError, ValueError, KeyError, subprocess.TimeoutExpired):
        code, payload = 2, {'status': 'CANNOT_EVALUATE', 'unexplained_cohorts': None, 'findings': [{'id': 'RECONCILIATION-READ', 'site': 'revision'}]}
    print(json.dumps(payload, sort_keys=True))
    return code


if __name__ == '__main__':
    sys.exit(main())
