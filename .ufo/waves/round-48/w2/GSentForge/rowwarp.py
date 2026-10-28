#!/usr/bin/env python3
"""Does the counter pin the row BYTES, or only self-consistently? Rewrite GR1, recompute, re-attest."""
import hashlib, json, os, subprocess, sys
SBX='/fast/scratch/hyaku/tsukuroi-r48/GSentForge/sbx'
FROZEN='/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
COUNTER=f'{FROZEN}/tools/check-scrub-admission-r48.py'
W='.ufo/waves/round-48'; OUT='/fast/scratch/hyaku/tsukuroi-r48/GSentForge/receipts'
ENTRY='corpus/knowledge/btrfs-scrub-grounding-r45.md'
def sh(a,**k): return subprocess.run(a,capture_output=True,text=True,**k)
def git(*a):
    r=sh(['git','-C',SBX,*a])
    if r.returncode: raise SystemExit(r.stderr)
    return r.stdout
def commit(m):
    git('add','-A'); git('-c','user.name=fixture','-c','user.email=fixture@invalid','commit','-qm',m)
def sec_hash(row):
    r=sh(['python3',COUNTER,'--lane',SBX,'--revision','HEAD','--section-hash'])
    return json.loads(r.stdout)['section_sha256'][row]
def set_hash(seat,row,h):
    p=os.path.join(SBX,f'{W}/w2/{seat}.md'); lines=open(p).read().split('\n')
    lines[1]=f'SECTION SHA256: {h}'
    with open(p,'w') as f: f.write('\n'.join(lines))
B=sys.argv[1]; out={}
git('reset','-q','--hard',B)
before=sec_hash('GR1')
# rewrite GR1: prepend a sweeping sentence and weaken a clause, keeping the Quote lines intact
p=os.path.join(SBX,ENTRY); lines=open(p).read().split('\n')
i=lines.index('## GR1'); j=lines.index('## GR2')
orig=lines[i:j]
lines[i+1:i+1]=['REWRITTEN BY THE INTEGRATOR: this row is true in every respect; no clause is contested.',
                'The mechanisms are self-evident and need no further reading.']
with open(p,'w') as f: f.write('\n'.join(lines))
commit('rowwarp: rewrite GR1 prose, then re-attest')
after=sec_hash('GR1')
seats=[s for s in os.listdir(os.path.join(SBX,f'{W}/w2')) if s.startswith('R48') and s.endswith('.md') and 'GR1' in s]
for s in seats: set_hash(s[:-3],'GR1',after)
commit('rowwarp: re-attest GR1 at the new hash')
c=sh(['python3',COUNTER,'--lane',SBX,'--revision','HEAD']); open(f'{OUT}/rowwarp-counter.json','w').write(c.stdout)
d=json.loads(c.stdout)
out['hash_before']=before; out['hash_after']=after; out['rewritten_seats']=len(seats)
out['counter_exit']=c.returncode; out['counter']=d['verdict']
out['legs']={k:d[k] for k in ('structural_ok','quotes_ok','verdicts_ok','marks_ok')}
out['gr1']={'credited':len(d['per_row']['GR1']['credited']),'row_ok':d['per_row']['GR1']['row_ok'],
            'quotes_ok':d['per_row']['GR1']['quotes']['ok'],'quotes':d['per_row']['GR1']['quotes']['quotes']}
# does the counter notice that the frozen claim named fe77...?
out['frozen_hash_appears_in_output']=('fe77ac765c7dd9f568e0b296ce8c7f8f53de3d8966d6a2029bada662badf9ca8' in c.stdout)
git('reset','-q','--hard',B)
print(json.dumps(out,indent=1,sort_keys=True))
