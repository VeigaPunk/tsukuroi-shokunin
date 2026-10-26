import re, collections, json, sys
LOG='/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-39/frozen/txcapture/pacman.log'
line_re=re.compile(r'^\[(?P<ts>[^\]]+)\] \[(?P<tag>[A-Z-]+)\] (?P<msg>.*)$')
rows=[]
with open(LOG, encoding='utf-8') as f:
    for i,l in enumerate(f,1):
        m=line_re.match(l.rstrip('\n'))
        rows.append({'ln':i,'tag':m.group('tag'),'msg':m.group('msg'),'ts':m.group('ts')})

txs=[]; cur=None
for r in rows:
    if r['tag']=='PACMAN' and r['msg'].startswith('Running '):
        cur={'cmd':r['msg'],'startline':r['ln'],'events':[]}; txs.append(cur)
    elif cur is not None:
        cur['events'].append(r)
print('windows',len(txs))
# classify windows
stat=collections.Counter()
for t in txs:
    n_start=sum(1 for e in t['events'] if e['tag']=='ALPM' and e['msg']=='transaction started')
    n_done=sum(1 for e in t['events'] if e['tag']=='ALPM' and e['msg']=='transaction completed')
    stat[(n_start,n_done)]+=1
print('window (started,completed) pattern:',dict(stat))
# commit phases
phases=[]
for t in txs:
    inside=False; ph=None
    for e in t['events']:
        if e['tag']=='ALPM' and e['msg']=='transaction started':
            inside=True; ph={'tx':t,'start':e['ln'],'end':None,'events':[]}; phases.append(ph); continue
        if e['tag']=='ALPM' and e['msg'].startswith('transaction ') and e['msg']!='transaction started':
            if ph: ph['end']=e['ln']; ph['endmsg']=e['msg']
            inside=False; ph=None; continue
        if inside and ph is not None: ph['events'].append(e)
print('phases',len(phases))

# classify events in commit phase
evk=collections.Counter()
for ph in phases:
    for e in ph['events']:
        if e['tag']=='ALPM-SCRIPTLET': evk['SCRIPTLET']+=1
        elif e['tag']=='ALPM': evk['ALPM '+e['msg'].split()[0].rstrip(':')]+=1
        else: evk['OTHER '+e['tag']]+=1
print('in-commit event kinds',dict(evk))

# blocks: package event line (installed/upgraded/removed/reinstalled/downgraded) starts a block
pkg_re=re.compile(r'^(installed|upgraded|removed|reinstalled|downgraded) (\S+) \((.*)\)$')
allblocks=[]
for idx,ph in enumerate(phases):
    blocks=[]; cur=None; pre=[]
    for e in ph['events']:
        m = pkg_re.match(e['msg']) if e['tag']=='ALPM' else None
        if m:
            cur={'verb':m.group(1),'name':m.group(2),'ver':m.group(3),'ln':e['ln'],'out':[],'pre_other':[]}
            blocks.append(cur)
        else:
            if cur is None: pre.append(e)
            else:
                if e['tag']=='ALPM-SCRIPTLET': cur['out'].append(e)
                else: cur['pre_other'].append(e)
    ph['blocks']=blocks; ph['pre']=pre
    allblocks.extend((idx,b) for b in blocks)

withscr=[(i,b) for i,b in allblocks if b['out']]
print('package blocks',len(allblocks),'with scriptlet output',len(withscr))
print('blocks with non-scriptlet non-package events (warnings) while open:',sum(1 for i,b in allblocks if b['pre_other']))
print('events before first package in phase (hook/pre):',collections.Counter(e['tag']+':'+e['msg'][:40] for ph in phases for e in ph['pre']).most_common(20))
# any 'running' (hook) events inside commit phases?
hooks_in_commit=[(i,e['ln'],e['msg']) for i,ph in enumerate(phases) for e in ph['events'] if e['tag']=='ALPM' and e['msg'].startswith('running')]
print('hook running lines inside commit phases:',len(hooks_in_commit))
for h in hooks_in_commit[:10]: print(' ',h)
json.dump([{'ph':i,'verb':b['verb'],'name':b['name'],'ver':b['ver'],'ln':b['ln'],
            'out':[(e['ln'],e['msg']) for e in b['out']],
            'other':[(e['ln'],e['msg']) for e in b['pre_other']]} for i,b in allblocks],
          open('blocks.json','w'))
json.dump([{'start':p['start'],'end':p['end'],'endmsg':p.get('endmsg'),'cmd':p['tx']['cmd'],
            'preblock':[(e['ln'],e['tag'],e['msg']) for e in p['pre']]} for p in phases], open('phases.json','w'), indent=0)
