# ExecGate — round-81 w1: independent behavioural audit of the round-80 counter repair

Seat: `ExecGate` (leaf executor, round-81 w1). Lane `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`,
base `96ad75b84160da58efaee4997576ce718fd72e2b`, declaration commit
`8023711867eaa788f68af09d7f29d24db749cca7` (pins the round-81 controls and *discloses predeclaration
trials*; it is **not** a compliant pre-data freeze — author trials at 17:15 and the control driver at 18:00
precede/ follow it).

Read-only over the lane tree: no production file was written, no git/jj state was mutated, no `task` call.
Receipts live in `.ufo/waves/round-81/w1/ExecGate/`; scratch was
`${HYAKU_SCRATCH:-/fast/scratch/hyaku}/tsukuroi-r81/ExecGate` and is removed before yield.

Axes named before any measurement:

| axis | question this seat answers |
|---|---|
| **depth** | Does the repair change *behaviour* (not wording), and does the frozen six-case table observe behaviour or only a self-report? |
| **operability** | Can the counter be run at base / HEAD / candidate; do the exit classes hold at the classification boundary; can an operator's digest file weaken a production verdict? |
| **freshness** | Which bytes were frozen when; is the table older than the candidate; is every receipt bound to a SHA-256? |

Scope limit: the seat is the C2 counter repair only. I did not audit the mount-unit/fstab plane, the
provenance headers, or any other seat's payload.

## 1. Exports and identities

| export | bytes from | sha256 |
|---|---|---|
| base counter | `git show 96ad75b8…:tools/measure-round80.py` | `688766756d0fb73ffb8f1d746e3377d58532bd4afa0a3aa92489c61165614d1d` |
| candidate counter | worktree `tools/measure-round80.py`, uncommitted (`M`) | `ca2c8be9c5996b27a7d05278f9845ef667bf8aa85b750fabe836d726f58a6af3` |
| helper | `git show 96ad75b8…:tools/_revision.py` (byte-identical to worktree) | `fc861ec8a4f2539ac3f16d1a04af8335a974c17c8ffba0a41f6dad972cad36de` |
| counter | `tools/measure-round81.py` (committed, unmodified) | `0e94c9b4a9bc0f3ab92ec33005ea2d8743f558ccac26719adcf1765bfd3f5db9` |

Command: `git show 96ad75b84160da58efaee4997576ce718fd72e2b:tools/measure-round80.py > exports/base/measure-round80.py`,
`cp tools/measure-round80.py exports/candidate/measure-round80.py`, then `sha256sum` on all three (output above).
`git status --porcelain tools/measure-round80.py` → ` M tools/measure-round80.py`.

## 2. The frozen six-case table, run by me against both exports

Table: `.ufo/waves/round-81/before/gate-standard-r81.json` (bytes as committed in `80237118`).
Runner: `.ufo/waves/round-81/w1/ExecGate/matrix.txt` records the runner I wrote for this seat
(`runner.py`, sha256 `5257ca3a56150151a4d7aa5dffff8b72654be396c1a88b745ee0403f0e842314`); it materialises a
pristine fixture from the lane, copies the export in, applies each case's mutations, and runs the tool
through its public CLI. It does **not** import `tools/measure-round81.py` — the independence leg.

Per-case `(rc, finding)` matrix (full raw stdout in `matrix.txt`):

| case | table | base rc / finding | candidate rc / finding |
|---|---|---|---|
| A-selftest | rc 0, `SELFTEST total=6 passed=6 failed=0` | 0 / `SELFTEST total=2 passed=2 failed=0` → **FAIL** | 0 / `SELFTEST total=6 passed=6 failed=0` → PASS |
| B-met | rc 0, `"met": true` | 0 / `met` → PASS | 0 / `met` → PASS |
| C-mismatch | rc 1, `matrix-mismatch` | 1 / `matrix-mismatch` → PASS | 1 / `matrix-mismatch` → PASS |
| D-tampered | rc 2, `snapshot_tampered` | **1** / `snapshot_tampered` → **FAIL** | 2 / `snapshot_tampered` → PASS |
| E-absent | rc 2, `snapshot_absent` | **1** / `missing-or-invalid:FileNotFoundError` → **FAIL** | 2 / `snapshot_absent` → PASS |
| F-noargs | rc 2, (no token) | 2 / argparse usage → PASS | 2 / argparse usage → PASS |

**Met: base 3/6, candidate 6/6.** The two exports agree on every C1 verdict except the could-not-evaluate
class; the repair moves exactly D and E from "unmet" (1) to "could-not-evaluate" (2), and rebuilds the
selftest so it drives the public CLI over six isolated fixture trees.

## 3. Hand mutants of a copy of the repaired tool

One clause per mutant, applied to a copy (`exports/candidate` bytes are never modified); mutant bytes and
their SHAs are in `mutants.txt`, `mutants/` under scratch. Kill = at least one of the six cases FAILs.

| mutant | clause | killing case(s) | verdict |
|---|---|---|---|
| a-tampered-exits-1 | `CannotEvaluate(snapshot_tampered)` returns 1 | **D** (rc 1 vs 2), and A (the tool's own selftest re-runs D and prints `passed=5 failed=1`) | KILLED |
| b-absent-exits-1 | `CannotEvaluate(snapshot_absent)` returns 1 | **E** (rc 1 vs 2), and A | KILLED |
| c-selftest-helper-only | `--selftest` checks one helper and prints the conformant token | **none** | **SURVIVED** |
| d-matrix-length-only | `json.loads(data) != expected` → `len(...) != len(...)` | **C** (finding degrades to `review-binding`, token lost), and A | KILLED |
| e-mismatch-promoted-to-met | mismatch returns the 42 cells it was meant to refute | **C** (rc 0 observed), and A | KILLED |
| f-noargs-accepted | bare invocation returns 0 instead of refusing | **F** (rc 0 observed) | KILLED |

**Tally: 5 killed, 1 survived.** Four of the five kills are double kills (the case, plus the repaired
tool's own selftest, which now re-runs the same table internally) — that is real added depth from the repair.

## 4. Counter runs (`counters.txt`)

| command | rc | observed |
|---|---|---|
| `python3 tools/measure-round81.py --selftest` | 0 | `SELFTEST total=2 passed=2 failed=0` |
| `… --revision 96ad75b8…` (no `--table`) | 2 | `cannot-evaluate:CalledProcessError` — the table does not exist at that revision |
| `… --revision 96ad75b8… --table <frozen table>` | 1 | `count: 3, target: 6, finding: "gate-standard"` |
| `… --revision e8e5d5b3…` (HEAD, pre-repair tool) | 1 | `count: 3, target: 6, finding: "gate-standard"` |
| `… --fixture <tree holding the candidate bytes>` | 0 | `count: 6, finding: "met"` |
| `… --fixture <tree holding mutant c>` | 0 | `count: 6, finding: "met"` — the survivor is scored conformant |

The counter's verdict on the base revision (3/6) and on the candidate (6/6) matches my independent runner
exactly. The counter cannot see the survivor: mutant c is scored `met`.

## 5. Boundary probes (`boundary.txt`)

The frozen table exercises two could-not-evaluate inputs (`expected.json` tampered, `systemd.service.xml`
absent) and never touches the rest of the boundary the repair rewrote. Probes on a fixture that can reach
C2 (SKILL.md, both tools, both receipts copied in):

| probe | base | candidate |
|---|---|---|
| C1, note JSON removed | rc 1 `missing-or-invalid:FileNotFoundError` | rc 1 `note-absent` |
| C1, `ReviewMatrix/verdict.json` removed | rc 1 `missing-or-invalid:FileNotFoundError` | **rc 2 `review_absent`** |
| C2, one receipt removed | rc 1 `missing-or-invalid:FileNotFoundError` | **rc 2 `receipt_absent`** |
| C2 control, everything present | rc 1 `count: 1 gate-standard` | rc 1 `count: 1 gate-standard` |

Revision-mode probe in a scratch clone with the candidate installed: `--claim C1 --revision e8e5d5b3…`
returns `count: 42, finding: "met"`, rc 0 **both with and without** a nonexistent `--digests`, so the digest
override never reaches the revision path.

## 6. Findings

**F1 — the repair is real and independently reproduced (depth).** [observation] base 3/6, candidate 6/6 on
my own runner; D and E both move to rc 2 with their own finding ids; the counter agrees (3/6 vs 6/6).
[inference] the routed round-80 defect ("a pinned input absent or edited is not a verdict") is closed for
the two inputs the table names.

**F2 — the table's only C2-observing case is a self-report (depth, routed).** [observation] mutant c keeps
rc 0 and prints `SELFTEST total=6 passed=6 failed=0` while doing no fixture work; the frozen table scores it
6/6 and `tools/measure-round81.py` reports `count: 6, finding: "met"` against it. [observation] both my
runner and the counter decide a case by `rc == spec['rc'] and spec['token'] in body`.
[inference] case A cannot distinguish "the selftest drives the public CLI over six fixture trees" — the
candidate's actual behaviour — from a token printer; the claim's one behavioural leg is audited by string
equality on a string the tool itself emits. The counter's own selftest shares the blind spot (its
`defective-double` mutant changes the token, not the work). Suggested closure for the next round: assert the
selftest's *fixture-tree side effects*, or require `--selftest` to exit non-zero when one of the six trees is
re-broken (e.g. inject the mutation through an env-var or a fixture hook), rather than matching its output.

**F3 — the could-not-evaluate boundary contradicts the tool's own rule (depth, routed).** [observation]
`note-absent` → rc 1, `review_absent` → rc 2, `receipt_absent` → rc 2 (boundary.txt). [observation] the
candidate's docstring states the rule: "the claim's own artifact missing is unmet, the evidence the claim
rests on being absent or edited is not a verdict at all". C1 is *"42 pinned restart cells with a digest-bound
review file"* and C2 is *"two named tools … carry byte-bound execution receipts"* — the review file and the
receipts are the claim's own artifacts, exactly like the note. [inference] the repair fixes the tampered→1
error and introduces its mirror: a *missing* review file or receipt now reads as an abstention instead of a
failing claim, so a claim can be downgraded from unmet to could-not-evaluate by deleting its own evidence.
No case in the frozen table covers this, so the gate cannot see it. This is the defect I would route to
round 82.

**F4 — `R80-C2-REGISTRY-NAME` is still live and unchanged (operability, routed).** [observation]
`grep -c '^| check-transaction-order-r39 ' SKILL.md` → `0` (rc 1); `grep -c '^| transaction-order-r39 '`
→ `14` (rc 0); the counter keys the row on `name[:-3]` (`measure-round80.py:92`), which the candidate did not
touch. [observation] C2 on the real lane returns `count: 1, target: 2, finding: "gate-standard"`, rc 1 for
**both** exports. [inference] the repair changes the exit map but not the registry-name leg, so round-80 C2
stays unmet after it; the repair must not be read as "C2 now passes".

**F5 — freeze ordering (freshness).** [observation] the table's bytes are in commit `80237118`
(2026-11-04 17:50:37) and `git status` shows the path clean; its worktree mtime is 17:57:16, *later* than the
candidate's file mtime 17:56:23, so an mtime-only ordering is inconclusive. [observation] the round-80 static
findings are dated 17:15 and `before/controls.json` / `run-controls.py` are 18:00 — after the table.
[inference] in commit-content order the table predates the candidate repair, but the same author wrote both
and the declaration commit discloses that trials preceded it; the table is therefore not independent
evidence on its own. My runner is the independent leg: it reproduces 3/6 → 6/6 without importing the counter.

**F6 — `--digests` cannot weaken a production verdict (operability).** [observation] revision-mode runs with
and without a nonexistent `--digests` are byte-identical (`count: 42, met`). [inference] the override is
inert outside `--fixture`; fixture-mode re-pinning is by design (the selftest needs it), but a reader must not
cite a `--fixture --digests` run as tamper evidence.

**F7 — measuring the base revision needs `--table` (operability).** [observation] `--revision 96ad75b8…`
without `--table` returns rc 2 `cannot-evaluate:CalledProcessError` because `gate-standard-r81.json` does not
exist at that revision; with `--table` it returns the honest `count: 3`. [inference] the counter's base
measurement is only meaningful with the frozen table passed explicitly — worth stating in the receipt that
cites it.

## 7. Risks, limits, scratch

- **Blockers:** none. The seat is read-only by design, so F2/F3/F4 are routed as findings, not fixed.
- **Limit:** fixture-mode verdicts depend on the fixture tree having SKILL.md, both C2 tools and both
  receipts; a tree missing them returns `cannot-evaluate:FileNotFoundError` at rc 2, which is correct
  behaviour but must not be mistaken for a claim verdict.
- **Limit:** case A's token is also satisfied by the base export's wording if the count were changed; the
  token encodes the number of internal cases, so any future change to the selftest's case count silently
  breaks the table.
- **Tooling:** nothing installed or upgraded; no pacman transaction was attempted (host-wide pause
  respected). `python3` was the system interpreter already on PATH.
- **Scratch:** `/fast/scratch/hyaku/tsukuroi-r81/ExecGate` (635 MB incl. a `--no-hardlinks` clone) is removed
  before yield; the scratch paths quoted inside the receipts are provenance only.
- **Lane state:** `git status --porcelain` after my work shows only the pre-existing entries
  (`corpus/SOURCES.md`, two knowledge notes, `tools/measure-round80.py`, the wave's own untracked files) plus
  my untracked `w1/ExecGate/` receipts. No production file was written by this seat.

## Receipts (sha256)

| file | sha256 |
|---|---|
| `.ufo/waves/round-81/w1/ExecGate/matrix.txt` | `f116c1be242af21c8bd70114c7d9b0401451eb60a42246546a49e2ed40902070` |
| `.ufo/waves/round-81/w1/ExecGate/mutants.txt` | `fa9dcc99712620915625e95386cb73fa221dbfe819d2e8ffa3efde3d07a110f8` |
| `.ufo/waves/round-81/w1/ExecGate/counters.txt` | `c6fd06079da5ea5361b32e966ea036a78f515fcedc784df65bbc2333a17d13b8` |
| `.ufo/waves/round-81/w1/ExecGate/boundary.txt` | `8f42e4ac7258dae556acd4337608b83a1e175d32bc2d19856d9a4bfbe9e5aa02` |
