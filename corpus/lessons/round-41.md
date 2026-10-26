# Round 41 — lesson (tsukuroi, hyaku run 9)

author: tsukuroi L1 (`TsukuroiR41`), 2026-10-26. Measured base `0e5805a1f149bd2ed9fe0db2e0a832afb034a835` (round-40 tip; the
lane tip at round start was `8b7c4132`, which adds only the round-40 spot-check lesson — see R41-BASE-MISREAD). Claims, controls and
outcome: `SCORECARD.md` sections "Round 41 — declaration" and "Round 41 — measured outcome". Wave: one v2 wave `w1`
of 74 seats plus a residual call of 6 reviewer seats (`.ufo/waves/round-41/w1-spec.json`, `w1-dispatch.json`,
`residual-dispatch.json`; reports in `.ufo/waves/round-41/w1/` and `residual/`; the orchestrator's results files beside them). Seats are the lane, not
outside reviewers (LEARNING.md); this round's non-author closure is pending.

The round-40 Gate's "Spot-check" item is answered by `corpus/lessons/round-40-verifier-spotcheck.md`: its §4 re-opened
S219-S222, S224-S226 and the sampled staged reject and agreed with every one; its §6 routed the five debts dispositioned
below.

## Gate

### New SOURCES rows (all opened 2026-10-26 by this round; each quote located with `grep -n` in the pinned snapshot)

| Row | URL (access 2026-10-26) | Located quote (≤25 words) | Location |
|---|---|---|---|
| S227 | https://man.archlinux.org/man/alpm-package.7 (raw rendering `alpm-package.7.raw`, alpm-docs 0.13.0-1) | "The following files must be present at the root of an ALPM based package:" | `frozen/src/alpm-package.7.raw:100` |
| S228 | https://gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/lib/libalpm/be_package.c | `_("missing package metadata in %s\n"), pkgfile);` | `frozen/src/be_package.c:653` |
| S229 | https://gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/scripts/makepkg.sh.in | "database files are placed at the beginning of the package regardless of" | `frozen/src/makepkg.sh.in:560` |
| S230 | https://gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/lib/libalpm/add.c | "reserve all files starting with '.' for future possibilities" | `frozen/src/add.c:180` |
| S231 | https://gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/src/pacman/check.c | `printf(_("%s: no mtree file\n"), pkgname);` | `frozen/src/check.c:318` |
| S232 | https://gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/doc/PKGBUILD.5.asciidoc | "This function is run inside `$startdir`." | `frozen/src/PKGBUILD.5.asciidoc:357` |
| S233 | https://gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/lib/libalpm/version.c | "different from RPM- always assume 0 epoch" | `frozen/src/version.c:61` |
| S234 | https://gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/lib/libalpm/be_local.c | `archive_read_support_format_mtree(mtree);` | `frozen/src/be_local.c:268` |
| S235 | https://gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/src/pacman/query.c | `ret = check_pkg_full(pkg);` | `frozen/src/query.c:321` |
| S236 | own-work capture `.ufo/waves/round-41/frozen/hostcap/` (`capture.sh`, run 2026-10-26T16:14:04Z) | header `entry desc files mtree install changelog dotfiles mtree_gzip mtree_lists_self`; `vercmp 1.0 1.0-5 = 0` | `frozen/hostcap/localdb-anatomy.tsv:1`, `frozen/hostcap/vercmp.txt:4` |

Snapshot digests: `.ufo/waves/round-41/frozen/src/SHA256SUMS`; fetch log `FETCH.txt`. Rows touched old→new: none (no
`status`, `recheck` or `used-by` cell of an older row changed: `git diff 0e5805a1 9cc9aa77 -- corpus/SOURCES.md`
adds ten lines and removes none). S230 shares its URL with S213 (commit-order scope) under a distinct scope (database
members); the census reports it as W04.

### Assimilation (theme: alpm package anatomy, `merge/tsukuroi/`) — staged entry re-grounded

Staged entry `knowledge/corpus/knowledge/alpm-package-anatomy-r26.md` (sha256 `3fa1b8098ee3398c4587f012bd84455f893a66d2a7ee00647c31279a0172d1a7`,
read-only), rejected in round 38 with flip "a revision that quotes PKGBUILD(5) for each function's working directory
and passes a QUALITY check" (`corpus/lessons/round-38.md:49`).

- **Admit, re-grounded:** the root-member statement (staged `:13-16` → PA1 on S227, the alpm-package(7) raw rendering at
  `:100-120`); `epoch` forcing a newer view (staged `:45-47` → PA8 on S232 `:67-74` and S233); the function list
  (staged `:52` → PA7, every function's directory quoted from `PKGBUILD.5.asciidoc:345-377`). No staged sentence, row
  or id is copied; each admitted proposition is lane text on rows opened this round.
- **Reject:** staged `:53-54` "`package()` runs inside `$pkgdir` under `fakeroot` and the others run inside `$srcdir`"
  — contradicted by `PKGBUILD.5.asciidoc:351` ("This function is run inside `$srcdir`." for `package()`) and `:357`
  (`verify()` runs inside `$startdir`). Reason class: false statement. Flip: none (the pinned source says otherwise).
- **Reject:** the staged ground pointer `:6` "`corpus/README.md:38-42`" as the frontier it extends — the lane README
  holds no packaging frontier there (round-38 F3). Flip: a README row that names it.
- **Not taken:** the `backup` sentence (staged `:48-49`; held by `pacman-backup-files-r35.md`) and the `install`
  directive sentence (staged `:50-51`; build-side, outside the province's read-only Core).
- Round-38 flip condition: met by PA7 (each function's working directory quoted) plus the entry's `## QUALITY check`.

Collision check (scratch, `.ufo/waves/round-41/assimilation/`): registry ids at base 226 (`reg-ids-base`), staged ids 147
(`staged-ids`), collisions at base 27 (S200-S226, `collisions-base`); every colliding id names a different document in
the lane. Guard proof: a scratch registry with an indented `  | S227 |` row collides under the 0-3-space pattern (1) and
not under the column-zero pattern (0) (`assimilation/guard-proof/`). Renumber map by document (no staged row appended):
staged S215 alpm-package(7) (`https://man.archlinux.org/man/alpm-package.7`) → lane S227 (same document, re-opened, lane
row); staged S217 PKGBUILD(5) man page (`https://man.archlinux.org/man/PKGBUILD.5`) → lane S232 (same text pinned at its
asciidoc source at 54d9411, a different URL). Quarantine slice: 12 rows (`assimilation/quarantine-slice`), unchanged
from round 40; none names alpm-package(7) or PKGBUILD(5).

### Spot-check

Non-author closure pending. Candidates for it: one admit (S232 / PA7, or S230 / PA4 with the host column) and the
staged reject `:53-54`.

## Mistakes

| ID | Class | Evidence | Captured-by | Fix |
|---|---|---|---|---|
| R41-LABEL-SUFFIX | vacuous | First C1 counter draft compared stderr `FAIL <label>: …` with stdout `PASS <label> (exit N, VERDICT)` lines, so no mutant could count as killed and the params capture matched no label (pre-freeze base run, survivors 13 of 13 although nine failed the selftest; observed once, not retained — re-runnable demonstration `.ufo/waves/round-41/w1/MistakesSweep/offline-counter-demos.txt`) | none — no criterion asks a counter to be scored on a known-killed mutant before freezing | `LABEL_TAIL` normalisation; the pre-freeze candidate run then showed 13 kills (`score-selftest-mounts-r41.py` at `e479fdc5`); a known-killed mutant is the able-to-fail case |
| R41-CAPTURE-FIFO | survivor | The capture line `cp -- "$FX/mounts" …` blocked on the FIFO fixture `storage-mounts-fifo`, timing the capture run out (pre-freeze debug run, rc 124, `Terminated cp`; observed once, not retained; an orphaned `cp` of that run stayed blocked 2 h 10 min until the L1 killed it after `w1/SentScope.md` S3) | QUALITY 82 (fixture views) does not cover instrumentation that reads fixtures | `[ -f "$FX/mounts" ]` guard in the injected line |
| R41-PIPEFAIL-SIGPIPE | vacuous | `capture.sh` under `set -o pipefail` used `zcat … \| grep -q` and `zcat … \| head`: grep/head exit early, zcat gets SIGPIPE, the pipeline fails, so a match reads as absent and the script aborted (first capture run exit 1, no `capture-meta.txt`; observed once, not retained) | none | `grep -c … \|\| true` and `sed -n 1,4p`; shown able to fail by `w1/MistakeFixAbleToFail.md` §1 (red 5/5 status 141, green 5/5), which also found a live instance in the census (next row) |
| R41-LEXICAL-OVERREACH | scope | A vocabulary conjunct (rule words must occur in the pinned sources) drafted for the C2 counter refused the author's own paraphrase (`runs`, `absent`, `outranks` …, 40 distinct words over the 8 rows of the first draft) while a filler copied from source words would pass it | QUALITY 81 (lexical predicates are format checks) | removed before the freeze; the per-row verdict files carry the read |
| R41-CENSUS-PIPEFAIL-692 | survivor | `tools/tsukuroi-census.sh:692` tests the merged `pacman -Qkk` sample output with `printf … \| grep -q '^error:'`; on a large output under pipefail the error line is consumed but the test reads false, so an unreadable probe is reported `DEGRADED` instead of `BLOCKED` (`w1/MistakeFixAbleToFail.md` §2: correct at 84-19,430 B, wrong from 78,846 B; `MistakeFixAbleToFail/live-defect-692.txt`) | none (the census selftest has no large-output case) | routed to round 42 (planned row): a selftest case with a large error-bearing sample, red before the fix |
| R41-GUARD-BYPASS | vacuous | Both round-41 guards were beaten by reading the guard: a here-document-stripping self-reader plus one shared fixture line passed the full C1 predicate (`w1/C1CritDecoy.md`), and a relation-literal writer with planted all-holds verdict files passed the full C2 predicate (`w1/C2CritControl.md`, `w1/C2CritXFalse.md`); the pre-data controls held no member of either family | QUALITY 88 (one-parameter controls) does not require the guard's own mirror evasion | QUALITY 89; round-42 amendment binds verdict files to the dispatch record and C1 kills to case-owned fixtures |
| R41-BASE-MISREAD | reference-drift | The declaration, both counters (`BASE` in `check-package-anatomy-r41.py`) and the receipts name `0e5805a1` (round-40 tip) as base; the lane tip at round start was `8b7c4132` (`jj-lane.sh state` local=`8b7c4132`), and the operator's `1f5e74aa` was rebased under the freeze commit by the helper. Effect bounded: `git diff --stat 0e5805a1 1f5e74aa -- tools corpus/SOURCES.md corpus/knowledge SKILL.md` is empty and the C2 novelty tokens have 0 hits at `8b7c4132` too | none | name the base from `jj-lane.sh state` `local=` at round start, recorded in the declaration |
| R41-TMP-MISROOT-REPEAT | landing | A wave seat ran `tools/check-self-assessment.py` at the dispatch tip, where the round-40 fix was still uncommitted, and a 300 MB lane archive was built under `/tmp` (`w1/SentScope.md` S1) | R40-TMP-MISROOT (routed) | the `--scratch` fix lands with this round's integration commit; `w1/RoutedSelfAssessScratch.md` shows it able to fail (old tool: census child under `/tmp`; new: none) |

## Round-40 routed defects — round-41 disposition

1. R40-ANSWER-KEY (both counters): C1 — `tools/score-selftest-mounts-r41.py` decoy (every mutant text in a dead
   here-document), kill attribution confirmed twice, controls K1/K3 (declare -f prologue on base and on candidate); the
   held-out H5/H6/H9 are frozen mutants. C2 — `tools/check-package-anatomy-r41.py` source windows, proposition relations
   and per-row verdict files; controls K1 (the round-40 token writer) and K3/K4 (X-false). Recorded bypasses:
   a self-reader that strips here-documents (C1), a relation-literal writer (C2, control K2).
2. `first_fails` empty and scratch after Ctrl-C: the round-41 counter reads stderr FAIL lines and removes its scratch on
   SIGINT/SIGTERM (`_cleanup`); the round-40 counter is frozen history and unchanged.
3. R40-TMP-MISROOT: `tools/check-self-assessment.py --scratch` (archive and census child TMPDIR under it).
4. S220 anchor drift: see the appended note in this lesson's Gate (wave item RoutedS220Anchor).
5. W04 delta: recorded in the report's Sources & frontier line.

## Sources census

Start: `tsukuroi ok`, exit 0, 39 W04 (`.ufo/waves/round-41/before/sources-census-start.txt`).

## considerthese — counter-attack scoreboard (`considerthese/2026-10-26.md`, proposal "Counter-attack scoreboard")

The one still-unimplemented proposal mined this round: "For each frozen counter, track how many attack arms the wave
fielded, how many survived, and which class beat it." Grounded on the wave reports it points at, not on the reflection:
`SKILL.md` "Counter-attack scoreboard — rounds 40-41" counts the arms of the round-40 and round-41 counters from the named
reports. Its reading — each round's guard is beaten by reading that guard — is the evidence behind QUALITY 89. The
2026-10-25 proposal "Evidence-weight watch" was measured by seat ConsiderWeight (`w1/ConsiderWeight.md`) as wave evidence
only; it is not this round's considerthese item.

## Sources census

End: `tsukuroi ok`, exit 0, 40 W04 (`.ufo/waves/round-41/after/sources-census-final.txt`); the new W04 is S230 (same add.c
URL as S213, distinct scope: database members vs commit order).
