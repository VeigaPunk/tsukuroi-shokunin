VERDICT: supports

# C2CounterAtTip — the C2 counter at the lane tip (item C2-F2)

Seat: L2, round 43 / hyaku run 9, wave w2. Revision under test
`8acf0b022586a0f3164c77659fb96ba5f90949b6`; base `6951ead90566b2d74f7c45b4efca29246badad64`.
Nothing in the lane was written except this report and its receipt directory; the counter was run from a
scratch copy, never imported from the lane.

## 1. Counter identity

| check | observed |
|---|---|
| copy of `tools/check-scrub-record-r43.py` in scratch, sha256 | `b4602c566b4f39277e068d27ad10ad0ec361ed7e81a938831cec72631e319854` |
| blob at `8acf0b0:tools/check-scrub-record-r43.py`, sha256 | `b4602c566b4f39277e068d27ad10ad0ec361ed7e81a938831cec72631e319854` |
| frozen pin (dispatch) | `b4602c56…9854` — **matches** |

Evidence: `receipts/counter.sha256` (`sha256sum` of the scratch copy and of `git show 8acf0b0:tools/…`).

## 2. Counter run at the tip

Command (from scratch, `TMPDIR` inside scratch):

```
python3 ./check-scrub-record-r43.py --lane /home/vgpnk/Projects/shokunin/tsukuroi-shokunin \
        --revision 8acf0b022586a0f3164c77659fb96ba5f90949b6
```

Exit `1`; one JSON line. Two runs were byte-identical (`cmp`), so the field set below is stable.

Conjuncts (`receipts/counter-at-tip.json`):

| conjunct | value | predicate target |
|---|---|---|
| `rows` | 3 | 3 ✔ |
| `quotes_ok` | 3 | 3 ✔ |
| `props_ok` | 3 | 3 ✔ |
| `host_ok` | 3 | 3 ✔ |
| `sources_ok` | 1 | 1 ✔ |
| `verdicts_ok` | **0** | 3 ✘ |
| `novelty_base_hits` | 0 | 0 ✔ |
| `pointer_ok` | 1 | 1 ✔ |
| `verdict` | **FAIL** | — |

Also `snapshots_ok: true`, `capture_ok: true`, `sources: {S237: true, S240: true, S241: true, source_line: true}`,
`transcripts_bound: 0`, `transcripts_checked: 0`.

Per-row quote counts as the counter reports them:

| row | good | in_window | bad | files |
|---|---|---|---|---|
| SR1 | 9 | 9 | 0 | scrub.c |
| SR3 | 14 | 13 | 0 | scrub.c |
| SR6 | 10 | 10 | 0 | ioctl.c, scrub.c |

Total 33 quote lines, 0 bad — i.e. every quote in the entry resolves on its named line of a digest-checked
snapshot.

## 3. Independent re-derivation (grep/awk/sed, no use of the tool's code paths)

Method: `git show <rev>:<path>` into scratch for the entry, `corpus/SOURCES.md` (tip and base),
`btrfs-scrub-record-r42.md` (tip and base), `scrub.c`, `ioctl.c`, `capture.txt`; then cell-by-cell shell
checks. Details in `receipts/derivation.txt`, tables in `receipts/quote-table.tsv`,
`receipts/quote-counts.txt`, `receipts/props.txt`, `receipts/sources-pointer.txt`, `receipts/novelty.txt`,
`receipts/host.txt`, `receipts/capture-lines.txt`.

- **Snapshot digests** at the revision: scrub.c `48df2e2f…0801`, ioctl.c `7b3488f2…ba01`, capture.txt
  `f7ecbe7c…c556` — all three equal the pins (capture.txt is 13 lines).
- **rows = 3**: the entry has exactly `## SR1` (line 17), `## SR3` (line 51), `## SR6` (line 97); the other
  `## ` headings are "How this changes OS triage" and "Limits".
- **quotes**: 33 quote lines, each compared as a fixed string against `sed -n "<n>p"` of the snapshot file
  it names (27 `scrub.c→S237`, 6 `ioctl.c→S240`, no crossed id): 33/33 present, 0 bad. Window membership
  recomputed from the counter's frozen window table transcribed by hand
  (`receipts/windows-transcribed.txt`) gives SR1 9/9, SR3 **14 good / 13 in-window** (line 1402 falls
  outside every SR3 window), SR6 10/10 — identical to the counter's numbers.
- **props**: every frozen token is present in the statement cell (block from `**Statement.**` to the first
  Quote/Host line): SR1 `O_TRUNC`, `_tmp`, `rename`, `unlink`; SR3 `scrub_resumed_stats`, `t_start`,
  `do_print`, `-B`, `err`; SR6 `is_scrub_running_in_kernel`, `CAP_SYS_ADMIN`, `EPERM`, `running` — 17/17.
- **host**: SR1 names `capture.txt:7`, SR3 `capture.txt:7`, SR6 `capture.txt:2,6,8,10,7` across its
  three-line cell; all five referenced lines exist (≤13) and are non-blank (`uid 1000 …`,
  `errno=EPERM (1)`, `var_lib_btrfs absent`, `scrub_status_exit 0`, `no stats available`).
- **sources**: S240 and S241 are absent from the base registry (base has S237 only) and at the tip are
  `code` / `own-work`, `mined`, opened `2026-10-26`, used-by naming `corpus/knowledge/btrfs-scrub-record-r43.md`;
  S240's anchor names `v7.2.11`; S237's used-by now names the r43 entry as well as r42; the entry's
  `source:` line names S237, S240, S241.
- **novelty**: at the base, `O_TRUNC` has exactly one hit, `corpus/knowledge/btrfs-scrub-record-r42.md:180`,
  which is at/after the base's `## Corrections — round-42 wave 2` heading (line 170) and so excluded;
  `scrub_resumed_stats` and `is_scrub_running_in_kernel` have 0 hits anywhere in `corpus/knowledge` +
  `SKILL.md`. Hits = 0.
- **pointer**: the r42 entry at the tip names `corpus/knowledge/btrfs-scrub-record-r43.md` on line 4 of its
  first 20 lines (0 occurrences at the base).

**No disagreement.** My hand-derived tuple is
`rows=3 quotes_ok=3 props_ok=3 host_ok=3 sources_ok=1 verdicts_ok=0 novelty_base_hits=0 pointer_ok=1`,
i.e. FAIL on `verdicts_ok` alone — field for field the counter's output, and exactly the state the frozen
claim states for `8acf0b0…`.

## 4. Why `verdicts_ok = 0` is the correct value here (checked, not assumed)

`git show 8acf0b0:.ufo/waves/round-43/w2-dispatch.json` → rc 128, "exists on disk, but not in
'8acf0b022586a0f3164c77659fb96ba5f90949b6'"; `w2-results.json` → "does not exist in
'8acf0b0…'". `git ls-tree -r 8acf0b0 -- .ufo/waves/round-43 | grep w2` returns nothing, and no
`C2RevSR{1,3,6}` / `C2CritSR{1,3,6}` report or `residual-*` file is tracked at the revision. So none of the
six counted seats can bind at the tip, no `partly` is in play, and no residual reviewer is required — the
value is 0 by absence, which is what the frozen counter says it must measure. (In the working tree
`w2-dispatch.json` exists uncommitted, and `w2/` holds C2CritSR1/C2CritSR6 reports and C2* dirs, but the
counter reads the revision, not the worktree, so those cannot count.)

## 5. Observations (no effect on any conjunct value)

1. The counter's host check collects `hl` only from lines that *begin* with `**Host reading.**`, so for a
   multi-line host cell it validates only the cell's first line — for SR6 that is `capture.txt:2`, while
   `:6`, `:8`, `:10`, `:7` on the continuation lines are never looked at. All of them do resolve to
   non-blank capture lines, so `host_ok` is 3 under the narrow and the full-cell reading alike. Worth
   knowing if a future row puts its only dangling ref on a continuation line.
2. SR3's `scrub.c:1402` quote is outside every frozen SR3 window; the row still clears `in_window >= 1`
   through its other 13 in-window quotes. If the window table is ever tightened, this is the quote that
   would be checked first for whether it belongs to the resume-write cell at all.
3. The counter writes nothing: no `tools/__pycache__` exists in the lane after the run (the copy was run
   from scratch), and the only outputs are the two JSON captures in `receipts/`.

## 6. Not done

- The counter was **not** run at the base or at `717b716a…`; that calibration is another seat's item, so I
  cannot speak to base-FAIL / implementation-PASS from this seat.
- `transcripts_bound` is 0/0 because no verdict line exists to look up; I did not attempt any transcript
  reading of my own (it is outside the predicate and outside this item).
- No host mutation of any kind: no scrub, no ioctl beyond reading the frozen capture, no package change;
  nothing installed, so no tooling record is owed.

Report path: `.ufo/waves/round-43/w2/C2CounterAtTip.md`; receipts:
`.ufo/waves/round-43/w2/C2CounterAtTip/`.
