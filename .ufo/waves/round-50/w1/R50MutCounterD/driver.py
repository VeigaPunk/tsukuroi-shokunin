import json, subprocess, sys, os
S='/fast/scratch/hyaku/tsukuroi-r50/R50MutCounterD'
L='/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
REV='8029cdba1049df25632c91a23c8db4eefb54be5f'
FX=[
 ('real',            [],                                                     'PASS'),
 ('k1-stub',         ['--province-file', f'{S}/fx/PROVINCE.f4-stub.md','--registry-file',f'{S}/fx/registry.f4-stub.json'], 'FAIL'),
 ('k2-wrongclass',   ['--province-file', f'{S}/fx/PROVINCE.k2-wrongclass.md'], 'FAIL'),
 ('k3-digest0',      ['--registry-file', f'{S}/fx/registry.k3-digest0.json'],   'FAIL'),
 ('f1-digest',       ['--registry-file', f'{S}/fx/registry.f1-digest.json'],    'FAIL'),
 ('f2-heading',      ['--province-file', f'{S}/fx/PROVINCE.f2-heading.md'],     'FAIL'),
 ('f3-drift',        ['--siblings-root', f'{S}/fx/root3'],                      'FAIL'),
 ('f6-stubrepo',     ['--siblings-root', f'{S}/fx/root6'],                      'PASS'),
 ('f7-emptyroot',    ['--siblings-root', f'{S}/fx/root7-empty'],                'FAIL'),
]
rows=[]
for m in ['pristine','M1','M2','M3','M4','M5']:
    for name,extra,exp in FX:
        cmd=[sys.executable, f'{S}/mut/{m}.py','--revision',REV,'--lane',L]+extra
        p=subprocess.run(cmd,capture_output=True,text=True,timeout=300)
        try: d=json.loads(p.stdout)
        except Exception: d={'verdict':'ERR','error':(p.stdout[:200]+p.stderr[:200])}
        rows.append({'counter':m,'fixture':name,'expected':exp,'verdict':d.get('verdict'),
                     'rc':p.returncode,'adj_rows':d.get('adj_rows'),'linked_rows':d.get('linked_rows'),
                     'bare_ranges':d.get('bare_ranges'),'anchors_ok':d.get('anchors_ok'),
                     'registry_ok':d.get('registry_ok'),'checker':d.get('anchors_checker_rc'),
                     'pin':d.get('quote_at_pin_ok'),'live':d.get('live_quote_ok'),
                     'stub_fails':d.get('stub_fails'),'stub_pin':d.get('stub_content_pin'),
                     'cmd':' '.join(cmd)})
json.dump(rows,open(f'{S}/results.json','w'),indent=1)
print(f"{'counter':9} {'fixture':13} {'exp':4} {'got':5} {'rc':2} adj lnk bare anch reg chk pin live sfails spin")
for r in rows:
    print(f"{r['counter']:9} {r['fixture']:13} {r['expected']:4} {str(r['verdict']):5} {r['rc']:<2} "
          f"{r['adj_rows']} {r['linked_rows']} {r['bare_ranges']} {r['anchors_ok']} {r['registry_ok']} "
          f"{r['checker']} {r['pin']} {r['live']} {r['stub_fails']} {r['stub_pin']}")
