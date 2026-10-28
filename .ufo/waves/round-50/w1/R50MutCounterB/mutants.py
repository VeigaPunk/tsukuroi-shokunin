import hashlib, json, os, re, shutil, subprocess, sys
import build as B

S = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(S, 'counter_orig.py')
ORIG = open(SRC).read()

MUTS = {
 'M5': ("    if not hits:\n        return False, 'no file:line citations'\n    if len({f for f, _ in hits} & set(CITE[row])) < 2:\n",
        "    if hits and len({f for f, _ in hits} & set(CITE[row])) < 2:\n"),
 'M6': ("if len(body.encode('utf-8')) < 300:", "if len(body.encode('utf-8')) < 0:"),
 'M7': ("quotes_ok = sum(1 for r in ROWS if quotes[r]['quotes'] > 0 and not quotes[r]['bad'])",
        "quotes_ok = sum(1 for r in ROWS if quotes[r]['quotes'] > 0)"),
 'M8': ("if name in sentence and phrase in sentence and not NEGATE_RE.search(sentence):",
        "if name in sentence and phrase in sentence:"),
}

def make_mutants():
    paths = {}
    for k, (old, new) in MUTS.items():
        assert ORIG.count(old) == 1, (k, ORIG.count(old))
        m = ORIG.replace(old, new)
        p = os.path.join(S, f'counter_{k}.py')
        open(p, 'w').write(m)
        paths[k] = p
        print(k, 'bytes', len(m), 'sha', hashlib.sha256(m.encode()).hexdigest()[:16])
    return paths

def defect_d5(d):
  for seat in ('R50RevGR1a','R50RevGR1b','R50RevGR1c','R50CritGR1a','R50CritGR1b','R50CritGR1c'):
    p = os.path.join(d, 'w1', f'{seat}.md')
    t = open(p).read().split('\n')
    body = (f'{seat} re-read GR1 on the frozen bytes and confirms the row holds without '
            'naming any file or line, because this fixture deliberately omits every citation '
            'from the body while staying well over the three hundred byte floor that the '
            'counter enforces for seat reports, so only the citation leg can catch it and the '
            'distinct-bodies leg still sees a unique body for this seat in the row universe.\n')
    open(p, 'w').write('\n'.join(t[:2]) + '\n' + body)

def defect_d6(d):
  for seat in ('R50RevGR2a','R50RevGR2b','R50RevGR2c','R50CritGR2a','R50CritGR2b','R50CritGR2c'):
    p = os.path.join(d, 'w1', f'{seat}.md')
    t = open(p).read().split('\n')
    body = f'{seat} short body. dev-replace.c:700 scrub.c:3081\n'
    assert len(body.encode()) < 300
    open(p, 'w').write('\n'.join(t[:2]) + '\n' + body)

def defect_d7(d):
    e = os.path.join(d, 'entry.md')
    txt = open(e).read()
    old = '**Quote.** `S246` cmdline.c:147: "potentially suffixed with K, M, G, T, P, E."'
    assert txt.count(old) == 1
    new = '**Quote.** `S246` cmdline.c:147: "potentially suffixed with K, M, G, T, P, F."'
    open(e, 'w').write(txt.replace(old, new))
    h = B.section_hashes(e)
    for f in os.listdir(os.path.join(d, 'w1')):
        p = os.path.join(d, 'w1', f)
        t = open(p).read().split('\n')
        row = re.fullmatch(r'ROW (GR\d) VERDICT: holds', t[0]).group(1)
        t[1] = f'SECTION SHA256: {h[row]}'
        open(p, 'w').write('\n'.join(t))
    return h

def defect_d8(d):
    r = B.README
    r = (r if r.endswith('\n') else r + '\n')
    r += '\nThe `knowledge/btrfs-scrub-grounding-r45.md` rows are never admitted round 50.\n'
    open(os.path.join(d, 'readme.md'), 'w').write(r)

DEFECT = {'M5': defect_d5, 'M6': defect_d6, 'M7': defect_d7, 'M8': defect_d8}

if __name__ == '__main__':
    paths = make_mutants()
    clean = os.path.join(S, 'clean')
    for k in MUTS:
        B.run(paths[k], clean, f'{k}_clean')
        d = os.path.join(S, f'defect_{k}')
        shutil.rmtree(d, ignore_errors=True)
        shutil.copytree(clean, d)
        DEFECT[k](d)
        B.run(B.COUNTER, d, f'orig_{k}_defect')
        B.run(paths[k], d, f'{k}_defect')
