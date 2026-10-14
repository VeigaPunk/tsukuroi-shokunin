# AUD-S11 — verdict table: the final audit (2 claims re-derived) + the census receipt re-run

Lane AUD-S11 (round-11 wave, width 32), 2026-10-14. **Write scope: this file
only** — `reports/r11-aud-s11.md` follows the r7–r10 per-repo audit precedent
(this repo's `r10-aud-s10.md`; siblings `r10-aud-m10.md`, `r10-aud-b10.md`,
`r10-aud-t10.md`);
nothing else in any repo was written, no commit, no `git add`. Scratch
`/tmp/w11-aud-s11-ev/` (raw captures kept: `selftest.{out,err,rc}`,
`live1.*`, `live2.*`, `pins-*`, `status-*`, `head.txt`, `window-*.txt`).

Task (verbatim): **"AUD-S11 — the final audit (2 claims + the census receipt
re-run). Verdict table; do NOT edit."**

**Binding of the "2 claims" (stated, not smoothed):** the dispatch names two
claims without naming their object. This lane binds them to the two terminal
claims the closeout stands on, both named in round-10/round-11 landed
artifacts and both re-derivable read-only at the wave's open:
**C1 — the terminal instrument claim** (identity + counts-move-together +
plane-set consistency; sources: `closeout-r11.md` §0.3/§1.3, `SKILL.md` r10
append) and **C2 — the receipt claim** (`corpus/knowledge/census-closeout-receipt-r10.md`
§0/§3/§4: the hardened gate re-run live). The "census receipt re-run" is
executed as the receipt's own recipe (§5/§7). A different intended pair is a
re-run of this table with new subjects — no row below depends on the binding
beyond its stated subject. **[unk — U1]**

Method: re-hash every audited artifact from disk **and** from the git object
store; execute the census's `--selftest` and two live runs unpiped with
stdout/stderr separate; mechanical SET-MATCH extraction (emitted `PLANE` names
vs rollup keys); re-derive the receipt's recipe and cross-probe table; re-derive
the committed gate arc from `git show <commit>:tools/tsukuroi-census.sh`.
Read-only host probes only: census runs, `md5sum`/`sha256sum`/`wc`/`stat`/
`git show`/`diff`/`grep`, `journalctl --list-boots`, `pacman -Qm`, `stat` on
sync dbs. No `pacman` transaction, no `-Sy`/`-Syu`, no service action, no root,
no external site; `db.lck` absent before/after every run (checked).

Tags: **[obs]** measured in my window with the command named · **[inf]**
inference · **[unk]** unsettled, probe named. Line counts are `wc -l`; the
census, `SKILL.md` and `closeout-r11.md` carry unterminated final lines, so a
Read counts one more — a pin states its convention.

Audit window: **2026-10-14 21:34:24Z – 21:38:13Z** (-0300 18:34–18:38), host
`plazir27`, user `vgpnk` (non-root). The round-11 wave is **in flight** at this
close (U3); every verdict binds the round-10 landed state below.

## 0. Audited bindings

| artifact | revision bound | size | note |
|---|---|---|---|
| lane HEAD | `af8adf15a2f5ea0be458ebc2144ca40ba4469e08` ("probation round 10 (training r9): see LOG", 18:28:23 -03) | — | unchanged through close; tree 0 entries at 21:34:24Z; one untracked entry appeared mid-window (O1) |
| census (`tools/tsukuroi-census.sh`) | md5 `945c76fc6cc548e47b91c23a9637df75` · sha256 `1045244387ffcd5d3db481dd0d3d30e34097abc24744d954e791b81d28b20c11` | 2402 `wc -l` / 126 075 B | mtime 18:03:12.467587319 -03; **worktree == `git show HEAD:` blob** (re-hashed); unchanged across all my runs |
| receipt (`corpus/knowledge/census-closeout-receipt-r10.md`) | md5 `c5041b5d03e38c774637f47a24304ca8` | 183 `wc -l` | mtime 17:54:47 -03; its §2 pin `e32aac98…` / 2349 / 123 410 B re-derived = **`af8adf1~1` blob** (the pre-hardening revision) |
| `SKILL.md` | md5 `19d989b32fb0b4040254a2503d503854` | 1569 `wc -l` | live restatements `:1484`, `:1529` (80 cases) |
| `LOG.md` / `SCORECARD.md` | `0c9b2f02…` / 173 · `52218ee5…` / 22 | — | the closeout note's own §5 pins reproduce |
| `closeout-r11.md` (other seat, S11-1) | moving subject: md5 `bdf80c2f…` / 322 L / 23 833 B at 21:35Z → `817a2867…` / 402 L / 28 613 B at 21:38Z | — | observed shape-only; **no verdict below binds it** |

Current-revision anchors [obs]: `VERSION='census-v2'` `:323`; usage + exit map
`:451` ("0 HEALTHY | 1 DEGRADED | 2 BLOCKED (worst plane wins; usage errors
also 2)"); six `PLANE` emitters `:2377-2382`; rollup `printf` `:2392`;
selftest `mktemp` `:1573` + EXIT/INT/TERM trap `:1574`.

## 1. Verdict table

**C1 — the terminal instrument claim** (identity + counts + plane-set):

| # | check | evidence (this lane) | verdict |
|---|---|---|---|
| C1.1 | identity binding | my re-hash vs the closeout note §0.3 and `SKILL.md:1519-1520`: md5/sha256/2402/126 075 B all equal; `git show HEAD:… \| md5sum` = same bytes | **PASS** |
| C1.2 | landing delta is additive | `git show --numstat af8adf1 -- tools/tsukuroi-census.sh` = `53 0`; `grep -c '^-[^-]'` on the diff = **0** deleted lines; the commit is one round commit (9 files, +2055/−1) | **PASS** |
| C1.3 | executed selftest + counts-move-together | my run `bash tools/tsukuroi-census.sh --selftest` (21:34:47Z): rc=0, wall 24.654 s, 80 `PASS` lines, stderr 0 B, terminal line verbatim `TSUKUROI_CENSUS_SELFTEST: PASS (80 cases, 80 passed, 0 failed)`; static `check`+`check_cli` declarations = **80**; live restatements `SKILL.md:1484`/`:1529` = 80; 17/26/35/49/63/74 stand as history (D3) | **PASS** |
| C1.4 | live runs + plane-set consistency (D11) | two runs, 21:35:17Z / 21:36:07Z, both unpiped: rc=1, **six** `PLANE` lines, names `drivers journal oom packages systemd update-safety`; my own set extraction: emitted-name set == rollup-key set — **SET-MATCH** (`diff` clean); rollup `TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=HEALTHY drivers=DEGRADED journal=DEGRADED update-safety=DEGRADED oom=HEALTHY)`; stderr 0 B both | **PASS** |
| C1.5 | exit map consistency | crown = worst plane = DEGRADED → rc 1, matching the declared map (`:451`); a BLOCKED live exercise was not taken (fail-closed arms are selftest cases — author evidence, verified by the suite's own run in C1.3) | **PASS** |

**C2 — the receipt claim** (the hardened gate re-run live):

| # | check | evidence (this lane) | verdict |
|---|---|---|---|
| C2.1 | receipt identity pin | receipt §2 binds `e32aac98…` / 2349 / 123 410 B; re-derived = `af8adf1~1`'s blob — **true for its revision**; at HEAD the same file is `945c76fc…` / 2402 / 126 075 B (the same commit carries both) | **PASS (drift recorded)** |
| C2.2 | receipt selftest count | receipt §3 binds `PASS (74 cases…)`; at HEAD the executed line is `PASS (80 cases…)` (C1.3) — both true at their revisions; at HEAD counts-move-together holds (executed 80 == restatement 80) | **PASS (drift recorded)** |
| C2.3 | receipt live verdict reproduces | my two runs reproduce §0/§1's verdict-bearing lines exactly: six plane names, the six-key `DEGRADED` rollup, rc=1; field values drifted (C2.6) — the receipt's own §6 doctrine | **PASS** |
| C2.4 | §4 set-match + exit map | SET-MATCH (C1.4); rc=1 with crown DEGRADED | **PASS** |
| C2.5 | §5 zero mutation | census md5 unchanged (before/through/after all runs); `git status --porcelain`: baseline **0 lines**, close 1 line (`?? corpus/knowledge/closeout-r11.md`, S11-1's untracked note — not the gate); `ls /var/lib/pacman/db.lck` absent after every run; no stderr anywhere | **PASS** |
| C2.6 | §6 drift is real and quiet-verdict | my two runs 50 s apart: `diff` = header stamp + drivers row + journal row (`C5_pswp` 76 721 717→76 728 127; `C6_avail_kb` 9 521 372→13 386 380; err 1047→1063, coredump 765→781) — verdict/plane set stable; my window's counts differ from the receipt's window (`coredump` 523→765, `err` 798→1047) as growth, not disagreement | **PASS** |
| C2.7 | §7 cross-probes | `journalctl --list-boots \| wc -l` = **14** (13 + header); `pacman -Qm \| wc -l` = **16**; `stat` sync dbs: core/extra/multilib/omarchy birth `2026-10-11 12:54:13.542054496 -0300` (4 dbs), `offline.db` `2026-10-03 17:41:33.994891750 -0300` — all agree with §7 | **PASS** |

**R — the receipt re-run** (recipe §7/§5, executed by this lane):

| # | recipe step | expected (receipt) | measured at HEAD | verdict |
|---|---|---|---|---|
| R1 | `md5sum tools/tsukuroi-census.sh` | `e32aac98…` | `945c76fc…` | **stale at HEAD** (superseded pin; re-point to the r10 identity — the closeout note's §5 has it right) |
| R2 | `bash tools/tsukuroi-census.sh --selftest` | rc=0, `PASS (74 cases…)` | rc=0, `PASS (80 cases…)` | **moved** (count superseded, C2.2) |
| R3 | `bash tools/tsukuroi-census.sh` | six `PLANE` lines == rollup keys | six lines, SET-MATCH | **PASS** |
| R4 | `echo $?` | 1 | 1 (both runs) | **PASS** |
| R5 | `git status --porcelain` | 0 lines | 0 at baseline; 1 at close (another seat's untracked note) | **PASS (as-of conditions stated)** |
| R6 | `ls /var/lib/pacman/db.lck` | absent | absent | **PASS** |

**A — arc rows** (support for `closeout-r11.md` §1.1/§0.4, re-derived from
committed bytes by this lane — every row `git show <commit>:tools/tsukuroi-census.sh`):

| commit | md5 (8) | `wc -l` | `PLANE` emitters | check-decls |
|---|---|---|---|---|
| `5f90645` (r2, census-v1) | `7a3d3b94` | 743 | **3** | 17 |
| `9bcd162` (r3, census-v2) | `41953ee9` | 976 | **4** | 26 |
| `da95290` (r5) | `e9327046` | 1032 | 4 | 35 |
| `aa136d6` (r7 arms) | `e2c4558a` | 1472 | 4 | 49 |
| `fac745b` (r9b) | `e32aac98` | 2349 | **6** | 74 |
| `af8adf1` (r10, HEAD) | `945c76fc` | 2402 | 6 | 80 |

| # | check | result | verdict |
|---|---|---|---|
| A1 | the note's §1.1 table reproduces | all six rows equal (md5, lines, plane counts, declared case counts); the final row's count is the one executed in C1.3 | **PASS** |
| A2 | §0.4 "no committed revision ever emitted five" | measured committed plane counts 3/4/4/4/6/6 — no five; the ~12-min five-plane intermediate is uncommitted and stays a citation (`SKILL.md:1349`), not re-derivable from history | **PASS** (as stated) |

**O — window observations, and the audit's own scope row:**

| # | observation | evidence | note |
|---|---|---|---|
| O1 | a round-11 sibling artifact landed mid-window | `?? corpus/knowledge/closeout-r11.md` (S11-1): 21:35Z `bdf80c2f…` / 322 L → 21:38Z `817a2867…` / 402 L — **still moving** | shape-only, no verdict binds it (D6) |
| O2 | concurrent seats agree with my captures | `/tmp/w11-s11-1-tsukuroi` (`hash-before.txt` = `945c76fc…`; selftest rc=0 80/80), `/tmp/w11-s11-4-tsukuroi` (`pins.txt` matches §0; live rc=1 six planes); `/tmp/w11-ver-s11` present (process census) | observations, not authority |
| O3 | standing stale wording carried, not repaired | `LOG.md` last line still reads "the 5-plane closeout receipt"; `SCORECARD.md` 22 L / `52218ee5…` (rows 16/21/22 malformed-paren states) — named by the closeout note §3.2 for the record seats | out of this lane's write scope |
| O4 | round-11 sibling artifacts not yet landed | no `HANDOFF.md`; `corpus/lessons/` = 0 files; `corpus/README.md` `98bd0066…` / 20 (stale since r3); `PROVINCE.md` / `SHONEN.md` unchanged | U3 |
| A-own | audit did not edit | `git status --porcelain` at close = only S11-1's untracked note; audited hashes unchanged across my window; my only write = this file | **PASS** |

Aggregate: **both bound claims reproduce at the landed revision; the receipt's
verdict-bearing readings (six planes, rollup, rc, set-match, zero mutation,
cross-probes) reproduce exactly; the receipt's identity/count pins are
superseded by the hardening landed in the same commit — recorded as drift, not
smoothed; the committed arc re-derives 3→4→4→4→6→6 planes with no committed
five.**

## 2. The census receipt re-run — where it stands

- The receipt is a **window capture of the pre-hardening revision**
  (`e32aac98…`, its §2 = `af8adf1~1`), and it says so of itself (§8). The
  round-10 commit then landed S10-2's +53-line hardening **into the same
  commit**, so at HEAD its recipe's first two steps (R1/R2) are superseded
  while its verdict steps (R3–R6) reproduce.
- The round-10 record already carries the supersession on the SKILL side
  (`:1483-1484` post-move line; `:1529` count restatement moved together to
  80), and the round-11 closeout note re-states the identity at HEAD
  (`closeout-r11.md` §0.3/§5). No repair is owed by this lane; the finding is
  the receipt-vs-landed revision split, recorded here for the record seats.
- Timing capture: my selftest wall **24.654 s** vs the receipt's 11.242 s and
  S11-1's 12.041 s — concurrent 32 lanes [inf, as S11-1 also inferred]; a
  capture, not the suite's cost.

## 3. Unknowns (carried, not smoothed)

- **U1** — the dispatch's "2 claims" object is unnamed in my copy; bound as
  stated in the header. A different intended pair re-runs this table with new
  subjects. [unk; probe: the dispatcher's wording]
- **U2** — the receipt's §5 transient selftest temp-dirs: I observed 2
  `/tmp/tsukuroi-r3-2-selftest.*` dirs at ~21:35Z and 0 at 21:38Z; the suite's
  own EXIT trap (`:1574`) removes its dir, and the concurrent seats' runs are
  the likely source — attribution stays [unk] (no lane-tagged prefix).
- **U3** — the round-11 wave is in flight at this close: the runbook, province/
  coverage rows, lesson, README/SCORECARD repairs, LOG append and the round-11
  commit are not landed (measured: no `HANDOFF.md`; `corpus/lessons/` 0 files).
  All verdicts here bind the round-10 landed state; the round-11 products are
  auditable when they settle.
- **U4** — writer attribution rests on scratch namespaces + my process reads,
  not OS-level forensics (as AUD-X9/X10 U2).
- **U5** — the five-plane intermediate's exact lifetime stays the round-9
  addendum's citation (`SKILL.md:1353`); no committed bytes can settle it.

## 4. What this is not

- Not a remediation, not a host-health review: every live value quoted here is
  a capture with a timestamp; the host's readings are the census's, not this
  lane's.
- Not the non-author verification of the round-9 planes or the r10 sweep
  (D13 debt named by the closeout note §3.2; separate products).
- Not the acceptance of the round-11 closeout: the runbook, contracts and
  non-author test are landing after this window (U3).
- Not a commit: this file is the lane's only write; the L1 owns every commit.