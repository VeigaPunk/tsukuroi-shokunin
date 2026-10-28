#!/usr/bin/env python3
"""Content-substance probe for counted seats, from committed bytes only.

flag3: a counted seat body that quotes at least one of its cited lines verbatim
(window of N words from the cited line appears in the body) OR covers >= FRAC of
the cited line's content words.
flag1: body cites a pinned file:line but no citation reaches the pinned bytes at all.

Calibration target (must not flag genuine work):
  round-47 w1 counted seats -> each body should show >=1 evidence line
"""
import os, re, sys, json, subprocess

FROZEN = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
SNAP = {}
for root, _, fs in os.walk(os.path.join(FROZEN, '.ufo/waves')):
    for f in fs:
        if f in ('scrub.c', 'sysfs.c', 'cmdline.c', 'vsprintf.c', 'kstrtox.c',
                 'dev-replace.c', 'ioctl.c', 'systemd.kill.xml',
                 'btrfs-scrub@.service', 'capture.txt'):
            SNAP.setdefault(f, []).append(open(os.path.join(root, f), errors='replace').read().split('\n'))
CITE = re.compile(r'\b([A-Za-z0-9_.@+-]+\.[a-z0-9]+):(\d+)\b')
STOP = set('the a an of to in is are and or for on with that this it be as by at from '
           'not no if then than which was were'.split())


def evidence_lines(body, n=4, frac=0.6):
    norm = ' '.join(body.split()).lower()
    got = set()
    for f, ln in CITE.findall(body):
        for lines in SNAP.get(f, []):
            if 1 <= int(ln) <= len(lines):
                words = ' '.join(lines[int(ln) - 1].split()).split()
                if len(words) < n:
                    continue
                if any(' '.join(words[i:i + n]).lower() in norm for i in range(len(words) - n + 1)):
                    got.add((f, ln))
                    continue
                cw = {t.lower().strip('`()[],;:') for t in words
                      if t.lower() not in STOP and len(t) > 2}
                if cw and len({t for t in cw if t in norm}) / len(cw) >= frac:
                    got.add((f, ln))
    return sorted(got)


if __name__ == '__main__':
    body = sys.stdin.read()
    print(json.dumps({'evidence_lines': evidence_lines(body)}, indent=1))
