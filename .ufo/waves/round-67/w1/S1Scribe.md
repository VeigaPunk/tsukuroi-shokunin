2026-11-03T22:05:45Z
# S1Scribe — seat report (tsukuroi lane, round 67, wave w1)

Seat: **S1Scribe** (scribe). Item: **C1-SCRIBE** — C1 knowledge note and two registry rows,
prose draft only. Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`. Writes: the draft
`.ufo/waves/round-67/drafts/S1Scribe-c1-note.md` and this report. No `corpus/` file written, no
census or selftest run, no git/jj mutation, no sudo, no pacman, no installs, no subagents.

## Axes named

1. **Depth / C1 truth** — every v7.3 and v7.1 fact in the note is a located line in a pinned file,
   re-read by this seat with its command and output below.
2. **Registry shape** — both rows NF 13, no pipe inside any cell, S284 directly after S283.
3. **Gate fidelity** — each row has URL, access date 2026-11-03, a quote of at most 25 words with
   its location.
4. **Watch honesty** — QUALITY 98 logged re-read of r42/r43: which hunks change, which statements
   stay true, none claimed where not observed.

## Pinned bytes re-read by this seat (commands and rc)

| # | command | rc | observed |
|---|---|---|---|
| 1 | `sha256sum -c SHA256SUMS` (in `.ufo/waves/round-67/before/src/`) | 0 | `scrub.c: OK`, `CHANGES: OK` |
| 2 | `grep -n 'Revert to the older scrub limits' .../before/src/scrub.c` | 0 | `1640:	/* Revert to the older scrub limits. */` (one hit) |
| 3 | `awk 'NR>=1596 && NR<=1608' frozen/src/scrub.c` (v7.1) | 0 | :1596 `for (i = 0; ...)`, :1597 `/* Revert to the older scrub limit. */`, :1598 `ret = write_scrub_device_limit(fdmnt, di_args[i].devid, sp[i].old_limit);`, :1605 `if (sp[i].skip)`, :1608 `ret = pthread_join(t_devs[i], NULL);` |
| 4 | `awk 'NR>=1596 && NR<=1650' before/src/scrub.c` (v7.3) | 0 | :1596 `for (...)` result loop, :1597-1598 `if (sp[i].skip) continue;`, :1600 `pthread_join(t_devs[i], NULL)`, :1638 `}`, :1640 `/* Revert to the older scrub limits. */`, :1641 `for (i = 0; i < fi_args.num_devices; ++i) {`, :1642 `write_scrub_device_limit(...sp[i].old_limit)`, :1645-1646 warning text, :1648 `}`, :1650 `if (do_print) {` |
| 5 | `sha256sum` frozen v7.1 and pinned v7.3 `scrub.c` | 0 | `48df2e2f…8f0801` (v7.1), `b58942cc…d528` (v7.3) — both match declaration |
| 6 | `awk 'NR==1||NR==20' before/src/CHANGES` | 0 | `1: btrfs-progs-7.3 (2026-10-23)`, `20:    * scrub limit: set to the original limit only after all devices finish` |
| 7 | `grep -n 'pthread_create\|pthread_join' ...` both copies | 0 | thread creates at :1565 and :1585 in both; v7.3 join at :1600, v7.1 join at :1608 |
| 8 | `diff -u frozen/src/scrub.c before/src/scrub.c \| grep -c '^@@'` | 0 | `4` hunks: `@@ -568,7 +568,7 @@` (typo "pos"→"position"), `@@ -1372,7 +1372,7 @@` (`ie.`→`i.e.` comment, line 1375 both), `@@ -1594,14 +1594,6 @@` (in-loop revert removed), `@@ -1645,6 +1637,16 @@` (post-loop revert added) |
| 9 | `diff -u frozen/src/CHANGES before/src/CHANGES \| grep -c '^@@'` | 0 | `1` hunk (7.3 and 7.2-skipped entries inserted at top) |
| 10 | line-shift check of every `scrub.c:N` cited by r42+r43 against v7.3 (python, read-only) | 0 | 47 distinct lines; 42 byte-identical at same line; 5 shift +2 (1698→1700, 1706→1708, 1833→1835, 1931→1933, 1946→1948) |
| 11 | `grep -n 'Revert to the older scrub limit' .../frozen/src/scrub.c` (v7.1) | 0 | `1597` only (singular "limit") |
| 12 | `awk 'NR==460||NR==467||NR==468' frozen/src/CHANGES` vs v7.3 `NR==487||494||495` | 0 | v7.1 460/467/468 = 6.6.3 header and two scrub bullets; v7.3 487/494/495 = same text |
| 13 | `grep -in 'revert\|old_limit\|scrub limit\|throughput limit' corpus/knowledge/btrfs-scrub-record-r42.md corpus/knowledge/btrfs-scrub-record-r43.md` | 0 | no `revert` and no `old_limit` in either note; `scrub limit` / `throughput limit` appear only as the 6.6.3 bullet, the sysfs attribute, and the SC5 / SR-free text (r42 lines 13, 16, 125-141, 203) |
| 14 | `awk -F'|' '/^\| S283 /{print NF}' corpus/SOURCES.md` | 0 | `13`; `grep -cE '^\| S[0-9]+ \|' corpus/SOURCES.md` → `283` (S283 last row) |
| 15 | `grep -c 'btrfs-progs/blob/v7.3' corpus/SOURCES.md` | 1 | `0` — no v7.3 URL already registered |

Word counts (`printf '%s' '<quote>' | wc -w`): S284 quote `/* Revert to the older scrub limits. */` → 8;
S285 quote `* scrub limit: set to the original limit only after all devices finish` → 13.

## Host applicability (E1Probe receipts, read by this seat, not re-run)

`.ufo/waves/round-67/probes/e1-applicability.md`: `APPLICABILITY: No`. Observed in the receipts:
one btrfs fs (`/dev/mapper/root`, `Total devices 1`, `devid 1`), `scrub_speed_max` = `0`,
`/var/lib/btrfs` absent, `btrfs-scrub@-.timer` `disabled`, `btrfs scrub status /` = `no stats
available`, installed `btrfs-progs 7.1-1`. The `MISSING` token in `btrfs filesystem show` is a
privilege artefact (`/dev/dm-0` `Permission denied`, `CapEff` zero), recorded by E1Probe as BLOCKED
and cross-checked against `findmnt` / `df` in the note's Limits.

## Deliverable

- `.ufo/waves/round-67/drafts/S1Scribe-c1-note.md` — sections `## NOTE` (body of
  `corpus/knowledge/btrfs-scrub-limit-revert-r67.md`, provenance trio first), `## ROWS` (S284,
  S285, 11 cells each), `## GATE` (Gate record per row, located quote, word count, supporting lines).
- The note's Watch section records the r42/r43 re-read: the two revert-bearing hunks, the two
  non-behavioural hunks, the 42 unchanged and 5 shifted cited lines, and that neither note states
  when the limit is restored (so nothing is contradicted).

## Self-checks on the draft (run after writing)

| command | rc | observed |
|---|---|---|
| `grep -c '^| S28[45] |' .../S1Scribe-c1-note.md` | 0 | `2` |
| `awk -F'|' '/^\| S28[45] \|/ {print NF}' .../S1Scribe-c1-note.md` | 0 | `13` `13` |
| `grep -E '^\| S28[45] \|' ... \| awk '{print gsub(/\|/,"|")}'` | 0 | `12` `12` (11 cells, no stray pipe) |
| `grep -nE '^\| SL[0-9]+ \|' ...` | 0 | 4 lines, SL1–SL4 at lines 35–38 |
| `grep -nE '^\| SL' ... \| grep -vE '^[0-9]+:\| SL[0-9]+ \|'` | 1 | empty — no other row begins `| SL` |
| `grep -n '^| row | claim | evidence |' ...` | 0 | line 33 (table header) |
| pipes per SL row | 0 | `4` each (3 cells) |
| first three NOTE lines | 0 | `source:` / `verified-at:` / `recheck:` (provenance trio) |

## Limits of this seat

- Nothing was executed on the host beyond reads; no scrub, no sysfs write, no timer, no record file.
- Non-author verification of S284/S285 (live re-open, quote re-count) is the scout's and the closure
  judge's job; the Gate block marks those fields `pending non-author verification` and does not
  claim them.
- The v7.1 Arch package carries no verified ordering (the Arch recipe is not reachable from this
  host); recorded as `[unknown]` in the note.
- An earlier draft's Limits enumerated some lines the note does not cite; corrected in the rewrite
  (the enumerated lines now match the cited ones: S284 → 1600, 1638, 1650; S237 → 1597, 1598,
  1601, 1602, 1605, 1608; S285 → CHANGES line 1).

## Tooling record

No installs. Read-only utilities only (`sha256sum`, `grep`, `awk`, `diff`, `python3` read-only
line comparison, `wc`, `date`). No tool installed or upgraded.

## Scratch

Scratch `/fast/scratch/hyaku/tsukuroi-r67/S1Scribe/` (holds `scrub.diff`) is removed before yield.
A stray copy `/fast/scratch_scrub_diff.txt` written outside the scratch root is removed too.
