#!/usr/bin/env python3
# Round 47 wave w1 spec generator (L1). Emits .ufo/waves/round-47/w1-spec.json.
import json
from collections import Counter

L = '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin'
W = f'{L}/.ufo/waves/round-47'
WD = f'{W}/w1'
SC = '/fast/scratch/hyaku/tsukuroi-r47'
BASE = '916019057147d7e9ba6b137647b2cee26decf4b8'
FREEZE = '77e9e2b2e96b85d8f048ae2087e246a542b71611'
IMPL = FREEZE
CEN = f'{L}/tools/tsukuroi-census.sh'
C1C = f'{L}/tools/check-scrub-admission-r47.py'
C1SHA = 'e20c322171db76f1d08b51066e602707516f62eccdf3f64ca8356c69767f023b'
ENTRY = f'{L}/corpus/knowledge/btrfs-scrub-grounding-r45.md'
SRC45 = f'{L}/.ufo/waves/round-45/frozen/src'
SRC44 = f'{L}/.ufo/waves/round-44/frozen/src'
PSCRUB = f'{L}/.ufo/waves/round-42/frozen/src/scrub.c'
CAP = f'{L}/.ufo/waves/round-45/frozen/hostcap'
SRC47 = f'{W}/frozen/src'
SHOKU = '/home/vgpnk/Projects/shokuknow/merge/tsukuroi'
HASH = {'GR1': 'fe77ac765c7dd9f568e0b296ce8c7f8f53de3d8966d6a2029bada662badf9ca8',
        'GR2': '909830c83cbcf0a02264153fa6f179415fb8388d3e08c43d79fbf33c8cfa11a2',
        'GR3': '43430a14069598947d225c1f8ae897d9baea1c0e268cb88c2b5ad9e247bbc32c'}

GODSPEED = """/skill:godspeed
1. **Name the axes.**
2. **Iterate cheap, in parallel.**
3. **Keep moves that improve any axis and harm none.**
4. **Don't aim — let the frontier walk itself.**
IMMEDIATELY STOP ASKING CLARIFYING QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can run in parallel. Do not output philosophical reasoning or verbose plans. Act directly via tool calls."""

CONTEXT = f"""{GODSPEED}

You are an L2 seat of tsukuroi lane round 47 (hyaku run 10, fresh-start round after three consecutive rejected closures), wave w1: the round's one v2 wave (build, falsify, and the counted verdicts of claim C1). The L1 (agent TsukuroiR47) holds the planner seat and is the only integrator and committer. Lane repo: {L} (host operability and repair on this Arch/omarchy host: package, systemd, driver, journal, update-safety, OOM planes; boot-chain audit; btrfs error counters and the unprivileged scrub-record view).
Declared, frozen claims (SCORECARD.md section "Round 47 — declaration"; impl commit {IMPL} = the freeze revision counted seats read; base {BASE}, the lane tip at round start):
- C1 depth: the pending rows GR1 (memparse as the scrub_speed_max write parser), GR2 (a device replace runs btrfs_scrub_dev with is_dev_replace true; non-replace scrubs refused with EINPROGRESS during a replace — AMENDED this round: the filesystem-closing -EAGAIN check leads the ordering, and the suspend sentence is narrowed to the unmount path), GR3 (systemctl stop of btrfs-scrub@.service under systemd v262: SIGINT to the control group, SIGCONT, SIGKILL after TimeoutStopSec; 5 s on this host) of {ENTRY} are admitted only if counted seats bind verdicts on current section bytes. Frozen counter {C1C} (sha256 {C1SHA}; `git -C {L} show {IMPL}:tools/check-scrub-admission-r47.py | sha256sum`): `python3 {C1C} --revision <REV>`; predicate `structural_ok == 1 and quotes_ok == 3 and verdicts_ok == 3 and marks_ok == 3`. Row extent bound: `## GR<n>` up to (exclusive) the expected next header (GR1->`## GR2`, GR2->`## GR3`, GR3->`## How this changes OS triage`); any other `## ` line inside fails closed. Sources: S246 ({SRC45}/cmdline.c, vsprintf.c, kstrtox.c), S247 ({SRC45}/dev-replace.c), S248 ({SRC45}/systemd.kill.xml), S242 ({SRC44}/scrub.c), S243 ({SRC44}/sysfs.c), S244 ({SRC44}/btrfs-scrub@.service), S237 ({PSCRUB}), S249 ({CAP}/capture.txt, own-work); digests in each dir's SHA256SUMS.
- C2 operability (sourced S252 mktemp(1), snapshot {SRC47}/mktemp.html + SHA256SUMS + FETCH.txt): the census selftest under a TMPDIR containing a space failed 13/162 at base; the harness now derives a classifiable fixture base (root_locator_class charset, falling back to /tmp) plus two (R47-C2) pinning cases. Counting command (frozen): `S=<scratch>; mkdir -p "$S/t 2"; env -i PATH=/usr/bin:/bin LC_ALL=C TMPDIR="$S/t 2" bash {CEN} --selftest` -> PASS (164 cases, 164 passed, 0 failed), rc 0. Kill rules: live census output digits-stripped byte-identical base vs final; --identity line shape unchanged; all six (R46-C1) cases still pass; exit map unchanged.
- The counted C1 seats bind through committed report bytes only: {C1C} reads .ufo/waves/round-47/<wave>-dispatch.json, <wave>-results.json and the seat's .md report; a seat binds one row only when its FIRST line is exactly `ROW GR<n> VERDICT: <holds|partly|fails>` and its SECOND line exactly `SECTION SHA256: <64-hex>`. Seat names are frozen (R47RevGR<n>a/b, R47CritGR<n>a/b, R47ResRevGR<n>, R47ResCritGR<n>; the R47Res2* generation is held for a possible second amendment).
- Battery: {W}/controls/battery.py + battery-summary-r47.jsonl (12 controls). Before receipts: {W}/before/ and /fast scratch logs (the L1's). Round-46 wave evidence: {L}/.ufo/waves/round-46/.

Rules for every seat (host guard):
- Your tools start at the fleet root /home/vgpnk/Projects/shokunin: cd into your scratch dir first and use absolute paths everywhere. Never write a tracked file of the fleet repo or of any lane; never write under /home/vgpnk/.local/bin or any PATH directory; never plant shims; never create files at the fleet root (a shell redirect there is a misroot).
- Read-only on lane content: never edit, create or delete any tracked lane file; never run git add/commit/stash/checkout/reset/push or any mutating jj command in the lane; never touch the lane's Git index or jj state, the fleet repo, any sibling lane, or /home/vgpnk/Projects/shokuknow (read-only source; never run its campaign tools). Never mutate the host: no package, service, unit start/stop/enable/disable, timer, sysfs write, mount outside a private `unshare` namespace, boot, /etc or /var/lib change; no sudo; never run `btrfs scrub start/cancel/resume`, `btrfs replace`, `btrfs scrub limit -l`, `btrfs device stats -z`, `systemctl enable|start|stop|kill`; never write scrub_speed_max. Read-only queries (`systemctl show`, `systemctl cat`, `systemd-analyze cat-config`, journalctl, findmnt, sysfs reads) are fine.
- Write ONLY your report and your receipts. Every `Report:` trailer path is relative to {L} — write it at {L}/<that path> (absolute), i.e. {WD}/<your seat name>.md. Small receipts (under 2 MB each) go in {WD}/<your seat name>/ (create it). Never write anywhere else in the lane or under the fleet root.
- Scratch: every clone, copy, mutant or fixture lives under {SC}/<your seat name>/ (mkdir -p; export TMPDIR there, NOT a path with a space unless your item says so). Never build under /tmp. Remove your scratch dir before you finish (trap 'rm -rf -- "$S"' EXIT), after copying receipts into your seat dir. A /tmp path is never evidence.
- Fixture git repos: D=$(mktemp -d {SC}/<seat>/fx.XXXXXX) && git -C "$D" init -q; every later git call names -C "$D"; verify `git -C "$D" rev-parse --show-toplevel` equals $D before the first commit; never commit with a throwaway identity anywhere else. To score a variant: git clone -q --shared {L} "$D"; git -C "$D" remote remove origin; toplevel check; commit the variant with `-c user.name=fixture -c user.email=fixture@invalid`; run a counter with `--lane "$D" --revision <sha>`.
- Tooling authorization (operator, 2026-10-19): you may install or upgrade tools that help the task — read /home/vgpnk/.omp/agent/RULES.md first (official channels, update-safety gate; record tool/version/channel/reason in your report). pacman guard: ALL pacman transactions are PAUSED host-wide — never pacman -S/-Sy/-Syu/-U/-R; install only via uv tool / npx / an official binary in ~/.local/bin; never restart a host service.
- You are a leaf: do not spawn agents (executors may spawn at most one read-only labrat), do not run a swarm, never message agent://all.
- Cost: the census selftest takes ~30-50 s (~6 CPUs). Never run more than one selftest or heavy counter at a time in your seat; serialize the identity counter if your item needs it.
- Evidence: every claim in your report carries a path:line, a command with its observed output, or a URL with access date and a <=25-word located quote. An unrun check has not passed; say what you did not do. Report findings even when they falsify the claims — that is the point.
- Report format: the FIRST line of your report file is `VERDICT: <supports|falsifies|defect-found|draft|no-finding>` for your item, then evidence, then exact proposed text where your item asks for a draft. The eighteen counted C1 seats (names R47RevGR<n>a/b, R47CritGR<n>a/b, R47ResRevGR<n>, R47ResCritGR<n>) use the two exact first lines their item names instead. The L1 reads your REPORT FILE, never your yield: write the report file first, then yield one short line naming its path.
"""

items = []


def add(name, role, axes, milestone, body):
    items.append({'name': name, 'role': role, 'axes': axes, 'milestone': milestone,
                  'prompt': GODSPEED + '\n' + body.strip()})


CLONE = (f'(score variants in a scratch clone: git clone -q --shared {L} "$D" under {SC}/<seat>/, '
         'remove origin, toplevel check, commit with `-c user.name=fixture -c user.email=fixture@invalid`, '
         'then run the counter with --lane "$D" --revision <sha>)')

ROWSRC = {
    'GR1': f'{SRC45}/cmdline.c, {SRC45}/vsprintf.c, {SRC45}/kstrtox.c (S246) and {SRC44}/sysfs.c (S243)',
    'GR2': f'{SRC45}/dev-replace.c (S247), {SRC44}/scrub.c (S242), {SRC44}/sysfs.c (S243)',
    'GR3': f'{SRC45}/systemd.kill.xml (S248), {SRC44}/btrfs-scrub@.service (S244), {PSCRUB} (S237) and {CAP}/capture.txt (S249)',
}

# ---------------- C1: counted verdicts (18) ----------------
for row in ('GR1', 'GR2', 'GR3'):
    n = row[2:]
    for nm, role, stance in ((f'R47RevGR{n}a', 'reviewer', 'review'), (f'R47RevGR{n}b', 'reviewer', 'review'),
                             (f'R47CritGR{n}a', 'critic', 'attack'), (f'R47CritGR{n}b', 'critic', 'attack'),
                             (f'R47ResRevGR{n}', 'reviewer', 'review'), (f'R47ResCritGR{n}', 'critic', 'attack')):
        add(nm, role, ['depth', 'C1', row, 'counted'], f'counted verdict {row}', f"""
Item C1-{row}-{nm} (COUNTED verdict for claim C1). Your job: {stance} row {row} of {ENTRY} at revision {IMPL} and decide whether it is admissible knowledge.
1. Read the row: everything from the line `## {row}` up to (not including) the row's expected next header — {'`## GR2`' if row == 'GR1' else '`## GR3`' if row == 'GR2' else '`## How this changes OS triage`'} — in `git -C {L} show {IMPL}:corpus/knowledge/btrfs-scrub-grounding-r45.md`. Also read the entry's `## Limits` section for context (round 47 GR2 was amended pre-wave per `.ufo/waves/round-46/r1/V46ResCritGR2.md`; judge the CURRENT bytes, not the history).
2. Compute the row's section hash: `python3 {C1C} --revision {IMPL} --section-hash` and take the value for {row} (expected {HASH[row]}; if they differ, use what the command prints and say so). Also re-derive it yourself: sha256 over the LF-joined lines from `## {row}` up to (exclusive) its expected next header.
3. Verify `sha256sum` of each snapshot you use against its SHA256SUMS ({SRC45}/SHA256SUMS, {SRC44}/SHA256SUMS; S237 against {L}/.ufo/waves/round-42/frozen/src/SHA256SUMS; {CAP}/capture.txt digest is in the entry header). Snapshots for this row: {ROWSRC[row]}.
4. For EVERY clause of the row's **Statement** and **Host reading**: open the quoted line(s) and the surrounding code/doc in the snapshot and decide whether the clause follows from them. Check that each `**Quote.**` text is on its cited line. Check that every [inference] mark sits where the pinned source stops, and that nothing stated as fact goes beyond the quoted lines.
5. Verdict words: `holds` = every clause is supported by the cited lines (inference marks correctly placed); `partly` = at least one clause overreaches or is imprecise but the row's core is right (name the clause and give exact replacement text); `fails` = a central clause is false against the source.
6. Write your report at {WD}/{nm}.md. Its FIRST line must be exactly `ROW {row} VERDICT: <holds|partly|fails>` and its SECOND line exactly `SECTION SHA256: <the 64-hex hash from step 2>` — no blank line before, no leading/trailing spaces, no markdown, no code fence, no BOM, LF line ends. Then your evidence: one bullet per clause with the snapshot `<file>:<line>` you read (e.g. `scrub.c:3094`) and why it supports or contradicts the clause — every file:line you cite must resolve in the pinned snapshots (the counter now verifies this). Do NOT write any other line of the form `ROW GR<d> VERDICT: <word>` anywhere else in the file. This file is the ONLY channel the frozen counter reads; your yield is ignored.
7. Yield one short line naming the report path. Read-only: change no lane file.""")

# ---------------- C1 support ----------------
for i in (1, 2, 3):
    add(f'C1RevCounter{i}', 'reviewer', ['depth', 'C1', 'counter'], f'counter review pass {i}', f"""
Item C1-R{i}. Review the frozen counter {C1C} (sha256 {C1SHA}; `git -C {L} show {IMPL}:tools/check-scrub-admission-r47.py | sha256sum`) against its docstring and the declaration in {L}/SCORECARD.md ("Round 47 — declaration", C1 row). It is the round-46 counter amended for the wave findings: F1 (row extent bound to the expected next header), F2 (marks ungrantable to negations), F3 (parse failures in-band), K22 (entry Quote lines verified on digest-pinned snapshots; seat-report citations must resolve), K23 (bound report bodies pairwise distinct). Does every leg do what the docstring and declaration say (same predicate sentence in code, docstring, receipt labels)? Find binding holes the battery does not cover: a seat binding without a spawn, a verdict bound to unread bytes, quorum by one seat, wave-name dependency, duplicate JSON keys, report-path traversal, the snapshot map (could a quote verify against the wrong file or a moved snapshot slip a pin?), the exact-line marks, the distinct-body rule (is whitespace-normalized identical content caught?), the universe regex of seat names. {CLONE} for any repro. Report VERDICT and findings F1..Fn, each with path:line.""")

add('C1MutBinding', 'mutation-tester', ['depth', 'C1', 'counter'], 'counter mutation',
    f"""Item C1-M1. Mutation-test the counter's binding: copy {C1C} into {SC}/C1MutBinding/, apply single mutants one at a time (drop the dispatch-count==1 check; drop the agent check; drop the results.json check; accept `\\r` in the first lines; skip the contradiction scan; lower the quorum to 1; ignore `fails` on old hashes; drop the 300-byte or citation rule; accept a quote against the wrong snapshot; skip the distinct-body check; drop one mark), and re-run the committed battery {W}/controls/battery.py against each mutant (adapt it to point COUNTER at the mutant; scratch only). Report a kill matrix (mutant x control) and every SURVIVOR with a proposed new control.""")

add('C1CritBattery', 'critic', ['depth', 'C1', 'controls'], 'battery attack',
    f"""Item C1-R4. Attack the pre-data battery ({W}/controls/battery.py, battery-summary-r47.jsonl): is each control what its name says and did each FAIL for its intended reason? Which cheap writer is missing — e.g. a report citing a REAL snapshot line that is the WRONG line for its claim (cites resolves, clause false), a seat of another lane's wave directory, a verdict on a hash of the wrong row, whitespace-only distinct bodies, a `partly` on current bytes that the quorum still admits? Build one or two missing controls {CLONE} and score them.""")

add('C1CritQuorum', 'critic', ['depth', 'C1', 'discernment'], 'quorum rule attack',
    f"""Item C1-R5. Attack the C1 admission rule itself as discernment: a row is admitted with >= 2 bound `holds` on its current bytes, any roles among up to 8 seats, no bound `fails`. Is 2 of 8 enough? Should reviewer AND critic both be required? Does per-row admission (vs r46's all-or-nothing predicate) plus the residual generations invite amendment-shopping? Compare with {L}/corpus/QUALITY.md criteria 81, 89, 90, 93 and the lessons R46-C2-RESIDUAL-UNIVERSE-ONE-SHOT, R45-C2-BINDING-CHANNEL. Give a verdict and, if the rule is weak, the exact rule you would freeze next round (do not ask to change this round's frozen rule).""")

add('C1CritAmend', 'critic', ['depth', 'C1', 'GR2'], 'amendment fidelity attack',
    f"""Item C1-R6. Attack the GR2 amendment: diff `git -C {L} show {BASE}:corpus/knowledge/btrfs-scrub-grounding-r45.md` against {IMPL} limited to the `## GR2` section and `## Limits`. The counted residual critic's exact corrections were (read {L}/.ufo/waves/round-46/r1/V46ResCritGR2.md in full): add the fs-closing -EAGAIN ordering and narrow the suspend sentence to the unmount suspend path. Did the amendment apply BOTH corrections exactly, or did it drift (added claims beyond the correction, or weakened wording that still overreaches)? Re-verify every clause of the new Statement against {SRC44}/scrub.c:3090-3160 and {SRC45}/dev-replace.c:1143-1144,1180-1245,1265-1300. Report per-clause verdicts.""")

add('C1RevAmend', 'reviewer', ['depth', 'C1', 'GR2'], 'amendment review',
    f"""Item C1-R7. Review the amended GR2 row as knowledge: read `git -C {L} show {IMPL}:corpus/knowledge/btrfs-scrub-grounding-r45.md` `## GR2` and `## How this changes OS triage`/`## Limits`. Between scrub.c:3095 (-EAGAIN) and :3109 (scrub_setup_ctx) there is an ASSERT about nodesize (scrub.c:3097-3100 region — check) — does the new ordering paragraph mislead anywhere about what runs between the fs-closing check and the context setup? Is the triage bullet consistent with the narrowed suspend claim? Does `## Limits` still contain text contradicted by the amendment (e.g. the round-45 narrowing history vs the new unmount-only claim)? Report per-point verdicts with line refs.""")

add('C1RevQuotes', 'reviewer', ['depth', 'C1', 'quotes'], 'independent quote audit',
    f"""Item C1-R8. Independently verify every `**Quote.**` line in `## GR1`, `## GR2`, `## GR3` of `git -C {L} show {IMPL}:corpus/knowledge/btrfs-scrub-grounding-r45.md` (52 lines expected) against the pinned snapshots: write your OWN parser (do not import the counter), map each `S###`/`file`/`line` to {SRC45}, {SRC44}, {PSCRUB} or {CAP}/capture.txt, sha256sum the snapshot first, then compare the quoted text to the cited line with whitespace normalization. Report a table: row, quote line, cite, verify/fail. Also flag any claim clause that has NO quote at all (host-reading values cite capture.txt by line; check those lines too).""")

add('C1ExecGatePred', 'executor', ['depth', 'C1', 'kill-rule'], 'predecessor counters',
    f"""Item C1-K1 (kill rule 'predecessor scrub counters PASS->PASS where measured'). Run at {BASE} and at {IMPL}, each `--revision <rev>`: tools/check-scrub-record-r42.py, tools/check-scrub-record-r43.py, tools/check-scrub-record-r44.py, tools/check-scrub-grounding-r45.py, tools/check-scrub-admission-r46.py, and tools/check-adjacency-anchors.py (read each --help first). Receipts in {WD}/C1ExecGatePred/<tool>-<rev8>.json. Report verdicts base vs impl per counter and every differing field (r44/r45/r46 counters are FAIL at base by design: verdicts_ok 0 — a FAIL->FAIL is not a violation).""")

add('C1ExecKillLive', 'executor', ['operability', 'C1+C2', 'kill-rule'], 'live census diff',
    f"""Item C1-K2 (kill rule 'live census output digits-stripped byte-identical base vs final'). Run `env -i PATH=/usr/bin:/bin LC_ALL=C bash <(git -C {L} show {BASE}:tools/tsukuroi-census.sh)` and `env -i PATH=/usr/bin:/bin LC_ALL=C bash {CEN}` from {SC}/C1ExecKillLive/, capture stdout+stderr+rc of both, strip [0-9] and diff (also unstripped for the record). Do the same for `--identity` (line shape: fields, planes, exit_map order — the digests legitimately differ). Report the diffs (expected: none digits-stripped) and every real difference.""")

add('C1ExecEntryDiff', 'executor', ['depth', 'C1', 'scope'], 'entry scope diff',
    f"""Item C1-K3 (scope kill rule 'GR1/GR3 section hashes equal to base'). Run `python3 {C1C} --revision {BASE} --section-hash` and `--revision {IMPL} --section-hash`; report the three hashes at each. Also `git -C {L} diff {BASE} {IMPL} -- corpus/knowledge/btrfs-scrub-grounding-r45.md` and confirm: only GR2's statement/quotes and the appended Limits bullet changed inside the row extents; no `## ` line exists inside a row; the marks lines are absent at IMPL (marks are written post-wave). Report the diff stat and every changed hunk inside the row extents.""")

add('C1SentSafety', 'sentinel', ['depth', 'C1', 'security'], 'counter safety review',
    f"""Item C1-S1. Security-review {C1C}: it runs `git -C <lane> show|ls-tree|rev-parse|merge-base` and python json/sha256 on repo bytes. Attack surfaces: a lane path escape via --lane, a rev injection via --revision, seat names containing `/` or `..` reaching a `git show` pathspec, regex DoS on huge reports (VERDICT_RE/CITE_RE/QUOTE_RE), unicode edge cases in verdict lines (homoglyph, NBSP), snapshot-digest spoofing via a second file with the same sha256 path. {CLONE} for repros. Report VERDICT and findings.""")

add('C1SentForge', 'sentinel', ['depth', 'C1', 'security'], 'bind forging attempt',
    f"""Item C1-S2. Try to bind a seat that was never spawned: in a scratch clone {CLONE}, craft .ufo/waves/round-47/wX-dispatch.json + wX-results.json + a seat report without the orchestrator's dispatch (the standing documented limit: committed bytes cannot tell forged records from real ones). Which additional evidence WOULD distinguish a forged bind (results.json agent ids, seat transcripts, timing)? Report what binds and what the lane could add next round to make forgery detectable. Do NOT write any real wave files in the lane.""")

add('C1ScribeGate', 'scribe', ['depth', 'C1', 'marks'], 'marks text draft',
    f"""Item C1-D1. Draft (as report text only; the L1 lands these on a counter PASS) the exact admission marks: (a) the entry block starting with the exact line `## Gate status — round 47 (GR1-GR3 admitted)` (name the revision, the counter, the counted seats that bound, the amendment history in one paragraph); (b) a SKILL.md section starting with the exact line `## Scrub grounding — round 47 admission` (3-8 lines: what the three admitted rules now say and where to read them); (c) the corpus/README.md line containing `btrfs-scrub-grounding-r45.md` and `admitted round 47` without any negation word. Read {L}/corpus/README.md's row style and {L}/SKILL.md's section style first. Also draft the lesson `## Gate` row for the S252 reject/new rows table as needed by {L}/corpus/lessons/round-47.md.""")

# ---------------- C2: operability / selftest TMPDIR ----------------
add('C2ExecRerunA', 'executor', ['operability', 'C2'], 'selftest re-run A',
    f"""Item C2-1. Reproduce the C2 counting command at {IMPL}: `S={SC}/C2ExecRerunA; mkdir -p "$S/t 2" "$S/h"; env -i PATH=/usr/bin:/bin HOME="$S/h" LC_ALL=C TMPDIR="$S/t 2" bash {CEN} --selftest` and again with TMPDIR="$S/t" (no space). Save both logs to {WD}/C2ExecRerunA/. Report rc, the PASS/FAIL line and case counts (expected: PASS 164/164 both). Also run the base census the same way: `git -C {L} show {BASE}:tools/tsukuroi-census.sh > $S/census-base.sh` under the space TMPDIR (expected FAIL 149).""")

add('C2ExecRerunB', 'executor', ['operability', 'C2', 'stability'], 'selftest re-run B',
    f"""Item C2-2. Independent environment: clone {L} at {IMPL} into {SC}/C2ExecRerunB (git clone -q --shared, remove origin, checkout {IMPL}); run `env -i PATH=/usr/bin:/bin HOME=<h> LC_ALL=C TMPDIR="<scratch with a space>" bash <clone>/tools/tsukuroi-census.sh --selftest` and once more with LC_ALL=en_US.UTF-8 if available. Report rc and the final line for each; name any divergence. Copy both logs to {WD}/C2ExecRerunB/.""")

add('C2ExecTmpdir', 'executor', ['operability', 'C2', 'edges'], 'TMPDIR edge cases',
    f"""Item C2-3. Edge-case the selftest under: TMPDIR with a trailing space, with a TAB inside, with a NEWLINE inside, a relative TMPDIR, an empty TMPDIR, and TMPDIR unset (env -u TMPDIR). For each: `env -i PATH=/usr/bin:/bin HOME=<h> LC_ALL=C TMPDIR=<case> bash {CEN} --selftest`, record rc + final line into {WD}/C2ExecTmpdir/<case>.log (mktemp may itself fail on some shapes — record what happens honestly). Which shapes does `root_locator_class` (in {CEN}) refuse? Cross-check the fallback triggers exactly on the classifier's unsafe charset. Report a table.""")

add('C2MutFix', 'mutation-tester', ['operability', 'C2', 'counter'], 'fix mutation',
    f"""Item C2-4. Mutation-test the C2 fix on a scratch copy of {CEN}: (a) remove the st_base guard but keep the (R47-C2) cases (the fixture base then fails under a space TMPDIR — do the cases FAIL as designed?); (b) make the fallback path unsafe too (e.g. st_base=/nonexistent path) and see whether the failure mode is still legible; (c) remove one of the two R47-C2 cases and check the PASS still means the other case covered the contract. Run each mutant under a space TMPDIR {SC}/C2MutFix/m*/. Report a kill matrix.""")

add('C2MutCases', 'mutation-tester', ['operability', 'C2'], 'case weakening attack',
    f"""Item C2-5. Can the two new (R47-C2) selftest cases be weakened into always-pass? On a scratch copy: (a) weaken `root_locator_class` to accept whitespace — does any case then catch a regression? (b) make `work` an empty string — do the cases fail or silently skip? (c) corrupt the fixture `sp dir` path so it lacks a space — does the unsafe pin still trip? Report which mutations survive and whether a third case is needed.""")

add('C2RevFix', 'reviewer', ['operability', 'C2'], 'fix review',
    f"""Item C2-R1. Review the C2 fix in {CEN} (diff `git -C {L} show {BASE}:tools/tsukuroi-census.sh` vs {IMPL}): the st_base guard, the two (R47-C2) cases, the two comment/usage updates. Is falling back to /tmp the right design vs (i) failing the selftest fast when TMPDIR is unsafe, (ii) creating a space-free subdir under TMPDIR? Does the guard change any LIVE-mode path (it should not — prove by reading the code)? Do the cases actually pin the contract or only the current implementation? Report per-change verdicts.""")

add('C2CritKill', 'critic', ['operability', 'C2', 'claim'], 'claim attack',
    f"""Item C2-R2. Attack claim C2 itself: (a) is the defect in scope — `root_locator_class`'s whitespace refusal is deliberate (census comments: `=` and whitespace rejected so a path like `/x root_mode=0755` cannot forge a token); does the fix blur a deliberate security boundary? (b) The declared target `PASS (164 cases, 164 passed, 0 failed) rc 0` — can a do-nothing control reach it? (prove: the pre-fix file FAILs 149). (c) Does the target underspecify — e.g. a TMPDIR with a different unsafe character, a TMPDIR that is a symlink, unwritable TMPDIR? Run the checks read-only and report. (d) Does `bytes=212252 lines=3644` of the identity line vs base `209208/3598` change shape? Report per-point.""")

add('C2ScoutMktemp', 'scout', ['freshness', 'C2', 'S252'], 'S252 re-open',
    f"""Item C2-6. Re-open S252 live: `curl -fsSL --max-time 30 https://man7.org/linux/man-pages/man1/mktemp.1.html` into {SC}/C2ScoutMktemp/, sha256sum vs {SRC47}/SHA256SUMS, `cmp` vs {SRC47}/mktemp.html. Confirm the located quote ("-t interpret TEMPLATE as a single file name component, relative to a directory: $TMPDIR, if set") is on the page (strip HTML). Empirically verify read-only: `TMPDIR=<scratch>/no\\ such\\ dir mktemp -d 'x.XXXX'` and `TMPDIR=<scratch-with-space> mktemp -d <scratch>/t.XXXXXX` — does mktemp honor a space TMPDIR? Report the digest compare, the quote, and the empirical result.""")

add('C2ExecKillRules', 'executor', ['operability', 'C2', 'kill-rule'], 'C2 kill rules',
    f"""Item C2-K4. C2 kill rules at {IMPL}: (a) `env -i PATH=/usr/bin:/bin LC_ALL=C bash {CEN} --selftest` (space-free TMPDIR) — expected PASS 164/164 including the 8 (R46-C1) and 2 (R47-C2) labels (grep -c each). (b) `bash {CEN} --identity` line shape: one line, fields version/sha256/md5/bytes/lines/planes/exit_map/verified in order, verified=yes. (c) `bash {CEN}` live run vs base (digits-stripped diff, as C1ExecKillLive does — coordinate not to collide: use {SC}/C2ExecKillRules). (d) `bash {L}/tools/boot-chain-audit.sh --selftest` still PASS 49/49. Receipts in {WD}/C2ExecKillRules/.""")

add('C2ExecSelftest', 'executor', ['operability', 'C2', 'identity'], 'r46 counter at impl',
    f"""Item C2-K5. Run the frozen round-46 counter's selftest legs at {IMPL}: `python3 {L}/tools/score-census-identity-r46.py --revision {IMPL} --scratch {SC}/C2ExecSelftest/s` (one run; ~2.5 min; TMPDIR={SC}/C2ExecSelftest). Report each leg — expected: identity_ok 1, selftest_pass 1 (the counter tolerates the new case count), selftest_r46 >= 6. If a leg fails, report whether it is a real regression or an underspecification of the frozen counter. Copy the JSON line to {WD}/C2ExecSelftest/.""")

add('C2ScribeEntry', 'scribe', ['operability', 'C2', 'draft'], 'evidence draft',
    f"""Item C2-D1. Draft (report text only) a short knowledge note paragraph for the lesson explaining the TMPDIR-space contract: the deliberate whitespace refusal of root_locator_class ({CEN}, read it), the fixture-base derivation now in run_selftest, the two pinning cases, and the S252 quote grounding mktemp's TMPDIR rule. Also draft the before->after measurement line for the report: base `FAIL (162 cases, 13 passed, 149 failed)` -> `PASS (164 cases, 164 passed, 0 failed)` under the frozen counting command. Exact prose.""")

add('C2SentTmp', 'sentinel', ['operability', 'C2', 'security'], 'tmp fallback safety',
    f"""Item C2-S2. Security-review the /tmp fallback in run_selftest ({CEN}): does a predictable ${{-}}-prefix-free mktemp dir under /tmp open a symlink/race hole another local user could exploit (selftest runs as uid 1000)? Is `chmod -R u+rwx`/`rm -rf` on the work tree safe if TMPDIR were attacker-controlled (e.g. TMPDIR=/)? Could an attacker-controlled TMPDIR make the census itself read/write outside the work dir (it only writes under `work` — verify)? Report VERDICT and any real hole.""")

add('C2CritTMP', 'critic', ['operability', 'C2', 'design'], 'fallback design attack',
    f"""Item C2-R3. Attack the design choice: falling back to /tmp means the selftest no longer honors the caller's TMPDIR at all — should it instead create a private space-free subdir (e.g. under XDG_RUNTIME_DIR or a mktemp under /tmp only when TMPDIR is unsafe, as implemented)? Is writing under /tmp acceptable at all given the lane's own scratch discipline (scratch rule 1: /tmp only for files under 50 MB — the selftest tree fits)? Compare with the run-46 finding's own proposal ({L}/.ufo/waves/round-46/w1/C1ExecRerunB.md §4) and {L}/.ufo/prompts/tsukuroi-round-47.md §7. Give a verdict and the alternative you would prefer, with evidence.""")

# ---------------- frontier / general ----------------
add('SrcGate', 'scribe', ['sources', 'frontier'], 'SOURCES curation',
    f"""Item F-1. Sources discipline for round 47: (a) verify the S252 row in {L}/corpus/SOURCES.md parses (11 columns, no literal or escaped `|` inside a cell, valid recheck cell, used-by names a real file); run `{L}...` — the census is `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` — and record exit + row count. (b) re-check every row the round touches old->new: `git -C {L} diff {BASE} {IMPL} -- corpus/SOURCES.md` should be only the S252 insertion. (c) draft the lesson `## Gate` new-row table entry for S252 (URL, access date 2026-10-27, located quote <=25 words, location) and confirm the row's quote appears verbatim on the fetched page ({SRC47}/mktemp.html, strip HTML). Report each check with output.""")

add('AsmGate', 'scout', ['sources', 'assimilation'], 'assimilation gate',
    f"""Item F-2. Assimilation check for round 47 (read-only source): read {SHOKU}/MERGE-REPORT.md and {SHOKU}/SOURCES.append.md header; re-derive the tsukuroi slice of /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md (data rows only, the lane cell `tsukuroi`): how many rows and which S-ids? Re-run the collision check: `grep -oE '^ {{0,3}}\\|[[:space:]]*S[0-9]{{3,}}' {L}/corpus/SOURCES.md | grep -oE 'S[0-9]+' | sort` vs the same on {SHOKU}/SOURCES.append.md; count intersections. Is there a staged theme that fits this round's surfaces (scrub grounding / census TMPDIR contract)? Verdict: assimilate <theme> or none, with evidence. Do not run any campaign tool; shokuknow is read-only.""")

add('ConsGate', 'scout', ['sources', 'considerthese'], 'considerthese mine',
    f"""Item F-3. Mine {L}/considerthese/ (operator-authored; never edit): list files (`ls {L}/considerthese/`), read the newest three (2026-10-24/25/26), and name every item that is (a) still unimplemented and (b) relevant to this round's claims (counter/verdict binding, selftest harness robustness, scrub grounding). For each relevant proposal: what it points at, whether already covered by this round's work, and what would land it (lesson, QUALITY criterion, SOURCES row). Round 46 mined 'Burst-aware reading' from 2026-10-26.md — check whether it landed or is still open.""")

add('LessonScribe', 'scribe', ['depth', 'lesson'], 'lesson verification',
    f"""Item F-4. Verify {L}/corpus/lessons/round-47.md: read it and check (a) the three Mistakes rows cite real evidence (verify each path/commit exists: `git -C {L} cat-file -e` / read the file); (b) draft (report text) the `## Round-46 routed defects — round-47 disposition` table: the r46 spotcheck defects D1-D10 and the carried items (read {L}/corpus/lessons/round-46-verifier-spotcheck.md §5 tail and the round-46 lesson's routed table), each with state at {IMPL} and evidence command; (c) draft `## Assimilation and considerthese` and `## Spot-check candidates` sections. Exact markdown, evidence per row.""")

add('ScoutKillRule', 'scout', ['depth', 'claims', 'do-nothing'], 'control audit',
    f"""Item F-5. Do-nothing control audit: would either claim's counter PASS without the round's work? (a) Run `python3 {C1C} --revision {BASE}` (expected FAIL — which legs?) and the C2 counting command on the BASE census extracted to scratch. (b) Check the cheapest shortcut writer per claim: could marks alone, or a forged wave, or a counter bypass reach PASS? (c) Any committed line since {BASE} that already satisfies a claim leg without the work? Report commands and outputs.""")

add('ScoutQuality', 'scout', ['depth', 'QUALITY'], 'quality criteria sweep',
    f"""Item F-6. QUALITY.md sweep ({L}/corpus/QUALITY.md, 183 lines): which numbered criteria does the amended GR2 row, the new counter, and the TMPDIR fix touch (5 source rejects, 8 headers, 9 negative host claims, 10 mention sweeps, 12 pinned mechanisms, 86 own-work citations, plus any criterion on counters/verdicts the wave added in earlier rounds — grep QUALITY.md for 'counter', 'bind', 'verdict')? For each: does the current state comply? Report criterion number, text, compliance with evidence.""")

add('ExecSelfAssess', 'executor', ['calibration', 'gate'], 'self-assessment run',
    f"""Item F-7. Run `python3 {L}/tools/check-self-assessment.py --revision {IMPL}` and report all 27 checks + mismatches (read --help first). If SCORECARD's self-assessment table now diverges (e.g. the operability cell says 162 cases while the census now prints 164), report exactly which check fails or is stale. Receipt into {WD}/ExecSelfAssess/.""")

add('ScoutHostScrub', 'scout', ['depth', 'C1', 'GR2'], 'host scrub state',
    f"""Item F-8. Re-check the host scrub sysfs state read-only for GR2's host-reading truth: read `/sys/fs/btrfs/*/exclusive_operation`, `/sys/fs/btrfs/*/devinfo/*/replace_target`, `systemctl show btrfs-scrub@-.service -p KillMode,KillSignal,TimeoutStopUSec,FinalKillSignal,SendSIGKILL`, `pacman -Qo /etc/systemd/system.conf.d/10-faster-shutdown.conf`, and `cat /etc/systemd/system.conf.d/10-faster-shutdown.conf`. Compare with {CAP}/capture.txt values (lines 1,2,3,4,5,8,9). Report each line: same/changed.""")

add('ConnRows', 'connector', ['depth', 'C1', 'consistency'], 'row consistency',
    f"""Item F-9. Cross-row consistency read: the amended GR2 at {IMPL} vs `## How this changes OS triage`, `## Limits`, and the round-44 entry {L}/corpus/knowledge/btrfs-scrub-record-r44.md (its `## Round-45` and SR7/SR8/SR9 references — does anything there contradict the admitted-form claims?). Also the SKILL.md scrub section — which lines become stale when the rows admit? Report each contradiction or stale line with path:line, or 'none' with the commands you ran.""")

add('ConnWave', 'connector', ['depth', 'pattern'], 'cross-lane pattern',
    f"""Item F-10. Cross-lane pattern scan (read-only): how do sibling lanes bind counted verdicts to seat output? grep sibling lane tools dirs for analogous counters (e.g. /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/, kumitate-shokunin/tools/) and compare the binding channel (results.json + report first-lines vs other channels). Which pattern is stronger and what should this lane take or avoid? One page of findings with paths.""")

add('ConnSources', 'connector', ['sources', 'contract'], 'SOURCES contract check',
    f"""Item F-11. Check the S252 row against the SOURCES.md contract v1 in /home/vgpnk/Projects/shokunin/CORPUS.md (section 'SOURCES.md — where a shokunin learns'): column count, type/tier vocab, status vocab (`mined`), recheck vocab (date, `NNd`, or symbolic cadence), used-by file existence, no cell containing a literal or escaped `|`. Also check the whole Registry block still has that shape (spot-check 5 other rows: S237, S242-S244, S250). Report violations or PASS with evidence.""")

add('ScoutDeadLinks', 'scout', ['depth', 'evidence'], 'citation resolution',
    f"""Item F-12. Citation-resolution sweep over the round-47 committed surface: for every path cited in SCORECARD.md 'Round 47 — declaration', LOG.md's round-47 entry, and {L}/corpus/lessons/round-47.md, verify `git -C {L} cat-file -e {IMPL}:<path>` or on-disk existence. Also re-check the round-44 strace log citation (`.ufo/waves/round-44/w1/C1ExecLiveRead/commands.txt:26,81` and `w2/SkillReview.md:55` cite `strace-rev-live1.log` — does the .log or only .log.gz resolve?). Report a table of dead/cold citations.""")

add('C1CritGR1', 'critic', ['depth', 'C1', 'GR1'], 'GR1 fresh attack',
    f"""Item C1-R9. Fresh attack on GR1 (independent of the counted seats): read `## GR1` at {IMPL} and attack it against the snapshots ({SRC45}/cmdline.c, vsprintf.c, kstrtox.c; {SRC44}/sysfs.c). The row claims base-0 parsing, one suffix letter, 1024 multipliers, -EINVAL rules and the bare-newline clears-limit claim. Find the weakest clause — e.g. does vsprintf.c really choose octal for `010`, does kstrtox.c prove the case-insensitive suffix, is the write path really the memparse one at sysfs.c:2040? Report per-clause verdicts.""")

add('ScoutSkill', 'scout', ['depth', 'freshness', 'SKILL'], 'SKILL staleness',
    f"""Item F-13. SKILL.md staleness sweep for this round's surfaces: grep {L}/SKILL.md for lines about the census selftest (case counts, TMPDIR, --identity, --selftest usage text) and the scrub grounding rows (round-44/45 status notes, FAILED/pending marks). Which become stale after this round's work? Report path:line and the proposed APPEND-ONLY correction text (never edit old lines — draft only).""")

add('ScoutPrompt', 'scout', ['depth', 'conformance'], 'prompt conformance',
    f"""Item F-14. Prompt-vs-report conformance precheck: read /home/vgpnk/Projects/shokunin/.ufo/prompts/tsukuroi-round-47.md §4 (report contract) and produce the checklist the final report must satisfy (sections in order, counting commands, verdicts, SHONEN line count matching {L}/SHONEN.md boxes, Stale-lane line, assimilation line). Also confirm the prompt's own contract items this lane must satisfy (S252 row, census exit 0 at end, mistake mining, sourced claim). Draft the checklist as markdown the L1 can paste.""")

add('ScribeReport', 'scribe', ['depth', 'report'], 'report skeleton',
    f"""Item F-15. Draft the round-47 report skeleton (the L1 writes /home/vgpnk/Projects/shokunin/.ufo/reports/round-47/tsukuroi.md; you draft text only): read the contract in /home/vgpnk/Projects/shokunin/.ufo/prompts/tsukuroi-round-47.md §4 and §6, and the round-46 report /home/vgpnk/Projects/shokunin/.ufo/reports/round-46/tsukuroi.md for shape. Every required section in order with placeholders for wave results; fill committed receipts (controls, before receipts, freeze/impl hashes, S252 row, sources census counts).""")

add('C1MutReports', 'mutation-tester', ['depth', 'C1', 'binding'], 'seat-report mutants',
    f"""Item C1-M2. Mutation-test the binding channel at the seat-report level: in a scratch clone {CLONE}, fabricate wave w9 reports that (a) put the verdict on the second line with a preamble first; (b) emit `ROW GR1 VERDICT: holds` with a unicode homoglyph space or a trailing space; (c) bind a hash computed over the WRONG row extent (e.g. include the expected next header line, or drop a trailing blank line); (d) carry a `ROW GR2 VERDICT: holds` inside a GR1 report body. Run {C1C} --revision <mutant-rev> --section-hash and the counter itself on each; report which bind, which refuse, and any that binds wrongly. Report a matrix.""")

add('ScribeLOG', 'scribe', ['depth', 'LOG'], 'LOG entry draft',
    f"""Item F-16. Draft (report text only) the round-47 LOG.md entry to be appended at integration: the round header (base {BASE}, impl {IMPL}), the two claims with frozen predicates and their before->after measurements (base receipts in {W}/before/, counter legs), the wave shape line (one v2 wave w1, seat count and role mix from {W}/w1-spec.json), the freshness re-verification line (which predecessor pins were re-run this round), the assimilation line, and the lesson/report pointers. Match the shape of {L}/LOG.md's round-46 entry.""")

spec = {'wave': 'w1', 'reportDir': '.ufo/waves/round-47/w1', 'maxLanes': 256,
        'context': CONTEXT, 'items': items}
names = [i['name'] for i in items]
assert len(names) == len(set(names)), 'duplicate names'
out = f'{W}/w1-spec.json'
with open(out, 'w') as f:
    json.dump(spec, f, indent=2)
c = Counter(i['role'] for i in items)
attack = sum(v for k, v in c.items() if k in ('reviewer', 'critic', 'mutation-tester', 'labrat'))
print(len(items), dict(c), 'attack', attack, round(attack / len(items), 3))
