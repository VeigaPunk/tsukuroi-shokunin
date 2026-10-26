#!/usr/bin/env python3
"""Builds the round-43 W2 wave spec (v1 wave 2 of 2: falsify; carries the six counted C2 reads). Writes w2-spec.json."""
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
L = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
W = f'{L}/.ufo/waves/round-43'
SC = '/fast/scratch/hyaku/tsukuroi-r43'
BASE = '6951ead90566b2d74f7c45b4efca29246badad64'
FREEZE = 'fe35700183188f7d712e2932cabde1944efca052'
IMPL = '717b716a8943151ace8657e0ca23d7d9b8434f26'
TIP = '8acf0b022586a0f3164c77659fb96ba5f90949b6'
BCA = f'{L}/tools/boot-chain-audit.sh'
ENTRY = f'{L}/corpus/knowledge/btrfs-scrub-record-r43.md'
OLDENTRY = f'{L}/corpus/knowledge/btrfs-scrub-record-r42.md'
C1C = f'{L}/tools/score-bootinputs-r43.py'
C2C = f'{L}/tools/check-scrub-record-r43.py'
SCRUB = f'{L}/.ufo/waves/round-42/frozen/src/scrub.c'
IOCTL = f'{W}/frozen/src/ioctl.c'
CAP = f'{W}/frozen/hostcap'
LESSON = f'{L}/corpus/lessons/round-43.md'

CONTEXT = f"""/skill:godspeed
You are an L2 seat of tsukuroi lane round 43 (hyaku run 9), wave w2 of two v1 waves (falsify). The L1 (agent TsukuroiR43) holds the planner seat and is the only integrator and committer. Lane repo: {L} (host operability and repair on this Arch/omarchy host; boot-chain audit; the btrfs scrub record is Frontier).
Frozen claims (SCORECARD.md "Round 43 — declaration", freeze {FREEZE}; base {BASE}; implementation {IMPL}; wave-1 integration and the lane tip under test {TIP}):
- C1 operability: {BCA} under `set -uo pipefail`: base boot_inputs_newer piped `find … -print -quit 2>/dev/null | grep -q .`, so a missing start point or unreadable directory listed before a newer input made it print 0 and BOOTED-OBSERVED passed (fail-open). Fix: helper inputs_newer_than decides on find's output; four `R43-C1-*` selftest cases (selftest 45 → 49 at {TIP}). Frozen counter {C1C} (sha256 886f92c8…e10f): PASS iff cases == 16 and correct == 16 and identity_ok == 1 and live_agree == 1 and selftest_pass == 1 and selftest_r43 >= 2. Kill rule: a function other than inputs_newer_than, boot_inputs_newer, run_selftest changes, or the round-42 C1 counter / census selftest regresses. Base FAIL (correct 8), {IMPL} PASS, {TIP} PASS (correct 16, selftest 49).
- C2 depth (sourced): {ENTRY} rows SR1, SR3, SR6 (sections `## SR1`, `## SR3`, `## SR6`: Statement, Quotes, Host reading) on S237 = btrfs-progs v7.1 cmds/scrub.c frozen at {SCRUB} (sha256 48df2e2f…0801), S240 = Linux v7.2.11 fs/btrfs/ioctl.c frozen at {IOCTL} (sha256 7b3488f2…ba01), S241 = own-work capture {CAP}/capture.txt (sha256 f7ecbe7c…c556). The text at {TIP} is final for this wave: wave-1 first falsifiers were integrated and each adopted sentence was checked against its source line (lesson {LESSON} "Entry gate (C2)"). Frozen counter {C2C} (sha256 b4602c56…9854): PASS iff rows == 3 and quotes_ok == 3 and props_ok == 3 and host_ok == 3 and sources_ok == 1 and verdicts_ok == 3 and novelty_base_hits == 0 and pointer_ok == 1; at {TIP} every conjunct but verdicts_ok holds. verdicts_ok counts ONLY this wave's seats C2RevSR<n> (reviewer) and C2CritSR<n> (critic). Kill rule: any bound `fails`; a `partly` without a bound residual `holds`; an unbound counted seat.
Rules for every seat (host guard):
- Your tools start at the fleet root /home/vgpnk/Projects/shokunin: cd into your scratch dir first and use absolute paths everywhere. Never write a tracked file of the fleet repo or of any lane; never write under /home/vgpnk/.local/bin or any PATH directory; never plant shims.
- Read-only on lane content: never edit, create or delete any tracked lane file; never run git add/commit/stash/checkout/reset/push or any mutating jj command in the lane; never touch the lane's Git index or jj state, the fleet repo (outside this lane), any sibling lane, or /home/vgpnk/Projects/shokuknow (read-only). Never mutate the host: no package, service, hook, sysfs, mount outside a private `unshare` namespace, boot, /etc or /var/lib change; no sudo; never run `btrfs scrub start/cancel/resume/limit -l` or `btrfs device stats -z`, never call a btrfs ioctl other than the read-only probe in {CAP}/capture.sh. Signal only processes you started (by PID); never pkill/killall by pattern. Never import lane tools as Python modules from the lane dir (it writes tools/__pycache__); copy them to your scratch first or run them as scripts.
- Write ONLY your report and your receipts. Every `Report:` trailer path is relative to {L} — write it at {L}/<that path> (absolute), i.e. {W}/w2/<your seat name>.md. Small receipts (under 2 MB each) go in {W}/w2/<your seat name>/ (create it). Never write anywhere else in the lane or under the fleet root.
- Scratch: every clone, copy, mutant or fixture lives under {SC}/<your seat name>/ (mkdir -p; export TMPDIR there; pass --scratch to the C1 counter). Never build under /tmp. Remove your scratch dir before you finish (trap 'rm -rf -- "$S"' EXIT), after copying receipts into your seat dir. A /tmp path is never evidence.
- Fixture git repos: D=$(mktemp -d {SC}/<seat>/fx.XXXXXX); `git clone -q --shared {L} "$D"`; `git -C "$D" remote remove origin`; verify `git -C "$D" rev-parse --show-toplevel` equals $D; commit variants only there with `-c user.name=fixture -c user.email=fixture@invalid`; run counters with --lane "$D" --revision <sha>.
- Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the task — read /home/vgpnk/.omp/agent/RULES.md first (official channels, update-safety gate; record tool/version/channel/reason in your report). pacman guard: ALL pacman transactions are PAUSED host-wide — never pacman -S/-Sy/-Syu/-U/-R; install only via uv tool / npx / an official binary in ~/.local/bin; never restart a host service.
- You are a leaf: do not spawn agents (executors may spawn at most one read-only labrat), do not run a swarm, never message agent://all.
- Heavy runs: the round-42 C1 counter takes 1-3 min and several CPUs, the census selftest ~25 s; never run more than one heavy counter at a time.
- Evidence: every claim carries a path:line, a command with its observed output, or a URL with access date and a <=25-word located quote. An unrun check has not passed; say what you did not do. Report findings even when they falsify the claims.
- Report format: first line `VERDICT: <supports|falsifies|defect-found|draft|no-finding>` (the six counted C2 seats use the form their item gives instead), then evidence. Your final yielded answer repeats that first line and names your report path.
"""

items = []


def add(name, role, axes, milestone, body):
    items.append({'name': name, 'role': role, 'axes': axes, 'milestone': milestone,
                  'prompt': '/skill:godspeed\n' + body.strip()})


VERDICT_RULES = ("Verdict meaning (decide by the pinned source lines, not by taste): `holds` — every sentence of the row's "
                 "**Statement.** and **Host reading.** is supported by the pinned source lines (S237 scrub.c, S240 ioctl.c, "
                 "S241 capture.txt), and every sentence the row marks [inference] is labelled as such and is a reasonable "
                 "reading of those lines; `partly` — no sentence is false but at least one unmarked sentence says more "
                 "than the lines support (name it and give the exact narrower text); `fails` — at least one sentence is "
                 "contradicted by a pinned line (quote that line). Judge only the row's own section (`## SR<n>` up to the "
                 "next `## `), at revision " + TIP + ". "
                 "OUTPUT FORM (binding, nothing else counts): (1) the FIRST line of your report file is exactly "
                 "`ROW SR<n> VERDICT: <holds|partly|fails>` — no prefix, no trailing spaces, no blank line before it; "
                 "(2) your final yielded data is a JSON object whose key `verdict_line` holds exactly that same line, plus "
                 "`report` (your report path) and `findings` (list); never write a second, different verdict line anywhere.")

ROWFOCUS = {
    'SR1': 'scrub.c:440-540 (scrub_datafile, scrub_open_file, _r, _w, rename), :770-793, :843-945 (scrub_write_file, scrub_write_progress), every `unlink`/`remove`/`truncate` (grep), the three scrub_write_progress call sites, cancellation (:905, :941, :1021, :1685-1687)',
    'SR3': 'scrub.c:795-830 (scrub_resumed_stats), :843-895, :1020-1130 (progress thread), :1136-1190, :1233-1340 (options, do_print/do_record), :1395-1460 (allocation, resume selection), :1495-1560, :1680-1730 (end of run, exit), :1755-1836',
    'SR6': f'scrub.c:180-190, :336-345, :1186-1206, :1370-1400, :1460-1480, :1900-1990, and {IOCTL}:3060-3145, :5560-5600',
}
for row in ('SR1', 'SR3', 'SR6'):
    n = row[2:]
    add(f'C2RevSR{n}', 'reviewer', ['depth', 'C2', row, 'counted'], f'{row} counted read (reviewer)',
        f"Item V-{row}-R (COUNTED VERDICT). Read row {row} of {ENTRY} at {TIP} (`git -C {L} show {TIP}:corpus/knowledge/btrfs-scrub-record-r43.md`). First verify the pins: `sha256sum {SCRUB}` = 48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801; `cd {W}/frozen/src && sha256sum -c SHA256SUMS`; `sha256sum {CAP}/capture.txt` = f7ecbe7c990e68d7b0dbdbd8bfe65f3acd1cbbdabe33d47e71a6f1ae1242c556. Check every **Quote.** verbatim on its named line. Then read the source around every sentence ({ROWFOCUS[row]}) and judge each sentence of the Statement and the Host reading; give, per sentence, the lines you checked. {VERDICT_RULES.replace('<n>', n)}")
    add(f'C2CritSR{n}', 'critic', ['depth', 'C2', row, 'counted'], f'{row} counted read (critic)',
        f"Item V-{row}-C (COUNTED VERDICT, adversarial). Hunt for the false or overreaching sentence in row {row} of {ENTRY} at {TIP}: alternate code paths ({ROWFOCUS[row]}), conditions the statement omits, universal words ('every', 'only', 'never', 'no', 'all', 'once'), unmarked inferences. Verify pins first (`sha256sum {SCRUB}` = 48df2e2f…0801; `sha256sum -c SHA256SUMS` in {W}/frozen/src; capture sha256 f7ecbe7c…c556). Wave-1 attacks are in {W}/w1/C2DraftCrit{row}.md and C2DraftRev{row}.md and their integration in {LESSON} 'Entry gate (C2)'; check whether the integrated text answers them, but judge the text as it stands. {VERDICT_RULES.replace('<n>', n)}")

# ---------------- C1 final ----------------
add('C1FinalRerun', 'executor', ['operability', 'C1'], 'C1 counter at the tip',
    f"Item C1-F1. Verify the C1 counter's sha256 equals 886f92c8cd58e52e4e74f4df81708f243b77e9d33de567b47371f21419b3e10f at {FREEZE} and in the working tree. Run `python3 {L}/tools/run-receipt.py --revision {TIP} --tool-revision {FREEZE} --out {W}/w2/C1FinalRerun/c1-tip-8acf0b0-<k>.jsonl -- tools/score-bootinputs-r43.py --revision '{{rev}}' --scratch {SC}/C1FinalRerun/s` three times (k = 1..3; TMPDIR={SC}/C1FinalRerun). Report every field per run (cases, correct, wrong, identity, live, selftest_line, selftest_r43, verdict). Confirm `git -C {L} diff --stat {IMPL} {TIP} -- tools/boot-chain-audit.sh` and say what changed.")
add('C1FinalSelftest', 'executor', ['operability', 'C1', 'fix-able-to-fail'], 'selftest and red-before per case',
    f"Item C1-F2. Export {BCA} at {TIP}; run `--selftest` twice (TMPDIR in scratch): expect `PASS total=49 failed=0`. For each of the four `R43-C1-*` cases build the smallest single revert of the fix that should turn it red (e.g. the base pipeline in inputs_newer_than; `2>/dev/null` dropped) and show which cases go red on each; report any R43 case that no revert can turn red (vacuous case).")
add('C1FinalKillRule', 'executor', ['operability', 'C1', 'kill-rule'], 'kill rules at the tip',
    f"Item C1-F3. Kill rules at {TIP}: (1) per-function sha256 of every top-level function of tools/boot-chain-audit.sh at {BASE} and {TIP}; list changed functions (allowed: inputs_newer_than (new), boot_inputs_newer, run_selftest). (2) `python3 {L}/tools/run-receipt.py --revision {TIP} --tool-revision {TIP} --out {W}/w2/C1FinalKillRule/r42-c1-8acf0b0.jsonl -- tools/score-size-invariance-r42.py --revision '{{rev}}' --scratch {SC}/C1FinalKillRule/s` (expect PASS). (3) census at {TIP} `--selftest` (expect `PASS (132 cases, 132 passed, 0 failed)`) and `git -C {L} diff --quiet {BASE} {TIP} -- tools/tsukuroi-census.sh`. Report each.")
add('C1MutFinal', 'mutation-tester', ['operability', 'C1'], 'mutants at the tip',
    f"Item C1-F4. Re-run the wave-1 mutant set ({W}/w1/C1MutFix.md (a)-(j), {W}/w1/C1MutSelftest.md) against {TIP}: score each with the frozen C1 counter in a scratch clone and with the {TIP} `--selftest`. Table: mutant, counter verdict/correct, selftest result. Which survivors remain, which are behaviour-changing on a real host, and are they named as recorded limits in {L}/SKILL.md 'Boot-input freshness under pipefail — round 43'?")
add('C1CritFinal', 'critic', ['operability', 'C1'], 'attack C1 as landed',
    f"Item C1-F5. Attack C1 as landed at {TIP}: is every declared conjunct met by honest means (no gating on namespace traces in the production code — read the diff {BASE}..{TIP} of tools/boot-chain-audit.sh line by line)? Does the declared surface match what moved? Is the axis (operability) and the 'improved' reading fair given the open channels (K7) and the counter gaps the wave found? Does any kill rule fire? Verdict with evidence.")
add('C1RevIntegration', 'reviewer', ['operability', 'C1'], 'integration review',
    f"Item C1-F6. Review `git -C {L} diff {IMPL} {TIP} -- tools/boot-chain-audit.sh SKILL.md` for C1: the added `R43-C1-missing-start-point-silent` case (does it test what its name says, any dependence on locale/umask/TMPDIR?), and the SKILL sections 'Boot-input freshness under pipefail — round 43' and the registry row `bootinputs-r43` (every number and claim vs receipts in {W}/before, after, controls, w1). Report each inaccuracy with line numbers.")

# ---------------- C2 final (non-counted) ----------------
add('C2EntryAudit', 'reviewer', ['depth', 'C2', 'QUALITY 91'], 'adopted-text audit',
    f"Item C2-F1. QUALITY 91 audit: diff the entry `git -C {L} diff {IMPL} {TIP} -- corpus/knowledge/btrfs-scrub-record-r43.md`. For every changed or added sentence find its row in {LESSON} 'Entry gate (C2)' and re-run the source-line check yourself (`sed -n <n>p` on {SCRUB} / {IOCTL}); report any adopted sentence with no recorded check or whose recorded line does not support it. Also check the triage bullets and Limits (not counted rows) against the sources.")
add('C2CounterAtTip', 'executor', ['depth', 'C2'], 'C2 counter at the tip',
    f"Item C2-F2. Copy {C2C} to your scratch (do not import it from the lane dir) and run `python3 <copy> --lane {L} --revision {TIP}`; report every conjunct and per-row quote counts; confirm the copy's sha256 = b4602c566b4f39277e068d27ad10ad0ec361ed7e81a938831cec72631e319854. Then independently re-derive quotes_ok/props_ok/host_ok/sources_ok/novelty/pointer by hand (grep/sed), and report any disagreement with the counter.")
add('SrcReopenS240', 'reviewer', ['sources', 'C2'], 'S240 re-open',
    f"Item C2-F3. Re-open S240 live: curl -sSfL 'https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/fs/btrfs/ioctl.c?h=v7.2.11' into scratch, sha256 vs {W}/frozen/src/SHA256SUMS, `git ls-remote https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git refs/tags/v7.2.11^{{}}`. Locate the Gate quote of {LESSON} for S240 at its lines; check every cell of the S240 row in {L}/corpus/SOURCES.md (kind, tier, scope, anchor lines, teaches, status, opened, recheck, used-by) against the source. Verdict per cell.")
add('SrcReopenS241', 'reviewer', ['sources', 'C2'], 'S241 re-open',
    f"Item C2-F4. Re-run `bash {CAP}/capture.sh {W}/w2/SrcReopenS241/capture-rerun.txt` (unprivileged, read-only), diff with {CAP}/capture.txt (timestamps excepted), locate the S241 Gate quotes of {LESSON}, and check every cell of the S241 row in {L}/corpus/SOURCES.md. Also read capture.sh: does it do exactly what its header says and nothing else? Verdict per cell.")
add('SrcReopenS237', 'reviewer', ['sources', 'C2'], 'S237 re-open',
    f"Item C2-F5. Re-open S237 live (raw https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/cmds/scrub.c, sha256 vs 48df2e2f…0801; `git ls-remote https://github.com/kdave/btrfs-progs refs/tags/v7.1^{{}}`), locate the S237 Gate quote of {LESSON}, and check the logged used-by change (`git -C {L} diff {BASE} {TIP} -- corpus/SOURCES.md`): only used-by changed on S237, logged old→new? Verdict.")
add('C2CritRejectF1', 'critic', ['depth', 'C2', 'discernment'], 'attack the integrator reject',
    f"Item C2-F6. The L1 rejected the wave-1 claim 'the device id is never emitted, so resume never engages for self-written records' ({W}/w1/C2DraftCritSR3.md F1) on {SCRUB}:782-792 and the harness in {W}/w1/C2ExecTailRepro.md. Attack the reject: re-read scrub_write_file :843-895, scrub_writev, scrub_write_buf and the reader's state machine (:577-760); if you can, compile the write path and the reader from the frozen file in scratch (stubs only) and show one record round-trip with its devid. Is the reject right? Is anything else in that F1 right?")

# ---------------- no-harm / curation / frontier ----------------
add('CritNoHarmFinal', 'critic', ['no-harm'], 'six-axis no-harm',
    f"Item N-1. No-harm at {TIP} vs {BASE}, per axis: `git -C {L} diff --numstat {BASE} {TIP}` (any deleted file or deleted line outside the claims' surfaces?), SCORECARD.md append-only (`git diff` shows only additions?), moved pins left unmarked (lane-internal pins into boot-chain-audit.sh and btrfs-scrub-record-r42.md lines), corpus/SOURCES.md rows only added or used-by changed, PROVINCE/README edits append-only. Name any harm with its command.")
add('RegistryFinal', 'executor', ['no-harm', 'operability'], 'registry and self-assessment',
    f"Item N-2. Run `python3 {L}/tools/check-registry-coverage.py --revision {TIP}` (expect PASS 68/68) and `python3 {L}/tools/check-self-assessment.py --revision {TIP}`; the latter is expected to show K07-K11 mismatches until the round-43 axes table lands — report exactly which checks mismatch and the observed values (they are the numbers the outcome table must carry). Use run-receipt.py receipts into {W}/w2/RegistryFinal/.")
add('SourcesCensusFinal', 'executor', ['sources'], 'sources census',
    f"Item N-3. Run `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` (exit code, findings) and the seven frozen manual census commands of /home/vgpnk/Projects/shokunin/CORPUS.md §Census on `git -C {L} show {TIP}:corpus/SOURCES.md` (in a scratch copy of the lane layout so used-by paths resolve). Rows before ({BASE}) and after; malformed, dup ids, enum violations, missing used-by. Paste commands and outputs.")
add('SkillReview', 'reviewer', ['depth', 'operability'], 'SKILL sections review',
    f"Item N-4. Review the SKILL.md sections 'Boot-input freshness under pipefail — round 43', 'Scrub record re-grounded — round 43' and 'Gate and probe registry — round43 superseding current rows' at {TIP}: every claim against the entry, receipts and counters; the registry table retains every round36-table row verbatim (`diff` the two tables' rows) plus two new rows; the decision table's rows say no more than SR1/SR3/SR6. Report inaccuracies with line numbers.")
add('ProvinceReadmeReview', 'reviewer', ['coverage', 'calibration'], 'PROVINCE/README notes review',
    f"Item N-5. Review the appended 'Round-43 note' in {L}/PROVINCE.md and 'Round-43 coverage note' in {L}/corpus/README.md at {TIP}: does the PROVINCE note's correction of the round-42 note hold (host has no record; 0600 mode argument; flock; the [inference] about root-only records), does README claim any coverage ground the round did not move? Verdict with evidence.")
add('LessonReview', 'critic', ['discernment', 'lessons'], 'Mistakes rows able to fail',
    f"Item N-6. For every row of {LESSON} `## Mistakes`, run the 'able to fail' command it names (at the revision it implies) and report whether it is red where it says red; check each class against the CORPUS.md vocabulary and each captured-by against corpus/QUALITY.md. Also check the 'Round-42 routed defects' dispositions against the repo at {TIP}. Report each row: ok / wrong (why).")
add('GateReview', 'reviewer', ['discernment', 'sources'], 'Gate section review',
    f"Item N-7. Review {LESSON} `## Gate` at {TIP}: every quote <=25 words and located at the stated line (grep -n), URLs and access date present, rows touched logged old→new, the Entry gate table's source lines (spot-check 6 rows yourself), the assimilation reject reasons (ext4 absent on this host: `findmnt -rno TARGET,FSTYPE`), the considerthese section's dependent list vs `git grep` at {TIP}. Verdict per subsection.")
add('AdjFinal', 'scout', ['adjacency', 'no-harm'], 'final sibling pin sweep',
    f"Item N-8. Re-run wave-1 AdjPins ({W}/w1/AdjPins.md) at {TIP}: boot-chain-audit.sh changed again after {IMPL} (one selftest case, +2 lines near the end). Sweep sibling repos (tracked files, `git -C <repo> grep -n`) for pins `boot-chain-audit.sh:<n>`, `btrfs-scrub-record-r42.md:<n>`, `tsukuroi-census.sh:<n>`, `SKILL.md:<n>` (tsukuroi's), and list each with base and tip content positions. Produce the final report-only handoff lines (tameshi service-optin-protocol.md:153 with its true referent at the tip; mori PROVINCE.md:287 with named referents).")
add('CritTrendFinal', 'critic', ['discernment'], 'trend verdicts draft',
    f"Item N-9. Draft the three LEARNING.md trend verdicts (expansion, quality, discernment; vocabulary improved/harmed/unchanged/unprovable-but-better) for round 43 at {TIP} with evidence, assuming C1 PASS and leaving C2 conditional on the counted reads (give both branches). Attack overclaiming: is the r43 entry 'uncovered coverage-map ground' (expansion) or deepening (quality)? Did any admitted entry fail its re-check? Does the discernment trend have an outside check yet?")
add('CritCalibration', 'critic', ['calibration'], 'self-assessment vs repo state',
    f"Item N-10. Count mismatches between the lane's self-assessment and observed repo state at {TIP}: the SCORECARD round-43 declaration (claims, before values, controls, sha256s — recompute them), SHONEN.md boxes (cited lines still say what SHONEN claims?), the lesson's statements about counts (rows, cases, seats). Each mismatch with command and observed value.")
add('ConnRound44', 'connector', ['coverage', 'frontier'], 'round-44 planned row',
    f"Item N-11. Using {W}/w1/ConnFrontier.md, {LESSON} (routed items still open: census :743 lookup case, single-line readers, the counter gaps recorded in SKILL round-43 sections) and {L}/PROVINCE.md Frontier, draft the round-44 planned row: 1-3 claims on distinct axes, one on the lowest axis (depth 8 / adjacency 8, or say why adjacency stays lane-unreachable), each with a do-nothing control that fails. Exact text.")
add('ConnQualityCriterion', 'connector', ['discernment', 'QUALITY'], 'criterion from this round',
    f"Item N-12. Read {LESSON} Mistakes and Entry gate, {W}/w1/C2MutBinding.md, {W}/w1/C1CritChannels.md, {W}/w1/ConnClaims.md and {L}/corpus/QUALITY.md (criteria 79-91). Is a new QUALITY criterion warranted by a mistake this round mined (each criterion must cite a lesson row)? If yes, draft exact text (number 92, lesson id, failing example); if no, say why the existing criteria already capture each row.")
add('SentScopeFinal', 'sentinel', ['no-harm', 'scope'], 'misroot sweep',
    f"Item N-13. Near the end of your run (after ~20 min) sweep for scope violations by this wave: `git -C /home/vgpnk/Projects/shokunin status --porcelain`, `git -C {L} status --porcelain --ignored` (anything outside .ufo/waves/round-43/w2/, including tools/__pycache__), files under /tmp and /var/tmp naming tsukuroi-r43 or bootinputs newer than {W}/make-w2-spec.py, tmpfs mounts on the host (`findmnt -t tmpfs`) named r43lib/r43view, and leftovers under {SC}. Report each with path, size and owner seat. Read-only: delete nothing.")
add('SimplifierCounters', 'simplifier', ['quality'], 'counter YAGNI review',
    f"Item N-14. Advisory YAGNI review of {C1C} and {C2C} and the two control scripts in {W}/controls/: dead code, conjuncts no control exercises, duplication with tools/_revision.py or run-receipt.py. Propose deletions for a future counter version with the reason each preserves behaviour; nothing that changes a frozen predicate this round.")
add('CritSeparabilityFinal', 'critic', ['discernment'], 'causal separability at the tip',
    f"Item N-15. At {TIP}: can C1 be verified with C2's changes reverted and vice versa? Build both partial trees in scratch clones (C1-only: {BASE} + the boot-chain-audit.sh at {TIP}; C2-only: {BASE} + the entry, r42 entry, SOURCES.md and frozen files at {TIP}) and run each counter on both (C2 will FAIL only on verdicts_ok there; say which conjuncts move). Report whether either counter reads the other claim's surface.")
add('ScoutConsiderMapFinal', 'scout', ['quality', 'considerthese'], 'propagation map closed?',
    f"Item N-16. Re-run the dependent sweep of {W}/w1/ConsiderMap.md (its §5 grep commands) at {TIP}. For each dependent it listed as needing a pointer (README:410, PROVINCE:239-244, SKILL:3914, :3918, the LOG round-43 entry), is there now an append-only pointer or correction? List any dependent still unpointed, and any new dependent the round-43 edits created.")

spec = {'wave': 'tsukuroi-r43-w2', 'reportDir': '.ufo/waves/round-43/w2', 'maxLanes': 64,
        'context': CONTEXT, 'items': items}
names = [i['name'] for i in items]
assert len(names) == len(set(names))
(HERE / 'w2-spec.json').write_text(json.dumps(spec, indent=1, ensure_ascii=False))
c = Counter(i['role'] for i in items)
flash = sum(v for k, v in c.items() if k in ('executor', 'scribe', 'sonic', 'simplifier', 'critic', 'revenger', 'sentinel'))
attack = sum(v for k, v in c.items() if k in ('reviewer', 'critic', 'mutation-tester'))
print(len(items), dict(c), 'm_flash', flash, 'attack', attack)
