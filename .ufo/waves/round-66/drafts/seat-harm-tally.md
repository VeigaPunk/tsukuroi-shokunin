2026-11-03T21:16:48Z

# E3Mistake — seat-harm incident tally (considerthese proposal "Seat-harm incident log")

Seat: E3Mistake (executor, round 66 wave w1). Read-only; no tracked file edited.

Proposal, verbatim (`considerthese/2026-10-26.md:19`):

> **Seat-harm incident log.** Seat-to-seat damage on the shared host (pkill, `/tmp` misroot, the
> round-37 fleet-root misroot) is now a recurring class separate from seat loss. A running tally
> per round would show whether isolation fixes are actually landing.

## 1. The item's sweep command, as run

```
$ cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
$ grep -n -E 'SEAT|misroot|pkill' corpus/lessons/round-37*.md corpus/lessons/round-39.md corpus/lessons/round-40.md corpus/lessons/round-41.md
corpus/lessons/round-37-verifier-spotcheck.md:23:| Fleet misroot | `git -C /home/vgpnk/Projects/shokunin status --porcelain` | no `corpus/` …
corpus/lessons/round-37.md:102:| R37-MISROOT-NOTE-DRAFT | misroot | Fleet root `git -C /home/vgpnk/Projects/shokunin status --porcelain` listed `?? corpus/` …
corpus/lessons/round-37.md:103:| R37-SEAT-REPORT-COUNT | number-drift | LOG.md "Round-37 W1 integration after WAVE-DONE" and the review-integration section above …
corpus/lessons/round-39.md:74:| R39-SEAT-PKILL | landing | Wave seat C1SentMounts ran `pkill -f 'tsukuroi-census\.sh'` at about 03:05 local …
grep_rc=0
```

Output lines above are excerpts (cut at the dispatcher's display width); the full rows were read
at the cited line numbers and are quoted in §2 (exclusions in §3).

### Per-file rc — the case-sensitive pattern misses two named incidents

```
$ for f in corpus/lessons/round-37.md corpus/lessons/round-37-verifier-spotcheck.md \
           corpus/lessons/round-39.md corpus/lessons/round-40.md corpus/lessons/round-41.md; do
    out=$(grep -n -E 'SEAT|misroot|pkill' "$f"); rc=$?; echo "FILE=$f rc=$rc"; done
FILE=corpus/lessons/round-37.md rc=0
FILE=corpus/lessons/round-37-verifier-spotcheck.md rc=0
FILE=corpus/lessons/round-39.md rc=0
FILE=corpus/lessons/round-40.md rc=1
FILE=corpus/lessons/round-41.md rc=1
```

Calibration finding: `R40-TMP-MISROOT` (`round-40.md:81`) and `R41-TMP-MISROOT-REPEAT`
(`round-41.md:80`) exist but contain uppercase `MISROOT`, so the lowercase `misroot` branch of
the item's pattern does not match them; the round-40 and round-41 files return rc 1. The rows
were read by id instead:

```
$ grep -n 'R40-TMP-MISROOT' corpus/lessons/round-40.md
81:| R40-TMP-MISROOT | landing | Seats ran `tools/check-self-assessment.py` without `TMPDIR`; each run extracted a 294 MB lane archive under `/tmp` …
rc=0
$ grep -n 'R41-TMP-MISROOT-REPEAT' corpus/lessons/round-41.md
80:| R41-TMP-MISROOT-REPEAT | landing | A wave seat ran `tools/check-self-assessment.py` at the dispatch tip, where the round-40 fix was still uncommitted, and a 300 MB lane archive was built under `/tmp` …
rc=0
$ grep -in 'misroot' corpus/lessons/round-40.md
81:| R40-TMP-MISROOT | landing | …
rc=0
$ grep -in 'misroot' corpus/lessons/round-41.md
80:| R41-TMP-MISROOT-REPEAT | landing | …
91:3. R40-TMP-MISROOT: `tools/check-self-assessment.py --scratch` (archive and census child TMPDIR under it).
rc=0
```

The case-insensitive form returns rc 0 on both files, confirming the miss is casing, not absence.

## 2. Incidents (one row per incident, fields as the source rows state them)

| Round | Id | Class | What the fix was (as the row states it) | Source |
|---|---|---|---|---|
| 37 | `R37-MISROOT-NOTE-DRAFT` | misroot | The draft is preserved byte-exact at `.ufo/waves/round-37/misroot/corpus/knowledge/journalctl-v262-field-filter-r36.md` (sha256 `c65a8d41db3b04521134455449c67b8ff3220539b9e47e4c1d9fdb4530223ac3`; `cmp` equal before deletion); it is not placed at the note's lane path (that would overwrite the committed C2 note with an unreviewed seat edit); the fleet copy and its empty `corpus/` directories were deleted; the red sweep (`?? corpus/`) shows the check can fail and no longer lists it after deletion; the draft is not adopted (C2 frozen). | `corpus/lessons/round-37.md:102` |
| 39 | `R39-SEAT-PKILL` | landing | No fix at the time ("none — the wave context forbade host mutation but said nothing about signalling processes the seat did not start"); wave contexts from round 40 say "signal only processes you started (by PID); never `pkill`/`killall` by pattern"; census numbers are cited only from clean runs or runs after 03:05, and the L1's final receipts re-measure every claim number. | `corpus/lessons/round-39.md:74` |
| 40 | `R40-TMP-MISROOT` | landing | Routed to round 41: "the tool takes `--scratch` and passes it to its census child. Not yet shown able to fail; no evidence cites a `/tmp` path (SentScope grep, 0 hits)." | `corpus/lessons/round-40.md:81` |
| 41 | `R41-TMP-MISROOT-REPEAT` | landing | "the `--scratch` fix lands with this round's integration commit; `w1/RoutedSelfAssessScratch.md` shows it able to fail (old tool: census child under `/tmp`; new: none)." | `corpus/lessons/round-41.md:80` |
| 41 | `R41-CAPTURE-FIFO` | survivor | "`[ -f \"$FX/mounts\" ]` guard in the injected line" — a capture-line `cp` blocked on the FIFO fixture, timing out the run (pre-freeze, rc 124; the orphaned `cp` stayed blocked 2 h 10 min until the L1 killed it). | `corpus/lessons/round-41.md:74` |

Provenance note: the item's grep matched four rows (37, 39, plus two non-incidents below);
`R41-CAPTURE-FIFO` was not matched by that pattern. It is included because the round-45
seat-harm ledger counts round 41 as two incidents and names it (see §5), and it is a
seat-to-seat shared-host damage row. No other round-41 row is added.

## 3. Matched rows excluded from the tally (not seat-to-seat damage)

- `R37-SEAT-REPORT-COUNT` (`corpus/lessons/round-37.md:103`, class `number-drift`): a
  seat-report counting error in LOG/review text (63 stated vs 62 observed), fixed by deriving
  seat counts with the dispatch-name loop. No host damage and no seat-to-seat effect. Excluded.
- `corpus/lessons/round-37-verifier-spotcheck.md:23` "Fleet misroot": a verifier check row whose
  result is `pass` ("no `corpus/` (the lane repaired it)"). It is the check on the round-37
  incident above, not an incident. Excluded.

## 4. Round 65 — marked 0 incidents

```
$ grep -c 'R65-.*SEAT\|misroot' corpus/lessons/round-65.md
0
grep_rc=1
$ ls -l corpus/lessons/round-65.md
-rw-r--r-- 1 vgpnk vgpnk 13604 Nov  3 17:33 corpus/lessons/round-65.md
rc=0
```

Round 65: **0 incidents** (0 lines matching `R65-.*SEAT` or `misroot`; grep rc 1 = no match,
not an error). Limit of the count: it is the item's two-shape pattern over
`corpus/lessons/round-65.md`; other seat-harm shapes in that lesson were not scanned, and no
absence claim is made beyond this command.

## 5. Cross-check against the existing round-45 ledger

The lane already has a ten-incident ledger (rounds 37-44) under the same proposal:
`corpus/lessons/round-45.md:124`. Its per-round counts for rounds 37-41, with the exact ids:

```
$ grep -n -E '^\| (37|38|39|40|41) \|' corpus/lessons/round-45.md
140:| 37 | 1 | `R37-MISROOT-NOTE-DRAFT` |
141:| 38 | 0 | — |
142:| 39 | 1 | `R39-SEAT-PKILL` |
143:| 40 | 1 | `R40-TMP-MISROOT` |
144:| 41 | 2 | `R41-TMP-MISROOT-REPEAT`, `R41-CAPTURE-FIFO` |
grep_rc=0
```

This seat's rows agree with that ledger for rounds 37, 39, 40 and 41 (2). Rounds 42-44 are
out of this item's named sources and are not re-read here; the round-45 ledger remains the
authority for them. Round 38 is 0 in the ledger and is not counted here either (no row).

## 6. Scope

Sources read: the item's named lesson files only — `corpus/lessons/round-37*.md`,
`round-39.md`, `round-40.md`, `round-41.md`, plus `round-65.md` for the zero count and
`round-45.md` for the cross-check. The row text is quoted as the rows state it; no fix was
re-verified and no incident was re-investigated. This is a tally, not a new audit.
