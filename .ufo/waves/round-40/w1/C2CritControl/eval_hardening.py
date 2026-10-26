#!/usr/bin/env python3
"""Evaluate two candidate hardening conjuncts against the honest entry and the mechanical writer."""
import importlib.util
import re
import subprocess
import sys
from pathlib import Path

LANE = Path('/home/vgpnk/Projects/shokunin/tsukuroi-shokunin')
MECH = Path(sys.argv[1])
sys.path.insert(0, str(LANE / 'tools'))
spec = importlib.util.spec_from_file_location('c2', LANE / 'tools/check-exec-environment-r40.py')
c2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c2)
src, cap = c2.load_frozen()
vals = c2.derive_values(src)


def cells(text, ex):
    for l in text.splitlines():
        if re.match(r'^\|\s*' + ex + r'\s*\|', l):
            return [c.strip() for c in l.strip().strip('|').split('|')]
    return None


def analyze(text, label):
    print('==', label)
    for ex in sorted(c2.REQUIRED):
        want = c2.REQUIRED[ex]
        c = cells(text, ex)
        if not c:
            print(ex, 'MISSING')
            continue
        rule, value, scell = c[1], c[2], c[3]
        ref = next(((int(a), int(b or a)) for f, a, b in c2.REF_RE.findall(scell) if f == want), None)
        lo, hi = ref
        window = c2.collapse(' '.join(src[want].splitlines()[lo - 1:hi])).lower()
        toks = list(c2.TOKENS[ex]) + ([vals['EX4_default']] if ex == 'EX4' else [])
        hits = [t for t in toks if c2.collapse(t).lower() in window]
        tok_words = set(re.findall(r'[a-z0-9_./+-]{4,}', c2.collapse(' '.join(toks) + ' ' + value).lower()))
        vocab = set(re.findall(r'[a-z0-9_./+-]{4,}', src[want].lower()))
        rw = set(re.findall(r'[a-z0-9_./+-]{4,}', c2.collapse(rule).lower()))
        extra = sorted((rw - tok_words) & vocab)
        print(f'{ex} window {want}:{lo}-{hi} token_hits={hits} extra_vocab={len(extra)} {extra[:8]}')


analyze(subprocess.run(['git', '-C', str(LANE), 'show', 'HEAD:corpus/knowledge/pacman-exec-environment-r40.md'],
                       capture_output=True, text=True).stdout, 'honest author entry @f951f28')
analyze((MECH / 'corpus/knowledge/pacman-exec-environment-r40.md').read_text(), 'mechanical writer')
