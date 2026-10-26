VERDICT: defect-found

# G-1 — No-harm: the lane's standing gates at `f50c28d8` (round 42, wave 1)

Seat `GateAllRegistry`. Item: run every `tools/check-*.py` that takes `--revision` at the dispatch tip
(`f50c28d83e1832ecd7eba765caace531f45d6b27`) from a scratch clone, report exit code and last line per gate,
and say for each nonzero exit whether it is pre-existing at the base `c8efaa3f120834541f8de1e5e0367e8d1593bae6`.

**Headline.** 37 gates, 26 exit 0. Of the 11 nonzero exits, **3 are new regressions introduced by round-42 commits**
(`check-adjacency-anchors` 0→1, `check-registry-coverage` 0→1, `check-self-assessment` 1→1 with mismatches 1→4),
5 are pre-existing at the base with byte-identical findings, and 3 are bare-CLI usage modes rather than measurements
(one of them, the C2 counter, is additionally red *by design* until wave 2). All three regressions are bookkeeping
(SKILL.md registry rows, two SCORECARD axis counts, one anchor line number); none touches the C1 census change or the
C2 entry. A correction set validated in a fixture clone (`7b66cd10`) turns exactly those three gates green and changes
no other gate (section "Validated correction set"). I did not apply it — the L1 integrates.

## Method (every read through a scratch clone; nothing written to the lane)

- `git clone -q --shared /home/vgpnk/Projects/shokunin/tsukuroi-shokunin /fast/scratch/hyaku/tsukuroi-r42/GateAllRegistry/lane`;
  `git -C <clone> remote remove origin`; `git rev-parse --show-toplevel` printed the clone; `git cat-file -t f50c28d8…`
  and `… c8efaa3f…` both printed `commit`. Clone HEAD `87c4f7c6`.
- `ls tools/check-*.py` → 37 files; `grep -q -- --revision` on each → all 37 accept `--revision`; none skipped.
- Per gate: `python3 <clone>/tools/<gate> --revision f50c28d8…` with cwd and `TMPDIR` under
  `/fast/scratch/hyaku/tsukuroi-r42/GateAllRegistry/`, serial (one process at a time). One full sweep = 28.5 s;
  a **second full sweep reproduced every exit code** (`rc differences: none`), so no result below is a one-off.
- Every nonzero exit re-run at `c8efaa3f…` with the same tool bytes (`--revision c8efaa3f…`).
- `check-self-assessment.py` exactly as the item asks: `--revision f50c28d8… --scratch /fast/scratch/hyaku/tsukuroi-r42/GateAllRegistry/sa`
  (base: `--scratch …/sa-base`).
- `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi`.
- Receipts in `.ufo/waves/round-42/w1/GateAllRegistry/`: `gates-tip/` (37 full outputs), `gates-base/` (the 11 nonzero at
  base), `gates-variant/` (37 at the corrected fixture), `attribution/` (freeze and C1-impl revisions), `self-assessment/`,
  `sources-census-validate.txt`, `tip-status.tsv`, `runs.txt` (exact commands). 334,288 bytes total.

## Result — 37 gates at `f50c28d8` (base column: only the nonzero exits were run there, as the item requires)

| gate | tip exit | base exit | tip status / last line |
|---|---|---|---|
| `tools/check-adjacency-anchors.py` | 1 | 0 | `FAIL`, `INBOUND-CLASSIFICATION-WRONG` |
| `tools/check-adjacency-overlap.py` | 0 | not run | PASS |
| `tools/check-appended-notices.py` | 0 | not run | PASS |
| `tools/check-boot-chain.py` | 0 | not run | PASS |
| `tools/check-boot-writers.py` | 0 | not run | PASS |
| `tools/check-boundary-contract.py` | 0 | not run | PASS |
| `tools/check-btrfs-repair-r31.py` | 0 | not run | `{"predicate": "new_sourced", "new_sourced": 8, "of": 8}` (last line) |
| `tools/check-btrfs-space-r30.py` | 0 | not run | `{"verified": 10, "of": 10}` (last line) |
| `tools/check-edit-contract.py` | 1 | 1 | `FAIL`, `EDIT-PROSE` |
| `tools/check-exec-environment-r40.py` | 0 | not run | `"result": "PASS", "exit": 0` |
| `tools/check-freshness-r17.py` | 0 | not run | PASS |
| `tools/check-hook-order-r38.py` | 0 | not run | `"result": "PASS", "exit": 0` |
| `tools/check-journalctl-v262-corrections.py` | 0 | not run | PASS |
| `tools/check-kernel-taint.py` | 0 | not run | PASS |
| `tools/check-knowledge-header.py` | 0 | not run | PASS |
| `tools/check-locator-clarification.py` | 0 | not run | PASS |
| `tools/check-memory-pressure.py` | 0 | not run | PASS |
| `tools/check-owed-statements-r29.py` | 0 | not run | `{"items": 12, "marked": 12}` (last line) |
| `tools/check-package-anatomy-r41.py` | 0 | not run | `"result": "PASS", "exit": 0` |
| `tools/check-path-reconciliation.py` | 0 | not run | PASS |
| `tools/check-pause-gate.py` | 1 | 1 | `FAIL`, `GATE-PREMISE` P3 |
| `tools/check-recheck-commands.py` | 0 | not run | PASS |
| `tools/check-registry-coverage.py` | 1 | 0 | `FAIL`, 2 × `REGISTRY-ROW-MISSING` |
| `tools/check-report-receipts.py` | 2 | 2 | usage error on stderr (needs `--report/--lane/--revision` or `--selftest`) |
| `tools/check-review-cohort.py` | 0 | not run | PASS |
| `tools/check-review-snapshots.py` | 1 | 1 | `FAIL`, 4 findings |
| `tools/check-revision-binding.py` | 2 | 2 | `CANNOT_EVALUATE` (`invalid arguments`; needs `--tools-revision`) |
| `tools/check-root-dac-correction.py` | 0 | not run | PASS |
| `tools/check-scrub-record-r42.py` | 1 | 1 | `"verdict": "FAIL"` (rows 5, verdicts_ok 0 — wave-2 seats unbound) |
| `tools/check-seat-bindings.py` | 1 | 1 | `FAIL`, 41 findings |
| `tools/check-seat-scope.py` | 2 | 2 | `CANNOT_EVALUATE` (`E-CLI`; needs `--wave`) |
| `tools/check-section-citations.py` | 0 | not run | PASS |
| `tools/check-selector-contract.py` | 0 | not run | PASS |
| `tools/check-self-assessment.py` | 1 | 1 | `FAIL`, `mismatches: 4` |
| `tools/check-source-scope-correction.py` | 0 | not run | PASS |
| `tools/check-storage-health.py` | 0 | not run | PASS |
| `tools/check-transaction-order-r39.py` | 0 | not run | `"result": "PASS", "exit": 0` |

## The eleven nonzero exits, resolved one by one

### A. New at the tip — three round-42 regressions

**(1) `check-adjacency-anchors.py`: 0 at base → 1 at tip.**
Finding: `INBOUND-CLASSIFICATION-WRONG` at `corpus/knowledge/adjacency-anchors-r19.json:inbound[108]` —
"classification DRIFTED is inconsistent: found_line is not an occurrence of evidence_quote".
The record is `IN-109` (`target_path` `tools/tsukuroi-census.sh`, `found_line` 2452). The quote
`check 'degraded: kernel ring class counts are evidence (D14/D15)' 1 DEGRADED` sits on line **2452 at the base and 2465
at the tip** (census 3177 → 3202 lines). Attributed to `44766208` ("round-42: C1 implementation … 130 cases"):
`git log --oneline c8efaa3f..f50c28d8 -- tools/tsukuroi-census.sh` → `44766208`; running the same gate at `44766208`
already returns rc 1, at the freeze commit `a84fc9de` it returns rc 0/PASS (receipts `attribution/c1impl-…`, `freeze-…`).
`IN-109` is the **only** inbound record that targets the census (checked every record's `target_path`), so the fix is one
field, not a sweep: `"found_line": 2452` → `2465` plus a note sentence naming round 42 and this seat.

**(2) `check-registry-coverage.py`: 0 at base → 1 at tip.**
Two findings `REGISTRY-ROW-MISSING`: `tools/check-scrub-record-r42.py` and `tools/score-size-invariance-r42.py`
("no operative row names this regular tools/ file"); counts `tools_total 66`, `registered 64`, `missing 2`
(base: 64/64, PASS). Both tools landed in `a84fc9de`, and `SKILL.md` is untouched in `c8efaa3f..f50c28d8`
(`git log --oneline c8efaa3f..f50c28d8 -- SKILL.md` → empty). The operative table is the highest-numbered one —
`## Gate and probe registry — round36 superseding current rows` at `SKILL.md:3050`, header at `:3056`, 64 rows ending
`| package-anatomy-r41 | gate | …` at `:3121` — and rows for later-round tools were added in place (e.g. `package-anatomy-r41`
itself), so the fix is two inserted rows, not a new table.

**(3) `check-self-assessment.py`: 1 at base → 1 at tip, mismatches 1 → 4.**
- `K07` mismatch **new at `f50c28d8`**: depth row states "62 notes"; `corpus/knowledge` holds **63** `.md` files
  (`btrfs-scrub-record-r42.md` landed in `f50c28d8`). Except at `44766208`/`a84fc9de` K07 still matches.
- `K13` mismatch **new at `44766208`**: operability row states "PASS (128 cases, 128 passed, 0 failed)"; the gate's own run
  of the census selftest reports `130` cases (`R42-C1` added two cases).
- `K17` mismatch **new at `44766208`**: the `host-census-gate` capability row states 128 cases; same 130.
- `K10` mismatch **pre-existing at the base**: depth row states "58 files" for `corpus/lessons`; the tree holds **59**
  (base c8efaa3f already reports `mismatches 1`).
At the freeze commit `a84fc9de` the gate reports mismatches 1 (K10 only); at `44766208`, 3 (K10, K13, K17); at the tip, 4.
Proposed exact text (SCORECARD.md, `## Axes — current self-assessment (round 41 final measured surface)` and the capability
table below it). Note this is the one place where the fix is **not** a three-token edit: see the validated set below —
adding the two registry rows also moves the depth row's own `SKILL.md` counts.

### B. Pre-existing at the base, findings identical (5)

| gate | tip | base | finding |
|---|---|---|---|
| `check-edit-contract.py` | 1 | 1 | `EDIT-PROSE` at `corpus/knowledge/structured-edit-r23.md` (1 finding at both revisions) |
| `check-pause-gate.py` | 1 | 1 | `GATE-PREMISE` at `P3:verdict-unverified-not-counted` (1 at both) |
| `check-review-snapshots.py` | 1 | 1 | `REVIEW-REPORT-MISSING` (site `ScribeDecision`) + 3 × `REVIEW-SCOPE-MISMATCH` (4 at both) |
| `check-seat-bindings.py` | 1 | 1 | 41 findings at both: `SCOPE-TOOL-UNKNOWN` 16, `SCOPE-PATH-DENIED` 23, `SCOPE-EXEC-DENIED` 2 (round-22 manifest oracle fixtures) |
| `check-self-assessment.py` | 1 | 1 | see A(3); the residue K10 is pre-existing, the other three are new |

Round-42 changes none of these: same ids, same counts, same sites at `c8efaa3f` and at `f50c28d8`.

### C. Bare CLI is a usage mode, not a measurement (3)

- `check-revision-binding.py`, bare `--revision` → exit 2, `CANNOT_EVALUATE`, finding `invalid arguments`, `branch_tip: null`.
  The documented invocation is `--tools-revision <REV>`; with `--tools-revision f50c28d8…` it exits **0**
  (`bound_tools 9`, `all_bound_tools 17`, `all_consistent_tools 16` of `all_total 19`), and at the base revision it also
  exits 0 with the same numbers. So: exit 2 here is an argument-shape artifact, identical at the base.
- `check-seat-scope.py`, bare → exit 2 `E-CLI`; with `--wave .ufo/waves/round-42 --revision f50c28d8…` → exit 2
  `E-SEAT-SOURCE-MISSING: 1`. That is correct at this revision: no seat source is committed at `f50c28d8`
  (`git ls-tree -r f50c28d8 -- .ufo/waves/round-42` lists `before/`, `controls/`, `frozen/`, `impl/` only); the w1 spec and
  dispatch land later, in `87c4f7c6`. Same at the base (no round-42 wave at all). Not evaluable at the tip — say so, do not
  read it as a pass.
- `check-report-receipts.py`, bare → exit 2 with the usage line on stderr
  (`--report PATH --lane REPO --revision REV or --selftest is required`). `--selftest` exits **0** (`cases 2, passed 2`).
  Report mode is not applicable at the tip: no round-42 report file is committed yet.

### D. Expected nonzero by design at wave 1 (1)

`check-scrub-record-r42.py` (the frozen C2 counter) exits 1 at the tip **and** at the base, for different reasons:
- tip: `rows 5`, `quotes_ok 5`, `novelty_ok 5`, `host_ok 5`, `capture_ok true`, but `verdicts_ok 0` — every `SC<n>.verdicts`
  is `{"crit": null, "residual": null, "rev": null}`. The predicate requires `verdicts_ok == 5`, and the counter's verdict
  conjunct counts only wave-2 seats `C2RevSC<n>`/`C2CritSC<n>` bound through `w2-dispatch.json` + `w2-results.json`, which do
  not exist in wave 1;
- base: `rows 0`, every SC row `present: false` (entry did not exist yet).
So a nonzero here at w1 is the designed state, not a defect and not a regression. Using this counter as a "tip gate must be
green" signal during wave 1 would be a false red.

## Validated correction set (fixture clone `7b66cd10`; nothing applied to the lane)

Fixture: `git clone -q --shared <clone> /fast/scratch/hyaku/tsukuroi-r42/GateAllRegistry/fx`, `remote remove origin`,
`git checkout -q --detach f50c28d8…`, toplevel asserted equal to the fixture dir, committed with
`-c user.name=fixture -c user.email=fixture@invalid`, then `git branch -f master <variant>` so the revision-binding
(`E-REVISION-NOT-LANDED`) accepts it. Contents, in four parts:

1. `corpus/knowledge/adjacency-anchors-r19.json`, record `IN-109`: `"found_line": 2452` → `"found_line": 2465`
   (the token occurs exactly once in the file), plus a note trailing round 39's: *"Round 42: the C1 census change (44766208)
   moved it from line 2452 to 2465 (found_line updated; wave-1 GateAllRegistry)."*
2. `SKILL.md`: two rows appended to the operative table after `:3121` (exact text validated by the gate, not paraphrase):

```
| scrub-record-r42 | gate | `python3 tools/check-scrub-record-r42.py --revision <REV> [--lane <repo>]` | 0 SC1-SC5 present with quotes inside the frozen source windows, novelty verified, at least three host values, one mined source row and five wave-2 seat verdicts bound through `w2-dispatch.json` and `w2-results.json`;1 one or more rows unverified;2 could-not-evaluate on a harness error | none: no self-test mode; the frozen SC1-SC5 row set and the wave-2 verdict binding are the measurement | R42 C2 frozen predicate `rows == 5 and quotes_ok == 5 and novelty_ok == 5 and host_ok >= 3 and sources_ok == 1 and verdicts_ok == 5 and novelty_base_hits == 0`; pinned btrfs-progs v7.1 `cmds/scrub.c` and `CHANGES` snapshots listed in `.ufo/waves/round-42/frozen/src/SHA256SUMS` | committed Git reads only | tsukuroi |
| size-invariance-r42 | gate | `python3 tools/score-size-invariance-r42.py --revision <REV> --scratch <DIR> [--lane <repo>]` | 0 predicate `cases == 10 and invariant == 10 and ns_invariant == 3 and selftest_pass == 1 and default_equal == 1` over ten P1-P6 and U1-U4 size twins and three `unshare -rm` production-path legs;1 any leg non-invariant or the census selftest not PASS;2 could-not-evaluate | none: no self-test mode; the ten fixture twins and the three namespace legs are the measurement | R42 C1 frozen counter sha256 `c511104a8e69fe6a90bb849847fe9c4635642f70ff0cb01fb62c38c098553e03`; 1 MiB verdict-neutral padding; fixtures built from the base census at `c8efaa3f` | private fixture copies under `--scratch`; `unshare -rm` namespace only for the N1/N3/N6 legs | tsukuroi |
```

3. `SCORECARD.md:2520` (operability axis) and `:2530` (`host-census-gate` capability row):
   `PASS (128 cases, 128 passed, 0 failed)` → `PASS (130 cases, 130 passed, 0 failed)`. The third occurrence of that
   string (`:2501`, the round-41 claim row's historical after-value) must **not** change.
4. `SCORECARD.md:2518` (depth axis): `62 notes` → `63 notes`; `` `corpus/lessons/` 58 files `` → `59 files`;
   and — this is what the first fixture attempt caught — `` `SKILL.md` 3847 `wc -l` / 956 table lines `` →
   `3849` / `958`, because part 2 adds two lines to `SKILL.md`.

Scored results. First fixture commit `1245f3f1` (parts 1-3 plus 62→63 and 58→59, no SKILL.md counts):
`check-registry-coverage` **PASS**, `check-adjacency-anchors` **PASS**, `check-self-assessment` **FAIL** on `K08`
(3847 stated / 3849 observed) and `K09` (956 / 958) — i.e. the correction set is self-consistent only with part 4.
Amended variant `7b66cd106db59c811c6fd814b08124423302f7e7` with part 4:
`check-registry-coverage` exit 0 PASS, `check-adjacency-anchors` exit 0 PASS, `check-self-assessment` exit 0 **0 mismatches**.
A full 37-gate sweep at `7b66cd10` changes **only** those three exits (1→0, 1→0, 1→0); the other 34 keep their tip exit
codes, so the set is minimal and introduces no new failure.

## `sources-census.sh validate` (fleet root, read-only)

Exit **0**; last line `tsukuroi	ok	/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md`.
40 `W04 duplicate url … across scopes` warnings, which is the recorded round-41 end state (`SCORECARD.md:2505`: "census exit 0,
W04 39 → 40"); `corpus/SOURCES.md` grew 236 → 239 rows (`c8efaa3f` → `f50c28d8`, `S237`-`S239`) and **none** of the 40 W04
lines names S237/S238/S239, so the three new rows added no new duplicate.

## What I did not do

- Did not apply the correction set, edit any lane file, or commit/stash/checkout/reset/push in the lane; the variant lives
  only in `/fast/scratch/…/fx` (master was moved there, never in the lane).
- Did not run `check-report-receipts.py` in report mode (no round-42 report is committed at the tip) or
  `check-seat-scope.py` at a revision that carries the w1 spec — neither is a tip measurement.
- Did not run the census selftest myself; the 130-case figure quoted for K13/K17 is the self-assessment gate's own
  subprocess output for that check, not an independent rerun.
- Did not run `score-size-invariance-r42.py` or `check-scrub-record-r42.py` beyond the mandated `--revision` sweep; no
  counter was run twice concurrently, no census selftest was run separately.
- No tool install, no `pacman`, no sudo, no service/mount/sysfs/boot change, no `btrfs scrub` or `device stats -z`; the
  only host contact is the read-only probing the gates perform themselves.
- Scratch `/fast/scratch/hyaku/tsukuroi-r42/GateAllRegistry/` is removed after the receipts were copied (see the seat dir).

## Risks

1. The lane's "standing gates at the dispatch tip" reading is **red on three gates** until the L1 integrates the set above;
   two of the three regressions are pure bookkeeping, so a reader who treats "gates green" as evidence about C1/C2 would
   mis-attribute them to the C1 census change or the C2 entry.
2. The registry table is the only guard that a new `tools/` file is documented: every future tool must add its row in the
   same commit, or `check-registry-coverage` goes red again (this is exactly what happened at `a84fc9de`).
3. `check-scrub-record-r42` cannot be green before wave 2 binds its five verdict seats; wave-2 dispatch must keep the two
   seat families `C2RevSC<n>`/`C2CritSC<n>` and the `w2-dispatch.json`/`w2-results.json` names the counter reads.
4. `check-adjacency-anchors` validates only that `found_line` holds the quote, so a line shift that leaves the quote on a
   different-but-containing line would pass silently; the round-42 shift happened to miss, which is why it was caught.
