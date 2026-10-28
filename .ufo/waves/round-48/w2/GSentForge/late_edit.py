#!/usr/bin/env python3
"""Realistic L1 edit: after reports land, drop the dissenting seat from the dispatch."""
import json, os, subprocess, sys
SBX='/fast/scratch/hyaku/tsukuroi-r48/GSentForge/sbx'
COUNTER='/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-scrub-admission-r48.py'
PROV='/fast/scratch/hyaku/tsukuroi-r48/GSentForge/check-wave-provenance.py'
W='.ufo/waves/round-48'; OUT='/fast/scratch/hyaku/tsukuroi-r48/GSentForge/receipts'
def sh(a): return subprocess.run(a,capture_output=True,text=True)
def git(*a):
    r=sh(['git','-C',SBX,*a]); assert r.returncode==0, r.stderr; return r.stdout
def commit(m):
    git('add','-A'); git('-c','user.name=fixture','-c','user.email=fixture@invalid','commit','-qm',m)
git('reset','-q','--hard',sys.argv[1])
# 1. a dissenting report exists, committed as filed
p=os.path.join(SBX,f'{W}/w2/R48RevGR1a.md'); lines=open(p).read().split('\n')
lines[0]='ROW GR1 VERDICT: fails'
with open(p,'w') as f: f.write('\n'.join(lines))
commit('seat filed a negative verdict')
# 2. the L1 removes the seat from the dispatch + results afterwards
d=json.load(open(os.path.join(SBX,f'{W}/w2-dispatch.json')))
d['taskCall']['tasks']=[t for t in d['taskCall']['tasks'] if t['name']!='R48RevGR1a']
d['registry']['members'].pop('R48RevGR1a',None)
d['counts']['total']=len(d['taskCall']['tasks']); d['counts']['spawn']=len(d['taskCall']['tasks'])
json.dump(d,open(os.path.join(SBX,f'{W}/w2-dispatch.json'),'w'),indent=1)
r=json.load(open(os.path.join(SBX,f'{W}/w2-results.json')))
r['results']=[e for e in r['results'] if e['name']!='R48RevGR1a']; r['seats']=len(r['results'])
json.dump(r,open(os.path.join(SBX,f'{W}/w2-results.json'),'w'),indent=1)
os.remove(p)
commit('L1 removes the dissenting seat from dispatch and results')
c=sh(['python3',COUNTER,'--lane',SBX,'--revision','HEAD'])
p2=sh(['python3',PROV,'--lane',SBX,'--revision','HEAD','--round','48','--wave','w2'])
open(f'{OUT}/late-edit-counter.json','w').write(c.stdout); open(f'{OUT}/late-edit-provenance.json','w').write(p2.stdout)
d2=json.loads(c.stdout); pr=json.loads(p2.stdout)
print(json.dumps({'counter':d2['verdict'],'counter_exit':c.returncode,
 'gr1_credited':len(d2['per_row']['GR1']['credited']),
 'provenance':pr['verdict'],'provenance_findings':pr['findings'],
 'P9':pr['checks']['P9_dispatch_not_edited_late']},indent=1))
