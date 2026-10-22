"""Independent C1 subcause recomputation (RevC1Subcauses, wave 2).

Inputs: frozen round-23 falsify bytes at commit 22fd1642 (identical to the lane working tree, verified by sha256).
Does not import report-red-causes.py. Grammar is restated from the frozen checker tools/check-seat-bindings.py
(functions local, requested_path, classify, classify_edit, evaluate) and implemented here independently.
"""
import json, re, sys, unicodedata, collections, hashlib

LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
F = LANE + '/.ufo/waves/round-23/falsify/'
OUT = LANE + '/.ufo/waves/round-24/w2/RevC1Subcauses/'
COMMITTED = LANE + '/.ufo/waves/round-24/measure/c1-22fd1642.json'
CHECKER_OUT = OUT + 'checker-22fd1642-falsify.json'

SEL_TOKEN = re.compile(r'\d+(?:[-+]\d*)?|-\d+')
ALLOWED = {'read': {'i', 'path'}, 'grep': {'i', 'pattern', 'path', 'case', 'gitignore', 'skip'},
           'glob': {'i', 'path', 'hidden', 'gitignore', 'limit'}, 'write': {'i', 'path', 'content'}}
EDIT_SHAPES = ({'path', 'stream_content'}, {'path', 'old_string', 'new_string'})
CONTROL = ('Cc', 'Cf', 'Cs', 'Zl', 'Zp')

SUB_OUTSIDE = 'outside the lane root'
SUB_SPELL_DECL = 'inside the lane, spelled outside the frozen grammar, base path declared'
SUB_SPELL_UNDECL = 'inside the lane, spelled outside the frozen grammar, base path undeclared'
SUB_WELL_UNBOUND = 'inside the lane, well formed, not bound to the seat'
SUB_OTHER_OP = 'declared for the other operation only'
SUB_EDIT_KEYS = 'argument key outside the frozen two-shape edit grammar'
SUB_TRACE = 'trace ends before a final message'


def sha256(path):
    with open(path, 'rb') as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def well_formed(p):
    if not isinstance(p, str) or not p or not p.startswith(LANE + '/'):
        return False
    if '\\' in p or any(unicodedata.category(c) in CONTROL for c in p) or any(c in p for c in '*?[];:'):
        return False
    return all(seg not in ('', '.', '..') for seg in p.split('/')[1:])


def strip_selector(value):
    if ':' not in value:
        return value
    base, *tokens = value.split(':')

    def valid(tok):
        return tok in ('raw', 'img', 'conflicts') or all(SEL_TOKEN.fullmatch(x) for x in tok.split(','))
    return base if tokens and all(valid(t) for t in tokens) else value


def lookup(value, selector):
    """(path, kind) where kind is None (lane-local, possibly unbound), 'FETCH' or 'PATH' (grammar denial)."""
    if re.match(r'(?i)^https?://', value) or re.match(r'^[^/:\s]+:[0-9]+/', value):
        return value, 'FETCH'
    if value == 'skill://godspeed':
        return value, None
    path = strip_selector(value) if selector else value
    return path, (None if well_formed(path) else 'PATH')


def base_of(value):
    return value.split('?', 1)[0].split(':', 1)[0]


def read_like(tool, args, seat, seat_id):
    """Yield dicts, one per finding, for read/grep/glob/write as the frozen classify() would emit them."""
    found = []
    if not isinstance(args, dict):
        return [{'id': 'SCOPE-SCHEMA', 'sub': 'non-dict arguments', 'value': None}]
    if set(args) - ALLOWED[tool]:
        found.append({'id': 'SCOPE-SCHEMA', 'sub': 'unknown argument key', 'value': None})
    value = args.get('path')
    if not isinstance(value, str) or not value:
        return [{'id': 'SCOPE-SCHEMA', 'sub': 'missing or non-string path', 'value': None}]
    pieces = value.split(';') if tool in ('grep', 'glob') else [value]
    own = seat['write_paths'] if tool == 'write' else seat['read_paths']
    other = seat['read_paths'] if tool == 'write' else seat['write_paths']
    for raw in pieces:
        path, kind = lookup(raw, selector=tool in ('read', 'grep'))
        if kind == 'FETCH':
            found.append({'id': 'SCOPE-FETCH-DENIED', 'sub': 'fetch spelling', 'value': raw})
        elif kind == 'PATH':
            if not raw.startswith(LANE + '/'):
                sub = SUB_OUTSIDE
            else:
                b = base_of(raw)
                sub = SUB_SPELL_DECL if (b in seat['read_paths'] or b in seat['write_paths']) else SUB_SPELL_UNDECL
            found.append({'id': 'SCOPE-PATH-DENIED', 'sub': sub, 'value': raw})
        elif path not in own:
            if not path.startswith(LANE + '/'):
                sub = SUB_OUTSIDE
            elif path in other:
                sub = SUB_OTHER_OP
            else:
                sub = SUB_WELL_UNBOUND
            found.append({'id': 'SCOPE-PATH-DENIED', 'sub': sub, 'value': raw})
    return found


def edit_rule(args, seat):
    if not isinstance(args, dict):
        return [{'id': 'SCOPE-SCHEMA', 'sub': SUB_EDIT_KEYS, 'value': None}]
    if (set(args) - {'i'}) not in EDIT_SHAPES:
        return [{'id': 'SCOPE-SCHEMA', 'sub': SUB_EDIT_KEYS, 'value': None}]
    value = args.get('path')
    if not isinstance(value, str) or not value:
        return [{'id': 'SCOPE-SCHEMA', 'sub': 'missing edit target', 'value': None}]
    if re.match(r'(?i)^https?://', value) or re.match(r'^[^/:\s]+:[0-9]+/', value):
        return [{'id': 'SCOPE-FETCH-DENIED', 'sub': 'fetch spelling', 'value': value}]
    if value not in seat['edit_paths']:
        return [{'id': 'SCOPE-EDIT-DENIED', 'sub': 'undeclared edit target', 'value': value}]
    return []


def main():
    B = json.load(open(F + 'bindings.json'))
    E = json.load(open(F + 'events.json'))
    bind = {s['name']: s for s in B['seats']}
    mine, rows, seats_by_row = [], collections.Counter(), collections.defaultdict(set)
    for s in E['seats']:
        seat = bind[s['name']]
        for i, ev in enumerate(s['events']):
            tool = ev['tool']
            if tool == 'edit':
                found = edit_rule(ev['args'], seat)
            elif tool in ('read', 'grep', 'glob', 'write'):
                found = read_like(tool, ev['args'], seat, s['name'])
            else:
                found = [{'id': 'SCOPE-TOOL-UNKNOWN', 'sub': 'unknown tool', 'value': None}]
            for f in found:
                site = f"{s['name']}:{i}"
                mine.append({'site': site, 'id': f['id'], 'tool': tool, 'sub': f['sub'], 'value': f['value']})
                if f['id'] == 'SCOPE-SCHEMA' and tool == 'edit' and f['sub'] == SUB_EDIT_KEYS:
                    pass
                key = (f['id'], tool, f['sub'])
                rows[key] += 1
                seats_by_row[key].add(s['name'])
        if not s['complete']:
            key = ('SCOPE-TRACE-INCOMPLETE', 'none (seat-level trace state)', SUB_TRACE)
            mine.append({'site': s['name'], 'id': 'SCOPE-TRACE-INCOMPLETE', 'tool': None, 'sub': SUB_TRACE, 'value': None})
            rows[key] += 1
            seats_by_row[key].add(s['name'])
    # Compare with the frozen checker's own finding list (oracle), as (site, id) multisets.
    checker = json.load(open(CHECKER_OUT))
    mc = collections.Counter((f['site'], f['id']) for f in mine)
    cc = collections.Counter((f['site'], f['id']) for f in checker['findings'])
    only_mine = mc - cc
    only_checker = cc - mc
    print('my findings', len(mine), 'checker findings', len(checker['findings']))
    print('finding multiset diff: only mine', dict(only_mine), '| only checker', dict(only_checker))
    # Compare my causes with the committed causes array.
    committed = json.load(open(COMMITTED))['causes']
    crow = {(c['finding'], c['operation'], c['subcause']): (c['count'], c['seats']) for c in committed}
    mrow = {k: (rows[k], len(seats_by_row[k])) for k in rows}
    print('committed rows', len(crow), 'recomputed rows', len(mrow))
    for k in sorted(set(crow) | set(mrow)):
        cv = crow.get(k)
        mv = mrow.get(k, (0, 0))
        status = 'AGREE' if cv == mv else 'DISAGREE'
        print(status, k, 'committed(count,seats)=', cv, 'recomputed(count,seats)=', mv)
    total_path = sum(1 for f in mine if f['id'] == 'SCOPE-PATH-DENIED')
    distinct_path_seats = len({f['site'].split(':')[0] for f in mine if f['id'] == 'SCOPE-PATH-DENIED'})
    print('path findings', total_path, 'distinct seats with path findings', distinct_path_seats)
    with open(OUT + 'recomputed-findings.json', 'w') as fh:
        json.dump({'findings': mine, 'rows': [{'finding': k[0], 'operation': k[1], 'subcause': k[2], 'count': rows[k], 'seats': len(seats_by_row[k])} for k in sorted(rows)]}, fh, indent=1, sort_keys=True)
    print('input sha256', {p: sha256(p) for p in (F + 'bindings.json', F + 'events.json', LANE + '/.ufo/waves/round-23/measure/post-falsify/falsify-limit.json', LANE + '/tools/check-seat-bindings.py')})


if __name__ == '__main__':
    sys.dont_write_bytecode = True
    main()
