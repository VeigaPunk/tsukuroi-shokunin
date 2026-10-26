# Round 41 — verifier spot-check (non-author closure)

author: hyaku closure (non-author integrator, @m_opus)

Lane-round: tsukuroi round 41. Lane tip before the round `8b7c4132680103cd7ac1590ef668f42259f9cd6c`, after
`6cc927dfcfaa66ca460eabe097fcce7ed5e23da0` (branch `master`). The lane measured against base
`0e5805a1f149bd2ed9fe0db2e0a832afb034a835` (round-40 tip). Report: `.ufo/reports/round-41/tsukuroi.md` (fleet repo).
Dispatched prompt: `.ufo/prompts/tsukuroi-round-41.md`. Closed 2026-10-26. This file is written by the closure, not
by the lane; the lane must not edit it. No re-check seats were dispatched; every command below was run by the closure
session. Neither lane counter nor the census selftest was executed (PROTOCOL §Gate standard, Closure consequence):
C1 is evidence-verified plus plain re-measure, C2 content is re-measured.

Driver digest (`.ufo/watchdog.log`, mutable, copied here):

    2026-10-26T13:00:51-03:00 launch tsukuroi round=41 pgid=264372 driver=hyaku-inline attempt=1
    2026-10-26T15:51:31-03:00 complete tsukuroi round=41; hyaku-inline attempt=1

## 1. Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report landed by the lane | `git log --format='%an %H' -- .ufo/reports/round-41/tsukuroi.md` (fleet) | `tsukuroi-shokunin c8cd8f3f42e7c611ce786246071a19e8b7af58ad` (author date 15:34:36, committer date 15:50:40 -03) | ok |
| Report lands last | `git -C tsukuroi-shokunin log -1 --format=%cd 6cc927df` | lane tip committed 15:48:46; report committer date 15:50:40, and the report bytes at `c8cd8f3f` cite `6cc927df` (4 mentions) | ok; note: author date 15:34:36 predates the cited tip, so the report commit was rewritten before push (note N2) |
| Cited commits exist and are ancestors of `master` | `git cat-file -t <h>`; `git merge-base --is-ancestor <h> master` for the 10 landed-change hashes plus `0e5805a1`, `8b7c4132` | 12/12 `commit`, 12/12 ancestor | ok |
| Lane pushed, clean | `scripts/hyaku/jj-lane.sh state …`; `git status --porcelain`; `git ls-remote origin refs/heads/master` | `branch=master local=6cc927df… remote=6cc927df… ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain empty; ls-remote `6cc927dfcfaa66ca460eabe097fcce7ed5e23da0` | ok |
| Round commits by the lane | `git log --format='%h %an' 8b7c4132..6cc927df` | 10 commits `tsukuroi-shokunin`, plus operator `1f5e74aa` (considerthese, rebased under the freeze; adds only `considerthese/2026-10-26.md`) | ok |
| `SHONEN` heading | `grep -c '^## SHONEN'`; box lines vs `SHONEN.md` | 1 heading; 4 `[~]` lines for 4 boxes | ok |
| Prompt carries the template contract | every non-placeholder line of `templates/round-prompt.md` present in the prompt | 140 template lines, 0 missing; hyaku addendum §6 present | ok |
| Marker test | report names 10 checkable lane commits, evidence pointers, LOG entry | real report | status `ok` |

Notes (status-neutral):
- N1 — R41-BASE-MISREAD (lane-recorded): counters and receipts name `0e5805a1` as base while the lane tip at start was
  `8b7c4132`. `git diff --stat 0e5805a1 8b7c4132` = `corpus/lessons/round-40-verifier-spotcheck.md` only, and `1f5e74aa`
  adds only `considerthese/2026-10-26.md`, so every measured surface is byte-identical at all three; no value changes.
- N2 — report commit `c8cd8f3f` carries author date 15:34:36, 14 min before the tip it cites; its committer date
  15:50:40 follows the tip. Landed-last holds on the committed and pushed bytes.
- N3 — the C1 before receipt `before/c1-before.jsonl` ran 17:56:30Z–18:02:14Z, after the after receipt at `568c397d`
  (17:17:35Z). It is pinned to revision `0e5805a1` with the frozen tool digest, and its value (`survivors 4`, H5/H6/H9/H10,
  `params 0`, FAIL) was written as the expected before value in the declaration at `d8b4d521` before either run, so the
  value stands; the declare → before → after order was not kept for this receipt.

## 2. Claims — re-check

### C1 — operability: census `--selftest` gains four held-out mount tables (frozen counter `tools/score-selftest-mounts-r41.py`)

Declared predicate: `baseline_pass == 1 and neutral_pass == 3 and decoy_pass == 1 and mutants_applied == 13 and
survivors == 0 and params == 4`, PASS at the implementation commit and the tip; kill rules: predicate false, or
`probe_storage_arm` differs from the base, or the round-40 counter stops passing at the tip.

Plain re-measure (committed bytes):

| Revision | `sha256(tools/tsukuroi-census.sh)` | `grep -cE '^[[:space:]]*check '` | `grep -c 'R41-C1 H'` | `sha256(probe_storage_arm())` (awk `/^probe_storage_arm\(\)/,/^}/`, 61 lines) |
|---|---|---|---|---|
| `0e5805a1` (base) | `032faa8f1c91…` | 121 | 0 | `71e6007e566e…` |
| `568c397d` (impl) | `646c84fcdc16…` | 125 | 4 | `71e6007e566e…` |
| `d7bf279f` | `646c84fcdc16…` | 125 | 4 | `71e6007e566e…` |
| `6cc927df` (tip) | `646c84fcdc16…` | 125 | 4 | `71e6007e566e…` |

`git diff 0e5805a1 568c397d -- tools/tsukuroi-census.sh` is one hunk inside `run_selftest` (+27/-0): four fixture
cases (`storage-mounts-mp-relative` H5, `storage-mounts-src-uuid` H6, `storage-mounts-no-subvol-opt` H9,
`storage-mounts-two-btrfs` H10), each writing its own `mounts` table and asserting
`state=BLOCKED … detail=mounts:btrfs-without-sysfs`. No self-reading construct (no `declare -f`, no read of the census
source). Census bytes are identical from `568c397d` to the tip, so the tip verdict equals the `d7bf279f` receipt.

Committed evidence (verified, not executed):
- counter digest `8306d9990b156ceb…` at `e479fdc5`, `d7bf279f` and `6cc927df` (`git show <r>:tools/score-selftest-mounts-r41.py | sha256sum`), equal to the declared sha256 and to every receipt's `tool_sha256`;
- `before/c1-before.jsonl`: revision `0e5805a1…`, `baseline_pass 1, neutral_pass 3, decoy_pass 1, mutants_applied 13, survivors 4, params 0`, exit 1; baseline label `PASS (124 cases, 124 passed, 0 failed)`;
- `after/c1-after-568c397.jsonl`: revision `568c397d…`, same fields with `survivors 0, params 4`, exit 0;
- `after/c1-final-d7bf279.jsonl`: revision `d7bf279f…`, `survivors 0, params 4`, exit 0; baseline `PASS (128 cases, 128 passed, 0 failed)` (124 + 4 = 128, matching +4 `check` calls).
- Kill rules: arm byte-identical (above); round-40 counter at the dispatch tip `w1/C1ExecPriorCounters.md` (evidence only).

Counter sufficiency is falsified by the lane's own seats (`w1/C1CritDecoy.md`, `w1/C1CritLabels.md`; QUALITY 89). The
closure's structural read of the landed hunk confirms the bytes that passed are four genuine fixture cases, so the
falsified counter did not carry this claim. **C1 verifies: operability `improved`** (ordinal 9 → 9).

### C2 — depth (sourced): `corpus/knowledge/alpm-package-anatomy-r41.md`, PA1–PA8 on S227–S236 (frozen counter `tools/check-package-anatomy-r41.py`)

Declared kill rule (SCORECARD.md "Round 41 — declaration", row C2): "the predicate is false; or any committed verdict file
for a row reads `VERDICT: fails`; or a row verdict stays `partly` without a later `holds` after an appended correction".

Re-measured:
- entry absent at base (`git cat-file -e 8b7c4132:corpus/knowledge/alpm-package-anatomy-r41.md` fails), 102 lines at tip, eight table rows `| PA1 |`…`| PA8 |`, `source:` S227–S236;
- `SOURCES.md` rows 226 → 236 (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` at `8b7c4132` / `6cc927df`), malformed 0 at both;
- frozen snapshots: `sha256sum -c SHA256SUMS` in `.ufo/waves/round-41/frozen/src/` → 9/9 OK;
- verdict files (`grep -HE '^\**VERDICT' w1/C2RevPA*.md residual/*.md`): w1 PA1 holds/holds, PA2 holds/partly, PA3 holds/partly, PA4 holds/holds, PA5 holds/partly, PA6 holds/partly, PA7 holds/partly, PA8 holds/holds; residual PA2c holds, PA3c holds, PA5c holds, **PA6c partly**, PA7c holds.
- Counter evidence: digest `c83e29a4f570422d…` at `e479fdc5`, `d7bf279f`, `6cc927df`; `before/c2-before.jsonl` 0/0/0/0 exit 1 at `0e5805a1`; `after/c2-after-d7bf279.jsonl` `rules_verified 8, verdicts_ok 8, host_ok 6, source_ok 1, duplicate_rows 0, duplicate_headings 0, novelty_base_hits 0`, exit 0.

PA6 stays `partly` after its appended correction with no later `holds`: the third kill clause fires, as the lane reports.
Closure read of the cause: `frozen/src/be_local.c` `_cache_mtree_open` returns NULL by three paths — `access` fails
(silent), `archive_read_new()` returns NULL (`GOTO_ERR`, no "error while reading file" log), open fails (logged). The
correction at `20c327b3` named two; the third bullet appended at `6cc927df` names all three and reads correctly
against the snapshot, but it carries no seat verdict and was written after the residual verdict, so it cannot reverse
the declared kill rule (a miss is an honest stop). **C2 does not verify: depth `unchanged`** (ordinal 8 → 8). Not
harmed: no PA row is false — PA6 is incomplete and marked by its appended corrections in the entry itself.

### No-harm

- `git diff --numstat 8b7c4132 6cc927df` — one file with deletions: `tools/check-self-assessment.py` (+18/-7, the routed
  R40-TMP-MISROOT `--scratch` fix); no file deleted. `SCORECARD.md` diff appends only (+106/-0); ordinals unchanged.
- `after/self-assessment-final.jsonl`: revision `64f9062e…`, `checked 27, mismatches 0`, exit 0 (evidence).
- `w1/GateAllRegistry.md`: seven lane gates exit 0 at `71851d63`, tool digests matched (evidence).
- R41-CENSUS-PIPEFAIL-692 (live census reports DEGRADED where BLOCKED is due on a large error-bearing `-Qkk` sample) is
  pre-existing: `git show 0e5805a1:tools/tsukuroi-census.sh | sed -n 692p` is the same `printf … | grep -q '^error:'`
  test; this round's census diff touches only `run_selftest`. Found, not introduced.
- Sources census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` → `tsukuroi ok`,
  exit 0, 40 W04 (39 before; the new one is S230, same `add.c` URL as S213 under a distinct scope — matches the report).

## 3. Axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| operability | improved | C1 verified: +4 genuine selftest cases, survivors 4 → 0 (receipts), arm identical; ordinal 9 → 9 |
| depth | unchanged | C2 declared kill rule fires on PA6; entry landed, marked, not false |
| coverage | unchanged | no PROVINCE/Frontier move; held pacman-state Core deepened |
| freshness | unchanged | not claimed; closure re-fetched three pinned URLs live, byte-identical to snapshots (§4) |
| calibration | unchanged | not claimed; self-assessment 27/0 (evidence); report and SCORECARD record C2 as not verified |
| adjacency | unchanged | not claimed; no sibling file touched |

Round verdict: **not admitted — `rejected-honest-stop`**. C1 verifies; C2 misses its own declared kill rule, reported
honestly by the lane; no axis harmed.

## 4. Discernment spot-check (LEARNING.md) — `corpus/lessons/round-41.md` `## Gate`

Live re-opens via `curl -sSfL https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/<path>` (2026-10-26):
`PKGBUILD.5.asciidoc` sha256 `15e8007bb11829b4…`, `add.c` `fd3136291885cae7…`, `version.c` `fa769e3081d25d74…` —
each equal to the frozen snapshot and to the row's anchor digest.

| Item | Gate decision | Re-opened source | Agree / disagree | Reason |
|---|---|---|---|---|
| S232 / PA7 — packaging-function working directories | admit | live `doc/PKGBUILD.5.asciidoc` @54d9411 :345-377 | agree | `package()` (:351), `prepare()` (:365), `build()` (:370), `check()` (:377) "run inside `$srcdir`"; `verify()` (:357) "inside `$startdir`"; fakeroot for the packaging stage (:349) — exactly the row |
| S230 / PA4 — members kept in the local database | admit | live `lib/libalpm/add.c` @54d9411 :168-189 | agree | `extract_db_file` maps `.INSTALL`→`install`, `.CHANGELOG`→`changelog`, `.MTREE`→`mtree`, skips other dot files (:180 quote present), sets 0644 |
| Staged `alpm-package-anatomy-r26.md:53-54` "`package()` runs inside `$pkgdir` under `fakeroot` and the others run inside `$srcdir`" | reject | staged file `~/Projects/shokuknow/merge/tsukuroi/knowledge/corpus/knowledge/alpm-package-anatomy-r26.md` (sha256 `3fa1b809…`, equal to the Gate's) against live PKGBUILD.5 :351, :357 | agree | false twice: `package()` runs in `$srcdir`, `verify()` in `$startdir` |
| Staged ground pointer `:6` `corpus/README.md:38-42` | reject | staged `:6` read | agree (not re-derived beyond the seat) | `w1/AsmGate.md` records those lines as boot/snapper debts; no packaging frontier |

SOURCES row re-open: S233 (`version.c`), Gate quote "different from RPM- always assume 0 epoch" (8 words, ≤25) found
at live `version.c:61`; S232 quote "This function is run inside `$startdir`." (6 words) at live `:357`; S230 quote at
live `add.c:180`. All three rows: tier A `code`/`docs`, `mined`, `used-by` the r41 entry — honest tiers.

## 5. Trend verdicts

- **expansion: unchanged** — the entry deepens held pacman-state Core (PROVINCE "`.pkg.tar.zst` receipt discipline"),
  no uncovered coverage-map ground or Frontier move, and its claim did not verify.
- **quality: unchanged** — C1 strengthens the census selftest and S220's anchor drift is marked, but the round's new
  entry fails its own re-check on PA6, so no stronger entry is admitted; nothing false is left unmarked (not harmed).
- **discernment: improved** — the outside spot-check agrees with the Gate on both sampled admits and both rejects, and
  the round's guard defeat (R41-GUARD-BYPASS) became a lesson behind a grounded QUALITY 89 criterion.

## 6. Routed defects (owner: tsukuroi, next round)

1. R41-PA6-UNJUDGED — the PA6 third-path correction (`be_local.c:263-265`) has no verdict. Next round: obtain a
   committed row verdict on PA6 with all three corrections, or record PA6 as unverified in the entry; until then
   `alpm-package-anatomy-r41.md` must not be cited as a verified C2 outcome.
2. R41-CENSUS-PIPEFAIL-692 — live census wrong verdict (DEGRADED for BLOCKED) at `tools/tsukuroi-census.sh:692`;
   fix with a selftest case red before the fix (the lane's planned row item 1).
3. R41-GUARD-BYPASS — both frozen counters beaten by reading the guard (here-document-stripping self-reader for C1;
   relation-literal writer with planted verdict files for C2). Amend under QUALITY 89: bind verdict files to the
   orchestrator results record and freeze the evasion members as should-fail controls before the next counted claim.
4. R41-BASE-MISREAD — counters and receipts must name the lane tip at round start (`jj-lane.sh state` local) as base.
5. N3 — capture each claim's before receipt before any implementation run, not only declare its value.

## 7. SHONEN (for the operator; promotion is operator-owned)

The report files 4 `[~]` lines for 4 boxes. Box 1 (decision tables, cited sources) is checkable by a non-author from
`SKILL.md` "Package anatomy and the local database — round 41" plus this file §4; boxes 2–4 still rest on lane
assertions or seat replays. No `[x]` is written here.
