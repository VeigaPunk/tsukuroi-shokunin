import json,subprocess,hashlib,os,re
LANE="/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
REV="55c07cd3f8bff2e12117c34d57b4c618de74d85c"
FR="/home/vgpnk/Projects/shokunin"
reg=json.load(open('adj-r19.json')); out={r['id']:r for r in reg['outbound']}
prov=open('PROVINCE.frozen.md').read().splitlines()
anchor={}; adj={}
for i,l in enumerate(prov,1):
    if not l.startswith('|'): continue
    c=[x.strip() for x in l.strip('|').split('|')]
    if c and re.fullmatch(r'OUT-0\d\d',c[0]) and len(c)>=6:
        anchor[c[0]]=dict(line=i,adj=c[1],loc=c[2],heading=c[3],quote=c[4],prop=c[5],ncells=len(c))
    if c and re.fullmatch(r'ADJ-0\d',c[0]):
        adj[c[0]]=dict(line=i,outs=re.findall(r'OUT-0\d\d',l),cells=c)
def run(cmd):
    p=subprocess.run(cmd,shell=True,capture_output=True,text=True); return p.returncode,p.stdout,p.stderr
rows=[]
for oid in ["OUT-002","OUT-003","OUT-004","OUT-005","OUT-006","OUT-007","OUT-008","OUT-009","OUT-010"]:
    r=out[oid]; sib=r['sibling']; repo=os.path.join(FR,sib+"-shokunin"); a=anchor[oid]
    e=dict(id=oid,sibling=sib,commit=r['sibling_commit'],tbl_line=a['line'])
    rc,_,err=run(f"git -C {repo} cat-file -e {r['sibling_commit']}^{{commit}}"); e['A_commit_exists']=(rc==0)
    rc,blob,_=run(f"git -C {repo} show {r['sibling_commit']}:{r['sibling_path']}")
    e['A_blob_read']=(rc==0)
    if rc==0:
        e['B_blob_sha256']=hashlib.sha256(blob.encode()).hexdigest()
        e['B_sha_match']=(e['B_blob_sha256']==r['sibling_blob_sha256'])
        lines=blob.splitlines()
        e['C_heading_line']=next((i for i,l in enumerate(lines,1) if l.strip()==r['heading']),None)
        e['C_heading_present']=e['C_heading_line'] is not None
        qh=[i for i,l in enumerate(lines,1) if r['quote'] in l]
        e['D_quote_lines']=qh; e['D_quote_at_quote_line']=(r['quote_line'] in qh)
        # pointer membership
        pr=re.search(r':([0-9,\-]+)$',r['province_pointer']); rng=[]
        if pr:
            for part in pr.group(1).split(','):
                if '-' in part: x,y=part.split('-'); rng+=list(range(int(x),int(y)+1))
                else: rng.append(int(part))
        e['D_quote_line_in_pointer']=(r['quote_line'] in rng)
        # unique prefix resolution
        m=re.search(r'`([0-9a-f]{4,40})`',a['loc']); pre=m.group(1) if m else None
        rc2,res,_=run(f"git -C {repo} rev-parse --verify --quiet {pre}^{{commit}}")
        e['E_prefix']=pre; e['E_prefix_resolves_to']=res.strip() if rc2==0 else None
        e['E_prefix_unambiguous_and_equal']=(rc2==0 and res.strip()==r['sibling_commit'])
    # cell exactness
    e['F_path_cell_eq']=(a['loc']==f"`{sib}-shokunin/{r['sibling_path']}` @ `{re.search(r'`([0-9a-f]+)`$',a['loc']).group(1)}`")
    e['F_heading_cell_eq']=(a['heading']==f"`{r['heading']}`")
    e['F_quote_cell_eq']=(a['quote']==r['quote'])
    e['F_prop_cell_eq']=(a['prop']==r['proposition'])
    # ADJ class consistency both ways
    e['G_tbl_adj']=a['adj']; e['G_adj_lists_it']=(oid in adj[a['adj']]['outs'])
    e['G_owner_cell']=adj[a['adj']]['cells'][2] if len(adj[a['adj']]['cells'])>2 else ''
    e['G_sibling_in_owner_cell']=(sib in e['G_owner_cell'])
    e['G_sibling_in_adj_prose']=(sib in adj[a['adj']]['cells'][1])
    # snapshot
    rc3,sb,_=run(f"git -C {LANE} show {REV}:{r['snapshot']}")
    e['H_snapshot_rc']=rc3
    if rc3==0:
        hh=hashlib.sha256(sb.encode()).hexdigest(); e['H_snapshot_sha256']=hh
        e['H_snapshot_matches_registry']=(hh==r['sibling_blob_sha256'])
    rows.append(e)
json.dump(rows,open('final.json','w'),ensure_ascii=False,indent=1)
for e in rows:
    print(json.dumps(e,ensure_ascii=False))
