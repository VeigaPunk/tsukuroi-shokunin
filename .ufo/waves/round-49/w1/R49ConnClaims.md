VERDICT: defect-found

# R49ConnClaims — F-4 cross-claim consistency (round 49, wave w1, hyaku run 11)

Seat: EXEC-AUTHORIZED (counters + fixture repos only). Lane repo read-only; every fixture under
`/fast/scratch/hyaku/tsukuroi-r49/R49ConnClaims/` (removed on exit). Receipts:
`.ufo/waves/round-49/w1/R49ConnClaims/*.json` (16 files, each `{"rc": …, "output": <counter JSON>}`).

Frozen bytes read: `git -C tsukuroi-shokunin show 55c07cd3f8bff2e12117c34d57b4c618de74d85c:<path>`.
Lane tip at round start `6256760d…`; lane `master` today `d7cfc27308e8af51b76b5cfe0c656acc1788cefb`
(two commits after the freeze: `32a85560`, `d7cfc273`).

## Bottom line

1. **C1 is causally separable from C2 and C3.** The C1 counter reads only C1-owned paths plus
   digest-pinned snapshots; it PASSes at a revision whose `PROVINCE.md`, `tools/tsukuroi-census.sh`
   and `corpus/knowledge/adjacency-anchors-r19.json` are at BASE bytes, and its JSON is byte-identical
   when the C2+C3 bytes are added.
2. **C2 is NOT separable from C3 at the freeze revision.** `tools/check-adjacency-table-r49.py:187-190`
   promotes the whole `tools/check-adjacency-anchors.py` verdict into a predicate leg, and that checker
   grades the round-19 *inbound* census, one row of which (IN-109) points at `tools/tsukuroi-census.sh`.
   C3's census edit shifts that pointer's line (2642 → 2660) and flips the checker to FAIL, so the C2
   counter FAILs at the freeze revision **with every C2-owned leg passing**.
3. **C2 cannot PASS on the frozen bytes at all.** The first revision where the predicate holds is
   `32a85560`, one commit *after* the freeze, which repins `corpus/knowledge/adjacency-anchors-r19.json`
   IN-109 `found_line` 2642 → 2660. `FROZEN.md:28-30` does not list that file among the post-wave edits,
   and the FROZEN amendment at `32a85560` documents only the control batteries, not the repin.
4. **Latent C1 → C2 coupling.** The same inbound census carries 19 rows targeting `SKILL.md` (largest
   referenced line 1968). Inserting C1's `## Scrub grounding — round 49 admission` line near the top
   (fixture: line 4) makes the checker FAIL with 18 findings and C2 FAIL; appending it at EOF leaves
   those rows intact. The marks leg itself is independent — its placement is not.
5. C3's own counter is separable (it extracts only `tools/tsukuroi-census.sh`). The dependency is
   one-way: C2 → C3.

## Evidence, in order

### E1 — C1 at the freeze revision: only the cohort+marks legs are open; row bytes match FROZEN

```
python3 tools/check-scrub-admission-r49.py --revision 55c07cd… --lane <lane>
→ rc 1; structural_ok 1, corr_ok 1, quotes_ok 3, verdicts_ok 0, seats_ok 0, marks_ok 0
  marks {"entry": false, "readme": false, "skill": false}
  section_sha256 GR1 3a2ba180…, GR2 d4296085…, GR3 43430a14…   (equal to FROZEN.md's table)
```
Receipt `c1-at-freeze.json`. Consequence: the freeze revision is not a legal C1 measurement point;
the gate-status heading (`corpus/knowledge/btrfs-scrub-grounding-r45.md:277`, text
`## Gate status — round 49 (pending; the frozen cohort has not settled)`) plus the SKILL/README marks
must land first — exactly the post-wave edits `FROZEN.md:28-30` allows, and the heading sits at line
277, outside every row extent (GR1 14-55, GR2 56-151, GR3 152-197).

### E2 — C1 with C2/C3 at BASE bytes: PASS (separability, C1 direction)

Fixture `fx1` = clone at `6256760d`, then freeze entry bytes + gate-heading rewrite + SKILL/README
marks + a synthetic 18-seat cohort (`w1-dispatch.json`, `w1-results.json`, 18 reports).
`PROVINCE.md`, `tools/tsukuroi-census.sh`, `corpus/knowledge/adjacency-anchors-r19.json` left at BASE
(byte-identical check: `PROVINCE.md` c2a7beb3504c…, census 375aa7370f84… at both BASE and the fixture).

```
C1@fx1 (C1-only)            rc 0 PASS  structural 1, corr 1, quotes 3, verdicts 3, seats 18, marks 3
C1@fx1b (+ C2/C3 freeze bytes) rc 0 PASS  … same six legs …
C1 output identical across C2/C3 bytes: True
```
Receipts `fx1-c1-armA-c1-only.json`, `fx1-c1-armB-c2-c3-added.json`. The fixture cohort is scaffolding
to probe the counter's read set; it is not and cannot be reported as a round-49 measurement.

Answer to the item's question 3: **yes** — C1's measured revision can be named without the C2/C3
commits landing, because the C1 counter never opens those paths (read set at
`tools/check-scrub-admission-r49.py:52-55`, `:58-84` snapshots, `:191-198`), and the row bytes it
hashes are frozen and verified against FROZEN.md's table.

### E3 — C2 at the freeze revision: FAIL, caused by C3's bytes

```
python3 tools/check-adjacency-table-r49.py --revision 55c07cd… --lane <lane>
→ rc 1 FAIL  adj_rows 7, linked_rows 7, bare_ranges 0, anchors_ok 7, registry_ok 7,
             anchors_checker_rc 1
  problems ["tools/check-adjacency-anchors.py rc=1: …"]
```
Receipt `c2-at-freeze.json`. Every C2-owned leg is at target; only the checker leg fails.

The chain, with the exact bytes:

| Hop | Evidence |
|---|---|
| counter promotes the whole checker verdict | `tools/check-adjacency-table-r49.py:187-190` (`checker = os.path.join(lane, CHECKER)`, `ok = … and checker_rc == 0`) |
| checker grades the round-19 inbound census | `tools/check-adjacency-anchors.py:847-856` reads the registry at `--revision` and evaluates it; `corpus/knowledge/adjacency-anchors-r19.json:2453` (id) / `:2468` (found_line) holds IN-109 with `"classification": "DRIFTED"`, `"found_line": 2642`, `"target_path": "tools/tsukuroi-census.sh"`, `"target_ranges": [[915,970]]` |
| C3's edit moves that line | `git diff -U0 6256760d… 55c07cd… -- tools/tsukuroi-census.sh` hunks `@@ -415 +415,3 @@` (+2), `@@ -604 +606,4 @@` (+3), `@@ -2070,5 +2075,9 @@` (+4), `@@ -2077,11 +2086,13 @@` (+2), `@@ -2101,3 +2112,10 @@` (+7) = **+18 lines before the pointer** |
| the pinned quote moves | `git show 6256760d…:tools/tsukuroi-census.sh \| sed -n 2642p` → `check 'degraded: kernel ring class counts are evidence (D14/D15)' 1 DEGRADED \` ; at freeze the same text is at line 2660 (`grep -n`) |
| observed failure | `anchors-checker-at-freeze.json`: `status FAIL`, `findings [{"id":"INBOUND-CLASSIFICATION-WRONG","site":"corpus/knowledge/adjacency-anchors-r19.json:inbound[108]"}]`, `inbound_by_class {DRIFTED 16, RESOLVES 96, UNRESOLVABLE 1}`; at BASE `status PASS`, findings `[]` (`anchors-checker-at-base.json`) |

Fixture isolation (`fx3` = clone at BASE + freeze `PROVINCE.md`, toggling one file per arm; entry,
`SKILL.md`, `corpus/README.md` stay at BASE in all four arms):

```
A base census, base SKILL        C2 rc=0 PASS  legs=(7,7,0,7,7) checker_rc=0   checker PASS
B freeze census (C3 bytes)       C2 rc=1 FAIL  legs=(7,7,0,7,7) checker_rc=1   checker FAIL, 1 finding @inbound[108]
C base census, SKILL mark@line 4 C2 rc=1 FAIL  legs=(7,7,0,7,7) checker_rc=1   checker FAIL, 18 findings @inbound[14,17,22,…]
D freeze census, SKILL mark@EOF  C2 rc=1 FAIL  legs=(7,7,0,7,7) checker_rc=1   checker FAIL, 1 finding @inbound[108]
byte legs equal B vs D: True
```
Receipts `fx3-c2-*.json`, `fx3-checker-*.json`. Arm B is the isolation proof: the only differing byte
between A and B is the census; the only differing verdict is the checker's, and it names an inbound row
whose target *is* the census.

### E4 — the post-freeze repair and its record

```
git log --oneline 55c07cd…master
d7cfc273 round-49: pre-data control batteries (K0..K-pass per claim) at 32a85560
32a85560 round-49: w1 spec + validated dispatch (73 seats, policy v2); IN-109 repin 2642->2660
git diff 55c07cd… master -- corpus/knowledge/adjacency-anchors-r19.json  → 2 lines (found_line, note)
IN-109 found_line: 55c07cd 2642 · 32a85560 2660 · master 2660
checker 32a85560 → PASS;  check-adjacency-table at master → rc 0 PASS (c2-at-master.json)
```
Two record problems:
* `FROZEN.md` at `master` still says `## Claims (1–3, causally separable, distinct axes)`
  (`FROZEN.md:11` unchanged; the only amendment, +8 lines at EOF, is the control-outcomes paragraph).
  At the freeze revision that assertion is false for C2 (E3).
* IN-109's repinned note says the move was "found_line updated in the round-49 freeze commit"
  (`git show master:corpus/knowledge/adjacency-anchors-r19.json`, IN-109 note tail). It was not: the
  freeze commit still holds 2642; the update is in `32a85560`, and the repin is a file
  `FROZEN.md:28-30` does not authorise as a post-wave edit.

### E5 — C1 marks placement is coupled to C2's checker leg

`corpus/knowledge/adjacency-anchors-r19.json` inbound targets, counted at freeze: `PROVINCE.md` 57
(largest range end 79), `SKILL.md` **19** (largest 1968), plus 15 other files, one row each for
`tools/tsukuroi-census.sh`, `tools/_revision.py`, `tools/check-seat-scope.py`, …
`SKILL.md` at freeze is 4546 lines and the round-45 scrub section starts at line 4286, so an EOF
append (line ≥ 4547) shifts none of the 19 rows; inserting above line 1968 breaks them (arm C: 18
findings, `DRIFTED 14 / RESOLVES 81`). The C1 counter itself accepts the line anywhere
(`tools/check-scrub-admission-r49.py:312-315`, `any(ln.strip() == MARK_SKILL …)`), so the placement
constraint is invisible to C1's own predicate and must be stated at the freeze level.

### E6 — C3 direction (static, no selftest run)

`tools/check-fd-band-r49.py:63-67` extracts exactly one path (`git archive … -- tools/tsukuroi-census.sh`)
and the legs at `:91-95` read that text; the selftest child gets `PATH=/usr/bin:/bin`,
`TMPDIR=<work>/run`, `HOME=<work>` (`:96-98`). No other claim's path is opened. I did **not** run the
`--selftest` leg of the C3 counter (cost + a host under ~90 seats; the sub-second fixture arms were
sufficient for a read-set question). Static conclusion: C3 does not read C1 or C2 bytes; the edge runs
only C2 → C3.

## Couplings found (file:line, and whether separability breaks)

| # | Edge | Where | Breaks separability? |
|---|---|---|---|
| 1 | C2 → C3 | `tools/check-adjacency-table-r49.py:187-190` → `corpus/knowledge/adjacency-anchors-r19.json` inbound[108] → `tools/tsukuroi-census.sh:915-970` / `found_line` 2642 | **Yes, at the freeze revision** (C2 counter FAIL, E3). Point-fixed at `32a85560`; structurally still coupled. |
| 2 | C1 marks → C2 | 19 inbound rows target `SKILL.md`, max line 1968 | Latent: breaks only if the mark is inserted above line 1968 (18 findings measured). EOF append is clean. |
| 3 | C1 → C2/C3 | C1 read set `:52-55`, `:58-84`, `:191-198` | No. fx1 arm A PASS, arm B byte-identical. |
| 4 | C3 → C1/C2 | `check-fd-band-r49.py:63-67`, `:91-95` | No (static). |
| 5 | C1 → pinned snapshots | `snapshots()` `:191-198` drops a quote when a pinned snapshot's digest differs **at the measured revision** | Not a claim read, but C1's quote leg depends on `.ufo/waves/round-4x/frozen/**` bytes at the revision; a post-freeze touch there silently empties `quotes_ok`. |
| 6 | C2 → worktree + sibling repos | checker path is `os.path.join(lane, CHECKER)` (worktree copy, not the revision's); `anchors_ok`/`registry_ok` are shape-only (`:176-181`), substance is `_live_object_hash` over `/home/vgpnk/Projects/shokunin/<sibling>-shokunin` (`check-adjacency-anchors.py:28,456`; `live_object_checked 10 / live_object_match 10`) | Not a claim cross-read, but C2 is not reproducible from the lane repo alone; today worktree checker blob `83a80e88…` equals the freeze blob. |
| 7 | C2 → branch/remote pointers | `bind` steps 4-6 (`tools/_revision.py:18-20`): measured commit must be under `refs/heads/master` **and** `refs/remotes/origin/master` | Fixture arm C returned `CANNOT_EVALUATE refs/heads/master` once the branch moved past it (receipt `fx3-checker-C-skill-mark-top.json`, rc 1). Freeze is an ancestor of both today (`merge-base --is-ancestor … rc=0`). |

## Axes affected

* **claims** — `FROZEN.md:11` asserts causal separability that is false for C2 at the freeze revision;
  the IN-109 note misstates which commit repinned the row. A claim whose counter cannot pass on the
  frozen bytes is not measured by those bytes.
* **cross-claim** — the 7-cell adjacency work is complete and correctly separable, but its *verdict* is
  hostage to a round-19 inbound census row that points at another claim's file. C2 → C3 is a live edge,
  C1→C2 is a placement-sensitive latent edge.
* **depth** — `anchors_checker_rc == 0` grades 113 inbound rows over 17 target files. As a predicate leg
  it cannot distinguish "the seven ownership cells point at the right anchors" from "no round-19
  inbound pointer anywhere in the lane has drifted", so the counter's depth signal is weakened in the
  direction the round cares about (it can FAIL for reasons the claim never moved).

## Proposed move (one, bounded)

**Split the C2 counter's checker leg: accept the checker's outbound verdict, report the inbound
verdict.** In `tools/check-adjacency-table-r49.py:186-202`, replace `checker_rc = p.returncode` with a
JSON read of the checker's stdout:

```
outbound_ok = counts.outbound_portable == 10 and counts.live_object_match == counts.live_object_checked
              and not [f for f in findings if not f['site'].endswith(']')]   # no outbound-site finding
checker_rc  = 0 if (p.returncode in (0, 1) and outbound_ok) else 1
inbound_findings = [f for f in findings if f['site'].startswith(REGISTRY + ':inbound[')]   # reported, not graded
```
plus emit `inbound_findings` and `counts.inbound_by_class` as reported fields. Same file, ~12 lines,
no claim byte touched, checker unchanged.

Why this one: it removes the only *breaking* edge (E3) at its source, it keeps every discriminating
control (K0-K3 fail on `bare_ranges` / `anchors_ok` / `adj_rows`, i.e. the outbound legs), and it makes
C2's PASS independent of whether the round-19 census is currently repinned — so the `32a85560` repin
becomes optional hygiene instead of a hidden precondition. If the L1 prefers the whole-lane invariant,
the alternative is the inverse: keep `checker_rc` and record the repin in `FROZEN.md` (file, lines,
cause) plus the IN-109 note fix — but then C2's claim must be stated as "PASS only at ≥ `32a85560`",
not on the frozen bytes.

Companion constraint (mechanical, one line in the freeze record): **C1's `SKILL.md` mark MUST be
appended at EOF** (below line 1968; the round-49 section starts at 4286, file is 4546 lines), because
an insertion above line 1968 adds 18 checker findings and re-breaks C2 (E5).

## Risks

* Narrowing `checker_rc` hides a genuine anchor regression if it ever surfaces as an inbound finding —
  mitigated by asserting `outbound_portable == 10`, `live_object_match == live_object_checked`, and
  reporting `inbound_findings` on every run so a drifted census is still visible, just not fatal.
* If the round keeps `checker_rc` whole, every future census or `SKILL.md` edit above line 1968 needs a
  census repin in the same commit; the note's history shows this has been missed-then-repaired in
  rounds 32, 38, 39, 42, 47, 48 and again at 49.
* Either variant leaves E6/E7 (worktree checker copy, sibling-repo digests, origin ancestry) untouched;
  they are pre-existing properties of the round-19 gate, not round-49 drift.

## Verification (all commands observed; re-run set after the change)

Observed now: `c1-at-freeze.json` (rc 1, legs above), `c2-at-freeze.json` (rc 1, `anchors_checker_rc 1`),
`c2-at-master.json` (rc 0), `anchors-checker-at-{base,freeze,master}.json` (PASS/FAIL/PASS), four `fx3`
arms and two `fx1` arms as tabulated.

After the proposed change, re-run: `check-adjacency-table-r49.py --revision 55c07cd…` (must now PASS
with the repin absent), `--revision 6256760d…` (must still FAIL, `bare_ranges 9`), the K0-K3 controls
(must still FAIL) and K-pass (must still PASS), then `--revision master` (PASS). For C1, re-run
`check-scrub-admission-r49.py --revision <wave commit>` once the marks land, and `--section-hash` on the
entry to confirm GR1/GR2/GR3 still equal `3a2ba180… / d4296085… / 43430a14…`.

Not run, and not claimed: the C3 counter's `--selftest` leg; no network; no lane mutation; no tool
installed or upgraded.

Write footprint: this seat wrote only `.ufo/waves/round-49/w1/R49ConnClaims.md` and
`.ufo/waves/round-49/w1/R49ConnClaims/` (16 receipts, 80 KB). `git status` also shows
`M corpus/SOURCES.md` (mtime 14:02:34, before this seat's first command) and other seats' untracked
wave files; none of them is from this seat. Every fixture lives under the scratch dir, which was
removed after the receipts were copied. Scratch `/fast/scratch/hyaku/tsukuroi-r49/R49ConnClaims/` removed after the
receipts were copied.
