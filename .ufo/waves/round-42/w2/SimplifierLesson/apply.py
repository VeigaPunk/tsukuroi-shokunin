#!/usr/bin/env python3
"""Apply the F-24 proposals to a copy of the lane and assert line-count / counted-row identity.

    P1 = S in .ufo/waves/round-42/w2/SimplifierLesson.md sec.3  (scope: drop the SH3/SH4 recap, 9 lines -> 9)
    P2 = T in sec.2                                            (triage: 7 lines -> 2)
    P3 = E in sec.4                                            (errata append after the last line)

P1 and P3 move no line number; P2 shifts every line at or below :144 by -5.
"""
import hashlib, os, re, sys

# F24_LANE = root of a clone/copy of the lane (the entry is edited under it). Default: this seat's
# (deleted) scratch clone, kept for provenance. Usage: F24_LANE=/path/to/copy python3 apply.py [P1|P2|P3 ...]
LANE = os.environ.get('F24_LANE', '/fast/scratch/hyaku/tsukuroi-r42/SimplifierLesson/lane')
ENTRY = os.path.join(LANE, 'corpus/knowledge/btrfs-scrub-record-r42.md')

P1_OLD = """The lane already holds what scrub verifies and repairs and that `btrfs scrub status` reads a file under
`/var/lib/btrfs` (`corpus/knowledge/storage-health-r26.md` SH3, SH4; S129, S139), including the record's name
pattern (SH4) and that a scrub run with recording disabled cannot be excluded (SH4 note). It held no statement of the
record itself: how the file is replaced, its line format, which process writes it and when recording is switched off,
how the status command turns per-device lines into one filesystem verdict, and the per-device throughput limit that
same command reports (SC5). Those decide how far "no record" may be read as "never scrubbed". Rows SC1-SC5 state upstream behaviour of btrfs-progs v7.1 (the
version this host runs) from `cmds/scrub.c` and `CHANGES`; the host readings are this machine's, unprivileged.
Nothing here runs a scrub, writes `/var/lib/btrfs` or changes a scrub limit (operator actions)."""

P1_NEW = """The lane already holds, in `corpus/knowledge/storage-health-r26.md`, what scrub verifies and repairs (SH3), the
record's name pattern (SH4) and that a scrub run with recording disabled cannot be excluded (SH4 note). It held no
statement of the record itself: how the file is replaced, its line format, which process writes it and when
recording is switched off, how the status command turns per-device lines into one filesystem verdict, and the
per-device throughput limit that same command reports (SC5). Those decide how far "no record" may be read as
"never scrubbed". Rows SC1-SC5 state upstream behaviour of btrfs-progs v7.1 (the version this host runs) from
`cmds/scrub.c` and `CHANGES`; the host readings are this machine's, unprivileged. Nothing here runs a scrub, writes
`/var/lib/btrfs` or changes a scrub limit (operator actions)."""

P2_OLD = """- Read "no scrub record" as a gap in evidence (`UNVERIFIED`, SH4), not as "never scrubbed" (SC3); what SC3 adds is
  the mechanism, not a new verdict.
- A record is per device; a filesystem `finished` needs every device that has a record finished, and one canceled
  device makes the whole run `aborted` (SC2, SC4).
- `interrupted` is a process outcome (an unfinished record, nothing running), not a media fault; read the error
  sums in the per-device lines (`btrfs scrub status -d`, raw `-R`) before calling the device (SC4).
- Before reading a slow scrub as a device problem, read `scrub_speed_max` (SC5)."""

P2_NEW = """- The operator actions for every scrub-status signal are the decision table under `## Scrub status record — round 42`
  in `SKILL.md` (rows SC1-SC5); what SC3 adds to triage is the mechanism behind "no record", not a new verdict."""

P3 = """## Errata (round 42, append-only)

- 2026-10-26 — **the triage section above restates the operator decision table; recorded, not silently edited.**
  The four bullets at `:144-150` repeat rows of the table under `## Scrub status record — round 42` in `SKILL.md`:
  bullet 1 the `no stats available` and `no scrub.status.<fsid>` rows, bullet 2 the `aborted` and `finished` rows,
  bullet 3 the `interrupted` row, bullet 4 the slow-scrub row. That table is the authority for what to do on a
  signal; this entry's section records what the rows change about reading one. New triage text lands in the table,
  not here. The bullets stay at this revision because wave-2 reports cite `:144`, `:146-149` and `:149-150`; the
  replacement that collapses them (7 lines to 2) is `.ufo/waves/round-42/w2/SimplifierLesson.md` §2, to land once
  those anchors retire.
"""


def sections(text):
    out, cur = {}, None
    for ln in text.splitlines():
        m = re.match(r'^## (SC\d)\s*$', ln)
        if m:
            cur = m.group(1); out.setdefault(cur, []); continue
        if re.match(r'^## ', ln):
            cur = None; continue
        if cur:
            out[cur].append(ln)
    return out


def apply(label, path, old, new):
    t = open(path).read()
    assert t.count(old) == 1, f'{label}: {t.count(old)} matches'
    t2 = t.replace(old, new)
    open(path, 'w').write(t2)
    ol, nl = t.count('\n'), t2.count('\n')
    a, b = sections(t), sections(t2)
    same = a.keys() == b.keys() and all(a[k] == b[k] for k in a)
    wide = [ln for ln in new.split('\n') if len(ln) > 120]
    print(f'{label}: lines {ol} -> {nl} ({nl-ol:+d}); bytes {len(t)} -> {len(t2)} ({len(t2)-len(t):+d})'
          f'; rows SC1-SC5 identical: {same}; lines >120 chars: {len(wide)}')
    return same


which = sys.argv[1:] or ['P1', 'P2', 'P3']
for w in which:
    if w == 'P1':
        assert apply('P1(scope)', ENTRY, P1_OLD, P1_NEW)
    elif w == 'P2':
        assert apply('P2(triage)', ENTRY, P2_OLD, P2_NEW)
    elif w == 'P3':
        t = open(ENTRY).read()
        assert t.endswith('\n')
        open(ENTRY, 'w').write(t + '\n' + P3)
        t2 = open(ENTRY).read()
        a, b = sections(t), sections(t2)
        print(f'P3(errata): appended {len(P3)+1} bytes at tail; lines {t.count(chr(10))} -> {t2.count(chr(10))}'
              f'; rows SC1-SC5 identical: {a.keys() == b.keys() and all(a[k] == b[k] for k in a)}')
