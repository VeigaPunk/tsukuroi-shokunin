#!/usr/bin/env python3
"""Generate the tsukuroi round-36 wave-2 spec (32 falsify seats). Filled at dispatch time
with the freeze and change commit hashes; attack items are seeded from wave-1 findings."""
import json, os, sys

GODSPEED = open(os.path.expanduser('~/.agents/skills/godspeed/directive.md')).read()
LANE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
FREEZE = sys.argv[1]
CHANGE = sys.argv[2]

TIMEBOX = ("\n\nTime-box: return within 15 minutes with your best findings+evidence; "
           "partial results are acceptable.\n"
           "You are an independent leaf: never block on or wait for another seat; "
           "if a needed artifact is absent, record the dependency as a finding and return.")

context = f"""/skill:godspeed
# Godspeed directive (verbatim bytes of ~/.agents/skills/godspeed/directive.md)
{GODSPEED}
# Goal
Tsukuroi round 36, attempt 1, wave w2 (FALSIFY wave, 32 seats): attack what wave 1 and the L1 integration produced. Freeze commit (counter bytes): {FREEZE}. Change commit (C1 five tools + C2 note + registry/rows): {CHANGE}. Declaration + pre-freeze corrections: SCORECARD.md at 6d76fb20f6ecbc940e5c8fff36c74060c885e161 and its correction block. Claims: C1 (operability) five live tools build child envs from fixed dicts, counted by tools/probe-child-env-allowlist-r36.py VERSION 7 --set livefive (measure: last JSON line leaking == 0, leaking_pairs [], harness_errors [], exit 0, predicate_label leaking; sensitivity conjuncts: MutAttrgetterCopy/MutPathCopy mutants each read > 0, claim/r33claim/regression sets read 0 at the base; named limit: livefive parity diffs recorded-not-evidence; untraced zero-records uninformative). C2 (depth, exploratory) corpus/knowledge/journalctl-v262-field-filter-r36.md on S198/S199 opened wave 1.

# Seat bounds (every seat)
- Your tools start at the fleet root /home/vgpnk/Projects/shokunin. Every path you read or write MUST be absolute. Lane write scope: ONLY {LANE}, and within it only your own seat directory .ufo/waves/round-36/w2/<YourSeatName>/ (plus mktemp scratch). NEVER write the fleet root, sibling lane repos, .ufo/state/, .ufo/watchdog.log, MANIFEST.json, templates/ or fleet scripts/. Do NOT edit production files — the L1 lands every production change from seat outputs.
- NEVER run git add/commit/push, jj, or any mutating VCS command anywhere; the L1 is the only committer. Read-only git is fine. Never touch the lane Git index. Sandbox clones for mutants go in mktemp (git clone --no-local file:// is fine there).
- You are a leaf: no delegation, no own swarm.
- Report trailer: `Report: .ufo/waves/round-36/w2/<SeatName>` is relative to {LANE} — write your report at {LANE}/.ufo/waves/round-36/w2/<SeatName>/ (a .md file named <SeatName>.md). Machine output as separate files in the same directory.
- Tooling authorization (operator, 2026-10-19): you may install or upgrade tools via official channels only (uv tool install / official binary into ~/.local/bin / cargo / npm -g); record tool/version/channel/reason. PACMAN GUARD: ALL pacman transactions are PAUSED host-wide — never run pacman in any form.
- Routing: the seat role decides the model route through the operator's global OMP table (~/.omp/agent/config.yml task.agentModelOverrides). Never pass or request a model parameter.
- Never message agent://all; message only your own wave peers by exact id if truly needed.
- Heading-time discipline: every timestamp is pasted from `date -u +%H:%M:%SZ` at write time, or omitted.
- Honesty: an unrun check has not passed; mark inference [inf], unknown [unk]."""

items = []
def seat(name, role, prompt, axes, milestone=None):
    it = {"name": name, "role": role, "prompt": prompt + TIMEBOX, "axes": axes}
    if milestone: it["milestone"] = milestone
    items.append(it)

seat("W2ReBefore","executor",
 f"Independently re-issue the C1 BEFORE evidence at the declaration base 6d76fb20f6ecbc940e5c8fff36c74060c885e161: run tools/probe-child-env-allowlist-r36.py --revision 6d76fb20f6ecbc940e5c8fff36c74060c885e161 --set livefive (expect leaking > 0 on all five targets) and confirm the committed before receipt under .ufo/waves/round-36/l1/ matches your run's last line (leaking count per target). Report per-target counts + any divergence.",
 ["operability","C1","receipts"])

seat("W2ReAfter","executor",
 f"C1 AFTER battery at {CHANGE}: python3 tools/probe-child-env-allowlist-r36.py --revision {CHANGE} --set livefive --scratch /tmp/w2-after; confirm last line leaking == 0, leaking_pairs [], harness_errors [], exit 0, predicate_label leaking, probe_sha256 equal to the freeze bytes a2a5acacaf5660754b39238a74d503c22c2241498012f6ee24c6aa27b4af443a. Paste the summary + per-target leaking counts. ALSO: run the r33claim and claim sets at {CHANGE} (expect 0 each) and the regression set (expect 0). Report any divergence.",
 ["operability","C1","receipts"])

seat("W2MutAttrgetter","mutation-tester",
 f"Kill-check after-mutant m-attrgetter: the patches apply at the round-34 change commit df66150 (r34 C1), NOT at 3457f287. Build a sandbox clone at df66150, apply .ufo/waves/round-34/w2/MutAttrgetterCopy/variant.patch (ambient copy via split-string operator.attrgetter with a reapplied fixed PATH) to tools/check-section-citations.py. KNOWN INVOCATION-COVERAGE GAP (L1, freeze LOG): the probe's --set claim runs --selftest, which spawns children through the tool's separate already-fixed sandbox_git and never exercises the mutated git() — at that invocation the frozen probe reads 0. Your job: (1) reproduce that 0 reading and confirm the gap; (2) exercise the ACTUAL unsafe builder: the tool's live mode (read its argparse: --revision/--lane) through the frozen probe is not directly expressible, so run the tool's live mode in a sandbox with a canary ambient name and the r34 git-alias detector (-c alias.x=!/usr/bin/env x) to show the ambient name reaches a git child spawned by git(); (3) report whether ANY frozen-probe invocation reaches git() (try --set claim with other argv? the probe's target argv is fixed, so document the gap precisely). Verdict: is the sensitivity conjunct satisfiable as declared, or must it be re-stated (live-mode detector)? Report KILLED/SURVIVED/GAP with evidence.",
 ["operability","C1","mutation-test"])

seat("W2MutPathCopy","mutation-tester",
 f"Kill-check after-mutant m-pathcopy: sandbox clone at df66150 (the patches apply at the r34 change commit, not 3457f287), apply .ufo/waves/round-34/w2/MutPathCopy/mutant.patch (ambient PATH via os.pathsep.join(os.get_exec_path())) to tools/measure-update-recheck.py, score once with the frozen probe (--set claim --only tools/measure-update-recheck.py). NOTE the same invocation-coverage risk as m-attrgetter: check whether measure-update-recheck --selftest exercises the mutated git(); if not, exercise the live mode with the git-alias detector and report both readings. Expect KILLED on the exercised builder; the untraced channel must read > 0 for the wrapper-reachable PATH preservation (that is the sensitivity conjunct). Report KILLED/SURVIVED/GAP with per-channel clauses.",
 ["operability","C1","mutation-test"])

for i in range(1,7):
    seat(f"W2MutTool{i}","mutation-tester",
     f"Kill-check after-mutant m{i}: sandbox clone at {CHANGE}; apply .ufo/waves/round-36/w1/MutToolMutants/mutant-{i}.diff (if absent, reconstruct the declared mutant: re-introduce the ambient copy into the i-th of the five tools per its mutants.md), score once with the frozen probe --set livefive --only <the mutated tool>; expect KILLED (leaking > 0). Report KILLED/SURVIVED + which channels fired + the ordinary-run check (the ambient marker reaches a child).",
     ["operability","C1","mutation-test"])

seat("W2RevCounter","reviewer",
 f"Adversarial review of the frozen counter tools/probe-child-env-allowlist-r36.py at {FREEZE}: read every clause added since r34 (VERSION 7 paragraph, livefive set + named limit, untraced channel, normalisation rules) and hunt for: a skip-work variant the livefive battery would read 0 (e.g. an env builder keyed on the probe's wrapper presence, a builder that copies ambient minus an expanded prefix list, an execveat path, a target engineered into harness_error); a normalisation that hides a real leak (over-broad HEX/path rules masking genuinely different argv); the M5 class (measure under-counts channels). For each: build the variant in a sandbox and score it, or reason precisely why the frozen clauses catch it. Output: variants table with receipts; ALSO fold the simplifier duty: list any dead weight in the +300-line probe delta with keep/drop recommendation.",
 ["operability","C1","attack:counter"])

seat("W2CritKill","critic",
 f"Attack the frozen kill rule: try to construct ANY variant of the five tools that skips part of the fixed-dict work and reads leaking 0 on --set livefive at a sandbox clone of {CHANGE} (this is the declared kill condition). Try at least: prefix-list expansion (ambient minus GIT_* and TSUKUROI_* and LC_*); inheriting spawn for ONE of the tool's children; a builder that special-cases the probe's scratch root; a source-channel evasion via importlib. If any succeeds, C1 is not verified — report with the receipt. If all fail, report each attempt's reading.",
 ["operability","C1","attack:kill-rule"])

seat("W2QuoteNews","reviewer",
 f"Re-open the pinned source bytes for S199: fetch https://raw.githubusercontent.com/systemd/systemd/v262/NEWS, verify sha256 equals a494f0389edd09702a90d1540c7e21c0af5a4d29a4d020855ca3062d885a7657, verify the quote 'journalctl now rejects -F/--field together with filters such as unit, boot, time, cursor or grep filters.' is at lines 129-133. Check the note corpus/knowledge/journalctl-v262-field-filter-r36.md cites it accurately. Report agree/disagree per item.",
 ["depth","sources","S199"])


seat("W2RevC2","reviewer",
 f"Review corpus/knowledge/journalctl-v262-field-filter-r36.md at {CHANGE}: every mechanism claim must cite a receipt (command+exit+stderr) in .ufo/waves/round-36/w1/ExecC2Live/ or ScribeC2Draft/matrix-mini.json; the decision table must cover the ReviewC2Draft blocking findings (-n allowed-silent third state; scope selectors -D/--file/--root/--system/--user allowed); the consumer section must be preventive (no lane tool uses -F/-N); honesty marks present; header trio consistent with S198/S199. Output review.md with blocking/minor findings.",
 ["depth","C2","review"])

seat("W2CritC2Depth","critic",
 f"Rule on C2's depth-vs-expansion question with evidence: read the note + S024/S198/S199 rows + the round-1 lesson's pinned quote (corpus/lessons/round-1.md:111 carries S024's pinned NEWS quote). Is the note genuinely new mechanism ground (exact line, exit code, the 16-term predicate, -n third state, scope-allowed list) that no prior entry held? Does it duplicate S024's teaching? State what the closure reviewer should rule and why. Output c2-depth-ruling.md.",
 ["depth","C2","attack:shape"])

seat("W2SentinelDiff","sentinel",
 f"Scope/diff hygiene at {CHANGE}: git diff --stat 6d76fb20f6ecbc940e5c8fff36c74060c885e161 {CHANGE} must touch ONLY: the five tools, tools/probe-child-env-allowlist-r36.py (new), corpus/knowledge/journalctl-v262-field-filter-r36.md (new), corpus/SOURCES.md (S198/S199 rows), SKILL.md (round36 registry table + NoUpgrade append), SCORECARD.md, LOG.md, corpus/lessons/round-36.md (new), corpus/README.md (row), .ufo/waves/round-36/ evidence. Append-only sweep on SCORECARD/LOG/corpus/QUALITY.md/SOURCES/SHONEN: no removed lines. Flag every out-of-scope or removed-line finding.",
 ["scope","sentinel"])


seat("W2ConnAfter","connector",
 f"Sibling-overlap re-scan at {CHANGE}: re-run the ConnSiblings checks (sibling lanes' last rounds for child-env/probe/journalctl collisions; mori's journalctl(1) S014/S160 neighborhood). Confirm no new collision from the landed rows; report the mori-neighborhood note (C2's rows must not be misread as fleet-novel against mori's S014). Output conn-after.md.",
 ["adjacency","connector"])

seat("W2ScribeMistakes","scribe",
 f"Sweep ALL wave-1 and wave-2 seat reports (.ufo/waves/round-36/w1/*/ + w2/*/ + wave-root *.md) for mistakes worth mining (defect classes: wrong revision cited, unrun check claimed, timestamp estimated, dependency not recorded, scope breach, receipt missing). Produce candidate rows (class, evidence pointer, captured-by, fix-able-to-fail) for corpus/lessons/round-36.md ## Mistakes. Do not invent; quote each report.",
 ["lesson","mistakes"])

seat("W2RevToolA","reviewer",
 f"Per-tool behaviour-change review of the five diffs at {CHANGE} vs 6d76fb20f6ecbc940e5c8fff36c74060c885e161 (tools/check-revision-binding.py + check-report-receipts.py): argv identical, fixed values identical (plus LC_ALL addition disclosed), control flow identical, no dropped protection, no remaining ambient read on any spawn path (AST check). Output review.md per tool.",
 ["operability","C1","review"])

seat("W2RevToolB","reviewer",
 f"Per-tool behaviour-change review of the other three diffs at {CHANGE} (score-census-handoff-r32.py, mutants-btrfs-space-r30.py incl. the import-re rewrite, run-receipt.py incl. the new GIT_CEILING_DIRECTORIES): same checks as W2RevToolA. Output review.md per tool.",
 ["operability","C1","review"])


seat("W2ExecGates","executor",
 f"Run all seven lane gates at {CHANGE} via run-receipt.py (QUALITY 77 receipts under your seat dir): check-self-assessment, check-registry-coverage, check-knowledge-header, check-recheck-commands, check-adjacency-anchors, report-red-causes, check-pause-gate --revision {CHANGE}. Expected: six exit 0, check-pause-gate 1 (inherited P3), check-self-assessment 0 (the SCORECARD axes row must state 48 lesson files). Report every exit + first failing check.",
 ["operability","gates"])

seat("W2ExecCensusSelftest","executor",
 f"No-harm at {CHANGE}: bash tools/tsukuroi-census.sh --selftest (expect PASS 105/105 rc=0), bash tools/tsukuroi-census.sh (live rc=1), python3 tools/mutants-btrfs-space-r30.py (battery rc 0), python3 tools/check-report-receipts.py --report ... --lane {LANE} --revision {CHANGE} (the livefive mode), python3 tools/run-receipt.py --help. Compare vs the wave-1 baseline .ufo/waves/round-36/w1/ExecSelftestNoHarm/. Report any regression.",
 ["operability","no-harm"])

seat("W2RevReceipts","reviewer",
 f"Receipt conformance sweep: every gate/measurement receipt committed under .ufo/waves/round-36/ must have a JSONL header naming its revision (6d76fb20/ freeze / {CHANGE}) and the tool sha256, and a footer exit_code (QUALITY 77). List every receipt violating the shape; check no receipt cites a revision absent from the lane. Output receipts-review.md.",
 ["calibration","receipts"])

seat("W2CritSeparability","critic",
 f"Verify causal separability of C1 and C2 at {CHANGE}: C1's battery must not read the C2 note (grep the probe for corpus/knowledge reads — expect none); C2's evidence must not depend on the five tools' change (the matrix ran at base); reverting C2's files must not change the C1 after receipt (reason or sandbox-test). Output separability.md.",
 ["calibration","claims"])

seat("W2ScribeLesson","scribe",
 f"Finalize corpus/lessons/round-36.md from the skeleton (.ufo/waves/round-36/w1/ScribeLessonDraft/round-36-lesson-skeleton.md) + W2ScribeMistakes candidates + the wave Gate table (S024/S198/S199 rows with quotes from SrcSystemdNews/SrcJournalctlMan/ScribeSourcesRows): fill ## Gate (one row per source object: S198 opened+mined, S199 opened+mined supersedes S024, S024 unchanged), ## Mistakes (all vetted rows), registry changes old->new, holds/cancellations/dead seats (from the L1's wave log). Do not invent quotes; copy them from the seat artifacts.",
 ["lesson"])

seat("W2RevSources","reviewer",
 f"SOURCES.md conformance at {CHANGE}: S198/S199 rows well-formed (11 cells, quotes <=25 words, no double quotes), S024 untouched, census validate exit 0 (run /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi), rows 197 -> 199, no duplicate ids. Output sources-review.md.",
 ["sources","registry"])

seat("W2ExecCensusEnd","executor",
 f"Registry + census close-out at {CHANGE}: run the sources census (exit 0 required, paste output), grep the SKILL.md round36 registry table exists with kinds in gate/probe/library (check-registry-coverage reads it — confirm its verdict), confirm the probe row names the freeze sha256. Output census-end.txt + report.",
 ["sources","registry","gates"])

seat("W2RevNoUpgrade","reviewer",
 f"Verify the NoUpgrade supersession sweep landed: the four append blocks (.ufo/waves/round-36/w1/ScribeNoUpgrade/*.append.md) are present at {CHANGE} in SKILL.md (EOF), corpus/knowledge/update-safety-note.md, corpus/knowledge/update-safety-v2.md (two sites), each quoting the original verbatim and naming pacman-backup-files-r35.md; originals not rewritten (append-only sweep clean); residual loci (update-safety-note.md:346, degraded-triage-r4.md:392) recorded as not-in-routed-scope. Output noupg-review.md.",
 ["freshness","repair"])



seat("W2ScribeRegistry","scribe",
 f"Check the SKILL.md round36 registry table at {CHANGE}: one row per new/changed tool (the probe: kind probe, entry command, verdict map, selftest note, pinned values = freeze sha256, write scope, owner), the census row unchanged, every row's kind accepted by check-registry-coverage (gate/probe/library). Draft the fix if anything is missing (do not edit SKILL.md yourself). Output registry-review.md.",
 ["operability","registry"])

seat("W2LiveOracle","executor",
 f"QUALITY-82 live-view rerun at {CHANGE}: run .ufo/waves/round-36/w1/ExecLiveViewDesign/run-live-view.sh against the real lane checkout at {CHANGE} (read-only modes only; if the harness needs a specific invocation read view-spec.md) with ten fresh canary names; expect 0 canaries reach any child for all five tools. Paste the per-tool summary. If the script cannot run at the change commit, run the underlying per-tool commands per view-spec.md and disclose. This is the production-like view named in the corrections.",
 ["operability","C1","quality-82","live-view"])

seat("W2CritFreeze","critic",
 f"Freeze-rule conformance: verify the freeze discipline — the probe bytes at {FREEZE} equal the bytes every control/before receipt names (sha256 in receipts), no counter/predicate/label/set/after-value change between {FREEZE} and {CHANGE} (git diff {FREEZE} {CHANGE} -- tools/probe-child-env-allowlist-r36.py must be empty), the kill rule and named limit text unchanged after any seat scored. Output freeze-conformance.md with verdicts.",
 ["operability","C1","freeze"])

seat("W2RevReport","reviewer",
 f"No-overclaim sweep of the L1's integration claims (read the SCORECARD correction block + LOG entries at {CHANGE}): every stated measurement must have a committed receipt (check the named paths exist); every verdict must match its receipt's exit/last line; the C1 verdict text must state the sensitivity conjuncts' outcomes explicitly. Output overclaim.md with per-claim verdicts.",
 ["calibration","claims"])


spec = {"wave": "tsukuroi-r36-w2", "reportDir": ".ufo/waves/round-36/w2",
        "maxLanes": 32, "context": context, "items": items}
out = f"{LANE}/.ufo/waves/round-36/w2-spec.json"
json.dump(spec, open(out, "w"), indent=1)
from collections import Counter
print("spec written:", out, "items:", len(items))
print(Counter(i["role"] for i in items))
