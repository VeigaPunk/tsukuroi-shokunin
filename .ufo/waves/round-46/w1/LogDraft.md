VERDICT: draft

# F-14 — round-46 LOG.md entry draft

Register: the round-45 entry (`LOG.md:1626-1654`) — heading, "Motivating evidence:", claims with base/freeze/measured
revisions, waves, "Measured at", integrated findings, routed-defect disposition, "**Freshness (D10).**", adjacency,
considerthese, assimilation, and a "Landed:" commit list closing with the lesson and report paths.

Provenance rule: a value enters the entry only when read from a file in this worktree at the revision named; that
file's commit status is recorded in §3. Values no receipt supplies are `<UPPER_SNAKE>` placeholders listed in §2.

## 1. Draft entry (exact Markdown, ready to paste at the end of `LOG.md`)

```markdown
## Round 46 — 2026-10-27 (hyaku run 9; L1 TsukuroiR46)

Motivating evidence: the round-45 closure (`corpus/lessons/round-45-verifier-spotcheck.md` §2, §5) — round 45 closed
`rejected-honest-stop` with C2 depth FAIL (`verdicts_ok` 0: no counted verdict bound), and it routed
D1 R45C-D3-R44-MARK-SWEEP, D2 R45C-D7-CITATION, D3 R45C-ASMGATE-RECEIPT, D4 R45C-START-CENSUS and D5
R45C-POSTFREEZE-NAME, plus the carried items (re-bind GR1-GR3 under a channel the seat writes itself, QUALITY 93; the
C1 review gaps; the C2MutBinding survivors). Base `2042117c` = the lane tip at round start (`jj-lane.sh state`:
`local=2042117c…`, it carries that spot-check); freeze `72cc2609` (declaration, frozen counters, pre-data controls,
round-start receipts, S250/S251 snapshots); implementation `a4477049` (C1 and its entry). Claims: C1 operability —
`tools/tsukuroi-census.sh` gains `--identity` (routed debt D12, open since round 10), one stdout line
`TSUKUROI_CENSUS_IDENTITY: version=… sha256=… md5=… bytes=… lines=… planes=… exit_map=… verified=yes|no` naming the
bytes the running bash executes, read through the descriptor bash holds re-opened as `/proc/$$/fd/<n>` (S250 bash 5.3
`shell.c` `5f3d539f…`, `general.c` `669ef408…`, `general.h` `bf9251e3…`; S251 proc_pid_fd(5) `3a50ddef…`) and only
when it resolves to the invoked file, `unverifiable`/`verified=no` for stdin, pipe and replaced-after-open, `--identity`
taking no other argument, `(R46-C1)` selftest cases, entry `corpus/knowledge/census-identity-r46.md`; frozen counter
`tools/score-census-identity-r46.py` sha256 `7c406eb5…`. C2 depth (sourced S246-S249) — the round-45 pending rows
GR1-GR3 of `corpus/knowledge/btrfs-scrub-grounding-r45.md` are admitted only if counted seats bind verdicts; frozen
counter `tools/check-scrub-admission-r46.py` sha256 `28c409be…`. Pre-data controls, scored with the frozen counters
before any seat: C1 9/9 as expected (`controls/battery-summary-c1.jsonl`), C2 22/22 (`battery-summary-c2.jsonl`); the
first C1 counter draft let K2 (a path hasher) PASS (`battery-summary-c1-draft1.jsonl`), and the frozen counter adds a
decoy-rename case that separates the path from the descriptor, with the matching selftest case in the candidate. At
base both counters read FAIL: C1 `identity_ok 0 … selftest_r46 0` (`before/c1-before-base.jsonl`), C2 `marks_ok 0`,
`verdicts_ok 0`, every row unbound (`before/c2-before-base.jsonl`). Waves: `w1`, the round's one v2 wave, 66 seats
(`w1-dispatch.json` `counts.spawn` 66); at draft time (HEAD `61e06740`, wave still running) 54 reports, 10 of the 12 counted seats reported
(`V46RevGR3b` missing), every report uncommitted. Measured at `<MEASURED_REV>`: C1 `<MEASURED_C1>`; C2
`<MEASURED_C2>`. At `a4477049` the C1 counter read `identity_ok 1`, `tracks_ok 1`, `symlink_ok 1`, `unverifiable_ok 1`,
`cli_ok 1`, `nowrite_ok 1`, selftest `PASS (160 cases, 160 passed, 0 failed)` with 6 `(R46-C1)` cases, and the identity
line `sha256=d925839c… md5=db08a606… bytes=209208 lines=3598` over the six planes
(`.ufo/waves/round-46/l1/c1-impl-a4477049.jsonl`, uncommitted). Counted verdicts as read: GR1 four `holds`, no `fails`;
GR2 one `holds` and two `partly`; GR3 one `holds` and one `partly`. Wave findings raised. `w1/C1CritRace.md` holds
that `verified=yes` is a best-effort identity of the open descriptor, not execution attestation (bash reads
incrementally; two agreeing hashes do not detect a concurrent or ABA in-place write) and proposes replacing
`corpus/knowledge/census-identity-r46.md:69-72`; `w1/C2CritQuorum.md` shows the frozen predicate admits on any two
same-role `holds` with no reviewer/critic diversity (`check-scrub-admission-r46.py:238-243`) and proposes a section hash
frozen before dispatch plus cross-role quorum; `w1/C2CritLimits.md` drafts the append-only round-46 gate status for the
r45 entry, `SKILL.md` and `corpus/README.md`; `w1/C1ExecPlaneDiff` ran the census three times at each of base and
implementation: all six runs rc=2, 13 lines, value-masked shapes identical, differences confined to volatile PLANE
fields (planes unchanged); the remaining `defect-found` reports (`C1CritClaim`, `C1CritControls`, `C2ExecGateR43`) are
`<INTEGRATION_FINDINGS>`. Integration then narrowed GR2 and GR3 on the counted `partly` reads (`b57740c2`), which moved
their section hashes (`a963df81…` → `4bf28bcf…`, `8fa62676…` → `43430a14…`; GR1 unchanged at `fe77ac76…`) and left the
counted GR2/GR3 verdicts bound to bytes no longer current; the frozen counter reads `bound_on_current 0` for all three
rows at `b57740c2`, also because no wave dispatch or results file is committed there (`waves_seen` empty; the counter
loads `-dispatch.json`/`-results.json` from the revision, `check-scrub-admission-r46.py:130-163`). The C2 kill rule for
this round reads "a GR row changed without every bound verdict on its current bytes re-read", so the narrowing is
recorded here as the round's own kill condition unless every bound seat re-reads the narrowed bytes:
`<ADMISSION_STATE>`. C1 was hardened after the first measurement (`61e06740`: `O_CLOEXEC`, the unique-descriptor rule,
`--identity --help` refused, two further `(R46-C1)` cases), so the measured C1 number is `<MEASURED_C1>` and not the
`a4477049` reading quoted above. Routed defects: D1 `<D1_STATUS>`; D2 closed in
`b57740c2` (corrections appended to `.ufo/waves/round-44/w1/C1ExecLiveRead/commands.txt` and `w2/SkillReview.md`,
citing `strace-rev-live1.log.gz`, blob `ec1848d6…`); D3 closed in `b57740c2` (`a2w1/AsmGate.md` correction, recount
249/147/50 at `44560592`); D4 closed — the sources census ran at this attempt's own start
(`before/sources-census-start.txt`, `2026-10-27T04:49:57Z`, `validate` exit 0, `rows=249`, 40 W04, lane tip
`2042117c`); D5 `<D5_STATUS>`. **Freshness.** Re-verification of predecessor pins, 2026-10-27: S246-S248
(`lib/cmdline.c` `1af5ad98…`, `lib/vsprintf.c` `cabb648a…`, `lib/kstrtox.c` `0c52ae02…`, `fs/btrfs/dev-replace.c`
`f07ef0a0…`, `man/systemd.kill.xml` `44832283…`), S237 (btrfs-progs v7.1 `cmds/scrub.c` `48df2e2f…`) and S242-S244
(`fs/btrfs/scrub.c` `f347931b…`, `fs/btrfs/sysfs.c` `ce146120…`, `btrfs-scrub@.service` `eaa7af92…`) re-fetched with
digests identical to their frozen `SHA256SUMS` rows, 9/9; byte-for-byte `cmp` was **not** established (that seat's
batch stopped before the compares finished), so identity rests on SHA-256; the tags re-peel to `a2de78ee…` (v7.2.11),
`8cc40e0c…` (v262) and `4ab0e80b…` (v7.1), while the Arch packaging pin `0c0a4d77…` (btrfs-progs 7.1-1, S244's tag) was
not re-resolved this round; the S249 host capture re-ran identical but for its timestamp (`2026-10-27T02:09:52Z` →
`05:21:49Z`, normalized diff empty) and the live sysfs still reads `exclusive_operation` 444 `none` and
`devinfo/1/replace_target` 0 (`w1/C2ExecLiveSources.md`, `w1/C2ExecHostRecheck.md`). Adjacency: `<ADJ_GATE>`; the
predecessor counters of the kill-rule list: `<PRIOR_COUNTERS>`. considerthese: `<CONSIDERTHESE>`. Assimilation: none —
the staged merge's continuous S-space collides with the lane registry (52 colliding ids at `a4477049`: 251 lane ids
against 147 staged S200-S346; 50 at `44560592` before S250/S251), and no staged row grounds this round's surfaces
(`w1/AsmGate.md`). Landed: `72cc2609` freeze; `a4477049` C1, entry and S250/S251; `<W1_DISPATCH_SHA>` w1 spec and
dispatch; `b57740c2` GR2/GR3 narrowing and the D2/D3 correction notes; `61e06740` C1 identity hardening from the wave; `<W1_INTEGRATION_SHA>` w1 integration;
`<W1_EVIDENCE_SHA>` w1 evidence; `<OUTCOME_SHA>` the outcome (C1/C2 measured, axes and capabilities tables,
`SCORECARD.md` "Round 46 — measured outcome"); this entry with the outcome, corrections, lesson and QUALITY. Lesson
`corpus/lessons/round-46.md`; report `.ufo/reports/round-46/tsukuroi.md` (fleet repo).
```

## 2. Placeholder ledger

| Placeholder | Must be supplied by | Notes |
|---|---|---|
| `<MEASURED_REV>` | a revision that carries the wave records, the gate marks and the report files | C2 is measured there, not at `a4477049`: `marks_ok` is 0 at base and at `b57740c2` |
| `<MEASURED_C1>` | `after/` C1 receipt at `<MEASURED_REV>` | the `a4477049` values are quoted separately |
| `<MEASURED_C2>` | `after/` C2 receipt (`r45_legs_ok`, `verdicts_ok`, `marks_ok`, `rows_ok`) | at draft `verdicts_ok` 0 at every revision tried |
| `<ADMISSION_STATE>` | the L1's decision after fresh counted reads on the narrowed bytes | GR1 binds `fe77ac76…` with four `holds`; GR2/GR3 have none on their current hashes |
| `<INTEGRATION_FINDINGS>` | `w1/C1CritClaim.md`, `w1/C1CritControls.md`, `w1/C2ExecGateR43.md` corrections as integrated | all three reports are `defect-found`; their proposed text is not in this draft |
| `<D1_STATUS>` | `w1/ScribeReadme.md` (seat: "README index and D1 marks") | at draft `corpus/README.md:434` still shows the r44 SR7-SR9 row with no pending mark; `marks_ok` still reads `readme: false` |
| `<D5_STATUS>` | the whole-round diff over `tools/score-*` (`72cc2609..HEAD`) | the freeze carries both counters and `git log` shows no counter commit after it; the final sentence needs that diff |
| `<ADJ_GATE>` | `after/` `check-adjacency-anchors` receipt at `<MEASURED_REV>` | not run in this wave at draft time; no `after/` directory exists |
| `<PRIOR_COUNTERS>` | the ten other kill-rule counters (readers-r45, scrub-arm-r44, bootinputs-r43, size-invariance-r42, selftest-mounts-r41, selftest-literals-r40, storage-hidden-r39, storage-arm-r38-q82, pacnew-arm-r35b, census-handoff-r32) at `<MEASURED_REV>` | none run at draft time; the entry MAY NOT claim PASS→PASS without them |
| `<CONSIDERTHESE>` | `w1/ConsiderMine.md`; `considerthese/2026-10-27.md` if written | `ls considerthese/` ends at `2026-10-26.md`, which round 45 already mined |
| `<W1_DISPATCH_SHA>`, `<W1_INTEGRATION_SHA>`, `<W1_EVIDENCE_SHA>`, `<OUTCOME_SHA>` | the L1's commits | not landed at draft time |
| wave death count | `w1.ready`/registry once the wave closes | 66 seats spawned, 54 reports at the last check (HEAD `61e06740`), 10/12 counted; a seat with no report is not yet a dead seat |

## 3. What the draft's numbers rest on (commit status at draft time, HEAD `61e06740`)

Committed in the freeze, the implementation or the integration commit — `git cat-file -e <REV>:<path>` → 0:
`.ufo/waves/round-46/controls/battery-summary-c1.jsonl`, `battery-summary-c1-draft1.jsonl`,
`battery-summary-c2.jsonl`, all 30 `C1-K*`/`C2-K*` receipts, `SCORECARD.md` (declaration), both counters,
`corpus/SOURCES.md` S250/S251, `corpus/knowledge/census-identity-r46.md`,
`.ufo/waves/round-46/frozen/src/{SHA256SUMS,FETCH.txt,shell.c,general.c,general.h,proc_pid_fd.5.html}`, and (from
`b57740c2`) `.ufo/waves/round-44/w1/C1ExecLiveRead/commands.txt`, `.ufo/waves/round-44/w2/SkillReview.md`,
`.ufo/waves/round-45/a2w1/AsmGate.md`, `corpus/knowledge/btrfs-scrub-grounding-r45.md`.

Read but **uncommitted** (every quoted value must be re-read from the commit that lands it):
`.ufo/waves/round-46/l1/c1-impl-a4477049.jsonl`, `before/{c1-before-base,c2-before-base}.jsonl`,
`before/sources-census-start.txt`, `before/c2r45-legs-base.json`, every `w1/*.md` report,
`w1/C2ExecLiveSources/{sha256-live.txt,tags.txt}`, `w1/C2ExecHostRecheck/{capture-now.txt,diff.txt}`,
`w1/C1ExecPlaneDiff/*`, `w1-dispatch.json`.

Not used: `w1.ready.partial` (dispatch-time snapshot) and `w1/swarm-registry.json` (roster, not a result).

Counts re-taken at draft time: `ls -1 .ufo/waves/round-46/w1/*.md | wc -l` → 50, then 54 minutes later; `V46*.md` → 10 of the 12 declared
counted names (`V46RevGR3b` absent); `w1-dispatch.json` `counts` `{"spawn": 66, "resume": 0, "total": 66}`,
`len(registry.members)` 66.

## 4. Findings that bear on this draft (verbatim conflicts for the canonical judge)

1. **The measured C2 is blocked twice over, and the entry must say so rather than carry a PASS.** At `b57740c2`
   I ran `python3 tools/check-scrub-admission-r46.py --revision b57740c2…` (read-only; 1 run, ~3 s): output
   `marks_ok 0`, `verdicts_ok 0`, `waves_seen []`, every row `bound_on_current 0`, `r45_legs_ok 1`, exit FAIL.
   (a) No `w1-dispatch.json` or `w1-results.json` is committed at either revision I checked — `git ls-tree b57740c2
   .ufo/waves/round-46/` lists only `before`, `controls`, `frozen` — and the counter loads both from the revision
   (`tools/check-scrub-admission-r46.py:130-163`), so no seat can bind until they land; there is no
   `.ufo/waves/round-46/w1/w1-results.json` in the worktree either.
   (b) `--section-hash` shows GR2 `a963df81…` → `4bf28bcf…` and GR3 `8fa62676…` → `43430a14…` between `a4477049` and
   `b57740c2`, while every GR2/GR3 counted report cites the earlier hash; GR1 is unchanged (`fe77ac76…`). The
   narrowing therefore converted the round's counted `partly` reads into history, exactly the hazard
   `w1/C2CritQuorum.md` names (`check-scrub-admission-r46.py:238-243` admits on any two same-role current-hash
   `holds`). The LOG entry should record the new hashes and that fresh counted reads are required, not imply the
   old ones still bind.
2. **The C1 kill rule's last clause ("a census line at or before `:3383` moves") is satisfied under one reading only.**
   `git diff 2042117c..61e06740 -- tools/tsukuroi-census.sh` has four hunks: `@@ -452,7 +452,7 @@` (`SELF=${BASH_SOURCE[0]}`
   → `SELF=${BASH_SOURCE[0]:-}  # round 46 (C1): …`), `@@ -591,7 +591,7 @@` (usage line gains `--identity`),
   `@@ -602,7 +602,7 @@` (the exit-map doc line gains the `--identity` sentence) and `@@ -3381,16 +3381,148 @@` (the identity
   block and its cases). The three pre-`:3383` lines change **content** and keep their line numbers; the insertion starts
   at 3381, so lines from 3381 down shift. Read as "moves" = "changes position", the claim survives; read as "changes",
   it is killed. I did not decide it; the judge holds the rule, and `w1/C1ExecAdjacency.md`/`w1/C1ExecRevLookup.md` are
   the seats that can measure the shift directly.
3. **`w1/C1CritRace.md` narrows the C1 wording in the declaration.** `verified=yes` establishes descriptor identity
   and equal endpoint hashes, not that the hashed bytes are the bytes bash executed; a replacement for
   `corpus/knowledge/census-identity-r46.md:69-72` is proposed. If it is integrated, the entry's phrase "naming the
   bytes the running bash executes" must be softened in the same round. I did not resolve it; the draft keeps the
   declaration's wording and flags it here.
4. **Collision counts that differ are revision differences, not a conflict:** `w1/AsmGate.md` reports 251 lane ids and
   52 collisions at `a4477049`; the D3 correction reports 249/50 at `44560592`. The delta is S250/S251. The round-45
   receipt's original "183 registry ids, 30 intersections" reproduces under neither revision.
5. **Host-guard deviations observed (not mine):** `w1/C2ExecHostRecheck.md` ends "Scratch cleanup was not performed in
   this seat", against the seat rule; `w1/C2ExecLiveSources.md` reports its `cmp` batch ran before its downloads
   finished and was not retried, so "byte-identical" there is digest-only.
6. **`C2ExecLiveSources/tags.txt` covers three tags only** (v7.2.11, v262, v7.1); the Arch packaging tag `7.1-1`
   (`0c0a4d77…`) behind S244's files was not re-resolved. The entry states this instead of claiming 4/4.

## 5. Work performed here

- Read: `LOG.md:1580-1654` (register), `SCORECARD.md:2964-3007` (declaration), the closure routing
  (`corpus/lessons/round-45-verifier-spotcheck.md:180-215`), the round-45 disposition table
  (`corpus/lessons/round-45.md:92-101`), all 45 wave-1 reports present, the control batteries (C1 9 + draft 1, C2 22),
  the base C1/C2 receipts, the L1 C1 receipt at `a4477049`, the live-source and host-recheck receipts, the plane-diff
  receipts, `considerthese/`, `w1-dispatch.json`, `w1-spec.json`.
- Ran read-only: `git cat-file -e`/`ls-tree`/`log`/`diff`, `check-scrub-admission-r46.py --revision b57740c2` (once)
  and `--section-hash` at `a4477049` and `b57740c2`. No C1 counter, no census, no selftest, no source re-fetch, no
  gate. I did not verify any of the wave reports' own claims; I read their first lines and quoted bodies.
- Did not modify lane content. Wrote only this report and `LogDraft/receipt-summary.txt`. Scratch
  `/fast/scratch/hyaku/tsukuroi-r46/LogDraft` was created and removed; no tool installed; no host mutation.
