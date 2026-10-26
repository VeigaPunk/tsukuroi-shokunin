VERDICT: defect-found

# MistakesSweep — Item M-1 (round 41): candidate mistakes not yet in a `## Mistakes` table

Seat `MistakesSweep` (L2 scout, leaf), 2026-10-26, lane HEAD `71851d636ab1bffaf8fee5016617c88878a666f1`. Read-only on lane
content; wrote this file and `.ufo/waves/round-41/w1/MistakesSweep/` (`sweep-commands.txt`, `repro-mounts-at-tip.txt`,
`offline-counter-demos.txt`). No install, no sudo, no pacman, no host change, no signal sent to a process I did not
start, no subagent. I ran **no counter and no full selftest**; I ran three census invocations on scratch mount tables and
four offline demonstrations against the `e479fdc5` bytes of the C1 counter. Scratch `/fast/scratch/hyaku/tsukuroi-r41/MistakesSweep/` removed.

**Result.** The four pre-freeze rows in the draft `corpus/lessons/round-41.md:69-72` are real; I reproduced the mechanism
of three of them (§2). I found **12 further candidates** (§3): 7 tied to this round's counters/declaration (A1-A7), 5 mined from round-40
wave reports that never reached a table (B1-B5); and I re-measured the **round-40 sweep's still-open candidates** at this tip (§4):
NUL-join, empty override, revision-binding hole and the missing `Scope:` marker are all still open; the K10 count drifts a third time.
**Round-40 sweep candidates were never tabled**: `grep` for their ids outside that report returns 0 hits (`sweep-commands.txt` line 5).

## 0. Sweep commands

Pasted in full in `MistakesSweep/sweep-commands.txt`. The load-bearing ones:

```
cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
grep -n '^## Mistakes' corpus/lessons/round-3{8,9}.md corpus/lessons/round-4{0,1}.md        # tables: r38 :80, r39 :66, r40 :73, r41 :67
(cd .ufo/waves/round-40/w1 && for f in *.md; do echo "$(head -1 $f|cut -c1-40) $f"; done | grep -iE 'falsifies|defect-found')   # 26 reports
git log --format='%h author=%aI committer=%cI' -7
git diff --numstat 0e5805a1 e479fdc5^
for r in e3bc9340 0e5805a1 HEAD; do echo "$r $(git ls-tree -r --name-only $r -- corpus/lessons | wc -l)"; done
ls .ufo/waves/round-41/controls | grep -c controls-c1 ; grep -n controls-c1 SCORECARD.md
grep -rln 'Terminated cp\|survivors 13 of 13\|rc 124' .ufo/waves/round-41 corpus/lessons/round-41.md SCORECARD.md LOG.md
grep -c 'Scope: executed' .ufo/waves/round-41/w1-spec.json
```

## 1. Already recorded (do not re-add)

| Source | Where recorded |
|---|---|
| R40-HOSTCELL-UNANCHORED, R40-ANSWER-KEY, R40-CONTROL-OWN-BASELINE, R40-HEADING-TIMES, R40-TMP-MISROOT | `corpus/lessons/round-40.md:73-79` |
| R41-LABEL-SUFFIX, R41-CAPTURE-FIFO, R41-PIPEFAIL-SIGPIPE, R41-LEXICAL-OVERREACH | `corpus/lessons/round-41.md:69-72` (untracked draft at HEAD) |
| round-40 closure §6.1-6.5 | dispositioned `corpus/lessons/round-41.md:75-89` |
| Round-38/39 routed defects | dispositioned in `round-39.md`/`round-40.md` tables; I found no unmatched closure item |
| Round-40 sweep's 18 candidates (`.ufo/waves/round-40/w1/MistakesSweep.md` §3) | **not recorded anywhere** — see §4 |

## 2. The three named pre-freeze counter bugs — verified, with the gap each row still has

| Row | Reproduced? | Evidence | What the row misses |
|---|---|---|---|
| R41-LABEL-SUFFIX | yes (mechanism) | `offline-counter-demos.txt`: `PASS <label> (exit 0, HEALTHY)` minus `PASS ` ≠ the `FAIL <label>: …` label; after `LABEL_TAIL` (`e479fdc5:tools/score-selftest-mounts-r41.py:71`) they match. Census format `ok "$label (exit $rc, $wverdict)"` (`tools/tsukuroi-census.sh:2183` region, `ok()` at `:2018`). I checked every `check` call's verdict token: only `HEALTHY` 59 / `DEGRADED` 32 / `BLOCKED` 34, so `[A-Z]+` in `LABEL_TAIL` covers all 125 labels; labels are unique (0 duplicates) | evidence is a "pre-freeze base run" that is committed nowhere (A1) |
| R41-CAPTURE-FIFO | yes | `cp` on a FIFO with no writer was still blocked after 3 s (`offline-counter-demos.txt`); the fixture is `census.sh:2999-3000` (`mkfifo "$FX/mounts"`); guard now at counter `:117` (`[ -f "$FX/mounts" ]`) | the row says QUALITY 82 does not cover "instrumentation that reads fixtures" — true — but no QUALITY criterion is proposed; and A1 |
| R41-PIPEFAIL-SIGPIPE | yes | `set -o pipefail; seq 1 400000 \| grep -q 1 && echo hit \|\| …` took the `\|\|` branch, `rc=141` (`offline-counter-demos.txt`). Frozen `capture.sh` (`frozen/hostcap/capture.sh:19,34`) now uses `grep -c … \|\| true` and `sed -n 1,4p` | residual: `capture.sh:33` `p=$(ls -d "$db"/pacman-[0-9]*/ \| head -n1)` under `set -euo pipefail` is the same shape (early-exit consumer). One `pacman-*` dir exists today so `ls` writes one line; **latent, not measured to fail** |

## 3. New candidates

Row format as in the lesson tables: ID | class | evidence | captured-by | fix (shown able to fail). "Status" is mine.

### Tier A — this round's counters, declaration and evidence

**A1. R41-PREFREEZE-EVIDENCE-UNCOMMITTED** — class **landing**. Status: open.
Evidence: the three pre-freeze rows cite runs "survivors 13 of 13", "rc 124, `Terminated cp`", "first capture run exit 1, no `capture-meta.txt`" (`round-41.md:69-71`).
`grep -rln 'Terminated cp\|survivors 13 of 13\|rc 124' .ufo/waves/round-41 corpus/lessons/round-41.md SCORECARD.md LOG.md` → only `corpus/lessons/round-41.md`.
The buggy counter bytes and the failing runs exist in no commit (`e479fdc5` is the fixed form), so no reader can re-run them. The lane's evidence rule (path:line, command + output) is not met by these cells.
Captured-by: QUALITY 77 (revision-cited results are receipts) — written for gate/measurement claims, not for lesson rows. Fix: replace each cell's evidence with a deterministic, re-runnable demonstration (the three in `offline-counter-demos.txt` are one) or mark the cell "observed once, not retained". Shown able to fail: the grep above must find a committed receipt path for each quoted string; today it finds none.

**A2. R41-PARAMS-POLARITY** — class **vacuous** (counter gap). Status: open in the frozen counter; no false credit today.
Evidence: `e479fdc5:tools/score-selftest-mounts-r41.py:182` credits a case when `any(WANT_BLOCK in x for x in args[1:])`; `check()` passes `ABSENT:`-prefixed patterns through the same argument list. Offline demo (`offline-counter-demos.txt`): a case whose only pattern is `ABSENT:detail=mounts:btrfs-without-sysfs`, with a two-btrfs-line table, is credited as P1, P3 and P4. The committed selftest has 0 such cases (`ABSENT:` + `btrfs-without-sysfs` search over `568c397d:tools/tsukuroi-census.sh`: 0 lines), so the 4/4 in `after/c1-after-568c397.jsonl` is not inflated.
Captured-by: QUALITY 88 requires the predicate to check the named parameters; it says nothing on polarity of the wanted pattern. The scribe note `w1/C1ScribeSkill.md` already says "`params` is a shape gate" but names no polarity hole. Fix (next round; counter is frozen): require `not x.startswith('ABSENT:')` and the case's wanted verdict BLOCKED; control = the demo above. Shown able to fail: the demo yields 3 params today and 0 after.

**A3. R41-CONTROLS-C1-PATH** — class **reference-drift**. Status: open; the dispatch prompt repeats it.
Evidence: `SCORECARD.md:2475` says "outputs `controls/controls-c1.jsonl`, `controls/controls-c2.jsonl`". `ls .ufo/waves/round-41/controls | grep -c controls-c1` → 0; `git log --all -- .ufo/waves/round-41/controls/controls-c1.jsonl` → empty. The files that exist are `C1-K1-…jsonl`, `C1-K2-…jsonl`, `C1-K3-…jsonl` (named in the appended paragraph `SCORECARD.md:2483-2492`) plus `controls-c2.jsonl`. The same sentence was written before the runner was split per control (`71851d63`: "controls runner name filter").
Captured-by: R38-ANCHOR-SHIFT's class (a pin that moves after it is written); no gate reads a path named in a SCORECARD declaration. Fix: append a one-line correction under the declaration naming the three C1 files and the before/after receipts. Shown able to fail: the `ls | grep -c` above.

**A4. R41-BASE-IS-NOT-PARENT** (with the third recurrence of R39-K10-CLOSURE-FILE) — class **number-drift / stale-premise**. Status: open, measured.
Evidence: the declaration's base `0e5805a1` is not the parent of the first round-41 commit. `git log --format='%h %p'`: `e479fdc5` has parent `1f5e74aa` (considerthese reflection, João Pedro Veiga), whose parent is `8b7c4132` (round-40 closure, `protocol-shokunin`), whose parent is `0e5805a1`. `git merge-base --is-ancestor 8b7c4132 0e5805a1` fails; `git diff --numstat 0e5805a1 e479fdc5^` → `21 0 considerthese/2026-10-26.md`, `159 0 corpus/lessons/round-40-verifier-spotcheck.md`. The declaration (`SCORECARD.md:2456`) cites that closure file as its own premise, but it is absent at the declared base (`git cat-file -e 0e5805a1:corpus/lessons/round-40-verifier-spotcheck.md` → "exists on disk, but not in '0e5805a1'").
Consequence measured: lessons files 56 at `e3bc9340` and at `0e5805a1`, **57 at HEAD** (58 in the working tree with the untracked `round-41.md`); the SCORECARD depth row says 56 (`:2429`), so K10 of `tools/check-self-assessment.py` (`:617-623`) is red at the round-41 start for the third round running (r39: 52→53 / 54→55; r40: 56→57), before any round-41 change. The foreign commits also sit inside every "base..tip" audit the lesson quotes (`git diff 0e5805a1 9cc9aa77 -- corpus/SOURCES.md` happens to be clean: `10 0`).
Captured-by: QUALITY 83 binds a verdict to declared conjuncts; nothing binds the declared base to the actual parent. Fix: declare the base as the freeze commit's parent, or state "base plus two foreign commits"; count `corpus/lessons/` excluding `*-verifier-spotcheck.md`, or restamp K10 in the declaration commit. Shown able to fail: `git rev-parse e479fdc5^` ≠ declared base; K10 reads 56 vs 57 at HEAD.

**A5. R41-FLAKE-CONFIRMED-TWICE** — class **survivor / attribution** (instrument noise vs kill). Status: open; mitigated in this round's receipts, recorded only as a limit in a seat draft.
Evidence: parsing both C1 receipts, first-run FAIL lines carrying `hostname override not honoured — possible host read` appear on M2, M4, M5, M9, H9 (`after/c1-after-568c397.jsonl`) and M8 (`before/c1-before.jsonl`): 6 of 26 mutant first runs. Every one dropped out of `confirm_labels` (`fail_count` > confirmed labels, e.g. M4 `fail_count 6`, 5 confirmed), so the second-run intersection (counter `:269-272`) did its job here. The rule still counts any baseline label that fails in both runs; under a loaded host the same flaky label can fail twice (`C1ScribeSkill.md` says the same in prose; no table row).
Captured-by: none — QUALITY 88's "exactly one parameter" says nothing on kill attribution noise. Fix: attribute kills only to labels whose FAIL reason is not `hostname override not honoured`, or confirm with a third run; add a control with a label that fails on every run for a load reason. Shown able to fail: not demonstrated — **[INFERENCE]** that a twice-reproduced flake would pass `killed()`; the code path (`:195-198`, `:269-272`) allows it.

**A6. R41-CONTROL-COUPLED-DECOY** — class **vacuous** (control does not isolate a conjunct). Status: open, **[INFERENCE]** on the missing control, measured on the existing ones.
Evidence: `controls/C1-K3-declare-f-prologue-on-candidate.jsonl`: `decoy_pass 0, survivors 13, params 4`; K1 on base: `decoy_pass 0, survivors 13, params 0`. Both self-reader controls move the decoy conjunct and the survivor conjunct together (the prologue's one-line FAIL summary carries no baseline label, so every mutant also reads as a survivor; SCORECARD.md paragraph says so). So neither control shows the decoy conjunct works alone: remove `decoy_pass == 1` and K3 still FAILs on `survivors`. The decoy only matters for a self-reader that prints a baseline label and the baseline case count — which the counter's own attribution rule (`:195-198`, `failed_base_labels`) would count as a kill; that variant is not a committed control.
Captured-by: QUALITY 88 / R40-CONTROL-OWN-BASELINE ("a control violates exactly one parameter, every other conjunct green") — K1/K3 violate two. Fix: a control whose prologue prints `FAIL <real baseline label>` plus the baseline's `(128 cases, …)` summary only when a marker is found; it must FAIL only on `decoy_pass 0`. Shown able to fail: today's K3 fails on two conjuncts.

**A7. R41-NOVELTY-NEVER-MOVES** (recurrence of round-40 C2CritAxis / C2MutCounter / SimplifierCounters) — class **vacuous**. Status: open.
Evidence: `controls/controls-c2.jsonl` nine rows, `novelty_base_hits` = 0 in all nine (K0-K8). The tokens (`e479fdc5:tools/check-package-anatomy-r41.py:115` `NOVELTY = ['extract_db_file', 'missing package metadata', …]`) are hand-picked code identifiers and phrases; the term is a function of the lane base, not of the candidate. Round 40 recorded the same shape: `w1/C2CritAxis.md` (conjunct "candidate-independent"), `w1/C2MutCounter.md` (novelty "cannot be guarded by any control"), `w1/SimplifierCounters.md` §2 (never moves). Credit: this round's counter does check that every cited S-id is on `source:` (`:362` "cited S-id not on source"), which closes round-40 C2MutEntry's "cited S-id never validated" survivors.
Captured-by: QUALITY 88's "a control that violates exactly one" — satisfied for the other conjuncts, not for this one. Fix: a control that restates a sentence the base holds (`pacman-backup-files-r35.md` for PA4/PA6 style rows) and must FAIL on `novelty_base_hits` alone. Shown able to fail: all nine rows read 0 today.

### Tier B — round-40 wave findings never tabled

**B1. R40-NONKERNEL-FIXTURE-COUNTS** (r40 M6; r41 H5) — class **scope**. Status: open, repeats in the round-41 claim.
Evidence: `w1/C1CritEquivalence.md` §2, §6: M6 (`${fst,,}`) is equivalent on every kernel-emittable table, killed only by `/dev/fx0 / BTRFS …`; its recommended notes ("M6 is a spec-level mutant, not an operability mutant"; declaration errata) were never landed: `grep -rn 'spec-level mutant' SCORECARD.md LOG.md SKILL.md corpus/lessons/*.md` → 0 hits. Round 41 repeats it: `w1/C1ScribeSkill.md` measured in a private user namespace that `mount(2)` with a relative target stores an absolute mountpoint, so H5's table (`/dev/vdc1 relative/mnt btrfs …`, `568c397d:tools/tsukuroi-census.sh` case `storage-mounts-mp-relative`) "is a shape the kernel does not print"; H6's UUID source is representable, unobserved for btrfs. The declared claim "H5 … fail it" counts H5's kill as operability evidence.
Captured-by: none. Fix: record the class on the claim: H5 and r40 M6 are parser-contract mutants over an overridable file (`TSUKUROI_PROC_MOUNTS`), not live-host exposures; declare how many of the 13 mutants a kernel-producible table separates. Shown able to fail: the namespace measurement in `C1CritEquivalence/host-kernel.txt` and `C1ScribeSkill.md`.

**B2. R40-COUNTER-EXIT-COLLISION** (r40 C1RevCounter D1, inherited) — class **scope**. Status: open in the r41 counter, **by code reading only**.
Evidence: `w1/C1RevCounter.md` D1: the r40 counter's `except (RevisionError, OSError, UnicodeDecodeError)` omits `subprocess.TimeoutExpired`, so an uncaught exception exits 1, the same code as FAIL, against the docstring's "2 could-not-evaluate". The r41 counter copies the shape: `e479fdc5:tools/score-selftest-mounts-r41.py:210-221` — `git show … timeout=60` inside the `try`, `except (_revision.RevisionError, OSError, UnicodeDecodeError)` at `:219`. The round-41 declaration says it closes the closure's §6.1-§6.2, not this. I did not make `git` hang to reproduce it (D1 was not reproduced live in round 40 either).
Captured-by: none. Fix: catch `subprocess.SubprocessError`; control = a stub `git` that sleeps. Shown able to fail: exit code 1 with a traceback today.

**B3. R40-SEAT-SCOPE-UNDECLARED** (r39 candidate 13, third round) — class **scope / landing**. Status: open; measured this round.
Evidence: `grep -c 'Scope: executed' .ufo/waves/round-41/w1-spec.json` → 0; `grep -c EXEC-AUTHORIZED …` → 0 (74 seats, `w1-dispatch.json` `counts.total 74`); this seat's own prompt asks for a `Report:` trailer and no `Scope:` line. Round 40: 0 as well (`w1/MistakesSweep.md` §3.13). Round-40 `SentScope` F1-F5 shows the seats' scope was held by hand, not by marker.
Captured-by: none. Fix: put the trailer rule and marker in the wave context at spec time; run `check-seat-scope --worktree` at integration. Shown able to fail: the two greps above.

**B4. R40-RECEIPT-HEADERS-RECUR** (r39 candidate 5 / `RoutedProvenance`) — class **attribution**. Status: partly open.
Evidence: round 40's `RoutedProvenance` found 4 of 9 receipt-class files headerless and a sentence that said "each". Round 41, same check over `.ufo/waves/round-41/{before,after,controls}/*`: bound (`tool_sha256` in line 1): `before/c1-before.jsonl`, `before/c2-before.jsonl`, `after/c1-after-568c397.jsonl`, `after/c2-impl-c7c40c0.jsonl`, `after/c2-impl-9cc9aa7.jsonl`; **headerless**: `before/sources-census-start.txt`, `controls/C1-K1…`, `C1-K2…`, `C1-K3…jsonl`, `controls/controls-c2.jsonl`. The declaration paragraph on the controls cites those files as scored "with the frozen counters at the freeze commit"; the controls' own `revision` field is inside each row, but the file header names no tool digest. The declaration does not claim "each written by run-receipt", so this is a class repeat, not a false sentence.
Captured-by: QUALITY 77 (admissibility of a revision-cited gate) — satisfied by the after/before receipts; controls are a different class. Fix: run controls through `tools/run-receipt.py` or state in the declaration which files are bound. Shown able to fail: the `head -1 | grep -o tool_sha256` loop in `sweep-commands.txt`.

**B5. R41-S227-VERSION-UNPINNED** (new at round 41, low) — class **attribution**. Status: open, low.
Evidence: the version `alpm-docs 0.13.0-1` appears in the SOURCES row S227 (`corpus/SOURCES.md:236`), the entry's `verified-at` (`alpm-package-anatomy-r41.md:2`), the lesson (`round-41.md:18`) and the declared item, but the frozen snapshot carries none: `.ufo/waves/round-41/frozen/src/alpm-package.7.raw:2` is `.TH "" "7" ""`; `frozen/src/FETCH.txt` lists the URL only; `grep -rn '0\.13\.0' frozen/` hits only an unrelated `yyjson-0.13.0-1` line in `hostcap/localdb-anatomy.tsv`; `pacman -Q alpm-docs` → not installed. Wave seats later verified it from the page footer and the Arch package JSON (`w1/C2RevPA1b.md:22-24`, `w1/C2ExecLiveSources.md:63`), so it is **true**, but the freeze did not pin it.
Captured-by: none — QUALITY 66 keeps every branch a quoted source states, and no criterion I read requires a version named in a row to sit inside the digested bytes. Fix: append the footer line (or the package-search JSON, with its sha256) to `frozen/src/FETCH.txt`'s evidence by a seat dir copy, or cite `w1/C2RevPA1b.md` in the S227 row's note. Shown able to fail: the grep above finds no version in the frozen bytes.

## 4. Round-40 sweep candidates re-measured at this tip

| Prior id (`round-40/w1/MistakesSweep.md` §3) | State at HEAD | Evidence |
|---|---|---|
| 1 R39-MOUNTS-NUL-JOIN (survivor) | **open, reproduced** | `repro-mounts-at-tip.txt`: NUL-joined table + absent sysfs → `STORAGE … state=HEALTHY filesystems=0 …` plus `line 1911: warning: command substitution: ignored null byte in input`; the NUL→newline twin → `BLOCKED … mounts:btrfs-without-sysfs`. Round 41 declares `probe_storage_arm` unchanged, so by construction not a round-41 kill |
| 2 R39-EMPTY-OVERRIDE-FALLBACK | **open, reproduced** | `tools/tsukuroi-census.sh:462-463` still `${TSUKUROI_BTRFS_SYSFS:-…}` / `${TSUKUROI_PROC_MOUNTS:-…}`; `TSUKUROI_PROC_MOUNTS=` (set, empty) + absent sysfs read the live table (4 btrfs lines) → `BLOCKED … mounts:btrfs-without-sysfs` |
| 3 R39-REVBIND-DISCOVERY-HOLE | **open** | `tools/check-revision-binding.py:261` `if b'"--revision"' in body.stdout:`; the round-41 counters spell `'--revision'` (`argparse` single quotes) — I did not re-run the judge |
| 4 R39-K10-CLOSURE-FILE | **open, third recurrence** | A4 above |
| 13 R39-WAVE-NO-EXEC-MARKER | **open, third round** | B3 above |
| 5, 6, 7 (routed) | closed in round 40 | `round-40.md:73-79`, routed dispositions (`RoutedProvenance`, `RoutedTimestamps`, `RoutedGatesRow`); the round-41 declaration states "the commit time of this section is its authority" and heading carries only a date (`SCORECARD.md:2454`) — consistent |
| 8, 9, 10-12, 14-18 | not re-measured | Not re-derived this round. 8 (`C1DetectHonest` production-path witness) remains outside both round-40 and round-41 claims by construction |

A time-attribution observation, not a mistake yet: the freeze commit `e479fdc5` has author date `2026-10-26T05:30:46-03:00` but committer date `14:08:46-03:00` (`git log --format='%h author=%aI committer=%cI'`); its parent `1f5e74aa` is 09:40 and the closure `8b7c4132` is 05:30:46 — the same second. Any check that reads author time (the R40 `check_heading_dates.py` reads which? I did not open it) would place the freeze before the 16:14:04Z host capture it contains. The declaration names committer time as authority (`SCORECARD.md:2461`), so the lane is consistent; I record the 8 h 38 min gap so the next date check names its clock.

## 5. Proposed rows (paste-ready, recommended for `round-41.md` `## Mistakes` in this order)

1. `R41-PREFREEZE-EVIDENCE-UNCOMMITTED | landing | …` (A1) — also edit the three existing cells.
2. `R41-BASE-IS-NOT-PARENT | number-drift | …` (A4, with K10 third recurrence).
3. `R41-CONTROLS-C1-PATH | reference-drift | …` (A3).
4. `R41-PARAMS-POLARITY | vacuous | …` (A2) and `R41-CONTROL-COUPLED-DECOY | vacuous | …` (A6) — one row each; A6 marked inference.
5. `R41-FLAKE-CONFIRMED-TWICE | survivor | …` (A5, inference on the second half).
6. `R41-NOVELTY-NEVER-MOVES | vacuous | …` (A7) and `R40-NONKERNEL-FIXTURE-COUNTS | scope | …` (B1).
7. B2-B5 as debt lines under "Round-40 routed defects" if no row is wanted.

Each row's evidence cell can use the exact text in §3. **Mark as already recorded:** the four R41 rows (§2), the five R40 rows (§1).

## 6. Not done

- I did not run `score-selftest-mounts-r41.py` or `check-package-anatomy-r41.py` or `tools/check-self-assessment.py` (K10 is derived from `git ls-tree` counts, not from the gate). The offline demos import the counter module and call two functions; no census child ran.
- A5 and A6 rest on reading `killed()` and `failed_base_labels()`; I constructed no variant that is killed by a flake or by a label-echoing self-reader.
- B2 and the `capture.sh:33` residual are code readings, not reproductions.
- Round-40 reports not opened beyond their headers or key sections: `AsmPackageScan`, `C1ExecRerun`, `C1HeldOutGuards` (read via its verdict line), `GateAllRegistry`, `C2ScoutUpstreamDocs`, `ConsiderLineage*`, `RevLessonXref`. The 26 `falsifies`/`defect-found` list is complete; I read roughly the first 3 KB (verdict, headline, method) of 25 of them, and C1RevCounter and C1SentScratch in more depth.
- Prior-sweep candidates 8-12, 14-18 were not re-measured (§4).
- The round-41 wave reports under `w1/` (74 seats) were read only where cited above (`C1ScribeSkill`, `C1ExecPriorCounters`, `C2RevPA1b`, `C2ExecLiveSources`, `AsmCollision`, `C2RevSourcesRows`, `C2ScribeGate`); I have not judged whether they carry further defects.
