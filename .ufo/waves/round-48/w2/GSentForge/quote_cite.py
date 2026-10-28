#!/usr/bin/env python3
"""Cheapest forgery that clears a 'substance' rule: cite the line you paste."""
import json, os, subprocess
SBX='/fast/scratch/hyaku/tsukuroi-r48/GSentForge/sbx'
FROZEN='/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
COUNTER=f'{FROZEN}/tools/check-scrub-admission-r48.py'
W='.ufo/waves/round-48'; OUT='/fast/scratch/hyaku/tsukuroi-r48/GSentForge/receipts'
def sh(a): return subprocess.run(a,capture_output=True,text=True)
def git(*a):
    r=sh(['git','-C',SBX,*a]); assert r.returncode==0, r.stderr; return r.stdout
PLAN={'GR1':('.ufo/waves/round-45/frozen/src/cmdline.c',156),
      'GR2':('.ufo/waves/round-45/frozen/src/dev-replace.c',1126),
      'GR3':('.ufo/waves/round-44/frozen/src/btrfs-scrub@.service',2)}
for row,(path,ln) in PLAN.items():
    src=open(os.path.join(SBX,path),errors='replace').read().split('\n')[ln-1].strip()
    fname=os.path.basename(path)
    h=json.loads(sh(['python3',COUNTER,'--lane',SBX,'--revision','HEAD','--section-hash']).stdout)['section_sha256'][row]
    for kind in ('Rev','Crit'):
        for x in 'abc':
            p=os.path.join(SBX,f'{W}/w2/R48{kind}{row}{x}.md')
            body=(f'The row holds. I read {fname}:{ln} and it says:\n  {src}\n'
                  f'That is the whole of my reading; I checked no other clause of the row, '
                  f'opened no other snapshot, and formed no second opinion. This seat did the '
                  f'minimum that the frozen counter can measure and no more, and it says so here '
                  f'in as many words as the 300-byte floor demands. Filler clause {kind}{x} keeps '
                  f'the bodies pairwise distinct so the distinct-bodies rule is satisfied too.')
            with open(p,'w') as f: f.write(f'ROW {row} VERDICT: holds\nSECTION SHA256: {h}\n{body}\n')
git('add','-A'); git('-c','user.name=fixture','-c','user.email=fixture@invalid','commit','-qm','cite-what-you-paste')
r=sh(['python3',COUNTER,'--lane',SBX,'--revision','HEAD']); open(f'{OUT}/quote-cite-counter.json','w').write(r.stdout)
d=json.loads(r.stdout)
print(json.dumps({'counter_exit':r.returncode,'counter':d['verdict'],
 'legs':{k:d[k] for k in ('structural_ok','quotes_ok','verdicts_ok','marks_ok')},
 'credited':{k:len(v['credited']) for k,v in d['per_row'].items()}},indent=1))
