VERDICT: defect-found — the battery is faithful (all 14 controls fail/pass for their named reasons) but it misses all five named cheap writers plus a sixth found while attacking; two of the built writers PASS where they should FAIL (marks leg is a byte-presence leg, not an assertion leg; the README negation denylist is incomplete).

# Seat: GCritBattery — item C2-A3 (attack the C2 pre-data battery)
Scope: `.ufo/waves/round-48/controls/battery-c2.py` + `battery-summary-r48-c2.jsonl`, scored semantics of frozen `tools/check-scrub-admission-r48.py` @ ae99f021. Fixtures: shared clones of the lane @ BASE 5fdf062f under /fast/scratch/hyaku/tsukuroi-r48/GCritBattery (each toplevel-asserted, commits inside the clone only, `user.name=ctl`), scored with the counter extracted at ae99f021 (sha256 eab29058…, byte-identical to the worktree copy; battery file itself sha256 e127c588… byte-identical to the frozen blob — `git show ae99f021:…` vs worktree, both hashes reproduced under `ls`/sha256sum above). Receipts: `.ufo/waves/round-48/w2/GCritBattery/` (per-fixture counter JSON + full `git diff BASE..fixture` patch + gcritbattery-summary.jsonl + driver.py + frozen-counter.py). Scratch removed after copying.

## 1. Battery audit — every control is what its name says, every FAIL for the intended reason
Cross-checked each JSONL leg set against the counter's legs (`git show ae99f021:tools/check-scrub-admission-r48.py`, run() per-row logic):

| case | legs (s,q,v,m) | named reason | leg verdict |
|---|---|---|---|
| K0 do-nothing base | 1,3,0,0 | no seats, no marks | ✔ |
| K1 marks-only | 1,3,0,3 | marks alone cannot admit | ✔ |
| K2 forged cohort, stale hash | 1,3,0,3 | hash ≠ current → 0 credited | ✔ (nit: hash used is `'0'*64`, not a *stale* real hash — my hashswap covers that) |
| K3 partly + bad citation | 1,3,2,3 | negative still blocks: `blocking` is verdict+hash, citation-independent (A2) | ✔ |
| K3b partly + clean citation | 1,3,2,3 | same leg from the reviewer side | ✔ |
| K3c contradicting body line | 1,3,2,3 | ANY_VERDICT_RE re-reads the seat as `partly` → blocks | ✔ |
| K3d two-byte `fails` | 1,3,2,3 | format-thin negative still blocks | ✔ |
| K4 byte-identical bodies | 1,3,0,3 | K23 distinct-bodies: equal body sha256 → `distinct` false | ✔ |
| K5 GR1 reviewers only | 1,3,2,3 | roles ⊆ {reviewer} ≠ {reviewer, critic} | ✔ |
| K6 unpinned citation | 1,3,2,3 | unbound-for-credit, GR3 left with 0 credited | ✔ |
| K7 no dispatch/results | 1,3,0,3 | 'dispatched 0 times' → unbound | ✔ (covers only the both-absent shape — see §2) |
| K8 negating README | 1,3,3,2 | NEGATE_RE hits → readme mark 0 | ✔ (only ONE phrasing — see defect D2) |
| F1a stray inner `## ` | 0,2,0,3 | structural fails closed inside GR1 extent | ✔ |
| K9 valid synthetic cohort | 1,3,3,3 | PASS capability of the counter | ✔ |

Summary verdicts all `as_expected: true` (14/14). Battery file is the frozen blob (e127c588…), so controls are pre-data as declared.

## 2. The cheap writers it is missing — ALL FIVE, plus three more found in the attack
Built and scored (driver `w2/GCritBattery/driver.py`; per-fixture JSON + diff receipts):

| fixture | mechanism exercised | score | reading |
|---|---|---|---|
| hashswap (missing writer 1) | every seat carries ANOTHER row's real section hash (GR1→GR2, GR2→GR3, GR3→GR1) with real snapshot citations | FAIL v0 | correct: `h == cur` fails, 0 credited. Missing battery case — K2's `'0'*64` never proved a *real sibling* hash can't cross-bind. |
| crlf (missing writer 2) | all 18 reports CRLF | FAIL v0 | correct: `VERDICT_RE.fullmatch` rejects `'…holds\r'` → unbound. Missing battery case. |
| crlfbody (companion) | LF headers, CRLF body | PASS | correct: byte-strictness confined to the two binding lines; a seat CAN quote CRLF content. |
| roleswap (missing writer 3) | counted names dispatched with swapped agent role | FAIL v0 | correct: `agent reviewer != critic`/`agent critic != reviewer` per seat — role laundering impossible; name↔role binding is bidirectional. Missing battery case (K5 only removed critics). |
| resultsonly (missing writer 4) | reports + results.json entries, EMPTY dispatch | FAIL v0 | correct: binding is dispatch-first; `hits==0` before results are read — a forged results.json earns nothing. Missing battery case (K7 only covers both-absent). |
| fencemarks (missing writer 5) | all three marks written only inside ```text fences, verbatim correct lines | **PASS** | **DEFECT D1** below. |
| readmeslip (found in attack) | README line `- btrfs-scrub-grounding-r45.md not yet admitted round 48`; entry+skill marks real | **PASS** | **DEFECT D2** below. |
| staleverdicts (found in attack) | GR1 critic `partly` on GR3's real hash; GR2 critic `fails` on GR1's real hash | FAIL, but GR1 row_ok **True** | ASYMMETRY A1 below. |
| foreignverdict (found in attack) | GR1 reviewer body quotes its peer's TRUE line `"ROW GR2 VERDICT: holds"` | FAIL, GR1 blocked | OVER-TRIP A2 below. |

## 3. Defects (PASS where it should FAIL)

### D1 — marks leg credits marks written inside fenced code blocks. Fixture: fx-fencemarks.
Frozen counter marks legs are pure line-presence (`MARK_ENTRY in entry_lines`, `MARK_SKILL in skill_lines`, README `any(all(x in ln …))`); no fence state is tracked, so a verbatim mark line inside a ```text block counts. The fixture appends only *quoted examples*:

```
entry tail:  Example of what a real gate mark would look like (quoted, not asserted):\n\n```text\n## Gate status — round 48 (GR1-GR3 admitted)\n```
SKILL tail:  ```text\n## Scrub grounding — round 48 admission\n```
README tail: ```text\n- btrfs-scrub-grounding-r45.md admitted round 48\n```
```
(bytes verbatim in `fx-fencemarks-diff.patch:190-220`). Counter output `fx-fencemarks-counter.json`: `marks {entry:true,readme:true,skill:true}`, marks_ok 3, verdict **PASS**. Nothing in the fixture asserts admission; a cheap writer that only documents the mark format satisfies the leg. Note the entry mark lands after `## How this changes OS triage` (outside every row extent), so structural_ok stays 1.
Smallest correction: fence-aware mark scan (track ``` toggles per file, or require the mark line at top level); alternatively declare marks a byte-presence check and accept the weakness — judge's call whether "written" means "asserted".

### D2 — NEGATE_RE denylist is incomplete; `not yet admitted` earns the README mark. Fixture: fx-readmeslip.
`NEGATE_RE = unadmitted|not admitted|never admitted|stay pending|stays pending`. The line `- btrfs-scrub-grounding-r45.md not yet admitted round 48` is a plain-language negation of admission that matches none of the alternation (`'not yet admitted' ⊄ 'not admitted'`). Fixture diff `fx-readmeslip-diff.patch:198`; counter `fx-readmeslip-counter.json`: readme mark true, marks_ok 3, verdict **PASS**. K8 proved exactly one negation phrasing; the leg is a denylist against an open phrasing space — `admission withdrawn`, `reverted`, `superseded`, `no longer admitted`, `admission: FALSE` all slip the same way. Neighbourhood note: the base README already contains `…not admitted.` (round-44 status line); it is protected only because it does not co-occur with `btrfs-scrub-grounding-r45.md` on one line.
Smallest correction: extend NEGATE_RE (`not yet|no longer|withdrawn|reverted|superseded|false|denied|pending\b`) or invert to an allowlist (require the exact declared mark line, e.g. `btrfs-scrub-grounding-r45.md admitted round 48` as a full-match line).

## 4. Asymmetries / over-trips (fail-closed side; not claim-violating, but they contradict the *declared* predicate wording "no seat on the CURRENT row hash reading partly or fails")

### A1 — `fails` blocks on ANY hash; `partly` blocks only on the current hash. Fixture: fx-staleverdicts.
`blocking = verdict in (partly,fails) and s.hash == cur` but `any_fails` is hash-blind. Measured: `R48CritGR1a` `partly` on GR3's hash → GR1 row_ok **true** (5 credited); `R48CritGR2a` `fails` on GR1's hash → GR2 row_ok false via `any_fails` alone (`blocking: []`, `fx-staleverdicts-counter.json`). Two bound-format negatives with identical staleness are treated differently; the declared per-row condition ("no seat on the current row hash") is satisfied in both cases, so `fails`-on-stale-hash is stricter than the claim — a false-FAIL risk for a real seat that misbinds, never a false-PASS.

### A2 — ANY_VERDICT_RE over-trips: quoting a true sibling verdict is a "self-contradiction". Fixture: fx-foreignverdict.
A GR1 reviewer whose body quotes `ROW GR2 VERDICT: holds` (verbatim true — the GR2 report says exactly that) is rebound as `partly` with detail `contradicting line ROW GR2 VERDICT: holds` and blocks GR1 (`fx-foreignverdict-counter.json`). Even a *consistent* foreign token (`r != row` alone suffices) trips A2's contradiction path. Real-seat hazard: a seat quoting a peer's binding line (a plausible evidence style) silently becomes a negative. Fail-closed, but worth a warning line in seat prompts: never write `ROW GR* VERDICT:` tokens except your own line 1. Smallest correction: restrict ANY_VERDICT_RE to the seat's own row (drop the `r != row` arm) or to lines disagreeing with the declared verdict on the *same* row.

## 5. Residual notes
- Hashswap/CRLF/roleswap/results-only all FAIL for the right mechanisms (detail strings above; receipts). The counter's binding order is dispatch → results → report file → header fullmatch → contradiction scan → hash → citations, and every stage is enforced.
- Also probed in analysis (no fixture needed): duplicate dispatch entries → 'dispatched 2 times'; results entry with wrong/missing agent → 'not exactly one results entry'; non-UTF-8/short/uppercase-hash reports → unbound; a report naming the wrong row in line 1 → unbound (never cross-credits).
- No pacman/pip installs made; stdlib python3 + git only. One counter run per fixture, sequential; no selftests run (not this seat's item).
- Not done (out of scope, stated honestly): no re-run of the full battery-c2.py itself (its JSONL legs were verified against counter semantics line-by-line instead); no mutation of seats' real w2 dispatch/results.
