# Round 92 lesson — tsukuroi lane

## Gate (sources opened this round; contract `CORPUS.md` §SOURCES.md)

Candidates opened 2026-11-08 by the L1 (URL, access date, located quote; ≤25 words each):

| row | URL opened | tier | located quote (≤25 words) |
|---|---|---|---|
| S377 | https://docs.python.org/3/using/cmdline.html#cmdoption-P | A | "python script.py command line: Don't prepend the script's directory." (`-P` entry; the `-I` entry adds "All PYTHON* environment variables are ignored, too.") |
| S378 | https://raw.githubusercontent.com/containers/bubblewrap/main/bwrap.xml | A | "--clearenv Unset all environment variables, except for PWD and any that are subsequently set by --setenv" |
| S379 | https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.6/common/lib/config.c | A | "if (p > config_addr) { *(p - 1) = '\0'; }" (raw 328-330, inside `create_menu_tree()`, raw 298-407) |
| S380 | https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.6/ChangeLog | A | "A config whose first line is an entry has had no global options since 12.9.5, whereas every option in it used to count as global." |
| S381 | https://github.com/Limine-Bootloader/Limine/issues/700 | C | "If the file starts with an entry, `p == config_addr`, so nothing is cut. Then global options work in all positions." |

Admitted: all five (S377/S378 support C1's launcher contract; S379/S380 support C2's era rule;
S381 is a community lead that corroborates S380 and is never sole support).

Rejected / refused this round:
- `https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.5/ChangeLog` as a separate row:
  rejected — the v12.9.6 ChangeLog carries the 12.9.5 entries too; one row (S380) is enough, the file
  stays pinned in `.ufo/waves/round-92/before/src/`.
- `https://man.archlinux.org/man/bwrap.1` as a separate row: rejected — same manual, a downstream
  rendering; the upstream `bwrap.xml` (S378) is the authoritative bytes.
- `https://docs.python.org/3.13/using/cmdline.html`: rejected — a version-pinned URL goes stale at the
  next Python release and would mislead a recheck; the version-less URL follows the current docs.
- issue #702 / NixOS discourse threads: leads, not opened this round; they stay in
  `corpus/SOURCES.md` §Leads if cited later.

Status changes this round: none in place; the five rows are new.

Spot-check result: the round-91 spot-check (§4 of `round-91-verifier-spotcheck.md`) agreed with the
r91 gate's admit and with its reject of the selftest-coverage claim; this round repeats the pattern —
its own non-author spot-check is the hyaku closure (`corpus/lessons/round-92-verifier-spotcheck.md`,
written by the closure, not by this lane).

## Mistakes

- **M1 (`landing`) — a round report cited a tip that four commits had already overtaken.** Class:
  `landing`. Evidence pointer: `corpus/lessons/round-91-verifier-spotcheck.md` §1 defect (a) and §6
  routed 1 — the r91 report cited `6d12e07f` while `20f65353`/`03b773e5`/`8a4826e9`/`71fc1b66` landed
  after it. Captured-by: `PROTOCOL.md` "A lane report lands last" (an existing rule that should have
  caught it) — no new criterion. Fix: this round's report is written only after the last lane commit,
  and the cited hash is re-derived with `git -C <lane> ls-remote origin refs/heads/master` and pasted
  into the report; shown able to fail: the check reads
  `git show <r91 report commit>:... ` ≠ `ls-remote` (mismatch) at r91 and equality at r92 —
  receipts in `.ufo/waves/round-92/after/m1-landing-check.txt`.
- **M2 (`vacuous`, self-found before filing) — a lying-control wrapper exec'd the reference gate by
  PATH, which the round's own isolation turns into a crash.** Class: `vacuous`. The battery's
  `--selftest` lie legs (`LIE_KINDS`) wrap the reference gate by running it; the first draft embedded
  the reference's absolute path, so under the r92 launcher the wrapper's child could not see it, every
  leg would have read `unmet` from `error:` rows, and the selftest would have been green for the wrong
  reason. Evidence pointer: `.ufo/waves/round-92/before/controls/m2-lie-wrapper-path.py` (the drafted
  form) against the landed `LIE_WRAPPER` (embeds `GATE_SRC`, writes it to the sandbox's `/tmp`).
  Captured-by: QUALITY 126 (`R88-CONTROL-PASSED-BY-CRASH`). Fix: the wrapper carries the reference's
  bytes, and the fix is shown able to fail — the path form yields `error` rows and reads `unmet` on the
  POSITIVE reference leg, the embedded form yields verdict rows and reads `met`
  (`.ufo/waves/round-92/after/m2-lie-wrapper-check.txt`).

- **M3 (`vacuous`, self-found by the before leg, before any candidate score) — the five channel
  controls were dead in both legs.** Class: `vacuous`. `make-controls.py` emitted `BATT = None` and a
  `find_oracle()` that was never called, so every control answered its constant fallback whether or not
  the launcher was in place: the channel-open leg read `0/82 unmet`, exactly the state a rejection
  looks like. Evidence pointer:
  `.ufo/waves/round-92/after/c1-controls/before-clone-dead-controls/summary.tsv` (the run) and
  `.ufo/plans/round-92.md` amendment A1 (the repair). Captured-by: none for this reading — QUALITY 126
  covers a control that crashes instead of judging, not one that never reaches its channel; this round
  adds QUALITY 133. Fix: `BATT = find_oracle()`, controls regenerated, freeze manifest regenerated; shown
  able to fail: the same controls now read `82/82 met` on the channel-open leg and `0/89` (0 error rows)
  under the launcher (`.ufo/waves/round-92/after/c1-controls/`).
- **M4 (`vacuous`, self-found by the before leg) — a wildcard picked a near-name module.** Class:
  `vacuous`/`attribution`. `K4-syspath` matched the first `limine-pin-battery-r*.py` on `sys.path`; in the
  clone that was the r87 battery, which has no `r1_key`, so the control crashed on all 984 rows
  (`bad-output`) and the before leg read `0/82` with 984 errors. Evidence:
  `.ufo/waves/round-92/after/c1-controls/before-clone/K4-syspath.json` (the crash rows) and
  `.ufo/waves/round-92/after/c1-controls/before-clone-fixed/K4-syspath.json` (the repair). Captured-by:
  none for the wildcard resolution — QUALITY 126 covers crashed rows, not why a control crashes; this
  round adds QUALITY 134. Fix: resolve the two frozen names explicitly; shown able to fail: the same
  control reads `82/82 met` on the channel-open leg and `0/89` (0 error rows) under the launcher.
- **M5 (`landing`, credential material in a committed receipt) — the isolation probe dumped the live
  environment.** Class: `landing` (secret material). My ExecIsolationProbe item asked it to "record
  `os.environ`" as an isolation channel; the seat did so literally and wrote 2 live 1Password
  service-account token lines into `w1/ExecIsolationProbe/probe-outside.txt` plus 2 more values in
  `w1/MutBattery/iso/iso-m1.json`. GitHub push protection refused the lane's push (GH013, path and line
  numbers in the error); the blob lived only in the unpushed commit `d1f6934f`. Evidence pointer:
  the GH013 text (quoted in the round report), the redacted files (`grep -c 'ops_[A-Za-z0-9_]\{20,\}'`
  → 0), and the re-landed commit `689623fd`. Captured-by: `CORPUS.md` "No credential material, ever"
  (an existing rule that fired only at the push), mado M56-17 (same class, r56) — no criterion covered
  an env-CHANNEL probe, so this round adds QUALITY 135. Fix: the value-free probe rule plus a
  seven-pattern redaction sweep with a rescan before every commit; shown able to fail: the GH013
  rejection is the red-before, the pushed blob's `grep -c` = 0 the green. VCS resolution (kasegi r94
  precedent): the unpushed revision was squashed into the working copy, which dropped it; no force push,
  no remote history rewrite.
- **M6 (`landing`, misroot) — an r91 seat's plan draft sat at the fleet root.** Class: `landing`. The
  pre-report sweep found `plans/round-91.md` (2630 B, 01:00, an older draft of the r91 narrowing
  amendment) untracked at the fleet root; the lane holds the final text at `.ufo/plans/round-91.md`
  (3381 B). Fix: copied byte-exact to `tsukuroi-shokunin/plans/round-91.md` (`cmp` identical), the fleet
  copy deleted; `.ufo/reports/round-83/souji.md` and `round-85/chousa.md` are other lanes' strays and were
  not touched.
## Wave summary

(pending WAVE-DONE)

## Wave summary

One v1 wave, 13 seats dispatched 2026-11-08 02:06 (4 executor, 2 critic, 2 reviewer, 2 mutation-tester,
1 scout, 1 scribe, 1 connector; 6 attack seats = 46%, one connector; no residual call). Dead seats: 0.

- **ReviewGate** (reviewer) — F1-F5: a 5000-digit version crashed `parse_limine_version` instead of rc 64
  (HIGH), leading-zero versions unpinned (MED), `--selftest` ran before the `bwrap` guard (MED), two
  selftest rows passed `tpm` as a truthy string, and the CLI description still said v12.9.4. All five are
  fixed in A3; its verification-of-correct section confirms the era logic, the `in_global` transition,
  the launcher, the error-row accounting and `--runs 3` independence by probe.
- **ExecIsolationProbe** (executor) — per-channel table through the frozen launcher: all five declared
  channels closed (`probe-inside.txt` vs `probe-outside.txt`); residuals named — `/proc/1/cmdline` argv
  and random path names, host fingerprint via `uname`/`/usr`/`/etc`, writable (transient) gate-copy parent
  dir, `/dev` writes (A6).
- **MutGate** (mutation-tester) — 12 killed / 8 survived of 20 held-out gate mutants. M02 (split at 12.9.6),
  M13 (first body line visible in era B) and M18 (era-B U1 restricted to the pre-cut text) are
  non-equivalent survivors proved by differential probes → A5; M07-M09 (refusal) are killed by
  `--usage-check`; M10/M11 are reporting-only.
- **MutBattery** (mutation-tester) — m1-m9 launcher mutants all leave the five controls at 0/89 with the
  honest gate at 89/89: the closure is the conjunction (private copy + file-only bind + `-I` +
  `--clearenv`), not any single element; the m0-open diagnostic (bind the lane `tools/` dir) restores
  K5/K6 → A7 §3.
- **CriticClaims** (critic) — §1 `0/89` is the fallback's property, not closure (a U1-aware fallback reads
  1/89); §4 the usage count was 8/8 vs 11 cases and "no verdict" was unasserted; §5 the manifest cannot
  bind itself; §6 K4's before leg was a crash. → A7 §1/§2/§4/§5.
- **CriticForgers** (critic) — five one-clause forgers killed; N01/N02 read `unmet` by crash
  (`IndentationError` in the bends) → A4; N04 survives the families and is killed by `--usage-check`.
- **ExecReplicate** (executor) — clean-room clone: gate 89/89 ×3, all five controls 0/89 ×3 with 0 error
  rows, before leg 82/82 (`w1/ExecReplicate/`).
- **ScoutUpstream** (scout) — host `limine 12.9.4-1`; no 12.9.7 (upstream HEAD is the v12.9.6 tag); no
  post-12.9.6 `config.c` commits; the three tagged files' hashes match the pins.
- **ConnectorOverlap** (connector) — 20 sibling repos, **0 conflicts**; kumitate owns orchestration-level
  seat isolation (adjacent, reported not absorbed); 103 sibling tools use dynamic imports (the same
  "subject can import the judge" class at fleet scale).
- **ScribeLesson** (scribe) — criteria 132-135 are taken by this round; redrafted the oracle criterion and
  the M2 row; the r91 draft's number was already used, which the round records rather than renumbers.
- **ExecLints** (executor) — lane gates: registry coverage, knowledge header/refs, line endings, census
  (receipts `w1/ExecLints/`).
- **ReviewSource** (reviewer) — pinned-source verification of the era rule (receipts `w1/ReviewSource/`).

Two seats' reports were still landing when this lesson was written; their receipt directories are the
evidence and the L1 integrated only what it re-read.
## Before → after

- Battery families: 82 (r91) → 89 (r92), +7 era families (ERA-FLE-PANIC-A/B, ERA-FLE-MEASURED-A/B,
  ERA-GLOBAL-KEY-A/B, ERA-DEFAULT); the launcher replaces `[sys.executable, gate, ...]` everywhere.
- Gate: `--limine-version X.Y.Z`, era-selected global-section scoping, `limine_version`/`visibility_era`
  fields, schema `tsukuroi-limine-pins-v3`, selftest 25 → 37 cases; `--usage-check` 11 cases.
- C1 measured: before `82/82 met` ×3 (K3/K5/K6/K7 `before-clone/`, K4 `before-clone-fixed/`), after
  `0/89 unmet` ×3 with 0 error rows in both layouts (`after-clone-final/`, `canonical-after-final/`);
  landed gate `89/89 met` ×3 both layouts.
- C2 measured: `89/89 met` ×3 canonical + clone at `35c1088b…`/`aef33925…`; `--usage-check` `met` 11/11
  both layouts; N01 87/89, N02 85/89, N03 88/89 `unmet` ×3 both layouts (0 error rows), N04 89/89 (limit)
  and `unmet` under `--usage-check`; refused versions print no JSON (`after/usage-stdout-check.txt`).
- Census: 376 → 381 `^tsukuroi` rows (5 new: S377-S381), exit 0 before and after; knowledge notes 108,
  header 108/108 clean; registry coverage 145/145; line-endings PASS (471 files).

## Frontier

- Landed: the oracle channel is closed and certified per channel (QUALITY 132, capability
  `battery-oracle-isolation`); the visibility rule is version-selected with the v12.9.5 boundary sourced
  (S377-S381, entry `knowledge/limine-r92-oracle-isolation.md`); the r91 frontier items "battery
  oracle-import channel", "freeze manifest does not pin the battery" and "selftest lacks V1/U1 coverage"
  are closed.
- Routed to round 93 (named limits, A5/A7): one family each for `--limine-version 12.9.5` (the exact
  boundary), the first body line after the cut in era B, and era-B U1; `N04-accept-any`'s family-level
  survival (`--usage-check` covers it); the launcher's argv/fingerprint/write residuals (A6); and the
  fleet-wide "subject can import the judge" class ConnectorOverlap counted in 103 sibling tools.
