Verdict: partly holds. C1 is verified as declared: the declared counter itself reads 12 of 12 at the tip, so changing the counter after wave 1 did not narrow the target. But the lesson's statement that the counter change "can only refuse more" is contradicted by the lane's own battery receipt. Only O01 to O04 add new sourced depth. C2 is verified as counted (3 of 8 before, 0 of 8 after, at 409ceed4 and at the tip). However, "the eight lane tools ... no longer follow" overstates a fix that touched 3 tools.

Revision under attack: lane tip `10d5288fc1051364e711203855e7c53710dfcc21`. The L1 after-receipts are at `409ceed4`. All runs happened in the sandbox clone `/fast/scratch/hyaku/tsukuroi-r29/CritClaimFraming2/repo`, with `GIT_DIR`, `GIT_WORK_TREE` and `GIT_INDEX_FILE` unset. Evidence copies are in `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w2/CritClaimFraming2/`.

## Verdict per claim

- **C1 (depth): holds as counted.** The counter change is a re-specification, not a narrowing:
  - The frozen target is byte-identical.
  - Hollow-marker refusal is much stricter.
  - Six format variants are newly accepted.
  - The after-value does not depend on those relaxations, because every counted marker also passes the declared counter.
  - The framing over-reports in two places. Depth is added only by O01 to O04; O05 to O12 carry corrections that already existed at the claim base. Also, four of the twelve markers cite no `S###` source at all.
- **C2 (operability): holds as counted; the wording overstates it.** The movable quantity was 3 tools. The other 5 never leaked.

## Findings

1. [obs] **Both C1 counters read 12 of 12 at the tip, exit 0.**
   - Declared counter, extracted with `git show 81a061a6:tools/check-owed-statements-r29.py` (sha256 `5b6cf227580ff26e…`): `{"revision": "10d5288f…", "items": 12, "marked": 12, "unmarked": []}`, rc 0. Copy: `c1-v1-tip.jsonl`, sha256 `6d3483ab38777ce6…`.
   - Version 2 (sha256 `c3f9cfe73e980db9…`): the same result, rc 0. Copy: `c1-v2-tip.jsonl`, sha256 `dc8f5a5e4b741e2c…`.
   - The L1 receipts at 409ceed4 agree: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/measure/c1-after-v1counter-409ceed4f067f4296f27fcb9cb843c7ca54d2e5d.jsonl:13` and `c1-after-409ceed4….jsonl:13`.
   - Before: 0 of 12 under the declared counter (`c1-before-81a061a6….jsonl:13`).
   - The only file in the six C1 targets that changed between 409ceed4 and the tip is `SKILL.md` (one line). The tip re-run covers it.

2. [obs] **The C1 target was not narrowed.**
   - The `ITEMS` tuple (ids, files, rows, fields, anchors) is byte-identical in v1 and v2. A Python slice compare from `ITEMS = (` to `KERNEL_MECHANISM` gives `ITEMS identical: True 1548`.
   - The `KERNEL_MECHANISM` set is still O01 to O04.
   - The declared counter, which was committed before any counted run, reaches the declared after-value on its own. So the post-wave-1 rewrite cannot have manufactured the result.

3. [obs] **"Version 2 can only refuse more" is false, by the lane's own receipt.**
   - In `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/measure/c1-battery-counter-v1-81a061a6.jsonl` (last line), the declared counter refuses 6 of the battery's 7 should-pass shapes:
     - G1: `now` restates the anchor in a dated qualifier.
     - G2: `now` quotes the literal tool output that equals the anchor.
     - G3: the S149 row contains `||`.
     - G5: bold marker id.
     - G6: JSON basis given as one string.
     - G7: basis path without an extension.
   - Version 2 accepts all six (`c1-battery-counter-v2-409ceed4.jsonl`: `"should_pass_refused": 0`).
   - The diff shows each relaxation:
     - the marker regex gains `\]\**` (bold);
     - M5 drops v1's `anchor in now` refusal and strips the anchor before counting;
     - `PATHREF` drops the required `\.[A-Za-z0-9]+` extension;
     - basis may be a plain string;
     - cells now split on unescaped pipes.
   - Contradicted text:
     - `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-29.md:34`: "Version 2 can only refuse more: a marker it counts also satisfies version 1's rules." (`grep -cF` → 1)
     - `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-owed-statements-r29.py:15`: "every change below only refuses more" (`grep -cF` → 1)
   - Strength of the change: the declared counter accepted 20 of 25 should-fail shapes; v2 accepts 0 of 25 (same receipts).
   - [inf] So v2 is a net tightening on substance (hollow `now`, irrelevant basis, hidden or duplicated markers, rewritten originals) and a relaxation on format only. Impacted axis: calibration. The disclosure is false; the count is not.

4. [obs] **Only O01 to O04 add new sourced depth.**
   - O01 to O04 cite S148 and S149, which were opened this round. Their `now` text adds new numbers: +200 equals 3,381,800 or 3,172,200 points, about 12.1 to 12.9 GiB. They also add the argmax rule and the cgroup scope (`corpus/knowledge/oom-event-plane.md:497,499`; `kill-event-deep-r8.md:400,402` at the tip).
   - O05, O06 and O07 cite `corpus/knowledge/memory-pressure-r25.md:387,390`. At the claim base `16e9ab2a`, those lines already carry the `OOMRules=` and `systemd-oomd.socket` qualifiers ("Units with `OOMRules=` are also monitored (S121 lines 1633-1644; S123 lines 115-116)").
   - O09 to O12 paraphrase `storage-health-r26.md` lines 128, 135, 133 and 129 as they stood at `16e9ab2a`. For example, the base line 128 reads "only write, read and flush have shorter names in sysfs", and O09's `now` reads "Only write, read and flush take shorter names in the sysfs view".
   - O08 closes its `[unk]` from round-27 capture lines 45, 49 and 55, which were present at the base.
   - [inf] So 8 of 12 items propagate existing corrections or evidence into companion files: QUALITY 67, which is calibration and freshness work. CritAxisFraming's finding 3 holds: it said 7 of 12 copy corrections, plus O08, which is freshness.
   - The ordinal is declared as depth 8 → 8, so this does not falsify the claim. It does bound what the report may say.

5. [obs] **"source-backed" is broader than the claim wording suggests.**
   - Four markers have no `S###` in their resolved basis: O05, O08, O10 and O11 show `"sources": []` in `c1-v2-tip.jsonl`. They rest on repository lines or a capture only.
   - O10's own basis says the systemd v262 reading is "not registered in corpus/SOURCES.md, so no S id exists for this claim".
   - Declared M6 allows `path:LINE`, so the count stands. The phrase "source-backed correction marker" should read "a correction marker with a resolvable basis (an `S###` row or a repository line)".

6. [obs] **False provenance: S150 is not cited by any O01 to O04 marker.**
   - The resolved bases of O01 to O04 list only S148 and S149, with `unresolved` empty (`c1-v2-tip.jsonl` lines 1-4).
   - `grep -n S150` over `oom-event-plane.md` and `kill-event-deep-r8.md` at the tip finds nothing. The only use in SKILL is `SKILL.md:2545`.
   - Yet `corpus/lessons/round-29.md:3` says "O01 to O04 cite S148, S149 and S150".
   - The S150 used-by cell in `corpus/SOURCES.md:156` and the registry note at `round-29.md:16` both list `corpus/knowledge/oom-event-plane.md, corpus/knowledge/kill-event-deep-r8.md`. Neither file cites S150.
   - Impacted axis: calibration (registry truth).

7. [obs] **C2 is 0 of 8 at the tip.**
   - The tip changed `tools/check-adjacency-overlap.py` (296 lines) after the 409ceed4 receipt, so the 409ceed4 receipt alone did not cover the tip. I re-ran the probe there.
   - Command: `python3 tools/probe-git-env-leak.py --revision 10d5288f… --lane <clone> --scratch <seat>/probe`. Result: rc 0, `"targets": 8, "leaking": 0, "harness_errors": []`. The probe sha256 `46a55ce7…` is unchanged from the declaration.
   - Copy: `c2-tip.jsonl`, sha256 `9907cfa24a80078a…`.

8. [obs] **C2's after-value moved 3 tools; 5 never leaked.**
   - At `81a061a6` only `check-adjacency-overlap.py`, `mutants-adjacency-overlap.py` and `mutants-kernel-taint.py` leak; the other five show `control_rc 0, canary_rc 0` (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/measure/c2-before-81a061a67466c5e1be812814a895a4b5ed89b4ff.jsonl:1-9`).
   - All three leaks are exit-code differences with `"canary_changed": false`. The tools' git calls followed the inherited variables and failed, but no write into the canary was observed.
   - The current wording overstates this:
     - `SCORECARD.md:1104`: "the eight lane tools that run git writes ... no longer follow"
     - `round-29.md:3`: "the eight lane tools ... stop following"
   - Both imply all eight did follow before. CritAxisFraming's finding 7 holds.

9. [obs] **The fourth leaker, outside the frozen set, is clean at the tip.**
   - `tools/check-self-assessment.py:1001` now passes `env=env` to `git init`.
   - A canary run from the clone checkout (GIT_DIR, GIT_WORK_TREE and GIT_INDEX_FILE pointed at a canary in my scratch) gives control rc 0, canary rc 0, and the canary file digests unchanged.
   - It is fixed but not counted, as the lesson says. [inf] The declaration's "widened ... to every tool with a sandbox git write" (`SCORECARD.md:1104`) is still false as a universal (CritAxisFraming finding 6): the frozen grep matches 8 tools, not every writer.

## Exact wording the report must use

- **C1:** "C1 (depth) verified: `marked` 12 of 12, exit 0, at `10d5288f`, under the declared counter (`5b6cf227…`) and under counter version 2 (`c3f9cfe7…`), which was rewritten after wave 1 over the same twelve frozen anchors (before 0 of 12). Version 2 refuses hollow markers the declared counter accepted (should-fail battery 20 of 25 → 0 of 25). It also accepts six format variants the declared counter refused (G1, G2, G3, G5, G6, G7). No counted marker depends on them. New depth is in O01 to O04 (the kernel victim-selection reading, from S148 and S149, opened this round). O05 to O12 carry corrections and evidence already in the lane at `16e9ab2a` into their companion files (QUALITY 67). O05, O08, O10 and O11 rest on repository lines, not on an `S###` row."
- **C2:** "C2 (operability) verified: `leaking` 3 of 8 at `81a061a6` → 0 of 8 at `409ceed4` and `10d5288f`, `harness_errors` empty, exit 0. Three of the eight frozen targets followed an inherited `GIT_DIR`, `GIT_WORK_TREE` or `GIT_INDEX_FILE` at the declaration: `check-adjacency-overlap.py --selftest`, `mutants-adjacency-overlap.py` and `mutants-kernel-taint.py`. These were seen as changed exit codes, with no canary write. The other five did not leak before. `check-self-assessment.py --selftest`, outside the frozen set, was fixed too and is not counted. The set is the eight tools matched by the frozen grep, not every lane tool with a git write."
- **Corrections owed in the lane:**
  - `round-29.md:34`: replace "Version 2 can only refuse more: a marker it counts also satisfies version 1's rules." with "Version 2 refuses more hollow shapes but is not a superset of version 1's refusals: it accepts six should-pass shapes version 1 refused (G1, G2, G3, G5, G6, G7); every marker counted at the tip passes both versions."
  - `tools/check-owed-statements-r29.py:15`: replace "every change below only refuses more" with "the changes refuse more hollow shapes; bold ids, anchor-quoting `now`, one-string basis, extension-less paths and escaped pipes are newly accepted".
  - `round-29.md:3`: change "O01 to O04 cite S148, S149 and S150" to "O01 to O04 cite S148 and S149; S150 is cited in `SKILL.md`".
  - S150 used-by, at `corpus/SOURCES.md:156` and `round-29.md:16`: drop `corpus/knowledge/oom-event-plane.md` and `corpus/knowledge/kill-event-deep-r8.md`.

Scope: read=SCORECARD.md:1097-1110, corpus/lessons/round-29.md, .ufo/waves/round-29/w1/CritAxisFraming.md, .ufo/waves/round-29/measure/{c1-before,c1-after,c1-after-v1counter,c2-before,c2-after,c1-battery-counter-v1,c1-battery-counter-v2}*.jsonl, git diff 81a061a6..10d5288 of tools/check-owed-statements-r29.py, git diff --stat 409ceed4..10d5288, tools/probe-git-env-leak.py:1-60, the O01-O12 markers at the tip, git show 16e9ab2a of storage-health-r26.md:127-136, memory-pressure-r25.md:385-391 and capture.txt:45,49,55, corpus/SOURCES.md:156-157, SKILL.md:2545; wrote=.ufo/waves/round-29/w2/CritClaimFraming2.md, .ufo/waves/round-29/w2/CritClaimFraming2/{c1-v1-tip.jsonl,c1-v2-tip.jsonl,c2-tip.jsonl}, scratch under /fast/scratch/hyaku/tsukuroi-r29/CritClaimFraming2/; executed=git clone --no-local and checkout 10d5288 into seat scratch (repo, mut), with GIT_* unset; read-only git show/diff/log/ls-files; python3 counter-v1.py and tools/check-owed-statements-r29.py --revision 10d5288 (rc 0, 12 of 12 each); python3 tools/probe-git-env-leak.py --revision 10d5288 (rc 0, 0 of 8); ITEMS byte compare; a canary run of tools/check-self-assessment.py --selftest with GIT_DIR, GIT_WORK_TREE and GIT_INDEX_FILE pointed at a scratch canary (control 0, canary 0, unchanged)
Model: not exposed
Installs: none
