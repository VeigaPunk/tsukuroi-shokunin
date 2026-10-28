import os

S = '/fast/scratch/hyaku/tsukuroi-r51/R51MutC3b'
src = open(S + '/battery.py', encoding='utf-8').read()
anchor = '    return out\n\n\ndef main():'
assert src.count(anchor) == 1, src.count(anchor)

EXTRA = r'''
STUB_CHILD = ("import json, sys\nprint(json.dumps({'verdict': 'PASS', 'control': 'accepting-child-stub'}))\n"
              "sys.exit(0)\n")
SELF_CHILD_OLD = "[sys.executable, os.path.abspath(__file__), '--revision', rev, '--lane', lane,"
SELF_CHILD_NEW = ("[sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'accepting_child.py'), "
                  "'--revision', rev, '--lane', lane,")
R50_MAIN_OLD = 'def main():\n'
R50_MAIN_NEW = ("def main():\n    if '--province-file' in sys.argv:\n"
                "        print(json.dumps({'verdict': 'FAIL', 'control': 'K7'}))\n        return 1\n")
DISPLAY_OLD = '            if not full_commit.startswith(m.group(2)):'
DISPLAY_NEW = '            if False:'
HEAD_NEW = '## Core / Frontier / Adjacent (fleet round 1, appended 2026-10-19)'


def c3_extra(freeze, scratch):
    """Round-51 mutation controls K6-K9. Each one makes a leg that the existing rows never see fail on purpose,
    so a counter whose leg is forced to 1 (or whose heading section test is dropped) no longer matches."""
    out = []
    base = open(C3, encoding='utf-8').read()
    r50 = open(os.path.join(os.path.dirname(C3), 'check-adjacency-table-r50.py'), encoding='utf-8').read()
    d = os.path.join(scratch, 'c3x')
    os.makedirs(d, exist_ok=True)

    def variant(name, c3_text, r50_text, extra):
        vd = os.path.join(d, name, 'tools')
        os.makedirs(vd, exist_ok=True)
        with open(os.path.join(vd, 'check-adjacency-table-r51.py'), 'w', encoding='utf-8') as fh:
            fh.write(c3_text)
        with open(os.path.join(vd, 'check-adjacency-table-r50.py'), 'w', encoding='utf-8') as fh:
            fh.write(r50_text)
        with open(os.path.join(vd, 'accepting_child.py'), 'w', encoding='utf-8') as fh:
            fh.write(STUB_CHILD)
        cmd = [sys.executable, os.path.join(vd, 'check-adjacency-table-r51.py'), '--revision', freeze,
               '--lane', L, '--no-base-check'] + extra
        return run_json(cmd)

    def add(name, expect, rc, obj):
        out.append({'control': name, 'expected': expect, 'got': obj.get('verdict'), 'rc': rc,
                    'as_expected': obj.get('verdict') == expect,
                    'legs': {k: obj.get(k) for k in ('display_bound_ok', 'quote_specific_ok', 'digests_bound_ok',
                                                     'display_forge_fails', 'override_blocked', 'r50_blind',
                                                     'quote_at_pin_ok', 'stub_fails')}})

    # K6: a self-run child that accepts the override (unguarded) must make the measurement FAIL
    rc, obj = variant('k6', base.replace(SELF_CHILD_OLD, SELF_CHILD_NEW), r50, [])
    add('K6 accepting self-run child: override leg must FAIL the measurement', 'FAIL', rc, obj)
    # K7: a round-50 sensitivity child that rejects overrides (r50 not blind) must make the measurement FAIL
    assert r50.count(R50_MAIN_OLD) == 1
    rc, obj = variant('k7', base, r50.replace(R50_MAIN_OLD, R50_MAIN_NEW), [])
    add('K7 round-50 child not blind to the forgery: r50_blind leg must FAIL the measurement', 'FAIL', rc, obj)
    # K8: a display check blind to the displayed OUT-009 commit must make the measurement FAIL (forge leg)
    rc, obj = variant('k8', base.replace(DISPLAY_OLD, DISPLAY_NEW), r50, [])
    add('K8 display check blind to a forged OUT-009 commit: display_forge leg must FAIL', 'FAIL', rc, obj)
    # K9: a displayed heading and registry heading moved to a section that does not hold the quote
    prov = git_show(freeze, 'PROVINCE.md')
    reg = json.loads(git_show(freeze, 'corpus/knowledge/adjacency-anchors-r19.json'))
    lines = prov.split('\n')
    hit = [i for i, ln in enumerate(lines) if ln.startswith('| OUT-010 |')]
    assert len(hit) == 1 and lines[hit[0]].count('`# tameshi-shokunin — Province`') == 1
    lines[hit[0]] = lines[hit[0]].replace('`# tameshi-shokunin — Province`', '`' + HEAD_NEW + '`')
    for row in reg['outbound']:
        if row['id'] == 'OUT-010':
            row['heading'] = HEAD_NEW
    p9 = os.path.join(d, 'k9-province.md')
    r9 = os.path.join(d, 'k9-registry.json')
    with open(p9, 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(lines))
    with open(r9, 'w', encoding='utf-8') as fh:
        fh.write(json.dumps(reg))
    rc, obj = variant('k9', base, r50, ['--control', '--province-file', p9, '--registry-file', r9])
    add('K9 heading moved to a section without the quote: quote_specific leg must FAIL', 'CONTROL-FAIL', rc, obj)
    return out

'''

new = src.replace(anchor, '    return out + c3_extra(freeze, scratch)\n' + EXTRA + '\ndef main():')
assert new != src
open(S + '/battery_prop.py', 'w', encoding='utf-8').write(new)
print('wrote battery_prop.py', len(new))
