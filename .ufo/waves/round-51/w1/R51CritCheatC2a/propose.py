import importlib.util, json, os, re, sys

S = '/fast/scratch/hyaku/tsukuroi-r51/R51CritCheatC2a'
spec = importlib.util.spec_from_file_location('matcher_frozen', os.path.join(S, 'matcher_frozen.py'))
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)

# Proposed leg: a pipe whose LEFT side starts a producer that expands a variable
# (printf/echo/cat of `$x`, or a variable used as the command word) and whose RIGHT side holds an
# early-exit consumer (grep with q/m flag or --quiet/--silent/--max-count, any head, any read,
# awk with `exit` before its END block, sed with a `q` command).
PROD = re.compile(
    r'(?:^|[;&!]|(?<!<)[({]|\$\(|\b(?:if|elif|then|do|while|until)\b)\s*!?\s*'
    r'(?:(?:(?:command|builtin|exec)\s+)?(?:/(?:usr/)?bin/)?(?:printf|echo|cat)\b[^|]*\$'
    r'|"?\$\{?[A-Za-z_][A-Za-z0-9_]*\}?"?\s)')
CONS = re.compile(
    r'\bgrep\b[^|]*\s-[A-Za-z]*[qm]|\bgrep\b[^|]*--(?:quiet|silent|max-count)|\bhead\b|\bread\b'
    r'|\bawk\b(?:(?!END)[^|])*\bexit\b|\bsed\b[^|]*[;\s\'"{]q\b')
PIPE = re.compile(r'(?<!\|)\|(?!\|)')


def idiom2_hits(text):
    hits = []
    for n, raw in enumerate(text.split('\n'), 1):
        ln = M.strip_comment(raw)
        if re.search(r'\|\|\s*true\)*\s*$', ln):  # status explicitly discarded: no abort, no branch
            continue
        for m in PIPE.finditer(ln):
            if PROD.search(ln[:m.start()]) and CONS.search(ln[m.end():]):
                hits.append((n, raw.strip()))
                break
    return hits


census = open(os.path.join(S, 'census.sh'), encoding='utf-8', errors='replace').read()
out = {'census_old_idiom_sites': M.idiom_sites(census),
       'census_new_hits': idiom2_hits(census)}
mut = {}
for sid in ['C0', 'S01', 'S02', 'S03', 'S04', 'S05', 'S06', 'S07', 'S08', 'S09', 'S10', 'S11', 'S12',
            'S13', 'S14', 'S15', 'S16', 'S17', 'S18', 'S19', 'S20', 'S21', 'S22']:
    t = open(os.path.join(S, 'mutants', f'{sid}.sh'), encoding='utf-8').read()
    mut[sid] = {'old': M.idiom_sites(t), 'new': len(idiom2_hits(t))}
out['mutants'] = mut
print(json.dumps(out, indent=1))
