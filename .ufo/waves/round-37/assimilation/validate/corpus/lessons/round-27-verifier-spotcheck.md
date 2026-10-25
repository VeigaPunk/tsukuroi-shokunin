# Round 27 — verifier spot-check (tsukuroi, non-author)

author: hyaku closure (non-author integrator, @m_opus)

Closure agent HyakuCloseTsukuroi27, a fresh `task` dispatched by the hyaku orchestrator (exposed runtime model `anthropic/claude-opus-5-5`). Three read-only reviewer seats were dispatched with no model parameter: CloseR27C1, CloseR27C2 and CloseR27Gate. No lane tool or gate was executed by this agent or its seats. Installs: none.

Judged revisions: base `3beab8ddcf4ed2ae9fdf12eab6ac7f840c74e333`, head `02996e4c868824a504cd1adb0530e8420fbb997a`. Both trees were exported read-only with `git archive <rev> | tar -x` into `/fast/scratch/hyaku/closure-tsukuroi-r27/{base,head}`. The round ran as two attempts: attempt 1 (L1 TsukuroiR27) pushed `db9eecfa`..`099c7b3f` and died in the omp restart at 17:26Z without a report; attempt 2 (L1 TsukuroiR27a2) inherited those commits, added `2e519d61`..`02996e4c` and filed the report. This check judges the landed whole against the claims as declared before data (`db9eecfa`).

Driver digest (copied from `.ufo/watchdog.log`):

- `2026-10-22T12:51:01-03:00 launch tsukuroi round=27 pgid=3887772 driver=hyaku-inline attempt=1`
- `2026-10-22T14:30:04-03:00 lane-dead-no-report tsukuroi round=27; retry same round (hyaku-inline attempt=1: omp process restart at 17:26Z; no landed report; fresh successor inherits work)`
- `2026-10-22T14:30:06-03:00 launch tsukuroi round=27 pgid=1002786 driver=hyaku-inline attempt=2`
- `2026-10-22T15:04:58-03:00 complete tsukuroi round=27; hyaku-inline attempt=2`

## Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report landed by the lane | `git log --format='%an <%ae> %H %cI' -- .ufo/reports/round-27/tsukuroi.md` (fleet root) | `tsukuroi-shokunin <tsukuroi@shokunin.local> fc94f5651f8c…` at 15:04:34 -0300, after the lane tip `02996e4c` (15:02:56) and before the `complete` line (15:04:58) | pass |
| `SHONEN` heading, one line per box | read report lines 78-83 | four `[~]` lines with pointers | pass |
| Cited commits exist and are ancestors of the branch | `git cat-file -e <h>^{commit}` and `git merge-base --is-ancestor <h> master` for the twelve round commits and `3beab8dd` | all thirteen exist and are ancestors | pass |
| Lane identity on round commits | `git log --format='%h %an %s' 3beab8dd..02996e4c` | twelve commits, all `tsukuroi-shokunin`; no other author in range | pass |
| Pushed, nothing ahead | `scripts/hyaku/jj-lane.sh state <lane>` | `local=remote=02996e4c… ahead=0 behind=0 head=detached tracked=0 untracked=0` | pass |
| Leftovers | `git status --porcelain` | empty | pass |
| Remote ref | `git ls-remote origin refs/heads/master` | `02996e4c868824a504cd1adb0530e8420fbb997a` | pass |
| Prompt carries the template contract | every non-blank, non-placeholder line of `templates/round-prompt.md` searched with `grep -qF` in `.ufo/prompts/tsukuroi-round-27.md` (committed `0ec746b`, one-line change in `e953776` for attempt 2; worktree equals `e953776`) | 105 lines checked, 0 missing; hyaku addendum is §6 at line 141 | pass |
| Append-only record files | `git diff --numstat 3beab8dd 02996e4c` rows with deletions | only `tools/check-self-assessment.py` (45/13) and `tools/check-storage-health.py` (26/2), the routed round-26 defects 2 and 3; `SCORECARD.md`, `LOG.md`, `SHONEN.md` and `corpus/SOURCES.md` delete 0 lines | pass |
| Counter bytes equal the pins; counters before data | `git diff --quiet 75f410c8 02996e4c -- tools/check-kernel-taint.py`; `git diff --quiet dd94cb1f 02996e4c -- tools/check-adjacency-overlap.py`; `merge-base --is-ancestor 75f410c8 b1647ff2`, `dd94cb1f 75784ea4`; `git cat-file -e <pin>:<entry>` | both diffs exit 0; both orderings hold; neither entry exists at its counter pin (exit 128) | pass |
| Measured revision vs tip | `git diff --name-only 0c5e3006 02996e4c` | only `.ufo/waves/round-27/measure/a2-final2/` receipts (16 files, 400 insertions); nothing a counter reads | pass |

Payload deviation (carried from round 26, now located): every seat text carries the host-appended `~/.omp/agent/RULES.md` block after the validated `taskCall` (report routed defect 5; `w2a2/RevDispatchFidelityA2.md`). The L1 passed the validated payload unchanged; the append is host injection, which the lane cannot change, and an L0 question is filed. Classification: a disclosed payload-fidelity conformance defect, status-neutral, no observed effect (all 44 wave-2 reports say `Installs: none`). The same block reached this closure's own seats.

Inherited-attempt state: the only attempt-1 leftover (`.ufo/waves/round-27/w2/swarm-registry.json`, 36 seats, every agent id null) was committed as evidence in `2e519d61`; nothing was reverted. Attempt 1's lost wave 2 left no report and is not counted as evidence.

## Per-claim re-check

Per §Gate standard, both counters are lane-owned gates with registry rows (`SKILL.md:2438`, round-27 registry table), so neither was executed. Each claim was re-measured with my own script `indep.py` (below) over the exported trees, applying the declared row rules at `SCORECARD.md:1000` and `:1002`, and the lane's committed evidence was checked as well.

### C1 — depth: kernel-taint entry, verified rows 0 → 6 of 6

Re-measured. `python3 indep.py base` → `c1_verified_rows 0` (entry and capture absent). `python3 indep.py head` → `c1_verified_rows 6`; per row, valid linked quotes / valid capture pointers: KT1 3/1, KT2 3/2, KT3 3/2, KT4 2/3, KT5 3/1, KT6 1/1. Capture sha256 `88d02d98…7841` equals the declaration. `jq` over the JSON lists ids KT1-KT6 once each; the `.md` table has 6 KT rows; `SKILL.md:2420` holds `## Kernel taint — round 27`.

Committed evidence agrees: `measure/c1-3beab8dd.json` `CANNOT_EVALUATE`, `KT-CAPTURE-MISSING`, `verified_rows` 0; `measure/a2-final2/c1.json` `PASS`, `verified_rows` 6, revision `0c5e3006`; `a2-final2/selftests.txt` shows all five selftests exit 0; `kt-selftest.json` 46 cases, 0 failed. CloseR27C1 independently resolved all 12 quotes and every capture pointer (25 resolutions, 0 failures) and found `git diff --quiet 0c5e3006 02996e4c` over the entry, JSON, capture, sources and tool exits 0, so the tally transfers to the tip.

Truth sample (the count proves links, not truth; the report says so): KT1's decode "12288 is 4096 + 8192: bit 12 (O) and bit 13 (E)" holds against S142 re-fetched live (`include/linux/panic.h` lines 83-84 `TAINT_OOT_MODULE 12`, `TAINT_UNSIGNED_MODULE 13`; sha256 `f9f64576…c6a8` equal to snapshot and anchor) and against S140 lines 97-98 (CloseR27Gate). `cat /proc/sys/kernel/tainted` on the host still prints `12288`. KT3 stays `UNVERIFIED` as recorded. The appended "Wave-2 corrections" and JSON `corrections_r27_a2` carry the narrowed branches; the KT6 verdict split is now `[]` in `a2-final2/q71-verdict-agreement.txt`.

Ruling: **verifies as declared** (6 verified rows, field `verified_rows`). C1 is deeper sourced ground inside the existing driver and firmware Core area, not new ground, as the refined declaration says.

### C2 — adjacency: mori overlap register, anchored rows 0 → 6 of 6

Re-measured. `python3 indep.py base` → `c2_anchored_rows 0`; `head` → `c2_anchored_rows 6`, every row with zero failure reasons. My recount is stricter than the pinned counter on the shapes wave 2 showed it accepts: it refuses a lane side under `.ufo/` or in the register itself, and requires the snapshot bytes to equal `git -C mori-shokunin cat-file -p ef9dbee1:corpus/knowledge/userspace-oom-killers-r26.md` (sha256 `a5368ee7…0b29d`). Rows: OV1 `INBOUND-RESOLVES`/tsukuroi, OV2 `INBOUND-DRIFTED`/mori (lane side `PROVINCE.md`), OV3 `AGREES`/tsukuroi, OV4 `CONFLICTS`/tsukuroi, OV5 `CONFLICTS`/mori, OV6 `LANE-GAP`/mori with a null lane side. OV6's gap is real: `git grep -l -E 'oomd_ooms|oomd_kill' 3beab8dd -- corpus SKILL.md PROVINCE.md` exits 1, and at the head only the register itself matches. CloseR27C2 re-derived the same 6 with its own code and confirmed the OV6 quote sits at line 198, inside the declared `quote_line + 2` window, as disclosed.

Committed evidence agrees: `measure/c2-3beab8dd.json` `register-missing`, 0; `measure/a2-final2/c2.json` `PASS`, `anchored_rows` 6, revision `0c5e3006`; `ov-selftest.json` 17 cases, 0 failed.

Ruling on the weak counter (orchestrator question). The author discloses that the pinned counter scores 6 on 19 of 24 should-fail register mutants (`w2a2/CritC2Tool.md`, `MutC2Counter.md`: extra rows, lane quotes from the register, `.ufo/` or the mori snapshot, six `LANE-GAP` rows, one-character quotes, heading-line anchors, fabricated snapshots without mori). That is real, and by the lane's own QUALITY 72 a count from this counter is a count of anchors, not proof of the claim. It does not fail C2 as declared, for three reasons: (1) the declared after-value is "6 anchored rows, OV1 to OV6, exit 0" in field `anchored_rows`, and the declaration refinement (`SCORECARD.md:1016`) already states what the counter does not check; (2) the 6 reproduce under an independent, stricter recount that refuses the mutant shapes, so the evidence is the re-derivation, not the counter alone; (3) no live row uses a mutant shape (all six name the pinned mori path, lane paths are only `memory-pressure-r25.md` and `PROVINCE.md`, quotes are multi-word, one `LANE-GAP` row whose gap is verified above). Class and owner judgements rest on RevRowOV1 to RevRowOV6 and are not proven by any count; the "pointers replayed" wording is correctly narrowed to OV1 and OV2. **Verifies as declared, as a count of anchors**; the counter's permissiveness is a routed gate defect, status-neutral (§Gate standard, Closure consequence).

### Per-axis verdicts

`git diff 3beab8dd 02996e4c -- SCORECARD.md` only appends (0 deleted lines): the declaration, refinements, a round-27 axes table with unchanged ordinals, the measured outcome and the falsify-wave outcome. No ordinal moved and no capability was entered.

| Axis | Verdict | Evidence |
|---|---|---|
| depth | improved | C1 verified 0 → 6; mechanism, decoding, per-module reading, persistence and operator actions sourced to S140-S145; ordinal stays 8 |
| adjacency | improved | C2 verified 0 → 6 anchored overlap rows against a pinned sibling blob; five outbound items for mori reported, not absorbed; ordinal stays 8 |
| coverage | unchanged | not claimed; README row only, no PROVINCE frontier paragraph |
| operability | unchanged | not claimed; registry-coverage harm at `099c7b3f` (2 missing) repaired to 31 of 31 at `0c5e3006` (`a2-final2/registry.json`) |
| freshness | unchanged | not claimed |
| calibration | unchanged | not claimed; the round-26 axes table's 5 stale counts are restated by the round-27 table |

No owned axis harmed: the one in-round harm found (registry FAIL at `099c7b3f`) is repaired at the measured revision.

Note for the next round: this spot-check adds a file under `corpus/lessons/`, so at the spot-check commit the round-27 axes table's lesson count (30, `SCORECARD.md:1027`) reads one short. That mismatch comes from this commit, not from the lane.

## Discernment spot-check

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` → exit 0, `tsukuroi ok`, 25 `W04` (same count as at round start). SOURCES rows 139 → 145 (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`); `git diff -U0 3beab8dd 02996e4c -- corpus/SOURCES.md | grep -cE '^-[^-]'` → 0.

| Item | Gate decision | Re-opened source (2026-10-22) | Agree / disagree | Reason |
|---|---|---|---|---|
| S142 Linux v7.2 `include/linux/panic.h` (new row) | admit (A, mined) | `curl` raw.githubusercontent URL: HTTP 200, sha256 `f9f64576…c6a8`, equal to the snapshot and the anchor | agree | Gate quotes `#define TAINT_OOT_MODULE 12` and `#define TAINT_UNSIGNED_MODULE 13` (3 words each) are at lines 83 and 84 as recorded; the teaches cell "bit 12 … bit 13" matches |
| S140 Linux v7.2 `tainted-kernels.rst` | admit (A, mined) | live HTTP 200, sha256 `727ddb82…0841`, equal to snapshot and anchor (CloseR27Gate) | agree | quotes at lines 51 (18 words), 171 (10), 12 (14) and 8 (22) are verbatim; lines 97-98 give `O 4096` and `E 8192` |
| S144 Linux v7.2 `kernel/module/signing.c` | admit (A, mined) | live HTTP 200, sha256 `96c80734…6735`, equal to snapshot and anchor (CloseR27Gate) | agree | `reason = "module with unavailable key";` (6 words) verbatim at line 107 |
| dkms 3.4.4 signing docs, Arch `nvidia-open` PKGBUILD | "Not registered" (not opened; seats dead) | capture `.ufo/waves/round-27/capture/capture.txt` lines 60-125 (`pacman -Qo`, `pacman -Q`) | agree with the deferral | KT4's package facts are host captures, not claims about DKMS key handling, so no row needs those sources yet; this is a deferral, not a reject decision |
| reject sample | none exists | `git show 02996e4c:corpus/lessons/round-27.md \| grep -ci reject` → 0 | cannot sample | the Gate records six admits and no reject, so LEARNING's "at least one admit and one reject" cannot be met this round (routed 1) |

The gate agrees with the outside check on all three sampled admits and on the one deferral. No reject was available to sample.

## Trend verdicts

- **expansion: unchanged.** Agree with the author. `driver-firmware-plane.md:101-106` at the base already held both taint journal lines inside the driver and firmware Core area; C1 deepens it. The register is an adjacency record, not new domain ground. Six new tier-A source rows are a new depth of kernel source, not a new kind.
- **quality: improved.** A weaker admitted statement was superseded by a stronger sourced one: `driver-firmware-plane.md` gains an appended round-27 note that the nvidia modules carry a signature (`modinfo -F signer`) and E means "not verified by the kernel", not "unsigned" (`git diff 3beab8dd 02996e4c -- corpus/knowledge/driver-firmware-plane.md`). The `memory-pressure-r25` `--kernel-oom` exception is withdrawn in both the `.md` (line 402) and the JSON (`corrections_r27`, row MP6). The storage JSON carries six correction markers. The items wave 2 found and did not fix (MP4 qualifier in `SKILL.md:2316` and its JSON action, `driver-firmware-plane.md:276` `[unk]`, further storage-JSON statements) are listed as owed debt in the lesson, and in each case the entry of record carries the correct reading, so none is false and unmarked (round-26 precedent); they are routed below.
- **discernment: improved.** The outside check agrees with the gate on three admits. Disagreements from the round-26 outside check became lessons with grounded criteria: R27-COMPANION-UNSWEPT (from spot-check routed defect 1) → QUALITY 67, and wave-2 findings → QUALITY 70, 71 and 72, each naming its lesson id and each with a lesson row (`grep -c <id>` in `corpus/lessons/round-27.md` and `corpus/QUALITY.md` → 1 or more for R27-COMPANION-UNSWEPT, R27-DECLARED-FRONTIER-OVERCLAIM, R27-REGISTRY-ROW-MISSING, R27-OWN-COMPANION-RULE-BROKEN, R27-COUNTER-PERMISSIVE). Limit: no reject was sampled.

SHONEN: all four boxes stay `[~]` (`SHONEN.md` unchanged in range; 0 `[x]`). Box 3 still lacks a whole-SKILL retest, so none is ready for non-author promotion review.

## Routed defects (the lane fixes these next round; all status-neutral)

1. The round-27 Gate records no reject, so the outside check could not sample one. Record each candidate considered and not admitted as an explicit reject (or defer) row with its reason, so every round's Gate offers at least one reject decision.
2. `tools/check-adjacency-overlap.py` accepts 19 of 24 should-fail register shapes (CritC2Tool, MutC2Counter). Before the next adjacency count is offered as evidence, apply QUALITY 72: should-fail selftest cases for extra or non-string ids, lane sides under `.ufo/`, in the register or in the sibling snapshot, a minimum quote length, a quote line on a heading, and `LANE-GAP` with a non-null lane side.
3. `tools/check-kernel-taint.py` accepts a one-word quote and a quote from a source the row does not list (CritC1Tool; MutC1Counter 27 of 30); its docstring R4 still says "appears in" (R27-CHECKER-DOC-LAG). Fix both with should-fail cases at the next change.
4. Owed companion debt named in the lesson: the MP4 qualifier (`OOMRules=`, `systemd-oomd.socket`) in `SKILL.md:2316` and the MP4 JSON action; `driver-firmware-plane.md:276` `[unk]`, which the round-27 capture resolves; the further unmarked statements in `storage-health-r26.json`. Mark each in its companion (QUALITY 67).
5. Mori's round-27 work says the lane's "+200 band scanned first" reading (`oom-event-plane.md:116,349`, `kill-event-deep-r8.md:147,260`) is false. Check it against a source and correct or rebut it.
6. `tools/check-self-assessment.py`: hyphenated measured-outcome headings match nothing, the docstring states the pre-QUALITY-65 rule, and three selftest cases named by MutSelfAssessQ65 are missing.
7. QUALITY 69 cites "(C2, round 27)" instead of its lesson id R27-SIBLING-POINTER-DRIFT; name the lesson id so the criterion-to-lesson link is greppable both ways.
8. Cross-lane, for mori (reported by this lane, not absorbed): the five items in the report's "Cross-lane items for mori" line (mori `PROVINCE.md:66` and `SKILL.md:345` pointers, OV4 qualifiers, S133 "only" wording, r12 `--kernel-oom` text). Operator, not lane: the host-appended RULES.md block (L0 question open) and the dead wave-1 scribe/executor route.

## Reproducible re-check script (run over `git archive` exports; no lane tool executed)

`indep.py <tree>` prints `c1_verified_rows` and `c2_anchored_rows` with per-row detail. C1 applies `SCORECARD.md:1000`: ids KT1-KT6 once each; non-empty statement and action; a verdict from the four words; every cited source a `mined` row opened 2026-10-22 whose `used-by` names the entry, with one tier-A source; one quote of at most 25 words that is a normalised substring of a `sources/<S###>.*` snapshot whose sha256 is in the anchor and equals that source's Gate located-quote cell after one outer pair of quotes or backticks is removed; one capture pointer to a unique non-header line holding a token of 3 or more characters (capture sha256 asserted); the id in a table row of `## Kernel taint — round 27`. C2 applies `SCORECARD.md:1002` (sibling `mori` at `ef9dbee1`, snapshot sha256 equal to `sibling_blob_sha256` and to the mori blob, nearest heading, quote within `quote_line`..`quote_line + 2`, lane quote found in the lane file or null only for `LANE-GAP`, vocabularies, non-empty action, id in the PROVINCE section) and additionally refuses lane sides under `.ufo/` or in the register itself.

```python
import glob, hashlib, json, os, re, subprocess, sys
root = sys.argv[1]; P = lambda *a: os.path.join(root, *a)
norm = lambda s: " ".join(s.split())
sha = lambda f: hashlib.sha256(open(f, "rb").read()).hexdigest()
out = {}
entry = P("corpus/knowledge/kernel-taint-r27.json"); cap = P(".ufo/waves/round-27/capture/capture.txt")
if not (os.path.exists(entry) and os.path.exists(cap)):
    out["c1_verified_rows"] = 0
else:
    assert sha(cap) == "88d02d98cbb5fd4633ff83cacb2256ac57af1d740c7c57b6ac7a98fceb067841"
    caplines = open(cap, encoding="utf-8", errors="replace").read().split("\n")
    rows = json.load(open(entry))["rows"]; ids = [r["id"] for r in rows]
    src = {}
    for line in open(P("corpus/SOURCES.md"), encoding="utf-8"):
        if re.match(r"^\|\s*S\d{3,}\s*\|", line):
            c = [x.strip() for x in line.rstrip("\n").split("|")]
            if len(c) == 13: src[c[1]] = dict(tier=c[4], anchor=c[6], status=c[8], opened=c[9], used=c[11])
    gate = open(P("corpus/lessons/round-27.md"), encoding="utf-8").read().split("\n## Gate", 1)[1].split("\n## ", 1)[0]
    gq = {}
    for line in gate.split("\n"):
        c = [x.strip() for x in line.split("|")]
        if len(c) >= 7 and re.match(r"^S\d{3,}$", c[1]):
            q = c[4]
            if len(q) >= 2 and q[0] == q[-1] and q[0] in "`\"": q = q[1:-1]
            gq.setdefault(c[1], []).append(norm(q))
    sec = open(P("SKILL.md"), encoding="utf-8").read().split("\n## Kernel taint — round 27", 1)[1].split("\n## ", 1)[0]
    skill_ids = {l.split("|")[1].strip() for l in sec.split("\n") if l.startswith("|")}
    per = {}
    for r in rows:
        good = ids.count(r["id"]) == 1 and str(r.get("statement", "")).strip() and str(r.get("action", "")).strip() \
            and r.get("verdict") in ("HEALTHY", "DEGRADED", "BLOCKED", "UNVERIFIED") and r["id"] in skill_ids
        good = good and all(s in src and src[s]["status"] == "mined" and src[s]["opened"] == "2026-10-22"
                            and "corpus/knowledge/kernel-taint-r27.md" in src[s]["used"] for s in r["sources"])
        good = good and any(src[s]["tier"] == "A" for s in r["sources"])
        nq = sum(1 for q in r["quotes"] if len(norm(q["text"]).split()) <= 25 and any(
            sha(f) in src.get(q["source"], {}).get("anchor", "")
            and norm(q["text"]) in norm(open(f, "rb").read().decode("utf-8", "replace"))
            and norm(q["text"]) in gq.get(q["source"], [])
            for f in glob.glob(P(".ufo/waves/round-27/sources", q["source"] + ".*"))))
        nc = sum(1 for c in r["capture_pointers"] if len(c["token"]) >= 3 and 1 <= c["line"] <= len(caplines)
                 and not caplines[c["line"] - 1].startswith(("### ", "$ ", "[exit "))
                 and c["token"] in caplines[c["line"] - 1] and caplines.count(caplines[c["line"] - 1]) == 1)
        per[r["id"]] = dict(base=bool(good), quotes=nq, caps=nc)
    ok = sum(1 for v in per.values() if v["base"] and v["quotes"] and v["caps"])
    out["c1_verified_rows"] = ok if sorted(ids) == [f"KT{i}" for i in range(1, 7)] else 0
    out["c1_rows"] = per
reg = P("corpus/knowledge/adjacency-mori-oom-r27.json")
if not os.path.exists(reg):
    out["c2_anchored_rows"] = 0
else:
    rows = json.load(open(reg))["rows"]; ids = [r["id"] for r in rows]
    prov = open(P("PROVINCE.md"), encoding="utf-8").read().split("\n## Adjacent — mori userspace OOM killers (round 27)", 1)[1].split("\n## ", 1)[0]
    prov_ids = {l.split("|")[1].strip() for l in prov.split("\n") if l.startswith("|")}
    per = {}
    for r in rows:
        snap = P(r["snapshot"]); why = []
        if ids.count(r["id"]) != 1: why.append("dup")
        if r.get("sibling") != "mori" or r.get("sibling_commit") != "ef9dbee136d6ed2ef98687f5cb0c0a16506a5155": why.append("sib")
        if not os.path.exists(snap) or sha(snap) != r["sibling_blob_sha256"] or r["snapshot"] != ".ufo/waves/round-27/siblings/mori/" + r["sibling_path"]: why.append("snap")
        else:
            L = open(snap, encoding="utf-8").read().split("\n"); ql = r["quote_line"]
            heads = [i for i in range(ql) if L[i].startswith("#")]
            if not heads or L[heads[-1]] != r["heading"]: why.append("heading")
            if len(norm(r["quote"]).split()) > 25 or norm(r["quote"]) not in norm("\n".join(L[ql - 1:ql + 2])): why.append("squote")
            mori = subprocess.run(["git", "-C", "/home/vgpnk/Projects/shokunin/mori-shokunin", "cat-file", "-p", r["sibling_commit"] + ":" + r["sibling_path"]], capture_output=True).stdout
            if hashlib.sha256(mori).hexdigest() != sha(snap): why.append("mori-blob")
        lp = r.get("lane_path")
        if lp is None:
            if r["class"] != "LANE-GAP": why.append("null-lane")
        else:
            if lp.startswith(".ufo/") or lp == "corpus/knowledge/adjacency-mori-oom-r27.md": why.append("self-sourced-lane")
            if not os.path.exists(P(lp)) or len(norm(r["lane_quote"]).split()) > 25 or norm(r["lane_quote"]) not in norm(open(P(lp), encoding="utf-8").read()): why.append("lquote")
        if r["class"] not in ("INBOUND-RESOLVES", "INBOUND-DRIFTED", "AGREES", "CONFLICTS", "LANE-GAP"): why.append("class")
        if r["owner"] not in ("mori", "tsukuroi", "contested"): why.append("owner")
        if not str(r.get("action", "")).strip(): why.append("action")
        if r["id"] not in prov_ids: why.append("province")
        per[r["id"]] = dict(ok=not why, why=why, cls=r["class"], owner=r["owner"], lane=lp)
    out["c2_anchored_rows"] = sum(v["ok"] for v in per.values()) if sorted(ids) == [f"OV{i}" for i in range(1, 7)] else 0
    out["c2_rows"] = per
print(json.dumps(out, indent=1))
```
