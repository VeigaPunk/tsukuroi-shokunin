2026-11-03T23:30:15Z
# K1Critic — attack on the two frozen claims and their predicates (round 69)

Scope: `SCORECARD.md` "Round 69 — declaration" at `920a9eea3c5c5400567be0e96141014f338973df`
(measured base `acce353bacad74043636018d829e9e9b8e0fdf1c`), `before/` receipts,
`drafts/` and `probes/` as they stood 2026-11-03T23:18–23:30Z. No lane file was written. All
lane reads are read-only git/file reads; the only git writes are in a `git clone --shared`
sandbox at `/fast/scratch/hyaku/tsukuroi-r69/K1Critic/clone` (deleted at EXIT).

Summary: **14 attacks, 3 fatal** (A1, A4, A5). C1 is mechanically met but its counting command
does not bind content or the named sources, and one of its two sources is a byte-identical
re-pin of an already-mined row. C2 is a genuine new read path whose live line is neutral, but
its `pending` field is false on the host's own installed LTS package and the frozen predicate
cannot see it. Verdicts: C1 **weakened**, C2 **weakened**.

---

## A1 — C1's S288 is a byte-identical re-pin of the already-registered, already-mined S140

Class: duplicate authority / depth inflation / freshness-shaped claim.

`S288` is not a new document. The v7.2.11 stable snapshot and the v7.2 torvalds snapshot that
round 27 registered as S140 are the same bytes:

```
$ sha256sum .ufo/waves/round-27/sources/S140.rst .ufo/waves/round-69/before/src/tk-v7211.rst
727ddb82bc042e4c5777592128bc8ca0dd640376af515efa8cba2dff5f9a0841  .ufo/waves/round-27/sources/S140.rst
727ddb82bc042e4c5777592128bc8ca0dd640376af515efa8cba2dff5f9a0841  .ufo/waves/round-69/before/src/tk-v7211.rst
$ cmp -s .ufo/waves/round-27/sources/S140.rst .ufo/waves/round-69/before/src/tk-v7211.rst; echo $?
0
```

S140's registry row already records that digest and the same content scope
(`git show 920a9eea:corpus/SOURCES.md`, row 146: `tag v7.2, Documentation/admin-guide/tainted-kernels.rst … raw bytes sha256 727ddb82…`), and round 27's note
`corpus/knowledge/kernel-taint-r27.md` holds KT1–KT6 of the same plane (KT1 decodes 12288 to bits
12/13, KT2 the O cause, KT3 the E cause). The draft itself concedes the point:
`drafts/c1/sources-rows.md` S288 cell: "S140 records the same sha256 at the torvalds v7.2 tag,
so this row pins the host release tag and claims no second document"; and KR1/KR2 say
"claims no new taint mechanism" / "re-grounds KT1/KR6 of corpus/knowledge/kernel-taint-r27.md".
The scribe's own probe (`probes/SC1Scribe/timing-and-crosschecks.txt`) measured the same
`cmp -s` rc 0, and R1Reviewer refused KR1/KR2 for the same reason
(`probes/R1Reviewer/attack.md:735`, `R1_VERDICT=refuse rows=KR1,KR2`).

The claim's depth headline is therefore inflated: of five KR rows, two are explicit re-pins of a
registered authority, and only S289 (`include/linux/vermagic.h`, no prior registry row:
`git show 920a9eea:corpus/SOURCES.md | grep -ci vermagic` → 0) adds a source. The surface the
claim moves is the taint plane of `kernel-taint-r27.md`; the command above shows it **unmoved**
— only the tag label changes. The additive depth is the vermagic header and its host
instantiation (KR3/KR4), not the taint plane the title leads with.

Repair forced: amend the claim's source accounting before scoring — S289 is the new authority;
S288 is a re-pin of S140 (same sha256) and must be stated as non-additive, or dropped from the
depth claim. The note may keep KR1/KR2 as re-grounding; the axis must not count them as new
depth. **FATAL** to the claim as worded ("SOURCED — S288, S289").

## A2 — The "content-sensitive" counter certifies boilerplate: statements are never compared to quotes

Class: counter vacuity / instrument does not measure the proposition.

Constructed at the frozen path in the sandbox, five rows whose statement cells are filler and
whose only real cells are one repeated quote and one digest:

```
| KR1 | This statement exists only to satisfy the minimum length requirement of the frozen counter | source=S140 | snapshot=tk-v7211.rst | digest=727ddb82bc042e4c5777592128bc8ca0dd640376af515efa8cba2dff5f9a0841 | quote="Table for decoding tainted state" |
… KR2–KR5 the same shape, unique ids only
$ python3 counter.py --revision HEAD --lane "$S/clone" --snapshots .ufo/waves/round-69/before/src
KR_ROWS=5 KR_VERIFIED=5
KR_ROW KR1 ok … KR_ROW KR5 ok
rc=0
```

A materially **false** statement with the same quote also verifies (`KR2` rewritten to "12288 is
4096 plus 12345, so bits twelve and thirteen are both clear and no taint bit is set"): counter
prints `KR_ROWS=5 KR_VERIFIED=5`, rc 0. The instrument author's own pre-data battery records the
same fact: `probes/E2Counter/outputs/boilerplate.md` is six rows whose statement cell is
`alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu` with one quote
("The kernel will mark itself as"), and `probes/E2Counter/outputs/boilerplate.txt` shows
`KR_ROWS=6 KR_VERIFIED=6`, rc 0 (`results.json`: `"boilerplate": {"rows":6,"verified":6,"rc":0}`).
The five malformed fixtures each break exactly one structural clause; none tests statement
entailment, so the battery cannot distinguish a note from a Greek alphabet.

What the counter actually enforces is row shape plus provenance bytes: unique id, ≥12 words,
`source=` membership, snapshot existence, sha256 equality, and quote located verbatim. The word
"content-sensitive" in the claim is not measured by any clause — quote presence is not statement
support. The draft note shows this live: KR4's 69-word statement (host vermagic, LTS token,
package ownership, "no reboot is pending") is bound to `quote="Simply sanity version stamp for
modules."`; KR5's applicability/falsifier statement is bound to
`quote="Don't worry too much about this, most of the time it's not a problem to run a tainted kernel"`.
Both verify 5/5 (`probes/SC1Scribe/note-selfcheck.txt`; my staged run of the real draft: see A4).

Repair forced: stop calling the instrument content-sensitive, or add the mechanical entailment
subset the claim can actually check — every decimal/hex token and backticked identifier in a
statement must occur in the quote or at the named snapshot anchor — and add a should-fail
fixture whose only defect is a statement unrelated to its quote. **HIGH**.

## A3 — The row grammar cannot source host measurements, yet the claim says "measured against this host"

Class: false provenance / evidence-shape mismatch.

Every row must carry `source=S###` and a quote from a committed snapshot under `before/src/`.
The only snapshots are the two documents, and neither contains the host measurements the note
asserts: `12288`, `7.2.11-arch1-1`, `6.18.57-2-lts`, the two `/usr/lib/modules` trees, or the
pacman owners. The claim's middle term, the "module-tree plane", has **no row at all**: KR1/KR2
are taint re-pins, KR3/KR4 are vermagic, KR5 is applicability; the module-tree facts live inside
KR4's statement cell and its quote is the file's 8-word purpose comment. The note's own
`## Relation to held ground` says `driver-firmware-plane.md:85` already holds an older
vermagic/single-tree observation, and `driver-firmware-plane.md:278` already records
"`/usr/lib/modules` holds 6.18.57-2-lts and 7.2.11-arch1-1" — the module-tree surface is
pre-existing corpus, not a row of this note. So the host half is either (a) unsourced prose
outside the counted rows, or (b) a statement whose quote does not entail it. The counter cannot
tell (b) from (a) (A2).

Repair forced: either add a per-row `host=` evidence cell bound to a committed receipt path plus
digest (host.txt/seat probe) and check it, or drop "measured against this host" from the claim
and state that the KR rows are document claims re-grounded by prose receipts. **HIGH**.

## A4 — The counter's source clause is existential: any registered S### passes, including one unrelated to the quote

Class: false provenance pass-through / headline unenforced.

The clause is membership only (`count-kr-rows-r69.py`:
`elif not re.fullmatch(r"source=S[0-9]{3,}", cells[2]) or cells[2][7:] not in sources:`). It never
checks that the named source's registered URL/digest matches the `snapshot=`/`digest=` cells.
Proven with the same boilerplate note, every row's source changed to `S001` (Arch Linux News,
`corpus/SOURCES.md` row 1) while the quote and digest stay in the kernel taint snapshot:

```
$ python3 counter.py --revision HEAD --lane "$S/clone" --snapshots .ufo/waves/round-69/before/src
KR_ROWS=5 KR_VERIFIED=5
KR_ROW KR1 ok … KR_ROW KR5 ok
rc=0
```

So the declared headline "SOURCED — S288, S289" is not what the counter measures; a note citing
only S140 (already registered) or only S001 satisfies the identical clause set. The real draft
happens to cite S288/S289, but the predicate that is supposed to prove it cannot reject the
substitution, and the after-predicate also counts `SOURCES` rows without binding each KR row's
source to the round's two ids.

Repair forced (mechanical, pre-data): require `source ∈ {S288,S289}` for this note, and require
the registry row's digest cell to equal the snapshot's sha256. Also bind the "directly after
S287" adjacency with a command (`awk`/`grep -A2 '^| S287 '`), which the frozen after-predicate
asserts but no counting command prints. **FATAL** to the claim's counting command.

## A5 — C2's `pending` is false on the host's own LTS package, and no frozen clause can catch it

Class: undefined field semantics / false operability value / untested positive branch.

The declaration freezes only the grammar `pending=NO|YES|UNKNOWN`; the derivation exists only in
the seat item (`E1KernelArm` step 4: "pkgver's last `.` replaced by `-`"). The arm implements it
(`drafts/c2/tsukuroi-census.sh:2333-2343`) and the host has the exact counterexample installed:
`linux-lts 6.18.57-2` owns the `6.18.57-2-lts` tree, and an LTS boot's release is
`6.18.57-2-lts` (`before/host.txt`: `pacman -Q linux-lts` → `linux-lts 6.18.57-2`;
`ls /usr/lib/modules/` → `6.18.57-2-lts`; `probes/S2Scout-host.md`: `pacman -Qo
/usr/lib/modules/6.18.57-2-lts` → owned by `linux-lts 6.18.57-2`). Running the drafted arm on
those real inputs (sandbox clone, real `pacman -Qo`, only the release/taint seams overridden):

```
$ TSUKUROI_KERNEL_OSRELEASE="$S/fx/osrelease" \
  TSUKUROI_KERNEL_MODULES=/usr/lib/modules/6.18.57-2-lts \
  TSUKUROI_KERNEL_TAINTED="$S/fx/tainted" bash tools/tsukuroi-census.sh 2>/dev/null | grep '^KERNEL'
KERNEL kernel-plane release=6.18.57-2-lts pkg=linux-lts pkgver=6.18.57-2 modules_tree=PRESENT tainted=12288 taint_bits=O,E pending=YES unreadable=0 detail=qo:multi-owner
rc=1
```

`pending=YES` is false: the running kernel **is** the installed `linux-lts` package; the string
surgery `6.18.57-2 → 6.18-57-2` can never equal `6.18.57-2-lts`. The frozen after-predicate
("every field exactly once in contract order", selftest ≥185 PASS) cannot see this, and the arm's
selftest never exercises the YES branch at all: `grep -c 'pending=YES'
drafts/c2/tsukuroi-census.sh` → 0 (the three case-insensitive `lts` hits are the word
"defaults"). A mutation that forces `pend=NO` whenever pkg and release are known would pass
every existing case; only UNKNOWN cases remain. C1's own note documents the LTS package/tree
mismatch (KR4, "the running tree is owned by linux … and linux-headers"), so the wave holds the
fact that falsifies its own new field.

Repair forced: freeze the derivation in the declaration (map the release to its owning package's
version, or compare against the tree name's package prefix rather than a dot→dash rewrite), add
an LTS-shaped hermetic case (release `6.18.57-2-lts`, pkgver `6.18.57-2`) and a YES case, or drop
`pending` from the line. **FATAL** to the claim as declared.

## A6 — `taint_bits=<csv>` and the closed 0–19 table are open at the edges

Class: unenumerated set / unpinned value grammar.

The declaration says only `<csv|none|UNKNOWN>`. The snapshot's Log column is two characters
(`_/O`, `_/E`, `_/J`), the kernel's own print uses single letters, and bits above 19 are a real
taint value: `1048576 = 2^20`. The E1 item lets the implementer "name the behaviour you chose"
for bits ≥20, and the drafted arm chose the safe behaviour (`taint_bits=UNKNOWN` with
`detail=tainted:bits-outside-closed-table`, selftest case at `drafts/c2/tsukuroi-census.sh:4118`).
But the frozen predicate does not require that choice: an arm that drops bit 20 and prints
`taint_bits=` empty or a partial csv also satisfies `<csv>` and "decoded with the closed table";
the raw `tainted=` int is the only guard, and no clause says the two must agree. Element grammar
is likewise unpinned (numbers `12,13` vs letters `O,E` are both "csv").

Repair forced: freeze `taint_bits` as uppercase log letters in ascending bit order, and require
any bit ≥20 to force `UNKNOWN` (or a `+N` marker) with the detail token; add the case to the
declaration, not only the seat item. **MEDIUM** for this artifact (the behaviour is safe), HIGH
for the predicate.

## A7 — C1 and C2 are not causally separable: one anchor, one inference, two artifacts

Class: duplicate authority / false separability clause.

The declaration says "C1 touches only its note … C2 touches only `tools/tsukuroi-census.sh`. Each
verifies without the other." Two couplings contradict that:

1. C2's decode authority is S288, and S288 exists as a registry row **only through C1's patch**
   (`SOURCES` at base has S140, not S288: absence receipt "S288 rows 0"). If C1's KR1/KR2 are
   refused (R1 recommends refusing them as non-additive), C2's "closed 0–19 table of S288" has
   no registry anchor; the same bytes are registered as S140, so the arm's citation must move to
   S140 or S288 must be registered under C2's own evidence. The arm's header comment already
   says "pinned by S288" (`drafts/c2/tsukuroi-census.sh:469`).
2. The release-token→package-version inference is asserted in **both**: C1's KR4 says "no reboot
   is pending", and the note's falsifier list says a `pacman -Q linux` / `uname -r` mismatch
   "would flip the reboot-pending predicate to YES"; C2's arm computes exactly that predicate.
   C1's note even documents the LTS case where the arm's rule is wrong (A5). Two artifacts now
   own one inference with different rules — the note's is an observed host mapping, the arm's is
   dot→dash string surgery.

Repair forced: name S140 (the registered authority) in the arm's contract, or register S288 as a
C2-owned re-pin; remove the pending conclusion from C1's KR4 (or make it cite the census field as
the operative instrument) so exactly one artifact owns the inference. **HIGH**.

## A8 — Vocabulary collision: `pending=` and `unreadable=` already mean something else in the same output

Class: operability/parse hazard (adjacency harm, not DEGRADED).

One census run now prints three different `pending=` grammars and two `unreadable=` domains:

```
PLANE update-safety: DEGRADED (status=UNKNOWN-UPSTREAM; pending=none; …)
DRIFT pacnew-plane pacnew=3 … unreadable=12 …
INITRAMFS initramfs-plane … unreadable=0
KERNEL kernel-plane release=7.2.11-arch1-1 … pending=NO … unreadable=0 …
```

Base evidence: `before/census-live-baseline.txt` (the update-safety and DRIFT lines); after
evidence: `probes/E1KernelArm/live.txt`. A consumer that parses `pending=` across lines gets
`none` (informational), `REQUIRES-PREP(...)` (a verdict-bearing value) and `NO|YES` (kernel
reboot state); a consumer of `unreadable=` gets pacnew-pane counts, initramfs counts and kernel
input counts. The line is outside the rollup, so this is not a false DEGRADED, but it is exactly
the kind of key collision that makes an operability line unparseable by the next tool.

Repair forced: namespace the new keys (`kernel_pending=`, `kernel_unreadable=`) or document the
scoped grammar in the census header contract. **MEDIUM**.

## A9 — Wave discipline: no seat is asked to run a lane gate or write outside the wave dir; one milestone wording invites a tracked write

Class: discipline / scope.

I read all 13 prompts in `.ufo/waves/round-69/w1-spec.json`. Every write target is under
`.ufo/waves/round-69/` (`drafts/{c1,c2,hygiene}`, `probes/<seat>/`); E1/E2/R2/M1/N1 use a
`git clone --shared` sandbox with an explicit `--lane`/`-C`; S1Scout re-fetches only from the
allowed `git.kernel.org`; no item asks a seat to run `scripts/sources-census.sh` or a lane gate
in the lane. One wording hazard: E3Hygiene's milestone and title say "**Land** the routed
repair" while step 6 says "Do not edit `corpus/QUALITY.md`; the L1 appends your draft." A seat
reading only the milestone could write a tracked corpus file. Repair: reword the milestone to
"Draft the routed repair". **LOW**; otherwise the wave's discipline stands.

## A10 — Do-nothing control: neither claim is reachable by doing nothing

Class: control reachability — **claim stands**.

`before/absence-controls-receipt.txt` at `acce353b`: C1 note `cat-file` rc 128, C1 counter
rc 128, `^| KR[0-9]` rows 0, `grep -c KERNEL tools/tsukuroi-census.sh` 0, selftest 177, SOURCES
287, S288/S289 rows 0. A do-nothing control therefore scores 0 rows / no counter / no KERNEL
line. Both claims require new artifacts to move at all.

## A11 — C2's neutrality and rollup separation stand

Class: false-DEGRADED / verdict-noise — **claim stands**.

`before/census-live-baseline.txt` (rc 1, six DEGRADED planes) and `probes/E1KernelArm/live.txt`
(rc 1, the same rollup line `TSUKUROI_CENSUS: DEGRADED (packages=… oom=…)`, the KERNEL line
outside it) agree; the selftest's A/B case
("one KERNEL line per run; rollup line, exit code and non-KERNEL line count identical with the
arm inputs present or absent") passes within the 192-case run. No false DEGRADED is introduced by
the arm; the only noise is A8's vocabulary and A5's false positive.

## A12 — The selftest count is a proxy: 192 cases pass, the only positive `pending` branch is untested

Class: count-as-proof / predicate hole.

The base count is 177 (`before/absence-controls-receipt.txt`), the draft has 192
(`probes/E1KernelArm/selftest.txt`: `TSUKUROI_CENSUS_SELFTEST: PASS (192 cases, 192 passed, 0
failed)`), 15 new `R69-C2` checks — the claim's "≥ 185 with ≥ 8 new cases" is met. But the count
binds nothing about the cases' content: no case emits `pending=YES`
(`grep -c 'pending=YES' drafts/c2/tsukuroi-census.sh` → 0), so the branch that produces the
positive operational signal is never executed, and a constant-NO mutant survives the whole
suite. The item's case list (a)–(i) is in the seat prompt, not in the frozen declaration; the
after-check cannot require it.

Repair forced: freeze the case list (or at least the YES case and the LTS case) in the
declaration, or require a mutation that flips `pending` to be killed by the suite. **MEDIUM**.

## A13 — The live line's values are not cross-checked by any frozen clause; a static line passes

Class: operability predicate gap.

The live-run clause checks "exactly one `KERNEL` line carrying every field exactly once in
contract order"; it never compares the six value fields to an independent capture. A `printf` of
the known host string would satisfy the after-predicate, and a subtly wrong live value (e.g. A5's
`pending=YES`) is invisible. The wave happens to have the independent capture
(`before/host.txt`, `probes/S2Scout-host.md`) but the frozen predicate does not name it. The
selftest proves the parser under fixtures, not the live seams.

Repair forced: add a live-equality clause against the pre-declaration host capture (with an
explicit allow-list for time-varying fields), or have the sentinel re-read the six fields and
diff them. **HIGH**.

## A14 — The pre-data battery's mutant set omits the vacuity shape it most needs to kill

Class: instrument coverage.

`probes/E2Counter/results.json` shows five malformed fixtures (duplicate, digest, quote, source,
short) correctly failing 3–4/5, and the `boilerplate` fixture passing 6/6. The battery therefore
proves the structural clauses bite, but not that a note with unrelated statements is rejected —
because none of the eight M1Mutation mutations listed in the wave spec
("drop the unique-id check; … accept a quote found only in the superseded snapshot; …") targets
statement–quote entailment either. The counter can be mutation-hardened and still certify A1/A2's
boilerplate. Repair: add the entailment-token clause (A2) and a `filler-statement` fixture to the
battery before the instrument is called content-sensitive. **MEDIUM**.

---

## Answers to the item's direct questions

- Do-nothing reachability: neither claim is reachable by doing nothing (A10).
- C1 depth vs pin re-read: the taint surface is unmoved (`cmp -s` rc 0 vs S140); only S289's
  vermagic rows are additive (A1). C1 is a partial re-pin, not new taint mechanism.
- C2 capability vs restatement: the *code* delta is real — the census reads none of
  `osrelease` (`grep -c osrelease tools/tsukuroi-census.sh` → 0), `taint` (0), `uname` (0),
  `/usr/lib/modules` (0) — one new line maps release→owning package→tree→taint decode. The
  *knowledge* is already held (`kernel-taint-r27.md` KT1–KT6, `driver-firmware-plane.md:278`,
  `update-safety-note.md:296/348`), so the acquisition is a machine-readable readout, not new
  knowledge. It stands as a (small) new repertoire row, weakened by A5/A6/A13.
- Universal/unenumerated/unsourced numbers: C1's "module-tree plane" has no row (A3); C2's
  `taint_bits` is open above bit 19 (A6); `pending` has no declared derivation (A5); the
  "directly after S287" adjacency is asserted with no command (A4).
- Counting command vacuity: yes — boilerplate, a false statement, and an unrelated registered
  source all read `KR_VERIFIED=5`, rc 0 (A2/A4); the E2 receipt does the same with six rows
  (A2).
- Causal separability: no — C2's S288 anchor and C1's pending inference couple them (A7).
- Axis harm: no false DEGRADED (A11); space small; vocabulary collision is a real parse hazard
  (A8); `pending=YES` on an LTS boot is a false operational signal (A5).
- Wave discipline: clean on gate runs and write paths; one "Land" milestone wording hazard
  (A9).

K1_ATTACKS=14 K1_FATAL=3 K1_C1_VERDICT=weakened K1_C2_VERDICT=weakened
