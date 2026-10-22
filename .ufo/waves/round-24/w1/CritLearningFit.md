# CritLearningFit — round 24, wave 1 (attempt 2)

Verdict: C2 is a Core quality-trend claim (superseding weaker entries on ground that is already covered), not expansion or frontier work, and it does not yet qualify because its checker accepts self-citation, stale sources and evidence from other captures, and its supersession list names text that round 17 had already superseded. C1 is a narrow but real repair of spot-check line 52 and only a partial repair of line 64: the "named cause" it reports is the checker's existing finding id, so the per-cause split that line 64 asks for is still hidden inside SCOPE-PATH-DENIED.

Axes named for this review: fitness to the declared claim kind (learning on Core, repair of routed defects), counting-instrument soundness, provenance of the before-values, identity of the evidence base, and privacy.

## C1 — repair of spot-check lines 52 and 64

1. [obs] The declared before-value is not produced by the declared counting command. Running the counting command at the claim base returns 268, not 0. Command: `python3 tools/report-red-causes.py --revision f169b3ba9a59abaf3e324c1b591e1e07a4d6003a` exited 0 and printed `"attributed_findings": 268` with `"preserved": true`. The tool runs from the working tree, and its four inputs (checker, bindings, events, falsify-limit) are byte-identical at f169b3ba and 10b45f05 (same sha256 values in the `inputs` field at both revisions). The declaration at /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SCORECARD.md:748 says "0 of 268 ... (no such report exists)". [inf] The 0 → 268 delta therefore measures that the instrument exists, not a change in lane bytes. Corpus criterion 49 at /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/QUALITY.md:97 says instrument existence alone is not an improvement.
   Impacted axes: calibration (the claim axis), provenance of the before-value.
   Smallest safe correction: restate the before-value as "counting command absent at f169b3ba (file not in tree), so no attribution was recorded", and either commit the report output as an artifact at the after-revision or make the counting command count a committed report, so that the before and after differ in committed bytes.

2. [obs] The "named cause" is the checker's finding id, copied unchanged. In /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/report-red-causes.py:96 the row key is `(fid, operation)`, where `fid` is the checker's own id. The only new dimension is `operation`, joined from `events.json` (lines 79-81). The checker output already gives id and site for all 268 findings (`python3 tools/check-seat-bindings.py --revision f169b3ba --manifest .ufo/waves/round-23/falsify/bindings.json --events .ufo/waves/round-23/falsify/events.json`, exit 2, CANNOT_EVALUATE, 266/1/1). [inf] The join with the operation is new information that the checker output does not contain. Calling the id a "cause" is a relabel.

3. [obs] Strongest counterexample to "per-cause observability" (spot-check /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-23-verifier-spotcheck.md:64): the 266 SCOPE-PATH-DENIED findings come from at least four mechanically different denial branches in /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-seat-bindings.py:33-58 and :111-112. C1 merges all four into one row per tool. I classified each denied path read-only, using the checker's own `requested_path` and `local` predicates over the frozen bytes at f169b3ba:
   - 182 are lane-local paths whose spelling falls outside the frozen grammar. Of these, 176 are `read` paths with a wildcard or query character, 175 of them with a `?q=` query suffix (for example `<lane>/.ufo/waves/round-23/preregister.json?q=.edit_decisions`). Five are `glob` paths that contain `**`, and one is a `read` of a directory with a trailing slash.
   - 69 are lane-local, well-formed reads of a file that is not bound to the seat.
   - 15 are paths outside the lane.
   - Of the 175 `?q=` reads, 100 target a base file that is in that seat's bound `read_paths`. Those denials come from request spelling, not from a scope overreach.
   - C1's output shows only `SCOPE-PATH-DENIED / read: 230`, which hides this split.
   - 114 of the 266 denials (43%) come from ConnFxPlanner, the seat whose trace is incomplete. The C1 cause rows do not flag that these counts are a lower bound for that seat.
   - [unk] Whether the Fx* seats (144 of the denials) planted their violations on purpose cannot be decided from the retained events.
   Impacted axes: calibration (attribution resolution) and the repair of line 64.
   Smallest safe correction: add a `denial_branch` sub-key computed by the frozen checker's own predicates. Its values are outside-lane, lane-local spelling outside the grammar (query, wildcard, trailing slash), and lane-local unbound. Add a `base_bound` flag for the query-suffix reads and a `from_incomplete_seat` count for each row. All 266 stay denied, so the old grammar is not widened.

4. [obs] "268 of 268 attributed to ... the recorded tool operation of the request at that site" is satisfied for 267 findings. For SCOPE-TRACE-INCOMPLETE the tool substitutes the synthetic string `seat-level trace state` (/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/report-red-causes.py:90-91). No request and no recorded operation exist at site `ConnFxPlanner`.
   Smallest safe correction: report `request_level: 267` and `seat_level: 1` instead of a single 268.

5. [obs] Line 52 repair is real and narrow. The report labels `replace_all` as "author recollection, not recoverable from retained events". It keeps `__unknown_argument__` at `FxC3Build08:17` (`unknown_tokens: 1`), CANNOT_EVALUATE, exit 2 and ConnFxPlanner (125 events, `trace_complete: false`). The selftest passes 9 of 9 cases (`python3 tools/report-red-causes.py --selftest`, exit 0).
   Weakness: `in_retained_events` is computed over every event of every seat (/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/report-red-causes.py:100-109), not over the schema site. [inf] If any other seat had passed a key named `replace_all` to any tool, the recollection would be marked recoverable even though the site at FxC3Build08:17 still holds only the unknown token.
   Smallest safe correction: compare each recollected key against the `retained_keys` of the schema site.

6. [obs] Line 64 has further routed requirements that C1 neither covers nor scopes out: keeping early-retry, scope and receipt debt visible (127 of 140 receipts well-formed) and committing a generator before any new capture. [inf] This is acceptable only if the lesson-routing text states that C1 repairs the first sentence of line 64 and line 52, not the whole of line 64.

## C2 — fitness as a learning claim

7. [obs] Province placement: update-safety is Core. /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/PROVINCE.md:13-14 lists "Update-safety questions: what an -Syu would touch, what pins/holds exist", and :20-22 lists the Arch News gate and Initramfs v42 as Core surfaces. The PROVINCE Frontier (:75-80) holds only handoff acknowledgement and RE arbitration. [inf] C2 is Core, not frontier.

8. [obs] The ground is not uncovered. The coverage map row /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/README.md:10 holds the update-safety plane. Existing entries include update-safety-note, -v2 and -v3, partial-upgrade-recheck-r15, initramfs-v42-sysroot-recovery, boot-chain-r17 and freshness-recheck-r17 and -r18. Same-ground freshness rechecks were already claimed at SCORECARD.md:425/447 (round 15) and :518 (round 17). [inf] Of the four quality-bar routes, only "an entry superseding a weaker one" is available (/home/vgpnk/Projects/shokunin/LEARNING.md:34). C2 is a quality-trend claim. It is not expansion, it is not a SKILL decision table grounded in admitted entries, and it is not a capability shown running.

9. [obs] The declared before-value and the draft's "Supersedes" list name text that round 17 had already superseded, which is false provenance for a quality gain.
   - SCORECARD.md:749 says "the corpus still records 413 pending upgrades and a pending mkinitcpio 42 upgrade". However, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/partial-upgrade-recheck-r15.md:176 (R17-FRESH-PARTIAL-02) already says "413 is not a current-use value".
   - /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/README.md:147-151 already supersedes the "Pending `mkinitcpio` 42 upgrade" Frontier bullet.
   - /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/initramfs-v42-sysroot-recovery.md:63,68 already record 42.2 as installed and the future-upgrade framing as stale.
   - Despite this, the draft /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/pause-lift-gate-r24.md:71-74 supersedes exactly these two items.

   Genuinely weaker live entries that the gate does supersede, but does not name:
   - "The current pending count is UNKNOWN" at /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/host-health-report-r3.md:628, and the R18-FRESH-SUPPLEMENT loci at update-safety-note.md:525, update-safety-v2.md:395 and update-safety-v3.md:461. P1 replaces these with a measured 3.
   - "[unknown] Whether `stable-mirror` lags upstream Arch" at /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/package-state-plane.md:39. P4 addresses this.
   - "namespace emulation; not boot-tested" at README.md:151. P3 now has two completed boots on 42.2 images.

   Impacted axes: freshness (claim axis), quality trend and QUALITY criterion 49.
   Smallest safe correction: rewrite the before-value to the R18 "UNKNOWN" state. Retarget "Supersedes" to the three live loci above, and cite the round-17 supersessions as prior, not as this round's.

10. [obs] The counting instrument accepts gates that the declared rule forbids. I loaded `evaluate()` from /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-pause-gate.py with an in-memory reader (no file writes), and the results were:
    - A gate with `sources_opened: "2026-10-15"` that cites a row opened 2026-10-15 returns exit 0 with `premises_verified` 5. The date is taken from the gate itself (:78, :122) and is not pinned to 2026-10-22.
    - A gate whose evidence lines all point into a round-18 capture returns exit 0 with 5 verified. Any committed path is accepted (:100-115). Nothing binds the evidence to the round-24 capture or to a `capture` field.
    - A gate whose evidence points at its own JSON line 1, containing `tsukuroi-pause-gate-v1`, returns exit 0 with 5 verified. This is self-citation.
    - A gate built to the schema in the assignment (`captured_at` and `capture`, no `sources_opened`) returns exit 1 with GATE-SCHEMA and 0 verified. The checker and the declared schema disagree.
    - The selftest passes 15 of 15 cases (`--selftest`, exit 0) but covers none of these four cases.

    Impacted axes: freshness (claim count) and instrument soundness.
    Smallest safe correction: pin the opened date to 2026-10-22, or bind it to the declaration date. Require every `evidence.path` to equal the gate's `capture` field. Require that capture to be committed, with its sha256 matching the `capture.sha256` beside it. Reject the gate's own path and corpus paths as evidence. Reconcile the schema field names with the assignment's schema. Add the four cases above as negative selftests.

11. [obs] The identity of the evidence base has drifted. The assignment names the committed /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/capture/l1/capture.txt (198 lines). That file has no mirror `Server` line, no `pacman -Sy`, `paccache` or `-Scc` lines, and no cache file count, so P4 and P5 cannot be evidenced from it (a grep for these patterns over l1 returned nothing).
    - Those lines exist in the committed `l1-2/capture.txt` (lines 201, 228-230, 234) and in the uncommitted `l1-3/capture.txt` (lines 194, 221-223, 227). The `capture.sh` behind l1-3 is a working-tree modification (`git status`: ` M .ufo/waves/round-24/capture/capture.sh`).
    - The draft gate md cites `l1-3` (pause-lift-gate-r24.md:1-2). That capture was taken at 2026-10-22T08:39:10Z (l1-3 `capture.txt:3`), and the md was rewritten at 05:39:29 -03 while this review was running.
    - [inf] Three captures with different line numbers, one of them uncommitted, plus a narrowed script mean that "a line in the committed round-24 capture" (SCORECARD.md:749) no longer has one identity.
    - I tested whether the narrowed plymouth grep hides error lines: it removes only "Dispatch Password Requests ... skipped" lines and sudo lines that matched a package filename, and it adds shutdown lines. No error line was dropped. That change is benign.

    Smallest safe correction: before measuring, commit exactly one capture together with its script, name it in the gate's `capture` field and in the declaration, and mark the other two as superseded runs.

12. [obs] Hidden coupling between P1 and P4. The gate summary says "A full upgrade now updates 3 third-party packages, none in the boot chain" (pause-lift-gate-r24.md:58). However, `-Syu` refreshes the databases first, and P4 records core and extra database mtimes of 2026-10-17 (l1 `capture.txt:31-32`). [inf] The 3 is a count against the local databases. It is a statement about a future `-Syu` only if the stable mirror's current `core.db` Last-Modified equals the local mtime, which is P4's own falsifier at :67.
    Smallest safe correction: scope P1's summary to "against local sync databases (snapshot 2026-10-17)", or make P1 cite P4's header evidence.

13. [obs] Duplicate authority and a contract breach. An untracked `corpus/knowledge/pause-lift-gate-r24.md` already exists inside production `corpus/` (`git status`: `??`), carrying verdicts. The JSON, which is the only file the checker reads, does not exist (`stat`: no such file), so `python3 tools/check-pause-gate.py --revision 10b45f050c16f5f1d4f7e15a285d9f5294f7a486` exits 1 with GATE-MISSING. [unk] Whether the L1 or a seat wrote the md; seats are barred from writing to corpus/. [inf] Verdicts in the md are checked by nothing, so they can drift from the JSON.
    Smallest safe correction: generate the md's verdict table from the JSON, or have the checker compare the two, and keep any draft outside corpus/ until the L1 integrates it.

14. [obs] Privacy side finding. The committed `l1/capture.txt:168-174` holds raw sudo "(command continued)" argument lists (package cache file paths), captured because the old plymouth grep matched `plymouth-…pkg.tar.zst`. The contract limits sudo journal lines to time, user, command name and flags. [inf] No secret is exposed, but the reduction rule is breached in committed history. l1-3 no longer captures these lines.
    Smallest safe correction: the L1 records this as a disclosed limit, and the gate does not cite l1 lines 168-174.

## Fixable defects and tradeoffs

- Fixable: findings 3, 4, 5, 9, 10, 11, 12 and 13 each have a local correction that keeps the frozen cohort, status, exit and the targets unchanged.
- Tradeoff for the judge: finding 1 (C1's delta is the instrument's own existence) and finding 8 (C2 is a fourth same-ground update-safety recheck, which can count only as quality-trend supersession) cannot be repaired by editing. The canonical judge should credit C1 as calibration at the resolution it actually adds, and credit C2 only for the live weaker loci it supersedes, not as expansion or frontier learning.

Scope: read=PROVINCE.md, SCORECARD.md:740-751 and earlier claim rows, corpus/lessons/round-23-verifier-spotcheck.md, corpus/QUALITY.md, corpus/README.md, corpus/SOURCES.md rows, corpus/knowledge (pause-lift-gate-r24.md, partial-upgrade-recheck-r15.md, initramfs-v42-sysroot-recovery.md, host-health-report-r3.md, package-state-plane.md), tools/report-red-causes.py, tools/check-pause-gate.py, tools/check-seat-bindings.py, .ufo/waves/round-24/capture/{l1,l1-2,l1-3}/capture.txt, round-23 falsify bindings/events/falsify-limit at f169b3ba, /home/vgpnk/Projects/shokunin/LEARNING.md and CORPUS.md (read-only), /home/vgpnk/.agents/skills/godspeed; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w1/CritLearningFit.md, /tmp/critlf-{seat,red,ev,b}.json (scratch copies of tool output and committed blobs); executed=python3 tools/check-seat-bindings.py --revision f169b3ba ... (exit 2), python3 tools/report-red-causes.py --revision 10b45f05… (exit 0) and --revision f169b3ba… (exit 0) and --selftest (exit 0), python3 tools/check-pause-gate.py --revision 10b45f05… (exit 1) and --selftest (exit 0), in-memory python probes of evaluate()/requested_path(), read-only git log/show/status/diff/ls-files, stat, wc, grep, date
Installs: none
