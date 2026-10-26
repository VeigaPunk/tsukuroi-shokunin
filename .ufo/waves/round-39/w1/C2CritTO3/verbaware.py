import json,re,glob,os
corpus={}
for d in glob.glob('/var/lib/pacman/local/*/'):
    d=d.rstrip('/'); desc=os.path.join(d,'desc'); ins=os.path.join(d,'install')
    if not os.path.exists(desc): continue
    txt=open(desc,encoding='utf-8',errors='replace').read()
    nm=re.search(r'%NAME%\n(\S+)',txt); vr=re.search(r'%VERSION%\n(\S+)',txt)
    corpus[(nm.group(1),vr.group(1))]=open(ins,encoding='utf-8',errors='replace').read() if os.path.exists(ins) else None
blocks=json.load(open('blocks.json'))
def target(b): return b['ver'].split(' -> ')[-1] if b['verb'] in ('upgraded','downgraded') else b['ver']
def fn(t,name):
    m=re.search(r'^%s\s*\(\)\s*\{(.*?)^\}'%name,t,re.M|re.S)
    return m.group(1) if m else None
bad=[]; ok=[]; skip=[]
for b in blocks:
    if (b['name'],target(b)) not in corpus: continue
    t=corpus[(b['name'],target(b))]
    if t is None: continue
    fname={'installed':'post_install','upgraded':'post_upgrade','reinstalled':'post_upgrade','downgraded':'post_upgrade'}[b['verb']]
    body=fn(t,fname)
    if body is None: continue
    code=[l.strip() for l in body.splitlines() if l.strip() and not l.strip().startswith('#')]
    if not code: continue
    unconditional = re.match(r'^(echo|printf|cat)\b',code[0]) is not None
    if unconditional:
        (ok if b['out'] else bad).append((b['name'],b['ln'],b['verb'],code[0][:70],len(b['out'])))
print('relevant-post-first-stmt-unconditional WITH output:',len(ok))
for x in ok: print('  OK  ',x)
print('... with NO output:',len(bad))
for x in bad: print('  CONTRADICTION',x)
