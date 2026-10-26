import re
LOG="/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-39/frozen/txcapture/pacman.log"
lines=open(LOG, encoding='utf-8').read().splitlines()
pat=re.compile(r'^\[(?P<ts>[^\]]+)\] \[(?P<tag>[^\]]+)\] (?P<msg>.*)$')
R=[]
for i,l in enumerate(lines,1):
    m=pat.match(l)
    R.append((i, m['ts'] if m else None, m['tag'] if m else None, m['msg'] if m else l))
# windows
win_of={}
wins=[]; cur=None
for (i,ts,tag,msg) in R:
    if tag=='PACMAN' and msg.startswith("Running '"):
        cur={'start':i,'cmd':msg,'rows':[]}; wins.append(cur)
    if cur:
        cur['rows'].append((i,ts,tag,msg)); win_of[i]=len(wins)-1
def tx(w):
    rows=w['rows']
    s=next((i for (i,t,g,m) in rows if g=='ALPM' and m=='transaction started'),None)
    e=next((i for (i,t,g,m) in rows if g=='ALPM' and m in ('transaction completed','transaction interrupted','transaction failed')),None)
    return s,e
for k,w in enumerate(wins): w['tx']=tx(w)
# owners / when
OWN={}
for l in open("/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-39/frozen/txcapture/hook-owners.tsv",encoding='utf-8').read().splitlines():
    p,o=l.split('\t'); OWN[p]=o
WHEN={}
for l in open("/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-39/frozen/txcapture/hook-when.tsv",encoding='utf-8').read().splitlines():
    p,w=l.split('\t'); WHEN[p]=w
def first_install(pkg):
    for k,w in enumerate(wins):
        for (i,t,g,m) in w['rows']:
            if g=='ALPM' and m.startswith('installed '+pkg+' ('): return k,i
    return None,None
def first_run(name):
    for (i,t,g,m) in R:
        if g=='ALPM' and m.startswith("running '"+name+"'"): return i,win_of[i]
    return None,None
def runs_in_window(k,name):
    return [i for (i,t,g,m) in wins[k]['rows'] if g=='ALPM' and m.startswith("running '"+name+"'")]
def pre_runs(k):
    s,e=wins[k]['tx']
    return [(i,m) for (i,t,g,m) in wins[k]['rows'] if g=='ALPM' and m.startswith("running '") and (s is None or i<s)]
pre=[(p,o) for p,o in OWN.items() if WHEN.get(p)=='PreTransaction']
print("Pre hooks:",len(pre))
print(f"{'hook':42s} {'owner':22s} {'1st-install(line/win)':24s} {'1st-run(line/win)':20s} win runs pre_runs")
for p,o in pre:
    name=p.split('/')[-1]
    k,i=first_install(o); rk,ri=first_run(name)
    print(f"{name:42s} {o:22s} L{i}/w{k} L{rk}/w{ri} {runs_in_window(k,name) if k is not None else 'NA'} {pre_runs(k) if k is not None else 'NA'}")
