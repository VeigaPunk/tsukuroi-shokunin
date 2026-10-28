import json, subprocess, hashlib, os, sys
S = os.environ['S']; D = open(os.path.join(S, 'fxdir')).read().strip()
PIN = '2732ee6c06108c031c4d8043239b994e0504eb2f'
K = '/home/vgpnk/Projects/shokunin/kumitate-shokunin'
OLD = '1770305fae20826b39905a8251ddeca6b4957ac4'
NEW = subprocess.run(['git','-C',K,'rev-parse','76bdda4bde02522829598c1c81f1836ffbea8d34'],capture_output=True,text=True,check=True).stdout.strip()
newblob = subprocess.run(['git','-C',K,'show',f'{NEW}:PROVINCE.md'],capture_output=True,check=True).stdout
NEW_SHA = hashlib.sha256(newblob).hexdigest()
OLD_SHA = 'fcd69667a1027d5edd07a8ff0390a716a467aff92719071e33cb6157673b665f'
QUOTE_OLD = '**Domain:** orchestration & tooling — scopes OMP task/hub, ufo-fsd scripts & runtime'
QUOTE_NEW = '**Refuses:** anything outside this domain; report cross-domain evidence back to the orchestrator rather than absorbing it.'
print('NEW', NEW, NEW_SHA)
def git(*a, inp=None):
    r = subprocess.run(['git','-C',D,'-c','user.name=fixture','-c','user.email=fixture@invalid',*a],capture_output=True,text=True)
    if r.returncode: raise SystemExit(f'git {a} rc={r.returncode} {r.stderr}')
    return r.stdout.strip()
def show(path):
    return subprocess.run(['git','-C',D,'show',f'{PIN}:{path}'],capture_output=True,check=True).stdout.decode('utf-8')
def rep(text, old, new, count=1):
    n = text.count(old)
    assert n == count, (old[:60], n)
    return text.replace(old, new)
def variant(name, prov_edit, reg_edit, snapshot=False, extra=None):
    git('checkout','-q','--detach',PIN)
    prov = show('PROVINCE.md'); reg = json.loads(show('corpus/knowledge/adjacency-anchors-r19.json'))
    prov = prov_edit(prov)
    for r in reg['outbound']:
        if r['id'] == 'OUT-006':
            reg_edit(r)
    with open(os.path.join(D,'PROVINCE.md'),'w',encoding='utf-8') as f: f.write(prov)
    with open(os.path.join(D,'corpus/knowledge/adjacency-anchors-r19.json'),'w',encoding='utf-8') as f:
        json.dump(reg,f,ensure_ascii=False,indent=2); f.write('\n')
    if snapshot:
        p = os.path.join(D,'.ufo/waves/round-19/l1-capture/siblings/kumitate/76bdda4bde02/PROVINCE.md')
        os.makedirs(os.path.dirname(p),exist_ok=True); open(p,'wb').write(newblob)
    git('add','-A'); git('commit','-q','-m',f'fixture {name}')
    sha = git('rev-parse','HEAD')
    git('update-ref','refs/heads/master',sha); git('update-ref','-d','refs/remotes/origin/master')
    print(name, sha)
    return sha
def fix_row(line_prefix, subs):
    def f(prov):
        lines = prov.split('\n'); hits=[i for i,l in enumerate(lines) if l.startswith(line_prefix)]
        assert len(hits)==1, (line_prefix, hits)
        i=hits[0]
        for a,b in subs:
            assert lines[i].count(a)==1, (line_prefix, a)
            lines[i]=lines[i].replace(a,b)
        return '\n'.join(lines)
    return f
def compose(*fs):
    def f(x):
        for g in fs: x = g(x)
        return x
    return f
# ADJ-05 -> kama anchor, ADJ-01 -> Core anchor (coordinated relink)
adj05 = fix_row('| ADJ-05 |', [('`OUT-006`, `OUT-007` |','`OUT-002` |')])
adj01 = fix_row('| ADJ-01 |', [('`OUT-002` |','`OUT-001` |')])
out002 = fix_row('| OUT-002 |', [('| ADJ-01 |','| ADJ-05 |')])
out001 = fix_row('| OUT-001 |', [('| Core |','| ADJ-01 |')])
relink_minimal = adj05
relink_full = compose(adj05, adj01, out002, out001)
# OUT-006 displayed row + digest line
out006_row = fix_row('| OUT-006 |', [('`1770305fae20`','`76bdda4bde02`')])
out006_quote = fix_row('| OUT-006 |', [(QUOTE_OLD,QUOTE_NEW)])
digest_line = fix_row('- OUT-006 ', [(OLD,NEW),(OLD_SHA,NEW_SHA)])
digest_quote_only_pin = None
def reg_quote_only(r):
    r['quote']=QUOTE_NEW; r['quote_line']=6
def reg_commit_only(r):
    r['sibling_commit']=NEW; r['sibling_blob_sha256']=NEW_SHA
def reg_commit_snap(r):
    reg_commit_only(r); r['snapshot']='.ufo/waves/round-19/l1-capture/siblings/kumitate/76bdda4bde02/PROVINCE.md'
prov_commit_only = compose(out006_row, digest_line)
prov_quote_only = out006_quote
prov_full = compose(out006_row, out006_quote, digest_line)
def nop(r): pass
which = sys.argv[1:]
R = {}
V = {
 'V1-relink-minimal': (relink_minimal, nop, False),
 'V2-relink-coordinated': (relink_full, nop, False),
 'V3-quote-swap-same-pin': (prov_quote_only, reg_quote_only, False),
 'V4-commit-swap-no-snapshot': (prov_commit_only, reg_commit_only, False),
 'V5-commit-swap-with-snapshot': (prov_commit_only, reg_commit_snap, True),
 'V6-full-coordinated': (compose(out006_row, out006_quote, digest_line), lambda r: (reg_commit_snap(r), reg_quote_only(r)), True),
 'V7-table-only-quote': (prov_quote_only, nop, False),
 'V8-table-only-commit': (prov_commit_only, nop, False),
 'V9-registry-only-commit': (lambda p: p, reg_commit_snap, True),
}
for n in (which or V.keys()):
    pe, re_, snap = V[n]
    R[n] = variant(n, pe, re_, snap)
json.dump(R, open(os.path.join(S,'variants.json'),'w'), indent=1)
git('checkout','-q','--detach',PIN)
