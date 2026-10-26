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
matched=[b for b in blocks if (b['name'],target(b)) in corpus]
print('blocks whose (name,target version) exist in local db:',len(matched))
withins=[b for b in matched if corpus[(b['name'],target(b))] is not None]
print('  of which package has an install file:',len(withins))
silent=[]; noisy=[]; other=[]
def post_body(t):
    m=re.search(r'^post_(?:install|upgrade)\s*\(\)\s*\{(.*?)^\}',t,re.M|re.S)
    return m.group(1) if m else None
for b in withins:
    t=corpus[(b['name'],target(b))]
    pb=post_body(t)
    if pb is None: other.append((b['name'],'no post')); continue
    prints = bool(re.search(r'\b(echo|printf|cat)\b',pb))
    if b['out']: noisy.append((b['name'],b['ln'],len(b['out']),prints))
    else: silent.append((b['name'],b['ln'],prints,(pb.strip().splitlines()[:2] if pb.strip() else [])))
print('\nblocks WITH output among matched:',len(noisy)); [print('  noisy',x) for x in noisy]
print('blocks WITHOUT output among matched:',len(silent)); [print('  silent',x) for x in silent]
print('no post func:',other)
# unconditional-echo check: post body whose first non-comment line is echo/printf/cat
bad=[]
for b in withins:
    pb=post_body(corpus[(b['name'],target(b))] or '')
    if not pb: continue
    lines=[l.strip() for l in pb.splitlines() if l.strip() and not l.strip().startswith('#')]
    if lines and re.match(r'^(echo|printf|cat)\b',lines[0]) and not b['out']:
        bad.append((b['name'],b['ln'],lines[0]))
print('\nunconditional-first-line-print post with NO logged output:',bad)
