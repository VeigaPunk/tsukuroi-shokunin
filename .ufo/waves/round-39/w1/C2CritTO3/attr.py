import json,re,glob,os,collections
LOG='/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-39/frozen/txcapture/pacman.log'
rows=[(i,l.rstrip('\n')) for i,l in enumerate(open(LOG),1)]
ph=json.load(open('phases.json'))
incommit=set()
for p in ph:
    for ln,t in rows:
        if p['start']<ln<p['end'] and '[ALPM-SCRIPTLET]' in t: incommit.add(ln)
# corpus: dbdir -> (name, version, install text)
corpus=[]
for d in glob.glob('/var/lib/pacman/local/*/'):
    d=d.rstrip('/'); desc=os.path.join(d,'desc'); ins=os.path.join(d,'install')
    if not os.path.exists(ins) or not os.path.exists(desc): continue
    txt=open(desc,encoding='utf-8',errors='replace').read()
    name=re.search(r'%NAME%\n(\S+)',txt); ver=re.search(r'%VERSION%\n(\S+)',txt)
    corpus.append({'dir':os.path.basename(d),'name':name.group(1) if name else '?','ver':ver.group(1) if ver else '?',
                   'text':open(ins,encoding='utf-8',errors='replace').read()})
print('corpus',len(corpus))
blocks=json.load(open('blocks.json'))
blk_of={}
for b in blocks:
    for ln,m in b['out']: blk_of[ln]=b
res={'agree':[], 'disagree':[], 'nofound':[], 'noblock':[]}
for ln,t in rows:
    if '[ALPM-SCRIPTLET]' not in t or ln not in incommit: continue
    msg=t.split('[ALPM-SCRIPTLET] ',1)[1]
    if not msg.strip():
        res['nofound'].append((ln,msg,'')); continue
    hits=[c for c in corpus if msg in c['text']]
    b=blk_of.get(ln)
    if not b: res['noblock'].append((ln,msg)); continue
    if not hits: res['nofound'].append((ln,msg,b['name'])); continue
    if any(h['name']==b['name'] for h in hits): res['agree'].append((ln,msg,b['name'],hits[0]['dir']))
    else: res['disagree'].append((ln,msg,b['name'],[(h['name'],h['ver']) for h in hits]))
print('agree',len(res['agree']),'disagree',len(res['disagree']),'nofound',len(res['nofound']),'noblock',len(res['noblock']))
for d in res['disagree']: print('DISAGREE',d[0],repr(d[1][:100]),'block=',d[2],'owners=',d[3])
print()
print('--- no verbatim owner (block, text) ---')
for d in res['nofound']: print(d[0],repr(d[1][:80]),'block=',d[2])
json.dump(res,open('attr.json','w'),indent=1)
