import re, collections
L='/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-39/frozen/txcapture/pacman.log'
lines=open(L).read().splitlines()
w=0; pre=collections.Counter(); post=collections.Counter(); nocommit_run=0
state=None; has_commit=collections.Counter(); cur=0
for raw in lines:
    m=re.match(r'^\[[^\]]+\] \[([A-Z-]+)\] (.*)$',raw)
    if not m: continue
    tag,msg=m.group(1),m.group(2)
    if tag=='PACMAN' and msg.startswith("Running '"):
        w+=1; cur=w; state='win'
        continue
    if tag=='ALPM' and msg=='transaction started': state='commit'; has_commit[cur]=1
    elif tag=='ALPM' and msg in ('transaction completed','transaction interrupted','transaction failed'): state='post'
    elif tag=='ALPM' and msg.startswith("running '"):
        if state=='commit': pre['INSIDE']+=1
        elif state=='post': post['POST']+=1
        elif state=='win': pre['PRE']+=1
        else: pre['NOWIN']+=1
print('running_before_started(PRE)=%d running_after_completed(POST)=%d inside=%d no_window=%d'%(pre['PRE'],post['POST'],pre['INSIDE'],pre['NOWIN']))
print('windows_with_commit=%d windows_total=%d'%(len(has_commit),w))
# scriptlet distribution per window-phase
sc=collections.Counter()
state=None
for raw in lines:
    m=re.match(r'^\[[^\]]+\] \[([A-Z-]+)\] (.*)$',raw)
    if not m: continue
    tag,msg=m.group(1),m.group(2)
    if tag=='PACMAN' and msg.startswith("Running '"): state='win'; continue
    if tag=='ALPM' and msg=='transaction started': state='commit'
    elif tag=='ALPM' and msg in ('transaction completed','transaction interrupted','transaction failed'): state='post'
    elif tag=='ALPM-SCRIPTLET': sc[state]+=1
print('scriptlet_by_phase',dict(sc))
