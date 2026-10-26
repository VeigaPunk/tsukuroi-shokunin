VERDICT: defect-found

Seat C1CritAxis, item C1-13 (round 41 / hyaku run 9), milestone "axis and surface honesty". Read-only on lane
content. Scratch `/fast/scratch/hyaku/tsukuroi-r41/C1CritAxis/` (removed after the receipts were copied).
Bytes under test: `git show 0e5805a1f149bd2ed9fe0db2e0a832afb034a835:tools/tsukuroi-census.sh` (base, 3149 lines)
and `git show 568c397da11339aed65181be598414f268835555:tools/tsukuroi-census.sh` (after, 3176 lines);
`git diff --stat 568c397d 71851d63 -- tools/tsukuroi-census.sh` is empty, so the after bytes are the lane tip's.
Counter `tools/score-selftest-mounts-r41.py` sha256 `8306d9990b156ceb625eabbe942910fc0d09b20f350a7e8af1ff2237fd07355c`,
matching the declaration (`SCORECARD.md:2465`). Receipts: `.ufo/waves/round-41/w1/C1CritAxis/{host-shapes.txt,
spotcheck-variants.txt,live-diff.txt,base-fixture-shapes.txt,receipts-and-controls.txt}`.

Findings are about the **framing**, not the numbers: the claim's surface statement is honest and I reproduced two
of its four survivors and two of its kills outside the counter. The defect is the axis label, the unstated
entailment behind `params == 4`, and the stale operability evidence cell.

## 1. Counterexample to the operability framing: the artifact does not change at all

| Observation | Command / source | Result |
|---|---|---|
| arm body identical | `probe_storage_arm()` extracted from both blobs, sha256 | `71e6007e566e1af3` in base and after (61 lines both); totals 3149 → 3176 lines |
| commit shape | `git show 568c397d --stat` | `tools/tsukuroi-census.sh | 27 +++++++++++++++++++++++++++` (27 insertions, 0 deletions), all inside `run_selftest` at `tools/tsukuroi-census.sh:3037-3062` |
| live output identical | `bash base.sh` and `bash after.sh` back to back on this host | STORAGE line byte-identical: `STORAGE btrfs-device-stats state=HEALTHY filesystems=1 devices=1 nonzero=0`; the only differing tokens in the six PLANE lines are live counters (`C5_pswp`, `C6_psi_full_total_us`, `C6_avail_kb`) — `live-diff.txt` |
| stated outcome identical | `bash <blob> --selftest` | base `PASS (124 cases, 124 passed, 0 failed)` rc=0; after `PASS (128 cases, 128 passed, 0 failed)` rc=0 |

`AXES.md:13` defines operability as "Runnable artifacts: checklists that are executable, commands that exist,
scripts that run", signal "A checklist item can be run and produces the stated outcome". The **base already met
both**: it ran, exited 0, printed PASS over 124 cases, and killed nine frozen mutants (base receipt
`.ufo/waves/round-41/before/c1-before.jsonl`: `survivors 4` of 13, i.e. M1–M9 all killed). After C1 the selftest
still runs, still exits 0, still prints PASS — over four more cases. No runnable artifact gained an outcome it did
not produce before, and the declaration says so itself ("`probe_storage_arm` is NOT changed", `SCORECARD.md:2465`).

What actually improved is *which hypothetical future arms the suite refuses* — a property of the verification
instrument, i.e. depth content in `AXES.md`'s own vocabulary ("Verifiable technical detail — decision tables with
real thresholds"), delivered through the operability instrument. So: **C1 is verification-depth work whose kill
count is measured with the operability evidence cell.** The label survives only because the lane's operability
counting command is the selftest case count (`SCORECARD.md:2431`), a proxy that any authored case/mutant pair can
advance forever with zero operator-visible change — the premature-saturation pattern, not an operability gain.

Two things keep this from being a mislabel pure and simple, and they belong in the record:

1. Lane precedent is explicit and already qualified: round 40's critic reached "axis fit = operability" while
   recording "the artifact's own output does not change" and "the before number is a ceiling" (`.ufo/waves/round-40/w1/C1CritAxis.md`
   §2–3). C1 repeats that move by one increment; the qualification is what is missing, not the precedent.
2. The mutants are not all author-chosen for the cases: H5, H6 and H9 come from an independent round-40 seat
   (`.ufo/waves/round-40/w1/C1HeldOutMutants.md`), and the landed cases follow that seat's prescribed bash
   almost verbatim (`storage-mounts-mp-relative`, `storage-mounts-src-uuid`, the same `UUID=` table line, the same
   expected regex). Only H10 is authored this round. The closed-loop worry is therefore mild; the value question
   below still stands.

Consequence at the revision C1 lands: `SCORECARD.md:2431` still reads
"`bash tools/tsukuroi-census.sh --selftest` prints PASS (124 cases, 124 passed, 0 failed)" while the selftest at
the lane tip prints **128** (after receipt `"last": "TSUKUROI_CENSUS_SELFTEST: PASS (128 cases, ...)"`). The
operability row's own counting command does not reproduce at the revision the operability claim lands on —
`QUALITY 57` red, and `tools/check-self-assessment.py:656-663` (K13) checks exactly this.

## 2. Is the before (survivors 4) reachable only by a do-nothing control? Yes — and it is forced

The before **is** the do-nothing control: the declaration says "K0 do-nothing is the before receipt itself
(`before/c1-before.jsonl`)" and that receipt binds `revision 0e5805a1…`, `survivors 4` (H5, H6, H9, H10),
`params 0`, FAIL. Nothing else is needed to reach the number, and I reproduced half of it without the counter:

| variant | run | observed |
|---|---|---|
| base + H9 (`subvol=` whole-table key) | `bash base-H9.sh --selftest` | rc 0, `PASS (124 cases, 124 passed, 0 failed)` → survivor |
| base + H10 (`$mt -eq 1`) | `bash base-H10.sh --selftest` | rc 0, `PASS (124 cases, 124 passed, 0 failed)` → survivor |
| after + H9 | `bash after-H9.sh --selftest` | rc 1, `FAIL (128 cases, 127 passed, 1 failed)`, label `… no subvol= option still counts, BLOCKED (R41-C1 H9)` |
| after + H10 | `bash after-H10.sh --selftest` | rc 1, `FAIL (128 cases, 127 passed, 1 failed)`, label `… two btrfs lines are still btrfs without sysfs, BLOCKED (R41-C1 H10)` |

(`spotcheck-variants.txt`; each replacement text occurs exactly once in both blobs.) The number is real. It is
also **uninformative**, for two independent reasons:

- **Survival is entailed by the base fixtures.** Every base must-block table carries a btrfs line with absolute
  mountpoint, `/dev/*` source, a `subvol=` key, and exactly one btrfs line per table: base
  `tools/tsukuroi-census.sh:2978` (`/dev/mapper/root / btrfs …subvol=/@`), `:3013` (`/dev/nvme0n1p3 /home btrfs
  …subvol=/`), `:3021` (`/dev/sda2 /var/lib/machines btrfs ro,…subvol=/machines`), `:3039` (`/dev/vdb /data btrfs
  …subvol=/`). A mutant keyed on any of those four shapes *cannot* be killed by that fixture set, so the four
  survivors are dictated by fixture design, not discovered by a probe.
- **`params == 0` at base is unsatisfiable by construction.** The base has no P1–P4 fixture at all, so the
  parameter conjunct can never hold at base. Two of the three FAIL conjuncts (`params`, and `survivors` via
  `:2978/:3013/:3021/:3039`) are definitional; only `decoy_pass 1` carries fresh information. The before
  certifies a hole in the suite; it does not show a malfunction, and the identical arm sha (§1) proves there was
  none.

Disclose one ordering fact: the before receipt's window is `2026-10-26T17:56:30Z–18:02:14Z`, **39 minutes after**
the after receipt (`17:17:35Z–17:23:56Z`, `receipts-and-controls.txt`). It re-derives base bytes from git (its
`revision` field is `0e5805a1…`, the census is read with `git show <rev>:` at
`tools/score-selftest-mounts-r41.py:212-213`), so the measurement is sound; but it is not a pre-implementation
capture, and "pre-data" is true only in the sense "before any wave seat".

## 3. H5 / H6: spec pinning or operability value? Two of the four shapes are live, one is a seam, one is a pin

Host evidence (`host-shapes.txt`): `awk '$3=="btrfs"' /proc/self/mounts | wc -l` → **4**; the four lines are
`/dev/mapper/root` at `/`, `/home`, `/var/cache/pacman/pkg`, `/var/log`, each with `subvolid=` and `subvol=`;
`awk '{print $2}' /proc/self/mounts | grep -vc '^/'` → **0** of 33 mountpoints non-absolute.

| shape | class | ground |
|---|---|---|
| H9 — btrfs line with no `subvol=` | **live** | btrfs(5) `subvol=<path>`: "This mount option overrides the default subvolume set for the given filesystem" (rendered lines 494-498) — without it the default subvolume is mounted, an ordinary mount. Real operator value: a subvol-less btrfs mount behind a hidden sysfs must not read `HEALTHY 0/0/0`. |
| H10 — two or more btrfs lines, counted with `-eq 1` | **live, highest value** | this host has 4 btrfs lines today (`host-shapes.txt`), so `-eq 1` would print `HEALTHY 0/0/0` here and now; that is the round-39 defect class in the opposite direction (`tools/tsukuroi-census.sh:359-366` requires BLOCKED). |
| H6 — source not under `/dev` (`UUID=…`) | **seam contract, not a host shape** | mount(8) on tags: "The recommended setup is to use tags (e.g. `UUID=uuid`) … The mount(8) command internally uses udev symlinks" (rendered lines 120-124) — a tag is resolved to a device path before `mount(2)`, so `/proc/self/mounts` shows `/dev/*`. The case only bites through the documented override `TSUKUROI_PROC_MOUNTS` (`tools/tsukuroi-census.sh:408`, `:463`), i.e. a user-supplied table. Mitigating: round 40's own fixture already wrote `UUID=0b1c /boot vfat` (base `:3020`), so the shape is in the lane's fixture vocabulary. |
| H5 — relative mountpoint | **spec pin, no operator outcome** | a table's second field *is* the mount point (fstab(5) lines 68-71: "This field describes the mount point (target) for the filesystem"); [INFERENCE] the kernel renders it from the namespace's mount tree, so a relative mountpoint cannot appear in `/proc/self/mounts` — observed 0/33. The case pins that the reader counts on field 3 alone for an input the documented default source cannot produce. |

Verdict on this sub-question: the kill count treats all four shapes as equal (`params 4`); two are operator
outcomes (H9, H10), one is a public-seam contract (H6), one is spec pinning (H5). Harmless to keep — none of the
four can be *wrong* — but the claim's "four mount-table cases" reads as four equal operability gains, and only
H9/H10 are. That distinction is the honest form of the row.

## 4. QUALITY 88: held in letter, and its isolating control is absent; the parameter conjunct is entailed here

`corpus/QUALITY.md:173` (criterion 88) requires (a) the frozen predicate to check the declaration's named content
parameters themselves "never only over the counter's own constants derived from them", and (b) a pre-data control
"that satisfies every other frozen check while violating exactly one named parameter, which must fail".

- **(a) satisfied.** The declaration names four table shapes; the counter derives P1–P4 from the *captured*
  fixture tables, not from constants: `params_from_capture` (`tools/score-selftest-mounts-r41.py:173-187`) reads
  every `*.mounts` file copied at `check()` time by the injected `CAPTURE_LINE`, keeps only labels the baseline
  printed as PASS whose arguments contain `detail=mounts:btrfs-without-sysfs`, and classifies with
  `mount_props` (`:162-171`). Predicate includes `params == 4`; base reads `params 0` with all four lists empty
  (`before/c1-before.jsonl`). This is exactly the class the round-40 failing example named (a candidate keeping
  four of five declared fixtures, `corpus/QUALITY.md:173`).
- **(b) not satisfied as written.** The control `C1-K2-candidate-without-H9-case` violates the parameter **and**
  a second conjunct: `controls/C1-K2-candidate-without-H9-case.jsonl` reads `survivors 1, params 3, FAIL`. No
  control shows the parameter check alone rejecting an otherwise-passing candidate.
- **And it cannot be independent for this mutant set.** Each new mutant is killed by exactly one purpose-built
  label and by no other: after receipt (`after/c1-after-568c397.jsonl`) gives H5 → only the H5 label, H6 → only H6,
  H9 → only H9, H10 → only H10; my own after-H9/after-H10 runs each fail exactly one label (§2). Killing H9
  requires a P3 table, H5 a P1 table, H6 a P2 table, H10 a P4 table, so `survivors == 0` entails `params == 4`.
  The parameter conjunct is a restatement of the kill result, not a second measurement of the declared content.

Smallest constructible isolating control (feasible with the frozen counter, no counter change): take the
candidate and narrow only the H9 case's expected regex from
`^STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs$`
to `^STORAGE btrfs-device-stats state=BLOCKED ` — H9 still fails that case (it prints `state=HEALTHY`), so
`survivors 0`, while the fixture no longer counts as P3 (no `detail=mounts:btrfs-without-sysfs` in the check's
arguments) → expected `survivors 0, params 3, FAIL`. That is the "every other frozen check satisfied, exactly one
parameter violated" variant 88 asks for.

## 5. Impacted axes and harm

| axis | impact |
|---|---|
| operability | label rests on the case-count proxy; the row's own count is stale (124 stated at `SCORECARD.md:2431` vs 128 printed). No operator-visible gain; no operator-visible harm. |
| depth | the real content: four reader shapes pinned, two of them live (H9, H10). Unharmed; under-credited. |
| calibration | three wording gaps: "four cases" reads as four equal operability gains; the forced before is presented as a plain FAIL; the before receipt postdates the after receipt. |
| freshness / coverage / adjacency | no effect. |
| host / lane | no host mutation, no lane write; live run creates no files; scratch removed. |

Nothing here falsifies the claim's arithmetic: `baseline_pass 1, neutral_pass 3, decoy_pass 1, mutants_applied 13,
survivors 0, params 4` is real and the kills are behavioural (my independent after-H9/H10 runs fail the intended
labels). Relabelling C1 as depth is **not** an available correction — `AXES.md:32` makes two claims on one axis in
one round count as one claim, and C2 already holds depth — so the correction has to be a qualification in the
row, not a relabel.

## 6. Exact proposed text (smallest safe correction)

1. `SCORECARD.md:2465`, Axis cell — replace `operability` with:

   `operability (instrument sensitivity: the runnable selftest's case set 124→128; `probe_storage_arm` is
   byte-identical (sha256 `71e6007e566e1af3`) and every live output is unchanged, so the gain is which future
   arms the suite refuses, not a new host outcome)`

2. Append to the same row (or the C1 receipt note):

   `Of the four declared shapes, H9 (no subvol= option — btrfs(5) "overrides the default subvolume set for the
   given filesystem") and H10 (>=2 btrfs lines — this host has 4) are live-host shapes; H6 (UUID= source) is a
   contract on the documented TSUKUROI_PROC_MOUNTS seam, since mount(8) resolves tags to /dev paths before
   mount(2); H5 (relative mountpoint) is spec pinning — 0 of 33 mountpoints in /proc/self/mounts here is
   non-absolute. Params==4 is entailed by survivors==0 for this mutant set (each new mutant is killed by exactly
   one purpose-built label, after/c1-after-568c397.jsonl), and control K2 violates params and survivors together
   (survivors 1, params 3); the isolating arm is the candidate whose H9 case expects
   "^STORAGE btrfs-device-stats state=BLOCKED " (expected survivors 0, params 3, FAIL).`

3. In the landing commit, refresh `SCORECARD.md:2431` `PASS (124 cases, 124 passed, 0 failed)` → `PASS (128 cases,
   128 passed, 0 failed)` (QUALITY 57; K13 at `tools/check-self-assessment.py:656-663`).

4. Mark `before/c1-before.jsonl` as a re-derivation from base git bytes at `17:56:30Z` (after the `17:17:35Z`
   after receipt), not a pre-implementation capture; and describe the before as "forced by fixture monoculture"
   (round-40 wording) rather than as a discovered defect.

## 7. What would change this verdict

A live-output or exit-code difference between base and after (none: §1); a counter that rejects an
otherwise-passing candidate on `params` alone (none exists); or a base must-block table that already carried one
of the four shapes (none: base `:2978`, `:3013`, `:3021`, `:3039`).

## 8. What I did not do

Did not run the frozen counter (left to the executor/reviewer seats; host is shared and the counter is a
five-to-twenty-minute job at `--jobs 4`), did not re-run its full after receipt, and did not re-run control K2 —
`C1-K2` is read from `controls/C1-K2-candidate-without-H9-case.jsonl`. I ran the base and after census live
(§1), and four selftest variants of my own (§2). No tool was installed or upgraded.
