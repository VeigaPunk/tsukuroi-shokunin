# Round 68 — lesson (tsukuroi, hyaku run 15, attempt 1)

author: tsukuroi L1 (round 68), integrating the wave `.ufo/waves/round-68/` (12 seats, one v1 wave)
basis: declaration `3f6edcc9` (frozen before data; base `42400ec6`); the fenced pre-data receipts in
`.ufo/waves/round-68/before/`; wave results `.ufo/waves/round-68/w1-results.json` and seat receipts in
`.ufo/waves/round-68/w1/` and `.ufo/waves/round-68/drafts/`.

## Gate

**Trigger.** The QUALITY 98 upstream watch fired on Linux v7.3. `$ sed -n '1p' .ufo/waves/round-68/before/src/FETCH.txt`
→ the round-68 pre-declaration fetch line (rc 0). Method: `curl -s --max-time 60 -o <file> <url>`, then `sha256sum`
over the saved bytes (`before/src/SHA256SUMS`).

**Candidates considered (the five v7.2-tag registry families and the v7.3 bytes).**

1. Linux v7.3 `Documentation/admin-guide/cgroup-v2.rst` — digest checks run inside
   `.ufo/waves/round-68/before/src/` with `sha256sum -c SHA256SUMS`:
   `v72-…cgroup-v2.rst` a9433bb0…, `v73-…cgroup-v2.rst` 2750c11a… (rc 0). **Admitted as S286** (`docs`, tier A, located
   quote line 1545, 11 words, `grep -cF` → 1). Supports S138's re-read (RW1).
2. Linux v7.3 `fs/btrfs/sysfs.c` — `$ diff -u` v7.2 vs v7.3: one hunk `@@ -1336,7 +1336,7 @@`, line 1339, a comment.
   **Admitted as S287** (`code`, tier A, located quote line 1339, 7 words, `grep -cF` → 1 on v7.3, 0 on v7.2). Supports
   S158's re-read (RW2).
3. Linux v7.3 `mm/oom_kill.c` — byte-identical to v7.2 (`cmp` rc 0; sha256 452f1348… at both tags). **Rejected**: a
   v7.3 row would repeat S149/S182 with no new authority. Flip: a v7.3 byte change in the file.
4. Linux v7.3 `Documentation/accounting/psi.rst` — byte-identical to v7.2 (`cmp` rc 0; sha256 11c6b712… at both tags).
   **Rejected**: same bytes as S185; S185 is already `rejected` as an exact duplicate of S115
   (`$ grep -n '^| S185 ' corpus/SOURCES.md` → status `rejected`). Flip: an opened, distinct source with class-specific evidence.
5. btrfs-progs v7.3 `CHANGES` — already registered as S285 (round 67). **Rejected** (duplicate).
6. systemd v262.1 — `before/src/FETCH.txt`: "host systemd 262.1-1 (no delta)". **Rejected**: no delta below the host.
7. Kernel stable-series trigger (S243 "stable series" pin) — not opened: kernel.org is outside the allowed read sources
   for this round. **Left open as a named limit** (see Limits in the note), not a reject.

**Admitted:** S286, S287 (registry rows in `corpus/SOURCES.md` after S285; NF 13 each; `status` mined; `used-by`
`corpus/knowledge/linux-v73-pinwatch-r68.md`). **Rejected in-round:** items 3–6 as above.

**Non-author spot-check (LEARNING.md).** Sample, one admit and two rejects, re-derived by the attack seats from committed
or pinned bytes (not the L1's word): R1Reviewer re-ran all eight `sha256` pairs against the pinned copies, the committed
blobs at `3f6edcc9`, and the live `api.github.com` contents; its verdicts agree on S286/S287 (admit) and on items 3–4
(reject, identical bytes). The **closure judge's** spot-check is owed and not recorded here (LEARNING.md: a seat this lane
dispatched is still the lane).

**Note verification (C1 note `corpus/knowledge/linux-v73-pinwatch-r68.md`).** Every evidence command re-run by R1Reviewer
over the pinned bytes; the note's RW1 row states the controller split (15 hunks outside the memory section, 1 inside).

**C2 gate (`tools/check-knowledge-refs-r68.py`).** Built in-round from the lane's header gate pattern. Attacked before
landing by R2Reviewer (two HIGH defects, below) and N1Sentinel (boundary sweep). After the fixes: selftest 21/21
(`$ TMPDIR=<scratch> python3 -B tools/check-knowledge-refs-r68.py --selftest` → `{"selftest": {"cases": 21, "failures": [], "passed": 21, "status": "PASS"}}`, rc 0); live base
`$ python3 -B … --revision 42400ec6 --lane <sandbox>` → `finding_count 0`, `note_count 85`, `registry_id_count 285`, rc 0;
red-before (S999 fixture, sandbox branch `r68-red-before`, fixture `4202136f…`): header gate rc 0 (passes `source: S999`),
new gate rc 1 with `KNOWLEDGE-REF-DANGLING` ref `S999`; master refuses the fixture (rc 2, E-REVISION-NOT-LANDED).

**Sources census.** Run at round start: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` →
rc 0, 0 E-code, 45 W04, 285 rows (`before/census-before-receipt.txt`). Run at the work revision: recorded in the report
(`corpus/SOURCES.md` 285 → 287 rows).

## Mistakes

- **R68-DECLARED-CONJUNCT-FALSE** — class `declaration-overclaim` · evidence: SCORECARD round-68 declaration, C1 cell
  "the changed hunks named and shown outside the memory-controller section"; `.ufo/waves/round-68/drafts/c1/S1Scout-verify.md`
  step 3 (S138 has 16 hunks; hunk 7 at v7.3 line 1939 is the `memory.pressure` access-mode change, inside the Memory
  section); R1Reviewer F2 · captured-by: none — the conjunct was written before the hunk attribution was measured ·
  fix: the note states the true split (15 outside, 1 inside); the C1 verdict is reported per conjunct (falsified on this
  one); an erratum corrects the declaration text; the predicate counters are not amended after data.
- **R68-DECLARED-ANCHOR-OFF-BY-ONE** — class `number-drift` · evidence: SCORECARD round-68 declaration, "oom_kill 1507 → 1533";
  `$ grep -n oom_kill .ufo/waves/round-68/before/src/v72-Documentation_admin-guide_cgroup-v2.rst` → `1506` (the label),
  `1507` is the description line; K1Critic A10, R1Reviewer F1 · captured-by: none — the CORPUS "a quote names its location"
  rule was applied to the note, not to the declaration's own numbers · fix: appended erratum in SCORECARD; the note
  cites the exact lines (`1508 → 1535` for the sentence; `1506 → 1533` for the label).
- **R68-DECLARED-REGISTRY-COUNT** — class `number-drift` · evidence: SCORECARD round-68 declaration, "the five v7.2-pinned
  registry rows"; R1Reviewer F4 enumerates eleven rows pinning v7.2-family bytes
  of the four files (`drafts/c1/R1-attack.md`, row IDs S115,S118,S119,S133,S138,S149,S158,S178,S182,S185,S243) · captured-by: none ·
  fix: erratum; the note re-reads the five named rows and names the other six as limits (their verdicts follow from the
  same four byte pairs; the re-derivation is not performed in this round).
- **R68-FENCE-FAILOPEN-GATE** — class `fail-open` · evidence: the first draft `tools/check-knowledge-refs-r68.py` (sha256
  `d4390b7a…`), R2Reviewer HIGH 1 (`registry_ids_at` had no fence state; a `| S999 |` row inside a fenced example
  registered S999 and every `S999` citation cleared) and HIGH 2 (`\bS\d{3,}\b` dropped glued ids such as `S138_S999`).
  Measured on the fixture branch `r68-defects` (sandbox commit `e0abe77e…`): draft rc 0, `status PASS`, `registry_id_count 286`,
  0 findings; patched rc 1, `status FAIL`, `registry_id_count 285`, two `KNOWLEDGE-REF-DANGLING` findings with ref `S999` ·
  captured-by: the draft's 19-case selftest, which covered the header gate's rules but neither case · fix: registry parse
  fenced like the header gate; id pattern `S[0-9]{3,}` as frozen; selftest cases `fenced-registry-row-is-example` and
  `glued-ids-are-counted` (21 cases). Shown able to fail: the draft reads PASS on the fixture and the patched tool FAILs it.
- **R68-SHAPE-ONLY-DECLARED-COUNTER** — class `vacuous` · evidence: the declared counting command
  `grep -cE '^\| RW[0-9]+ \| '` accepts six boilerplate rows (R1Reviewer F3; K1Critic A1, A2, A6, A8: one unenumerated
  universal, the sha-pair kill rule has no executable command in the counting column); M1Mutation independent kill matrix
  (`probes/m1-kill-matrix.txt`) · captured-by: the declaration said "strict from the start" but its counting column named
  the shape-only grep · fix: the strict counter (`drafts/c1/count-rw-r68.py`, battery `probes/c1-battery.txt`: 5 of 5
  red fixtures below the control's 6, control 6, 14 of 14 extra controls) is reported alongside the declared grep; the
  declared predicate is not replaced after data; the amendment is routed to the next round, declared before data.

## Trend verdicts

- **expansion: improved.** Two registry rows (S286, S287) on the v7.3 ground the lane did not hold; one knowledge entry
  (`linux-v73-pinwatch-r68.md`) cites them; `status` mined, `used-by` names the note.
- **quality: improved.** Five v7.2-tag pins are re-read against the upstream tag the watch fired on; the two changed pins
  carry located v7.3 anchors and a stated applicability (RW6); the gate gap (K1 C1 Attack 2) is closed by an executable
  gate with red-before proof; two fail-open defects were caught before landing and shown able to fail.
- **discernment: unchanged.** The attack seats caught two declaration errors, one falsified conjunct, one declared
  counter that is shape-only, and two tool defects before landing — evidence the adversarial pass works. No non-author
  admit/reject spot-check is recorded in this lesson; the closure judge's spot-check is owed (see Gate).

## Considerthese

Mined one proposal: **Counter-attack scoreboard**, `considerthese/2026-10-26.md:18`
(opened this round). Grounding: E2's `probes/c1-battery.txt` and M1's
`probes/m1-kill-matrix.txt` distinguish malformed-data fixtures from counter-code mutants.
The scoreboard must not conflate their denominators:

| Instrument | Attack cohort | Observed result | Evidence |
|---|---|---|---|
| E2 strict counter | Five malformed-row fixtures | All below well-formed control 6; values 0/1/3/0/5 | `w1/E2Battery.md` |
| M1 independent counter | Six counter-code mutants | Five killed; c3 equivalent for the specified fixture survives | `w1/M1Mutation.md` |
| Frozen literal grep | Boilerplate-only six-row note | Accepted; content conjunct unproved | `w1/R1Reviewer.md` F3 |

This lesson is the proposal's first per-instrument scoreboard, not a claim that
the frozen predicate has been repaired. Other proposals remain untouched.

## Sources

- **S286** — Linux v7.3 `Documentation/admin-guide/cgroup-v2.rst`, opened 2026-11-03, kind `docs`, tier A; used by
  `corpus/knowledge/linux-v73-pinwatch-r68.md`.
- **S287** — Linux v7.3 `fs/btrfs/sysfs.c`, opened 2026-11-03, kind `code`, tier A; used by
  `corpus/knowledge/linux-v73-pinwatch-r68.md`.
