VERDICT: defect-found

# G-2 — C1/C2 causal separability and six-axis no-harm (CritSeparability, round 42 w1)

**Separability holds.** The two frozen counters read disjoint file sets, and a fixture tree that
carries the freeze plus the C2 entry but the *base* census still satisfies every non-verdict C2
conjunct (`rows 5, quotes_ok 5, novelty_ok 5, host_ok 5, sources_ok 1, novelty_base_hits 0`).
**No-harm fails at two shared round-level gates**, both repairable by the L1 without touching
either claim's counter:

- **adjacency** — `tools/check-adjacency-anchors.py` PASSes at the base and FAILs at the tip on
  IN-109 (`found_line 2452`, quote now at `2465`); the shift is caused by C1's census edit.
- **calibration** — `tools/check-self-assessment.py` gains K07 (62→63 notes, C2's commit) and
  K13/K17 (128→130 selftest cases, C1's commit); `tools/check-registry-coverage.py` FAILs on the
  two new counters added by the freeze commit (66 tools, 64 rows).

Base `c8efaa3f120834541f8de1e5e0367e8d1593bae6`; freeze `a84fc9dec860f8bea516dff7ddfdc98223cdae52`;
C1 `447662088dfd3155e31aed239179a79c1d1046c7`; C2 `f50c28d83e1832ecd7eba765caace531f45d6b27`;
tip at review `87c4f7c627e377e5f6d361498e8db9b3886d7953`.

## 1. Separability

### 1.1 What each counter reads

| Counter (frozen sha256) | Paths read | Source lines |
|---|---|---|
| C1 `tools/score-size-invariance-r42.py` (`c51110…`) | `<REV>:tools/tsukuroi-census.sh` and `<BASE>:tools/tsukuroi-census.sh`; generated fixtures and `--scratch`/`$TMPDIR` work dirs | `:59` BASE, `:60` CENSUS, `:307-308` the only two `git_show` calls, `:303` `mkdtemp(dir=parent)`, `:66` `_cleanup` |
| C2 `tools/check-scrub-record-r42.py` (`dbe933…`) | `<REV>:corpus/knowledge/btrfs-scrub-record-r42.md`; `<REV>:.ufo/waves/round-42/frozen/src/{scrub.c,CHANGES}` (digest-checked); `<REV>:.ufo/waves/round-42/frozen/hostcap/capture.txt` (digest-checked); `<REV>` and `<BASE>:corpus/SOURCES.md`; `git grep -c -F <row token> BASE -- corpus/knowledge SKILL.md`; `<REV>:.ufo/waves/round-42/{w2,residual}-{dispatch,results}.json` and `…/{w2,residual}/<seat>.md`; host-local `~/.omp/agent/sessions/…/<seat>[-<k>].jsonl` | `:46` ENTRY, `:49-55` SNAP/CAPTURE, `:162` frozen, `:164` capture, `:169-170` BASE grep, `:173` entry, `:176-177` SOURCES, `:119-136` bound(), `:139-146` transcripts |

Negative greps (both run, output empty / only a docstring):

- `grep -nE "\.ufo|corpus|SKILL|SCORECARD|w2-" tools/score-size-invariance-r42.py` → no output:
  the C1 counter never reads a corpus, SCORECARD, SKILL or wave file.
- `grep -nE "tools/|census" tools/check-scrub-record-r42.py` → only `:33` (its own usage
  docstring): the C2 counter never reads the census or any tool.
- The census itself has no runtime read of repo prose: its only `SKILL.md` occurrences are note
  strings it prints (`tools/tsukuroi-census.sh:665,1571,1815`), and no `source`/`cat` of a repo
  file exists.

### 1.2 Does either counter's input change with the other's commit?

No. The commit path sets are disjoint from the other counter's read set:

- C1 commit `4476620` touches `.ufo/waves/round-42/before/{c1-before.jsonl,c2-before.jsonl,sources-census-at-freeze-a84fc9de.txt,sources-census-start.txt}`,
  `.ufo/waves/round-42/impl/c1-able-to-fail.txt`, `tools/tsukuroi-census.sh`. The C2 read set
  contains none of these. (The C1 commit also lands the *C2 before-receipt*; that receipt is not
  read by the C2 predicate, so it is a provenance curiosity, not a coupling.)
- C2 commit `f50c28d8` touches only `corpus/SOURCES.md` and
  `corpus/knowledge/btrfs-scrub-record-r42.md`. The C1 read set (the census at two revisions)
  contains neither.
- Census blob identity (the C1 counter's whole input): `dda066f4` at base; `ed83079c` at
  `4476620`, at `f50c28d8`, and at the tip. C1's counter therefore appraises byte-identical
  census inputs at the C1-only revision and at the tip.
- C2 blobs at `f50c28d8` and at the tip are identical: entry `e0afccd4`, SOURCES `643f9314`.

Shared provenance is only the freeze commit, which lands both counters' frozen code and C2's
snapshots; that is infrastructure, not a claim input. C1's kill rule and C2's kill rule
(`SCORECARD.md` "Round 42 — declaration") therefore cannot fire each other.

### 1.3 Empirical crossing test — C2 without C1

Fixture clone of the lane at the freeze `a84fc9de` + only the two C2 blobs from `f50c28d8`,
committed with fixture identity (`git rev-parse --show-toplevel` asserted first); fixture rev
`8e161dd7b0434a368b4edd02924e97b66fb20cea`, census blob `dda066f4` (the base, unfixed census).
Frozen C2 counter, `--lane <fixture> --revision 8e161dd7`:

```
rows 5, quotes_ok 5, novelty_ok 5, host_ok 5, sources_ok 1, novelty_base_hits 0,
verdicts_ok 0, verdict FAIL
```

Every non-verdict conjunct holds with **no C1 commit in the tree**; the FAIL is only
`verdicts_ok`, whose input is the wave-2 orchestrator records (`C2RevSC<n>` / `C2CritSC<n>`),
not C1. Receipt: `w1/CritSeparability/c2-only-from-freeze.jsonl`.

Controls on the same method:

- Same tree built on the base instead of the freeze (no snapshots) → `quotes_ok 0, host_ok 0`
  (`c2-only-tree.jsonl`, exit 1): C2 depends on the *freeze*, not on C1.
- Frozen C2 counter at the tip `87c4f7c6` → the same five lexical values, `verdicts_ok 0`
  (`c2-counter-at-tip.jsonl`).

### 1.4 What I did not run

I did not run `tools/score-size-invariance-r42.py` (C1-1's executor `C1ExecRerun` owns it; host
guard allows one heavy counter at a time). The C1 side is argued from the two `git_show` calls
(`:307-308`), the absence of any other tracked read, and the census blob identity in §1.2.
I also did not run the C1 kill-rule counter `score-selftest-mounts-r41.py`
(executor `C1ExecPriorCounters` owns it).

## 2. Six axes — can round 42 so far harm each?

| Axis | Verdict | Evidence |
|---|---|---|
| depth | **no harm measured** | `git diff --name-status c8efaa3f 87c4f7c6 -- corpus/knowledge` → `A corpus/knowledge/btrfs-scrub-record-r42.md` only (no M, no D). `check-knowledge-header` PASS at tip (63 notes, 63 complete, 0 findings; 62/62 at base). C2 counter at tip: `quotes_ok 5, host_ok 5, novelty_base_hits 0`. Claim truth is wave-2's subject, not a local defect. |
| coverage | **no harm** | Six `printf 'PLANE` emitters at base and at tip (6/6); `PROVINCE.md` absent from the whole diff; the census hunks are confined to `probe_packages` (`:692-697`), `probe_update_safety` (`:1624-1655`) and `run_selftest` (`:2350-`, `:2556-`), so no plane or arm was removed. |
| operability | **census behaviour holds; registry surface harmed** | Census selftest at the tip prints `PASS (130 cases, 130 passed, 0 failed)` (observed by `check-self-assessment` K13 at `87c4f7c6`). But `check-registry-coverage`: PASS at base (64 registered / 64 tools) → FAIL at tip: `REGISTRY-ROW-MISSING` for `tools/check-scrub-record-r42.py` and `tools/score-size-invariance-r42.py` (66 tools, 64 rows). Receipts `registry-coverage-c8efaa3f.json`, `registry-coverage-87c4f7c6.json`. Kill-rule counter not run by me (see §1.4). |
| freshness | **no harm observed** | Entry `verified-at: 2026-10-26` and host facts match live: `btrfs-progs v7.1`, `uname -r 7.2.11-arch1-1`; the entry's stated host build `7.1-1` matches the pinned v7.1 sources; counter `capture_ok true` at tip (capture.txt sha256 matches the pin). SC5's `6.6.3` rows are "arrived in" history, not host claims. I did not re-run `capture.sh`. |
| calibration | **harmed at the tip; needs a measured-outcome restatement** | `check-self-assessment`: base FAIL with **K10 only** (states 58 lesson files, holds 59 — pre-existing, not round 42); tip FAIL with **K07** (states 62 notes, holds 63 — C2's note), **K13** (operability row states 128 cases, holds 130 — C1's two cases), **K17** (host-census-gate row 128 vs 130), K10 unchanged. K08/K09/K11 still match (SKILL 3847 lines / 956 table lines, README 404). Receipts `self-assessment-*.json`. |
| adjacency | **harmed; cause isolated to C1** | `check-adjacency-anchors`: PASS at base (114/114 classified, exit 0); FAIL at `4476620` and at tip: `INBOUND-CLASSIFICATION-WRONG` at `corpus/knowledge/adjacency-anchors-r19.json:inbound[108]` (IN-109). The quote `check 'degraded: kernel ring class counts are evidence (D14/D15)' 1 DEGRADED` is at `2452` at base and `2465` at tip (+13 = the +3 comment lines inserted at 692 and the +10 lines of the first new selftest case at 2350). Receipts `adjacency-anchors-*.json`. |

Adjacency note on siblings: a read-only grep of every sibling lane's durable surfaces
(`corpus/`, `tools/`, `SKILL.md`, `PROVINCE.md`) finds **no** pin of `tsukuroi-census.sh:6` or
`:16`, and those two lines are byte-identical at base and tip. The sibling pins that do exist
(tameshi `fleet-kill-rate-ledger.md:71` `:915-920`, `service-optin-protocol.md:153` `:915-970`,
`mutation-case-tsukuroi-census.md:356-370` `:473/:281/:434-452/:578/:615/:210/:160/:935/:967/:487-493`)
are revision-pinned history (`aae45531`, `165307fe`, `dc3436d`) and do not claim the tip; the
only live cross-lane record is IN-109. Report, do not absorb: no sibling file was read-writable
in this review.

## 3. Smallest safe corrections for the L1 (not applied; lane is read-only to me)

1. **Adjacency.** In the same commit that lands the census change, set IN-109 `found_line` to
   `2465` and extend its `note` ("round 42: the C1 census comment and two selftest cases moved
   the case 2452→2465"). Validated in a scratch clone: the gate then PASSes with
   `inbound_classified 114/114` and no findings (`adjacency-fixed-in109.txt`). Note that
   `SKILL.md:600`'s `915-970` pin was already stale before this round (IN-109's own note records
   that the range held probe_drivers kernel-ring code at round 19, not the block it names); the
   round-42 shift only moves that already-stale range to `918-973`, so a notice, not an edit, is
   the proportionate response. Do not edit tameshi.
2. **Calibration counts.** The measured-outcome axes table at the final revision must state
   `63` notes and `130` selftest cases (both the operability row and the `host-census-gate`
   capability row), and `59` lesson files to clear the pre-existing K10. K08/K09/K11 need no
   change.
3. **Registry.** Add the two SKILL.md registry rows for `tools/check-scrub-record-r42.py` and
   `tools/score-size-invariance-r42.py` (round-27 precedent: an unregistered new counter is a
   gate FAIL, not a style nit).

## 4. Receipts

All under `.ufo/waves/round-42/w1/CritSeparability/`:

- `counter-read-sets.txt` — source-line extraction of both counters' reads.
- `c2-only-from-freeze.jsonl` — C2 at freeze+entry, census = base, rev `8e161dd7`.
- `c2-only-tree.jsonl` — same method on the base (no snapshots), rev `8ba6052c`.
- `c2-counter-at-tip.jsonl` — frozen C2 counter at `87c4f7c6`.
- `adjacency-anchors-{c8efaa3f,44766208,87c4f7c6}.json` — gate outputs (PASS, FAIL, FAIL).
- `adjacency-fixed-in109.txt` — fixture clone with `found_line 2465`; gate PASS.
- `registry-coverage-{c8efaa3f,87c4f7c6}.json` — PASS 64/64 vs FAIL 66/64.
- `self-assessment-{c8efaa3f,87c4f7c6}.json` — K10 only vs K07/K10/K13/K17.
- `check-{adjacency-overlap,knowledge-header,appended-notices,section-citations}-{c8efaa3f,87c4f7c6}.txt`
  — all PASS at both revisions (the adjacency-overlap rows and the C2 note's headers/append-only
  notices are clean).

## 5. Compliance

- No tracked lane file was written except this report and the receipts above; no git/jj mutation
  in the lane or any fixture outside my scratch; every fixture asserted
  `rev-parse --show-toplevel` before its first commit and used the fixture identity.
- No package/tool install or upgrade; no host mutation, no sudo, no scrub/device-stats command;
  no service restart. Sibling lanes and shokuknow were read-only.
- Scratch `/fast/scratch/hyaku/tsukuroi-r42/CritSeparability/` (clone fixtures at the base, at
  the freeze+C2, and at the tip; gate TMPDIRs) was removed after the receipts were copied.
