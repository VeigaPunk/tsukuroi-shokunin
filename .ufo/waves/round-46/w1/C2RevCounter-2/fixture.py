#!/usr/bin/env python3
"""C2RevCounter-2 fixtures for check-scrub-admission-r46.py review. Scratch-only; never touches the lane."""
import json, os, shutil, subprocess, sys

S = '/fast/scratch/hyaku/tsukuroi-r46/C2RevCounter-2'
LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
IMPL = 'a44770491eb5ca15ce9f8b3207309d1af683ffaf'
CTR = LANE + '/tools/check-scrub-admission-r46.py'
ENTRY = 'corpus/knowledge/btrfs-scrub-grounding-r45.md'
W46 = '.ufo/waves/round-46'
H_IMPL = 'fe77ac765c7dd9f568e0b296ce8c7f8f53de3d8966d6a2029bada662badf9ca8'
DIR = None

def sh(*a):
    return subprocess.run(list(a), capture_output=True, text=True)

def git(*a):
    return sh('git', '-C', DIR, *a)

def commit(msg):
    g = git('add', '-A')
    assert g.returncode == 0, g.stderr
    c = git('-c', 'user.name=fixture', '-c', 'user.email=fixture@invalid', 'commit', '-q', '-m', msg)
    assert c.returncode == 0, c.stderr
    return git('rev-parse', 'HEAD').stdout.strip()

def counter(rev, *extra):
    return sh('python3', CTR, '--revision', rev, '--lane', DIR, *extra)

def lastj(p):
    return json.loads(p.stdout.strip().splitlines()[-1])

def clone(name):
    global DIR
    DIR = f'{S}/{name}'
    shutil.rmtree(DIR, ignore_errors=True)
    r = sh('git', 'clone', '-q', '--shared', LANE, DIR)
    assert r.returncode == 0, r.stderr
    git('remote', 'remove', 'origin')
    top = git('rev-parse', '--show-toplevel').stdout.strip()
    assert top == DIR, f'toplevel {top} != {DIR}'
    git('checkout', '-q', '--detach', IMPL)

def read(p):
    with open(f'{DIR}/{p}') as f:
        return f.read()

def write(p, s):
    os.makedirs(os.path.dirname(f'{DIR}/{p}'), exist_ok=True)
    with open(f'{DIR}/{p}', 'w') as f:
        f.write(s)

def report(seat, row, h):
    body = ('Evidence for GR1 against the pinned snapshot bytes. cmdline.c:150 decides the memparse radix '
            'path; kstrtox.c:30 decides the suffix handling; sysfs.c:2035 decides the EINVAL on trailing '
            'text. ' + 'filler text for the 300 byte body floor. ' * 6)
    return f'ROW {row} VERDICT: holds\nSECTION SHA256: {h}\n{body}\n'

def add_w9(h):
    write(f'{W46}/w9-dispatch.json', json.dumps(
        {'taskCall': {'tasks': [{'name': 'V46RevGR1a', 'agent': 'reviewer'},
                                {'name': 'V46RevGR1b', 'agent': 'reviewer'}]}}))
    write(f'{W46}/w9-results.json', json.dumps(
        {'results': [{'name': 'V46RevGR1a', 'agent': 'reviewer'},
                     {'name': 'V46RevGR1b', 'agent': 'reviewer'}]}))
    write(f'{W46}/w9/V46RevGR1a.md', report('V46RevGR1a', 'GR1', h))
    write(f'{W46}/w9/V46RevGR1b.md', report('V46RevGR1b', 'GR1', h))

def gr1_row(entry):
    lines = entry.split('\n')
    i = lines.index('## GR1')
    j = i + 1
    while not lines[j].startswith('## '):
        j += 1
    return '\n'.join(lines[i:j])

out = []

def log(tag, obj):
    out.append(f'== {tag}\n{obj}\n')
    print(f'== {tag}')
    print(obj)

# ---------- FX1: embedded "## " line opens an unbound tail inside GR1 ----------
clone('fxmain')
e = read(ENTRY)
ann = ('## Annotation — round 46 probe (header terminates the counted section)\n'
       'TAIL-V1: admission of GR1 does not depend on the bytes below this header.\n')
e1 = e.replace('## GR2\n', ann + '\n## GR2\n', 1)
assert e1 != e
write(ENTRY, e1 + '\n## Gate status — round 46 (GR1-GR3 admitted)\n')
sk = read('SKILL.md')
write('SKILL.md', sk + '\n## Scrub grounding — round 46 admission\n')
rd = read('corpus/README.md')
write('corpus/README.md', rd + '\nbtrfs-scrub-grounding-r45.md: admitted round 46 (GR1-GR3).\n')
revA = commit('A: entry annotation + marks')
hh = lastj(counter(revA, '--section-hash'))
log('FX1 section-hash at A', json.dumps(hh['section_sha256'], sort_keys=True))
assert hh['section_sha256']['GR1'] == H_IMPL, 'GR1 hash must be unchanged by the annotation'

add_w9(H_IMPL)
revB = commit('B: w9 records binding two GR1 seats on current bytes')
pB = counter(revB)
jB = lastj(pB)
log('FX1 counter at B', json.dumps({k: jB[k] for k in ('r45_legs_ok', 'verdicts_ok', 'marks_ok', 'verdict')}, sort_keys=True))
log('FX1 GR1 row at B', json.dumps({k: jB['per_row']['GR1'][k] for k in ('section_sha256', 'bound_on_current', 'any_fails', 'row_ok')}, sort_keys=True))

e2 = read(ENTRY).replace('TAIL-V1: admission of GR1 does not depend on the bytes below this header.',
                         'TAIL-V2: the GR1 row now also claims something unvetted and weak.', 1)
assert e2 != read(ENTRY)
write(ENTRY, e2)
revC = commit('C: in-row bytes moved after the terminating header; no seat re-read')
jC = lastj(counter(revC))
hC = lastj(counter(revC, '--section-hash'))
diff = git('diff', '--unified=1', f'{revB}..{revC}', '--', ENTRY)
log('FX1 diff B..C (entry, in-row change)', diff.stdout)
log('FX1 counter at C', json.dumps({k: jC[k] for k in ('r45_legs_ok', 'verdicts_ok', 'marks_ok', 'verdict')}, sort_keys=True))
log('FX1 GR1 row at C', json.dumps({k: jC['per_row']['GR1'][k] for k in ('section_sha256', 'bound_on_current', 'any_fails', 'row_ok')}, sort_keys=True))
log('FX1 hash B vs C', json.dumps({'at_B': hh['section_sha256']['GR1'], 'at_C': hC['section_sha256']['GR1']}))

# control: make the annotation header non-terminating -> bytes become bound again
e3 = read(ENTRY).replace('## Annotation — round 46 probe', '### Annotation — round 46 probe', 1)
write(ENTRY, e3)
revD = commit('D: control — non-terminating header')
hD = lastj(counter(revD, '--section-hash'))
jD = lastj(counter(revD))
log('FX1 control at D', json.dumps({'GR1_hash': hD['section_sha256']['GR1'], 'equals_impl_hash': hD['section_sha256']['GR1'] == H_IMPL,
                                    'bound_on_current': jD['per_row']['GR1']['bound_on_current'], 'row_ok': jD['per_row']['GR1']['row_ok']}))

# ---------- FX5: negating text still grants the skill/readme marks ----------
write('SKILL.md', read('SKILL.md').replace('## Scrub grounding — round 46 admission',
                                           '## Scrub grounding — round 46 admission (WITHHELD — rows stay pending)', 1))
write('corpus/README.md', read('corpus/README.md').replace(
    'btrfs-scrub-grounding-r45.md: admitted round 46 (GR1-GR3).',
    'btrfs-scrub-grounding-r45.md remains unadmitted round 46.', 1))
write(ENTRY, read(ENTRY).replace('## Gate status — round 46 (GR1-GR3 admitted)',
                                 '## Gate status — round 46 (GR1-GR3 not admitted)', 1))
revE = commit('E: negating marks text')
jE = lastj(counter(revE))
log('FX5 marks under negating text', json.dumps({'marks': jE['marks'], 'marks_ok': jE['marks_ok']}, sort_keys=True))

# ---------- FX1b: duplicate ## GR1 header — only the FIRST block is hashed ----------
write('SKILL.md', read('SKILL.md').replace(' (WITHHELD — rows stay pending)', '', 1))
write('corpus/README.md', read('corpus/README.md').replace(
    'btrfs-scrub-grounding-r45.md remains unadmitted round 46.',
    'btrfs-scrub-grounding-r45.md: admitted round 46 (GR1-GR3).', 1))
write(ENTRY, read(ENTRY).replace('## Gate status — round 46 (GR1-GR3 not admitted)',
                                 '## GR1\nDUP-TAIL-V1: a second GR1 section appended after admission.\n\n'
                                 '## Gate status — round 46 (GR1-GR3 admitted)', 1))
revF = commit('F: duplicate ## GR1 header, operative text in second block')
hF = lastj(counter(revF, '--section-hash'))
write(ENTRY, read(ENTRY).replace('DUP-TAIL-V1: a second GR1 section appended after admission.',
                                 'DUP-TAIL-V2: the operative duplicated row text just moved.', 1))
revG = commit('G: duplicated row text moved')
hG = lastj(counter(revG, '--section-hash'))
log('FX1b duplicate-header hashes F vs G', json.dumps({'at_F': hF['section_sha256']['GR1'],
                                                       'at_G': hG['section_sha256']['GR1'],
                                                       'equals_impl_hash': hG['section_sha256']['GR1'] == H_IMPL}))

# ---------- FX3: deeply nested dispatch JSON crashes the counter ----------
clone('fxsec')
deep = '{"taskCall":{"tasks":[],"deep":' + '[' * 50000 + ']' * 50000 + '}}'
write(f'{W46}/zz-deep-dispatch.json', deep)
revR1 = commit('R1: deeply nested dispatch json')
pR1 = counter(revR1)
log('FX3 crash run', json.dumps({'exit': pR1.returncode, 'stdout_bytes': len(pR1.stdout),
                                 'stderr_first': (pR1.stderr.strip().splitlines() or [''])[0],
                                 'stderr_last': (pR1.stderr.strip().splitlines() or [''])[-1]}))

# ---------- FX4: wave name ".." reads the report from outside round-46 ----------
git('rm', '-q', f'{W46}/zz-deep-dispatch.json')
write(f'{W46}/..-dispatch.json', json.dumps({'taskCall': {'tasks': [{'name': 'V46RevGR1a', 'agent': 'reviewer'}]}}))
write(f'{W46}/..-results.json', json.dumps({'results': [{'name': 'V46RevGR1a', 'agent': 'reviewer'}]}))
write('.ufo/waves/V46RevGR1a.md', report('V46RevGR1a', 'GR1', H_IMPL))
revR2 = commit('R2: wave named .. with report outside round-46')
jR2 = lastj(counter(revR2))
log('FX4 traversal bind', json.dumps(jR2['per_row']['GR1']['seats']['V46RevGR1a'], sort_keys=True))
probe = sh('git', '-C', DIR, 'show', f'{revR2}:.ufo/waves/round-46/../V46RevGR1a.md')
log('FX4 git-show probe', json.dumps({'rc': probe.returncode, 'head': probe.stdout.splitlines()[:1],
                                      'err': probe.stderr.strip().splitlines()[:1]}))

with open(f'{S}/fixture-results.txt', 'w') as f:
    f.write('\n'.join(out))
print('DONE')
