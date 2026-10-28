import importlib.util
import json
import os
import sys

S = '/fast/scratch/hyaku/tsukuroi-r51/R51MutC3b'
T = S + '/lane/tools'
C3 = T + '/check-adjacency-table-r51.py'
R50 = T + '/check-adjacency-table-r50.py'
FREEZE = '2732ee6c06108c031c4d8043239b994e0504eb2f'
ORIG3 = open(S + '/orig/check-adjacency-table-r51.py', encoding='utf-8').read()
ORIG50 = open(S + '/orig/check-adjacency-table-r50.py', encoding='utf-8').read()
WORK = S + '/work'
os.chdir(WORK)


def line_edits(text, edits):
    lines = text.split('\n')
    for start, end, expect, new in sorted(edits, reverse=True):
        assert expect in lines[start - 1], (start, lines[start - 1])
        lines[start - 1:end] = new.split('\n') if new is not None else []
    return '\n'.join(lines)


MUT = {
    'orig': lambda t: t,
    'M5': lambda t: line_edits(t, [(256, 263, "q = subprocess.run(", "            override_blocked = 1")]),
    'M6': lambda t: line_edits(t, [(273, 273, "r50_blind = int(f.returncode", "            r50_blind = 1")]),
    'M7a': lambda t: line_edits(t, [(134, 135, "if not any(quote in ln", "                pass  # M7a")]),
    'M7b': lambda t: line_edits(t, [(129, 135, "hidx = next(", None)]),
    'M8': lambda t: line_edits(t, [(244, 244, "display_forge_fails = int(", "    display_forge_fails = 1")]),
}

spec = importlib.util.spec_from_file_location('battery_prop', S + '/battery_prop.py')
bat = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bat)
bat.C3 = C3

summary = {}
try:
    for label, fn in MUT.items():
        with open(C3, 'w', encoding='utf-8') as fh:
            fh.write(fn(ORIG3))
        with open(R50, 'w', encoding='utf-8') as fh:
            fh.write(ORIG50)
        rows = bat.c3_battery(FREEZE, WORK + '/prop-' + label)
        miss = [r['control'] for r in rows if not r['as_expected']]
        summary[label] = {'rows': len(rows), 'as_expected': len(rows) - len(miss), 'killed_by': miss,
                          'got': {r['control'][:3]: r['got'] for r in rows}}
        print(label, 'rows', len(rows), 'killed_by', miss, flush=True)
finally:
    with open(C3, 'w', encoding='utf-8') as fh:
        fh.write(ORIG3)
    with open(R50, 'w', encoding='utf-8') as fh:
        fh.write(ORIG50)
    with open(S + '/prop-summary.json', 'w', encoding='utf-8') as fh:
        json.dump(summary, fh, indent=1, ensure_ascii=False)
print(json.dumps(summary, ensure_ascii=False)[:3000])
