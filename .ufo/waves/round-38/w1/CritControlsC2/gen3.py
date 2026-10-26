import functools, json, locale, os, pathlib, subprocess, sys
repo=pathlib.Path(sys.argv[1]); S=os.environ['S']
cap=repo/'.ufo/waves/round-38/frozen/hooks-capture'
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
        w,a,nd,e,tr=files[(tag,n)]; pos[w]+=1
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
DOC='''source: {src}
verified-at: 2026-10-26

# Control: cheap table

## Effective hook order (r38 capture)

{}

## Control notes

- [obs] table only; no rule text, no source reading.
'''
allrows=[(tag,p.name) for tag,sub in DIRS for p in sorted((cap/sub).iterdir()) if p.name.endswith(SUF)]
locale.setlocale(locale.LC_ALL,'en_US.UTF-8')
def strip_etcfirst(namekey):
    return rows_from(dedup(sorted(allrows,key=lambda t:(namekey(t[1]), 0 if t[0]=='etc' else 1))))
ctl={}
ctl['stripC-enUS-dedup-etcfirst']=(strip_etcfirst(lambda n:locale.strxfrm(n[:-len(SUF)])), 'S999 in `corpus/SOURCES.md` — control row for counter isolation')
ctl['stripC-dedup-etcfirst-srcS212']=(strip_etcfirst(key), 'S212 in `corpus/SOURCES.md` — own-work capture only; no libalpm row cited')
base=repo/'corpus/knowledge/pacman-hook-order-r38.md'
for name,(rows,src) in ctl.items():
    base.write_text(DOC.format(render(rows), src=src))
    subprocess.run(['git','-C',str(repo),'-c','user.name=ctl','-c','user.email=ctl@invalid','commit','-q','-am',f'control {name}'],check=True)
    sha=subprocess.run(['git','-C',str(repo),'rev-parse','HEAD'],capture_output=True,text=True).stdout.strip()
    out=subprocess.run(['python3',str(repo/'tools/check-hook-order-r38.py'),'--repo',str(repo),'--revision',sha],capture_output=True,text=True)
    j=json.loads(out.stdout); open(f'{S}/{name}.json','w').write(out.stdout)
    print(name, sha, j['rows_matched'], j['mismatches'], j['extra_rows'], j['source_ok'], j['source_ids'], j['result'])
# save baseline json from the S999 base commit
b=subprocess.run(['git','-C',str(repo),'rev-list','--max-parents=0','HEAD'],capture_output=True,text=True).stdout.strip()
sha999=subprocess.run(['git','-C',str(repo),'log','--format=%H','--grep=add fabricated S999'],capture_output=True,text=True).stdout.strip()
out=subprocess.run(['python3',str(repo/'tools/check-hook-order-r38.py'),'--repo',str(repo),'--revision',sha999],capture_output=True,text=True)
open(f'{S}/baseline-real-entry.json','w').write(out.stdout)
j=json.loads(out.stdout); print('baseline', sha999, j['rows_matched'], j['mismatches'], j['extra_rows'], j['source_ok'], j['result'])
