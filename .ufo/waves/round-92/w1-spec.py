#!/usr/bin/env python3
"""Compose the round-92 w1 wave spec (v1 policy, band 8-16) and validate it.

Roles: 6 attack seats (2 mutation-tester, 2 critic, 2 reviewer) of 13 = 46% >= 25%; one connector.
Every prompt leads with /skill:godspeed and the verbatim directive bytes (host rule).
"""
import json
import os
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
WAVE = os.path.join(LANE, ".ufo/waves/round-92")
SRC = os.path.join(WAVE, "before")
OUT = os.path.join(WAVE, "w1-spec.json")
GODSPEED = """To the operator reading this card: slow down. This is not a checklist.
Something breaks? Do not patch the symptom.
Maintain The Standard."""  # replaced below by the real bytes

D = "/home/vgpnk/Projects/ufo-fsd-alpha/scripts/ufo-swarm-wave.mjs"


def godspeed():
    for p in ("/home/vgpnk/.agents/skills/godspeed/directive.md",
              "/home/vgpnk/.omp/agent/skills/godspeed/directive.md"):
        if os.path.isfile(p):
            return open(p, encoding="utf-8").read().rstrip("\n")
    return None


GS = godspeed() or ""
if "Godspeed-enabled subagent" not in GS:
    # fall back to the bytes the r91 dispatch carried (verbatim from the skill's directive block)
    GS = ("/skill:godspeed\n\nYou are a Godspeed-enabled subagent.\n\n"
          "1. **Name the axes.**\n2. **Iterate cheap, in parallel.**\n"
          "3. **Keep moves that improve any axis and harm none.**\n"
          "4. **Don't aim — let the frontier walk itself.**\n\n"
          "## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in "
          "large batches. Do not serialize what can run in parallel. Do not output philosophical "
          "reasoning or verbose plans. Act directly via tool calls.")
elif not GS.startswith("/skill:godspeed"):
    GS = "/skill:godspeed\n\n" + GS

FREEZE = "da99b2f4bc442e5154a6c1da7350891c11ee7cb1"
GATE_H = "af90ae637222a21b5c098ceed289e29cd010a629df143c2fcd8d92539839c123"
BATT_H = "fde864ea29f1b61d9e8cdcb1063942e6c9b07bfdf81cec5766e804488542b166"

CONTEXT = GS + f"""

Tsukuroi round 92, wave w1 (13 seats). Lane root {LANE} (git branch master, jj-colocated); every
`Report:` trailer path the validator renders is relative to {LANE} — write it at {LANE}/<that path>.
Lane axes: operability + freshness (host operability and repair). Scratch: every clone/fixture/work
dir lives under /fast/scratch/hyaku/tsukuroi-r92/<YourSeat>/ (mkdir -p; TMPDIR there; delete it on
exit — a seat that leaves its tree behind reports that as its own defect). No hardcoded /tmp: `/tmp`
is for files under 50 MB only.

Freeze commit {FREEZE}. Instruments (do not edit them: they are frozen; a mutant or forgery is a COPY
under your seat dir):
- gate {LANE}/tools/check-limine-pins.py sha256 {GATE_H} (V2: `--limine-version X.Y.Z`, default 12.9.4)
- battery {LANE}/tools/limine-pin-battery-r92.py sha256 {BATT_H} (89 families; ISOLATION launcher)
- do-nothing battery {LANE}/tools/limine-pin-battery-r91.py sha256 655ee8f3… (82 families, no sandbox)
- freeze manifest {SRC}/freeze-manifest.sha256 (30 lines, `sha256sum -c` from the lane root)
- pinned sources {SRC}/src/ (v12.9.4/v12.9.5/v12.9.6 config.c, ChangeLogs, issue #700, bwrap.xml,
  python docs text)
- controls {SRC}/controls/: gates/K3-sibling.py K4-syspath.py K5-abspath.py K6-proc.py K7-env.py
  (C1 oracle channels), c2gates/N01-era-flat-a.py N02-era-flat-b.py N03-default-b.py
  N04-accept-any.py (C2 one-clause bends), run-controls.py (driver), make-controls.py,
  make-c2-gates.py (generators)
- declaration {LANE}/.ufo/plans/round-92.md and SCORECARD.md "Round 92 — declaration"

The two claims under attack:
C1 (operability) — under the ISOLATION launcher (gate bytes copied to a private directory holding
nothing else, run as `bwrap --unshare-all --die-with-parent --new-session --clearenv` with only /usr
and /etc ro, fresh /dev /proc /tmp, the case dir and the gate copy ro, cwd = case dir, `python3 -I`)
the landed gate reads 89/89 `met` x3 and each of the five channel controls reads `unmet` with 0/89
and 0 error rows x3 (canonical + clone); the same controls read 82/82 `met` against the r91 battery
in a clone.
C2 (depth) — the gate applies the visibility rule of the era `--limine-version` selects (before
12.9.5: the r91 first-line-is-entry exception; from 12.9.5: `create_menu_tree`'s in-place cut with no
exception), refuses versions outside X.Y.Z with rc 64, and passes all 89 families x3 both layouts.

Rules for every seat: you are read-only on the lane — write ONLY under
{LANE}/.ufo/waves/round-92/w1/<YourSeat>/ (receipts) or in your scratch clone. Never run git/jj
mutation commands in the lane (no add/commit/push/stash/checkout/reset, no `jj commit/new/describe/
squash/rebase/abandon/bookmark`); read-only git (`log`, `show`, `diff`, `status`, `rev-parse`,
`ls-remote`) is fine. Never edit MANIFEST.json, the fleet root, a sibling repo, `.ufo/state/`,
`.ufo/watchdog.log`, or the instruments above. No `sudo`, no write to /boot /efi /etc /usr /var, no
pacman/sysctl/limine/bootctl/efibootmgr/objcopy. Fixture repos: `D=$(mktemp -d)` under your scratch
root, `git -C "$D" init -q`, assert `git -C "$D" rev-parse --show-toplevel` = `$D` before any commit.
Never call the `ask` tool; never message `agent://all`. Tooling authorization (operator 2026-10-19):
you may install or upgrade a tool that helps the task — read /home/vgpnk/.omp/agent/RULES.md first
(official channels, update-safety gate; record tool/version/channel/reason in your report). pacman
transactions are PAUSED host-wide: install via `uv tool`/`npx`/official binary in ~/.local/bin, or
file the need in your report. Do not run builds, linters or test suites across the lane; run exactly
the commands your item names. End your report with a `## Verdict` line naming the claim(s) your
evidence supports or falsifies, with the receipts that prove it."""


def item(name, role, axes, body):
    return {"name": name, "role": role, "axes": axes,
            "prompt": GS + "\n\n" + role.upper() + " seat.\n" + body.strip() + "\n"}


ITEMS = [
    item("ExecReplicate", "executor", ["operability"], f"""
EXECUTOR — independent replication of C1's AFTER state. Receipts in {LANE}/.ufo/waves/round-92/w1/ExecReplicate/.
1. `git clone --shared {LANE} "$S/clone"` under /fast/scratch/hyaku/tsukuroi-r92/ExecReplicate; `git -C "$S/clone" log -1 --format=%H` (record it), and `sha256sum` the gate and the battery there; they must equal the freeze manifest lines.
2. In the clone, run the honest gate: `TMPDIR=$S/tmp python3 tools/limine-pin-battery-r92.py --gate tools/check-limine-pins.py --runs 3 --work $S/work --json $S/c1-gate.json` -> each run must print `families_passed 89/89 verdict met`.
3. In the clone, run the five channel controls twice — once with the r91 battery (before: each must read 82/82 met) and once with the r92 battery (after: each must read `unmet`, families_passed 0, and the JSON must carry 0 `error` rows):
   `TMPDIR=$S/tmp PYTHONPATH=$S/clone/tools python3 .ufo/waves/round-92/before/controls/run-controls.py --battery tools/limine-pin-battery-r91.py --gates .ufo/waves/round-92/before/controls/gates --runs 3 --jobs 5 --label before-clone --out $S/before`
   `TMPDIR=$S/tmp PYTHONPATH=$S/clone/tools python3 .ufo/waves/round-92/before/controls/run-controls.py --battery tools/limine-pin-battery-r92.py --gates .ufo/waves/round-92/before/controls/gates --runs 3 --jobs 5 --label after-clone --out $S/after`
4. Copy the whole `$S/before` and `$S/after` dirs into your receipts dir (they are small JSON+txt), write `<seat>.md` with the exact commands, the two summary tables and a verdict per claim clause.
Recipes that are slow: the isolated battery is ~2 min/run; run the five controls in parallel with `--jobs 5`."""),

    item("ExecReplicate2", "executor", ["depth"], f"""
EXECUTOR — independent replication of C2's AFTER state. Receipts in {LANE}/.ufo/waves/round-92/w1/ExecReplicate2/.
1. `git clone --shared {LANE} "$S/clone"` (scratch under /fast/scratch/hyaku/tsukuroi-r92/ExecReplicate2); record the commit and the gate/battery sha256.
2. `python3 tools/limine-pin-battery-r92.py --gate tools/check-limine-pins.py --runs 3 --work $S/w --json $S/c2-gate.json` in the clone -> 89/89 met in each of three runs.
3. `python3 tools/limine-pin-battery-r92.py --usage-check --gate tools/check-limine-pins.py --work $S/w` -> `verdict met` with 8 cases (12.9, abc, 12.9.6.1, "" -> rc 64; 12.9.4, 12.9.5, 13.0.0, absent -> rc 0).
4. The three near-misses, each x3, both layouts: `run-controls.py --battery tools/limine-pin-battery-r92.py --gates .ufo/waves/round-92/before/controls/c2gates --runs 3 --jobs 4 --label c2-near-miss --out $S/near`. Expected: N01 87/89, N02 86/89, N03 88/89 (unmet, 0 error rows); N04 reads 89/89 met — that survival is a NAMED LIMIT, not a defect: say so in your report and explain why (its families never send an out-of-range version).
5. Also run the do-nothing: in the clone `python3 tools/limine-pin-battery-r92.py --gate <clone>/tools/check-limine-pins.py` is the candidate; the do-nothing is `git show {FREEZE}^:tools/check-limine-pins.py > $S/r91-gate.py` then `--gate $S/r91-gate.py --runs 1` -> expect 0/89 with every row an `error:` (rc 64 per invocation); count the error rows and the rc values.
Write `<seat>.md` with commands, outputs and the per-clause verdict."""),

    item("ExecLints", "executor", ["operability"], f"""
EXECUTOR — the lane's own gates and selftests at the freeze tip. Receipts in {LANE}/.ufo/waves/round-92/w1/ExecLints/.
1. `cd {LANE} && python3 tools/check-limine-pins.py --selftest` -> record the tally (must be PASS 37/37) and the three new V1/U1 and four era rows.
2. `python3 tools/limine-pin-battery-r92.py --selftest --reference {LANE}/tools/check-limine-pins.py` -> record every leg (roster-literal, four negative gates, reference-gate, 12 lie legs). Any FAIL is a finding.
3. Registry + corpus checkers at {FREEZE}: `python3 tools/check-registry-coverage.py --revision {FREEZE}`, `python3 tools/check-knowledge-header.py --revision {FREEZE}`, `python3 tools/check-knowledge-refs-r68.py` (read each tool's `--help` first; use the spelling it accepts). Record pass counts and every finding.
4. `python3 tools/check-line-endings-r64.py --check` and `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` -> rc and the row count (must be 381 rows).
5. Report whether the SKILL.md registry row for `limine-pins` still matches the gate's real interface (entry command, verdict map 0/1/2/64, selftest spelling, pinned sources S350-S353/S361/S362/S374-S376/S379-S380); propose the exact one-line edit the L1 should make (do not edit SKILL.md yourself)."""),

    item("ExecIsolationProbe", "executor", ["operability"], f"""
EXECUTOR — measure the launcher's channels from inside (QUALITY 129: one probe per channel). Receipts in {LANE}/.ufo/waves/round-92/w1/ExecIsolationProbe/.
1. `python3 {LANE}/tools/limine-pin-battery-r92.py --isolation-check --work $S` -> record the JSON verbatim (root entries, cwd, sibling_files, lane_visible, battery_visible, env, pids, sys_path).
2. Write your own probe gate under $S (do NOT touch the lane): it must try, and record the outcome of each channel: (a) `os.listdir(os.path.dirname(__file__))`; (b) `import` of `limine_pin_battery_r92` after `sys.path.insert(0, ...)` of its own dir, of `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools`, and of `os.getcwd()`; (c) `open()` of the canonical lane battery path, of `$PWD/../tools/...`, and of `~/.cache/...`; (d) `/proc` listing, `/proc/1/cmdline`, `/proc/self/environ`; (e) `os.environ`; (f) whether the case directory contains anything but the conf and the ESP; (g) whether `/tmp` holds leftovers from a previous case. Run it through the frozen battery's launcher: easiest is to make your probe a "gate" and let `--gate` run it under `run_battery` — or copy `sandbox_argv` semantics by calling the battery's own function via `python3 -c` with `sys.path` on the lane tools dir; record which you did.
3. Run the same probe WITHOUT the sandbox (plain `python3 -I probe.py`) to show each channel's pre-change state.
4. Name every channel the launcher does NOT close (timing, behaviour, argv contents, fixture shape) and say whether the claim's wording covers it.
Write `<seat>.md` with the channel table: channel · inside the launcher · outside · closed/uncertified."""),

    item("MutBattery", "mutation-tester", ["operability"], f"""
MUTATION-TESTER — prove each element of the launcher is load-bearing. Receipts in {LANE}/.ufo/waves/round-92/w1/MutBattery/.
Copy `{LANE}/tools/limine-pin-battery-r92.py` to $S and emit mutants, each changing ONE element of the launcher: (m1) drop `--clearenv`; (m2) drop `--unshare-all` (keep the binds); (m3) drop `-I` from the inner python argv; (m4) skip `copy_gate` (run the gate in place); (m5) drop `--ro-bind <case> <case>`; (m6) drop `--unshare-pid` only (add `--share-net` to keep a valid combination if needed); (m7) keep the gate copy dir shared with the case dir; (m8) drop `--setenv HOME/TMPDIR`; (m9) run the *original* gate path as well as the copy (two bind points); (m10) drop the version pass-through (`--limine-version` never sent).
For each mutant measure BOTH: (a) the five channel controls under it (`run-controls.py --battery <mutant> --gates .ufo/waves/round-92/before/controls/gates --runs 1 --jobs 5`): a mutant that lets any control read more than 0/89 is DETECTED (state which control and which channel), and one that leaves all five at 0/89 is UNDETECTED; (b) the honest gate under it (`--gate .../check-limine-pins.py --runs 1`) must still be 89/89 — a mutant that breaks the honest gate is a broken mutant, not a killed one.
Write `<seat>.md` with a mutant x control matrix, the detected/undetected verdict per mutant and the element it proves. Do not edit the lane files; the mutants live in your scratch dir."""),

    item("MutGate", "mutation-tester", ["depth"], f"""
MUTATION-TESTER — held-out mutants of the V2 clause, aimed at the era branch and its edges. Receipts in {LANE}/.ufo/waves/round-92/w1/MutGate/.
Write at least 14 one-clause mutants of `{LANE}/tools/check-limine-pins.py` under $S (copy, never edit the lane): e.g. era split at 12.9.4 / at 12.9.6; era_b inverted; the era applied to `in_global` but not to `on_panic`; `--limine-version` accepted but ignored; default 12.9.6; `parse_limine_version` accepting `12.9` or `12`; `--limine-version` empty accepted; `visibility_era` string swapped; `limine_version` echoed wrong; the label-end cut applied one line early/late; the first-line exception kept in era B but only for `measured_boot`; the exception removed in era A; `on_panic` computed from the whole file in era B; U1 list computed on the pre-cut text in era B.
Measure each with `python3 {LANE}/tools/limine-pin-battery-r92.py --gate <mutant> --runs 1 --work $S/w` and record: killed (met != 89/89) with the failed families, or SURVIVED (89/89) — a survivor is a coverage gap and must be named that way. Also run the candidate gate as the positive control.
Write `<seat>.md` with the mutant table: mutant · family semantics · failed families · killed/survived · equivalent-or-gap judgment."""),

    item("CriticClaims", "critic", ["operability", "depth"], f"""
CRITIC — falsify the CLAIMS' WORDING, not their arithmetic (Amendment 59: the number re-deriving is necessary, not sufficient). Receipts in {LANE}/.ufo/waves/round-92/w1/CriticClaims/.
Read `{LANE}/.ufo/plans/round-92.md` and `{LANE}/SCORECARD.md` round-92 declaration. Then attack:
1. C1's "0 error rows" and "0 of 89 families passed": can a control reach `unmet` for a reason other than the closed channel (a fallback that would also fail on the unmodified lane, a crash counted as a verdict, a control that models nothing so its fallback is not evidence)? Read the control source and say which of its rows are verdict rows and which are not.
2. C1's launcher sentence: try to reach the battery from inside the sandbox through channels the wording does not name (argv, `/tmp` leftovers, `/proc/self`, the case dir, a second run's work dir, an inherited file descriptor). Write a probe or a gate that tries; report every channel that works.
3. C2's era sentence: is "before 12.9.5" the right boundary? Compile or diff the pinned v12.9.4/v12.9.5/v12.9.6 sources yourself (a scratch harness is fine) and say whether any config shape other than first-line-is-entry behaves differently between the eras — if one does, the battery roster is a coverage gap and the claim's wording is wider than the instrument.
4. The `--usage-check` clause: is rc 64 measured through the launcher, or is it the gate's own exit? Say exactly which bytes enforce it and whether `N04-accept-any` surviving the families leaves the clause uncertified by the counting command.
5. The kill rule: is `sha256sum -c` on the freeze manifest actually able to fail (try editing a copy in scratch and running the check against the copy)?
Write `<seat>.md` with one finding per item, each `falsifies-wording` / `falsifies-number` / `neutral-shaped` plus the artifact path, the exact sentence it touches, and the narrowing it would require."""),

    item("CriticForgers", "critic", ["depth"], f"""
CRITIC — forgery battery against the era families (discrimination, not isolation). Receipts in {LANE}/.ufo/waves/round-92/w1/CriticForgers/.
1. Write a docstring-only independent implementation of the gate's V2 rules (from the battery docstring's R1-R10, V1, V2, U1 text, without importing the battery or the gate) and run it under the frozen battery: it should read 89/89 — if it does, that is the battery's honest-floor evidence; if it does not, name which rule text is ambiguous and where the docstring and the battery oracle disagree.
2. Write one-clause forgers for the era rules: a gate that answers `prompt` whenever the file's first line is an entry (era A only); one that answers `panic` always in that shape; one that ignores the flag but matches both eras by reading the file twice; one that special-cases the battery's family names or fixture sizes; one that copies the expected `on_panic` from a hardcoded table keyed by line count. Measure each with `--gate <forger> --runs 1` and state killed/survived with the failed families.
3. Check the battery's fixtures for answer leakage: does any fixture name, size, ordering or line count correlate with the expected answer for the era families (QUALITY 128/129)? Say what a forger could learn from the case directory alone.
Write `<seat>.md` with the forger table and the leakage analysis."""),

    item("ReviewGate", "reviewer", ["operability"], f"""
REVIEWER — surgical code review of the V2 gate diff and the battery launcher. Receipts in {LANE}/.ufo/waves/round-92/w1/ReviewGate/.
1. `git -C {LANE} show {FREEZE} -- tools/check-limine-pins.py` (and `git diff {FREEZE}^ {FREEZE} -- tools/check-limine-pins.py`): review every changed hunk for correctness — `parse_limine_version` (ASCII digits, empty, `12.9.6.1`, `1.2.03`), the era comparison, the `in_global` transition at the first entry line (era A vs era B, the first-line case), the two new JSON fields, the `--live` path, and that R1-R10/U1 behaviour is unchanged for era A.
2. Review the battery's `sandbox_argv`, `copy_gate`, `run_gate` and `usage_check`: argv order for bwrap, `--` before the inner command, the `-I` position, path quoting, timeouts, temp cleanup, and the `--isolation-check` probe. Name any path where the sandbox silently degrades to an unsandboxed run.
3. Look for defects that would make a receipt lie: a pass that could be reported when `bwrap` is missing; a `got is None` path counted as a family pass; the error-row accounting in `run_battery`; whether `--runs 3` really means three independent fixture draws.
4. Prove or disprove two concrete counterexamples in scratch (e.g. era A vs B on a config whose first line is `/` with a `\r`; a version string `12.09.4`).
Write `<seat>.md` with findings F1..Fn: severity, file:line, the counterexample, and the one-line fix (do not edit the lane)."""),

    item("ReviewSource", "reviewer", ["depth"], f"""
REVIEWER — verify the era rule against the pinned sources. Receipts in {LANE}/.ufo/waves/round-92/w1/ReviewSource/.
1. Re-open `{SRC}/src/limine-v12.9.4-common_lib_config.c`, `…v12.9.5…`, `…v12.9.6…` and quote the cut paths: v12.9.4 `init_config` raw 638-650 (guard `c > config_addr`), v12.9.5/6 `create_menu_tree` raw 298-407 (forward scan, raw 328-330 cut, raw 362-365 label-end NUL), and the read order (raw 666/668, accessor 733+). Confirm or refute the line numbers the battery docstring and the knowledge entry cite.
2. Reproduce the era difference yourself on the pinned bytes: extract the two parsers into a scratch harness (allocate `config_addr`, run `create_menu_tree`, then `config_get_value(NULL,0,"hash_mismatch_panic")`), compile with stubs, and feed the four shapes: global key before an entry; entry first + key after the body; entry first + no key; no entry at all. Record the v12.9.4 vs v12.9.6 answers.
3. Check the ChangeLog quote (S380) and issue #700 (S381) against the pinned files, and say whether the battery's V2 families cover exactly the shapes that differ and no others.
4. Verify that `ERA-GLOBAL-KEY-A/B` and `ERA-DEFAULT` do not rest on the same discriminating element as the A/B flip (QUALITY 128).
Write `<seat>.md` with one confirmation/refutation per numbered item and the harness output."""),

    item("ScoutUpstream", "scout", ["freshness"], f"""
SCOUT — per-surface reconnaissance of the Limine visibility surface. Receipts in {LANE}/.ufo/waves/round-92/w1/ScoutUpstream/.
1. Read-only host facts: `pacman -Q limine`, `limine --version`, `pacman -Si limine` (network/sync DB read is fine, do NOT install), `ls /sys/class/tpm`, `cat /boot/limine.conf | head -5`, and the two `path:` lines the r91 receipt characterised. Record exact outputs.
2. Upstream: list the v12.9.4 → v12.9.6 tags and their dates (`git ls-remote --tags https://github.com/limine-bootloader/limine.git` or the GitHub API); find every ChangeLog line mentioning config parsing/global options between the three tags; check whether 12.9.7+ exists and whether it touches `common/lib/config.c` again (fetch `https://api.github.com/repos/Limine-Bootloader/Limine/releases?per_page=10`).
3. Check the pinned `v12.9.4`/`v12.9.5`/`v12.9.6` file hashes against the raw URLs you refetch (they must match `{SRC}/src/SHA256SUMS`).
4. Report the freshness boundary the claim should carry: the first release that would invalidate the V2 rule, and the host-side trigger (a pacman update) that should re-run the battery.
Write `<seat>.md` with a table: fact · command · output · implication for the claim's freshness clause. Do not install anything."""),

    item("ScribeLesson", "scribe", ["discernment"], f"""
SCRIBE — draft the QUALITY criterion the r91 wave proposed, in house style, and a lesson row. Receipts in {LANE}/.ufo/waves/round-92/w1/ScribeLesson/.
1. Read `{LANE}/corpus/QUALITY.md` tail (criteria 124-131) and `{LANE}/.ufo/waves/round-91/w1/ScribeLesson/draft-mistakes.md` (the drafted criterion 132 text).
2. Redraft criterion 132 as **R92-JUDGE-ORACLE-IMPORTABLE** in the house shape: bold title with the tag, a red (what went wrong, with the measured r91 evidence), a green (the rule to follow, phrased as an executable requirement), and "shown able to fail" (the r92 before/after receipts: r91 battery 82/82 on the controls vs r92 battery 0/89). Make it precise about what a launcher must close and what it cannot (behaviour/timing), and cite `corpus/lessons/round-92.md`.
3. Verify the number is still free: `grep -cE '^[0-9]+\. \*\*' {LANE}/corpus/QUALITY.md` and the last numbered criterion; if 132 is taken, say which number is next.
4. Draft the round-92 `## Mistakes` row for M2 (lie-wrapper path under isolation, `vacuous`, captured-by QUALITY 126) in the required class · evidence · captured-by · fix shape, and check it against the mistakes vocabulary in `CORPUS.md`.
5. State the exact edit the L1 should make (file, insertion point, bytes) — do not edit QUAALITY.md or the lesson yourself.
Write `<seat>.md` with the drafted criterion, the number check and the insertion instruction."""),

    item("ConnectorOverlap", "connector", ["adjacency"], f"""
CONNECTOR — sibling-overlap scan and cross-source pattern finding. Receipts in {LANE}/.ufo/waves/round-92/w1/ConnectorOverlap/.
1. Scan the fleet for ground that would conflict with this round: `grep -rl -i -e 'bwrap' -e 'unshare-all' -e 'oracle' -e 'limine' /home/vgpnk/Projects/shokunin/*-shokunin/{'{PROVINCE.md,SKILL.md}'} 2>/dev/null` and the same over each sibling's `corpus/knowledge/` (20 repos). For every hit, say whether it contradicts, duplicates or is silent on (a) the oracle-channel rule (a judge's oracle must not be importable by the subject) and (b) the Limine 12.9.5 visibility boundary.
2. Check whether another lane owns a *generic* sandboxing claim (kumitate? tameshi? revenger?) that this round's C1 would collide with; if so, name the lane, the file and the arbitration the CONNECTOR recommends (this lane reports, never absorbs).
3. Cross-source pattern: does the same "subject imports the judge" class appear in another lane's gates (search for `spec_from_file_location`, `importlib` in sibling `tools/`)? List instances with paths and say whether the pattern is the same defect class.
4. Re-read this round's knowledge entry `{LANE}/corpus/knowledge/limine-r92-oracle-isolation.md` against the pinned sources and flag any sentence a source does not support.
Write `<seat>.md` with a table: repo/file · what it holds · conflict/duplicate/silent · recommendation. Zero conflicts must be stated with the search commands that produced the absence."""),
]

SPEC = {
    "wave": "w1",
    "maxLanes": 16,
    "reportDir": ".ufo/waves/round-92/w1",
    "milestone": ("round-92: limine-pins battery oracle-isolation (C1 operability) and version-selected "
                  "visibility V2 (C2 depth), 89 families, 5 channel controls + 4 one-clause bends"),
    "axes": ["operability", "depth"],
    "context": CONTEXT,
    "items": ITEMS,
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(SPEC, f, indent=1)
print("wrote", OUT, "items:", len(ITEMS))
print("roles:", {r: sum(1 for i in ITEMS if i["role"] == r) for r in sorted({i["role"] for i in ITEMS})})
