#!/usr/bin/env python3
"""Absurd-body forge: bodies that assert nonsense but cite in-list existing lines."""
import json, os, subprocess
SBX='/fast/scratch/hyaku/tsukuroi-r48/GSentForge/sbx'
COUNTER='/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-scrub-admission-r48.py'
W='.ufo/waves/round-48'; OUT='/fast/scratch/hyaku/tsukuroi-r48/GSentForge/receipts'
def sh(a): return subprocess.run(a,capture_output=True,text=True)
def git(*a):
    r=sh(['git','-C',SBX,*a]); assert r.returncode==0, r.stderr; return r.stdout
ABS={
'GR1':'The row is correct because it is correct. I did not read any source. '
      'cmdline.c:120 and vsprintf.c:900 and kstrtox.c:100 and sysfs.c:900 exist, '
      'therefore the row is admitted. This body asserts nothing about the row and '
      'was not derived from the cited bytes; it was typed to clear the length floor. '*2,
'GR2':'No reading was performed. dev-replace.c:1126 is a line in a file; scrub.c:1500 is a line in a file; '
      'ioctl.c:3000 is a line in a file; sysfs.c:900 is a line in a file. Because those four '
      'lines exist, the row holds. I am asserting this without opening them. '*2,
'GR3':'I did not verify the unit, the kill semantics or the worker. systemd.kill.xml:100, '
      'btrfs-scrub@.service:3, scrub.c:1500 and capture.txt:3 are lines that exist on disk. '
      'That is my whole argument for admission. '*2,
}
for row in ('GR1','GR2','GR3'):
    h=json.loads(sh(['python3',COUNTER,'--lane',SBX,'--revision','HEAD','--section-hash']).stdout)['section_sha256'][row]
    for kind in ('Rev','Crit'):
        for x in 'abc':
            p=os.path.join(SBX,f'{W}/w2/R48{kind}{row}{x}.md')
            tail=(f'\nSeat-specific filler sentence number {kind}{x}: this clause is unique filler text, '
                  'written so that the pairwise-distinct-bodies rule cannot see that the seat did no work.')
            with open(p,'w') as f: f.write(f'ROW {row} VERDICT: holds\nSECTION SHA256: {h}\n{ABS[row]}{tail}\n')
git('add','-A'); git('-c','user.name=fixture','-c','user.email=fixture@invalid','commit','-qm','absurd bodies')
r=sh(['python3',COUNTER,'--lane',SBX,'--revision','HEAD'])
open(f'{OUT}/absurd-counter.json','w').write(r.stdout)
d=json.loads(r.stdout)
print(json.dumps({'exit':r.returncode,'verdict':d['verdict'],
  'legs':{k:d[k] for k in ('structural_ok','quotes_ok','verdicts_ok','marks_ok')},
  'credited_per_row':{k:len(v['credited']) for k,v in d['per_row'].items()}},indent=1))
