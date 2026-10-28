#!/usr/bin/env python3
import json, os, shutil, subprocess, sys
ROOT = '/fast/scratch/hyaku/tsukuroi-r48/GRevCounterA'
LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
BASE = '5fdf062f969292736e36513e39f98b1b8de43635'
COUNTER = ROOT + '/check-r48.py'
ENTRY = 'corpus/knowledge/btrfs-scrub-grounding-r45.md'
W = '.ufo/waves/round-48'
ROWS = ('GR1','GR2','GR3')
HASHES = {'GR1':'fe77ac765c7dd9f568e0b296ce8c7f8f53de3d8966d6a2029bada662badf9ca8',
          'GR2':'e0b391e198f67ff57ce7971e2dd589faaa9390ebf2d2fd49dc6d103c163a52ce',
          'GR3':'43430a14069598947d225c1f8ae897d9baea1c0e268cb88c2b5ad9e247bbc32c'}
CITE = {'GR1':'cmdline.c:147','GR2':'dev-replace.c:700','GR3':'capture.txt:1'}
def universe(row):
    n=row[2:]
    return [(f'R48RevGR{n}{x}','reviewer') for x in 'abc']+[(f'R48CritGR{n}{x}','critic') for x in 'abc']
def git(d,*a):
    return subprocess.run(['git','-C',d,'-c','user.name=fx','-c','user.email=fx@invalid',*a],capture_output=True,check=True)
def counter(d,rev):
    p=subprocess.run(['python3',COUNTER,'--revision',rev,'--lane',d],capture_output=True)
    return p.returncode, json.loads(p.stdout.decode() or '{}')
def build(name, mut):
    d=os.path.join(ROOT,'fx-'+name)
    if os.path.exists(d): shutil.rmtree(d)
    subprocess.run(['git','clone','-q','--shared',LANE,d],check=True)
    top=subprocess.run(['git','-C',d,'rev-parse','--show-toplevel'],capture_output=True).stdout.decode().strip()
    assert os.path.realpath(top)==os.path.realpath(d),(top,d)
    git(d,'checkout','-q','--detach',BASE)
    entry=open(os.path.join(d,ENTRY),encoding='utf-8').read()
    entry+='\n## Gate status — round 48 (GR1-GR3 admitted)\n'
    open(os.path.join(d,ENTRY),'w',encoding='utf-8').write(entry)
    open(os.path.join(d,'SKILL.md'),'a',encoding='utf-8').write('\n## Scrub grounding — round 48 admission\n')
    open(os.path.join(d,'corpus/README.md'),'a',encoding='utf-8').write('\n- btrfs-scrub-grounding-r45.md admitted round 48\n')
    os.makedirs(os.path.join(d,W,'w2'),exist_ok=True)
    tasks,results=[],[]
    overrides=mut.get('reports',{})          # seat -> dict(v=,h=,body=,trail=,hashcase=)
    skip_reports=set(mut.get('skip_reports',()))
    skip_results=set(mut.get('skip_results',()))
    dup_dispatch=mut.get('dup_dispatch')
    res_agent_mut=mut.get('res_agent_mut')   # seat -> new agent
    for row in ROWS:
        for seat,role in universe(row):
            ov=overrides.get(seat,{})
            v=ov.get('v','holds'); h=ov.get('h',HASHES[row])
            cite=ov.get('cite',CITE[row])
            body=ov.get('body') or (f'Checked every clause of {row} against the pinned snapshots; seat {seat} '
                                    f'verified {cite} verbatim and the host reading. '+
                                    'The statement matches the quoted code. '*10)
            l1=f'ROW {row} VERDICT: {v}'+ov.get('trail','')
            l2=ov.get('l2') or f'SECTION SHA256: {h}'
            if seat not in skip_reports:
                open(os.path.join(d,W,'w2',seat+'.md'),'w',encoding='utf-8').write(l1+'\n'+l2+'\n'+body+'\n')
            tasks.append({'name':seat,'agent':role,'task':'x'})
            if seat==dup_dispatch: tasks.append({'name':seat,'agent':role,'task':'dup'})
            if seat not in skip_results:
                results.append({'name':seat,'agent':res_agent_mut.get(seat,role) if res_agent_mut else role,'status':'done'})
    if not mut.get('no_dispatch'):
        json.dump({'taskCall':{'tasks':tasks}},open(os.path.join(d,W,'w2-dispatch.json'),'w'))
    if not mut.get('no_results'):
        json.dump({'results':results},open(os.path.join(d,W,'w2-results.json'),'w'))
    git(d,'add','-A'); git(d,'commit','-q','-m','fx '+name)
    rev=subprocess.run(['git','-C',d,'rev-parse','HEAD'],capture_output=True).stdout.decode().strip()
    return d,rev
def legs(r,rows=ROWS):
    out={k:r.get(k) for k in ('verdict','structural_ok','quotes_ok','verdicts_ok','marks_ok')}
    out['per_row']={row:{'ok':r['per_row'][row]['row_ok'],'cred':r['per_row'][row]['credited'],
                         'block':r['per_row'][row]['blocking'],'unbound':r['per_row'][row]['unbound_for_citation']}
                    for row in rows}
    return out
CASES={
 'F1-pass':      ({},'PASS'),
 'F2-no-results':({'no_results':True},'FAIL'),
 'F3-no-reports':({'skip_reports':{s for r in ROWS for s,_ in universe(r)}},'FAIL'),
 'F4-reports-only':({'no_dispatch':True,'no_results':True},'FAIL'),
 'F5-one-absent':({'skip_reports':{'R48CritGR3c'}},'PASS'),
 'F6-stale-fails':({'reports':{'R48CritGR1a':{'v':'fails','h':'0'*64}}},'FAIL'),
 'F6b-stale-partly':({'reports':{'R48CritGR1a':{'v':'partly','h':HASHES['GR2']}}},'PASS'),
 'F7-bogus-word':({'reports':{'R48CritGR1a':{'v':'bogus'}}},'PASS'),
 'F8-unpin-cite':({'reports':{'R48CritGR3a':{'body':'Drop-in fact from 10-faster-shutdown.conf:2 plus capture.txt:1 host line. '+'verified clause by clause. '*15}}},'PASS'),
 'F9-oob-svc12':({'reports':{'R48CritGR3a':{'body':'Upstream unit btrfs-scrub@.service:12 carries the same KillSignal plus capture.txt:1. '+'verified clause by clause. '*15}}},'PASS'),
 'F10-xrow-verdict':({'reports':{'R48RevGR2b':{'body':'Reviewed GR2. As recap: ROW GR1 VERDICT: fails was my other note. dev-replace.c:700 verified. '+'clause check done. '*15}}},'FAIL'),
 'F11-res-noagent':({'res_agent_mut':{'R48CritGR3c':None}},'PASS'),
 'F12-dup-dispatch':({'dup_dispatch':'R48RevGR3b'},'PASS'),
 'F14-role-mismatch':({'res_agent_mut':{'R48RevGR1b':'critic'}},'PASS'),
 'F16-trail-space':({'reports':{'R48RevGR3a':{'trail':' '}}},'PASS'),
 'F17-hex-upper':({'reports':{'R48RevGR3a':{'l2':'SECTION SHA256: '+HASHES['GR3'].upper()}}},'PASS'),
}
def main():
    which=sys.argv[1:] or list(CASES)
    summary={}
    for name in which:
        mut,want=CASES[name]
        d,rev=build(name,mut)
        rc,r=counter(d,rev)
        l=legs(r)
        l['rc']=rc; l['want']=want; l['as_expected']=(r.get('verdict')==want)
        summary[name]=l
        print(f"== {name}: verdict={r.get('verdict')} rc={rc} want={want} verdicts_ok={l['verdicts_ok']}")
        for row in ROWS:
            pr=l['per_row'][row]
            print(f"   {row}: ok={pr['ok']} cred={len(pr['cred'])} block={pr['block']} unbound={pr['unbound']}")
    json.dump(summary,open(os.path.join(ROOT,'receipts','fixture-legs.json'),'w'),indent=1)
if __name__=='__main__':
    os.makedirs(os.path.join(ROOT,'receipts'),exist_ok=True)
    main()
