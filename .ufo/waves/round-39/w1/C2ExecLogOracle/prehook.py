import re, sys, collections
L='/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-39/frozen/txcapture/pacman.log'
CAP='/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-39/frozen/txcapture/'
hookwhen={}
for ln in open(CAP+'hook-when.tsv'):
    p,v=ln.rstrip('\n').split('\t'); hookwhen[p]=v
hookowner={}
for ln in open(CAP+'hook-owners.tsv'):
    p,v=ln.rstrip('\n').split('\t'); hookowner[p]=v
pre=[h for h,w in hookwhen.items() if w=='PreTransaction']
lines=open(L).read().splitlines()
first_install={}     # pkg -> line index (1-based) of first `installed pkg`
first_any={}         # pkg -> first line of installed|upgraded|reinstalled|downgraded
runs=collections.defaultdict(list)   # hook basename -> line idxs
win_of=[0]*len(lines)                 # window index per line
winstart={}                           # window -> line of Running
txstart_line=set()
w=0; ws=0
for i,raw in enumerate(lines,1):
    m=re.match(r'^\[[^\]]+\] \[([A-Z-]+)\] (.*)$',raw)
    if not m: continue
    tag,msg=m.group(1),m.group(2)
    if tag=='PACMAN' and msg.startswith("Running '"):
        w+=1; winstart[w]=i
    win_of[i-1]=w
    if tag=='ALPM' and msg=='transaction started': txstart_line.add(i)
    if tag=='ALPM':
        rm=re.match(r'^running \'([^\']*)\'',msg)
        if rm: runs[rm.group(1)].append(i)
        im=re.match(r'^installed (\S+) \(',msg)
        if im:
            first_install.setdefault(im.group(1),i)
            first_any.setdefault(im.group(1),i)
        am=re.match(r'^(?:upgraded|reinstalled|downgraded) (\S+) ',msg)
        if am: first_any.setdefault(am.group(1),i)
print('pre_hooks',len(pre))
hit=[]; miss=[]
for h in sorted(pre):
    pkg=hookowner[h]; base=h.rsplit('/',1)[-1]
    if pkg in first_install:
        hit.append((base,pkg,first_install[pkg],base in hookowner))
print('pre_hooks_whose_owner_first_installed_in_capture_local',len([x for x in hit]))
# recompute: pkg first installed in capture AND its first appearance is `installed`
res=[]
for h in sorted(pre):
    pkg=hookowner[h]; base=h.rsplit('/',1)[-1]
    fa=first_any.get(pkg); fi=first_install.get(pkg)
    if fi is not None and fa==fi:
        res.append((base,pkg,fi))
print('pre_hooks_owner_first_seen_as_installed',len(res))
bad=[]
for base,pkg,fi in res:
    wl=win_of[fi-1]
    txs=[l for l in txstart_line if win_of[l-1]==wl]
    for r in runs.get(base,[]):
        if win_of[r-1]==wl and any(r<tx for tx in txs):
            bad.append((base,pkg,fi,r,wl))
print('pre_hook_ran_in_its_first_install_window_pre_phase',len(bad),bad[:5])
print('pre_hooks_never_run_in_capture',len([h for h in pre if h.rsplit('/',1)[-1] not in runs]))
print('distinct_pre_hooks_that_ran',len([h for h in pre if h.rsplit('/',1)[-1] in runs]))
# hook-basename uniqueness check
import os
base_count=collections.Counter(h.rsplit('/',1)[-1] for h in hookwhen)
print('dupe_basenames',[b for b,c in base_count.items() if c>1])
for base,pkg,fi in res[:20]:
    print(' ',base,'owner',pkg,'first_installed_line',fi,'runs',len(runs.get(base,[])))
