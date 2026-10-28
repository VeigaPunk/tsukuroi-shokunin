#!/usr/bin/env python3
"""Composition: rewrite all three rows to FALSE claims about the pinned sources,
recompute the hashes, write content-free bodies at the new hashes, keep the marks.
Does the frozen counter still admit the corpus?"""
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
LIE={
'GR1':['## GR1',
       'Statement: the btrfs scrub module parameter is parsed by an unreviewed shell wrapper, not by the kernel parser.',
       'Host reading: no kernel parser is involved anywhere in the scrub parameter path.',
       '**Quote.** `S246` cmdline.c:156: "	unsigned long long ret = simple_strtoull(ptr, &endptr, 0);"',
       'Confidence: holds.'],
'GR2':['## GR2',
       'Statement: the unmount suspend path cancels the running scrub by calling btrfs_scrub_cancel.',
       'Host reading: cancellation happens inside btrfs_dev_replace_suspend_for_unmount, not in btrfs_dev_replace_cancel.',
       '**Quote.** `S247` dev-replace.c:1126: "	case BTRFS_IOCTL_DEV_REPLACE_STATE_SUSPENDED:"',
       'Confidence: holds.'],
'GR3':['## GR3',
       'Statement: the packaged unit sends SIGKILL to every scrub worker, which is why scrubs never resume.',
       'Host reading: KillMode is set to none in the unit file.',
       '**Quote.** `S248` systemd.kill.xml:101: "        <para>Defaults to <option>control-group</option>.</para>"',
       'Confidence: holds.'],
}
git('reset','-q','--hard',sys.argv[1])
p=os.path.join(SBX,ENTRY); lines=open(p).read().split('\n')
for row,new in LIE.items():
    i=lines.index(f'## {row}'); nxt={'GR1':'## GR2','GR2':'## GR3','GR3':'## How this changes OS triage'}[row]
    j=lines.index(nxt)
    lines[i:j]=new
with open(p,'w') as f: f.write('\n'.join(lines))
commit('compose: rows rewritten to claims the pinned sources contradict')
h=json.loads(sh(['python3',COUNTER,'--lane',SBX,'--revision','HEAD','--section-hash']).stdout)
assert h['structural_ok']==1, h
hashes=h['section_sha256']
CITE={'GR1':('cmdline.c',156,'\tunsigned long long ret = simple_strtoull(ptr, &endptr, 0);'),
      'GR2':('dev-replace.c',1126,'\tcase BTRFS_IOCTL_DEV_REPLACE_STATE_SUSPENDED:'),
      'GR3':('systemd.kill.xml',101,'        <para>Defaults to <option>control-group</option>.</para>')}
for row in ('GR1','GR2','GR3'):
    for kind in ('Rev','Crit'):
        for x in 'abc':
            pb=os.path.join(SBX,f'{W}/w2/R48{kind}{row}{x}.md')
            fn,ln,qt=CITE[row]
            body=(f'The row is admitted. I read {fn}:{ln} and quote it: `{qt}`\n'
                  f'That single line is the whole of my reading. I opened no other snapshot, checked '
                  f'no clause of the statement against the cited bytes, and did not test whether the '
                  f'statement follows from this line at all. The claim I am admitting may contradict '
                  f'the very bytes I quoted; I did not look. This paragraph exists only to clear the '
                  f'300-byte floor and to differ from its siblings, so the distinct-bodies rule and '
                  f'the citation rule are both satisfied without any review having happened. '
                  f'Seat {kind}{row}{x} says nothing else.\n')
            with open(pb,'w') as f:
                f.write(f'ROW {row} VERDICT: holds\nSECTION SHA256: {hashes[row]}\n{body}')
commit('compose: content-free bodies at the new hashes')
r=sh(['python3',COUNTER,'--lane',SBX,'--revision','HEAD']); open(f'{OUT}/compose-counter.json','w').write(r.stdout)
d=json.loads(r.stdout)
print(json.dumps({'counter_exit':r.returncode,'counter':d['verdict'],
 'legs':{k:d[k] for k in ('structural_ok','quotes_ok','verdicts_ok','marks_ok')},
 'quotes_per_row':{k:(v['quotes']['ok'],v['quotes']['quotes']) for k,v in d['per_row'].items()},
 'credited':{k:len(v['credited']) for k,v in d['per_row'].items()},
 'hashes_now':hashes,
 'frozen_record_says':json.load(open(os.path.join(SBX,'.ufo/waves/round-48/frozen/gr-section-hashes.json')))},indent=1))
