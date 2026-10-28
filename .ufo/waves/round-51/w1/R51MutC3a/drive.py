import sys, json, importlib.util, os, shutil
sys.dont_write_bytecode = True
B = '/fast/scratch/hyaku/tsukuroi-r51/R51MutC3a'
REV = '2732ee6c06108c031c4d8043239b994e0504eb2f'
name = sys.argv[1]
spec = importlib.util.spec_from_file_location('battery', f'{B}/battery.py')
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)
b.C3 = f'{B}/{name}/tools/check-adjacency-table-r51.py'
scratch = f'{B}/scratch-{name}'
os.makedirs(scratch, exist_ok=True)
try:
    rows = b.c3_battery(REV, scratch)
finally:
    shutil.rmtree(scratch, ignore_errors=True)
with open(f'{B}/out-{name}.jsonl', 'w', encoding='utf-8') as fh:
    for r in rows:
        fh.write(json.dumps(r, sort_keys=True) + '\n')
print(f'== {name}: {len(rows)} controls, {sum(r["as_expected"] for r in rows)} as expected')
for r in rows:
    print(('  OK  ' if r['as_expected'] else '  FLIP'), r['control'], '| expected', r['expected'], '| got', r['got'], '| rc', r['rc'], '|', json.dumps(r['legs'], sort_keys=True))
