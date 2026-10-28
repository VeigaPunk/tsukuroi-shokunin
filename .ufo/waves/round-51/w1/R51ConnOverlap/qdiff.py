import importlib.util, re, subprocess
R = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'; REV = '2732ee6c06108c031c4d8043239b994e0504eb2f'
spec = importlib.util.spec_from_file_location('l51', 'lint51copy.py'); L = importlib.util.module_from_spec(spec); spec.loader.exec_module(L)
def show(p):
    r = subprocess.run(['git', '-C', R, 'show', f'{REV}:{p}'], capture_output=True)
    return r.stdout.decode('utf-8', errors='replace') if r.returncode == 0 else None
cache = {}
for sid, files in L.SNAPSHOTS.items():
    for base, (path, want) in files.items():
        t = show(path)
        if t is not None:
            cache[(sid, base)] = t.split('\n')
def qgood(src, n, q):  # round-45 counter rule, copied from check-scrub-grounding-r45.py quote_good
    if not src or not (1 <= n <= len(src)): return False
    whole = src[n-1].strip(); qs = q.strip()
    if not qs or qs not in src[n-1]: return False
    return (len(qs) >= 10 or qs == whole) and 2*len(qs) >= len(whole)
Q = re.compile(r'^\*\*Quote\.\*\* `(S\d+)` ([^:]+):(\d+): "(.*)"\s*$')
lines = open('entry.md', encoding='utf-8').read().split('\n')
dis = []; tot = 0; lint_ok = r45_ok = 0
for i, ln in enumerate(lines):
    m = Q.match(ln)
    if not m: continue
    tot += 1
    sid, base, n, want = m.group(1), m.group(2).strip(), int(m.group(3)), m.group(4)
    src = cache.get((sid, base))
    lo = bool(src and 1 <= n <= len(src) and L.norm(want) == L.norm(src[n-1]))
    ro = qgood(src, n, want)
    lint_ok += lo; r45_ok += ro
    if lo != ro: dis.append((i+1, sid, base, n, lo, ro))
print('quotes', tot, 'lint_whole_line_ok', lint_ok, 'r45_rule_ok', r45_ok)
print('disagreements', dis)
print('snapshots loaded', len(cache), 'of', sum(len(f) for f in L.SNAPSHOTS.values()))
