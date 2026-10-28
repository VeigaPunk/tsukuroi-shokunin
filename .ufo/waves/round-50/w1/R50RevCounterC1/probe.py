#!/usr/bin/env python3
"""R50RevCounterC1 receipt driver: every finding in the report is regenerated here.

Writes receipts.jsonl next to this file. Scratch under /fast/scratch/hyaku/tsukuroi-r50/R50RevCounterC1.
Read-only on the lane: the counter is invoked, never edited; no git mutation anywhere.
"""
import json, os, shutil, subprocess, sys
LANE='/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
REV='8029cdba1049df25632c91a23c8db4eefb54be5f'
CNT=os.path.join(LANE,'tools/check-scrub-admission-r50.py')
HERE=os.path.dirname(os.path.abspath(__file__))
S='/fast/scratch/hyaku/tsukuroi-r50/R50RevCounterC1'

def show(p):
    r=subprocess.run(['git','-C',LANE,'show',f'{REV}:{p}'],capture_output=True)
    return r.stdout.decode('utf-8') if r.returncode==0 else None

ENTRY=show('corpus/knowledge/btrfs-scrub-grounding-r45.md')
SKILL='# SKILL\n## Scrub grounding — round 50 admission\n'
README='The rows in btrfs-scrub-grounding-r45.md are admitted round 50.\n'
HASH={'GR1':'3a2ba1807a7f2308acb11b2f928f85dba5156c6eb9fe865216a06ba2a843fee1',
      'GR2':'a2e955cefbd110ced928407c79b2cedb3cc431734487aa29e74682b23aeb7f3f',
      'GR3':'43430a14069598947d225c1f8ae897d9baea1c0e268cb88c2b5ad9e247bbc32c'}
SRC={'GR1':['cmdline.c','vsprintf.c','kstrtox.c','sysfs.c'],
     'GR2':['dev-replace.c','scrub.c','sysfs.c','ioctl.c'],
     'GR3':['systemd.kill.xml','btrfs-scrub@.service','scrub.c','capture.txt']}
SEATS={r:[(f'R50RevGR{r[2:]}{x}','reviewer') for x in 'abc']+[(f'R50CritGR{r[2:]}{x}','critic') for x in 'abc'] for r in ('GR1','GR2','GR3')}
FILLER=(' This paragraph exists only to carry the report body past the three-hundred-byte floor that '
        'the frozen counter applies to every seat report, so that the citation legs are the only legs '
        'under test in this fixture run of the counter.')*2
DEF={'GR1':[('cmdline.c',156),('vsprintf.c',86)],
     'GR2':[('dev-replace.c',700),('scrub.c',3159)],
     'GR3':[('systemd.kill.xml',68),('btrfs-scrub@.service',9)]}
ADM=ENTRY.replace('## Gate status — round 50 (pending; the round-50 cohort has not settled)',
                  '## Gate status — round 50 (GR1-GR3 admitted)')
LOG=[]
def rec(tag, **kw):
    LOG.append({'probe':tag, **kw})

def body(row, seat, cites):
    c=' '.join(f'{f}:{n}' for f,n in cites)
    return f'{seat} reads {row}. The deciding lines are {c}.{FILLER}'

def mkcohort(d, cites=None, bodies=None, hashmap=None):
    os.makedirs(d, exist_ok=True)
    dispatch={'taskCall':{'tasks':[]}}; results={'results':[]}
    for row in ('GR1','GR2','GR3'):
        for seat,role in SEATS[row]:
            c=(cites or {}).get(seat) or DEF[row]
            b=(bodies or {}).get(seat) or body(row,seat,c)
            h=(hashmap or HASH)[row]
            open(os.path.join(d,f'{seat}.md'),'w').write(f'ROW {row} VERDICT: holds\nSECTION SHA256: {h}\n{b}\n')
            dispatch['taskCall']['tasks'].append({'name':seat,'agent':role})
            results['results'].append({'name':seat,'agent':role,'output':'done'})
    json.dump(dispatch,open(os.path.join(d,'dispatch.json'),'w'))
    json.dump(results,open(os.path.join(d,'results.json'),'w'))

def run(entry=ADM, wave=None, tag='run'):
    d=os.path.join(S,'out',tag); os.makedirs(d,exist_ok=True)
    ep=os.path.join(d,'entry.md'); open(ep,'w').write(entry)
    sp=os.path.join(d,'skill.md'); open(sp,'w').write(SKILL)
    rp=os.path.join(d,'readme.md'); open(rp,'w').write(README)
    cmd=['python3',CNT,'--revision',REV,'--entry-file',ep,'--skill-file',sp,'--readme-file',rp]
    if wave: cmd+=['--wave-dir',wave,'--results-file',os.path.join(wave,'results.json'),
                   '--dispatch-file',os.path.join(wave,'dispatch.json')]
    r=subprocess.run(cmd,capture_output=True,text=True,env={**os.environ,'TMPDIR':S})
    return r.returncode, json.loads(r.stdout)

def sec(entry,tag):
    d=os.path.join(S,'out',tag); os.makedirs(d,exist_ok=True)
    ep=os.path.join(d,'entry.md'); open(ep,'w').write(entry)
    r=subprocess.run(['python3',CNT,'--revision',REV,'--entry-file',ep,'--section-hash'],capture_output=True,text=True)
    return json.loads(r.stdout)

def row1(out,row='GR1'):
    return out.get('per_row',{}).get(row,{})

def main():
    # P0 production invocation at the freeze revision (no overrides)
    r=subprocess.run(['python3',CNT,'--revision',REV],capture_output=True,text=True,env={**os.environ,'TMPDIR':S})
    o=json.loads(r.stdout)
    rec('P0-production-at-freeze', rc=r.returncode, verdict=o.get('verdict'),
        structural_ok=o.get('structural_ok'), corr_ok=o.get('corr_ok'), quotes_ok=o.get('quotes_ok'),
        verdicts_ok=o.get('verdicts_ok'), seats_ok=o.get('seats_ok'), marks_ok=o.get('marks_ok'),
        counter_field=o.get('counter'), section_sha256=o.get('section_sha256'),
        output_keys=sorted(o.keys()))

    # P1 clean K-pass on an admitted-heading fixture
    w=os.path.join(S,'wA'); mkcohort(w)
    rc,o=run(wave=w,tag='P1'); rec('P1-kpass', rc=rc, verdict=o.get('verdict'), verdicts_ok=o.get('verdicts_ok'), seats_ok=o.get('seats_ok'), marks_ok=o.get('marks_ok'))

    # P2 junk citations: line 1 of two row sources per row, plus one lane artifact
    c={s:[(SRC[r][0],1),(SRC[r][1],1),('entry.md',5)] for r in ('GR1','GR2','GR3') for s,_ in SEATS[r]}
    w=os.path.join(S,'wB'); mkcohort(w,cites=c)
    rc,o=run(wave=w,tag='P2'); rec('P2-junk-citations-line-1', rc=rc, verdict=o.get('verdict'), verdicts_ok=o.get('verdicts_ok'), seat_notes=o.get('seat_notes'))

    # P3 entry.md:999999 rejected (the LANE_FILES line-count check works)
    c={s:DEF[r] for r in ('GR1','GR2','GR3') for s,_ in SEATS[r]}
    c['R50RevGR1a']=DEF['GR1']+[('entry.md',999999)]
    w=os.path.join(S,'wC'); mkcohort(w,cites=c)
    rc,o=run(wave=w,tag='P3'); rec('P3-entry-999999', rc=rc, verdict=o.get('verdict'), verdicts_ok=o.get('verdicts_ok'), seat_notes=o.get('seat_notes'))

    # P4 entry.md at the phantom line count('\n')+1
    n=ENTRY.count('\n')+1
    c['R50RevGR1a']=DEF['GR1']+[('entry.md',n)]
    w=os.path.join(S,'wD'); mkcohort(w,cites=c)
    rc,o=run(wave=w,tag='P4'); rec('P4-entry-phantom-line', rc=rc, verdict=o.get('verdict'), verdicts_ok=o.get('verdicts_ok'),
                                  cited_line=n, real_lines=len(ENTRY.split('\n'))-1, seat_notes=o.get('seat_notes'))

    # P5 GR3 cites kernel scrub.c:3000, out of the btrfs-progs S237 snapshot range
    c={s:DEF[r] for r in ('GR1','GR2','GR3') for s,_ in SEATS[r]}
    for s,_ in SEATS['GR3']: c[s]=[('systemd.kill.xml',68),('scrub.c',3000)]
    w=os.path.join(S,'wE'); mkcohort(w,cites=c)
    rc,o=run(wave=w,tag='P5'); rec('P5-cross-snapshot-scrub.c', rc=rc, verdict=o.get('verdict'), verdicts_ok=o.get('verdicts_ok'), seat_notes=o.get('seat_notes'))

    # P6 snapshot phantom line scrub.c:3338 (kernel S242 has 3337 lines)
    for s,_ in SEATS['GR2']: c[s]=[('dev-replace.c',700),('scrub.c',3338)]
    w=os.path.join(S,'wR'); mkcohort(w,cites=c)
    rc,o=run(wave=w,tag='P6'); rec('P6-snapshot-phantom-line', rc=rc, verdict=o.get('verdict'), verdicts_ok=o.get('verdicts_ok'), seat_notes=o.get('seat_notes'))

    # P7 one row source + declared lane artifacts + padding -> refused
    c={s:DEF[r] for r in ('GR1','GR2','GR3') for s,_ in SEATS[r]}
    for s,_ in SEATS['GR1']:
        c[s]=[('cmdline.c',156),('entry.md',5),('FROZEN.md',10),('check-scrub-admission-r50.py',130),('SHA256SUMS',3)]
    w=os.path.join(S,'wM'); mkcohort(w,cites=c)
    rc,o=run(wave=w,tag='P7'); rec('P7-one-source-plus-artifacts', rc=rc, verdict=o.get('verdict'), verdicts_ok=o.get('verdicts_ok'), seat_notes=o.get('seat_notes'))

    # P8 two junk row sources + artifact padding -> PASS
    for s,_ in SEATS['GR1']:
        c[s]=[('cmdline.c',1),('vsprintf.c',1),('FROZEN.md',10),('entry.md',5)]
    w=os.path.join(S,'wN'); mkcohort(w,cites=c)
    rc,o=run(wave=w,tag='P8'); rec('P8-two-junk-sources-plus-artifacts', rc=rc, verdict=o.get('verdict'), verdicts_ok=o.get('verdicts_ok'), seat_notes=o.get('seat_notes'))

    # P9 a real lane artifact outside the whitelist (the round-49 critic report) -> refused
    c={s:DEF[r] for r in ('GR1','GR2','GR3') for s,_ in SEATS[r]}
    for s,_ in SEATS['GR2']: c[s]=DEF['GR2']+[('R49CritGR2b.md',12)]
    w=os.path.join(S,'wP'); mkcohort(w,cites=c)
    rc,o=run(wave=w,tag='P9'); rec('P9-round49-critic-report-cited', rc=rc, verdict=o.get('verdict'), seat_notes=o.get('seat_notes'))

    # P10 corpus/SOURCES.md cited (the entry's own source: line names it) -> refused
    for s,_ in SEATS['GR2']: c[s]=DEF['GR2']+[('SOURCES.md',1)]
    w=os.path.join(S,'wQ'); mkcohort(w,cites=c)
    rc,o=run(wave=w,tag='P10'); rec('P10-SOURCES.md-cited', rc=rc, verdict=o.get('verdict'), seat_notes=o.get('seat_notes'))

    # P11 url:port in a body -> seat refused
    c={s:DEF[r] for r in ('GR1','GR2','GR3') for s,_ in SEATS[r]}
    b={s:body('GR1',s,DEF['GR1'])+' See https://example.com:8443/scrub for the record.' for s,_ in SEATS['GR1']}
    w=os.path.join(S,'wO'); mkcohort(w,cites=c,bodies=b)
    rc,o=run(wave=w,tag='P11'); rec('P11-url-port-in-body', rc=rc, verdict=o.get('verdict'), verdicts_ok=o.get('verdicts_ok'), seat_notes=o.get('seat_notes'))

    # P12 distinct bodies: trailing-space padding collapses (repair works)
    b0=body('GR1','R50RevGR1a',DEF['GR1'])
    b={'R50RevGR1a':b0,'R50RevGR1b':'\n'.join(l+'   ' for l in b0.split('\n'))}
    w=os.path.join(S,'wF'); mkcohort(w,cites=c,bodies=b)
    rc,o=run(wave=w,tag='P12'); rec('P12-trailing-space-pad', rc=rc, verdict=o.get('verdict'), verdicts_ok=o.get('verdicts_ok'),
                                     distinct=row1(o).get('distinct_bodies'), credited=row1(o).get('credited'))

    # P13 distinct bodies: one internal double space -> distinct (repair hole)
    b={'R50RevGR1a':b0,'R50RevGR1b':b0.replace('deciding','deciding  deciding',1)}
    w=os.path.join(S,'wG'); mkcohort(w,cites=c,bodies=b)
    rc,o=run(wave=w,tag='P13'); rec('P13-internal-double-space', rc=rc, verdict=o.get('verdict'), verdicts_ok=o.get('verdicts_ok'),
                                     distinct=row1(o).get('distinct_bodies'), credited=row1(o).get('credited'))

    # P14 C9/C10: defects paraphrased in-row, the four required strings parked after every row
    L=ADM.split('\n')
    for i,ln in enumerate(L):
        if ln.startswith('[inference: how `btrfs scrub start`'):
            L[i]='[inference: how the btrfs-progs CLI prints these returns, and the ioctl side with it, is not pinned here]'
        elif ln.startswith('**Quote.** `S247` dev-replace.c:1128: "* Scrub doing the replace'):
            L[i]="**Quote.** `S247` dev-replace.c:1128: Scrub doing the replace isn't running so we need to do the"
        elif ln.startswith('- Round 50: the widened S247 ranges still do not list'):
            L[i]='- Round 50: the S247 ranges were left as registered; the cancel and suspend lines are cited above.'
        elif ln.startswith('source: ') and 'S240' in ln:
            L[i]=ln.replace('S240','S999')
    H='\n'.join(L)+('\n\n<!-- round-50: strings parked outside every row extent -->\n'
        '[inference: how `btrfs scrub start` and `btrfs scrub status` print these returns is not pinned here\n'
        'source: S240\n'
        'dev-replace.c:1128: "* Scrub doing the replace\n'
        'the widened S247 ranges still do not list\n')
    sh=sec(H,'P14h'); w=os.path.join(S,'wH'); mkcohort(w,hashmap=sh['section_sha256'])
    rc,o=run(entry=H,wave=w,tag='P14')
    rec('P14-c9-strings-parked-outside-rows', rc=rc, verdict=o.get('verdict'), corr_ok=o.get('corr_ok'),
        corr49_missing=o.get('corr49_missing'), corr49_forbidden_present=o.get('corr49_forbidden_present'),
        structural_ok=o.get('structural_ok'), quotes_ok=o.get('quotes_ok'), verdicts_ok=o.get('verdicts_ok'),
        gr2_hash=sh['section_sha256']['GR2'], frozen_gr2_hash=HASH['GR2'],
        defect_lines=[l for l in H.split('\n') if 'btrfs-progs CLI prints' in l or 'dev-replace.c:1128: Scrub' in l],
        parked_lines=[l for l in H.split('\n') if l.startswith('source: S240') or l.startswith('the widened S247')])

    # P15 structural: a '## ' line inside GR1 silently truncates the extent
    L=ADM.split('\n'); g1=L.index('## GR1')
    L2=L[:g1+40]+['## note (truncates the extent silently)']+L[g1+40:]
    for i in range(g1+42,len(L2)):
        if L2[i].startswith('**Quote.** `S246` kstrtox.c:29:'):
            L2[i]='**Quote.** `S246` kstrtox.c:29: "line number deliberately wrong, parsed only if inside the extent"'
            break
    I='\n'.join(L2); sh=sec(I,'P15h'); w=os.path.join(S,'wI'); mkcohort(w,hashmap=sh['section_sha256'])
    rc,o=run(entry=I,wave=w,tag='P15')
    rec('P15-inner-heading-truncation', rc=rc, verdict=o.get('verdict'), structural_ok=o.get('structural_ok'),
        problems=o.get('problems'), quotes_ok=o.get('quotes_ok'), verdicts_ok=o.get('verdicts_ok'),
        gr1_quotes=row1(o).get('quotes'), gr1_hash=sh['section_sha256']['GR1'], frozen_gr1_hash=HASH['GR1'])

    # P16 a malformed '**Quote**' line with a bad line number is silently skipped
    L=ADM.split('\n')
    for i,ln in enumerate(L):
        if ln.startswith('**Quote.** `S246` kstrtox.c:29:'):
            L[i]='**Quote** `S246` kstrtox.c:999999: "malformed marker, bad line number, silently skipped"'
            break
    J='\n'.join(L); sh=sec(J,'P16h'); w=os.path.join(S,'wJ'); mkcohort(w,hashmap=sh['section_sha256'])
    rc,o=run(entry=J,wave=w,tag='P16')
    rec('P16-malformed-quote-skipped', rc=rc, verdict=o.get('verdict'), quotes_ok=o.get('quotes_ok'),
        gr1_quotes=row1(o).get('quotes'))

    # P17 duplicate dispatch task name
    w=os.path.join(S,'wK'); mkcohort(w)
    d=json.load(open(os.path.join(w,'dispatch.json')))
    d['taskCall']['tasks'].append({'name':'R50RevGR1a','agent':'critic'})
    json.dump(d,open(os.path.join(w,'dispatch.json'),'w'))
    rc,o=run(wave=w,tag='P17')
    rec('P17-duplicate-dispatch-task', rc=rc, verdict=o.get('verdict'), verdicts_ok=o.get('verdicts_ok'),
        seats_ok=o.get('seats_ok'), seat_notes=[n for n in o.get('seat_notes',[]) if 'GR1a' in n])


    # P18 a whitespace-only results output still counts as a completed output
    w=os.path.join(S,'wS'); mkcohort(w)
    d=json.load(open(os.path.join(w,'results.json')))
    for e in d['results']:
        e['output']=' '
    json.dump(d,open(os.path.join(w,'results.json'),'w'))
    rc,o=run(wave=w,tag='P18')
    rec('P18-whitespace-output', rc=rc, verdict=o.get('verdict'), seats_ok=o.get('seats_ok'), verdicts_ok=o.get('verdicts_ok'))

    with open(os.path.join(HERE,'receipts.jsonl'),'w') as fh:
        for e in LOG: fh.write(json.dumps(e,sort_keys=True)+'\n')
    print(json.dumps({'probes':len(LOG),'out':os.path.join(HERE,'receipts.jsonl')}))

if __name__=='__main__':
    try: main()
    finally: shutil.rmtree(S, ignore_errors=True)
