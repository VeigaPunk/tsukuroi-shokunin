#!/usr/bin/env python3
"""Build .ufo/waves/round-71/w1-spec.json — tsukuroi round 71, one v1 wave (band 8-16, 14 seats).

Deterministic: same inputs -> same spec. Run from the lane root:
    python3 .ufo/waves/round-71/make-spec.py
"""
import json
from pathlib import Path

LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
DECL = "0fcfca315fbdf4ff6a47abeff08efa7fd27aa32e"
GODSPEED = (
    "/skill:godspeed\nYou are a Godspeed-enabled subagent.\n\n"
    "1. **Name the axes.**\n"
    "2. **Iterate cheap, in parallel.**\n"
    "3. **Keep moves that improve any axis and harm none.**\n"
    "4. **Don't aim \u2014 let the frontier walk itself.**\n\n"
    "## IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large "
    "batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or "
    "verbose plans. Act directly via tool calls.\n\n"
)

CONTEXT = GODSPEED + f"""You are an L2 seat of tsukuroi lane round 71 (hyaku run 15), wave w1 — the round's ONLY wave (v1 band 8-16, 14 seats). Host: canonical Linux/omp host (Arch). Lane: {LANE}. Declaration commit (frozen before data): {DECL}. Read SCORECARD.md "Round 71 — declaration" at that commit; the predicates there are frozen — never reinterpret, never amend, never substitute a counter of your own.

YOUR WRITE SCOPE (hard): only {LANE}/.ufo/waves/round-71/w1/ and {LANE}/.ufo/waves/round-71/probes/ (create your own subdirectory). Never write, stage, commit or push in {LANE} (the lane tree), the fleet repo /home/vgpnk/Projects/shokunin, any sibling lane, /home/vgpnk/Projects/shokuknow, .ufo/state, .scratch, MANIFEST.json or .ufo/watchdog.log. Never run mutating git/jj commands anywhere; a sandbox clone is created only as `git clone --shared {LANE} <scratch>/clone` and every git call names `-C <scratch>/clone`. The L1 is the only writer of the lane tree and the only one who commits.

SCRATCH: S=/fast/scratch/hyaku/tsukuroi-r71/<YourSeatName>; mkdir -p "$S"; trap 'rm -rf -- "$S"' EXIT (or python finally). Never use /tmp for anything over 50 MB; delete your tree before you yield and report if you could not.

EVERY PATH IS ABSOLUTE. Every `Report:` trailer path the validator renders is relative to {LANE} — write it at {LANE}/<that path>. Never message agent://all; you are a leaf: no delegation, no background jobs, no sub-swarm. Finish inside ~25 minutes of work.

TOOLING (operator authorization 2026-10-19): you may install or upgrade tools that help the task; read /home/vgpnk/.omp/agent/RULES.md first (official channels only; record tool/version/channel/reason in your report). PACMAN GUARD (orchestrator ruling 2026-10-20): all pacman transactions are PAUSED host-wide — install via `uv tool`/`npx`/an official binary in ~/.local/bin, or file no install at all. Never run pacman -S/-Sy/-Syu/-U/-R. Never restart a host service.

READ-ONLY HOST: no writes to /sys, /proc, /etc, /boot, package state, service state, module parameters; `sudo -n` is allowed only for read-only queries your item names; never `sudo` interactively. Writing any `/sys/module/*/parameters/*` file is operator-owned and must never be executed, not even on a fixture that points at the real sysfs.

BOUNDARY: the lane is read-only detection and report. Secrets are shape-only (never read or echo key material, tokens, session bytes). Host serials, WWIDs and hostnames beyond the fixture host name are not needed.

CLAIM CONTEXT — FROZEN in SCORECARD.md "Round 71 — declaration":
- C1 depth (lowest non-retired, 8 tied with adjacency; SOURCED — four new registry rows): the note `corpus/knowledge/module-parameter-plane-r71.md` carries exactly six rule rows MP1-MP6. Row grammar (one physical line, exactly 6 cells, no pipe inside a cell): `| MP<n> | <statement >= 12 words> | source=S### | snapshot=<file> | digest=<64 lowercase hex> | quote="<verbatim text from that snapshot, <= 25 words>" |`. The frozen counter `tools/count-mp-rows-r71.py` (sha256 fa67d4deb5f01a5124120276a8571fa36c7367d9db711ceb39bc1ca6fded48bc) requires per row: unique contiguous id; statement >= 12 words; >= 6 distinct non-stopword tokens (len >= 4) shared with the row's snapshot text AND shared/total >= 0.5; `source=` a registry id at the same revision; snapshot sha256 == digest == the SOURCES.json map digest; the registry row's `source` cell contains that map URL and its `anchor` cell contains the snapshot basename; quote <= 25 words, no pipe, located verbatim (whitespace-normalized) in the snapshot. Any MP-shaped line that does not parse is a `malformed-row` finding; no snapshot may be cited more than twice. Target: `MP_ROWS=6 MP_VERIFIED=6 MP_SOURCES=4 MP_SNAPSHOTS=4 MP_MALFORMED=0` and `met=1`, rc 0.
- Committed snapshots (read them; never re-write them): {LANE}/.ufo/waves/round-71/before/src/{{kernel-parameters.rst, params.c, moduleparam.h, main.c}} with SHA256SUMS and SOURCES.json. Digests: kernel-parameters.rst 45587d8e411db06dc600550f03236d3b7cbe7ad5bd898dbb9f965934ecd88799; params.c 923610d5de631d8b8dddcb89bf4b0f6932fb0dbf1f500d07453ea0b73b3782a4; moduleparam.h 220f2dac723a7b080211791a33cb3308ed12eaeb2309747232786d786cd14846; main.c e1e1a1c8a13f3d5e402bb8773b4aea3561dadcdca446b3dfb0482b0ddcb95929. URLs are in src/SOURCES.json (git.kernel.org plain at h=v7.2.11). Planned registry ids: S297 = kernel/params.c, S298 = include/linux/moduleparam.h, S299 = kernel/module/main.c, S300 = Documentation/admin-guide/kernel-parameters.rst.
- C2 operability (9; capability `selftest-case-timeout`): `tools/tsukuroi-census.sh` bounds every selftest case — each case child in its own process group, polled to a per-case bound (`TSUKUROI_SELFTEST_CASE_TIMEOUT`, default 60 s), killed TERM then KILL, and reported as a FAIL line naming the case and `timeout`; a hermetic self-check case proves the bound fires on a blocking child and does NOT fire on a child that finishes. Read-only, never a verdict term. Target: >= 3 case labels containing `R71-C2`, selftest `PASS (N cases, N passed, 0 failed)` with N >= 217 (baseline 214), the suite finishing under an external 300 s bound.
- Host facts (read-only capture {LANE}/.ufo/waves/round-71/before/host.txt): kernel 7.2.11-arch1-1; 136 modules publish a parameters dir, 829 parameter files; nvidia_drm parameters color_pipeline/fbdev/modeset/vblank all 0444, modeset=Y; nvidia NVreg_* 0444; nvidia_uvm parameters 0644 root-writable, none writable by the unprivileged reader; /sys/module/btrfs/parameters/read_policy absent (perm == 0); /proc/cmdline carries resume=, zswap.enabled=1, rootflags=subvol=@ and no module.parameter token; /etc/modprobe.d holds 3 files, /usr/lib/modprobe.d 4 (paths and modes only, contents never read).
- Pre-data receipts: {LANE}/.ufo/waves/round-71/before/ (absence-controls.txt, novelty-sweep.txt, control/battery.txt 12/12, redbefore-timeout.txt rc 124, selftest-base.txt 214 PASS, census-live-base.txt DEGRADED rc 1).

ASSIMILATION: none this round (L0 tsukuroi | round-64 open and unanswered). Do not read or use /home/vgpnk/Projects/shokuknow/merge/tsukuroi/.
MISROOT GUARD: a relative path can land in the fleet repo; always name the absolute lane path.

YOUR FINAL MESSAGE: at most 12 lines — one line per receipt/draft path you wrote, then the KEY=VALUE results your item asks for. No narrative.
"""

ITEMS = [
    dict(
        name="S1Scout", role="scout", axes=["depth", "C1", "sources"],
        milestone="C1 source re-open by a second route and quote locations",
        task="""Independently re-open all four C1 sources and prove the committed snapshots are the upstream bytes.
1. S=/fast/scratch/hyaku/tsukuroi-r71/S1Scout; mkdir -p "$S"; trap 'rm -rf -- "$S"' EXIT.
2. For each of kernel-parameters.rst, params.c, moduleparam.h, main.c: fetch the URL from {lane}/.ufo/waves/round-71/before/src/SOURCES.json by a route OTHER than git.kernel.org's plain endpoint (e.g. raw.githubusercontent.com/torvalds/linux/v7.2.11/<path>), sha256 it, and compare with the committed snapshot and the map digest. Record ROUTE2_OK=<n>/4 and every mismatch.
3. Locate, with line numbers, the exact quotes the six planned rows must carry: (a) params.c "invisible parameters" area and the perm==0 skip; (b) params.c "Do not allow runtime DAC changes to make param writable." and attr.mode = kp->perm; (c) moduleparam.h struct kernel_param_ops set/get contract; (d) main.c "unknown parameter '%s' ignored"; (e) main.c "Module %s is blacklisted"; (f) kernel-parameters.rst lines 20-37 (two specification routes, built-ins need the cmdline, sysfs reveal).
4. Independently capture the host module-parameter surface read-only (no writes): `ls -d /sys/module/*/parameters | wc -l`, `ls /sys/module/*/parameters/* | wc -l`, the four nvidia modules' file modes and values, /proc/cmdline, modprobe.d file list with modes (never contents).
5. Write {lane}/.ufo/waves/round-71/probes/S1Scout/{route2.txt,quotes.tsv,host-enum.txt} and a short .md report.
KEY=VALUE: ROUTE2_OK=, QUOTES_LOCATED=, PARAM_DIRS=, PARAM_FILES=, NVIDIA_DRIFT=""".replace("{lane}", LANE)),
    dict(
        name="E1Harness", role="executor", axes=["operability", "C2", "census"],
        milestone="C2 per-case timeout harness patch and hermetic cases",
        task="""Draft the C2 per-case timeout harness as a patch against {lane}/tools/tsukuroi-census.sh. You are the only writer of this draft; the L1 applies it.
1. S=/fast/scratch/hyaku/tsukuroi-r71/E1Harness; mkdir -p "$S"; trap 'rm -rf -- "$S"' EXIT. Copy the census into $S and work on the copy only.
2. In `run_selftest`, every case ultimately runs through `out=$(env "${ENV_BASE[@]}" "${EXTRA_ENV[@]}" "$BASH" "$SELF" 2>&1)` (and `check_cli` likewise). Add ONE bounded runner used by both: start the child in its own process group (`setsid` when available, else plain background), poll every 0.1 s to a per-case bound `${TSUKUROI_SELFTEST_CASE_TIMEOUT:-60}`, then TERM the group, wait 2 s, KILL the group; capture output in a temp file under the existing `$work`; return the child's rc or a distinct timeout rc. On timeout the case must FAIL with a line that names the case label and the word `timeout` (never a silent skip, never a crash of the suite).
3. Add exactly three hermetic cases labelled `(R71-C2)` and count them: (a) a blocking child (a FIFO read) with `TSUKUROI_SELFTEST_CASE_TIMEOUT=2` is killed within ~5 s and the case asserts the FAIL line names `timeout`; (b) a slow-but-finishing child (sleep 1) under the same 2 s bound PASSES (no false positive); (c) a child that ignores TERM is still killed (escalation) within the bound. Cases must not depend on the real host and must leave no process behind.
4. Prove the harness able to fail: with the bound lowered to 1 s and a child that sleeps 3 s, the suite must report a timeout FAIL and still exit with its normal FAIL rc. Capture the pre-patch hang evidence from {lane}/.ufo/waves/round-71/before/redbefore-timeout.txt (do not re-run it).
5. Write the unified diff at {lane}/.ufo/waves/round-71/probes/E1Harness/harness.patch plus `cases.txt` (the three case bodies) and a .md report naming every touched function and line range.
KEY=VALUE: PATCH_LINES=, CASES=3, BOUND_DEFAULT=, ESCALATION=yes|no, NOFALSEPOS=yes|no""".replace("{lane}", LANE)),
    dict(
        name="E2CounterAttack", role="executor", axes=["calibration", "C1", "counter"],
        milestone="independent source-level mutants of the C1 counter",
        task="""Attack the frozen C1 counter by source mutation, independently of the committed battery.
1. S=/fast/scratch/hyaku/tsukuroi-r71/E2CounterAttack; mkdir -p "$S"; trap 'rm -rf -- "$S"' EXIT.
2. Copy {lane}/tools/count-mp-rows-r71.py and build the fixture mirror the battery uses (a well-formed 6-row note over the four committed snapshots; see {lane}/.ufo/waves/round-71/before/control/battery.py for the shape — build your own, do not import it).
3. Build >= 7 source-level mutants, each removing ONE frozen clause (e.g. drop the >= 0.5 share test, drop the anchor binding, drop malformed-row detection, allow snapshot reuse 3, drop quote location, accept a 7-word quote, accept a non-contiguous id set, drop map-digest binding). Score each mutant against (i) the well-formed control and (ii) the matching bad fixture: a mutant is KILLED when the bad fixture still reads met=0 rc 1 or the control stops reading met=1.
4. Report survivors with the class that beat the counter, and whether the committed battery alone would have caught them.
5. Write {lane}/.ufo/waves/round-71/probes/E2CounterAttack/{mutants.txt,score.md}.
KEY=VALUE: MUTANTS=, KILLED=, SURVIVORS=, SURVIVOR_CLASSES=""".replace("{lane}", LANE)),
    dict(
        name="E3Repairs", role="executor", axes=["freshness", "D1", "D2"],
        milestone="r70 routed-defect receipts (stale tallies, shebang, final-revision receipts)",
        task="""Produce the receipts the round-70 non-author spot-check routed (corpus/lessons/round-70-verifier-spotcheck.md section 5), without touching the lane tree.
1. S=/fast/scratch/hyaku/tsukuroi-r71/E3Repairs; mkdir -p "$S"; trap 'rm -rf -- "$S"' EXIT.
2. D1 stale selftest tallies: find EVERY selftest figure in PROVINCE.md, corpus/README.md, SKILL.md, LOG.md, SCORECARD.md (`grep -nE '21[0-9] cases|196 ->|196 →|214 cases' ...`) and classify each as final (214 / 18 R70-C2 lines) or stale. Produce the exact append-only correction lines (never an in-place rewrite) with file, anchor quote and replacement sentence.
3. D2 unbacked final-revision re-run claims: identify the report's `79dac76c` claims (counter 6/6, cited-receipts PASS 75 files) and produce the corrected sentence plus the receipt path that does exist (after/gates-at-40c35ee7.txt, 74 files at 50389560).
4. D3 shebang: `head -1 tools/count-xs-rows-r70.py` and the documented invocation; produce the one-line fix and a red-before/after check (`./tools/count-xs-rows-r70.py --revision <rev>` before = exec error; after = works).
5. Also verify the r71 counter's shebang and that `python3 tools/count-mp-rows-r71.py --revision 0fcfca31` prints `MP_NOTE absent` rc 128.
6. Write {lane}/.ufo/waves/round-71/probes/E3Repairs/{tallies.tsv,corrections.md,shebang.txt}.
KEY=VALUE: STALE_TALLIES=, CORRECTIONS=, SHEBANG_FIXED=yes|no""".replace("{lane}", LANE)),
    dict(
        name="SC1Entry", role="scribe", axes=["depth", "C1", "knowledge"],
        milestone="C1 knowledge entry draft MP1-MP6 in the frozen grammar",
        task="""Draft the C1 knowledge entry, and prove it against the frozen counter yourself.
1. S=/fast/scratch/hyaku/tsukuroi-r71/SC1Entry; mkdir -p "$S"; trap 'rm -rf -- "$S"' EXIT.
2. Read the four committed snapshots under {lane}/.ufo/waves/round-71/before/src/ and the counter {lane}/tools/count-mp-rows-r71.py. Draft exactly six rows MP1-MP6 in the frozen grammar. Each statement is a rule (>= 12 words) and each quote is verbatim from that row's snapshot (<= 25 words, no pipe). Cover: perm==0 invisibility; mode == perm and store only with a write bit; the kernel_param_ops set/get contract; unknown parameter warned and ignored; module_blacklist refusing the load; the two specification routes plus the sysfs reveal.
3. Build a fixture mirror under $S (corpus/SOURCES.md with S297-S300, corpus/knowledge/module-parameter-plane-r71.md, the four snapshots and SOURCES.json) and run `python3 {lane}/tools/count-mp-rows-r71.py --fixture $S/mirror`. Iterate on YOUR OWN wording until it prints met=1 rc 0 — do not touch the counter.
4. Add a short host-applicability section: for each row, one line saying what the live capture (before/host.txt) shows (nvidia_drm modeset=Y at 0444, nvidia_uvm 0644 root-only, btrfs read_policy absent).
5. Write the note draft at {lane}/.ufo/waves/round-71/w1/SC1Entry/module-parameter-plane-r71.md plus `counter-run.txt` with the final met=1 output.
KEY=VALUE: MP_ROWS=6, MET=1|0, SOURCES=4, SNAPSHOTS=4""".replace("{lane}", LANE)),
    dict(
        name="SC2Sources", role="scribe", axes=["depth", "C1", "registry"],
        milestone="C1 registry rows S297-S300 and Gate record",
        task="""Draft the four registry rows and the Gate record for the new sources.
1. S=/fast/scratch/hyaku/tsukuroi-r71/SC2Sources; mkdir -p "$S"; trap 'rm -rf -- "$S"' EXIT.
2. Read {lane}/corpus/SOURCES.md's Registry table shape (11 cells, NF=13 under `awk -F'|'`) and the four snapshots plus src/SOURCES.json.
3. Write rows S297 (kernel/params.c), S298 (include/linux/moduleparam.h), S299 (kernel/module/main.c), S300 (Documentation/admin-guide/kernel-parameters.rst): kind code/code/code/docs, tier A, a scoped `scope` cell, an `anchor` cell that names the tag AND the snapshot basename AND the line range, a one-benefit `teaches` cell, status `mined`, opened 2026-11-04, recheck `on-release`, used-by `corpus/knowledge/module-parameter-plane-r71.md`. No cell may contain a pipe.
4. Gate block: for each row the URL, access date 2026-11-04 and a <= 25-word located quote with line numbers. Then mirror the lane's corpus in $S with your rows appended and run `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file $S/corpus/SOURCES.md`; iterate until rc 0 with warnings allowed.
5. Write {lane}/.ufo/waves/round-71/w1/SC2Sources/{rows.md,gate.md,census.txt}.
KEY=VALUE: ROWS=4, CENSUS_RC=, MALFORMED=0""".replace("{lane}", LANE)),
    dict(
        name="SC3Lesson", role="scribe", axes=["calibration", "lesson", "quality"],
        milestone="round lesson, Mistakes, and QUALITY criterion drafts",
        task="""Draft the round-71 lesson skeleton and the QUALITY criterion the r70 spot-check routed.
1. S=/fast/scratch/hyaku/tsukuroi-r71/SC3Lesson; mkdir -p "$S"; trap 'rm -rf -- "$S"' EXIT.
2. Read {lane}/corpus/lessons/round-70.md, round-70-verifier-spotcheck.md and corpus/QUALITY.md's last five criteria (numbers 100-104) to match house style.
3. Draft `corpus/lessons/round-71.md`: `## Gate` (candidates, admitted, rejected with reasons and flip, the non-author spot-check placeholder), `## Mistakes` with at least the r70-routed class rows the round actually repaired (stale-tally drift D1, unbacked final-revision receipts D2, shebang/source mismatch D3) written as class / evidence pointer / captured-by / fix, `## Considerthese` (the measured status of the four proposals in considerthese/2026-10-26.md — read that file and verify each status with a grep; no new adoption), and the `## Trend verdicts` skeleton.
4. Draft ONE new QUALITY criterion (number 105) that would have caught the D1 class BEFORE the report: every selftest figure a round touches must be diffed against the final receipt line in a pre-report sweep; cite the lesson path. Also draft the scoreboard continuation row set for round 71 (C1 counter arms, C2 harness arms) with empty survivor cells for the wave to fill.
5. Write {lane}/.ufo/waves/round-71/w1/SC3Lesson/{lesson.md,quality.md}.
KEY=VALUE: MISTAKES=, QUALITY_CRITERION=105, CONSIDERTHESE_STATUS=verified|not""".replace("{lane}", LANE)),
    dict(
        name="C1Connector", role="connector", axes=["adjacency", "C1", "overlap"],
        milestone="sibling-overlap and held-ground scan",
        task="""Scan for overlap and for recurrence of the r70 defects.
1. S=/fast/scratch/hyaku/tsukuroi-r71/C1Connector; mkdir -p "$S"; trap 'rm -rf -- "$S"' EXIT.
2. Read every sibling lane's PROVINCE.md under /home/vgpnk/Projects/shokunin/*-shokunin/ (read-only; do not write there) and decide whether the kernel module-parameter surface (sysfs parameters, modprobe.d, module_blacklist, kernel cmdline module tokens) belongs to tsukuroi or to a sibling (kama for endpoint/serving, revenger/kaidoku for RE, mori for fleet capacity). Quote the ownership sentence you rely on, with the file and line.
3. Held-ground check: at {lane} HEAD, confirm the novelty claims in the declaration (`modprobe.d`, `kernel-parameters`, `module_blacklist`, `NVreg`, `module_param`, `kernel_param_ops`, `param_attr_store` = 0 hits across corpus/ SKILL.md PROVINCE.md) and report any counterexample with its path:line.
4. Recurrence scan: does the D1 stale-tally class appear in other lane files the round will touch (corpus/README.md round-70 index row, PROVINCE.md:372, SKILL.md round-70 block)? List every occurrence with the exact figure and the final receipt figure.
5. Write {lane}/.ufo/waves/round-71/probes/C1Connector/{overlap.md,recurrence.tsv}.
KEY=VALUE: SIBLING_OWNERS=, NOVELTY_COUNTEREXAMPLES=, STALE_SITES=""".replace("{lane}", LANE)),
    dict(
        name="R1Reviewer", role="reviewer", axes=["depth", "C1", "falsify"],
        milestone="independent re-implementation of the C1 grammar",
        task="""Falsify C1 with your own implementation, not the lane's counter.
1. S=/fast/scratch/hyaku/tsukuroi-r71/R1Reviewer; mkdir -p "$S"; trap 'rm -rf -- "$S"' EXIT.
2. Read SCORECARD.md "Round 71 — declaration" at {decl} and write your OWN checker (python, under $S) for the six-row grammar and every frozen clause. Do not import or copy the lane counter's code.
3. Run your checker over the wave's SC1Entry draft ({lane}/.ufo/waves/round-71/w1/SC1Entry/module-parameter-plane-r71.md) and over a fixture you build yourself. Then run the lane counter on the same inputs and diff the verdicts row by row.
4. Attack the note's substance: for each MP row, re-locate the quote in the snapshot and judge whether the statement is what the quoted bytes say (overreach, missing qualifier, wrong direction). Name every defect with the row id and the snapshot line.
5. Write {lane}/.ufo/waves/round-71/w1/R1Reviewer/{review.md,verdicts.tsv}.
KEY=VALUE: ROWS=, AGREE=, DEFECTS=, INDEPENDENT_RC=""".replace("{lane}", LANE).replace("{decl}", DECL)),
    dict(
        name="R2Reviewer", role="reviewer", axes=["operability", "C2", "falsify"],
        milestone="apply the harness patch in a sandbox and attack it",
        task="""Attack C2 by applying the harness patch in a sandbox clone and running it.
1. S=/fast/scratch/hyaku/tsukuroi-r71/R2Reviewer; mkdir -p "$S"; trap 'rm -rf -- "$S"' EXIT; git clone --shared {lane} "$S/clone" -q.
2. Apply {lane}/.ufo/waves/round-71/probes/E1Harness/harness.patch inside $S/clone (patch -p1 or git apply). If the patch does not apply, say so with the reject text and stop.
3. Run `TMPDIR=$S bash tools/tsukuroi-census.sh --selftest` in the clone under an external 300 s bound; record case count, PASS/FAIL and every R71-C2 line. Run it twice to prove determinism.
4. Attack groups: (a) a case child that blocks on a FIFO; (b) a child that traps and ignores TERM; (c) a child that spawns a grandchild which outlives it (does the group kill reach it?); (d) a slow-but-finishing child under a tight bound (false positive?); (e) `TSUKUROI_SELFTEST_CASE_TIMEOUT` unset, 0, empty and non-numeric; (f) the suite's exit code and the `PASS (...)` line shape unchanged when nothing times out. Report which groups the patch survives.
5. Check the patch does not change any live census output line or exit code: `bash tools/tsukuroi-census.sh` in the clone vs {lane}/.ufo/waves/round-71/before/census-live-base.txt (diff the rollup and every PLANE line).
6. Write {lane}/.ufo/waves/round-71/w1/R2Reviewer/{review.md,selftest-run1.txt,selftest-run2.txt,live-diff.txt}.
KEY=VALUE: PATCH_APPLIES=yes|no, CASES=, PASS=, R71_C2_LINES=, GROUPS_SURVIVED=""".replace("{lane}", LANE)),
    dict(
        name="K1Critic", role="critic", axes=["calibration", "claims", "falsify"],
        milestone="re-run every declaration receipt and falsify both claims",
        task="""Falsify the round's two claims against the declaration's own receipts.
1. S=/fast/scratch/hyaku/tsukuroi-r71/K1Critic; mkdir -p "$S"; trap 'rm -rf -- "$S"' EXIT.
2. Re-run every receipt named in SCORECARD.md "Round 71 — declaration" (a)-(f): `sha256sum -c` on before/src/SHA256SUMS, the counter sha256, the battery (12 cases), the absence controls, the novelty sweep, the red-before. Report every figure that does not reproduce and every command whose quoted output differs.
3. Attack the predicates themselves: C1 — can a note pass the counter while stating something the snapshot does not say (build one such note in your scratch and score it)? C2 — can a case pass without the bound firing (name the mutation)? Name each channel with the clause that fails to close it.
4. Attack the claim sizing: is C1's after-state re-derivable with ONE command over committed bytes? Is C2's target a do-nothing control cannot reach? Say yes/no with the command.
5. Write {lane}/.ufo/waves/round-71/w1/K1Critic/{critique.md,receipts.txt}.
KEY=VALUE: RECEIPTS_REPRODUCED=, DEFECTS=, PREDICATE_CHANNELS=""".replace("{lane}", LANE)),
    dict(
        name="M1Mutation", role="mutation-tester", axes=["operability", "C2", "mutation"],
        milestone="harness mutants and case-attribution scoring",
        task="""Mutation-test the C2 harness and its three cases.
1. S=/fast/scratch/hyaku/tsukuroi-r71/M1Mutation; mkdir -p "$S"; trap 'rm -rf -- "$S"' EXIT; git clone --shared {lane} "$S/clone" -q; apply {lane}/.ufo/waves/round-71/probes/E1Harness/harness.patch there.
2. Build >= 8 harness mutants, each removing ONE guarantee: no process-group kill; TERM only (no KILL escalation); bound ignored (infinite wait); bound read once at startup so a per-case override is ignored; timeout reported as PASS; timeout line without the case label; no output capture (child inherits stdout so the FAIL line is lost); temp file under /tmp instead of $work. Score each against the three R71-C2 cases: killed when a case FAILs or the suite hangs under an external 120 s bound.
3. Report survivors with the class that beat the case, and whether the harness's own self-check can catch its own removal.
4. Write {lane}/.ufo/waves/round-71/probes/M1Mutation/{mutants.txt,score.md}.
KEY=VALUE: MUTANTS=, KILLED=, SURVIVORS=, SURVIVOR_CLASSES=""".replace("{lane}", LANE)),
    dict(
        name="N1Sentinel", role="sentinel", axes=["calibration", "safety", "audit"],
        milestone="read-only, secret and misroot audit of the wave",
        task="""Audit the wave for boundary violations.
1. S=/fast/scratch/hyaku/tsukuroi-r71/N1Sentinel; mkdir -p "$S"; trap 'rm -rf -- "$S"' EXIT.
2. After the other seats have written (poll the wave dirs, do not block more than ~10 minutes): audit every file under {lane}/.ufo/waves/round-71/{w1,probes} for (a) host writes to /sys /proc /etc /boot or any package/service state command; (b) secret-shaped strings (keys, tokens, session bytes, op:// refs) — report shape only, never the value; (c) `/tmp` as evidence or scratch root; (d) relative paths that would land in the fleet repo; (e) any write outside the wave dirs (use `git -C {lane} status --porcelain` and `git -C /home/vgpnk/Projects/shokunin status --porcelain` read-only).
3. Check every claimed scratch tree is gone: `ls -d /fast/scratch/hyaku/tsukuroi-r71/*` and report what remains.
4. Write {lane}/.ufo/waves/round-71/probes/N1Sentinel/audit.md.
KEY=VALUE: WRITES=, SECRETS=, SUDO_NONREADONLY=, TMP_EVIDENCE=, LANE_DIRTY=, MISROOT=""".replace("{lane}", LANE)),
    dict(
        name="SC4Index", role="scribe", axes=["coverage", "C1", "index"],
        milestone="coverage-map row, PROVINCE paragraph and SKILL table drafts",
        task="""Draft the index/province/skill text for the new plane (drafts only).
1. S=/fast/scratch/hyaku/tsukuroi-r71/SC4Index; mkdir -p "$S"; trap 'rm -rf -- "$S"' EXIT.
2. Read {lane}/corpus/README.md's coverage-map style (a round-NN section with a two-column table), {lane}/PROVINCE.md's promotion-paragraph style (see "Round-44 promotion — R44-SCRUB-VIEW") and {lane}/SKILL.md's last decision-table block (round 68/70 shape).
3. Draft: (a) a `## Round 71 — kernel module-parameter plane` coverage-map row naming the note and S297-S300; (b) a PROVINCE paragraph that says what is Core now (reading the parameter surface: which parameters exist, their modes, their values, and the boot/modprobe routes), what stays operator-owned (writing any parameter, modprobe.d edits, module load/unload, blacklist changes) and what is explicitly NOT claimed (no module internals, no RE); (c) a SKILL decision table with >= 6 rows mapping an observed `/sys/module/<name>/parameters/<p>` shape to a verdict and an operator action (e.g. 0444 + value Y, 0644 + unprivileged EACCES, absent + module loaded, unknown param warning in dmesg, blacklisted module).
4. Every table row cites the row id (MP1-MP6) it rests on and no row may claim a write capability.
5. Write {lane}/.ufo/waves/round-71/w1/SC4Index/{coverage.md,province.md,skill.md}.
KEY=VALUE: TABLE_ROWS=, CITED_IDS=, WRITE_CLAIMS=0""".replace("{lane}", LANE)),
]


def main():
    spec = {
        "wave": "w1",
        "reportDir": ".ufo/waves/round-71/w1",
        "maxLanes": 256,
        "context": CONTEXT,
        "items": [
            {
                "name": it["name"], "role": it["role"], "axes": it["axes"],
                "milestone": it["milestone"], "item": it["name"],
                "prompt": GODSPEED + it["task"],
            }
            for it in ITEMS
        ],
    }
    out = Path(__file__).with_name("w1-spec.json")
    out.write_text(json.dumps(spec, indent=1) + "\n")
    print(f"wrote {out} items={len(spec['items'])} context={len(spec['context'])}")


if __name__ == "__main__":
    main()
