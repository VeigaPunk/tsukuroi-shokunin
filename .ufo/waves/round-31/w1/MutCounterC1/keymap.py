#!/usr/bin/env python3
"""Map source vocabulary -> sealed answer-key groups (dictionary attack over the snapshot text).

Used only to build a positive control fixture for the C1 mutation test: the counter's R7
requires the statement to contain, per question, one word whose salted digest is in each
sealed group. The digests are sha256('tsukuroi-r31 ' + word)[:16].
"""
import hashlib
import json
import os
import re
import sys

SALT = 'tsukuroi-r31'
KEYHASH = {
    'Q01': [['e9f83bb8c4fb0c83', 'e042504e4f57919e', '8df0eb4a526f579d', '996b00bd8f1b370d'], ['1e66576b2db2c6d8', '14f7a27a9c172703', '0a272dcbfb26dfc1', '68ddfdcb4477a00b', 'da1d499cd919a133'], ['2bbfee52fcdcb998']],
    'Q02': [['3a4813eea4487192'], ['61e28ad79423b1c7'], ['0b1ca4a2eb109fd8']],
    'Q03': [['c9750f12e3d1243f', '911cf51c6bcc67a5'], ['8c3fc6432ae36fb8']],
    'Q04': [['3d96f80cb16d26f7'], ['799a3d51ae7e194e'], ['5bd906efc6b93c51', 'f1bd9034c4680457']],
    'Q05': [['97a2c6bc7c5443e1', 'fd91650e3a3b2942'], ['0b1ca4a2eb109fd8'], ['74cf638237a546c3'], ['113742ff0d19e837', 'cd033c7f3fc9a42c']],
    'Q06': [['812c2b78f3ecf74e'], ['cad259cab1cc5604', 'c90ae5532c805905', '310b77b4f9eceb8a', '7a3a87e0891cf387'], ['c40ee4515577800c']],
    'Q07': [['0d7c981d8b9cf553'], ['97da85b585bb19c3', '8ea70292222061c3'], ['f7168bd13229f123']],
    'Q08': [['86d37128605fd526'], ['666af48e08924b62'], ['6ca322cbae2da243', 'c77f5f3f237f5170']],
}
FILES = {'Defragmentation.rst': 'Q01', 'btrfs-rescue.rst': 'Q02', 'btrfs-check.rst': 'Q03',
         'ch-mount-options.rst': 'Q04', 'btrfs-replace.rst': 'Q07', 'Trim.rst': 'Q08'}


def words(text):
    return re.findall(r"[a-z0-9][a-z0-9=_.+/-]*", text.lower())


def digest(w):
    return hashlib.sha256((SALT + ' ' + w).encode()).hexdigest()[:16]


def main():
    snapdir = sys.argv[1]
    hits = {}
    for fname in sorted(os.listdir(snapdir)):
        if not fname.endswith('.rst'):
            continue
        text = open(os.path.join(snapdir, fname), encoding='utf-8').read()
        toks = set(words(text))
        pieces = set()
        for w in list(toks):
            for p in re.split(r'[-/.]', w):
                if p:
                    pieces.add(p)
        for w in toks | pieces:
            d = digest(w)
            for qid, groups in KEYHASH.items():
                for gi, g in enumerate(groups, 1):
                    if d in g:
                        hits.setdefault((qid, gi), []).append((fname, w))
    for (qid, gi), lst in sorted(hits.items()):
        print(qid, 'group', gi, sorted(set(w for _, w in lst)), '->',
              sorted(set(f for f, _ in lst)))
    json.dump({f'{k[0]}-{k[1]}': sorted(set(w for _, w in v)) for k, v in hits.items()},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'keymap.json'), 'w'),
              indent=1)


if __name__ == '__main__':
    main()
