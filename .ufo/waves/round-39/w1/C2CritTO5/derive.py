import re, sys, json
LOG="/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-39/frozen/txcapture/pacman.log"
lines=open(LOG, encoding='utf-8').read().splitlines()
pat=re.compile(r'^\[(?P<ts>[^\]]+)\] \[(?P<tag>[^\]]+)\] (?P<msg>.*)$')
recs=[]
for i,l in enumerate(lines,1):
    m=pat.match(l)
    if not m: recs.append((i,None,None,l)); continue
    recs.append((i,m['ts'],m['tag'],m['msg']))
# windows
wins=[]
cur=None
for (i,ts,tag,msg) in recs:
    if tag=='PACMAN' and msg.startswith("Running '"):
        cur={'start':i,'cmd':msg,'lines':[]}
        wins.append(cur)
    if cur is not None:
        cur['lines'].append((i,ts,tag,msg))
for w in wins:
    w['tx']=[]  # list of (started_idx, end_idx, endkind)
    started=None
    for (i,ts,tag,msg) in w['lines']:
        if tag=='ALPM' and msg=='transaction started':
            started=i
        elif tag=='ALPM' and started and msg in ('transaction completed','transaction interrupted','transaction failed'):
            w['tx'].append((started,i,msg)); started=None
        # installs
    if started: w['tx'].append((started,None,'OPEN'))
owners=[l.split('\t') for l in open("/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-39/frozen/txcapture/hook-owners.tsv",encoding='utf-8').read().splitlines()]
when={}
for l in open("/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-39/frozen/txcapture/hook-when.tsv",encoding='utf-8').read().splitlines():
    p=l.split('\t'); when[p[0]]=p[1]
print("windows:",len(wins),"transactions:",sum(len(w['tx']) for w in wins))
# map: line -> window index
def find_first_install(pkg):
    rx=re.compile(r'^installed '+re.escape(pkg)+r' \(')
    for wi,w in enumerate(wins):
        for (i,ts,tag,msg) in w['lines']:
            if tag=='ALPM' and rx.match(msg):
                return wi,i,ts,msg
    return None
def find_any(pkg):
    out=[]
    for wi,w in enumerate(wins):
        for (i,ts,tag,msg) in w['lines']:
            if tag=='ALPM' and (msg.startswith('installed '+pkg+' (') or msg.startswith('upgraded '+pkg+' ')):
                out.append((wi,i,msg))
    return out
rows=[]
for path,owner in owners:
    if when.get(path)!='PreTransaction': continue
    if owner=='-':
        rows.append((path,owner,None,None,None,'UNOWNED')); continue
    fi=find_first_install(owner)
    allv=find_any(owner)
    rows.append((path,owner,fi,allv,len(allv),'ok' if fi else 'NEVER-INSTALLED'))
print("\n=== PRE HOOKS: %d ==="%len(rows))
for path,owner,fi,allv,n,st in rows:
    print(f"{path.split('/')[-1]:45s} owner={owner:22s} status={st}")
    if fi:
        wi,i,ts,msg=fi
        print(f"    first-install: line {i} window#{wi} {ts} :: {msg}")
        print(f"    window cmd: {wins[wi]['cmd'][:160]}")
        print(f"    window tx: {wins[wi]['tx']}")
    if allv and len(allv)<=6:
        for a in allv: print("     occ:",a)
json.dump([{'path':p,'owner':o,'first_install':f,'status':s} for p,o,f,a,n,s in rows], open('/fast/scratch/hyaku/tsukuroi-r39/C2CritTO5/pre-hooks.json','w'), indent=1)
