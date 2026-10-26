import json,re,collections
LOG='/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-39/frozen/txcapture/pacman.log'
raw=open(LOG,encoding='utf-8').read().splitlines(True)
rows=[(i,l.rstrip('\n')) for i,l in enumerate(raw,1)]
ph=json.load(open('phases.json')); blocks=json.load(open('blocks.json'))
line_re=re.compile(r'^\[(?P<ts>[^\]]+)\] \[(?P<tag>[A-Z-]+)\] (?P<msg>.*)$')
# 1. structural counts
print('log lines',len(rows))
print('windows',len(ph)+26,'phases',len(ph))
print('in-commit scriptlet lines',sum(len(b['out']) for b in blocks))
print('total scriptlet lines',sum(1 for ln,t in rows if '[ALPM-SCRIPTLET]' in t))
print('blocks',len(blocks),'blocks with output',sum(1 for b in blocks if b['out']))
# 2. contiguity: any non-scriptlet line strictly between first and last out line of a block
gap=[]
for b in blocks:
    if len(b['out'])<2: continue
    lo,hi=b['out'][0][0],b['out'][-1][0]
    span=[ln for ln,_ in b['out']]
    between=[ln for ln,t in rows if lo<ln<hi and ln not in set(span)]
    if between: gap.append((b['name'],b['ln'],lo,hi,between))
print('blocks whose output run is interrupted by other log lines:',len(gap))
for g in gap[:5]: print('  ',g)
# 3. warnings position: warning line vs next package line
pat=re.compile(r'^\[\S+\] \[ALPM\] (installed|upgraded|removed|reinstalled|downgraded) (\S+) \((.*)\)$')
for ln,t in rows:
    if '[ALPM] warning' in t:
        nxt=[(l2,t2) for l2,t2 in rows if l2>ln and pat.match(t2)][:1]
        prv=[(l2,t2) for l2,t2 in rows if l2<ln and pat.match(t2)][-1:]
        print(f"warning@{ln} PREV pkg={prv[0][0] if prv else None} NEXT pkg={nxt[0][0] if nxt else None} {nxt[0][1][:70] if nxt else ''}")
# 4. removed
rem=[(ln,t) for ln,t in rows if re.match(r'^\[\S+\] \[ALPM\] removed ',t)]
print('removed lines',len(rem))
# 5. hooks inside commit
print('hook running lines inside commit:',sum(1 for p in ph for ln,t in rows if p['start']<ln<p['end'] and '[ALPM] running ' in t))
