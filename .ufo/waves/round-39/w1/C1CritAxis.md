VERDICT: defect-found

Seat C1CritAxis, item C1-15 (attack C1's axis and sizing). Read-only on lane content: I wrote only this file and
`.ufo/waves/round-39/w1/C1CritAxis/` (two receipts). No install, no sudo, no pacman, no host mutation; scratch
`/fast/scratch/hyaku/tsukuroi-r39/C1CritAxis/` removed after both receipts were copied. Lane tip read:
`394e1ba4fab39a417abe66a7802f87cf1ff8dd61` (`git rev-parse HEAD`; worktree shows ` M PROVINCE.md` plus untracked
`.ufo/waves/round-39/w1*` — not written by this seat).

Summary: the target is sound (a do-nothing control cannot reach it) and the predicate is one sentence in plan,
code and receipt. The defect is on the axis the claim chose: operability is the artifact **and its stated
outcome**, and the round moved the artifact while leaving the stated outcome at its pre-change value and now
false. The round also leaves its own frozen r38 gate red at tip with a registry row that still advertises the
old exit semantics — the same defect class round-38 closure routed as §6.6.

## 1. Is operability the right axis?

**Signal.** `AXES.md:13` — operability is "Runnable artifacts: checklists that are executable, commands that
exist, scripts that run"; its signal is "A checklist item can be run and produces the **stated outcome**".
`AXES.md:12` files surfaces, tools and **edge classes** under coverage.

**Candidate 1 — operability (declared, `SCORECARD.md:2220`). Admissible on lane precedent.** The changed object
is one runnable gate's verdict mapping, i.e. "gate verdict correctness". Round 12 did the identical shape — a
census silent-blind-spot replaced by an explicit finding — and the verifier graded it operability
(`corpus/lessons/round-12-verifier-spotcheck.md:213`: "operability | improved | Root metadata 0→1, unchanged
six-plane contract, live demonstration and 97/97 selftest"). That commit paired the census with the operator doc
in one commit: `git show --stat 70fede2` → `SKILL.md | 43 +-`, `tools/tsukuroi-census.sh | 291 +++`; the doc
section is `SKILL.md:1676` "## Round 12 — root metadata and create-failure discrimination".

**Candidate 2 — coverage. Refuted by the round's own texts.** A critic can file "hidden/absent sysfs root" as an
edge class under `AXES.md:12`, but (a) the round-38 closure routed it as a defect, not as frontier ground
(`corpus/lessons/round-38-verifier-spotcheck.md:174`: "R38-ABSENT-ROOT: an absent `/sys/fs/btrfs` gives HEALTHY
0/0/0. Add a `/proc/self/mounts` btrfs cross-check under a new frozen counter."), and (b) the round's own province
paragraph says the new read "is not a new owned surface" (PROVINCE.md, round-39 limit-closure section — present
**only in the uncommitted worktree** at `394e1ba`, `git diff PROVINCE.md`).

**Candidate 3 — depth. Defensible and worse.** The change is literally a decision-table row with a named error
signature (`detail=mounts:btrfs-without-sysfs`) and a threshold (fsid count 0 ∧ btrfs-mount count > 0),
`tools/tsukuroi-census.sh:1903-1914`. But choosing depth collapses C1 into C2 under AXES.md "two claims on one
axis in one round count as one claim", costing the round its second claim. Operability is the better of the two
admissible labels; keep it and finish the move.

**Where C1 fails the axis it chose.** Operability is artifact ∧ stated outcome. The artifact moved at `49cc53c`
(`tools/tsukuroi-census.sh:1903-1914`); the stated outcome did not:

- `SKILL.md:3137` still reads, for `state=HEALTHY filesystems=0 devices=0 nonzero=0`: "The sysfs root is absent.
  Declared as \"no btrfs mounted\", but a namespace or container that hides `/sys/fs/btrfs` prints the same line
  (wave-1 C1CritAbsentRoot)" — the exact behavior the claim says it removed.
- The `detail` grammar at `SKILL.md:3131-3133` and `:3140` lists `unreadable`, `malformed`, `no-devinfo`,
  `bad-devid`, `root:unreadable`. Neither `mounts:btrfs-without-sysfs` nor `mounts:unreadable` appears in the
  operator section: `grep -n "mounts:" SKILL.md` → only the registry row `:3116`.
- `git show --stat 49cc53c` → `corpus/knowledge/adjacency-anchors-r19.json`, `tools/tsukuroi-census.sh`. No doc.
- The row is byte-unchanged from base:
  `git show 0eff65b2:SKILL.md | grep -n "The sysfs root is absent"` → `3135` (same text);
  `git diff 0eff65b2 394e1ba -- SKILL.md | grep -c "sysfs root is absent"` → `0`.

One command shows the contradiction at tip (receipt `.ufo/waves/round-39/w1/C1CritAxis/census-tip-absent-root.txt`):

```
$ env -i PATH=/usr/bin:/bin LC_ALL=C HOME=<scratch> TMPDIR=<scratch> \
    TSUKUROI_BTRFS_SYSFS=<scratch>/absent-root bash tools/tsukuroi-census.sh </dev/null | grep '^STORAGE '
STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs
$ grep -c btrfs /proc/self/mounts
4
```

The documented row states `HEALTHY 0/0/0` for exactly this input, and the arm prints a `detail` token the
documented grammar does not contain. A reader acting on `SKILL.md` alone is told the hole is still open.

**Second operability harm, same class as the routed §6.6.** The rule change makes the lane's frozen r38 gate red
at tip while its registry row still advertises exit-0 semantics. My run at tip (receipt
`.ufo/waves/round-39/w1/C1CritAxis/r38-counter-at-tip-394e1ba.json`):

```
$ timeout 600 python3 tools/score-storage-arm-r38.py --revision 394e1ba4fab39a417abe66a7802f87cf1ff8dd61 --scratch <scratch>
exit=1
{"fixtures_matched": 9, "live_match": 1, "result": "FAIL", "exit": 1, "revision": "394e1ba4...", "counter": "score-storage-arm-r38"}
FAILED FIXTURE: F06-no-btrfs-root expected ['HEALTHY',0,0,0] got ['BLOCKED',0,0,0]
```

`SKILL.md:3113` still says "0 ten fixtures, the live leg and six PLANE lines per run match;1 any fixture … differs"
and carries no historical note (`grep -n "F06\|historical" SKILL.md` → nothing for this row). The declaration does
predict the failure (`SCORECARD.md:2232`, "Predicted side effect, declared now"), but round-38 closure asked for
exactly this annotation (`corpus/lessons/round-38-verifier-spotcheck.md:183`: "Mark it historical in the registry,
or pin its census input, so no future round cites it at a new revision"), and the lane did write the equivalent
note for the r35b probe (`SKILL.md:3147-3148`). Predicting a red gate in SCORECARD is not annotating the gate row:
a closure that re-runs the gate battery at tip gets `1` from a row that explains nothing.

**Strongest argument against admission.** C1 is declared on operability (`SCORECARD.md:2220`); at its measured
revision and at the current tip the arm's stated outcome is still the pre-change one, so the axis C1 claims is,
in the same window, the axis the round makes false; and the round's own registry now holds a gate returning `1`
at tip under a row whose stated outcome is `0`. AXES.md admits a round only if every claim verifies and no axis
is harmed; this harms the claimed axis (operability) and freshness (a claim made stale without a flag). It is a
fixable textual gap, not a tradeoff that must sink C1 — but it must be closed before the operability verdict is
recorded as improved.

Impacted axes: **operability** (claim's own axis — artifact moved, stated outcome not; plus one new red gate row),
**freshness** (`SKILL.md:3137` and the `detail` grammar stale, unflagged). Coverage and depth are correctly not
claimed.

## 2. Could a do-nothing control reach the target? No.

- `.ufo/waves/round-39/controls/controls.jsonl:1` — `C1-K0-do-nothing`: `hidden_matched 0, views_matched 3,
  fixtures_matched 2, live_match 1, six_planes_all 1`, `result FAIL`, `exit 1`, revision `6a08925d`.
- Independent of the control script, the base before receipt gives the same numbers at `0eff65b2`: hidden 0/2
  (both legs `HEALTHY 0/0/0`), fixtures 2/5 (F1 and F4 match), live 1, six 1, FAIL exit 1
  (`.ufo/waves/round-39/before/c1-before.jsonl`, 3 objects; the counter object carries `hidden_matched`…).
- The near-miss controls fail on the legs the claim is about: K1 fixture-gated → fixtures 5/5 but hidden 0/2
  (`controls.jsonl:2`); K2 over-block → hidden 2/2 but fixtures 4/5 (`:3`, fails F1: absent root with no btrfs
  mount must stay `HEALTHY 0/0/0`); K3 mountinfo-keyed → hidden 2/2, fixtures 2/5 (`:4`). Cheapest hacks the set
  does not name all fail a fixture: "block whenever `fsn==0`" fails F1; "block when the root directory is
  missing" fails F2; "block when the root exists and holds no fsid" fails F2 as well because F2's root is absent.
  5/5 + 2/2 requires both branches (fsid count, then mount table), i.e. the claimed work
  (`tools/score-storage-hidden-r39.py:64-78`).

## 3. Is the predicate one sentence in plan, code and receipt? Yes.

`hidden_matched == 2 and views_matched == 3 and fixtures_matched == 5 and live_match == 1 and six_planes_all == 1`
appears byte-identical in all four places:

- counter docstring `tools/score-storage-hidden-r39.py:28-29`;
- the code's verdict expression `:265-266`;
- the emitted `predicate` field `:268-270`, whose keys are exactly the receipt labels
  (`hidden_matched`, `views_matched`, `fixtures_matched`, `live_match`, `six_planes_all`);
- the declaration's target cell `SCORECARD.md:2220`.

Only an internal variable differs (`six_all` vs the emitted `six_planes_all`). Author after receipt at `49cc53c`
is PASS on all five conjuncts (`.ufo/waves/round-39/after/c1-after-49cc53c.jsonl`: `hidden_matched 2`,
`views_matched 3`, `fixtures_matched 5`, `live_match 1`, `six_planes_all 1`, PASS exit 0).

The claim's third prose clause — "a root with fsid entries never reads the table" — is exercised, not assumed:
views V0-V2 run in the same namespace shape whose mount table lists the host's btrfs mounts (the hidden legs
BLOCK in that shape), and they require no `mounts:` token (`:229`, `:154`). F4 alone would not test it.

## 4. Sizing residuals (non-blocking; record as limits, do not retarget)

- **Seed not replayable.** `seed = os.urandom(16).hex()` (`tools/score-storage-hidden-r39.py:213`) is printed but
  there is no `--seed` flag, so the closure can re-derive the predicate, never the identical view draw. State this
  where "re-derive with one command" is claimed.
- **F3 tests absence, not unreadability.** `F3-absent-root-mounts-unreadable` (`:72`) passes no mounts file, so
  the exercised input is a missing table. `cat … 2>/dev/null` (`tools/tsukuroi-census.sh:1906`) folds
  permission-denied and missing into `mounts:unreadable`, so the branch is shared and the gap is naming only.
- **Host dependence reads as claim failure.** The hidden legs need a btrfs mount in the child table; on a host
  without one the counter exits 1, not 2. Exit 2 exists only for revision, `unshare`/`bash` and no-STORAGE-line
  (`:172-179`, `:210-212`).
- **Receipt format.** The counter prints `indent=1` into `.jsonl`; line-wise readers fail (`json.loads` on line 1
  raises), `jq -c .` works. Cosmetic binding nit for the closure's re-derivation script.

## 5. Smallest safe correction (append-only; no counter, predicate or receipt change)

**(a) `SKILL.md` — append after the round-38 storage section (nothing deleted; the round-38 table stays as the
historical row).** Proposed text:

```
## Storage integrity arm — round 39 (supersedes the round-38 absent-root row)

Appended 2026-10-26 (round-39 C1, `49cc53c7`). The round-38 table above stays as written and its row
`state=HEALTHY filesystems=0 devices=0 nonzero=0` is superseded in part: an absent root, or a root holding no
fsid entry, reads `HEALTHY 0/0/0` **only** when the mount table (`TSUKUROI_PROC_MOUNTS`, default
`/proc/self/mounts`) lists no `btrfs` mount.

- A btrfs mount listed while no fsid entry is readable: `state=BLOCKED filesystems=0 devices=0 nonzero=0
  detail=mounts:btrfs-without-sysfs`. A namespace or mount that hides `/sys/fs/btrfs` is not a clean disk; the
  manual `findmnt -t btrfs` cross-check is no longer required for this case.
- An unreadable mount table: `state=BLOCKED … detail=mounts:unreadable`.
- A root with fsid entries never reads the table; the line keeps its verdict-neutral contract (no `PLANE`, no
  rollup term, no exit-code change).

Add `mounts:btrfs-without-sysfs` and `mounts:unreadable` to the round-38 `detail` token list. Counting:
`python3 tools/score-storage-hidden-r39.py --revision <REV>`. The round-38 counters are historical:
`score-storage-arm-r38.py` reads F06 (`HEALTHY 0/0/0` on an absent root) as BLOCKED from `49cc53c` and exits 1 at
9/10 fixtures by construction.
```

**(b) `SKILL.md:3113` — append to the `storage-arm-r38` row's last cell.** Proposed text:

```
; historical from round 39: valid at revisions <= b0005ae9; from 49cc53c F06 (absent root -> HEALTHY 0/0/0) reads
BLOCKED, so it exits 1 at 9/10 fixtures by construction (round-39 declaration, predicted side effect; run at
394e1ba in .ufo/waves/round-39/w1/C1CritAxis/r38-counter-at-tip-394e1ba.json)
```

Both are text appends. The counter bytes (`75a9e8ab…`) and the predicate stay frozen, so the after receipt at
`49cc53c` stands and nothing is re-scored after seats scored.

## 6. What I did not do

- Did not run `tools/score-storage-hidden-r39.py` end-to-end (other seats hold that leg); I ran the r38 counter at
  tip and the census directly.
- Did not run `bash tools/tsukuroi-census.sh --selftest` (the C1 kill rule's selftest conjunct; seat
  C1ExecSelftest holds it). The author receipt says 117/117 at `49cc53c` — unverified by me.
- Did not port the four round-38 Q82 arms onto `49cc53c` (kill-rule clause; seat C1LeakArms holds it).
- Did not judge C2/TO rows, any other claim, or admission itself.
