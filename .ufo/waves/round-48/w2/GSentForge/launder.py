#!/usr/bin/env python3
"""Negative laundering: can a blocking verdict be erased by a one-line binding slip?"""
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
def verdict(tag):
    c=sh(['python3',COUNTER,'--lane',SBX,'--revision','HEAD'])
    open(f'{OUT}/{tag}-counter.json','w').write(c.stdout)
    d=json.loads(c.stdout); g=d['per_row']['GR1']
    p=sh(['python3',PROV,'--lane',SBX,'--revision','HEAD','--round','48','--wave','w2'])
    open(f'{OUT}/{tag}-provenance.json','w').write(p.stdout)
    pd=json.loads(p.stdout)
    return {'counter_exit':c.returncode,'counter':d['verdict'],'gr1_credited':len(g['credited']),
            'gr1_blocking':g['blocking'],'gr1_row_ok':g['row_ok'],'verdicts_ok':d['verdicts_ok'],
            'provenance':pd['verdict'],'provenance_findings':pd['findings']}
def set_verdict(txt,new):
    lines=txt.split('\n'); lines[0]=f'ROW GR1 VERDICT: {new}'.rstrip(); return '\n'.join(lines)
B=sys.argv[1]; out={}
for tag,mutate in [
 ('L6_emptied_report', 'empty'),
 ('L0_clean_holds', None),
 ('L1_fails_bound', 'fails'),
 ('L2_fails_dup_dispatch', 'fails+dup'),
 ('L3_fails_role_mismatch', 'fails+role'),
 ('L4_partly_dup_dispatch', 'partly+dup'),
 ('L5_fails_dup_dispatch_order', 'fails+dup_order'),
]:
    if False: pass
    git('reset','-q','--hard',B)
    if mutate == 'empty':
        p=os.path.join(SBX,f'{W}/w2/R48RevGR1a.md')
        with open(p,'w') as fh: fh.write('')
        commit('launder probe '+tag)
    elif mutate:
        p=os.path.join(SBX,f'{W}/w2/R48RevGR1a.md')
        txt=open(p).read()
        with open(p,'w') as fh: fh.write(set_verdict(txt, mutate.split('+')[0]))
        if 'dup' in mutate:
            d=rd(f'{W}/w2-dispatch.json')
            if 'order' in mutate:
                d['taskCall']['tasks'].insert(0,dict(d['taskCall']['tasks'][0]))
            else:
                d['taskCall']['tasks'].append(dict(d['taskCall']['tasks'][0]))
            wr(f'{W}/w2-dispatch.json',d)
        if 'role' in mutate:
            r=rd(f'{W}/w2-results.json')
            for e in r['results']:
                if e['name']=='R48RevGR1a': e['agent']='critic'
            wr(f'{W}/w2-results.json',r)
        commit('launder probe '+tag)
    out[tag]=verdict(tag)
git('reset','-q','--hard',B)
print(json.dumps(out,indent=1,sort_keys=True))
