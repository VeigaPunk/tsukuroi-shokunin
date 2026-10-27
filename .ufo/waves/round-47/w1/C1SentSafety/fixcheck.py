#!/usr/bin/env python3
"""C1SentSafety: verification of the two proposed remediations, plus the regex-cost probes.

Run: python3 fixcheck.py /path/to/lane/HEAD-report.md
"""
import re
import sys
import time
import unicodedata

NEGATE_OLD = re.compile(r'unadmitted|not admitted|never admitted|stay pending|stays pending')
MARK_README = ('btrfs-scrub-grounding-r45.md', 'admitted round 47')


def old_ok(ln):
    """Frozen rule as shipped (counter lines 77-78, 369-371)."""
    return all(x in ln for x in MARK_README) and not NEGATE_OLD.search(ln)


NEG_NEW = re.compile(r"(?:^|[\s\u2014|(\[])(?:un|not|never|no|non)[\s\-]*admitted|pending")


def new_ok(ln):
    """Fallback remediation: NFKC + NBSP->space + casefold + whitespace collapse."""
    s = unicodedata.normalize('NFKC', ln).replace('\u00a0', ' ')
    s = ' '.join(s.casefold().split())
    if not all(x in s for x in MARK_README):
        return False
    head, _, tail = s.partition('admitted round 47')
    return not NEG_NEW.search(head[-40:]) and not NEG_NEW.search(tail)


CASES = [
    ('A1 capital N', '| `knowledge/btrfs-scrub-grounding-r45.md` | Not admitted round 47: still pending |'),
    ('A2 NBSP', '| `knowledge/btrfs-scrub-grounding-r45.md` | not\u00a0admitted round 47; still pending |'),
    ('A3 control', '| `knowledge/btrfs-scrub-grounding-r45.md` | not admitted round 47: still pending |'),
    ('A4 homoglyph', '| `knowledge/btrfs-scrub-grounding-r45.md` | \u043d\u043e\u0442 admitted round 47, row pending |'),
    ('GENUINE 1', '| `knowledge/btrfs-scrub-grounding-r45.md` | GR1-GR3 admitted round 47 (all three holds) |'),
    ('GENUINE 2', '| `knowledge/btrfs-scrub-grounding-r45.md` | admitted round 47 after two amendments |'),
]

CITE_RE = re.compile(r'\b([A-Za-z0-9_.@+-]+\.[a-z0-9]+):(\d+)\b')
CITE_POSS = re.compile(r'\b([A-Za-z0-9_.@+-]++\.[a-z0-9]++):(\d+)\b')


def hits_tok(body, cap=512):
    out = []
    for tok in body.split():
        out.extend(CITE_RE.findall(tok[:cap]))
    return out


def main():
    print(f'python {sys.version.split()[0]}')
    print(f"{'case':14} {'shipped':8} {'fixed':8}")
    for name, ln in CASES:
        print(f'{name:14} {str(old_ok(ln)):8} {str(new_ok(ln)):8}')
    for kib in (16, 64):
        body = 'a.' * (kib * 512)
        t = time.perf_counter()
        a = len(CITE_RE.findall(body))
        t1 = time.perf_counter() - t
        t = time.perf_counter()
        b = len(CITE_POSS.findall(body))
        t2 = time.perf_counter() - t
        assert a == b == 0
        print(f'CITE shipped {kib}KiB {t1:.4f}s | possessive {t2:.4f}s (still quadratic)')
    for kib in (16, 64, 1024):
        body = 'a.' * (kib * 512)
        t = time.perf_counter()
        n = len(hits_tok(body))
        print(f'token-split {kib}KiB {time.perf_counter() - t:.4f}s hits={n}')
    if len(sys.argv) > 1:
        real = open(sys.argv[1], encoding='utf-8').read()
        print('recall on real report:', CITE_RE.findall(real) == hits_tok(real),
              len(CITE_RE.findall(real)), 'hits')
        mix = real + '\n' + 'a.' * (512 * 1024)
        t = time.perf_counter()
        hits_tok(mix)
        print(f'token-split mixed real+512KiB: {time.perf_counter() - t:.4f}s')


if __name__ == '__main__':
    main()
