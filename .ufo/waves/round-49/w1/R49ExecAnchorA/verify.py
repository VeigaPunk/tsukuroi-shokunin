import json,subprocess,hashlib,os,re
LANE="/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
REV="55c07cd3f8bff2e12117c34d57b4c618de74d85c"
FR="/home/vgpnk/Projects/shokunin"
reg=json.load(open('adj-r19.json'))
out={r['id']:r for r in reg['outbound']}
prov=open('PROVINCE.frozen.md').read().splitlines()
anchor_tbl={}; adj_tbl={}
for i,l in enumerate(prov,1):
    if not l.startswith('|'): continue
    cells=[c.strip() for c in l.strip('|').split('|')]
    if cells and re.fullmatch(r'OUT-0\d\d',cells[0]) and len(cells)>=6:
        anchor_tbl[cells[0]]=dict(line=i,adj=cells[1],loc=cells[2],heading=cells[3],quote=cells[4],prop=cells[5],ncells=len(cells))
    if cells and re.fullmatch(r'ADJ-0\d',cells[0]):
        adj_tbl[cells[0]]=dict(line=i,outs=re.findall(r'OUT-0\d\d',l))
print("anchors table rows:",sorted(anchor_tbl))
print("adj table:",{k:v['outs'] for k,v in adj_tbl.items()})
def run(cmd):
    p=subprocess.run(cmd,shell=True,capture_output=True,text=True)
    return p.returncode,p.stdout,p.stderr
results=[]
for oid in ["OUT-002","OUT-003","OUT-004","OUT-005","OUT-006","OUT-007","OUT-008","OUT-009","OUT-010"]:
    r=out[oid]; sib=r['sibling']; repo=os.path.join(FR,sib+"-shokunin")
    rec=dict(id=oid,sibling=sib,repo=repo,commit=r['sibling_commit'])
    rc,_,err=run(f"git -C {repo} cat-file -e {r['sibling_commit']}^{{commit}}")
    rec['commit_exists']=(rc==0); rec['commit_err']=err.strip().splitlines()[0][:160] if err.strip() else ''
    rc,blob,err=run(f"git -C {repo} show {r['sibling_commit']}:{r['sibling_path']}")
    rec['blob_read_rc']=rc
    if rc==0:
        rec['blob_sha256']=hashlib.sha256(blob.encode()).hexdigest()
        rec['sha_match']=(rec['blob_sha256']==r['sibling_blob_sha256'])
        lines=blob.splitlines()
        rec['blob_lines']=len(lines)
        rec['heading_present']=(r['heading'] in blob)
        rec['heading_line']=next((i for i,l in enumerate(lines,1) if l.strip()==r['heading']),None)
        qhits=[i for i,l in enumerate(lines,1) if r['quote'] in l]
        rec['quote_lines']=qhits
        rec['quote_verbatim']=bool(qhits)
        rec['quote_exact_line']=(r['quote_line'] in qhits)
        rec['quote_line_delta']=min([abs(x-r['quote_line']) for x in qhits]) if qhits else None
        rec['quote_line_text']=lines[r['quote_line']-1] if 0<r['quote_line']<=len(lines) else None
        rec['quote_line_contains_quote']=(bool(rec['quote_line_text']) and r['quote'] in rec['quote_line_text'])
        # quote must be *inside* the province_pointer's declared line set? report pointer
    snap=r['snapshot']
    rc2,snapbytes,_=run(f"git -C {LANE} show {REV}:{snap}")
    rec['snapshot_rc']=rc2
    if rc2==0:
        rec['snapshot_sha256']=hashlib.sha256(snapbytes.encode()).hexdigest()
        rec['snapshot_matches_registry']=(rec['snapshot_sha256']==r['sibling_blob_sha256'])
        rec['snapshot_eq_sibling_blob']=(rec['snapshot_sha256']==rec.get('blob_sha256'))
    a=anchor_tbl.get(oid); rec['in_anchor_table']=bool(a)
    if a:
        rec['tbl_line']=a['line']; rec['tbl_adj']=a['adj']; rec['tbl_loc']=a['loc']
        rec['tbl_heading_match']=(a['heading'].strip('`')==r['heading'])
        rec['tbl_quote_match']=(a['quote'].strip('`')==r['quote'])
        rec['tbl_prop_match']=(a['prop']==r['proposition'])
        rec['adj_table_links_back']=(oid in adj_tbl.get(a['adj'],{}).get('outs',[]))
        pm=re.search(r'@\s*`?([0-9a-f]{4,40})`?',a['loc'])
        rec['tbl_commit_prefix']=pm.group(1) if pm else None
        rec['prefix_ok']=bool(pm) and r['sibling_commit'].startswith(pm.group(1))
        rec['tbl_path_ok']=(a['loc'].split('`')[0].strip()==sib+'-shokunin/'+r['sibling_path'])
    results.append(rec)
json.dump(dict(anchor_tbl=anchor_tbl,adj_tbl=adj_tbl,results=results),open('verify.json','w'),ensure_ascii=False,indent=1)
for rec in results:
    print(json.dumps(rec,ensure_ascii=False))
