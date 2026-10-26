import re,json,collections
LOG='/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-39/frozen/txcapture/pacman.log'
rows=[(i,l.rstrip('\n')) for i,l in enumerate(open(LOG),1)]
pat=re.compile(r'^\[\S+\] \[ALPM\] (installed|upgraded|reinstalled|downgraded|removed) (\S+) \((.*)\)$')
last={}
seq=[]
for ln,t in rows:
    m=pat.match(t)
    if not m: continue
    v,n,ver=m.group(1),m.group(2),m.group(3)
    if v=='upgraded':
        old,new=[x.strip() for x in ver.split('->')]
        last[n]=new; seq.append((ln,n,'upgraded',old,new))
    elif v=='downgraded':
        old,new=[x.strip() for x in ver.split('->')]
        last[n]=new; seq.append((ln,n,'downgraded',old,new))
    elif v in('installed','reinstalled'):
        last[n]=ver; seq.append((ln,n,v,'',ver))
    else:
        seq.append((ln,n,'removed',last.get(n,'<none>'),ver))
print('per removed line: name removed_version last-known-installed match')
mismatch=0
for ln,n,v,prev,ver in seq:
    if v!='removed': continue
    ok = prev==ver
    if not ok: mismatch+=1
    print(f"  {ln} {n:26} removed={ver:22} last_known={prev:22} {'OK' if ok else 'MISMATCH'}")
print('mismatches:',mismatch)
# names appearing twice in one phase?
ph=json.load(open('phases.json'))
for p in ph:
    ev=[(ln,pat.match(t)) for ln,t in rows if p['start']<ln<p['end'] and pat.match(t)]
    c=collections.Counter(m.group(2) for ln,m in ev)
    dup={k:v for k,v in c.items() if v>1}
    if dup: print('phase',p['start'],'duplicate package events:',dup)
