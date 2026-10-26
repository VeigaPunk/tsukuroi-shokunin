import functools, json, locale, os, pathlib, re, subprocess, sys
repo = pathlib.Path(sys.argv[1]); S=os.environ['S']
cap = repo/'.ufo/waves/round-38/frozen/hooks-capture'
DIRS=(('usr','usr-share-libalpm-hooks'),('etc','etc-pacman.d-hooks'))
SUF='.hook'
def parse(p):
    section=when=None; abort=needs=False; exec0=None; triggers=0
    for raw in p.read_text(errors='replace').splitlines():
        line=raw.strip()
        if not line or line.startswith('#'): continue
        if line.startswith('[') and line.endswith(']'):
            section=line[1:-1]
            if section=='Trigger': triggers+=1
            continue
        k,_,v=line.partition('='); k,v=k.strip(),v.strip()
        if section!='Action': continue
        if k=='When': when=v
        elif k=='AbortOnFail': abort=True
        elif k=='NeedsTargets': needs=True
        elif k=='Exec': exec0=v.split()[0] if v.split() else ''
    return when,abort,needs,exec0 or '-',triggers
files={}
for tag,sub in DIRS:
    for p in sorted((cap/sub).iterdir()):
        if p.name.endswith(SUF) and not p.is_dir(): files[(tag,p.name)]=parse(p)
def key(n): return n[:-len(SUF)].encode()
def rows_from(seq):
    pos={'PreTransaction':0,'PostTransaction':0}; out=[]
    for tag,n in seq:
        w,a,nd,e,tr=files[(tag,n)]
        if tr==0:
            out.append(('masked','-',n,tag,'yes' if a else 'no','yes' if nd else 'no',e)); continue
        pos[w]+=1
        out.append((w,str(pos[w]),n,tag,'yes' if a else 'no','yes' if nd else 'no',e))
    return out
def dedup(seq):
    seen=set(); out=[]
    for tag,n in seq:
        if n in seen: continue
        seen.add(n); out.append((tag,n))
    return out
def render(rows):
    lines=['| when | pos | name | dir | abort | needs | exec |','|---|---|---|---|---|---|---|']
    for r in rows: lines.append('| '+' | '.join(r[:6])+f' | `{r[6]}` |')
    return '\n'.join(lines)
DOC='''source: S999 in `corpus/SOURCES.md` — control row for counter isolation
verified-at: 2026-10-26

# Control: cheap table

## Effective hook order (r38 capture)

{}

## Control notes

- [obs] table only; no rule text, no source reading.
'''
def entry(rows): return DOC.format(render(rows))
usr=[('usr',p.name) for p in sorted((cap/'usr-share-libalpm-hooks').iterdir()) if p.name.endswith(SUF)]
etc=[('etc',p.name) for p in sorted((cap/'etc-pacman.d-hooks').iterdir()) if p.name.endswith(SUF)]
allrows=usr+etc
ctl={}
ctl['lsdir-usr-then-etc']=rows_from(allrows)
ctl['dup-bytefull-global']=rows_from(sorted(allrows,key=lambda t:t[1].encode()))
def sort_dedup(namekey, rank):
    seq=sorted(allrows,key=lambda t:(namekey(t[1]), rank[t[0]]))
    return rows_from(dedup(seq))
ctl['dedup-bytefull-global']=sort_dedup(lambda n:n.encode(), {'etc':0,'usr':1})
locale.setlocale(locale.LC_ALL,'en_US.UTF-8')
ctl['dedup-enUSfull-global']=sort_dedup(locale.strxfrm, {'etc':0,'usr':1})
man=[l.split('  ',1)[1] for l in (cap/'MANIFEST.sha256').read_text().splitlines() if '  ' in l]
mseq=[('usr' if r.startswith('usr') else 'etc', pathlib.PurePosixPath(r).name) for r in man]
ctl['manifest-line-order']=rows_from(dedup(mseq))
ctl['stripC-dedup-usrfirst']=sort_dedup(key, {'usr':0,'etc':1})
ctl['stripC-dedup-etcfirst']=sort_dedup(key, {'etc':0,'usr':1})
ctl['lsdir-dedup-usrfirst']=rows_from(dedup(allrows))
ctl['lsdir-dedup-etcfirst']=rows_from(dedup([r for r in allrows if r[0]=='usr' and r[1] not in {n for _,n in etc}]+etc))
log=pathlib.Path('/var/log/pacman.log').read_text(errors='replace')
names=[]; 
for m in re.finditer(r"running '([^']+)'", log):
    if m.group(1) not in names: names.append(m.group(1))
name2tag={n:tag for tag,n in files}
ctl['pacmanlog-firstseen']=rows_from([(name2tag[n],n) for n in names if n in name2tag])
base=repo/'corpus/knowledge/pacman-hook-order-r38.md'
summary=[]
# baseline
sha0=subprocess.run(['git','-C',str(repo),'rev-parse','HEAD'],capture_output=True,text=True).stdout.strip()
r0=subprocess.run(['python3',str(repo/'tools/check-hook-order-r38.py'),'--repo',str(repo),'--revision',sha0],capture_output=True,text=True)
j0=json.loads(r0.stdout); summary.append(('baseline-real-entry',j0['rows_expected'],j0['rows_matched'],j0['mismatches'],j0['extra_rows'],j0['source_ok'],j0['result']))
for name,rows in ctl.items():
    base.write_text(entry(rows))
    subprocess.run(['git','-C',str(repo),'-c','user.name=ctl','-c','user.email=ctl@invalid','commit','-q','-am',f'control {name}'],check=True)
    sha=subprocess.run(['git','-C',str(repo),'rev-parse','HEAD'],capture_output=True,text=True).stdout.strip()
    out=subprocess.run(['python3',str(repo/'tools/check-hook-order-r38.py'),'--repo',str(repo),'--revision',sha],capture_output=True,text=True)
    j=json.loads(out.stdout)
    open(f'{S}/{name}.json','w').write(out.stdout)
    summary.append((name,j['rows_expected'],j['rows_matched'],j['mismatches'],j['extra_rows'],j['source_ok'],j['result']))
for row in summary: print('|'.join(map(str,row)))
