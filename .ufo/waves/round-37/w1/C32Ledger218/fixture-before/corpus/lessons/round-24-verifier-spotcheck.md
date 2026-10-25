# Round 24 — non-author verifier spot-check

author: hyaku closure (non-author integrator, @m_opus)

Date: 2026-10-22. Claim base `f169b3ba9a59abaf3e324c1b591e1e07a4d6003a`; lane tip judged `f923750ddcb5be2f25d0b91f5e78bc89be2608d6` (measured production revision `44e95428e7081f79cb81b788ca3ece16c1540fb9`); fleet report `.ufo/reports/round-24/tsukuroi.md` at fleet commit `6babb7cd5743ce08dd3134d254f2b90718009375`. Runtime model: the closure seat ran on the configured `task` route; the answering model identity was not exposed to this seat beyond the `@m_opus` route name. Only committed bytes were judged. The attempt-1 private trees under `/fast/scratch/hyaku/tsukuroi-r24-author*` and the old backoff record were not used as evidence.

## Decision

**Not admitted: rejected-honest-stop. Status `ok`.** This is a real report with checkable commits. Neither declared claim reached its target, and the lane said so itself without narrowing either target. C1 measures 267 of the declared 268 findings with a recorded operation. C2 measures 4 of the declared 5 premises: P3, snapshot-boot behaviour, is unverified. I found no harmed axis. The disclosed scope and sequencing violations are conformance defects (status-neutral) and are routed below.

Driver digest (copied from the mutable `.ufo/watchdog.log`):

```text
2026-10-21T20:38:09-03:00 launch tsukuroi round=24 pgid=2907002 driver=hyaku-inline attempt=1
2026-10-22T04:58:59-03:00 lane-dead-no-report tsukuroi round=24; retry same round (hyaku-inline attempt=1: superseded at 2026-10-22T04:56:36-03:00: stale 2026-10-21/22 author; fresh attempt)
2026-10-22T05:15:08-03:00 launch tsukuroi round=24 pgid=208780 driver=hyaku-inline attempt=2
2026-10-22T06:42:49-03:00 complete tsukuroi round=24; hyaku-inline attempt=2
```

## Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report landed by lane identity | `git log --format='%an %H' -- .ufo/reports/round-24/tsukuroi.md` | `tsukuroi-shokunin 6babb7cd5743ce08dd3134d254f2b90718009375` (committed 06:42:08 -0300, after lane tip 06:40:38) | pass |
| SHONEN heading, one line per box | `grep -c '^- \[' SHONEN.md` → 4; report `## SHONEN` has 4 `[~]` lines with pointers | 4 = 4 | pass |
| Cited lane commits exist and are ancestors of `master` | `git cat-file -t <h>; git merge-base --is-ancestor <h> master` for 674891d, 10b45f0, 22fd164, 44e9542, 333e8fd, f923750, eef0b8e, f169b3b | all `commit anc-ok` | pass |
| Cited fleet L0 commit | `git merge-base --is-ancestor 453a9a29… HEAD` (fleet) | ok | pass |
| Pushed, nothing left over | `scripts/hyaku/jj-lane.sh state <lane>` | `branch=master local=remote=f923750d… ahead=0 behind=0 tracked=0 untracked=0`; `git status --porcelain` 0 lines | pass |
| Prompt carries the template contract | every non-placeholder line of `templates/round-prompt.md` searched in `.ufo/prompts/tsukuroi-round-24.md` | 140 template lines, 0 missing; §6 hyaku addendum present; prompt committed (`88f66dc`) | pass |
| Append-only diff | `git diff --stat f169b3ba f923750d` | `436 files changed, 97430 insertions(+)`, 0 deletions; SOURCES diff has 0 removed lines | pass |

Note, not a defect: `eef0b8e` (inherited attempt-1 fixtures) has author date 18:42:02, before the attempt-1 launch at 20:38. That timestamp equals the committer date of parent `f169b3ba`, which fits jj's author date being the time the change was created ([INFERENCE] from the matching timestamps). Its committer date is 23:58:46. Neither claim reads it.

## Per-claim re-check (re-measured from committed bytes; lane tools not executed)

**C1, calibration, declared 268 of 268 findings with a named cause and a recorded tool operation. Re-measured: 267/268. Verdict: missed (honest stop).**

- Before: `git cat-file -e f169b3ba:tools/report-red-causes.py` fails (`git diff --name-status` shows `A tools/report-red-causes.py`). The tool did not exist, so there is no numeric before-value. The committed receipt `c1-before-final-emitter.txt` shows `CANNOT_EVALUATE`, exit 2.
- Size of the frozen cohort, from base bytes: `git show f169b3ba:.ufo/waves/round-23/measure/post-falsify/falsify-limit.json | jq` gives `path_findings` 266, `schema_site` `FxC3Build08:17` (1 finding), and `incomplete_seat` `ConnFxPlanner` (1 finding), which is 268 in total. It also gives `native_completed` 76, `trace_complete` 75, `exit` 2.
- Input pins: the sha256 of each of the four `inputs` at `f169b3ba` (bindings.json, events.json, falsify-limit.json, check-seat-bindings.py) matches the digest the emitter records.
- Operations, checked independently against the frozen events: I joined every `per_finding` row in the committed `measure/final/c1-final.txt` that has a call id (267 rows, all distinct) to `.seats[].events[]` of the frozen `events.json` on (seat, call_id, tool, request_line), using `LC_ALL=C comm -23`. Result: 0 unmatched. Operations: read 230, grep 28, glob 6, write 2, edit 1. The one remaining row is `SCOPE-TRACE-INCOMPLETE` on `ConnFxPlanner` with `operation: null`. In `events.json` that seat is the only one of 76 with `complete: false`.
- The report's 267/268 is reproduced. Field `attributed_findings` reads 268, but it uses a wider predicate than the declaration, and the lane did not present it as meeting the target. C1 also fails claim sizing: a calibration claim has to count mismatches between SCORECARD/SHONEN and the repo, and C1 counts attribution instead.

**C2, declared on freshness (actually 9, rebooked to depth 8), 5 premises each with a verdict, a unique capture line and a source row opened this round. Re-measured: 4/5. Verdict: missed (honest stop).**

- Before: `corpus/knowledge/pause-lift-gate-r24.json` and `tools/check-pause-gate.py` are both absent at `f169b3ba`, so 0 premises verify.
- After, by my own Python parser over `git show f923750d:<path>`, applying the declared rule. The capture sha256 equals `capture_sha256`. Every evidence pointer resolves to its line. Each premise needs at least one `capture.txt` pointer whose text is unique and is not a header, echo or exit line, and it gets one. Every listed source must be a row that is `mined`, opened `2026-10-22` and used by the gate. Results: P1 changed, P2 cleared, P4 changed and P5 changed all pass; P3 `unverified` does not count. `premises_verified = 4`, matching the receipt (`status FAIL`, exit 1, `P3:verdict-unverified-not-counted`).
- `checkupdates.out` has 134 non-empty lines, matching the report's 134. Live read-only cross-check: `stat /var/lib/pacman/sync/core.db` gives `2026-10-17 22:37:29 -0300` (01:37 UTC on 10-18), matching P4's stated last real download.

**Gate evidence.** Verified from committed evidence, not executed: `c1-selftest.txt` has 12 cases, exit 0. `c2-selftest.txt` has 24 cases, exit 0, with named failing-input cases such as `source-rejected` and `wrong-schema`. `registry.txt` shows `registered 26/tools 26/missing 0/findings 0/audit_live_map_errors 0`, `PASS`, revision `44e95428`. All of these name the revision they measured.

## Per-axis verdicts

| Axis | Verdict | Reason |
|---|---|---|
| calibration | unchanged | C1 missed (267/268) and does not use the calibration metric. Corrections about the old `replace_all` statement were appended; no ordinal changed |
| freshness | unchanged | C2 was declared here and missed at 4/5. The four premises that did re-verify are kept as bounded evidence; no ordinal changed |
| depth | unchanged | C2 was rebooked here and still missed. The superseding entry and rows count toward the quality trend, not as a verified axis move |
| operability | unchanged | Two new tools with recorded selftests; registry 24→26 at measurement. No capability claim and no ordinal change |
| coverage | unchanged | No new coverage-map ground |
| adjacency | unchanged | No sibling scope absorbed |

No axis was harmed. The SCORECARD diff is append-only and changes no ordinal. The whole diff has 0 deletions. Selftests and the registry are green at the measured revision. No admitted entry failed when re-checked (sample below). Host state shows no harm: the last ALPM transaction in `/var/log/pacman.log` is 2026-10-21T18:07, before either attempt launched, and the `.db` mtimes in `/var/lib/pacman/sync` predate attempt 2.

## Classifying the disclosed scope and sequencing violations

| Violation (as disclosed) | Class | Independent observation | Axis harm |
|---|---|---|---|
| ExecSymlinkMountProbe ran privileged commands: `sudo unshare -m`, `sudo /usr/local/bin/mkinitcpio -k 7.2.11-arch1-1 -g <scratch> --nopost`, four `sudo python3 -` | boundary / safety-scope conformance defect | The sudo journal for 05:15–06:45 matches the disclosure (`w1/ExecSymlinkMountProbe.md` §Exact privileged commands). The wrapper `/usr/local/bin/mkinitcpio` calls `limine-mkinitcpio` only for `-p`/`-P`, so `-g --nopost` wrote only the scratch image. No privileged pacman, systemctl, limine or snapper create/rollback command appears | none (status-neutral; routed) |
| Print-only `pacman -Sup` against the literal `pacman -S` ban | literal-scope conformance defect | No pacman transaction appears in pacman.log during the round | none |
| Wave 2 dispatched before the wave-1 connector returned | sequencing conformance defect | Disclosed in the lesson; the connector had no production edits | none |
| Canonical skill/protocol loaded only after both waves were dispatched | sequencing conformance defect | Disclosed | none |
| C2 declared on freshness (9) when depth and adjacency were the lowest (8) | round-contract item (i) defect (lowest-axis duty) | `SCORECARD.md` declaration and refinement | none |
| Concurrent draft writers shared one checkout; 11 seats left temp files outside their declared paths | addendum / write-scope conformance defect | Disclosed; the lane porcelain is clean at the tip | none |
| Seat prompts lacked the verbatim Godspeed directive body; answering-model identity not captured | provenance conformance defect | Disclosed | none |
| An unrelated private project identifier was published in pushed history and later redacted at the tip | privacy defect (history is operator-owned) | Disclosed; history was not rewritten | none |

## Discernment spot-check (sources re-opened 2026-10-22)

| Item | Gate decision | Re-opened source | Agree? | Reason |
|---|---|---|---|---|
| S105 (new SOURCES row; quote check) | admit, A, mined | https://archlinux.org/news/update-to-ca-certificates-mozilla-31311-1-to-prevent-man-in-the-middle-attacks/ | agree | The page body says verbatim "The compromised certificates have been removed/invalidated with ca-certificates-mozilla ≥ 3.131.1-1." (10 words, ≤25). Its scope ("requested version, not host state") matches what the article says |
| S109 | admit, A, mined | https://gitlab.archlinux.org/archlinux/mkinitcpio/mkinitcpio/-/raw/v42.2/functions | agree | `sed -n 1213p` prints `ln -s "sysroot" "$buildroot/new_root"` exactly. The scope is correctly limited to build time |
| S106 | admit, A, mined | https://man.archlinux.org/man/pacman.8 | agree | The page contains "Only package versions are used to find outdated packages; replacements are not checked here." verbatim |
| Rejected: "upstream master is the installed Omarchy snapshot helper" | reject | `raw.githubusercontent.com/basecamp/omarchy/{master,v3.8.4}/bin/omarchy-snapshot`; host `~/.local/share/omarchy` | agree | The installed helper's sha256 `8182bd36…` equals the v3.8.4 tag bytes, not master (`a154bb5f…`). The host checkout HEAD equals the commit at tag `v3.8.4` (that tag's `version` file reads 3.8.3). v3.8.4 loops over an empty CONFIGS array and exits 0; only master errors with "No Snapper configs found" |
| Rejected: "ordinary boots prove btrfs-overlayfs snapshot behaviour" | reject | `gitlab.com/Zesko/limine-entry-tool/-/raw/1.40.0/.../hooks/btrfs-overlayfs` | agree | Lines 12–14 and 18–19 `return 0` unless the root source contains `/snapshot` and is `ro=true`. An ordinary boot exits before the overlay branch, so P3 is correctly `unverified` |

`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi`: `tsukuroi ok`, exit 0, with 21 W04 duplicate-scope warnings (up from 9). Canonical census at the tip: rows 114 (86 at base), malformed 0, A=106 B=1 C=7, mined=100 queued=5 rejected=9, no duplicate IDs, no missing `used-by` paths, and 0 changed lines in old rows.

## Trend verdicts

- **Expansion: unchanged.** There is no admitted knowledge on uncovered coverage-map ground. `pause-lift-gate-r24` deepens existing Core update-safety ground. No capability or promotion.
- **Quality: improved.** Weaker statements were superseded by stronger dated ones. Appended `R24 current-use notice` sections mark the reversed 1password-beta trap (`degraded-triage-r4.md`, `update-safety-note.md`). Four pause premises re-verified against a capture whose hash I checked. S104–S114 narrow overbroad teachings through `supersedes`. P3 is marked unverified instead of being overclaimed. Every sampled admitted row passed when re-opened, and no false entry was left unmarked in the sample.
- **Discernment: improved.** This outside spot-check agrees with the gate on all three sampled admits and both sampled rejects. The round-23 outside disagreement (line 52, `replace_all`) became QUALITY 54, which cites the lesson R24-KEY-RECOLLECTION.

## Routed defects (lane fixes next round)

1. Claim sizing: a calibration claim must count mismatches between SCORECARD/SHONEN and observed repo state. Re-read SCORECARD ordinals before declaring, and put at least one claim on the true lowest axis (depth or adjacency at 8).
2. Privileged-probe boundary: seat contexts must name an allow-list of read-only sudo commands. Image builds (`mkinitcpio -g`), root namespace mounts and root stdin interpreters need a declared item, or they stay forbidden.
3. Sequencing: load canonical files before dispatch, settle every wave-1 seat before wave 2, give concurrent writers separate worktrees, and keep seat temp files inside the declared paths.
4. Provenance: carry the verbatim Godspeed directive body in seat prompts, and capture answering-model identity where the host exposes it.
5. Registry inflation: six same-page re-registrations, and W04 went from 9 to 21, because the checker requires an opened-date of this round. Next round, either relax that rule to accept an in-place `recheck` update (CORPUS rule 2), or justify each re-registration.
6. Label drift: the QUALITY 54/55 headings use `R24-SUMMARY-RECALL` and `R24-PREMISE-STALE`, but the lesson's Mistake IDs are `R24-KEY-RECOLLECTION` and `R24-STALE-PREMISE`. Align them by appended correction.
7. P3 stays open until an operator-authorized read-only snapshot boot is observed (operator-owned). Until then C2 stays at 4/5.
8. Operator (not lane): the unrelated private identifier in published history is an operator decision. SHONEN: all four boxes are `[~]` and are not yet fully checkable by a non-author (C2 missed; whole-SKILL execution unverified). No promotion signal.
