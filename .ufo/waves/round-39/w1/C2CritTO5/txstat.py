import re
LOG="/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-39/frozen/txcapture/pacman.log"
lines=open(LOG,encoding='utf-8').read().splitlines()
pat=re.compile(r'^\[(?P<ts>[^\]]+)\] \[(?P<tag>[^\]]+)\] (?P<msg>.*)$')
wins=[];cur=None
for i,l in enumerate(lines,1):
    m=pat.match(l)
    if not m: continue
    ts,tag,msg=m['ts'],m['tag'],m['msg']
    if tag=='PACMAN' and msg.startswith("Running '"):
        cur={'start':i,'cmd':msg,'rows':[]};wins.append(cur)
    if cur: cur['rows'].append((i,tag,msg))
for k in (0,5,7,8,10,27,53,14,11):
    w=wins[k]; s=e=None; add=[];rem=[];up=[];inst=[]
    for (i,tag,msg) in w['rows']:
        if tag!='ALPM': continue
        if msg=='transaction started': s=i
        elif msg in ('transaction completed','transaction interrupted','transaction failed'): e=i
        elif msg.startswith('installed '): inst.append(msg.split()[1])
        elif msg.startswith('upgraded '): up.append(msg.split()[1])
        elif msg.startswith('removed '): rem.append(msg.split()[1])
    print(f"w{k} L{w['start']} tx {s}->{e} installed={len(inst)} upgraded={len(up)} removed={len(rem)}")
    if up: print("   upgraded:", up[:20])
    if rem: print("   removed:", rem[:20])
