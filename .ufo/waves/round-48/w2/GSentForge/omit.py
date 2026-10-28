#!/usr/bin/env python3
"""Omission probes: is deleting a dissenting seat free?"""
import json, os, subprocess, sys
SBX='/fast/scratch/hyaku/tsukuroi-r48/GSentForge/sbx'
FROZEN='/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
COUNTER=f'{FROZEN}/tools/check-scrub-admission-r48.py'
PROV='/fast/scratch/hyaku/tsukuroi-r48/GSentForge/check-wave-provenance.py'
W='.ufo/waves/round-48'; OUT='/fast/scratch/hyaku/tsukuroi-r48/GSentForge/receipts'
def sh(a,**k): return subprocess.run(a,capture_output=True,text=True,**k)
def git(*a):
    r=sh(['git','-C',SBX,*a])
    if r.returncode: raise SystemExit(r.stderr)
    return r.stdout
def commit(m):
    git('add','-A'); git('-c','user.name=fixture','-c','user.email=fixture@invalid','commit','-qm',m)
def rd(p): return json.load(open(os.path.join(SBX,p)))
def wr(p,o):
    with open(os.path.join(SBX,p),'w') as f: json.dump(o,f,indent=1); f.write('\n')
def probe(tag):
    c=sh(['python3',COUNTER,'--lane',SBX,'--revision','HEAD']); open(f'{OUT}/{tag}-counter.json','w').write(c.stdout)
    d=json.loads(c.stdout); g=d['per_row']['GR1']
    p=sh(['python3',PROV,'--lane',SBX,'--revision','HEAD','--round','48','--wave','w2']); open(f'{OUT}/{tag}-provenance.json','w').write(p.stdout)
    pd=json.loads(p.stdout)
    return {'counter_exit':c.returncode,'counter':d['verdict'],'gr1_credited':len(g['credited']),
            'gr1_blocking':g['blocking'],'gr1_row_ok':g['row_ok'],'verdicts_ok':d['verdicts_ok'],
            'provenance':pd['verdict'],'provenance_findings':pd['findings']}
def set_fails(p):
    txt=open(p).read(); lines=txt.split('\n'); lines[0]='ROW GR1 VERDICT: fails'
    with open(p,'w') as fh: fh.write('\n'.join(lines))
def drop_seat(update_counts):
    d=rd(f'{W}/w2-dispatch.json'); d['taskCall']['tasks']=[t for t in d['taskCall']['tasks'] if t['name']!='R48RevGR1a']
    d['registry']['members'].pop('R48RevGR1a',None)
    if update_counts: d['counts']['total']=len(d['taskCall']['tasks']); d['counts']['spawn']=len(d['taskCall']['tasks'])
    wr(f'{W}/w2-dispatch.json',d)
    r=rd(f'{W}/w2-results.json'); r['results']=[e for e in r['results'] if e['name']!='R48RevGR1a']
    if update_counts: r['seats']=len(r['results'])
    wr(f'{W}/w2-results.json',r)
    os.remove(os.path.join(SBX,f'{W}/w2/R48RevGR1a.md'))
B=sys.argv[1]; out={}
git('reset','-q','--hard',B); out['O0_clean']=probe('omit-O0')
# O1: emptied report AND results entry with no verdict (P5 blind spot probe)
git('reset','-q','--hard',B)
p=os.path.join(SBX,f'{W}/w2/R48RevGR1a.md')
with open(p,'w') as fh: fh.write('')
r=rd(f'{W}/w2-results.json')
for e in r['results']:
    if e['name']=='R48RevGR1a': e['output']=json.dumps({'report':f'{W}/w2/R48RevGR1a.md','row':'GR1'},indent=2)
wr(f'{W}/w2-results.json',r); commit('omit O1: blank report, verdict-free output')
out['O1_blanked_seat']=probe('omit-O1')
# O2: dissenting seat, deleted from dispatch+results+report (stale counts)
git('reset','-q','--hard',B)
set_fails(os.path.join(SBX,f'{W}/w2/R48RevGR1a.md')); drop_seat(False); commit('omit O2: delete dissenting seat')
out['O2_deleted_negative']=probe('omit-O2')
# O3: same, but counts/seats/registry kept consistent
git('reset','-q','--hard',B)
set_fails(os.path.join(SBX,f'{W}/w2/R48RevGR1a.md')); drop_seat(True); commit('omit O3: delete dissenting seat, coherent counts')
out['O3_deleted_negative_coherent']=probe('omit-O3')
git('reset','-q','--hard',B)
print(json.dumps(out,indent=1,sort_keys=True))
