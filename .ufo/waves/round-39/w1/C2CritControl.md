VERDICT: defect-found

# C2-10 — beating `tools/check-transaction-order-r39.py`

Eight of eleven entries whose TO rules are false (`V1`, `V2`, `V3`, `V7`), whose host column contradicts the
capture (`V6`), whose provenance is cross-wired (`V4`, `V10`), or whose rows sit outside the Rules table
(`V8`) score `PASS` from the frozen counter (sha256 `f1c97836abb50887231b82d27cd026d05b8083cefcdd713217071648b07c991e`,
recomputed locally: `f1c97836…c991e`). Two variants fail, which shows the counter does enforce per-file upstream
rows and quote-at-the-cited-lines; the rule *text* is never read.

## Method

```
S=/fast/scratch/hyaku/tsukuroi-r39/C2CritControl; export TMPDIR=$S; mkdir -p $S
D=$(mktemp -d $S/fx.XXXXXX)
git clone -q --shared /home/vgpnk/Projects/shokunin/tsukuroi-shokunin "$D"
git -C "$D" remote remove origin
git -C "$D" rev-parse --show-toplevel            # -> $D (asserted before the first fixture commit)
# identity used only inside $D: -c user.name=fixture-c2crit -c user.email=fixture-c2crit@localhost.invalid
python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-transaction-order-r39.py \
        --repo "$D" --revision <variant sha>      # --branch defaults to master; tip has the variant
```
Baseline: published entry at `4078eb2` in the clone → `PASS`, `rules_verified=8`, `counts_ok=2`,
`{windows:86, transactions_started:60, scriptlet_tag_outside_commit:252, scriptlet_tag_total:441,
running_inside_commit:0}`. Each variant is a commit on `master` in `$D` carrying the entry text below
(SOURCES variant where noted); the counter and frozen snapshots come from the lane, unmodified.

Receipts (entry blob per variant, JSON result per variant): `.ufo/waves/round-39/w1/C2CritControl/`
(`V1..V10.entry.md`, `variants1..4.json`).

| id | mutation of the published entry | truth | counter | sha in `$D` |
|---|---|---|---|---|
| V1 | TO3 rule text inverted: files extracted **before** `pre_install`, `installed`/`upgraded` before the files, pre scriptlet skipped on upgrade; source cell untouched | all four claims FALSE (add.c:470-474 pre scriptlet, add.c:599 db write, add.c:617-619 `installed`, add.c:638-647 post scriptlet) | **PASS** 8/8 | `86187f139fe6` |
| V2 | all 8 rule cells = “Every claim this row would make is the opposite of what libalpm does, and no rule is stated here” | empty of understanding | **PASS** 8/8 | `6e479a3078a6` |
| V3 | all 8 rule cells = `x` | empty | **PASS** 8/8 | `1845192f03b4` |
| V4 | `S217 ` prefixed to every row's source cell; each row keeps its own `file:line “quote”` | S217 names trans.c only (SOURCES:226) — a sync.c/add.c/hook.c/remove.c/util.c row is now “sourced” to trans.c too | **PASS** 8/8 | `67143e993f8d` |
| V4b | every row cites only `S217 trans.c:201-208 “…”` | control | FAIL 1/8 (`no mined upstream row for sync.c/add.c/hook.c/remove.c/util.c`) | `a3c4ca38afd2` |
| V5 | TO7 quote replaced by a sentence absent from remove.c at 699-733 | control | FAIL 7/8 (`no 4-25 word quote found in remove.c at the cited lines`) | `91efe034a94e` |
| V6 | TO1/TO8 host cells assert the opposite while keeping the literal substrings `60 transactions` / `252 of 441` | host column false | **PASS**, `counts_ok=2` | `18459c4a5b75` |
| V7 | every row's source = its S-ids + `<file>:4-4 “Copyright (c) 2006-2025 Pacman Development Team”`, rule cells false | citation is the licence header of the file | **PASS** 8/8 | `6efece5e4e76` |
| V8 | all 8 TO rows moved into a fenced block under a new `## Appendix: machine rows` after Boundaries; the Rules table keeps no row | rows not in the Rules section | **PASS** 8/8 | `c09b30073505` |
| V9 | duplicate `S213` row appended to SOURCES whose title names sync.c | duplicate S-id resolves last-wins | FAIL 5/8, exit 1, no duplicate reported | `affdf4d1f4bc` |
| V10 | new SOURCES row `S219` whose title names **both** `add.c` and `sync.c`; TO2/TO3/TO6 cite S219 only | one row authorizes two files' rules | **PASS** 8/8 | `3231245cd36d` |

## Mechanism (counter line numbers)

- The rule cell is never read. `src_cell, host_cell = cells[2], cells[3]` at
  `tools/check-transaction-order-r39.py:199`; `cells[1]` does not occur anywhere in the file. Everything else
  the counter checks is about the *source* and *host* cells — hence V1/V2/V3/V7.
- Rows are collected file-wide by `ROW_RE` (`:69`, loop `:186-189`), with no section scope — hence V8.
- Quote fidelity is a substring test inside the collapsed cited range (`:211-219`): any 4-25 word fragment of
  those lines satisfies it, so the licence header does (V7) while a fabricated sentence does not (V5).
- Upstream provenance is one title-substring match per wanted file (`:204-206`), and `parse_sources` builds a
  dict keyed by S-id with last-wins (`:142`) — hence V10 (multi-file title) and V9 (silent override).
- Host counts are substring tests (`:223`, `:225`), so a false sentence containing the digits passes (V6).
- Duplicate detection covers only TO ids (`:189`) and `## ` headings (`:177`), not duplicate SOURCES ids.

## Does the declared QUALITY 81 kill rule close it?

Partly, and only through a reviewer. The kill rule bites V1/V2/V7 (“any TO row judged FALSE against the pinned
source at its cited lines”) **if** a seat judges each row. It does not reach:

- V3 — a one-word rule cell makes no claim that can be judged FALSE;
- V6 — the kill rule's scope is “TO row … against the pinned source at its cited lines”; the host column is
  read from the capture, not from a cited line, so a false host sentence is outside its wording;
- V4/V10 — rule text stays true; the defect is in provenance;
- V8 — rows are true and placeable elsewhere.

So the counter's PASS is a statement about citations, exactly as `tool` and declaration say; it is not evidence
of rule truth, and a scoring reader must not take `PASS` as C2 depth proven.

## Smallest safe correction (measured, does not reject the frozen entry)

Three deterministic conjuncts, no truth table, no second authority (implemented in scratch and scored over the
receipt blobs):

```
J1  every TO row lives in the `## Rules (source-level, pacman 54d9411)` section
J2  rule cell has >= 8 content words (len>=5) AND (>=1 backticked token of the rule cell occurs in the
    collapsed cited lines  OR  >=2 content words of the quote occur in the rule cell)
J3  every S-id cited by the row is a mined row opened 2026-10-26, used_by this entry, title carrying
    54d9411, whose title names one of the *files the row's own source cell cites*
```

Measured: frozen entry 8/8 (so the conjuncts are satisfiable by today's PASS entry) — V2 0/8, V3 0/8, V4 1/8,
V7 0/8, V8 0/8, V9 5/8. Residuals: V1 8/8 (order inversion — rule truth, the reviewer's job), V6 8/8 (host
prose), V10 8/8 (a SOURCES row naming two files is legitimate under J3).

Additions I would make alongside J1-J3 rather than in place of them:

1. Duplicate SOURCES ids in the rows cited by the entry → exit 2 (`E-SOURCES-DUP-ID`), instead of last-wins
   (`:142`). V9 shows the override is silent and direction-dependent.
2. Extend the QUALITY 81 kill-rule wording to: “any TO row whose rule text is FALSE, empty or degenerate, or
   whose host-consequence column is FALSE against the frozen capture, judged by a reviewer seat, kills C2”.
   That closes V3 and V6, which no cheap counter conjunct can close.
3. Keep the reviewer `TO<n>: holds|partly|fails — <file:line>` line mandatory; V1 is caught by nothing else.

I would not add a pinned per-row expectation table to the counter: it duplicates the declaration's rule text
and creates a second authority over the same sentences.

## Not done / not touched

No lane file edited, no lane git/jj command run, no host mutation, no pacman, no service, no tool installed.
I did not run pacman live, did not re-verify the capture, and did not judge TO rows other than TO3 (needed to
ground V1's falsity). Scratch (`/fast/scratch/hyaku/tsukuroi-r39/C2CritControl`) removed after the receipts
were copied.

TO3: holds — add.c:470-474
