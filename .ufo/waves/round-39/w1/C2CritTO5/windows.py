import re
LOG="/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-39/frozen/txcapture/pacman.log"
lines=open(LOG, encoding='utf-8').read().splitlines()
pat=re.compile(r'^\[(?P<ts>[^\]]+)\] \[(?P<tag>[^\]]+)\] (?P<msg>.*)$')
R=[]
for i,l in enumerate(lines,1):
    m=pat.match(l); R.append((i, m['ts'] if m else None, m['tag'] if m else None, m['msg'] if m else l))
wins=[]; cur=None
for (i,ts,tag,msg) in R:
    if tag=='PACMAN' and msg.startswith("Running '"):
        cur={'start':i,'cmd':msg,'rows':[]}; wins.append(cur)
    if cur: cur['rows'].append((i,ts,tag,msg))
def summarize(k):
    w=wins[k]; rows=w['rows']
    start=[i for (i,t,g,m) in rows if g=='ALPM' and m=='transaction started']
    end=[i for (i,t,g,m) in rows if g=='ALPM' and m in ('transaction completed','transaction interrupted','transaction failed')]
    s=start[0] if start else None; e=end[-1] if end else None
    pre=[(i,m) for (i,t,g,m) in rows if g=='ALPM' and m.startswith("running '") and (s is None or i<s)]
    post=[(i,m) for (i,t,g,m) in rows if g=='ALPM' and m.startswith("running '") and e is not None and i>e]
    add=[(i,m) for (i,t,g,m) in rows if g=='ALPM' and (m.startswith('installed ') or m.startswith('upgraded ')) and s and (e is None or i<e)]
    rem=[(i,m) for (i,t,g,m) in rows if g=='ALPM' and m.startswith('removed ') and s and (e is None or i<e)]
    print(f"--- window#{k} lines {w['start']}-{rows[-1][0]} tx {s}->{e}")
    print("  cmd:", w['cmd'][:120])
    print("  PRE runs:", pre)
    print("  n_add:", len(add), " n_rem:", len(rem), " post_runs:", len(post))
    names=[re.match(r'(?:installed|upgraded) ([^ ]+) ',m).group(1) for (i,m) in add]
    kern=[n for n in names if re.match(r'^linux(-lts|-zen|-hardened|-rt)?$',n) or n in ('linux-headers','linux-firmware','nvidia-open-dkms','nvidia-utils','lib32-nvidia-utils')]
    print("  add names count:", len(names), " kernel-ish:", kern)
    print("  removed:", [m for (i,m) in rem])
    return names
for k in (0,5,7,8,10,27):
    summarize(k)
# rsync install timing
print("\n=== rsync occurrences ===")
for (i,ts,tag,msg) in R:
    if tag=='ALPM' and (' rsync' in msg) and (msg.startswith('installed ') or msg.startswith('upgraded ')):
        print(i,msg)
print("\n=== first 'running 10-limine-snapper-lock' ===")
for (i,ts,tag,msg) in R:
    if tag=='ALPM' and "10-limine-snapper-lock" in msg:
        print(i,msg)
