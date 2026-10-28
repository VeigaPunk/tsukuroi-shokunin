import json, subprocess, hashlib, os, sys
S = os.environ['S']; D = open(os.path.join(S, 'fxdir')).read().strip()
PIN = '2732ee6c06108c031c4d8043239b994e0504eb2f'
K = '/home/vgpnk/Projects/shokunin/kumitate-shokunin'
OLD = '1770305fae20826b39905a8251ddeca6b4957ac4'
QUOTE_OLD = '**Domain:** orchestration & tooling — scopes OMP task/hub, ufo-fsd scripts & runtime'
QUOTE_NEW = '**Refuses:** anything outside this domain; report cross-domain evidence back to the orchestrator rather than absorbing it.'
OLD_SHA = 'fcd69667a1027d5edd07a8ff0390a716a467aff92719071e33cb6157673b665f'
def git(*a):
    r = subprocess.run(['git','-C',D,'-c','user.name=fixture','-c','user.email=fixture@invalid',*a],capture_output=True,text=True)
    if r.returncode: raise SystemExit(f'git {a} rc={r.returncode} {r.stderr}')
    return r.stdout.strip()
def show(path): return subprocess.run(['git','-C',D,'show',f'{PIN}:{path}'],capture_output=True,check=True).stdout.decode('utf-8')
def fix_row(prefix, subs):
    def f(prov):
        lines = prov.split('\n'); hits=[i for i,l in enumerate(lines) if l.startswith(prefix)]
        assert len(hits)==1, (prefix, hits); i=hits[0]
        for a,b in subs:
            assert lines[i].count(a)==1, (prefix,a); lines[i]=lines[i].replace(a,b)
        return '\n'.join(lines)
    return f
def compose(*fs):
    def f(x):
        for g in fs: x=g(x)
        return x
    return f
def variant(name, newc, prov_edit, reg_edit):
    git('checkout','-q','--detach',PIN)
    newblob = subprocess.run(['git','-C',K,'show',f'{newc}:PROVINCE.md'],capture_output=True,check=True).stdout
    nsha = hashlib.sha256(newblob).hexdigest()
    prov = prov_edit(show('PROVINCE.md'))
    reg = json.loads(show('corpus/knowledge/adjacency-anchors-r19.json'))
    for r in reg['outbound']:
        if r['id']=='OUT-006':
            r['sibling_commit']=newc; r['sibling_blob_sha256']=nsha
            r['snapshot']=f'.ufo/waves/round-19/l1-capture/siblings/kumitate/{newc[:12]}/PROVINCE.md'
            r['quote']=QUOTE_NEW; r['quote_line']=6
    p=os.path.join(D,'PROVINCE.md'); open(p,'w',encoding='utf-8').write(prov)
    open(os.path.join(D,'corpus/knowledge/adjacency-anchors-r19.json'),'w',encoding='utf-8').write(json.dumps(reg,ensure_ascii=False,indent=2)+'\n')
    sp=os.path.join(D,f'.ufo/waves/round-19/l1-capture/siblings/kumitate/{newc[:12]}/PROVINCE.md')
    os.makedirs(os.path.dirname(sp),exist_ok=True); open(sp,'wb').write(newblob)
    git('add','-A'); git('commit','-q','-m',f'fixture {name}')
    sha=git('rev-parse','HEAD'); git('update-ref','refs/heads/master',sha)
    git('update-ref','-d','refs/remotes/origin/master')
    print(name, sha, 'newc', newc, 'nsha', nsha[:16]); return sha
TIP = subprocess.run(['git','-C',K,'rev-parse','76bdda4bde02522829598c1c81f1836ffbea8d34'],capture_output=True,text=True).stdout.strip()
OFF = '4bc966c4febd9ada521b91897b90dfde09e71ef1'
OFF = subprocess.run(['git','-C',K,'rev-parse',OFF],capture_output=True,text=True,check=True).stdout.strip()
adj05 = fix_row('| ADJ-05 |', [('`OUT-006`, `OUT-007` |','`OUT-002`, `OUT-007` |')])
adj01 = fix_row('| ADJ-01 |', [('`OUT-002` |','`OUT-001` |')])
out002 = fix_row('| OUT-002 |', [('| ADJ-01 |','| ADJ-05 |')])
out001 = fix_row('| OUT-001 |', [('| Core |','| ADJ-01 |')])
out006_row = fix_row('| OUT-006 |', [('`1770305fae20`','`%s`' % TIP[:12]), (QUOTE_OLD, QUOTE_NEW)])
digest = lambda newc, nsha: fix_row('- OUT-006 ', [(OLD, newc), (OLD_SHA, nsha)])
R = {}
R['V2b-relink-keep-OUT007'] = variant('V2b-relink-keep-OUT007', TIP, compose(adj05, adj01, out002, out001, fix_row('| OUT-006 |', [('`1770305fae20`','`%s`' % TIP[:12]), (QUOTE_OLD, QUOTE_NEW)]), fix_row('- OUT-006 ', [(OLD, TIP), (OLD_SHA, subprocess.run(['sha256sum'], input=subprocess.run(['git','-C',K,'show',TIP+':PROVINCE.md'],capture_output=True).stdout, capture_output=True).stdout.decode().split()[0])])), lambda r: None)
# V10: the spec forgery (quote swap + digest swap) to an OFF-master commit (only jj keep ref)
newblob_off = subprocess.run(['git','-C',K,'show',f'{OFF}:PROVINCE.md'],capture_output=True,check=True).stdout
off_sha = hashlib.sha256(newblob_off).hexdigest()
def prov_off(p):
    p = fix_row('| OUT-006 |', [('`1770305fae20`','`%s`' % OFF[:12]), (QUOTE_OLD, QUOTE_NEW)])(p)
    return fix_row('- OUT-006 ', [(OLD, OFF),(OLD_SHA, off_sha)])(p)
R['V10-offmaster-full'] = variant('V10-offmaster-full', OFF, prov_off, lambda r: None)
json.dump(R, open(os.path.join(S,'variants2.json'),'w'), indent=1)
git('checkout','-q','--detach',PIN)
