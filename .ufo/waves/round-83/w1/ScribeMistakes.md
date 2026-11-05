# Round 83 · wave w1 · seat ScribeMistakes — report

Scope: draft the `## Mistakes` table for `corpus/lessons/round-83.md`. Draft at
`.ufo/waves/round-83/w1/ScribeMistakes/draft.md` (sha-free plain file; written with `write`).
No lane file, instrument, fixture, manifest, `.ufo/state/`, or sibling repo was edited. No git or jj mutation was run.

## Verification (read or grep, all pointers resolved)

| Row | Pointer checked | Result |
|---|---|---|
| R83-CHRONOLOGY | `SCORECARD.md:7086`, `:7088`; `controls.txt:1-5` | resolved; `:7086` heading and `:7088` "Chronology, stated plainly" match the frozen commit `d78b3b39` byte-for-byte in line position |
| R82-V2 | `tools/check-scorecard-ordinals.py:102` | resolved: `if key[0] == round_no or True:` |
| R82-V2 red | `controls.txt:33-36` | resolved: r82 counter over late-contradiction fixture → `"finding": "clean"`, rc 0 |
| R82-V5 | `tools/check-anchor-coordinates.py:110` | resolved (`def load`); `grep -n "snapshot_sha256\|digest"` on that file returned no match |
| R82-V5 red | `controls.txt:20-22` | resolved: `rc=0 {'claim': 'C1', 'count': 8, 'target': 8, 'finding': 'met'}` on doctored snapshot |
| R82-V1 | `.ufo/waves/round-82/before/mutants-r82.json:123,126,187,190` | resolved: C16 and M06 `old` strings contain `\\n` |
| R82-V1 reach | `.ufo/waves/round-83/before/do-nothing-reencoded-mutation-r83-at-tip.json` | resolved: `"killed": 24, "total": 26, "genuine_killed": 17, "target_killed": 24, "target_genuine": 17` |
| R82-V3 | `tools/check-scorecard-ordinals.py:204-206`; `controls.txt:50-53` | resolved: raise at :204, handler `_revision.RevisionError` at :206; control shows `CannotEvaluate: absent-at-revision:SCORECARD.md (traceback; R82-V3)` |
| R82-V7 | `corpus/SOURCES.md:344` (13 pipe-fields, used-by cell = field 12) | resolved; cell text quoted in draft |
| R82-V7 knowledge refs | `corpus/knowledge/mount-unit-fstab-plane-r81.md:3`; `.json` rows | resolved: `source: S331 …; S332 …`; `grep -n 'S33[13]'` returns S331 and S332 only |
| R82-V7 census gap | `grep -n 'used-by\|used_by' scripts/sources-census.sh tools/check-knowledge-refs-r68.py` | no match (no reverse used-by check) |
| Seat-harm / provider | `.ufo/waves/round-83/` listing | no `w1-results.json` yet; row written as "none observed" |

## Selftest run (r82 ordinal counter, dead-check-free)

Command (run from my scratch, `TMPDIR` set explicitly):
`TMPDIR=/fast/scratch/hyaku/tsukuroi-r83/ScribeMistakes python3 tools/check-scorecard-ordinals.py --selftest` → exit 0.

Verbatim output:

```
  ok   contradiction: rc=1 findings=1 examined=2
  ok   named-correction: rc=0 findings=0 examined=1
  ok   silent-correction: rc=1 findings=1 examined=1
  ok   single-block: rc=0 findings=0 examined=1
  ok   two-axes: rc=1 findings=2 examined=2
  ok   no-blocks: rc=2 could-not-evaluate no-round-blocks
  ok   hyphenated-name: rc=0 findings=0 examined=1
  ok   ascii-arrow: rc=1 findings=1 examined=1
SELFTEST total=8 passed=8 failed=0
rc=0
```

This supports R82-V2's "no late-contradiction case" claim: all eight cases are green while the
defect at `:102` is present. The late-contradiction shape (correction, then later re-assertion) is absent from the list.

## Observations outside the table (for the L1; not rows)

1. **Control labels.** `.ufo/waves/round-83/before/controls.txt` titles the anchor-digest legs
   "C2 gate" and "C2 positive" (lines 23, 27) and "C2 red-before" (line 20). In `SCORECARD.md`
   those legs are C1.a–C1.c (depth), and C2 is the ordinal calibration claim. The labels in the
   receipt disagree with the frozen declaration. Not a tool defect; the L1 decides whether to note it.
2. **R82-V4 has no row.** The frozen declaration (`SCORECARD.md:7100`) cites R82-V4 (timeout arm
   synthesised as rc 124) next to V1. The spec's row list omits it. I did not draft a row and did
   not verify `tools/mutation-kill-r83.py`'s timeout arm. Open for the L1.
3. **Fix pointers not verified by me.** `bind_digest` (`tools/check-anchor-coordinates-r83.py`),
   positional retirement (`tools/check-ordinals-r83.py`) and `read_scorecard_at` (`:222-229`,
   verified as present) are cited as fixes. I read `read_scorecard_at` only. The battery was not run
   by me (scribe seat, no verification assignment); the controls receipt is the only measurement cited.
4. **Used-by fix choice.** The spotcheck (`corpus/lessons/round-82-verifier-spotcheck.md:187-193`)
   offers two fixes. The draft uses the spec's path (`corpus/lessons/round-82.md`). Alternative not drafted.

## Tools

No tools installed or updated. `python3` (system) was used for one selftest run only.

## Refusals and limits

- Nothing refused. No write outside the two seat-named paths and my scratch dir.
- Scratch: `/fast/scratch/hyaku/tsukuroi-r83/ScribeMistakes/` (empty; created for the selftest's `TMPDIR`).
- Dead or blocked checks: none. Not run: battery, mutation harness, anchor counter (out of seat scope; the controls receipt records their results).
