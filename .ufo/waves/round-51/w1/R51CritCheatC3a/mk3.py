import json, subprocess, hashlib, os
S=os.environ['S']; D=open(os.path.join(S,'fxdir')).read().strip()
PIN='2732ee6c06108c031c4d8043239b994e0504eb2f'; K='/home/vgpnk/Projects/shokunin/kumitate-shokunin'
OLD='1770305fae20826b39905a8251ddeca6b4957ac4'; OLD_SHA='fcd69667a1027d5edd07a8ff0390a716a467aff92719071e33cb6157673b665f'
QUOTE_OLD='**Domain:** orchestration & tooling — scopes OMP task/hub, ufo-fsd scripts & runtime'
def git(*a):
    r=subprocess.run(['git','-C',D,'-c','user.name=fixture','-c','user.email=fixture@invalid',*a],capture_output=True,text=True)
    if r.returncode: raise SystemExit(f'git {a} {r.stderr}')
    return r.stdout.strip()
def show(path): return subprocess.run(['git','-C',D,'show',f'{PIN}:{path}'],capture_output=True,check=True).stdout.decode()
def fix_row(prefix, subs):
    def f(prov):
        lines=prov.split('\n'); hits=[i for i,l in enumerate(lines) if l.startswith(prefix)]; assert len(hits)==1,(prefix,hits); i=hits[0]
        for a,b in subs: assert lines[i].count(a)==1,(prefix,a); lines[i]=lines[i].replace(a,b)
        return '\n'.join(lines)
    return f
def compose(*fs):
    def f(x):
        for g in fs: x=g(x)
        return x
    return f
def variant(name, prov_edit, reg_fn=None, snapshot=None):
    git('checkout','-q','--detach',PIN)
    prov=prov_edit(show('PROVINCE.md'))
    open(os.path.join(D,'PROVINCE.md'),'w',encoding='utf-8').write(prov)
    if reg_fn:
        reg=json.loads(show('corpus/knowledge/adjacency-anchors-r19.json')); reg_fn(reg)
        open(os.path.join(D,'corpus/knowledge/adjacency-anchors-r19.json'),'w',encoding='utf-8').write(json.dumps(reg,ensure_ascii=False,indent=2)+'\n')
    if snapshot:
        p,b=snapshot; fp=os.path.join(D,p); os.makedirs(os.path.dirname(fp),exist_ok=True); open(fp,'wb').write(b)
    git('add','-A'); git('commit','-q','-m',f'fixture {name}'); sha=git('rev-parse','HEAD')
    git('update-ref','refs/heads/master',sha); git('update-ref','-d','refs/remotes/origin/master')
    print(name,sha); return sha
TIP='76bdda4bde02522829598c1c81f1836ffbea8d34'
adj05=fix_row('| ADJ-05 |',[('`OUT-006`, `OUT-007` |','`OUT-002`, `OUT-007` |')])
adj01=fix_row('| ADJ-01 |',[('`OUT-002` |','`OUT-001` |')])
out002=fix_row('| OUT-002 |',[('| ADJ-01 |','| ADJ-05 |')])
out001=fix_row('| OUT-001 |',[('| Core |','| ADJ-01 |')])
R={}
R['V2c-relink-only']=variant('V2c-relink-only', compose(adj05,adj01,out002,out001))
# V11: quote from section OUTSIDE the declared heading (line 11 bullet substring), registry+table consistent
L11='gated by `scripts/claims-check.mjs` + `scripts/proxy-check.mjs` (`coverage_script`).'
KB=subprocess.run(['git','-C',K,'show',OLD+':PROVINCE.md'],capture_output=True,check=True).stdout.decode().split('\n')
L11N=[i+1 for i,l in enumerate(KB) if L11 in l]; assert L11N, 'no line'; L11N=L11N[0]; print('L11 line',L11N)
def reg11(r):
    for x in r['outbound']:
        if x['id']=='OUT-006': x['quote']=L11; x['quote_line']=L11N
q11=lambda p: fix_row('| OUT-006 |',[(QUOTE_OLD,L11)])(p)
R['V11-quote-outside-section']=variant('V11-quote-outside-section', q11, reg11)
json.dump(R,open(os.path.join(S,'variants3.json'),'w'),indent=1)
git('checkout','-q','--detach',PIN)
