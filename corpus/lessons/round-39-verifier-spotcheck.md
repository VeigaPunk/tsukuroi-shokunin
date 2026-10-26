# Round 39 — verifier spot-check (integrator, hyaku)

author: hyaku closure (non-author integrator, @m_opus)

Lane-round: tsukuroi round 39 (hyaku run 8, attempt 1). Base `0eff65b21bb81195ee06c96a83afbd7a07e52eef`, after
`a6ca81717f97b9b38d5386be246e9218c07839dc`, measured revision `a2d7aad740977088ff9fc70ed36d3ef978b27e81`. Report
`.ufo/reports/round-39/tsukuroi.md` (fleet repo), prompt `.ufo/prompts/tsukuroi-round-39.md`. Closure date 2026-10-26.
This file is the only lane path the closure writes. No lane-authored file was edited. I ran no sibling gate, counter or
census. Every "re-measured" line below is a plain read by the closure or by one of its three read-only seats
(reviewer C1, reviewer C2, critic no-harm). The tools were git, sha256sum, jq, awk, curl of upstream, and small Python
re-derivations over committed bytes.

Driver digest. Copied from the mutable `.ufo/watchdog.log`, lines 1478 and 1493:
`2026-10-26T02:35:53-03:00 launch tsukuroi round=39 pgid=3529108 driver=hyaku-inline attempt=1`;
`2026-10-26T03:38:41-03:00 complete tsukuroi round=39; hyaku-inline attempt=1`.

## 1. Step-1 conformance (re-run results)

| Check | Command | Observed | Result |
|---|---|---|---|
| Report committed by lane identity | `git log --format='%an <%ae> %H %ci' -- .ufo/reports/round-39/tsukuroi.md` | `tsukuroi-shokunin <tsukuroi@shokunin.local> c9cd39c9d67e358bd44cb3544c8fba7ab6219558 2026-10-26 03:38:11 -0300` | pass. Filed after the last cited lane commit `a6ca8171` (03:36:27) and before the driver completion line (03:38:41) |
| SHONEN heading | read report `## SHONEN` | 4 lines, one per box, all `[~]` with evidence pointers | pass |
| Cited commits exist and are ancestors | `git cat-file -e <h>^{commit}` + `git merge-base --is-ancestor <h> master` for the 9 round hashes and the base | all resolve; all ancestors of `master`. All 9 round commits are authored by `tsukuroi-shokunin` | pass |
| Lane pushed and clean | `scripts/hyaku/jj-lane.sh state …/tsukuroi-shokunin`; `git status --porcelain \| wc -l`; `git ls-remote origin refs/heads/master` | `branch=master local=a6ca8171… remote=a6ca8171… ahead=0 behind=0 head=detached tracked=0 untracked=0`; `0`; remote `a6ca8171…` | pass |
| Prompt carries template contract | every nonblank line of `kimi-shokunin/templates/round-prompt.md` (140 lines, 116 nonblank) against the 599-line prompt | 0 missing. The one textual difference is the rendered `<{{LANE}}-repo>` → lane path. Hyaku addendum §6 at `:141`. §3 quotes no route map, so there is no MISSION bucket to compare | pass |
| Gate registry rows | `git show a6ca8171:SKILL.md \| grep -n 'storage-hidden-r39\|transaction-order-r39'` | both rows present | pass |
| Sources & frontier, Trend verdicts sections | read report | both present | pass |

Conformance notes (status-neutral):
- **Future-dated timestamps** (PROTOCOL §Evidence standard):
  - The `SCORECARD.md` heading "Round 39 — declaration (2026-10-26T06:20Z …)" was committed in `93fddb2c` at 05:59:31Z, about 20 minutes before the time it states.
  - The `LOG.md` heading "Round 39 — hyaku run 8, 2026-10-26T07:45Z" was committed in `eeba342e` at 06:35:44Z, about 70 minutes before the time it states.
  - Command: `git log --format='%h %cI' -S'<heading text>' -- <file>`. Routed (§6).
- **Unstated red row in a cited receipt.** `after/gates-final-a2d7aad.txt` holds 8 gate rows. The report and SCORECARD name 7 as PASS. The 8th row is
  `check-self-assessment rc=1 … "mismatches": 7, "status": "FAIL", "declaring_round": 38` at `a2d7aad7`. That red is the stale
  round-38 table before `eeba342e` rewrote it, and `after/self-assessment-final.json` reads `eeba342e`, 27 checks, 0
  mismatches, PASS. So nothing is overclaimed at the tip, but the cited file's red row is not mentioned. Routed (§6).
- **Receipt-provenance wording.** `SCORECARD.md:2245` says the receipts under `after/` are "each written by
  `tools/run-receipt.py` (revision, tool, tool_sha256, tool_revision …)". `grep -oE 'tool_sha256|tool_revision'` finds those
  fields only in the `c1-*`/`c2-*.jsonl` receipts. The gates, self-assessment and sources-census receipts carry none.
  Routed (§6).
- **Order of declaration and implementation.** The declaration `93fddb2c` (02:59:31) precedes the C1 and C2 implementation commits by 6–8 s, so the
  implementation was written before the declaration landed. The counters themselves were frozen earlier, at `6a08925d`
  (02:47:11), and their bytes are unchanged afterwards (§2). The predicate was therefore fixed before the
  implementation landed. Noted, not a defect.

Status: real report with checkable work and pushed commits → **ok**.

## 2. Per-claim re-check (closure's own measurements)

`git diff --stat a2d7aad7 a6ca8171` touches only 6 receipt files under `.ufo/waves/round-39/after/`, `LOG.md` and
`SCORECARD.md`. Neither counter reads any of these, so the measured revision and the tip are equivalent for both claims.

### C1 (operability) — re-measured by code read and emulation, plus evidence-verified receipts. VERIFIED.

| Check | Measurement | Observed |
|---|---|---|
| Production path, not fixture-gated | read `probe_storage_arm`, `git show a2d7aad7:tools/tsukuroi-census.sh` `:1906-1919`, `:460` | The mount-table branch runs when `fsn -eq 0 && blocked -eq 0`. `PROC_MOUNTS=${TSUKUROI_PROC_MOUNTS:-/proc/self/mounts}`, and the branch runs whether or not the override is set |
| Parse | `:1912-1913` | `while read -r _src _mp fst _rest; do [ "${fst:-}" = btrfs ]`. This is exact equality on the third field, not a substring or literal key |
| Populated root unchanged | `:1906`; selftest `storage-mounted-populated` `:2995-2997` | A populated root never reads the table and stays HEALTHY 1/1/0 |
| Verdict-neutral, read-only | `:3093-3110`; `:1908-1918` | STORAGE is printed outside the six-plane rollup. The branch only runs `[ -f ]`, `cat` and `read` |
| Independent emulation (Python re-implementation of `:1865-1924`) | absent root plus this host's `/proc/self/mounts` (4 btrfs mounts: `/`, `/home`, `/var/cache/pacman/pkg`, `/var/log`); real root; FIFO table; empty table; ext4-only table | `state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs`, byte-identical to the committed hidden legs. The real root gives HEALTHY 1/1/0, and `cat /sys/fs/btrfs/*/devinfo/*/error_stats` reads five zeros (fsid `1d02a454…`). FIFO and empty tables give `mounts:unreadable`. ext4-only gives HEALTHY 0/0/0, so it does not over-block |
| Counter frozen | `git show <r>:tools/score-storage-hidden-r39.py \| sha256sum` at `6a08925d 49cc53c7 a2d7aad7 a6ca8171`; `git log -- <file>` | `75a9e8ab…` at all four revisions; only `6a08925` touches the file |
| Receipts (evidence-verified) | `jq` on `before/c1-before.jsonl`, `after/c1-after-49cc53c.jsonl`, `after/c1-final-a2d7aad.jsonl` | Before: 0/3/2/1/1, FAIL exit 1, revision `0eff65b2`, `tool_sha256 75a9e8ab…`. After: 2/3/5/1/1, PASS exit 0 at `49cc53c7` and `a2d7aad7`. Live leg `HEALTHY 1/1/0`, matching my sysfs read |
| Selftest no-harm (evidence-verified) | `after/selftest-final-a2d7aad.txt`; round-38 `after/selftest-final-b0005ae.txt` | 119/119 PASS against the base's 113/113. The 6 new cases are in the diff |
| Controls and leak arms (evidence-verified) | `jq` on `controls/controls.jsonl`, `w1/C1LeakArms/scores.jsonl` | C1-K0 to K3 all FAIL and the candidate PASSes, all with the same `counter_sha256`. The four round-38 leak arms all FAIL. Round-38 routed defects §6.1 and §6.2 are closed |
| IN-109 anchor | `jq` on the anchor JSON; `awk 'NR==2452'` on the census at `a2d7aad7` | `found_line 2452`, and the quote equals census line 2452 verbatim |

- The recorded counter-sensitivity defects are the fixture literal monoculture (`w1/C1CritControl.md`) and the namespace-detecting literal arm (`w1/C1DetectHonest.md`).
- These defects falsify the counter's sufficiency, not the landed arm. The arm has no namespace introspection and builds its line from computed values, and my emulation reproduces every leg.
- Axis verdict: **operability improved** (ordinal 9 → 9 by the lane's choice).

### C2 (depth, sourced S208, S213–S218) — re-measured by independent re-derivation plus an upstream re-open. VERIFIED.

The lane reports that its frozen counter never reads the rule cell (R39-CONTENT-UNREAD), so the counter alone cannot
carry this claim. The closure therefore judged every rule's content against pinned source.

| Check | Measurement | Observed |
|---|---|---|
| Base absence | `git cat-file -e 0eff65b2:corpus/knowledge/pacman-transaction-order-r39.md` | `fatal: … not in '0eff65b2'` |
| Upstream equals snapshots and anchors | `curl -fsSL https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/lib/libalpm/{add,sync,remove,util,trans,hook}.c` + `sha256sum` | `fd313629…`, `6b297364…`, `a052d455…`, `381618b6…`, `637c1165…`, `99f1044b…`. All six equal `frozen/src/SHA256SUMS` and the S208/S213–S217 anchors |
| TO1 | trans.c `:202-208`, `:235-238` | Pre `_alpm_hook_run` :202 runs before `transaction started` :208, and Post :238 runs after `transaction completed` :235. **holds** |
| TO2 | sync.c `:1340-1354` | `_alpm_remove_packages` :1345 runs before `_alpm_upgrade_packages` :1354. **holds** |
| TO3 | add.c `:466-647` | pre scriptlet :470-473, then extraction, then the log switch :616-636, then the post scriptlet :638-647. The appended correction's verbs and the NOSCRIPTLET skips :469/:640 are confirmed. **holds** |
| TO4 | add.c `:472-473`; trans.c `:389-413` | new version first, then old. **holds** |
| TO5 | hook.c `:532-560` | `opendir` :554 sits inside the per-call hookdirs loop, and Pre and Post are separate calls. **holds** |
| TO6 | add.c `:686-692` | Failure sets `skip_ldconfig`, and `_alpm_ldconfig` runs at most once. **holds**. The host cell's "interrupted" case has 0 host instances. It is now re-attributed append-only as a source consequence (R39-HOSTCELL-INFERRED-AS-SEEN) |
| TO7 | remove.c `:711`, `:722`, `:731` | `pre_remove`, then `removed`, then `post_remove`, all `!newpkg`-guarded. **holds** |
| TO8 | util.c `:527`, `:665-666` | `alpm_logaction(handle, "ALPM-SCRIPTLET", "%s", line)`, and the child's stdout and stderr are both dup2'd. **holds** |
| Host oracle (own Python over `frozen/txcapture/pacman.log`; sha256 chain to MANIFEST `cb5cb4f4…` verified) | count and order within transaction windows | 60 started, 60 completed, 0 interrupted, 0 failed. 295 `running` hook lines, 0 inside a commit window. 441 ALPM-SCRIPTLET lines: 189 inside, 252 outside. 0 windows mix `upgraded` and `removed`. This equals the entry's host cells, S218 and the report |
| Counter frozen; receipts (evidence-verified) | sha256 of `tools/check-transaction-order-r39.py` at `6a08925d`, `a2d7aad7`; `jq` on the receipts | `f1c97836…` at both revisions. Before: 0/0/0, FAIL exit 1. After: 8, dup 0/0, `source_ok 1`, `counts_ok 2`, oracle 0, PASS exit 0, revision `a2d7aad7` |
| Append-only wave corrections | `git diff --numstat 4078eb23 a2d7aad7 -- <entry>` | `27 0` |

- Content tally: **8 holds, 0 partly, 0 false** at pacman 54d9411.
- The wave's `partly` verdicts on TO3 and TO5 asked for completeness and host-column sharpening. Both are answered append-only.
- Axis verdict: **depth improved** (ordinal 8 → 8). This rests on the closure's re-derivation, not on the defective counter.

### Owned axes not claimed

`git diff --numstat 0eff65b2 a6ca8171 -- SCORECARD.md` → `82 0`. Ordinals are unchanged (depth 8, coverage 9,
operability 9, freshness 9, calibration 9, adjacency 8).

Deletions across the round (`git diff --numstat … | awk '$2>0'`):
- `tools/tsukuroi-census.sh`, 5 lines: the "Known limit, recorded not repaired" comment, which is superseded by the implemented rule at `:364-370`.
- `adjacency-anchors-r19.json`, 2/2: the IN-109 repin.
- `corpus/SOURCES.md`, 1: S208's used-by cell only. A cell-split compare shows S210 is byte-identical.

The TO1/TO8 corrections in 7 notes and 3 SKILL sections are append-only, none of those files deletes a line, and two spot-reads (util.c :665-666; pacman.log :1950/:1977-1979) are accurate.

A sibling `PROVINCE.md` sweep with `grep -ciE 'transaction order|alpm-scriptlet|btrfs-without-sysfs|proc/self/mounts|sysfs root'` scores 0 in all 20 other lanes. The tsukuroi `PROVINCE.md` diff is `14 0`.

Verdicts:
- **coverage unchanged**: no claim. The limit closure sits inside the existing Core arm.
- **freshness unchanged**: no claim. The libalpm re-open is creditable work, but it was not declared.
- **calibration unchanged**: the self-assessment is 27/0 at `eeba342e`. The wording defects above are routed, not harm.
- **adjacency unchanged**.

No axis is harmed. The declared side effect (round-38 v1 F06 now reads BLOCKED) was pre-declared in `93fddb2c` and is
pinned historical in `SKILL.md`. It is not harm.

## 3. Discernment spot-check (LEARNING.md — from outside)

| Item | Gate decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S216 (libalpm util.c) → `pacman-transaction-order-r39.md` TO8 | admit, tier A, mined | https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/lib/libalpm/util.c (fetched 2026-10-26; sha256 `381618b6…` = anchor) | agree | The quote `alpm_logaction(handle, "ALPM-SCRIPTLET", "%s", line);` sits at :527 inside `_alpm_chroot_process_output` :521. The `teaches` cell ("every chrooted child's output … hook or scriptlet or ldconfig") is grounded because all three callers route through `_alpm_run_chroot`: hook.c :525/:528, trans.c :410, and util.c :833 (`_alpm_ldconfig` at :820) |
| S214 (libalpm sync.c) → TO2 | admit, tier A, mined | …/-/raw/54d9411/lib/libalpm/sync.c (sha256 `6b297364…` = anchor) | agree | The quote `/* remove conflicting and to-be-replaced packages */` is at :1340. `_alpm_remove_packages` :1345 runs before `_alpm_upgrade_packages` :1354 |
| Staged `pacman-hook-timing-r25.md` interpretive sentences (`:22`, `:26-27`) | reject | the staged file `shokuknow/merge/tsukuroi/knowledge/corpus/knowledge/pacman-hook-timing-r25.md` (sha256 `e18c146e…` = the Gate's); https://devblog.archlinux.page/2026/on-scripts-and-hooks/ (fetched 2026-10-26); …/-/raw/54d9411/doc/alpm-hooks.5.asciidoc (sha256 `2970cb35…`) | agree | The devblog sentence is real and verbatim: "we are missing a documented ordering system for alpm-hooks(5) in the distribution to establish ranges of number prefixes for specific tasks". It sits under "Notes for package maintainers › Documentation", and the page never says "alphabet" (0 hits in my fetch). The sentence is about a distribution prefix-range convention, not about ordering being undesigned. alpm-hooks(5) :38-39 documents the order ("Hooks are run in alphabetical order of their file name, where the ordering ignores the suffix."), and :98-100 documents override by a higher-priority directory. So "no documented precedence scheme … filename is the only lever" is contradicted. The flip condition is stated |
| Staged "independent confirmation" sentence (`:59-61`) | reject | the same staged file `:55-63` | agree | The candidate itself says the Chinese page is "a community translation of an older ArchWiki revision (translation source `en:Pacman` …)", so it cannot independently confirm the page it translates |

New `corpus/SOURCES.md` row re-opened: **S216**.
- Its quote is 6 words (≤25) and resolves at util.c:527.
- Every line its anchor cell names checks: :521-528, :610 and :820.
- The snapshot digest equals my fetch.

S214's quote likewise resolves at :1340.

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` → `tsukuroi ok`, exit 0, with 34
W04 advisories only.

| Revision | Rows (`grep -cE '^ {0,3}\| *S[0-9]{3,} *\|'`) | Malformed (`awk NF!=13`) |
|---|---|---|
| base `0eff65b2` | 212 | 0 |
| tip `a6ca8171` | 218 | 0 |

The `SOURCES.md` diff is 7+1: six appended rows, plus S208's used-by cell (`7 1`). This matches the report (212 → 218).

Result: the closure agrees with every sampled admit (S216, S214) and with both sampled rejects.

## 4. Axis grades (closure)

| Axis | Verdict | Basis |
|---|---|---|
| operability | improved | C1 verified. The guard is in the production path with an exact fstype parse. My emulation reproduces every leg, the counter is frozen, the receipts agree, the selftest reads 113 → 119, and the leak arms FAIL |
| depth | improved | C2 verified by independent re-derivation: 8/8 TO rows hold at pinned 54d9411, the six upstream files equal the snapshots, and the log oracle shows 0 in-commit hook lines |
| coverage | unchanged | no claim; no harm |
| freshness | unchanged | no claim; no harm |
| calibration | unchanged | self-assessment 27/0 (receipt); wording defects routed |
| adjacency | unchanged | no sibling overlap (province sweep) |

Admission: **admitted**. Both claims verify, and no axis is harmed. Verdict: `admitted`.

## 5. Trend verdicts (closure)

- **expansion: improved.**
  - One new admitted entry on ground the base did not hold (base absence above).
  - Its `source:` cites only `mined` rows (S208, S213–S218), and its content holds 8/8 at pinned source.
  - No admitted entry fails its bar.
- **quality: improved.**
  - S210's wrong anchor is superseded by the stronger row S217. The S210 bytes are unchanged.
  - The TO1/TO8 corrections in 7 older notes and 3 SKILL sections are append-only, and both spot-reads are accurate.
  - The TO6 host cell inferred as seen is re-attributed append-only.
  - No admitted entry failed my re-checks.
- **discernment: improved.**
  - The outside spot-check agrees with the Gate on both sampled admits and both sampled rejects.
  - QUALITY 85–87 each cite a lesson row (R38-Q82-LEAK, R38-C2-COUNTER-GAPS, R39-CONTENT-UNREAD).
  - The lane named the defects in both of its own new counters instead of hiding them.

## 6. Routed defects / next-round debts (owner: tsukuroi)

1. **C2 counter reads no content** (R39-CONTENT-UNREAD; self-filed):
   - Any re-claim on transaction order must use an amended counter that reads the rule cell.
   - Freeze X-empty and X-false as should-fail controls (QUALITY 87).
   - The closure's 8/8 is a one-time re-derivation, not a standing instrument.
2. **C1 fixture monoculture and the detect-honest class** (R39-FIXTURE-MONOCULTURE; `w1/C1DetectHonest.md`):
   - Vary device, subvolume and option literals across fixtures.
   - Freeze a one-literal arm as a should-fail control.
   - The counter's live leg ignores `census_exit` (`2` was recorded while matching): decide whether that is intended and record the decision.
3. **Future-dated timestamps**: the SCORECARD declaration heading says 06:20Z but was committed at 05:59:31Z, and the LOG heading says 07:45Z but was committed at 06:35:44Z. Append a named correction. Do not rewrite.
4. **Gates receipt disclosure**: the report and SCORECARD should name the 8th row of `after/gates-final-a2d7aad.txt`, `check-self-assessment rc=1`, 7 mismatches at `a2d7aad7`, and say why it was superseded by `eeba342e`. Append a correction.
5. **Receipt-provenance wording**: `SCORECARD.md:2245` says "each written by `tools/run-receipt.py` (… tool_sha256 …)". Only the `c1-*`/`c2-*.jsonl` receipts carry those fields. Scope the sentence with an appended correction, or bind the other receipt classes too.
6. **Residual staged propositions** (NeedsTargets→stdin, `.pacnew` trigger target, scriptlet cwd, interpreter): these are deferred with flip conditions in the Gate. Land them on new rows from S219 if pursued.
7. **Lesson cross-reference**: the lesson Gate "Spot-check: Non-author closure pending" (`corpus/lessons/round-39.md:61-64`) is answered by this file. Cross-reference it next round.

## 7. Closure disposition

Status **ok**. Admitted **true** (`admitted`).

Verdicts:
- improved: operability, depth
- unchanged: coverage, freshness, calibration, adjacency

Trends: expansion improved, quality improved, discernment improved.

SHONEN:
- Boxes 1–2 look checkable by a non-author from the cited evidence: the SKILL tables "Storage integrity arm — round 39" and "Transaction order — round 39", and the LOG end-to-end task, whose pacman.log oracle I reproduced (60 transactions, 0 in-commit hook lines, 252 of 441 tag lines outside commits).
- Box 3 does not: the whole-SKILL retest is unexecuted.
- Box 4 does not: no-bleed is self-asserted, although my province sweep found no crossing.

Promotion is operator-owned.
