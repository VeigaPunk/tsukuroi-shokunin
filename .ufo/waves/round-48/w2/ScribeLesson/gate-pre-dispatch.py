#!/usr/bin/env python3
"""Proposed pre-dispatch gate for a wave spec (draft text for the lesson; the lane is not edited).
Rules, each one a mistake this round or round 47 already made:
 R1 the spec context names a FREEZE revision, and it is a commit       (attempt 1 named none)
 R2 that freeze is an ancestor of the lane tip at dispatch             (a stale/mutable tip is not bytes)
 R3 every tools/*.py the context names as frozen exists AT the freeze  (attempt 1 named a file that never existed)
 R4 a freeze record exists at the freeze: FROZEN.md + pinned digests   (attempt 1's frozen/ was empty)
 R5 the spec's reportDir is not the reportDir of a voided wave
"""
import json, re, subprocess, sys
L = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
def git(*a): return subprocess.run(['git','-C',L,*a], capture_output=True)
spec = json.load(open(sys.argv[1])); ctx = spec['context']; bad = []
m = re.search(r'FREEZE revision\s*=\s*([0-9a-f]{40})', ctx)
if len(sys.argv) > 2:  # --freeze override, for probing rules R2-R4 on a spec that names none
    import types; m = types.SimpleNamespace(group=lambda i: sys.argv[2])
if not m: bad.append('R1 context names no FREEZE revision')
else:
    rev = m.group(1)
    if git('cat-file','-e',rev+'^{commit}').returncode: bad.append(f'R1 freeze {rev[:12]} is not a commit')
    tip = git('rev-parse','master').stdout.decode().strip()
    if git('merge-base','--is-ancestor',rev,tip).returncode: bad.append(f'R2 freeze {rev[:12]} is not an ancestor of tip {tip[:12]}')
    for name in sorted(set(re.findall(r'tools/[A-Za-z0-9._-]+\.py', ctx))):
        if git('cat-file','-e',f'{rev}:{name}').returncode: bad.append(f'R3 {name} does not exist at freeze {rev[:12]}')
    tree = git('ls-tree','-r','--name-only',rev,'--','.ufo/waves').stdout.decode()
    if 'frozen/FROZEN.md' not in tree: bad.append('R4 no frozen/FROZEN.md at the freeze')
    if not re.search(r'frozen/.*(sha256|SHA256|hashes)', tree): bad.append('R4 no pinned digest file at the freeze')
if 'w1' == spec.get('wave'): bad.append('R5 reportDir targets the voided wave')
print(json.dumps({'spec': sys.argv[1], 'verdict': 'BLOCK' if bad else 'ALLOW', 'problems': bad}, indent=1))
sys.exit(1 if bad else 0)
