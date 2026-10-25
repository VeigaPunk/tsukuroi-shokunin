# Round 37 — verifier spot-check (integrator, hyaku)

author: hyaku closure (non-author integrator, @m_opus)

Lane-round: tsukuroi round 37 (hyaku run 7). Base `564db0b614b2914de5452f9ebd537a0653ae1de5`, after
`c231d0bbc0aba3f9f1a08b588cd5a338d9c46e98`. Report `.ufo/reports/round-37/tsukuroi.md` (fleet repo),
prompt `.ufo/prompts/tsukuroi-round-37.md`. Closure date 2026-10-25. This file is the only lane path
the closure writes. No lane-authored file was edited.

Driver digest. Copied from the mutable `.ufo/watchdog.log`, lines 1390 and 1403:
`2026-10-25T15:56:14-03:00 launch tsukuroi round=37 pgid=3181823 driver=hyaku-inline attempt=1`;
`2026-10-25T16:59:19-03:00 complete tsukuroi round=37; hyaku-inline attempt=1`.

## 1. Step-1 conformance (re-run results)

| Check | Command | Observed | Result |
|---|---|---|---|
| Report committed by lane identity | `git log --format='%an %H %cI' -- .ufo/reports/round-37/tsukuroi.md` | `tsukuroi-shokunin 7c2442f9c0f6cae6dd557c2813a0b52c7c362e06 2026-10-25T16:58:44-03:00` | pass. Filed after its last cited commit `c231d0b` (16:56:49) and before the driver completion line (16:59:19). |
| SHONEN heading | read report `## SHONEN` | 4 lines, one per box, all `[~]` with evidence pointers | pass |
| Cited commits exist and are ancestors | every backticked hash in the report: `git rev-parse --verify` + `git merge-base --is-ancestor <h> master` | 22 distinct hashes, all resolve, all ancestors of `master` (the 19 round commits `083cd0c`…`c231d0b`, base `564db0b614`, operator commits `09045c5`, `f0b8f7a`) | pass |
| Lane pushed and clean | `scripts/hyaku/jj-lane.sh state …/tsukuroi-shokunin`; `git status --porcelain` | `branch=master local=c231d0bb… remote=c231d0bb… ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain empty; `ls-remote origin refs/heads/master` = `c231d0bb…` | pass |
| Prompt carries template contract | every one of the 140 lines of `kimi-shokunin/templates/round-prompt.md`: literal lines matched verbatim, placeholder lines matched by their fixed fragments | 0 missing lines. The hyaku addendum is §6 (`.ufo/prompts/tsukuroi-round-37.md:141` ff.) | pass |
| Fleet misroot | `git -C /home/vgpnk/Projects/shokunin status --porcelain` | no `corpus/` (the lane repaired it). Only `?? .ufo/waves/round-30/` (another lane's, untouched) plus driver/state files | pass |
| Gate registry rows | `SKILL.md` diff | `journalctl-v262-corrections-r37` (gate) and `child-env-allowlist-r37` (probe) rows added. The `self-assessment` gate row already existed | pass |

Conformance notes (status-neutral):
- The watchdog records one hyaku-inline attempt (`attempt=1`). The report's "attempt 2" is an L1 respawn inside that single dispatch: L1 `TsukuroiR37` filed no report and L1 `TsukuroiR37a2` filed this one. This is attribution only.
- The report says it "rejected 2 of 3 staged entries with flip conditions". Only `errno-name-discrimination-r25.md` carries a flip condition (`corpus/lessons/round-37.md:22`). The `mount-errno-contract-r26.md` rejection (`:74`) states a reason and no flip.

Status: real report with checkable work and pushed commits → **ok**.

## 2. Per-claim re-check (closure's own measurements at `c231d0b`)

### C1 (operability) — evidence-verified. NOT VERIFIED, as the lane filed.

- Freeze held. `git show 29b22df:tools/probe-child-env-allowlist-r37.py | sha256sum` and the same at `c231d0b` both give `9aee085b45d7566d6ce398733c10d3d87ae29bce107c4bd13fcdffcb4854b064`. Only `29b22df` touches the file in the round.
- Before receipt (committed). The last 3 lines of `.ufo/waves/round-37/before/v7-livefive-base.err` are `probe-child-env-allowlist-r36.py, line 499, in one_run` / `RuntimeError: cannot create local master branch`. This matches the report.
- After receipt (committed). The last line of `.ufo/waves/round-37/before/v8-livefive-baseline.jsonl` reads `targets 5, pairs 15, leaking 0, leaking_pairs [], harness_errors [], probe_version 8, probe_sha256 9aee085b…`. This matches the report.
- Sensitivity conjunct. The declaration requires "committed mutant probes (one per fix) each read above 0". `git ls-files .ufo/waves/round-37/ | grep -i mutant` lists no V8 per-fix mutant receipt; every hit is an assimilation or fixture copy of older rounds' files. So the conjunct is unmet.
- Kill evidence. `w1/C17S407/receipts/vb-derived-zero.jsonl` shows V-B2 (ambient PATH via `shutil.which`) scored `leaking 0, harness_errors [], exit 0`. That run used **V7** (`probe_version 7`, sha `a2a5acac…`), not V8. The V8 attribution rests on `emulated-fix-scan.txt` (`OS_AMBIENT | {'get_exec_path'} -> []`). I checked V8 line 795: `OS_AMBIENT = frozenset(('environ', 'environb', 'getenv', 'getenvb', 'get_exec_path'))`, the same set. The source-channel inference is therefore sound. No V8 dynamic-channel run on V-B2 exists.
- I did not run the probe, because it is a sibling's gate (§Gate standard, Closure consequence).
- Axis verdict: **operability unchanged**. The V8 direct mode does remove the S1 crash, but the declared discrimination after-state is unproven, and no ordinal moved.

### C2 (depth) — re-measured by plain reads plus upstream re-open. VERIFIED by closure, which disagrees with the author's post-wave downgrade.

Declared after-state (SCORECARD.md "Round 37 — declaration", C2) checked conjunct by conjunct at `c231d0b`:

| Conjunct | Closure measurement | Observed |
|---|---|---|
| exactly the corrected 15-term predicate | `curl -fsSL https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journalctl-filter.c` lines 26-42 | 15 OR terms (`arg_boot_filter` … `arg_pattern`). These are identical to the note's `### Predicate: 15 terms` list and to the 15 REJECT rows of the base decision table |
| `-n` row: `-F` truncation vs unchanged `-N` | read note `### -n: distinct observed outputs` | present. Two argv rows cite `ext_lines1_F` (2 bytes) and `ext_lines1_N` = `ext_plain_N` (2882 bytes, same sha) |
| action-override classification | read note `### Action replacement is not field enumeration`; upstream `journalctl.c` 805-814 and 958-960 | present and correct. `-F` sets `ACTION_LIST_FIELDS` (805-810), `--list-boots` later sets `ACTION_LIST_BOOTS` (812-814, matching the note's anchor), and the guard tests the final action |
| rejection line stays verbatim (the conjunct the counter does not assert) | `git diff --numstat 564db0b614 c231d0b -- corpus/knowledge/journalctl-v262-field-filter-r36.md` | `58 0`: pure append, 0 deleted lines, so the 84-byte rejection block is byte-unchanged |
| S199 quote | `curl …/systemd/v262/NEWS`, lines 129-130 | "journalctl now rejects -F/--field together with filters such as unit, boot, time, cursor or grep filters." present verbatim |

- Counter receipts, evidence-verified (committed json): `before/c2-before.json` gives 3 checked, 15 mismatches, FAIL at `564db0b6`. `after/c2-after-d621b7.json` and `attempt2/c2-at-a3cf2ef.json` give 0, PASS. `c2-selftest.json` gives 7 passed. All match the report.
- Why closure disagrees with "not verified":
  - The counter gap (rejection line) is closed by the plain diff above.
  - The C24ActionOverride12 order-dependence and `--list-boots --merge` findings are extensions beyond the declared conjunct. The note's rule "the later action won" already states the order-dependence. They are routed as depth debt (§6) and do not falsify the after-state.
  - The declaration has no kill rule that fires.
- Defects found (routed, §6):
  - (a) The round-37 correction block is appended **twice**: headings at note lines 129 and 158, introduced in `543a7ce` (`grep -c '^## Round 37 correction'` = 2 at every round commit). The blocks differ by one phrase.
  - (b) The counter was amended twice after the change commit (`718cc8f`, `d621b71`), and no freeze sha names its bytes.
- Axis verdict: **depth improved**. The round-36 false "16 terms" and the `--list-boots` misclassification are now corrected against the pinned upstream source. No ordinal moved, by the lane's choice.

### C3 (calibration) — re-measured (the 5 changed cells) plus evidence-verified (27-check receipts). VERIFIED by closure, which disagrees with the author's post-wave downgrade.

Closure re-derivation from committed trees (`git ls-tree` / `git show`, no checkout):

| Revision | knowledge notes (maxdepth 1) | SKILL `wc -l` | SKILL `^\|` lines | lesson files | README `wc -l` |
|---|---|---|---|---|---|
| base `564db0b6` tree | 56 | 3110 | 839 | 49 | 269 |
| base operative table (round-35, SCORECARD.md:1564-1575 at base) | 55 | 3009 | 784 | 46 | 256 |
| `29b22df`, `6dbfe32`, `a3cf2ef`, `c231d0b` tree | 58 | 3112 | 841 | 50 | 282 |
| final operative table ("round 37 final measured surface") | 58 | 3112 | 841 | 50 | 282 |

- Before: 5 of 5 cells mismatch (K07-K11). After: 0 mismatches at every revision from `29b22df` through the tip. This matches the report (5 → 0).
- Receipts `before/c3-before.json` (27/5/FAIL), `after/c3-after-29b22d.json`, `after/c3-final-6dbfe.json`, `attempt2/c3-at-a3cf2ef.json` and `after/c3-after-a3cf.json` (27/0/PASS) are committed and agree. The other 22 checks are evidence-verified only.
- On the author's separability downgrade: C3 is verifiable without C1 or C2 landing, because at the base counts the same table would verify. The coupling makes it a moving snapshot that must be re-stamped last. That is a design defect, routed in §6, and not a falsification of the frozen predicate `mismatches == 0 && checked == 27 && exit == 0`.
- Capability table: four evidence paths dropped mid-round are restored at `a3cf2ef` (SCORECARD "Capabilities — current full evidence set"). The net pointer set is not reduced.
- Axis verdict: **calibration improved**.

### Owned axes not claimed

`git diff 564db0b614 c231d0b -- SCORECARD.md` is 250 insertions and 0 deletions. Ordinals are unchanged (depth 8, coverage 9, operability 9, freshness 9, calibration 9, adjacency 8). The round adds two errno notes on existing frontier ground (README:38-42) and changes no census or tool file other than the two new tools. Verdicts: **coverage unchanged, freshness unchanged, adjacency unchanged**. No axis is harmed.

## 3. Discernment spot-check (LEARNING.md — from outside)

| Item | Gate decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S200 (mount(2)) → `mount-errno-contract-r37.md` | admit, tier A | https://man7.org/linux/man-pages/man2/mount.2.html (fetched 2026-10-25; footer "Linux man-pages 6.19 2026-02-11") | agree | The quote "Some filesystems instead return the error EROFS on an attempt to mount a read-only filesystem." is present verbatim (16 words). The note's EPERM/CAP_SYS_ADMIN line is scoped to mount(2), which is correct |
| S201 (btrfs ioctl.c v7.2) | admit, tier A | https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/btrfs/ioctl.c | agree | The quote is present across a comment wrap (`* are limited …`) at lines 1182-1186, inside the cited 1178-1186 range |
| S202-S205 → `errno-contract-variance-r37.md` (the admitted staged entry) | admit, tier A | errno(3) at man7 (6.19); `include/uapi/asm-generic/errno-base.h` at v7.2 | agree | All four quotes are present verbatim. `#define EACCES 13 /* Permission denied */` is present (tab-separated). The note carries `## QUALITY check` (line 35) |
| S206/S207 own-work | admit | `/home/vgpnk/Projects/shokuknow/lanes/tsukuroi/round9/host-errno-capture.txt:6`, `lane-errno13-probe.txt:3` | agree | Both quoted lines match byte-for-byte. Caveat: the anchor is a sibling-repo path, not a lane path (§6) |
| `mount-errno-contract-r26.md` (staged) | reject | the staged file in `shokuknow/merge/tsukuroi/…:28-46`; upstream `btrfs_mksubvol()` at v7.2 | agree | The staged entry says "The ioctls that change the filesystem require CAP_SYS_ADMIN and return EPERM without it" and maps EPERM to subvolume ops. At v7.2, `btrfs_mksubvol` gates on `may_create_dentry` (DAC → EACCES), and the source's own comment says "Subvolume creation is not restricted". So the entry would revive the round-12 CX2 refutation (`.ufo/waves/round-12/MatrixCritic.md:81`). The rejection lacks a flip condition (§6) |
| `errno-name-discrimination-r25.md` (staged) | reject | the staged file | agree | `grep -n QUALITY` returns 0 hits, so QUALITY 14 is unmet as the Gate says. I did not independently re-judge the overlap half of the reason |

New `corpus/SOURCES.md` row re-opened: **S200**. Its `teaches` cell is 16 words and its quote resolves on the live page, with the `ERRORS` anchor and revision present.

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` gives 33 W04 advisories (S203/S204 share the errno(3) URL across scopes) and `tsukuroi ok`, exit 0. Rows: 207 at the tip vs 199 at base, the diff is `13 0` (pure append), and malformed rows = 0. This matches the report.

Result: the closure agrees with every sampled admit (S200, S201, S202-S207) and both rejects.

## 4. Axis grades (closure)

| Axis | Verdict | Basis |
|---|---|---|
| operability | unchanged | C1 not verified: sensitivity conjunct undelivered; V-B2 kill evidence (V7 run plus V8-equivalent source-set emulation) |
| depth | improved | C2's four declared conjuncts re-measured true at `c231d0b`; predicate re-verified against upstream v262 |
| calibration | improved | C3's 5 re-derived cells: 5 → 0; 27-check receipts agree |
| coverage | unchanged | no new coverage surface; errno notes deepen existing frontier |
| freshness | unchanged | no recheck claim |
| adjacency | unchanged | no handoff change |

Admission: **not admitted**. C1 does not verify, and a round is admitted only if every claim verifies. No axis is harmed. Verdict: `rejected-honest-stop`. The lane filed C1 not verified on its own kill evidence. The closure upgrades C2 and C3 to verified on re-measurement, and that does not change the admission outcome.

## 5. Trend verdicts (closure)

- **expansion: unchanged.** Two admitted notes (`mount-errno-contract-r37.md`, `errno-contract-variance-r37.md`) sit on errno/snapshot ground the coverage map already held (README:38-42, as the lane's own README addendum says). There are no new coverage rows and no capability rows.
- **quality: improved.** A false admitted entry, the round-36 note ("16 terms"; `--list-boots` as field enumeration), is now marked and corrected against the pinned source. The closure re-opened that source. The stale self-assessment counts are re-measured. No admitted entry failed the closure's re-checks. The duplicate correction block is a blemish, not a falsehood.
- **discernment: improved.** The outside spot-check agrees with the Gate on the admits and both rejects (LEARNING.md "improved when").

## 6. Routed defects / next-round debts (owner: tsukuroi)

1. `corpus/knowledge/journalctl-v262-field-filter-r36.md` carries the round-37 correction block twice (lines 129-157 and 158-185, introduced by `543a7ce`). Append a named correction that marks the second block a duplicate (append-only; do not delete).
2. C2 counter `tools/check-journalctl-v262-corrections.py` has no freeze sha or kill rule, and was amended twice after the change commit (`718cc8f`, `d621b71`). Any re-claim must freeze the counter bytes and add the rejection-line-verbatim assertion.
3. Depth debt from C24ActionOverride12: the reverse order (`--list-boots -F` → field list) and the `--list-boots --merge` 60-byte error class (`journalctl.c:962-964`) are unrecorded.
4. C1 re-claim: deliver one committed V8 mutant per fix, each reading `leaking > 0`. Score V-B2 under **V8**, not V7. The `shutil.which` / `os.path.expandvars` ambient-PATH family needs a dynamic or value-provenance channel, because a name-level source set cannot see it.
5. C3 design: count cells coupled to same-round commits make a moving snapshot. Bind the calibration predicate to an explicit final measured revision declared up front, or exclude same-round-mutated counts.
6. The Gate rejection of `mount-errno-contract-r26.md` (`corpus/lessons/round-37.md:74`) lacks a flip condition, and the report says "with flip conditions" for both. Append a flip condition.
7. S206/S207 own-work anchors are sibling-repo paths (`shokuknow/lanes/tsukuroi/round9/…`). Commit the captures into the lane, or cite a re-runnable command.
8. Lesson Gate line 24 and line 105 still say "Non-author closure remains pending". This file answers them. The lane should cross-reference it next round.

## 7. Closure disposition

Status **ok**. Admitted **false** (`rejected-honest-stop`). Verdicts: operability unchanged, depth improved, calibration improved, coverage/freshness/adjacency unchanged. Trends: expansion unchanged, quality improved, discernment improved. SHONEN: boxes 1-2 (decision tables at SKILL.md:38-50 etc.; `corpus/knowledge/host-health-report-r3.md`) look checkable by a non-author from the cited evidence. Box 3 (whole-SKILL retest unexecuted) and box 4 (kaidoku/revenger ownership unruled) do not. Promotion is operator-owned.
