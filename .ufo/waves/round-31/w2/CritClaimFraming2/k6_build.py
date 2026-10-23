#!/usr/bin/env python3
"""K6 fetched-but-not-read control: K3's junk rows plus one source-free dictionary word per
sealed key group. Never opens the pinned btrfs-progs files (or any btrfs text). Prints counts
and digests only; plaintext words stay in the sandbox tree."""
import hashlib, importlib.util, json, os, re, subprocess, sys

repo = sys.argv[1]
env = {k: v for k, v in os.environ.items() if not k.startswith(('GIT_', 'LD_', 'PYTHON'))}
env.update({'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': os.devnull, 'GIT_CONFIG_SYSTEM': os.devnull})
spec = importlib.util.spec_from_file_location('ctr', os.path.join(repo, 'tools/check-btrfs-repair-r31.py'))
ctr = importlib.util.module_from_spec(spec); spec.loader.exec_module(ctr)

def toks(text):
    out = set()
    for w in ctr.words(text):
        out.add(w); out |= {p for p in re.split(r'[-/.]', w) if p}
    return out

tiers = {}
tiers['questions'] = set()
for q in ctr.QUESTIONS.values():
    tiers['questions'] |= toks(q['q']) | toks(' '.join(q['tokens']))
tiers['cracklib'] = toks(open('/usr/share/cracklib/cracklib-small', errors='replace').read())
units = ['', 's', 'ms', 'sec', 'secs', 'second', 'seconds', 'min', 'minutes', 'k', 'kb', 'kib', 'm', 'mb', 'mib', 'g', 'gb', 'gib', '%']
tiers['numbers'] = {f'{n}{u}' for n in range(0, 1001) for u in units}
base_txt = ''
for path in ('SKILL.md', 'PROVINCE.md'):
    base_txt += subprocess.run(['/usr/bin/git', '-C', repo, 'show', f'{ctr.BASE}:{path}'], capture_output=True, env=env).stdout.decode('utf-8', 'replace')
files = subprocess.run(['/usr/bin/git', '-C', repo, 'ls-tree', '-r', '--name-only', ctr.BASE, 'corpus'], capture_output=True, env=env).stdout.decode().split()
for f in files:
    base_txt += subprocess.run(['/usr/bin/git', '-C', repo, 'show', f'{ctr.BASE}:{f}'], capture_output=True, env=env).stdout.decode('utf-8', 'replace')
tiers['lane_base'] = toks(base_txt)

def dig(w):
    return hashlib.sha256((ctr.SALT + ' ' + w).encode()).hexdigest()[:16]

def recover(cands):
    table = {}
    for w in cands:
        table.setdefault(dig(w), w)
    return table

full = recover(set().union(*tiers.values()))
summary = {'dictionary_size': len(set().union(*tiers.values()))}
for name in tiers:
    t = recover(tiers[name])
    summary[f'groups_{name}_only'] = sum(any(d in t for d in g) for gs in ctr.KEYHASH.values() for g in gs)
picked, missing = {}, []
for qid, groups in ctr.KEYHASH.items():
    picked[qid] = []
    for n, g in enumerate(groups, 1):
        hit = [full[d] for d in g if d in full]
        if hit:
            picked[qid].append(hit[0])
        else:
            missing.append(f'{qid}g{n}')
summary['groups_recovered'] = 48 - 24 - len(missing)
summary['missing'] = missing

entry = os.path.join(repo, ctr.ENTRY)
doc = json.load(open(entry))
for r in doc['rows']:
    r['statement'] = r['statement'] + ' Words: ' + ' '.join(picked[r['id']]) + '.'
with open(entry, 'w') as fh:
    fh.write(json.dumps({'rows': doc['rows']}, indent=1) + '\n')
print(json.dumps(summary))
