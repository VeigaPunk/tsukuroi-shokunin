2026-11-03T23:34:00Z
# K1Critic — attack on the two frozen claims and their predicates (round 69, re-based on the landing)

Scope: declaration `920a9eea3c5c5400567be0e96141014f338973df` (measured base
`acce353bacad74043636018d829e9e9b8e0fdf1c`) and the landed artifacts at
`32c0b50e64e6c5300fe604d8df8b87d19173a9d8` (`corpus/knowledge/kernel-taint-plane-r69.md`,
`tools/count-kr-rows-r69.py`, `tools/tsukuroi-census.sh`, `corpus/lessons/round-69.md`,
`corpus/QUALITY.md` 102/103, `.ufo/waves/round-69/after/`). This file was first written at
23:30Z against the pre-landing drafts; it is re-based on the landed content (the committed copy
of this file inside 32c0b50e is the earlier draft-based version). No lane file was written. All
lane reads are read-only git/file reads; the only git writes were in a `git clone --shared`
sandbox at `/fast/scratch/hyaku/tsukuroi-r69/K1Critic/clone` (deleted at EXIT).

Summary: **14 attacks, 3 fatal** (A1, A2, A5). **C1 fails as a depth claim**: the landed lesson
itself reports the depth verdict **unchanged**, and S288 is an explicitly admitted re-pin of the
already-mined S140. **C2 is weakened**: the arm is a genuine new read path, live and
verdict-neutral, but `pending` is false on the host's installed LTS package and the frozen
predicate cannot see it.

---

## A1 — C1's S288 is a re-pin of the mined S140, and the landing reports the depth verdict unchanged

Class: duplicate authority / no axis movement / freshness-shaped claim.

The two snapshots are the same bytes:

```
$ sha256sum .ufo/waves/round-27/sources/S140.rst .ufo/waves/round-69/before/src/tk-v7211.rst
727ddb82bc042e4c5777592128bc8ca0dd640376af515efa8cba2dff5f9a0841  .ufo/waves/round-27/sources/S140.rst
727ddb82bc042e4c5777592128bc8ca0dd640376af515efa8cba2dff5f9a0841  .ufo/waves/round-69/before/src/tk-v7211.rst
$ cmp -s .ufo/waves/round-27/sources/S140.rst .ufo/waves/round-69/before/src/tk-v7211.rst; echo $?
0
```

The landing admits both facts. `corpus/lessons/round-69.md` §Gate: "**Admitted as S288, as a
re-pin**: the bytes are byte-identical to S140's torvalds v7.2 snapshot (`cmp` rc 0 …) so no new
document content is claimed", and "Candidates refused … (a) A second torvalds-v7.2 registration
of `tainted-kernels.rst` — the same bytes as S140, adding no authority; refused." The note's KR5
says "Re-grounding only: S288's closed 0-19 taint table … is byte-identical to S140's v7.2 copy …
this entry claims no new taint mechanism." The registry row's own cell says "S140 records the
same sha256 … claims no second document".

The claimed axis movement does not occur. `corpus/lessons/round-69.md:38` (and Mistake 1):
"the integrator restructured the note so four rows carry the new mechanism and host binding and
one row states the re-grounding, and the depth verdict is reported as **unchanged**, not
improved." The landed note: KR1–KR4 are S289 vermagic rows, KR5 is the S288 re-grounding. So the
additive surface is the vermagic header (S289) instantiated on the host; the taint plane the
claim's title leads with is re-grounding, and the "module-tree plane" is held elsewhere (A3).
The after-predicate (`KR_ROWS=5 KR_VERIFIED=5`, SOURCES 289, NF 13) is met by the landed note —
I ran the landed counter on the landed note: `KR_ROWS=5 KR_VERIFIED=5`, rc 0 — but a met row
count is not a moved axis, as the landing's own verdict states.

Repair forced: the depth claim must be withdrawn or restated as "re-grounding + one new header";
the judge must not credit depth. **FATAL** to C1 as a depth claim.

## A2 — The "content-sensitive" counter certifies boilerplate; the landing's own mistake row concedes it

Class: counter vacuity / instrument does not measure the proposition.

Landed counter on the landed note (read-only, `--lane` the lane, `--revision 32c0b50e`):

```
$ python3 counter-landed.py --revision 32c0b50e --lane <lane> --snapshots .ufo/waves/round-69/before/src
KR_ROWS=5 KR_VERIFIED=5
KR_ROW KR1 ok … KR_ROW KR5 ok
rc=0
```

The same clause set, at the frozen path in the sandbox, passes a note whose statements are
unrelated filler:

```
| KR1 | This statement exists only to satisfy the minimum length requirement of the frozen counter | source=S140 | snapshot=tk-v7211.rst | digest=727ddb82…841 | quote="Table for decoding tainted state" |
… KR2–KR5 the same shape, unique ids only
KR_ROWS=5 KR_VERIFIED=5   rc=0
```

A materially **false** statement with the same quote also verifies (`KR2` rewritten to "12288 is
4096 plus 12345, so bits twelve and thirteen are both clear and no taint bit is set"): 5/5, rc 0.
The instrument author's own receipt is the same shape: `probes/E2Counter/outputs/boilerplate.md`
is six rows whose statement cell is `alpha beta gamma delta epsilon zeta eta theta iota kappa
lambda mu` with one quote; `probes/E2Counter/outputs/boilerplate.txt` prints
`KR_ROWS=6 KR_VERIFIED=6`, rc 0 (`results.json` `"boilerplate": {"rows":6,"verified":6,"rc":0}`).
The landing knows: `corpus/lessons/round-69.md` Mistake 2 (`R69-DECLARED-BOILERPLATE-KILL`)
records that the wave item told E2 a boilerplate six-row note "must not reach 5" "while the
frozen predicate counts the statement's words only", that the seat measured the acceptance and
refused to add semantic filtering, and routes "a content-sensitivity class for statements" to
the next frozen-counter amendment. `corpus/QUALITY.md` 102 clause (b) records the missing
held-ground sweep; no clause records the entailment gap.

What the counter enforces is row shape plus provenance bytes: unique id, ≥12 words, `source=`
membership, snapshot existence, sha256 equality, quote located verbatim. Quote presence is not
statement support: landed KR3's host string (`7.2.11-arch1-1 SMP preempt mod_unload`) is quoted
to the four token macros, landed KR4's LTS module reading (`6.18.57-2-lts SMP preempt mod_unload`)
is quoted to `UTS_RELEASE … MODULE_VERMAGIC_SMP MODULE_VERMAGIC_PREEMPT`; neither quote contains
the host string, and both verify. The note's depth rows are genuinely additive content, but the
instrument cannot be the proof of that.

Repair forced: the claim must stop calling the counter content-sensitive (the landing's lesson
already does), and the next frozen-counter amendment needs the mechanical entailment subset —
every decimal/hex token and backticked identifier in a statement must occur in the quote or at
the named snapshot anchor — plus a should-fail filler-statement fixture. **FATAL** to C1's
declared evidence.

## A3 — The "module-tree plane" is held ground, not a row of this note

Class: duplicate ground / scope overclaim.

The note's own `## Relation to held ground` says `boot-chain-r17.md` "already lists both module
trees as boot-input paths; this entry adds the ownership binding of each tree, not the fact that
two trees exist", and `driver-firmware-plane.md:278` already records "`/usr/lib/modules` holds
`6.18.57-2-lts` and `7.2.11-arch1-1`". The claim's phrase "the kernel taint, vermagic and
module-tree plane measured against this host" therefore names three surfaces, of which one is a
re-pin (A1), one is the actual additive rows (vermagic), and one is held ground with only an
ownership binding added. No KR row carries a module-tree source: KR4 is a vermagic row whose
statement includes the LTS tree's token, quoted to the header, not to any module-tree document
(none exists); the two-tree/owner facts are host receipts, not sources.

Repair forced: restate the claim as "the vermagic composition rule and host instantiation, with
the taint table re-grounded at the running tag"; drop "module-tree plane" from the depth claim.
**HIGH**.

## A4 — The counter's `source=` clause is existential; a row citing an unrelated registered source passes

Class: false provenance pass-through / headline unenforced.

The landed clause is membership only (`tools/count-kr-rows-r69.py:86`:
`elif not re.fullmatch(r"source=S[0-9]{3,}", cells[2]) or cells[2][7:] not in sources:`); it
never checks that the named source's registered URL/digest matches the `snapshot=`/`digest=`
cells. With every row's source changed to `S001` (Arch Linux News, `corpus/SOURCES.md` row 1)
while the quote and digest stay in the kernel snapshot, the counter prints
`KR_ROWS=5 KR_VERIFIED=5`, rc 0. The headline "SOURCED — S288, S289" is not what the clause
measures; a note citing only S140 (already registered) or only S001 satisfies the identical
clause set. The landed note happens to cite the right ids, but the predicate that is supposed to
prove it cannot reject the substitution, and the after-predicate's `SOURCES` row count does not
bind each row's source. The "directly after S287" adjacency is likewise asserted with no command
the counting command prints.

Repair forced (mechanical, pre-data): require `source ∈ {S288,S289}` for this note and registry
digest == snapshot digest; bind adjacency with `awk`/`grep -A2 '^| S287 '`. **HIGH** (same
instrument family as A2; the artifact is correct, the predicate is not).

## A5 — C2's `pending` is false on the host's own LTS package, and the frozen predicate cannot see it

Class: undefined field semantics / false operability value / untested positive branch.

The declaration freezes only `pending=NO|YES|UNKNOWN`; the derivation exists only in the seat
item ("pkgver's last `.` replaced by `-`"). The landed arm implements it
(`tools/tsukuroi-census.sh:2337`, `mapped="${pkgver%.*}-${pkgver##*.}"`), and the host has the
counterexample installed: `linux-lts 6.18.57-2` owns the `6.18.57-2-lts` tree, and an LTS boot's
release is `6.18.57-2-lts` (`before/host.txt`: `pacman -Q linux-lts` → `linux-lts 6.18.57-2`;
`ls /usr/lib/modules/` → `6.18.57-2-lts`; `probes/S2Scout-host.md`: `pacman -Qo
/usr/lib/modules/6.18.57-2-lts` → owned by `linux-lts 6.18.57-2`). Running the landed arm on
those real inputs (sandbox clone, real `pacman -Qo`, only the release/taint seams overridden):

```
$ TSUKUROI_KERNEL_OSRELEASE="$S/fx/osrelease" \
  TSUKUROI_KERNEL_MODULES=/usr/lib/modules/6.18.57-2-lts \
  TSUKUROI_KERNEL_TAINTED="$S/fx/tainted" bash tools/tsukuroi-census.sh 2>/dev/null | grep '^KERNEL'
KERNEL kernel-plane release=6.18.57-2-lts pkg=linux-lts pkgver=6.18.57-2 modules_tree=PRESENT tainted=12288 taint_bits=O,E pending=YES unreadable=0 detail=qo:multi-owner
rc=1
```

`pending=YES` is false: the running kernel **is** the installed `linux-lts` package; the string
surgery `6.18.57-2 → 6.18-57-2` can never equal `6.18.57-2-lts`. The landed mainline line is
correct (`after/census-live-postarm.txt`: `… release=7.2.11-arch1-1 pkg=linux … pending=NO …`),
but the predicate cannot distinguish it from a wrong LTS line. The landed selftest has no
positive-branch case: `grep -c 'pending=YES' tools/tsukuroi-census.sh` → 0, and the three
case-insensitive `lts` hits are the word "defaults"; a mutation forcing `pend=NO` whenever pkg
and release are known survives the whole 192-case suite. The note's own pending section is
mainline-specific (`pacman -Q linux`), so the wave holds the fact that falsifies the generalized
field.

Repair forced: freeze the derivation in the declaration (map the release to its owning package's
version, or only rewrite a `.archN-` component as the note's own `s/\.(arch[0-9]+)-/-\1-/` does),
add an LTS-shaped case (release `6.18.57-2-lts`, pkgver `6.18.57-2`) and a YES case, or drop
`pending`. **FATAL** to C2 as declared.

## A6 — `taint_bits=<csv>` and the closed 0–19 table are open at the edges

Class: unenumerated set / unpinned value grammar.

The declaration says only `<csv|none|UNKNOWN>`. The snapshot's Log column is two characters
(`_/O`, `_/E`, `_/J`), the kernel's own print uses single letters, and bits above 19 are a real
taint value (`1048576 = 2^20`). The seat item lets the implementer "name the behaviour you
chose"; the landed arm chose the safe behaviour (`taint_bits=UNKNOWN` with
`detail=tainted:bits-outside-closed-table`, landed selftest case). But the frozen predicate does
not require that choice: an arm that drops bit 20 and prints an empty or partial csv satisfies
`<csv>` and "decoded with the closed table"; the raw `tainted=` int is the only guard, and no
clause says the two must agree. Element grammar is unpinned (numbers `12,13` vs letters `O,E` are
both "csv"), though the landed cases pin letters for this implementation.

Repair forced: freeze `taint_bits` as uppercase log letters in ascending bit order and require
any bit ≥20 to force `UNKNOWN` (or a `+N` marker) with the detail token. **MEDIUM** for this
artifact, HIGH for the predicate.

## A7 — C1 and C2 are not causally separable: one anchor, one inference, two artifacts

Class: duplicate authority / false separability clause.

The declaration says "C1 touches only its note … C2 touches only `tools/tsukuroi-census.sh`.
Each verifies without the other." Two couplings contradict that:

1. C2's decode authority is S288, and S288 exists as a registry row **only through C1's patch**
   (`SOURCES` at base has S140, not S288: absence receipt "S288 rows 0"). If C1's S288 row is
   refused as the re-pin the lesson admits it is, the arm's "closed 0–19 table of S288" has no
   registry anchor; the same bytes are registered as S140, so the arm's citation must move to
   S140 or S288 must be registered under C2's own evidence. The landed arm's header comment
   says "closed bit->log table pinned by S288" (`tools/tsukuroi-census.sh:469-470`).
2. The release-token→package-version inference is asserted in **both**: the landed note's
   "reboot-pending predicate measured, not assumed" paragraph computes it, and the arm's
   `pending` field implements it. C1's note even documents the LTS package/tree mismatch that
   falsifies the arm's generalized rule (KR4/Reading: `linux-lts 6.18.57-2` owns the
   `6.18.57-2-lts` tree), while the arm prints `pending=YES` on that boot.

Repair forced: name S140 (the registered authority) in the arm's contract, or register S288 as a
C2-owned re-pin; and make exactly one artifact own the pending inference (the arm), with the
note citing it rather than recomputing it. **HIGH**.

## A8 — Vocabulary collision: `pending=` and `unreadable=` already mean something else in the same output

Class: operability/parse hazard (adjacency harm, not DEGRADED).

One census run prints three `pending=` grammars and multiple `unreadable=` domains:

```
PLANE update-safety: DEGRADED (status=UNKNOWN-UPSTREAM; pending=none; …)
DRIFT pacnew-plane pacnew=3 … unreadable=12 …
INITRAMFS initramfs-plane … unreadable=0
KERNEL kernel-plane … pending=NO … unreadable=0 …
```

Base: `before/census-live-baseline.txt`; after: `after/census-live-postarm.txt` (the landed KERNEL
line). A consumer parsing `pending=` across lines gets `none` (informational),
`REQUIRES-PREP(...)` (a verdict-bearing value) and `NO|YES` (kernel reboot state); a consumer of
`unreadable=` gets pacnew-pane counts, initramfs counts and kernel input counts. The line is
outside the rollup, so this is not a false DEGRADED, but it is a real key collision.

Repair forced: namespace the new keys (`kernel_pending=`, `kernel_unreadable=`) or document the
scoped grammar in the census header contract. **MEDIUM**.

## A9 — Wave discipline: no seat is asked to run a lane gate or write outside the wave dir; one milestone wording invites a tracked write

Class: discipline / scope.

All 13 prompts in `.ufo/waves/round-69/w1-spec.json` write under `.ufo/waves/round-69/`
(`drafts/{c1,c2,hygiene}`, `probes/<seat>/`); E1/E2/R2/M1/N1 use a `git clone --shared` sandbox
with an explicit `--lane`/`-C`; S1Scout re-fetches only from the allowed `git.kernel.org`; no
item asks a seat to run `scripts/sources-census.sh` or a lane gate in the lane. One wording
hazard: E3Hygiene's milestone/title says "**Land** the routed repair" while step 6 says "Do not
edit `corpus/QUALITY.md`; the L1 appends your draft." Repair: reword the milestone to "Draft".
**LOW**; otherwise discipline stands.

## A10 — Do-nothing control: neither claim is reachable by doing nothing

Class: control reachability — **claim stands**.

`before/absence-controls-receipt.txt` at `acce353b`: C1 note `cat-file` rc 128, C1 counter
rc 128, `^| KR[0-9]` rows 0, `grep -c KERNEL tools/tsukuroi-census.sh` 0, selftest 177, SOURCES
287, S288/S289 rows 0. A do-nothing control scores 0 rows / no counter / no KERNEL line.

## A11 — C2's neutrality and rollup separation stand

Class: false-DEGRADED / verdict-noise — **claim stands**.

`before/census-live-baseline.txt` (rc 1, six DEGRADED planes) and
`after/census-live-postarm.txt` (the same rollup line; the KERNEL line outside it) agree; the
selftest's A/B case ("one KERNEL line per run; rollup line, exit code and non-KERNEL line count
identical with the arm inputs present or absent") passes in the 192-case run. No false DEGRADED
is introduced by the arm; the only noise is A8's vocabulary and A5's false positive.

## A12 — The selftest count is a proxy: 192 cases pass, the only positive `pending` branch is untested

Class: count-as-proof / predicate hole.

Base 177 (`before/absence-controls-receipt.txt`), landed 192
(`after/selftest-at-work.txt`: `TSUKUROI_CENSUS_SELFTEST: PASS (192 cases, 192 passed, 0
failed)`), 15 new `R69-C2` checks — the claim's "≥ 185 with ≥ 8 new cases" is met. But the count
binds nothing about the cases' content: no case emits `pending=YES` (`grep -c 'pending=YES'
tools/tsukuroi-census.sh` → 0), so the branch that produces the positive operational signal is
never executed and a constant-NO mutant survives. The item's case list (a)–(i) is in the seat
prompt, not in the frozen declaration; the after-check cannot require it.

Repair forced: freeze the case list (at least the YES and LTS cases) in the declaration, or
require a mutation that flips `pending` to be killed. **MEDIUM**.

## A13 — The live line's values are not cross-checked by any frozen clause; a static line passes

Class: operability predicate gap.

The live-run clause checks "exactly one `KERNEL` line carrying every field exactly once in
contract order"; it never compares the value fields to an independent capture. A `printf` of the
known host string would satisfy the after-predicate, and a subtly wrong live value (A5's
`pending=YES`) is invisible. The landed line happens to match `before/host.txt`
(`release=7.2.11-arch1-1 pkg=linux pkgver=7.2.11.arch1-1 modules_tree=PRESENT tainted=12288
taint_bits=O,E pending=NO unreadable=0 detail=qo:multi-owner`), but only a human comparison
established that.

Repair forced: add a live-equality clause against the pre-declaration host capture (with a
time-varying-field allow-list), or have the sentinel re-read the six fields and diff them.
**HIGH**.

## A14 — The pre-data battery's mutant set omits the vacuity shape it most needs to kill

Class: instrument coverage.

`probes/E2Counter/results.json` shows five malformed fixtures (duplicate, digest, quote, source,
short) correctly failing 3–4/5, and the `boilerplate` fixture passing 6/6. The battery proves the
structural clauses bite, but not that a note with unrelated statements is rejected; none of the
eight M1Mutation mutants named in the wave spec targets statement–quote entailment either. The
landing's Mistake 2 records the same limit and routes it. Repair: add the entailment-token clause
(A2) and a filler-statement fixture to the next frozen counter. **MEDIUM**.

---

## Answers to the item's direct questions

- Do-nothing reachability: neither claim is reachable by doing nothing (A10).
- C1 depth vs pin re-read: the taint surface is unmoved (`cmp -s` rc 0 vs S140); the landing's
  own verdict is **depth unchanged**; only S289's vermagic rows are additive, and one source's
  worth (4 rows) did not move the axis (A1). C1 is a re-grounding plus one new header, not the
  claimed taint/vermagic/module-tree depth.
- C2 capability vs restatement: the *code* delta is real — the census reads none of `osrelease`
  (`grep -c osrelease tools/tsukuroi-census.sh` → 0), `taint` (0), `uname` (0), `/usr/lib/modules`
  (0) — one new line maps release→owning package→tree→taint decode. The *knowledge* is already
  held (`kernel-taint-r27.md` KT1–KT6, `driver-firmware-plane.md:278`,
  `update-safety-note.md:296/348`), so the acquisition is a machine-readable readout, not new
  knowledge. It stands as a (small) new repertoire row, weakened by A5/A6/A13.
- Universal/unenumerated/unsourced numbers: C1's "module-tree plane" has no row (A3); C2's
  `taint_bits` is open above bit 19 (A6); `pending` has no declared derivation (A5); the
  "directly after S287" adjacency is asserted with no command (A4).
- Counting command vacuity: yes — boilerplate, a false statement and an unrelated registered
  source all read `KR_VERIFIED=5`, rc 0 (A2/A4); the E2 receipt reads 6/6 with six
  Greek-alphabet rows (A2); the landed lesson's Mistake 2 concedes the predicate counts words
  only.
- Causal separability: no — C2's S288 anchor and C1's pending inference couple them (A7).
- Axis harm: no false DEGRADED (A11); space small; vocabulary collision is a real parse hazard
  (A8); `pending=YES` on an LTS boot is a false operational signal (A5).
- Wave discipline: clean on gate runs and write paths; one "Land" milestone wording hazard
  (A9).

K1_ATTACKS=14 K1_FATAL=3 K1_C1_VERDICT=fails K1_C2_VERDICT=weakened
