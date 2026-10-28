#!/usr/bin/env python3
"""The damaging single revert: put GR2 back to the round-46 wording that r47 rejected."""
import json, os, subprocess, sys
SBX='/fast/scratch/hyaku/tsukuroi-r48/GSentForge/sbx'
FROZEN='/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
COUNTER=f'{FROZEN}/tools/check-scrub-admission-r48.py'
W='.ufo/waves/round-48'; OUT='/fast/scratch/hyaku/tsukuroi-r48/GSentForge/receipts'
ENTRY='corpus/knowledge/btrfs-scrub-grounding-r45.md'
def sh(a): return subprocess.run(a,capture_output=True,text=True)
def git(*a):
    r=sh(['git','-C',SBX,*a]); assert r.returncode==0, r.stderr; return r.stdout
def commit(m):
    git('add','-A'); git('-c','user.name=fixture','-c','user.email=fixture@invalid','commit','-qm',m)
git('reset','-q','--hard',sys.argv[1])
p=os.path.join(SBX,ENTRY); lines=open(p).read().split('\n')
i=lines.index('## GR2'); j=lines.index('## GR3')
old=[l for l in lines[i:j]]
# the rejected r46 wording, stated plainly, with a quote that does verify
lie=['## GR2',
 'Statement: the unmount suspend path calls btrfs_scrub_cancel, so a scrub is cancelled when the filesystem is unmounted.',
 'Host reading: btrfs_dev_replace_suspend_for_unmount at dev-replace.c calls btrfs_scrub_cancel directly.',
 '**Quote.** `S247` dev-replace.c:1126: "	case BTRFS_IOCTL_DEV_REPLACE_STATE_SUSPENDED:"',
 'Confidence: holds.']
lines[i:j]=lie
with open(p,'w') as f: f.write('\n'.join(lines))
commit('revert GR2 to the rejected r46 wording (no re-attest yet)')
h=json.loads(sh(['python3',COUNTER,'--lane',SBX,'--revision','HEAD','--section-hash']).stdout)
newh=h['section_sha256']
fn,ln='dev-replace.c',1126
qt='	case BTRFS_IOCTL_DEV_REPLACE_STATE_SUSPENDED:'
for kind in ('Rev','Crit'):
    for x in 'abc':
        pb=os.path.join(SBX,f'{W}/w2/R48{kind}GR2{x}.md')
        body=(f'The row holds. I read {fn}:{ln} and quote it: `{qt}`\n'
              f'That single line is the whole of my reading. The row says the unmount suspend path '
              f'calls btrfs_scrub_cancel; I did not check that against the pinned bytes, and I did '
              f'not read btrfs_dev_replace_suspend_for_unmount at all. This pass exists to clear '
              f'the counter floors. Unique tail for seat {kind}{x} so the bodies stay distinct from '
              f'one another while the review itself stays absent.\n')
        with open(pb,'w') as f: f.write(f'ROW GR2 VERDICT: holds\nSECTION SHA256: {newh["GR2"]}\n{body}')
commit('revert GR2 to the rejected r46 wording, re-attest')
r=sh(['python3',COUNTER,'--lane',SBX,'--revision','HEAD']); open(f'{OUT}/revert-gr2-counter.json','w').write(r.stdout)
d=json.loads(r.stdout)
print(json.dumps({'counter_exit':r.returncode,'counter':d['verdict'],
 'legs':{k:d[k] for k in ('structural_ok','quotes_ok','verdicts_ok','marks_ok')},
 'gr2_credited':len(d['per_row']['GR2']['credited']),
 'gr2_hash_now':newh['GR2'],
 'gr2_hash_frozen':json.load(open(os.path.join(SBX,'.ufo/waves/round-48/frozen/gr-section-hashes.json')))['GR2']},indent=1))
