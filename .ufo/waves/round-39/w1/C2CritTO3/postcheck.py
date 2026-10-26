import json,re,glob,os
corpus={}
for d in glob.glob('/var/lib/pacman/local/*/'):
    d=d.rstrip('/'); desc=os.path.join(d,'desc'); ins=os.path.join(d,'install')
    if not os.path.exists(desc): continue
    txt=open(desc,encoding='utf-8',errors='replace').read()
    name=re.search(r'%NAME%\n(\S+)',txt); ver=re.search(r'%VERSION%\n(\S+)',txt)
    corpus[(name.group(1),ver.group(1))]={'dir':os.path.basename(d),'install':open(ins,encoding='utf-8',errors='replace').read() if os.path.exists(ins) else None}
blocks=json.load(open('blocks.json'))
def target(b):
    if b['verb'] in ('upgraded','downgraded'):
        return b['ver'].split(' -> ')[-1]
    return b['ver']
print(f"{'pkg':32} {'target':16} {'dbmatch':7} {'has_post':8} outlines")
for b in blocks:
    if not b['out']: continue
    tv=target(b); key=(b['name'],tv)
    hit=corpus.get(key)
    if hit:
        ins=hit['install']
        post= bool(ins and re.search(r'^(post_install|post_upgrade)\s*\(\)',ins,re.M))
        pre = bool(ins and re.search(r'^(pre_install|pre_upgrade)\s*\(\)',ins,re.M))
        print(f"{b['name']:32} {tv:16} {'MATCH':7} {str(post):8} pre={str(pre):5} {len(b['out'])}")
    else:
        # show current version present
        cur=[k for k in corpus if k[0]==b['name']]
        print(f"{b['name']:32} {tv:16} {'db='+ (cur[0][1] if cur else 'absent'):30} {len(b['out'])}")
