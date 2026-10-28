import importlib.util, json, os, shutil, subprocess, sys, tempfile

S = '/fast/scratch/hyaku/tsukuroi-r51/R51CritCheatC2a'
spec = importlib.util.spec_from_file_location('matcher_frozen', os.path.join(S, 'matcher_frozen.py'))
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)

CENSUS = os.path.join(S, 'census.sh')
text = open(CENSUS, encoding='utf-8', errors='replace').read()
TARGET = "    elif ! out_has 'host=fixture-host'; then"
assert text.count(TARGET + '\n') == 1, text.count(TARGET)
base_sites = M.idiom_sites(text)

SPELL = [
    ('C0', 'control: printf | grep -q', "printf '%s\\n' \"$out\" | grep -q 'host=fixture-host'"),
    ('S01', 'producer through variable', "{ p=printf; \"$p\" '%s\\n' \"$out\" | grep -q 'host=fixture-host'; }"),
    ('S02', 'command printf', "command printf '%s\\n' \"$out\" | grep -q 'host=fixture-host'"),
    ('S03', 'builtin printf', "builtin printf '%s\\n' \"$out\" | grep -q 'host=fixture-host'"),
    ('S04', 'consumer in brace group', "printf '%s\\n' \"$out\" | { grep -q 'host=fixture-host'; }"),
    ('S05', 'process substitution', "grep -q 'host=fixture-host' <(printf '%s\\n' \"$out\")"),
    ('S06', 'grep -E -q', "printf '%s\\n' \"$out\" | grep -E -q 'host=fixture-host'"),
    ('S07', 'grep --quiet (control)', "printf '%s\\n' \"$out\" | grep --quiet 'host=fixture-host'"),
    ('S08', 'grep -m1', "printf '%s\\n' \"$out\" | grep -m1 'host=fixture-host' >/dev/null"),
    ('S09', 'sed -n 1p then grep -q', "printf '%s\\n' \"$out\" | sed -n 1p | grep -q 'host=fixture-host'"),
    ('S10', 'awk match-exit', "printf '%s\\n' \"$out\" | awk '/host=fixture-host/ { exit 0 } END { exit 1 }'"),
    ('S11', 'read -r (probe)', "printf '%s\\n' \"$out\" | read -r _"),
    ('S12', 'head -c 64 then grep -q', "printf '%s\\n' \"$out\" | head -c 64 | grep -q 'host=fixture-host'"),
    ('S13', 'head --lines=1 then grep -q', "printf '%s\\n' \"$out\" | head --lines=1 | grep -q 'host=fixture-host'"),
    ('S14', 'grep -e PAT -q (q after pattern)', "printf '%s\\n' \"$out\" | grep -e 'host=fixture-host' -q"),
    ('S15', '/usr/bin/grep -q', "printf '%s\\n' \"$out\" | /usr/bin/grep -q 'host=fixture-host'"),
    ('S16', 'command grep -q', "printf '%s\\n' \"$out\" | command grep -q 'host=fixture-host'"),
    ('S17', 'subshell consumer', "printf '%s\\n' \"$out\" | ( grep -q 'host=fixture-host' )"),
    ('S18', 'awk NR==1{exit} (probe)', "printf '%s\\n' \"$out\" | awk 'NR==1{exit}'"),
    ('S19', 'grep -m 1 (spaced)', "printf '%s\\n' \"$out\" | grep -m 1 'host=fixture-host' >/dev/null"),
    ('S20', 'echo producer, grep -E -q', "echo \"$out\" | grep -E -q 'host=fixture-host'"),
    ('S21', 'timeout wrapper then grep -q', "printf '%s\\n' \"$out\" | timeout 5 grep -q 'host=fixture-host'"),
    ('S22', 'head -n 1 then grep -q (control)', "printf '%s\\n' \"$out\" | head -n 1 | grep -q 'host=fixture-host'"),
]

HAZ = r'''set -euo pipefail
big=$(printf '%%*s' 200000 '' | tr ' ' x)
if [ "%(pos)s" = first ]; then out=$(printf '%%s\n' 'host=fixture-host' "$big")
else out=$(printf '%%s\n' "$big" 'host=fixture-host' "$big"); fi
ok=0; bad=0
for i in $(seq 20); do
  if %(cond)s; then ok=$((ok + 1)); else bad=$((bad + 1)); fi
done
printf 'OK %%d BAD %%d\n' "$ok" "$bad"
'''

env = {'PATH': '/usr/bin:/bin', 'LC_ALL': 'C', 'TMPDIR': os.path.join(S, 'tmp')}
os.makedirs(env['TMPDIR'], exist_ok=True)
os.makedirs(os.path.join(S, 'mutants'), exist_ok=True)

rows = []
try:
    for sid, desc, cond in SPELL:
        new_line = f"    elif ! {cond}; then"
        mut = text.replace(TARGET + '\n', new_line + '\n', 1)
        mpath = os.path.join(S, 'mutants', f'{sid}.sh')
        open(mpath, 'w', encoding='utf-8').write(mut)
        syn = subprocess.run(['bash', '-n', mpath], capture_output=True, text=True, env=env)
        sites = M.idiom_sites(mut)
        haz = {}
        for pos in ('first', 'mid'):
            hpath = os.path.join(S, 'mutants', f'{sid}.{pos}.haz.sh')
            open(hpath, 'w').write(HAZ % {'pos': pos, 'cond': cond})
            p = subprocess.run(['bash', hpath], capture_output=True, text=True, env=env, timeout=600)
            haz[pos] = (p.stdout.strip() or p.stderr.strip()[-200:])
        rows.append({'id': sid, 'desc': desc, 'bash_n_rc': syn.returncode, 'idiom_sites': sites,
                     'delta_vs_base': sites - base_sites, 'haz_first': haz['first'], 'haz_mid': haz['mid'],
                     'line': new_line})
finally:
    shutil.rmtree(env['TMPDIR'], ignore_errors=True)

print(json.dumps({'base_idiom_sites': base_sites, 'target': TARGET, 'rows': rows}, indent=1))
