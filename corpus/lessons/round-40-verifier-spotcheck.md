# Round 40 — verifier spot-check (non-author closure)

author: hyaku closure (non-author integrator, @m_opus)

Lane-round: tsukuroi round 40. Base `53b294a274656be6479aadf2ec2fee890ded77ce`, tip `0e5805a1f149bd2ed9fe0db2e0a832afb034a835`
(branch `master`). Report: `.ufo/reports/round-40/tsukuroi.md` (fleet repo). Dispatched prompt:
`.ufo/prompts/tsukuroi-round-40.md`. Closed 2026-10-26. This file is written by the closure, not by the lane; the
lane must not edit it. Read-only re-check seats used by this closure: R40C1Recheck, R40C2Recheck, R40NoHarm
(reviewer role, dispatched by the closure, not by the lane). No lane gate, counter or selftest was executed by the
closure (PROTOCOL §Gate standard, Closure consequence); everything below is either a plain re-measurement over committed
bytes / live upstream sources, or a check of committed gate evidence, and each line says which.

Driver digest (copied from `.ufo/watchdog.log`, which is mutable):
- `2026-10-26T03:48:27-03:00 launch tsukuroi round=40 pgid=2520481 driver=hyaku-inline attempt=1`
- `2026-10-26T05:19:42-03:00 complete tsukuroi round=40; hyaku-inline attempt=1`

## 1. Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report landed by lane identity | `git log --format='%an <%ae> %H %ci' -- .ufo/reports/round-40/tsukuroi.md` | `tsukuroi-shokunin <tsukuroi@shokunin.local> 3d5b808ba5ca5612f74469538e09e11cf1b25e3c 2026-10-26 05:18:55 -0300` | ok |
| Report lands last | `git -C tsukuroi-shokunin log --format='%h %ci %s' 53b294a2..0e5805a1` | last lane commit `0e5805a` 05:18:45, report 05:18:55, driver `complete` 05:19:42 | ok |
| `SHONEN` heading, one line per box | `grep -c '^## SHONEN' <report>`; `git show 0e5805a1:SHONEN.md \| grep -cE '^\s*- \[[ x~]\]'` | `1`; 4 boxes; report carries 4 `[~]` lines | ok |
| Cited commits exist and are ancestors | `git cat-file -e <h>^{commit} && git merge-base --is-ancestor <h> master` for the 10 hashes of the report's Landed-changes table | 10/10 `ok` (a447b67b, 758a4b08, c707e356, bf238050, f951f288, aad01138, e3bc9340, d84e2aab, 6c20e44b, 0e5805a1) | ok |
| Lane pushed, nothing uncommitted | `scripts/hyaku/jj-lane.sh state <lane>`; `git status --porcelain`; `git ls-remote origin refs/heads/master` | `ahead=0 behind=0 head=detached tracked=0 untracked=0`, local=remote=`0e5805a1…`; porcelain empty; remote prints `0e5805a1…` | ok |
| Prompt carries the template contract | every non-placeholder line of `templates/round-prompt.md` searched in the prompt (python, exact substring) | 140 template lines, 0 missing; hyaku addendum §6 present | ok |
| LOG entries | `git show 0e5805a1:LOG.md \| grep -n '^## Round 40'` | `:1479` erratum (R40-HEADING-TIMES), `:1509` "Round 40 — hyaku run 8" | ok |
| Marker test | report names work, evidence pointers, LOG entries and 10 resolvable hashes | real report, not a marker | status `ok` |

Conformance defects: none that bear on status. Minor items are routed in §6.

## 2. Claims — re-check

### C1 — operability: census `--selftest` varies mount-table literals (frozen counter `tools/score-selftest-literals-r40.py`)

Evidence-verified (committed counter receipts) plus plain re-measurement of the landed bytes; the counter and the
census selftest were not executed.

| Re-check | Command | Observed |
|---|---|---|
| Change confined to `run_selftest` | `git diff 53b294a2 c707e356 -- tools/tsukuroi-census.sh`; same against `0e5805a1` | identical diffs: 1 hunk `@@ -3006,6 +3006,42 @@` inside `run_selftest` (+36/−0), 5 new `check` cases |
| Arm untouched | awk-extract `probe_storage_arm() {`…`^}` from `git show` at base, c707e356, tip; `sha256sum` | all three `71e6007e566e1af32feb495e04e4f291c75fdddb2b521d9822b7363fcdf34d56` (report: `71e6007e…`) |
| Fixtures are real, no self-reading | read the 36 added lines; grep `declare\|BASH_SOURCE\|BASH_ARGV0\|\$0\|/dev/fd\|eval\|source\|mapfile` over tip `run_selftest` | five mount-table fixtures (varied `/home` subvol line mid-table; 4-line table with ro/compress `/var/lib/machines`; ext4 line with `btrfs` in label, mountpoint and option; fstype `BTRFS`; unreadable root with `/dev/vdb /data btrfs` mounted); self-read grep hits only the word "declared" |
| Case count | `git show 0e5805a1:tools/tsukuroi-census.sh \| grep -cE '^\s*check(_cli)? '` | 124 (all inside `run_selftest`), equals receipt `PASS (124 cases, 124 passed, 0 failed)` |
| Counter frozen | `git show a447b67b:tools/score-selftest-literals-r40.py \| sha256sum`; same at tip; `git diff a447b67b 0e5805a1 -- <tool>` | both `8b06de18ca7eec1d928a0dfac8ca6930bf808bfd1f4250374ec300640f2f0159`; diff empty |
| Receipts | `git show 0e5805a1:.ufo/waves/round-40/{before/c1-before.jsonl,after/c1-after-c707e35.jsonl,after/c1-final-aad0113.jsonl}` | before rev `53b294a2…` exit 1, survivors 9, baseline 119/119; after rev `c707e356…` and `aad01138…` exit 0, baseline_pass 1, neutral_pass 3, mutants_applied 9, survivors 0, selfref 5; every `tool_sha256` = `8b06de18…`, `tool_revision` `a447b67b…` |
| Kill mechanism (reasoned from bytes, not executed) | read mutant M1 (`case $mtab in *'/dev/mapper/root'*)`) and M7 (guard drops `blocked -eq 0`) against the new fixtures | M1: the varied tables carry no `/dev/mapper/root`, so the mutant reads HEALTHY where the pin expects `BLOCKED …mounts:btrfs-without-sysfs` (receipt M1 `122 passed, 2 failed`); M7: the unreadable-root-with-btrfs fixture gains `mounts:btrfs-without-sysfs` in its detail under the mutant (receipt M7 `123 passed, 1 failed`) |

Before → after re-derived: survivors 9 → 0, baseline 119 → 124/124, predicate as declared. Limits the lane itself
recorded and the closure confirms by reading `w1/C1CritControl.md`, `w1/C1HeldOutMutants.md`, `w1/C1HeldOutGuards.md`:
a one-line `declare -f`/`${0}`/`${BASH_ARGV0}` prologue would pass the frozen predicate without any fixture (counter
sufficiency, R40-ANSWER-KEY); held-out mutants H5/H6/H9 survive the 124-case suite; the counter's `first_fails` is
always empty (FAIL lines go to stderr). The landed selftest uses none of the self-reading routes, so the kills are
fixture-driven. **C1 verifies.**

### C2 — depth (sourced): `corpus/knowledge/pacman-exec-environment-r40.md`, EX1–EX8 on S219–S225 (frozen counter `tools/check-exec-environment-r40.py`)

Content re-measured from the frozen snapshots and from the live upstream sources; counter receipts evidence-verified;
the counter was not executed.

| Re-check | Command | Observed |
|---|---|---|
| Entry absent at base, present at tip | `git cat-file -e 53b294a2:corpus/knowledge/pacman-exec-environment-r40.md`; `git show 0e5805a1:… \| wc -l` | absent (rc 128); 115 lines; `git diff bf238050 0e5805a1 -- <entry>` 0 removed, 63 added (corrections appended) |
| Frozen snapshots intact | each `git show 0e5805a1:.ufo/waves/round-40/frozen/src/<f> \| sha256sum` vs `SHA256SUMS` | 6/6 match |
| Live upstream equals the snapshots | `curl -sSfL https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/{lib/libalpm/util.c,lib/libalpm/trans.c,lib/libalpm/hook.c,meson_options.txt,doc/alpm-hooks.5.asciidoc}` and `…/packaging/packages/pacman/-/raw/7.1.0.r9.g54d9411-3/PKGBUILD`, `sha256sum` | util.c `381618b6…`, trans.c `637c1165…`, hook.c `99f1044b…`, meson_options.txt `89e5b350…`, alpm-hooks.5 `2970cb35…`, PKGBUILD `32d40dfd…` — all equal the Gate digests |
| Host capture (S225) | `strings /usr/lib/libalpm.so.16.0.1 \| grep -nx '/usr/bin/bash\|/bin/sh'`; count of effective `*.hook` files (`/etc/pacman.d/hooks` overriding `/usr/share/libalpm/hooks`) containing `NeedsTargets` | `1277:/usr/bin/bash`, no `/bin/sh`; 69 hooks, 14 with `NeedsTargets` — equal the capture |
| Per-rule truth (seat R40C2Recheck, read against the snapshots; EX1, EX3, EX4 also read live by the closure) | see table below | 8/8 supports at the tip, counting the appended corrections |
| SOURCES rows | `git show <rev>:corpus/SOURCES.md \| grep -cE '^ {0,3}\| *S[0-9]{3,} *\|'`; malformed-row awk (CORPUS.md census) | 218 → 226; malformed 0; S219–S226 `mined`, used-by the entry |
| Receipts | `git show 0e5805a1:.ufo/waves/round-40/{before/c2-before.jsonl,after/c2-after-bf23805.jsonl,after/c2-final-aad0113.jsonl,after/c2-final-e3bc934.jsonl}` | before rev `53b294a2…` rules 0 FAIL exit 1; three afters (`bf238050…`, `aad01138…`, `e3bc9340…`) rules_verified 8, source_ok 1, counts_ok 2, novelty_base_hits 0, PASS exit 0; `tool_sha256` `d4a2bb94…` = tool bytes at a447b67b and tip |

| EX | Rule (short) | Source line read | Verdict |
|---|---|---|---|
| EX1 | child starts in `/` | util.c:628 `chdir(handle->root)`; :679 chroot only if root ≠ `/`; :683 `chdir("/")` | supports |
| EX2 | stdout+stderr one socket; stdin second socket, closed when no input callback | util.c:665-667; :722-726 | supports |
| EX3 | SHLVL=1 unless inherited, BASH_ENV unset, umask 0022 | util.c:692 `setenv("SHLVL", "1", 0)`, :694, :695 | supports |
| EX4 | scriptlet shell `/usr/bin/bash` on Arch, upstream default `/bin/sh` | PKGBUILD:115; meson_options.txt:17; trans.c:357-358 | supports |
| EX5 | `<root>/tmp/alpm_XXXXXX/.INSTALL`, removed afterwards | trans.c:360-377, :412-420 | supports (host sentence "/tmp is a tmpfs" was false and is withdrawn append-only; the correction is accurate — `/tmp` is xfs) |
| EX6 | NeedsTargets stdin sorted, de-duplicated, one per line | hook.c:521-524, :476 | supports |
| EX7 | `running` logged before Depends checked; abort only with AbortOnFail | hook.c:653 then :660; :509-516; :660-668 | supports (with the appended Post-phase correction) |
| EX8 | Path trigger on file-list names; NoExtract skipped; NoUpgrade ignored | hook.c:271, :274; `grep -ci noupgrade hook.c` → 0; alpm-hooks.5:126-129 | supports (with the appended operation split) |

The lane's own seats show the C2 counter is a shape/provenance gate, not a reading check (`w1/C2CritControl.md`
token-list writer, `w1/C2CritXFalse.md` non-negated false rules both pass 8/8). The closure therefore does not rest C2
on the counter: content truth rests on the per-rule re-read above, which holds 8/8. Novelty (`w1/C2ScoutNovelty.md`):
EX1, EX3, EX4, EX5, EX6, the EX7 ordering and the EX8 trigger half are not held at the base; the EX2 merge half and the
EX7 AbortOnFail half were already held. **C2 verifies.**

### No-harm

| Re-check | Command | Observed |
|---|---|---|
| Deletions across the round | `git diff --numstat 53b294a2 0e5805a1 \| awk '$2>0'` | only `corpus/SOURCES.md` 10/2: S208, S209 rows, cell-compared — only `used-by` differs (CORPUS.md rule 2 permits; logged old→new in the Gate) |
| Append-only owned files | `git diff --numstat 53b294a2 0e5805a1 -- LOG.md SCORECARD.md corpus/QUALITY.md corpus/README.md SKILL.md` | 55/0, 163/0, 237/0, 2/0, 36/0 |
| Lane gates (committed evidence) | `git show 0e5805a1:.ufo/waves/round-40/after/gate-*-aad0113.jsonl`, `r39-c2-aad0113.jsonl`, `self-assessment-final.jsonl` | seven gates rev `aad01138…` exit 0 PASS; round-39 C2 counter exit 0; self-assessment rev `e3bc9340…` 27 checked, 0 mismatches, exit 0 |
| Axes-table counts | `git ls-tree`/`git show … \| wc -l` at aad01138 and tip | knowledge notes 61, SKILL.md 3559 lines / 928 table lines, lessons 56, README 353 — equal at both revisions |
| Sources census | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` (run by the closure) | `tsukuroi ok`, exit 0; W04 advisories 34 → 39: the five new ones are S221–S224 and S226 sharing a URL with an earlier row under a distinct scope (declared in the Gate) |
| SKILL registry rows for both counters | `git show 0e5805a1:SKILL.md` registry rows `selftest-literals-r40`, `exec-environment-r40` | present: kind gate, entry command, verdict map 0/1/2, self-test/footprint, pinned sha256 |

## 3. Axis verdicts

| Axis | Verdict | Reason |
|---|---|---|
| operability | improved | C1 verified: selftest kills the 9 frozen literal/guard mutants that survived at the base, arm byte-identical, fixture-driven (§2 C1) |
| depth | improved | C2 verified: new sourced entry, 8/8 rules hold at pinned and live source, corrections append-only (§2 C2); ordinal stays 8 per the lane's own table |
| coverage | unchanged | no Frontier move; the entry deepens held update-safety Core |
| freshness | unchanged | sources re-opened byte-identical to round 39's; round-39 counters still pass |
| calibration | unchanged | self-assessment 27/0 at e3bc9340; axes-table counts re-derived equal |
| adjacency | unchanged | no claim; adjacency-anchors gate exit 0; no crossing found |

No axis harmed. Both claims verify. **Admitted.**

## 4. Discernment spot-check (LEARNING.md) — `corpus/lessons/round-40.md` `## Gate`

| Item | Gate decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S220 Arch PKGBUILD `-Dscriptlet-shell=/usr/bin/bash \` | admit, tier A | `https://gitlab.archlinux.org/archlinux/packaging/packages/pacman/-/raw/7.1.0.r9.g54d9411-3/PKGBUILD` (live, sha256 `32d40dfd…` = Gate) | agree | line 115 carries the quote verbatim inside `build()`; `_git_patch_level_commit=54d9411…` at :9 ties it to the libalpm source used. Anchor nit: the meson call is :111-117 (:110 is blank), the row and Gate say :110-117 |
| S221 util.c quote “/* bash sources $BASH_ENV when run non-interactively */” | admit, tier A | `…/pacman/pacman/-/raw/54d9411/lib/libalpm/util.c` (live, `381618b6…`) | agree | quote at :693 verbatim; `chdir("/")` :683, SHLVL :692, umask :695 as the row anchors; 8 words |
| S222 trans.c quote “/* create a directory in $root/tmp/ for copying/extracting the scriptlet */” | admit, tier A | `…/lib/libalpm/trans.c` (live, `637c1165…`) | agree | quote at :360 verbatim; `mkdtemp` :368, `.INSTALL` :377 |
| S224 / S226 alpm-hooks(5) | admit, tier A | `…/doc/alpm-hooks.5.asciidoc` (live, `2970cb35…`) | agree | NeedsTargets quote at :92-93; CAVEATS `.pacnew` quote at :126-127 (23 words) |
| S225 own-work host capture | admit, own-work | live host: `strings /usr/lib/libalpm.so.16.0.1`; effective hook census | agree | `/usr/bin/bash` at strings index 1277, no `/bin/sh`; 14 of 69 effective hooks carry NeedsTargets — capture reproduces |
| Staged inference “so every path inside them must be absolute” (`merge/tsukuroi/…/pacman-hook-timing-r25.md:47-48`, sha256 `e18c146e…` re-checked) | reject | util.c:679-687 (live) | agree | the child changes to `/` after the optional chroot, so a relative path resolves from `/`; no pacman source or doc requires absolute paths. It is advice stated as a requirement |

Newly written `corpus/SOURCES.md` row re-opened: S220 (above) — its ≤25-word Gate quote `-Dscriptlet-shell=/usr/bin/bash \`
is present verbatim at the cited line; S219 quote `option('scriptlet-shell', type : 'string', value : '/bin/sh',` is
present at meson_options.txt:17 (live, `89e5b350…`). `sources-census.sh validate`: `tsukuroi ok`, exit 0.

## 5. Trend verdicts

- **expansion: unchanged.** The entry is admitted and new relative to the base, but it deepens held update-safety
  Core ground; the coverage map gains no uncovered area and no Frontier area moves (`corpus/README.md` round-40
  section). The closure agrees with the lane's grading under LEARNING.md ("ground the coverage map did not hold").
  Note: the round-39 closure graded a same-plane deepening `improved`; this closure applies the stricter reading the
  lane itself argued.
- **quality: improved.** C1's selftest now refuses nine mutants that passed at the base; the entry's one false host
  sentence (EX5 tmpfs) was caught in-round and withdrawn append-only rather than left unmarked; the seven round-39
  routed defects carry appended corrections/disclosures; no admitted entry fails its re-check (8/8).
- **discernment: improved.** The outside spot-check agrees with the Gate on every sampled admit (S219–S222, S224–S226)
  and on the sampled reject, and the round's counter-sufficiency disagreement (R40-ANSWER-KEY) became a lesson behind
  a new grounded criterion, QUALITY 88. The lane graded `unchanged` pending this check; the check is now on record.

## 6. Routed defects (owner: tsukuroi, next round)

1. **R40-ANSWER-KEY (both counters).** Amend under QUALITY 88 as the lane's planned row says: C1 selfref over the
   executed selftest plus the `declare -f`/`${0}`/`${BASH_ARGV0}` prologue and held-out H5/H6/H9 as frozen should-fail
   arms; C2 a per-row proposition check refusing the token-list writer and the `w1/C2CritXFalse` entries.
2. **C1 counter `first_fails` always empty** (FAIL lines on stderr, counter scans stdout) and neutral_pass flakiness
   under load (`w1/C1CritControl.md`); scratch kept after Ctrl-C (`w1/C1SentScratch.md`).
3. **R40-TMP-MISROOT not yet shown able to fail:** `tools/check-self-assessment.py --scratch` passed to its census child.
4. **S220 anchor drift:** row and Gate say "meson call lines 110-117"; the live and snapshot PKGBUILD put it at
   :111-117 (:110 blank). Correct by an appended note (registry rows are append-only except status/recheck/used-by).
5. **Census W04 34 → 39:** the five new same-URL rows are declared distinct scopes; record that W04 delta in the next
   report's Sources & frontier line instead of "W04 advisories only".

## 7. SHONEN (for the operator; promotion is operator-owned)

All four boxes are `[~]` in the report. Box 1 (real decision tables with cited sources) looks checkable by a non-author
from the evidence above: the round-40 EX table re-verified 8/8 against pinned and live source. Box 2 (end-to-end task
in LOG.md) was not replayed by this closure. Boxes 3 and 4 rest on unexecuted or self-asserted checks. No box is
written `[x]` here.
