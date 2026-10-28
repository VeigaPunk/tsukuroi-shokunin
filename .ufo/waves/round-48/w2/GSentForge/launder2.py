#!/usr/bin/env python3
"""Stale-hash laundering: keep a `fails` verdict, break its hash line by one character."""
import json, os, subprocess, sys, hashlib
SBX='/fast/scratch/hyaku/tsukuroi-r48/GSentForge/sbx'
FROZEN='/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
COUNTER=f'{FROZEN}/tools/check-scrub-admission-r48.py'
PROV='/fast/scratch/hyaku/tsukuroi-r48/GSentForge/check-wave-provenance.py'
W='.ufo/waves/round-48'; OUT='/fast/scratch/hyaku/tsukuroi-r48/GSentForge/receipts'
CUR='fe77ac765c7dd9f568e0b296ce8c7f8f53de3d8966d6a2029bada662badf9ca8'
OLD='dcf2b0d0b4e8e9f1f2a5c3b9a0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9'
def sh(a,**k): return subprocess.run(a,capture_output=True,text=True,**k)
def git(*a):
    r=sh(['git','-C',SBX,*a])
    if r.returncode: raise SystemExit(r.stderr)
    return r.stdout
def commit(m):
    git('add','-A'); git('-c','user.name=fixture','-c','user.email=fixture@invalid','commit','-qm',m)
def probe(tag):
    c=sh(['python3',COUNTER,'--lane',SBX,'--revision','HEAD']); open(f'{OUT}/{tag}-counter.json','w').write(c.stdout)
    d=json.loads(c.stdout); g=d['per_row']['GR1']
    p=sh(['python3',PROV,'--lane',SBX,'--revision','HEAD','--round','48','--wave','w2']); open(f'{OUT}/{tag}-provenance.json','w').write(p.stdout)
    return {'counter_exit':c.returncode,'counter':d['verdict'],'gr1_credited':len(g['credited']),
            'gr1_blocking':g['blocking'],'gr1_row_ok':g['row_ok'],
            'seat':g['seats']['R48RevGR1a'],'verdicts_ok':d['verdicts_ok'],'provenance':json.loads(p.stdout)['verdict']}
B=sys.argv[1]; out={}
def rewrite(p, verdict=None, hashv=None):
    txt=open(p).read(); lines=txt.split('\n')
    if verdict: lines[0]=f'ROW GR1 VERDICT: {verdict}'
    if hashv: lines[1]=f'SECTION SHA256: {hashv}'
    with open(p,'w') as f: f.write('\n'.join(lines))

# L7: genuine fails on the CURRENT bytes, hash line scrambled -> laundered
git('reset','-q','--hard',B)
p=os.path.join(SBX,f'{W}/w2/R48RevGR1a.md')
rewrite(p, verdict='fails', hashv=OLD)
commit('launder L7: fails with stale hash')
out['L7_fails_stale_hash']=probe('L7')

# L8: fails with the correct hash -> must block (control)
git('reset','-q','--hard',B)
rewrite(p, verdict='fails', hashv=CUR); commit('control L8: fails correct hash')
out['L8_fails_correct_hash_CONTROL']=probe('L8')

# L9: fails + correct hash + <300-byte body (unbound for credit only)
git('reset','-q','--hard',B)
rewrite(p, verdict='fails', hashv=CUR)
with open(p,'w') as f: f.write(f'ROW GR1 VERDICT: fails\nSECTION SHA256: {CUR}\nThis row is wrong.\n')
commit('control L9: fails short body')
out['L9_fails_short_body']=probe('L9')

# L10: fails + correct hash + unresolvable citation
git('reset','-q','--hard',B)
rewrite(p, verdict='fails', hashv=CUR)
with open(p,'a') as f: f.write('\nSee nosuchfile.c:1 for the defect.\n')
commit('control L10: fails unresolvable citation')
out['L10_fails_bad_citation']=probe('L10')
git('reset','-q','--hard',B)
print(json.dumps(out,indent=1,sort_keys=True))
