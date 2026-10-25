# Round 18 — verifier spot-check (non-author)

author: hyaku closure (non-author integrator, @m_opus)

Date: 2026-10-20. Lane-round: tsukuroi r18. Lane HEAD before `842a5312b704b5cda10fd80ec1fdee5fb381ba97`, after
`c68945c272efda203f214d3a02322f5fe6e46874`. Report: fleet `.ufo/reports/round-18/tsukuroi.md` at `0b469d14b6d9580c7fd6284b67a3fed36540c4d3`.
This closure did not author the round. It edits no lane-authored file. It writes only this file and the MANIFEST
closure entry. It ran no lane tool, gate or selftest (§Gate standard, Closure consequence). It made no host mutation.
It made read-only host observations for the host-safety check (§2.5): pacman.log, journal and `stat` without sudo.
It also re-opened one public URL (§3). Five read-only reviewer seats ran inside this closure: C1BootRegistry,
C2BinderBehaviour, C3FreshnessRecheck, GatesEvidenceScope and HostSafetyWindow. This closure re-measured their key
figures itself, as marked below.

Driver digest (copied from mutable `.ufo/watchdog.log`, lines 502/513 at read time):

```text
2026-10-20T15:38:16-03:00 launch tsukuroi round=18 pgid=3024526 driver=hyaku-inline attempt=1
2026-10-20T17:29:03-03:00 complete tsukuroi round=18; hyaku-inline attempt=1
```

## 1. Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report landed by lane identity | `git log --format='%an %ae %H' -- .ufo/reports/round-18/tsukuroi.md` | one commit, `tsukuroi-shokunin tsukuroi@shokunin.local 0b469d1…`, 17:28:43 | pass |
| Report lands after the commits it cites | `git log -1 --format=%ci <h>` | latest cited lane commit c68945c is at 17:24:48, before the report at 17:28:43 | pass |
| `SHONEN` heading, one line per box | read report §SHONEN | 4 lines, all `[~]`, each with a pointer | pass |
| Cited hashes exist and are ancestors of the branch | `git merge-base --is-ancestor <h> refs/heads/master`, run on all 8 full hashes in the report plus cca3343 and 661020f | all are `commit` objects; all exit 0 | pass |
| Lane commit identity | `git log --format='%an <%ae>' 842a531..refs/heads/master \| sort \| uniq -c` | `6 tsukuroi-shokunin <tsukuroi@shokunin.local>` | pass |
| Each landing has a matching LOG entry | `grep -n round18 LOG.md` | six `## 2026-10-20 — round18 …` entries (951/955/960/971/982/989), matching the report's six rows | pass |
| Pushed, nothing uncommitted | `scripts/hyaku/jj-lane.sh state <lane>`; `git status --porcelain`; `git ls-remote origin refs/heads/master` | `local=remote=c68945c… ahead=0 behind=0 tracked=0 untracked=0`; porcelain empty; remote = c68945c | pass |
| Prompt carries template contract | `diff <(sed -n 1,140p .ufo/prompts/tsukuroi-round-18.md) kimi-shokunin/templates/round-prompt.md`; lines 141–335 vs `scripts/hyaku/lane-addendum.md`@46f7f2f (last change before the prompt commit bb44c29 at 15:38:14) | lines 1–140 differ only by `{{LANE}}/{{ROUND}}/{{FLEET_ROOT}}/{{AXES}}` substitutions. The tail differs only by placeholders (`LANE, ROUND, ATTEMPT, TARGET, LANE_CWD, FLEET_ROOT, CANON, PREV`). `grep -c` finds 7 report-path/SHONEN/L0 lines | pass |
| Godspeed and dispatch | Python over `build/dispatch.json` and `falsify/dispatch.json` | 81/81 and 76/76 tasks start with `/skill:godspeed\n\n` and hold the 429-byte directive (`db88963c…`) exactly once. 0 `model` params. Role mixes equal the report table | pass |
| Seat tally | `outcome.json` plus a named `.md` per dispatched seat | build: 81 dispatched, 80 reports, 1 dead. The dead seat is RerunExecLog (`provider invalid_prompt policy rejection on openai-codex/gpt-6-luna`, not replaced). Falsify: 76/76/0. Model receipts carry 81 and 76 unique ids | pass |
| Marker vs report | real hashes, LOG entries and measurements | real report | `ok` |
| Prior-round tail | report §"Correction of the previous report's uncited tail" | names cca3343/661020f and the 81/37/44 final r17 tally (r17 defect 1) | pass |

## 2. Claim re-check

Three declared claims: C1 depth, C2 operability, C3 freshness. None is exploratory. No capability row was added.
Ordinal deltas are 0 on every axis.

### 2.1 Re-measured (plain committed-byte measurements by this closure or its seats)

- **C1: 0 → 4 boot-chain statement corrections (r17 defect 3).**
  - Count at B:59. `git show 842a531:.ufo/waves/round-17/l1-capture/boot-chain-capture.txt | sed -n 59p` gives
    `pacman -Syu --needed --noconfirm nvme-cli smartmontools fio xfsprogs pacman-contrib earlyoom iotop-c sysstat
    stress-ng btrbk linux-lts linux-lts-headers`. That is **12** names. Baseline `boot-chain-r17.md:19` said "13 named
    packages".
  - B:115 is `omarchy_linux.efi_sha256_2e9c…` at 09:29:18 (the history copy). B:124 is the live `omarchy_linux.efi`
    at 09:26:22.
  - The TIP appends R18-CORR-01..04 (`boot-chain-r17.md:192-226`) against `statement-corrections-r18.json`, which
    holds 4 records:
    - CORR-01: 12 packages;
    - CORR-02: linux-lts init digest B:198 added;
    - CORR-03: hooks B:199-200 added;
    - CORR-04: live mtime at B:124, with history-copy SHA equality B:171/B:219.
  - Each was re-read against the capture lines (seat C1BootRegistry; CORR-01 and CORR-04 re-read by this closure).
  - Append-only: the 15,754 baseline bytes are an exact prefix of the 20,060 TIP bytes (+41/−0). `boot-chain-r17.json`
    is unchanged.
  - **Matches the report.**
- **SKILL.md:1833 (r17 defect 5): fixed, append-only.**
  - Baseline :1833 reads "Installed `mkinitcpio 41.1-1` with 42.2-1 pending".
  - The TIP appends NoticeSkill-06 (`SKILL.md:1927`), citing `host-capture-r18.txt:34`
    `/var/lib/pacman/local/mkinitcpio-42.2-1` (re-read). It keeps compatibility labelled untested.
  - The 168,208 baseline bytes of `SKILL.md` are an exact prefix of the TIP bytes (+87/−0).
- **Registry drift (r17 defect 4): fixed by a superseding table.**
  - The TIP adds `## Gate and probe registry — round18 superseding current rows` (`SKILL.md:1952-1970`, 13 rows). It
    says the old "53/44/five-tools/probe/23 and capability44 figures are not current assertions".
  - boot-chain is a gate, and counts are delegated to `measure/final/results.json` (83 PASS). boot-chain-audit is a
    probe (45). revision-binding is a gate over the original nine (52). recheck-commands names `--exec-log` and
    `EXEC-STEER-VIOLATION`.
  - `SCORECARD.md:554` supersedes the 44/44 capability cell (:164) with the measured 45/45 (:520).
  - `measure/final/operative-registry.json` states the selector: the unique highest-numbered complete table; old rows
    are historical, never a fallback.
- **C2: consistent 1 → 9, shared 0 → 9, local copies 9 → 0.**
  - `git grep -l merge-base <rev> -- tools/` finds 10 files at 842a531: the nine consumers plus the judge. At c68945c it
    finds `_revision.py`, the judge, and `check-root-dac-correction.py:540`, which is help text only.
  - `git grep -l -E '^\s*(import _revision|from _revision import)' c68945c -- tools/ | wc -l` gives **10**: the nine
    consumers plus the new appended-notices checker. At baseline it gives 0.
  - The judge `check-revision-binding.py` has no module import of `_revision` (string literals only). Its sha
    `cfce34a8…` is identical at c0f6303/07cc6ea/c68945c.
  - **Matches the report.**
- **C2 behaviour on the six r17 divergences (static read: BASE copies vs TIP `tools/_revision.py`; seat C2BinderBehaviour).**
  1. **Bad branch id.** BASE was mixed: `E-CLI`, `E-REVISION-INVALID`, or no check in three tools. TIP `:85-94` emits
     `E-BRANCH-INVALID`. Probes: branch-range, branch-slash, branch-space.
  2. **Precedence.** BASE was split: revision-first in freshness, recheck and seat-scope; branch-first in boot-chain
     and locator. TIP `:136` is branch-first. Probe: branch-first.
  3. **merge-base rc≥2.** Four tools read it as non-ancestry; five raised E-GIT-FAILED. TIP `:105-122` takes rc∈{0,1};
     anything else is E-GIT-FAILED, as S061 says (status not 1 = error). Probes: blob-revision, git-failed.
  4. **Double finding in root-dac.** BASE `:282-289` returned both NOT-LANDED and NOT-PUSHED. TIP returns exactly one
     finding. Probes: single-id, strict-refusals (`finding_count==1`).
  5. **Missing branch.** 8 of 9 tools said `E-REVISION-NOT-LANDED`. TIP `:143-145` emits `E-BRANCH-MISSING`, matching
     the judge contract. The exit-2 class is unchanged.
  6. **`a..b`/`a/` acceptance.** recheck and seat-scope regexes accepted these, and boot-chain allowed a trailing `/`.
     TIP `:41`, `:88-94` reject them, per S062. Probes: branch-range, branch-slash.

  On the accepted inputs (tip, landed parent, short tip, origin-absent), every consumer still binds `revision==tip`.
  No legitimate accept→refuse flip appears in the consumer diffs.

  The malformed-input finding ids changed on purpose. That change is disclosed in Gate row 1 and QUALITY28. It is not a
  domain-verdict change.
- **C3: 0 → 97 notices across 17 paths.** Python over `git show`:
  - `freshness-recheck-r18.json` is absent at 842a531.
  - At c68945c it has **97** records with 97 unique ids over **17** paths: 49 primary and 48 `SUPPLEMENT`.
  - For all 97, `notice_heading` is in TIP and not in BASE. 0 failures.
  - All 17 paths are append-only (`tip.startswith(base)`). 0 non-prefix files.
  - Every r17 defect-5 locus is targeted:
    - SKILL :118, :129-135, :1833;
    - journal-boot-plane :147-149, :364-365;
    - package-state, aur-risk and foreign-provenance planes;
    - oom-event and kill-event (earlyoom, zswap);
    - host-health-report-r3 U1.
  - Four sampled records (NoticeSkill-06, NoticeAur-01, SUPPLEMENT-13, SUPPLEMENT-47) are source-correct and bounded.
    For example, 1395 is called a local-DB directory count, not `pacman -Q`. 413 pending stays historical; no `-Qu`
    was run.
  - **Matches the report.**
- **Protected files.** `git diff --numstat 842a531 c68945c` is empty for `PROVINCE.md`, `SHONEN.md` and
  `corpus/lessons/*verifier*`. LOG.md +44/−0. QUALITY.md +3/−0 (items 28–30). SCORECARD.md +55/−0, append-only, with
  only a `## Round 18` section and no ordinal change.
- **Sources.** The `^| S…|` row count goes 59 → 65 (S060–S065). The only `-|` row is S058; its mutable `used-by` change
  is logged in the report and lesson.

### 2.2 Evidence-verified (lane-owned gates; not executed by this closure)

- **Selftests.** All 14 committed `measure/final/selftest-*.stdout` files report PASS at the counts the report gives.
  Recheck and seat-scope are the exceptions in that directory; they keep their initial reds (85/86 and 53/54, exit 1
  at c0f6303).
  - Their repairs are `measure/repair/` 86/86 and 54/54, exit 0 at 07cc6ea.
  - All stderr files are empty.
  - The `evaluator-digests.json` hashes match `git show <rev>:tools/X | sha256sum` for each run's revision. Twelve
    tools are byte-identical across c0f6303, 07cc6ea and c68945c.
  - The repair diff c0f6303 → 07cc6ea weakens no gate. The appended-notices checker is unchanged. Recheck now *also*
    requires `not unresolved` for clean. The seat-scope change only updates a selftest schema counter.
  - The C3 fix added five capture anchors in the corpus.
- **Census.** 97 PASS with exactly 2 explicit `SKIP` lines, neither labelled passed:
  - a non-root-owned fixture that needs CAP_CHOWN;
  - an EACCES fixture, since uid 0 bypasses DAC.
- **C1 gate.**
  - `c1-before` / `c1-actual-stale-baseline`: exit 1 at 842a531, 4 `STALE-UNFLAGGED`.
  - `c1-after`: exit 0, count 4 at c0f6303.
  - `repair/input-equality-and-history.json`: all 10 inputs are equal between c0f6303 and 07cc6ea, so the carry-forward
    holds.
- **C2 gate.**
  - `final/c2-before.stdout`: revision 842a531, consistent 1/9 (seat-scope only), consolidated 0, copies 9, exit 1.
  - `repair/c2-after.stdout`: revision 07cc6ea, `consistent_tools 9`, `consolidated_tools 9`,
    `local_rev_regex_copies 0`, `consolidation_status PASS`, exit 0.
  - Each tool passes all 18 probes. The extra tool (appended-notices) passes 1/1, reported separately.
- **C3 gate.** The baseline with the fixed registry gives 97 stale findings. The initial run was 92/97 (red, retained).
  `repair/c3-after.stdout` gives 97/97, exit 0, at 07cc6ea. That stdout is stored at c68945c, which is not a defect:
  the evidence was produced after the measured commit and ships in a later commit.
- **Recheck gate (r17 defect 6): `aur-risk-plane.md:347` is now covered.**
  - `final/recheck-aur-before.stdout` at BASE names `aur-risk-plane.md:347` `RECHECK-POINTER-UNRESOLVED`.
  - `tools/check-recheck-commands.py` (TIP, 369-457 and 490-559) resolves same-file §N/Appendix pointers and checks
    their commands. Advisory or missing targets fail. Traversal is one level.
  - The TIP appends a file-read-only R18 procedure at `aur-risk-plane.md:437-453`.
  - The repair run passes with that file resolved.
  - Whole-corpus result is `repair/recheck-all-after.stdout`: 37 files, 21 clean + 16 resolved, 0 findings.
    `final/recheck-all-after.stdout` keeps the pre-repair red (1 finding, degraded-triage).
- **Exec log.** `repair/exec-log-after.stdout` at 07cc6ea: `exec_violation_count 0`, PASS, 81 invocations. Its scope is
  the supplied `host-capture-r18.txt` only, which the lane states.
- **Declaration/scope gates: red, retained.** `seat-scope-build` exit 1: 37 `EXEC-UNAUTHORIZED`, 1 `REPORT-MISSING`
  (the dead seat), 4 `TRAILER-MALFORMED`, 2 `SCOPE-UNDECLARED`. `seat-scope-falsify` exit 1: 9 / 0 / 0 / 2. The counts
  are identical in `final/` and `repair/`.
  - A sweep of the build/falsify `Scope:` declarations found no pacman -S/-U/-R/-Syu, no mutating sudo/systemctl, no
    mkinitcpio/bootctl, and no `/boot` or `/etc` write.
  - Disclosed writes go to drafts or the seat's own report. Git mutations happened in temp clones.
  - **Ruling:** a conformance defect, status-neutral (§Gate standard). It is honestly disclosed and not relabelled
    green. No disclosed action contradicts the C1/C2/C3 measurements. A third consecutive round of seat-scope reds is
    routed (defect 1).
- **Registry home.** Rows exist at TIP `SKILL.md:1952-1970` for 13 of the 14 selftested tools. `tools/_revision.py`
  has only prose (`### Shared revision adapter`) even though its selftest is counted. It is a shared library, not a
  verdict gate, so this is minor (defect 2).

### 2.3 CritNoHarm disposition (the lane asked closure to rule)

The lane declined to annotate the old registry rows in place and appended a superseding highest-round table plus a
selector artifact. **Ruling: acceptable, not harm.**
- PROTOCOL §Evidence standard asks for a named appended correction, not a rewrite. The lane's protected-prefix
  invariant has been byte-verified for SKILL.md.
- The new table names every stale figure as non-current.
- Limitation: a reader who stops at the old rows (`SKILL.md:1893-1902`) gets no adjacent pointer. The cue comes after
  them, and an append-only file cannot place one before them. This is observed, not routed as a defect.

### 2.4 Per-axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| depth | improved | C1 re-measured 0 → 4. Every correction is checked against the capture lines. Append-only. No historical verdict changed |
| coverage | unchanged | no new ground; PROVINCE unchanged |
| operability | improved | C2 re-measured: copies 9 → 0, imports 0 → 10. Judge evidence 1/9 → 9/9. The six r17 divergences are uniform and probed; accepted-input behaviour is preserved |
| freshness | improved | C3 re-measured 97/97 across 17 paths, all append-only. The r17 defect-5 backlog is fully targeted. Sampled notices are source-bounded |
| calibration | unchanged | No calibration claim. Registry/capability drift is corrected by supersession (§2.3). The initial reds are retained honestly, and the declaration reds are disclosed. No new false count was found: zcode completion is at L3165, S061 is verbatim, and 13 operative rows hold. Nothing harmed |
| adjacency | unchanged | PROVINCE unchanged. The Mori pointer drift is reported to the sibling, not edited |

No axis harmed. All three claims verify. **Admitted.**

### 2.5 Host safety (read-only observation by this closure's seat)

- **pacman.log.** Nothing in the window 15:38:16–17:29:03 (`grep 2026-10-20T(1[56]:|17:[012])` → no matches). The last
  entry is zcode at 13:23:09.
- **Journal.** No system-unit stop, restart or reload in the window.
- **sudo in the window.** There were two kinds of sudo use. Neither was by tsukuroi and neither mutated anything:
  - 15:55 read-only `grep`/`find`/`head` from the fleet root;
  - 16:47–16:54 `sudo unshare -n` under the tabi lane harness.
- **/boot.** Child mtimes are unreadable without sudo. The journal shows `limine-snapper-sync … Updated:
  /boot/limine.conf` at 16:07:16 and 17:07:16. Both follow the hourly `snapper-cleanup` timer. This is host
  automation, not the round.
- **Lane-side checks.**
  - The sha256 of `capture-r18.sh` equals the capture header (`bfe32ba3…`). The script holds only read-only commands.
  - A grep of the whole round-18 tree for mutating commands finds only quoted, fixture or prose hits.
- **Verdict.** The round made no pacman transaction, service restart, boot-file write or tool install. The lane's claim
  is bounded, not exhaustive, and this closure agrees with that bound.

## 3. Discernment spot-check (Gate in `corpus/lessons/round-18.md`)

| Item | Gate decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S060 dated observations | admit as source, narrow scope | `l1-capture/host-capture-r18.txt`:1,17-18,25,34,76-77; `sha256sum capture-r18.sh` | agree | Script digest `bfe32ba3…` equals header line 1. Line 34 `mkinitcpio-42.2-1`, 17-18 `active`/`enabled`, 76-77 `home`/`root`, verbatim. The row's scope disclaims rollback, pressure and update clearance |
| Original-nine shared revision binding | admit | §2.1 grep/import census; `repair/c2-after.stdout` | agree | Re-measured 9 → 0 copies and 0 → 10 imports. All six divergences are probed |
| 97 current-use notices | admit, bounded | Python over `git show` (§2.1); 4 sampled records against captures | agree | 97/97 headings new and append-only. Samples are source-correct and do not claim pending state |
| "Current installed count remains 1394 after the morning upgrade" | reject | `host-capture-r18.txt:24-25` | agree | Line 25 is `1395` at 16:06; 1394 is a dated earlier capture |
| "Pending updates are now zero" | reject | `host-capture-r18.txt:40-48` and the script | agree | No `-Qu`/checkupdates ran. Core/extra sync DBs are dated 2026-10-17 |
| "Consolidating revision binding changes no behavior" | reject | BASE copies vs `_revision.py` (§2.1) | agree | The malformed-input ids really changed (missing branch: NOT-LANDED → E-BRANCH-MISSING; root-dac double finding → one) |
| "Change old registry cells in place" | reject proposal | `SKILL.md` BASE prefix check; `:1952-1970` | agree | An in-place edit breaks the verified protected prefix. Supersession plus a selector gives the same reader outcome, with the limit noted in §2.3 |

New `corpus/SOURCES.md` row re-opened:
- **S061** (https://git-scm.com/docs/git-merge-base, read 2026-10-20). Under `--is-ancestor` the page says verbatim:
  "Errors are signaled by a non-zero status that is not 1." (11 words, ≤25). The version panel "last updated in
  2.43.0 · 2.43.1 → 2.56.0 no changes" matches the row's `where`. Agree.
- **S065** (`l1-capture/pacman-events-r18.txt`). Event-capture line 43 (`HOST-L3095`) is verbatim “[ALPM] upgraded elephant (2.21.0-1 -> 2.22.1-1)”, and line 69 (`HOST-L3121`) is “[ALPM] transaction completed”, as the Gate quotes (≤25 words).
  Line 101 `HOST-L3165 … [ALPM] transaction completed` at 13:23:09 follows `installed zcode (3.16.2-1)` at line 100,
  so the row's "zcode installation/completion 13:23:09" is supported. Agree.

Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi`
→ exit 0. It prints eight W04 cross-scope duplicate-URL warnings (S038, S041, S042, S043, S044, S046, S049, S058), then
`tsukuroi ok …/corpus/SOURCES.md`. This is identical to the report's end state.

## 4. Trend verdicts

- **expansion: unchanged.** No entry is on new coverage-map ground and no capability row was added. Agree with the
  author.
- **quality: improved.**
  - Four source-correct boot corrections, verified against the capture bytes.
  - 97 bounded current-use notices close the whole r17 defect-5 backlog. They are append-only and sampled correct.
  - One shared binder removes six real divergences. The recheck gate now catches the pointer evasion that r17 routed.
  - No stale statement was introduced. The LEARNING `harmed` trigger was weighed and not applied: the known backlog is
    now noticed, not left unmarked.
- **discernment: improved.** The r17 outside routed defects became QUALITY28–30 with fixes that can fail: the baseline
  judge exits 1, mutants are killed, and initial main reds are retained. The rejected proposals are grounded (§3). This
  outside sample agrees with all 3 admits and 4 rejects sampled. The author correctly left the no-harm ruling to
  closure.

## 5. Routed defects (status-neutral; lane fixes next round)

1. **Seat-scope declaration gates red, third consecutive round.**
   - build81: 37 `EXEC-UNAUTHORIZED`, 1 missing, 4 malformed, 2 undeclared. falsify76: 9 / 0 / 0 / 2. Both at 07cc6ea.
   - Either authorize read-only inspection explicitly in the item text (`EXEC-AUTHORIZED`) for seats that need it, or
     dispatch no-execution seats with read/grep-only instructions.
   - Re-measure both waves at a landed hash. Do not authorize after the fact.
2. **`tools/_revision.py` has no registry row.** It has a counted selftest (39) but appears only in prose. Append a row
   to the operative table: kind library/probe, `--selftest`, write scope none. Or state explicitly that it is not a
   gate and drop it from the selftest tally.
3. **Exec-log scope.** `--exec-log` reads only `host-capture-r18.txt`. Zero violations is a bounded result, as the lane
   says. Next round, either bind the L1's other host-touching reads (the S065 pacman.log ranges) into the same
   harness-captured log, or keep stating the bound wherever the 0 is cited.
4. **L1 process deviations** (late canonical load order, shell text helpers): retained by the lane. Follow the load
   order first next round.
5. **Cross-lane (not tsukuroi):** Mori `PROVINCE:66` and `SKILL:318` point at outdated tsukuroi line ranges (current:
   ADJ-04 at PROVINCE:49, no-restart boundary at :28). Routed to mori by the orchestrator.
6. **Operator note (host, not lane):** `limine-snapper-sync` rewrites `/boot/limine.conf` hourly after
   snapper-cleanup (16:07:16, 17:07:16). That is expected automation, and it is a `/boot` write source that boot-chain
   audits should expect.

## 6. SHONEN note for the operator

All four boxes remain `[~]`:
- Box 3 (executable without oral context) still has no context-naive whole-SKILL retest.
- Box 4 (no cross-domain bleed) has PROVINCE unchanged and overlap findings reported. An external promotion verifier is
  still required.

The boxes are **not** fully checkable by a non-author from this round. No promotion signal. No `[x]` written.
