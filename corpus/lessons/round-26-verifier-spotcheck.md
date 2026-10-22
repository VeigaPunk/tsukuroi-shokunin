# Round 26 — verifier spot-check (tsukuroi, non-author)

author: hyaku closure (non-author integrator, @m_opus)

Closure agent HyakuCloseTsukuroi26, a fresh `task` dispatched by the hyaku orchestrator; exposed runtime model `anthropic/claude-opus-5-5`. No reviewer seats were dispatched: every check below was run by this agent. No lane tool or gate was executed. Installs: none.

Judged revisions: base `e9f5356cd68c9281d07a22e54d1bfd72b12306ac`, head `420a1ae106fc28524b9e7a7aa98080dea976ac15`. Both trees were exported read-only with `git archive <rev> | tar -x` into `/fast/scratch/hyaku/closure-tsukuroi-r26/{base,head}`. Commit `4677350a5249a56da693005a78f636d815bbc372` (operator, "considerthese: 2026-10-22 daily reflection") sits in the range and is not judged. No round-26 commit touches `considerthese/` (`git log e9f5356c..420a1ae1 -- considerthese` lists only `4677350`).

Driver digest (copied from `.ufo/watchdog.log`, lines 702 and 715 when read):

- `2026-10-22T10:33:25-03:00 launch tsukuroi round=26 pgid=2784134 driver=hyaku-inline attempt=1`
- `2026-10-22T12:39:34-03:00 complete tsukuroi round=26; hyaku-inline attempt=1`

## Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report landed by the lane | `git log --format='%an <%ae> %H' -- .ufo/reports/round-26/tsukuroi.md` (fleet root) | `tsukuroi-shokunin <tsukuroi@shokunin.local> e0dda73dd1ba…` at 12:38:57 -0300, after the lane tip `420a1ae1` (12:37:49) | pass |
| `SHONEN` heading, one line per box | read report lines 69-74 | four `[~]` lines with pointers | pass |
| Cited commits exist and are ancestors of the branch | `git cat-file -t <h>` and `git merge-base --is-ancestor <h> refs/heads/master` for the nine round commits, `4677350a` and `e9f5356c` | all eleven are commits and ancestors | pass |
| Lane identity on round commits | `git log --format='%h %an <%ae> \| %cn' e9f5356c..420a1ae1` | nine round commits by `tsukuroi-shokunin`; `4677350` by the operator | pass |
| Pushed, nothing ahead | `scripts/hyaku/jj-lane.sh state <lane>` | `local=remote=420a1ae1… ahead=0 behind=0 untracked=2` | pass |
| Leftovers | `git status --porcelain --untracked-files=all` | `?? .ufo/waves/round-26/w1-dispatch.err`, `?? .ufo/waves/round-26/w2-dispatch.err`, both 0 bytes | defect (routed 4), not round work |
| Prompt carries the template contract | every non-placeholder line of `templates/round-prompt.md` searched with `grep -qF` in `.ufo/prompts/tsukuroi-round-26.md` (committed `d5a4f2f`) | 105 lines, 0 missing; hyaku addendum is §6 at line 141 | pass |
| Append-only record files | `git diff --numstat e9f5356c 420a1ae1` rows with deletions | only `SHONEN.md` (3/3) and three `tools/*.py`; the three SHONEN evidence lines are disclosed with their old text in `corpus/lessons/round-26.md` "Record of in-place edits this round" | pass |
| Tool bytes equal the pins | `sha256sum tools/check-storage-health.py tools/check-self-assessment.py` at head | `6aadca51…f367`, `77c946a9…c26d`, equal to the declaration pins | pass |

Payload deviation (classified): in both waves each seat's task text carried the operator tooling-directive block after the validator's text, so the dispatched text differs from the validated `taskCall` (`w1-dispatch.json` and `w2-dispatch.json` hold no "Tooling directive" string). The block is the operator's always-on directive, already in force for every agent, so it adds no authority. The 67 committed seat reports all say `Installs: none`. Classification: a disclosed payload-fidelity conformance defect, status-neutral, with no observed effect and no harm (routed 5).

Dead seats: wave-2 MutC1Run, MutC2Run, MutC1GateParse and MutC2Ordinal died at start with "No model selected" (4 of 35, 11 percent, under the 20 percent sentinel). The route is operator-owned and no seat was replaced. The L1 ran the mutation runs itself (`.ufo/waves/round-26/l1-mutation/README.md`: C1 20 of 20 rule mutants killed, C2 8 of 8). That is author-run evidence, not an outside attack. Live attack seats were still 39 of 64.

## Per-claim re-check

Per §Gate standard, `check-storage-health` and `self-assessment` are registered gates (`SKILL.md`, round-26 registry rows), so I did not execute them. Each claim was re-measured with my own commands over the exported trees, and the lane's committed evidence was checked as well.

### C1 — depth: storage-integrity entry, verified rows 0 → 6 of 6

Re-measured. My own recount (`c1_indep.py`, below) applies the declared row rule at `SCORECARD.md:897`: ids SH1 to SH6 once each; non-empty statement and action; a verdict from the four-word vocabulary; every cited source a `mined` row opened 2026-10-22 whose `used-by` names the entry, with at least one tier-A source; at least one quote of 25 words or fewer that is a whitespace-normalised substring of a `sources/<S###>.*` snapshot whose sha256 is in that row's anchor and also appears in that source's Gate row; at least one capture pointer to a unique, non-header line holding the token, with capture sha256 `002bef16…71dd`; and a SKILL table row inside `## Storage integrity — round 26`.

- base `e9f5356c`: entry and capture absent → 0, exit 2.
- head `420a1ae1`: `verified_rows` 6. Linked quotes per row: SH1 5, SH2 4, SH3 6, SH4 5, SH5 3, SH6 4. Valid capture pointers: 4, 2, 1, 2, 3, 3.
- Committed evidence agrees: `measure/c1-e9f5356c.exit` exit 2; `c1-7dfea924`, `c1-dd923c03` and `c1-03b9990e` exit 0 with `verified_rows` 6. Selftest receipt `.ufo/waves/round-26/w2/RerunC1/selftest.out` shows `{"cases": 41, "failed": 0}`. Between `03b9990e` and the head only receipts, one wave-2 report and one lesson line change (`git diff --stat 03b9990e 420a1ae1`).

Ruling. The declared after-value (6 verified rows, field `verified_rows`) equals what the counter counts, and it re-derives. The word "verified" claims more than the counter proves: the rule checks evidence links and a non-empty statement, not whether the statement is true. The report says this itself. As the non-author I checked whether the corrected rows are true against their committed sources:

- SH6 (correction line 125): S135 excerpt lines 238-258 give the "if, and only if" trigger with branches a) controller not ready to be powered off and b) shutdown in progress or complete while an out-of-band Ignore Shutdown admin command kept the media up. The correction matches; withdrawing "not a count of host-visible crashes" is right, because a hard power-off falls under a). The SKILL.md wave-2 note marks the count `UNVERIFIED`.
- SH4 (correction line 131): S139 (re-opened, below) has repair-on-read at lines 17-18 inside the replicated-profile paragraph, and "damage is detected by checksum validation" at lines 28-29. The withdrawal of "ordinary reads do verify checksums" as a general statement and its new grounding match.
- SH2 (correction line 132): S132 `btrfs_remove_dev_stat_item` begins at line 2294, is called from `btrfs_rm_device` (line 2405, function from 2326), and the only-writable-device guard is at lines 2372-2374. The kernel reset branch is at lines 8477-8486. The withdrawal of "only on an explicit reset" matches.
- SH5: S134 lines 448-451 (`!w ? "PASSED" : "FAILED!"`), lines 785-788 (`FAILID` return) and lines 833-842 (`FAILSMART` before `print_critical_warning`) support the corrected statement.
- SH1: S133 lines 2074-2100, re-opened, print `write_errs`, `read_errs`, `flush_errs`, `corruption_errs` and `generation_errs`. The correction that only three names are shorter in sysfs matches.

With the appended corrections, the sampled rows are true against their sources, so C1 is a learning claim on ground the lane did not cover before: a sweep of `corpus/knowledge`, `SKILL.md`, `corpus/README.md` and `PROVINCE.md` for `error_stats|device stats|btrfs scrub|scrub status|smartctl|smart-log|Unsafe Shutdowns|corruption_errs` matches 0 files at base and 5 at head. Defect: the corrections did not reach the JSON companion `corpus/knowledge/storage-health-r26.json`, last changed in `ef72f10`. It still says "clears them only on an explicit reset" (SH2) and "Ordinary reads do verify checksums" (SH4), keeps the withdrawn SH6 trigger with verdict `HEALTHY`, and gives the S129 location as line 190 (the snapshot has the quote at line 192). The JSON carries no marker, while `SKILL.md` names the `.md` "and `.json`" as normative (routed 1). The `.md` entry and `SKILL.md` do carry the corrections, so the entry is marked, not left false. **Verifies.**

### C2 — calibration: self-assessment mismatches 5 → 0 of 27

Re-measured with plain commands for the 21 observed-state checks; evidence-verified for K13 (census selftest; `tools/tsukuroi-census.sh` is unchanged in range).

| Check | base `e9f5356c` stated / observed | head `420a1ae1` stated / observed | Command |
|---|---|---|---|
| K07 notes | 47 / 47 | 48 / 48 | `ls corpus/knowledge/*.md \| wc -l` |
| K08 SKILL lines | 2355 / 2355 | 2418 / 2418 | `wc -l < SKILL.md` |
| K09 table lines | 297 / 297 | 336 / 336 | `grep -c '^[|]' SKILL.md` |
| K10 lesson files | 26 / 27 **mismatch** | 28 / 28 | `find corpus/lessons -type f \| wc -l` |
| K11 README lines | 231 / 231 | 248 / 248 | `wc -l < corpus/README.md` |
| K24 box 1 | cites `root-dac-decision-r12.md`, "Superseded" at its line 7 **mismatch** | four plane notes, 0 markers in first 20 lines | `shonen_check.sh` (below) |
| K26 box 3 | cites `root-dac-decision-r12.md` **mismatch** | two notes, 0 markers | same |
| K20-K23, K25, K27 | all cited paths exist | all cited paths exist, 0 markers | same |

Observed-state checks: 3 → 0, matching the report. The committed receipts agree: `measure/c2-e9f5356c.json` 5 (K02, K06, K10, K24, K26), `c2-7dfea924`, `c2-dd923c03` and `c2-03b9990e` 0, `c2-75449b13` 2 (K08, K11 before the re-stated table). Nothing that C2 reads changes between `03b9990e` and the head.

Ruling. The declared after-value (0 of 27, field `mismatches`) is met and re-derives. The "5 → 0" headline overstates the gain by 2: K02 and K06 were mismatches only under the v2 rule this round wrote, and they were cleared by this round's own ordinal-record line in the same table section. K01 to K06 therefore show the round agreeing with itself, not calibration. The part this round earned is 3 → 0 on K07 to K27: a stale lesson count, and two SHONEN boxes citing a superseded note. Those are self-assessment-versus-repository mismatches, so on that part C2 is a valid calibration claim under Claim sizing. The report already discloses the split, and QUALITY 65 records the fix the lane owes (routed 2). **Verifies on its earned part.**

Note for the next round: this spot-check adds a 29th file under `corpus/lessons/`, so at the spot-check commit K10 reads 28 stated against 29. That mismatch comes from this commit, not from the lane, as in round 25.

### Per-axis verdicts

`git diff e9f5356c 420a1ae1 -- SCORECARD.md` only appends (0 deleted lines). It adds the declaration, refinements, a correction to the round-25 record, two current tables with the same ordinals, the measured outcome and the falsify-wave outcome. No ordinal moved and no capability was entered.

| Axis | Verdict | Evidence |
|---|---|---|
| depth | improved | C1 verified; six sourced SKILL rows SH1-SH6 and error patterns SE1-SE4 on new ground; ordinal stays 8 |
| calibration | improved | C2 earned part 3 → 0 on observed state; K01-K06 self-agreement not credited |
| coverage | unchanged | not claimed; new frontier paragraph in PROVINCE and a README row, ordinal 9 |
| operability | unchanged | not claimed; memory-pressure checker hardened (replay `w1/ExecMemCheckerHarden/result-w2.json`: 16 killed, 1 survived); its claim still holds (`measure/memory-pressure-dd923c03.json` 6, PASS); census tool unchanged |
| freshness | unchanged | not claimed |
| adjacency | unchanged | the PROVINCE correction splits free space by question with mori, and the `/tmp` xfs observation is reported to mori, not absorbed |

No owned axis harmed.

## Discernment spot-check

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` → exit 0, `tsukuroi ok`, 25 `W04`. Manual census, base → head: rows 127 → 139, malformed 0, duplicate ids 0, tiers A 117 → 129 (B 3, C 7), mined 113 → 125 (queued 5, rejected 9). `git diff -U0 e9f5356c 420a1ae1 -- corpus/SOURCES.md | grep -E '^-[^-]'` prints 0 lines.

| Item | Gate decision | Re-opened source (2026-10-22) | Agree / disagree | Reason |
|---|---|---|---|---|
| S139 btrfs-progs v7.1 `ch-scrub-intro.rst` | admit (A, mined) | `curl` of the raw.githubusercontent URL: HTTP 200, sha256 `c3b9d344…3485`, equal to the snapshot and the anchor | agree | the Gate quote "The scrubbing status is recorded in :file:`/var/lib/btrfs/` in textual files named" (13 words) is at line 71 as recorded; lines 13-31 support SH3 and SH4 as corrected |
| S131 Arch btrfs-progs 7.1-1 `btrfs-scrub@.timer` | admit (A, mined) | gitlab.archlinux.org raw URL: HTTP 200, sha256 `9a0b6cc2…f8ad`, equal to the snapshot, the anchor and the installed `/usr/lib/systemd/system/btrfs-scrub@.timer` | agree | "OnCalendar=monthly" is at line 5 |
| upstream `kdave/btrfs-progs` v7.1 `units/btrfs-scrub@.timer` | reject (404; S131 registered instead) | raw URL: HTTP 404; GitHub tree API for tag v7.1 (`truncated: false`) lists no `.timer` or `.service` path | agree | upstream ships no unit, so the packaging copy is the right primary source |
| S133 Linux v7.2 `fs/btrfs/sysfs.c` (new row) | admit (A, mined) | raw URL: HTTP 200, sha256 `ce146120…1c43`, equal to the snapshot and the anchor | agree | the Gate quote "static ssize_t btrfs_devinfo_error_stats_show(struct kobject *kobj," (5 words) is at line 2074; lines 2074-2100 support the teaches cell |
| S129 "Uncorrectable" Gate location | admit (A, mined) | committed snapshot `S129.rst` (digest in anchor) | disagree on location only | the quote is at line 192, not 190; the lane already records this in the entry's wave-2 corrections (line 134), so the disagreement is learned |

The gate agrees with the outside check on the sampled admits and the reject. The one location disagreement was already found and recorded by the lane.

## Trend verdicts

- **expansion: improved.** One new admitted entry on ground the coverage map did not hold: the sweep above finds 0 files at base and 5 at head. Its `source:` line cites S128-S135 and S139, all `mined` and tier A. The README carries a coverage row and PROVINCE a frontier paragraph.
- **quality: unchanged.** No earlier admitted entry was superseded by a stronger one or re-verified. Statement errors in the new entry are marked by appended corrections in the `.md` entry and `SKILL.md`, which I confirmed against sources for SH1, SH2, SH4, SH5 and SH6. The unswept JSON companion is a defect, not an unmarked false entry, because the entry of record carries the corrections. S136-S138 supersede source rows, not knowledge.
- **discernment: improved.** This outside spot-check agrees with the gate on 3 admits, 1 reject and 1 new row. Wave-2 disagreements became Mistakes rows, and QUALITY 60-66 each cite a round-26 lesson id (`grep` finds each of the eight ids both as a lesson row and in `corpus/QUALITY.md`).

SHONEN: all four boxes stay `[~]`. Box 3 depends on a whole-SKILL retest that was not run, and the lane's late notes say box 4's evidence line overstates. None is ready for non-author promotion review yet.

## Routed defects (the lane fixes these next round; all status-neutral)

1. `corpus/knowledge/storage-health-r26.json` still carries the withdrawn SH2 ("clears them only on an explicit reset"), SH4 ("Ordinary reads do verify checksums") and SH6 trigger text, the SH6 verdict `HEALTHY` and the S129 location 190, with no in-file marker. Give the JSON an appended correction marker or pointer for each, so "Corrections sweep every mention" holds for the companion `SKILL.md` calls normative.
2. C2 K01-K06 compare the round against its own record. Implement QUALITY 65 (an ordinal check reads only an earlier round's measured outcome) before calibration credit is claimed from those checks.
3. `tools/check-storage-health.py` reads a Gate row from the wrong column, so a plain unquoted quote is not found (R26-GATE-COLUMN-OFFSET). Fix it with the QUALITY 64 selftest cell shapes, disclose the change and re-measure.
4. Two 0-byte untracked files, `.ufo/waves/round-26/w1-dispatch.err` and `w2-dispatch.err`, remain in the lane tree. Write validator stderr outside the lane repo, or remove the files.
5. The dispatched seat text differed from the validated `taskCall` (the appended tooling-directive block). Put any appended text into the spec before validation, so dispatched text and validated text are equal.
6. Operator, not lane: four wave-2 mutation-tester seats died with "No model selected" (operator-owned route). Recorded only, no lane action.

## Reproducible re-check scripts (run over `git archive` exports; no lane tool executed)

`c1_indep.py <tree>`:

```python
import glob, hashlib, json, os, re, sys
root = sys.argv[1]; P = lambda *a: os.path.join(root, *a)
entry = P("corpus/knowledge/storage-health-r26.json"); cap = P(".ufo/waves/round-26/capture/capture.txt")
if not os.path.exists(entry) or not os.path.exists(cap): print('{"verified_rows": 0}'); sys.exit(2)
assert hashlib.sha256(open(cap, "rb").read()).hexdigest() == "002bef16de9bfbffff7905904a1e7f44dae486ca2e60f38090ac2a87132a71dd"
caplines = open(cap, encoding="utf-8", errors="replace").read().split("\n")
rows = json.load(open(entry))["rows"]; ids = [r["id"] for r in rows]; norm = lambda s: " ".join(s.split())
src = {}
for line in open(P("corpus/SOURCES.md"), encoding="utf-8"):
    if re.match(r"^\|\s*S\d{3,}\s*\|", line):
        c = [x.strip() for x in line.rstrip("\n").split("|")]
        if len(c) == 13: src[c[1]] = dict(tier=c[4], anchor=c[6], status=c[8], opened=c[9], used=c[11])
gate = open(P("corpus/lessons/round-26.md"), encoding="utf-8").read().split("\n## Gate", 1)[1].split("\n## ", 1)[0]
gate_rows = {}
for line in gate.split("\n"):
    m = re.match(r"^\|\s*(S\d{3,})\s*\|", line)
    if m: gate_rows.setdefault(m.group(1), []).append(norm(line))
sec = open(P("SKILL.md"), encoding="utf-8").read().split("\n## Storage integrity — round 26", 1)[1].split("\n## ", 1)[0]
skill_ids = {l.split("|")[1].strip() for l in sec.split("\n") if l.startswith("|")}
ok = 0
for r in rows:
    good = ids.count(r["id"]) == 1 and str(r.get("statement", "")).strip() and str(r.get("action", "")).strip() \
        and r.get("verdict") in ("HEALTHY", "DEGRADED", "BLOCKED", "UNVERIFIED") and r["id"] in skill_ids
    good = good and all(s in src and src[s]["status"] == "mined" and src[s]["opened"] == "2026-10-22"
                        and "corpus/knowledge/storage-health-r26.md" in src[s]["used"] for s in r["sources"])
    good = good and any(src[s]["tier"] == "A" for s in r["sources"])
    q_ok = any(len(norm(q["text"]).split()) <= 25 and any(
        hashlib.sha256(open(f, "rb").read()).hexdigest() in src.get(q["source"], {}).get("anchor", "")
        and norm(q["text"]) in norm(open(f, "rb").read().decode("utf-8", "replace"))
        and any(norm(q["text"]) in g for g in gate_rows.get(q["source"], []))
        for f in glob.glob(P(".ufo/waves/round-26/sources", q["source"] + ".*"))) for q in r["quotes"])
    c_ok = any(len(c["token"]) >= 3 and 1 <= c["line"] <= len(caplines)
               and not caplines[c["line"] - 1].startswith(("### ", "$ ", "[exit "))
               and c["token"] in caplines[c["line"] - 1] and caplines.count(caplines[c["line"] - 1]) == 1
               for c in r["capture_pointers"])
    ok += bool(good and q_ok and c_ok)
print(json.dumps({"verified_rows": ok if sorted(ids) == [f"SH{i}" for i in range(1, 7)] else 0}))
```

`shonen_check.sh <tree>`: for each `Author-side evidence` line of `SHONEN.md`, extract `[A-Za-z0-9_./-]+\.(md|json|sh|py)` paths, test that each exists, and for `corpus/knowledge/*.md` count `head -20 <path> | grep -ciw superseded`.
