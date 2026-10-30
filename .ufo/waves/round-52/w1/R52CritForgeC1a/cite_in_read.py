#!/usr/bin/env python3
"""Independent reviewer check for a real C1 PASS: for each of the 18 counted seats, the report's
pinned-source citations must fall inside line ranges that seat's OWN transcript shows it opened,
and the transcript must show the seat opened the row bytes and wrote the report path.

The counter (tools/check-scrub-admission-r52.py) reads only lane bytes: the report files, the
results registry (name/agent-role/output) and the dispatch registry. It never consults a seat's
transcript, so it cannot tell a seat-authored report from a hand-written one. This check does.

Inputs: lane report files + history://<agentId> transcripts (harness-side).
"""
import json
import os
import re
import sys

LANE = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
WAVE = os.path.join(LANE, '.ufo/waves/round-52')
READY = os.path.join(WAVE, 'w1.ready.partial')

# Snapshot file -> the line ranges the transcript shows the seat opened.
# A read selector may carry several comma-joined ranges, e.g. `scrub.c:1220-1305,1490-1565`.
OPEN_RE = re.compile(r'frozen/(?:src|hostcap)/(?P<f>[A-Za-z0-9_.@+-]+)(?::(?P<sel>[0-9,\-]+))?')
RANGE_RE = re.compile(r'(\d+)(?:-(\d+))?')
# Any mention of a pinned file in a tool call (read/grep/bash) counts as ACCESS.
ACCESS_RE = re.compile(r'(?:read|grep|bash)\(([^)]*frozen/(?:src|hostcap)/[^)]*)\)')
CITE_RE = re.compile(r'\b([A-Za-z0-9_.@+-]+\.[a-z0-9]+):(\d+)\b')
SNAP_FILES = {'cmdline.c', 'vsprintf.c', 'kstrtox.c', 'sysfs.c', 'scrub.c', 'ioctl.c',
              'dev-replace.c', 'systemd.kill.xml', 'btrfs-scrub@.service', 'capture.txt',
              'SHA256SUMS', 'FETCH.txt'}


def opened_ranges(transcript):
    """basename -> list of (lo, hi) ranges read; a whole-file access gives (1, 10**9)."""
    ranges = {}
    for m in OPEN_RE.finditer(transcript):
        f = m.group('f')
        sel = m.group('sel')
        if sel:
            for rm in RANGE_RE.finditer(sel):
                lo = int(rm.group(1))
                hi = int(rm.group(2)) if rm.group(2) else lo
                ranges.setdefault(f, []).append((lo, hi))
        else:
            ranges.setdefault(f, []).append((1, 10 ** 9))
    return ranges


def accessed_files(transcript):
    """basenames of pinned files the seat touched with ANY tool (read/grep/bash)."""
    out = set()
    for m in ACCESS_RE.finditer(transcript):
        for fm in re.finditer(r'frozen/(?:src|hostcap)/([A-Za-z0-9_.@+-]+)', m.group(1)):
            out.add(fm.group(1))
    return out


def main(seats, read_transcript):
    ready = json.load(open(READY))
    out = []
    for seat, role in seats:
        rec = {'seat': seat, 'role': role}
        rep = os.path.join(WAVE, 'w1', seat + '.md')
        rec['report_exists'] = os.path.exists(rep)
        aid = ready.get(seat)
        rec['agent_id'] = aid
        if not rec['report_exists'] or not aid:
            rec['verdict'] = 'NO-REPORT' if not rec['report_exists'] else 'NO-AGENT-ID'
            out.append(rec)
            continue
        body = open(rep, encoding='utf-8').read()
        rec['first_line'] = body.split('\n')[0]
        rec['second_line'] = body.split('\n')[1]
        tr = read_transcript(aid)
        rec['transcript_len'] = len(tr)
        rec['wrote_lane_report'] = os.path.join(WAVE, 'w1', seat + '.md') in tr
        rec['has_yield'] = 'yield(' in tr
        rec['mentions_section_hash'] = 'SECTION SHA256' in tr
        rec['read_row_bytes'] = bool(re.search(r'entry\.md:\d+', tr))
        rng = opened_ranges(tr)
        acc = accessed_files(tr)
        rec['opened_files'] = sorted(rng)
        rec['accessed_files'] = sorted(acc)
        # every citation of a PINNED source must name a file the seat actually touched
        bad = []
        for f, ln in CITE_RE.findall(body):
            if f not in SNAP_FILES:
                continue
            spans = rng.get(f) or []
            if f not in acc:
                bad.append(f'{f}:{ln} (seat never accessed {f})')
            elif spans and not any(lo <= int(ln) <= hi for lo, hi in spans):
                bad.append(f'{f}:{ln} (seat opened {spans})')
        rec['citations_outside_read_ranges'] = bad
        rec['verdict'] = 'OK' if (rec['wrote_lane_report'] and rec['has_yield']
                                  and rec['read_row_bytes'] and not bad) else 'SUSPECT'
        out.append(rec)
    return out


if __name__ == '__main__':
    print('import-only module; run through eval for history:// access')
