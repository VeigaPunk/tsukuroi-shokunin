#!/usr/bin/env python3
"""Run BOTH the frozen counter and the provenance check on T7-T10 and on a
partly-with-stale-hash probe, so the report table is measured, not inferred."""
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
def both(tag):
    c=sh(['python3',COUNTER,'--lane',SBX,'--revision','HEAD']); open(f'{OUT}/{tag}-counter.json','w').write(c.stdout)
    p=sh(['python3',PROV,'--lane',SBX,'--revision','HEAD','--round','48','--wave','w2']); open(f'{OUT}/{tag}-provenance.json','w').write(p.stdout)
    d=json.loads(c.stdout); q=json.loads(p.stdout)
    return {'counter':d['verdict'],'gr1_credited':len(d['per_row']['GR1']['credited']),
            'gr1_blocking':d['per_row']['GR1']['blocking'],'any_fails':d['per_row']['GR1']['any_fails'],
            'provenance':q['verdict'],'provenance_findings':q['findings']}
B=sys.argv[1]; out={}
def md(n): return os.path.join(SBX,f'{W}/w2/{n}.md')
def setfirst(seat,val):
    t=open(md(seat)).read().split('\n'); t[0]=f'ROW GR1 VERDICT: {val}'
    with open(md(seat),'w') as f: f.write('\n'.join(t))

# T7 duplicate dispatch entry
git('reset','-q','--hard',B)
d=json.load(open(os.path.join(SBX,f'{W}/w2-dispatch.json')))
d['taskCall']['tasks'].append(dict(d['taskCall']['tasks'][0]))
json.dump(d,open(os.path.join(SBX,f'{W}/w2-dispatch.json'),'w'),indent=1); commit('T7')
out['T7_duplicate_dispatch']=both('T7')
# T8 results role mismatch
git('reset','-q','--hard',B)
r=json.load(open(os.path.join(SBX,f'{W}/w2-results.json')))
for e in r['results']:
    if e['name']=='R48RevGR1a': e['agent']='critic'
json.dump(r,open(os.path.join(SBX,f'{W}/w2-results.json'),'w'),indent=1); commit('T8')
out['T8_role_mismatch']=both('T8')
# T9 duplicate results entry
git('reset','-q','--hard',B)
r=json.load(open(os.path.join(SBX,f'{W}/w2-results.json')))
r['results'].append(dict(r['results'][0]))
json.dump(r,open(os.path.join(SBX,f'{W}/w2-results.json'),'w'),indent=1); commit('T9')
out['T9_duplicate_results']=both('T9')
# T10 CRLF
git('reset','-q','--hard',B)
data=open(md('R48RevGR1a')).read().replace('\n','\r\n')
open(md('R48RevGR1a'),'w',newline='').write(data); commit('T10')
out['T10_crlf']=both('T10')
# P1: partly WITH A STALE HASH (no dup) -- is a dissent on other bytes ever noticed?
git('reset','-q','--hard',B)
t=open(md('R48RevGR1a')).read().split('\n')
t[0]='ROW GR1 VERDICT: partly'
t[1]='SECTION SHA256: dcf2b0d0b4e8e9f1f2a5c3b9a0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9'
with open(md('R48RevGR1a'),'w') as f: f.write('\n'.join(t))
commit('partly on a stale hash')
out['P1_partly_stale_hash']=both('P1-partly-stale')
# P2: fails with a stale hash (why did L7 fail? any_fails?)
git('reset','-q','--hard',B)
t=open(md('R48RevGR1a')).read().split('\n')
t[0]='ROW GR1 VERDICT: fails'
t[1]='SECTION SHA256: dcf2b0d0b4e8e9f1f2a5c3b9a0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9'
with open(md('R48RevGR1a'),'w') as f: f.write('\n'.join(t))
commit('fails on a stale hash')
out['P2_fails_stale_hash']=both('P2-fails-stale')
git('reset','-q','--hard',B)
print(json.dumps(out,indent=1,sort_keys=True))
