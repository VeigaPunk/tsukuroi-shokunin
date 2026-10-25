# Round 17 — verifier spot-check (non-author)

author: hyaku closure (non-author integrator, @m_opus)

Date: 2026-10-20. Lane-round: tsukuroi r17. Lane HEAD before `6923fe0bd3add04fc90f3bc3522895b27cf44bbe`,
after `661020f077f510e5ec3bc8d3799fecda2e9125bc`. Report: fleet `.ufo/reports/round-17/tsukuroi.md`, judged at its
final bytes (main `df689518b613ae43bdc38ac6c0c41e82ffca5f6d`, addenda `fc05a552a5140a55d3642fcbd90f52740492aaf5`,
`e8645e94c991491da5b8e708d9327f51deab3998`). This closure did not author the round. It edits no lane-authored file
and writes only this file and the MANIFEST closure entry. It touched no host surface: no sudo, pacman, `/boot`,
`/sys` or journal reads. Every check below reads committed bytes, plus three public upstream URLs (§3).

Driver digest (copied from mutable `.ufo/watchdog.log`, lines 491/498 at read time):

```text
2026-10-20T12:29:53-03:00 launch tsukuroi round=17 pgid=1943783 driver=hyaku-inline attempt=1
2026-10-20T15:25:10-03:00 complete tsukuroi round=17; hyaku-inline attempt=1
```

## 1. Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report landed by lane identity | `git log --format='%an %ae %H %ad' -- .ufo/reports/round-17/tsukuroi.md` | 3 commits by `tsukuroi-shokunin tsukuroi@shokunin.local`: df68951 14:44:08, fc05a55 14:56:21, e8645e9 15:06:57 | pass |
| Each report revision lands after the commits it cites | `git log -1 --format=%ci <h>` (lane) | dd15c18 13:55:01, 90037c2 14:34:30, c53adee 14:43:15 < df68951; ed2ddd4 14:56:07 < fc05a55; 3bce4d7 15:06:38 and 119d8bf 15:06:55 < e8645e9 | pass |
| `SHONEN` heading, one line per box | read report §SHONEN | 4 lines, all `[~]`, each with a pointer | pass |
| Cited lane hashes exist and are ancestors of the branch | `git merge-base --is-ancestor <h> refs/heads/master` for dd15c18, 90037c2, c53adee, ed2ddd4, 3bce4d7 | all exit 0, all `commit` objects | pass |
| Cited fleet L0 hashes | `git merge-base --is-ancestor <h> HEAD` (fleet) for ac792a7, 6fe9984, f92afc1, 6a5c8bc | all exit 0 (12:34:38, 13:02:50, 14:25:35, 14:25:43) | pass |
| Lane commit identity | `git log --format='%an <%ae>' 6923fe0..661020f \| sort \| uniq -c` | `8 tsukuroi-shokunin <tsukuroi@shokunin.local>` | pass |
| Pushed, nothing uncommitted | `scripts/hyaku/jj-lane.sh state <lane>`; `git status --porcelain`; `git ls-remote origin refs/heads/master` | `ahead=0 behind=0 tracked=0 untracked=0`; porcelain empty; remote = local = 661020f | pass |
| Prompt carries template contract | `diff <(sed -n 1,140p .ufo/prompts/tsukuroi-round-17.md) kimi-shokunin/templates/round-prompt.md`; tail vs `scripts/hyaku/lane-addendum.md`@b8afbd0 (last change before the prompt commit c68f001 12:29:51) | only `{{LANE}}/{{ROUND}}/{{FLEET_ROOT}}/{{AXES}}` substitutions in 1–140; the §6 addendum differs only in placeholders; child-lane items grep-present (report path ×3, SHONEN, commit-then-push, hash rule, write scope, L0 ×3) | pass (route-map note: defect 10) |
| Prompt committed | `git log -- .ufo/prompts/tsukuroi-round-17.md` | c68f001 by tsukuroi-shokunin | pass |
| Marker vs report | report names real committed hashes with LOG entries and measurements | real report | `ok` |
| Report covers the final tip | `git log --oneline 3bce4d7..661020f` | 119d8bf (named in addendum 2), cca3343 15:17 and 661020f 15:23 land **after** the last addendum. They hold the used-by correction, the late FxMdJsonAgree, FxSourcesContract and FxSimplifyBind reports, and the C3 docstring/plan. None is cited in the report. | defect 1 (status-neutral) |

## 2. Claim re-check

Three declared claims: C1 depth, C2 freshness, C3 operability. The capability `boot-chain-audit` sits inside C1.
None is exploratory.

### Re-measured (plain committed-byte measurements, run by this closure)

- **C1 0 → 5.** `git cat-file -e 6923fe0:corpus/knowledge/boot-chain-r17.json` → absent.
  At 661020f, `jq '.entries[]'` gives 6 entries. 5 carry a kernel verdict: BOOTED-OBSERVED, UNTESTED,
  PATH-ALIASED-EMULATED ×2, CONSISTENT-PRE42. The sixth is NOT-A-KERNEL-ENTRY. **Matches the report.** Every JSON
  sha256/verdict equals `l1-capture/audit-live.txt:5-10`. The audit digest `495750fb…` in that file's header equals
  `git show 90037c2:tools/boot-chain-audit.sh | sha256sum` (and 661020f), so the live run used the shipped tool.
- **Priority claim (next-boot safety), re-derived from the captures:**
  - The default entry was booted: `supplement-capture.txt:113` `LoaderEntrySelected… Omarchy.linux`.
    `/boot/EFI/Linux/omarchy_linux.efi` has mtime 09:26:22 (`boot-chain-capture.txt:124`), before boot 0 at 09:57:09.
    Its sha256 `2e9c9bdc…` is VERSION 42.2 with 7 `/sysroot` and 0 `/new_root` refs (B:171-175).
  - In 42.2 images `new_root` is typed `lrwxrwxrwx new_root -> sysroot` in all four 42.2 trees. The 41.1 tree has a
    directory instead (`overlay-emulation.txt:51-66`; mkinitcpio `functions:1212-1213` `ln -s "sysroot"` at E:9-10).
  - The namespace emulation (E:23-48) runs `findmnt --mountpoint`, `mount --move` and the overlay mount through the
    symlink. It ends with `sysroot FSTYPE=[overlay]`. E:2 states its limits (tmpfs stands in for btrfs, user
    namespace, no boot test).
  - Upstream v42.2 `init` (re-opened, §3) mounts at `/sysroot` (66-67) and checks
    `stat -c %D / != stat -c %D /sysroot` (77) before `switch_root /sysroot` (110). An overlay mounted through
    `/new_root` passes that check. So PATH-ALIASED-EMULATED is a sound, honestly scoped verdict. It is not a boot test.
  - The first L0 line (`ac792a7`) is wrong as the lane says. Its correction is `6fe9984` (+28 min). The erratum
    `f92afc1` and the precision note `6a5c8bc` follow. The withdrawn hook-override option was not applied to the image:
    the default UKI hash is unchanged from 09:26 (B:124/171) to the 14:29 live audit (audit-live:5).
- **C2 0 → 48.** Python over `git show`: `freshness-recheck-r17.json` has 48 records with 48 unique ids over six
  files. For **every** record:
  - `baseline_quote` ∈ the baseline (6923fe0) bytes;
  - `notice_heading` ∉ the baseline and ∈ 661020f;
  - `capture_quote` ∈ the cited capture line;
  - the baseline quote is still present after.

  Failing records: `[]`. All six files are append-only (`after.startswith(baseline)`), with 0 → 1/2/5/2/2/1 `## R17-`
  headings. **Matches the report.**
- **C3 legacy 0/5 → 5/5, all 0/9 → 9/9 (marker census).** I grepped the nine `--revision` tools at both revisions for
  binding markers (`branch_tip`, `NOT-LANDED`, `NOT-PUSHED`, `{7,64}` hex rule, `merge-base`, origin ref):
  - 6923fe0: the five legacy tools carry 0 of these markers; the four new tools are absent.
  - 661020f: all nine carry all six marker classes.

  This is a presence census, not behaviour. Behaviour rests on the evidence below.
- **Recheck frontier 5 → 0.**
  - At 6923fe0, 7 knowledge files have a `recheck:` line mentioning pacman. The gate's 5 are the last-line backticked
    invocations: driver-firmware:268, foreign-provenance:313, initramfs-v42:3, package-state:328, snapper-eacces:3.
  - Of the other two: `pacnew-plane.md:3` names no invocation, and `aur-risk-plane.md` has its last `recheck:` at :347,
    which points to the §7 pacman probes (defect 6).
  - At 661020f the five files carry 6 `## R17-RECHECK` blocks.
- **Sources.** Rows 50 → 59 (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`), S051–S059. The only `-|` rows are
  S015/S016/S021/S022 (mutable `used-by`, logged in the lesson) plus late used-by fixes to this round's own S051/S055/S056.
- **Protected files.** `git diff --stat 6923fe0 661020f -- PROVINCE.md SHONEN.md 'corpus/lessons/*verifier*'` is empty.
  The only removed SKILL.md line is re-added byte-identical with a trailing newline.
- **SCORECARD.** `git diff … -- SCORECARD.md` is append-only: one capability row plus the `## Round 17` section.
  No ordinal changed (depth 8→8, freshness 9→9, operability 9→9).
- **Wave-2 final tally** (committed bytes, not the report's interim numbers): `falsify/dispatch.json` 81 tasks,
  37 `Fx*.md` reports and 44 dead.
  - Delivered: 29 at 14:43, plus 8 late (FxBindSectCita, FxC2Rerun, FxConnUnknowns, FxMdJsonAgree, FxOwnS055,
    FxSimplifyBind, FxSourcesContract, FxSteerScopeFix).
  - Dead: 36 on 429, plus 8 late (FxBindSourScopCorr, FxFreshUpdaSafeV3, FxFrozenMarker, FxReadmeFrontier,
    FxRecheckRerun, FxRevengerSnapperCopy, FxRevengerSwitchRoot, FxSeparability).
  - The brief's "39/43" does not reproduce from committed bytes.
- **Godspeed bytes.** Every task in `build/dispatch.json` (72) and `falsify/dispatch.json` (81) starts with
  `/skill:godspeed\n\n` followed by the 429-byte directive (sha256 `db88963c…`), and contains it exactly once: 72/72 and 81/81.
  Role tallies equal the report's table.

### Evidence-verified (lane-owned gates; not executed by this closure per §Gate standard, Closure consequence)

- `measure/final/` at 90037c2 against baseline 6923fe0 (`rc.txt`):
  - c1: 0 FAIL → 5 PASS (exit 1 → 0);
  - c2: 0 → 48 (1 → 0), and baseline-stale rc 1;
  - c3: legacy 0/5, all 0/9 → 5/5 and 9/9 (1 → 0);
  - recheck: 5 flagged → 0 (1 → 0).
- `measure/late/` at 3bce4d7: C1 5, C2 48, recheck 0 flagged / 5 resolved. The `--exec-log` run shows
  `EXEC-STEER-VIOLATION` ×1 at `exec-log.txt:5`, the real L1 `pacman -Q`.
- Selftests at 90037c2 (`measure/final/selftests.txt`): boot-chain 61, freshness 53, recheck 40, seat-scope 42,
  revision-binding 28, audit 45, all PASS. The 62 (boot-chain) and 43 (recheck `--exec-log`) tallies after the
  addenda are author-reported in the report/LOG only.
- C3 is not re-measured at the tip. `git diff 90037c2 661020f -- tools/` touches the binding code of none of the nine
  tools: boot-chain gets a witness change, recheck gets `--exec-log` plumbing, and the harness gets docstring only.
  So the 9/9 measured at 90037c2 carries to the tip [inf, code-read].
- Registry rows exist at the registry home (`SKILL.md:1897-1902`), but their counts drifted (defect 4).

### Per-axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| depth | improved | C1 re-measured 0→5. Every verdict re-derives from typed image facts and the firmware binding. The non-author reviewer seat BootChainTruthR17 found 4 low-severity statement defects outside the verdicts (defect 3). None changes a verdict, so not ruled harm. |
| coverage | unchanged | boot ground already held (README); no new ground |
| operability | improved | C3 marker census 0/9 → 9/9 plus gate evidence; steer-safe rechecks 5 → 0; `boot-chain-audit` demonstrated running (rc 0, 6 entries) with the shipped digest |
| freshness | improved | C2 re-measured 48/48 records valid and append-only. The known un-noticed backlog predates the round (09:15 upgrade); it is disclosed and planned (defect 5). |
| calibration | unchanged | Ruling on critic FxNoHarm's "harmed (residual)", below |
| adjacency | unchanged | PROVINCE unchanged; the sibling-overlap seat died on 429 (unverified, disclosed) |

**Calibration ruling.** FxNoHarm's residuals were repaired before the tip:
- the urgent L0 overreach got the named appended correction `6fe9984`, then the erratum `f92afc1` and `6a5c8bc`
  (PWD split, dkms 7.2.3, option (b) withdrawn);
- it was mined as R17-TYPE-BLIND and R17-L0-OVERCLAIM, with QUALITY25;
- the entry's [obs]/[inf] labels were repaired (3bce4d7).

At landing, no operator-facing false statement stands uncorrected. The round also added honest self-limits, such as
"exec-log is an L1 excerpt" and "9/9 holds on probed inputs". Against that, it left registry and capability counts
drifted (defect 4). Net: unchanged, not harmed. The author correctly declined to self-certify no-harm. This closure
makes that ruling.

No axis harmed. All three claims verify. **Admitted.**

## 3. Discernment spot-check (Gate in `corpus/lessons/round-17.md`)

| Item | Gate decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| `boot-chain-r17.md` + `.json` | admit | E:51-66, S:113-115, B:124,169-200, audit-live:5-12; upstream `raw/v42.2/init` lines 66-67/77/110; MR !482 via GitLab API | agree | Verdicts follow from typed facts and are scoped as emulation/inference. Four citation/count slips are routed (defect 3), and none affects a verdict. |
| 48 R17 freshness records | admit | `git show` baseline/after bytes and capture lines (Python, §2) | agree | 48/48 quote, notice and capture bindings hold; append-only |
| Five revision tools bound | admit | the nine tools at 6923fe0 and 661020f (marker census); `c3-before/after.json` per-probe outcomes | agree | `HEAD`/branch/unpushed are rejected after and accepted before. FxSimplifyBind's off-probe divergences are scoped out by the lane itself. |
| "snapshot #2 DEGRADED-PREDICTED, hook silently no-ops" | reject (withdrawn) | E:51-66 typed listing; E:9-10; MR !482 description; v42.2 init:77 | agree | `/new_root` is a symlink, and the hook's moves and overlay land on `/sysroot`, which passes init's mount check |
| "linux-lts is a fallback for a hook problem" | reject | B:182-184 vs B:198-200 | agree | init, btrfs-overlayfs and plymouth hashes are identical in both UKIs |
| "EFI fallback is an independent rescue path" | reject | S:93-95 | agree | `BOOTX64.EFI` sha256 `94308b4e…` = `limine_x64.efi` |
| "the 09:15 `-Syu` left 0 pending updates" | reject | F:10-14 | agree | no `-Qu` was run; core/extra sync DBs date to 2026-10-17 |

New `corpus/SOURCES.md` rows re-opened (all ≤25-word quotes, located):
- **S057:** the MR !482 API `description` contains “To avoid issues (or to at least try to avoid them), /new_root will be
  kept as a symlink to /sysroot.” (19 words, verbatim). Merge commit `00392d94…` and merged 2026-08-11T17:09:08Z match the row.
- **S058:** `curl …/raw/v42.2/init | grep -n sysroot` gives 66 `# Mount root at /sysroot` and 110
  `switch_root /sysroot`. Verbatim, at the cited lines.
- **S053:** the releases API v42 description line 5 is “Busybox-based init now uses /sysroot as the root mountpoint
  just like …”. v42.1 (2026-09-27) and v42.2 (2026-10-01) mention neither `new_root` nor `sysroot`, as the row's
  `teaches` says.
- **S059:** E:54 `lrwxrwxrwx new_root -> sysroot` sits under `[x-omarchy_linux-lts.efi]`. Verbatim.

All agree.

Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi`
→ exit 0. It prints eight W04 cross-scope duplicate-URL warnings (S038, S041, S042, S043, S044, S046, S049, S058),
then `tsukuroi ok …/corpus/SOURCES.md`. This is identical to the report's end state.

## 4. Trend verdicts

- **expansion: unchanged.** No knowledge entry is on uncovered coverage-map ground. The `boot-chain-audit` capability
  row widens the repertoire, but LEARNING's `improved` test is new-ground entries. Agree with the author.
- **quality: improved.** 48 stale current-use statements now carry validated append-only notices. Five pacman recheck
  procedures became steer-safe. S054/S055 are superseded by stronger S058/S059. The C1 gate now requires a typed
  witness.

  The LEARNING `harmed` trigger ("found stale and left unmarked") was weighed against the FxUnflagged* findings and not
  applied, for four reasons:
  - the staleness predates dispatch (09:15 upgrade);
  - the flagged lines are dated observations or dated round sections, true at their date;
  - the backlog is named file-by-file in the committed SCORECARD `planned` line;
  - the round introduced no stale statement.

  The SKILL.md:1833 sibling of a corrected fact is a Corrections-sweep defect (defect 5).
- **discernment: improved.** QUALITY27 turns the outside JjAuditTsukuroi R1/R2 into a gate (0/5 → 5/5). QUALITY24 is
  shown able to fail on the r16 closure's routed seat-scope defect. This outside sample agrees with the gate on all
  3 admits and 4 rejects sampled. The seat-found L0 error is mined, not credited. Agree.

## 5. Routed defects (status-neutral; lane fixes next round)

1. **Report does not cover the final tip.** cca3343 and 661020f landed after the last addendum and are uncited.
   `falsify/outcome.json` is frozen at 14:43 (29 delivered, 16 "still running"). The addendum lists FxGodspeedW2 as
   late, but it landed in c53adee. Record the final tally: 37 delivered and 44 dead of 81.
2. **C3 binding is copied, not shared.** FxSimplifyBind found six same-input divergences outside the probes: bad
   branch, check precedence, merge-base rc≥2, the double finding in root-dac, missing branch, and `a..b`/`a/`
   acceptance. The planned `tools/_revision.py` should add probes that fail on each one.
3. **boot-chain-r17.md statement fixes (named correction, appended).**
   - :19 says "13 named packages"; B:59 names 12.
   - :40-42 and :43-46 cite only the linux image for "both UKIs" equal to the installed init/hooks. Add B:198-200.
   - :88 says mtime 09:26:22 but cites B:115, which is the history copy at 09:29:18. The correct line is B:124.
4. **Registry and capability count drift.**
   - `SKILL.md:1897` boot-chain gives "53 cases"; the evidence says 61, and 62 is author-reported.
   - :1898 audit gives "44"; the evidence says 45.
   - :1902 revision-binding is listed as `probe` over "all five" with "23 cases". It is the C3 gate over nine tools with 28.
   - :1900 recheck-commands omits `--exec-log`/`EXEC-STEER-VIOLATION`.
   - SCORECARD capability row "44/44" contradicts the same file's 45/45.
5. **C2 backlog and Corrections sweep.** Un-noticed stale statements from FxUnflaggedBoot/Mem/Pkg/Skill:
   - SKILL.md:118, :129-135 and :1833. Line 1833 repeats "mkinitcpio 41.1-1 … 42.2-1 pending", the fact corrected
     by R17-FRESH-01.
   - journal-boot-plane.md:147-149, :364-365.
   - package-state, aur-risk and foreign-provenance planes; oom-event and kill-event (earlyoom, zswap).
   - host-health-report-r3 U1.

   Notice them as the SCORECARD `planned` line says.
6. **Recheck gate scope.** The gate reads backticked argv0 in the last `recheck:` line only. `aur-risk-plane.md:347`
   defers to the §7 `pacman -Qm/-Si/-Qmdtq` probes and stays green. Treat pointer procedures as invocations, or append
   an R17-RECHECK block.
7. **Steer breach R17-STEER-SCOPE.** The L1 ran a read-only `pacman -Q` despite "never run pacman"
   (`exec-log.txt:5`). It is disclosed and gated. The exec log is an L1-written excerpt, not a harness trace, so
   bind it to a harness-captured log.
8. **Seat scope.** `measure/final/seat-r17-build.json` gives 30 `SCOPE-EXEC-UNAUTHORIZED`, but lesson
   R17-SEAT-EXEC says 29. `seat-r17-falsify.json` gives 16. Both files are measured on `worktree`, not a named
   revision (§Gate standard, "Two evidences"). These are recorded deviations: reconcile the count, measure at a
   landed hash, and authorize or forbid execution in the item text.
9. **Unverified this round (429 deaths).** Separability, the README frontier supersession, the sibling-overlap check
   and the frozen-marker check got no outside attack. Re-attack them next falsify wave.
10. **Prompt route map (operator/protocol, not lane).** The §6 addendum quotes a role→alias routing map, and PROTOCOL
    step 1 requires a quoted route map to match the MISSION.md bucket. MISSION.md buckets roles into classes:
    connector is heavy-reasoning; critic, sentinel and reviewer are economy. The addendum routes connector→m_flash and
    critic/sentinel→m_opus. No alias→bucket mapping is published to reconcile the two. Routed to the
    orchestrator/protocol lane.

## 6. SHONEN note for the operator

All four boxes remain `[~]`:
- Box 3 (executable without oral context) has not been run by a context-naive agent.
- Box 4 (no cross-domain bleed) lost its seat to 429.

So the boxes are **not** fully checkable by a non-author from this round. No promotion signal. No `[x]` written.
Optional operator action, from the lane's open L0 rollback question: snapshot #1 is the only pre-42 image and may rotate out.
