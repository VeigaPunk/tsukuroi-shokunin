import json, subprocess, sys
S='/fast/scratch/hyaku/tsukuroi-r50/R50MutCounterD'
L='/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
REV='8029cdba1049df25632c91a23c8db4eefb54be5f'
FX=[
 ('f8-strongstub', ['--province-file', f'{S}/fx/PROVINCE.f8-strongstub.md'], 'FAIL'),
 ('real',          [], 'PASS'),
 ('k1-stub',       ['--province-file', f'{S}/fx/PROVINCE.f4-stub.md','--registry-file',f'{S}/fx/registry.f4-stub.json'], 'FAIL'),
]
for m in ['pristine','M1','M2','M3','M4','M5','M6']:
    for name,extra,exp in FX:
        cmd=[sys.executable, f'{S}/mut/{m}.py','--revision',REV,'--lane',L]+extra
        p=subprocess.run(cmd,capture_output=True,text=True,timeout=300)
        d=json.loads(p.stdout)
        print(f"{m:9} {name:13} exp={exp:4} got={str(d.get('verdict')):4} pin={d.get('quote_at_pin_ok')} "
              f"live={d.get('live_quote_ok')} stub_fails={d.get('stub_fails')} stub_pin={d.get('stub_content_pin')} rc={p.returncode}")
        det={k:v['why'] for k,v in d.get('content_detail',{}).items() if v['why']}
        if det: print('   why:', {k:v[0] for k,v in det.items()})
