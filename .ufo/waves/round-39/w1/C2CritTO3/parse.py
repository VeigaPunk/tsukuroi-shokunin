import re, json, collections, sys
LOG='/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-39/frozen/txcapture/pacman.log'
line_re=re.compile(r'^\[(?P<ts>[^\]]+)\] \[(?P<tag>[A-Z-]+)\] (?P<msg>.*)$')
rows=[]
with open(LOG, encoding='utf-8', errors='replace') as f:
    for i,l in enumerate(f,1):
        m=line_re.match(l.rstrip('\n'))
        if not m: rows.append((i,'BAD',l.rstrip('\n'),None)); continue
        rows.append((i,m.group('tag'),m.group('msg'),m.group('ts')))
kinds=collections.Counter()
for i,tag,msg,ts in rows:
    if tag=='BAD': kinds['BAD']+=1; continue
    if tag=='PACMAN': kinds['PACMAN '+msg.split()[0]]+=1
    elif tag=='ALPM':
        kinds['ALPM '+msg.split()[0].rstrip(':')]+=1
    else: kinds[tag]+=1
for k,v in kinds.most_common(): print(v,k)
print('total',len(rows))
# segment windows
wins=[]; cur=None
for i,tag,msg,ts in rows:
    if tag=='PACMAN' and msg.startswith('Running '):
        cur={'start':i,'cmd':msg,'lines':[]}; wins.append(cur)
    elif cur is not None: cur['lines'].append((i,tag,msg))
print('windows',len(wins))
starts=[(i,msg) for i,tag,msg,ts in rows if tag=='ALPM' and msg.startswith('transaction ')]
print('transaction lines',len(starts), collections.Counter(m for _,m in starts))
