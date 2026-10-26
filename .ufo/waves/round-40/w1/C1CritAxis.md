VERDICT: defect-found

Seat C1CritAxis, item C1-12 (round 40 / hyaku run 8). Read-only on lane content; every variant built and run
under `/fast/scratch/hyaku/tsukuroi-r40/C1CritAxis/` and removed after the receipts were copied. Census bytes
under test: `git show c707e356:tools/tsukuroi-census.sh` = sha256 `032faa8f1c914dd63a1de673aa9ed6767c4bd19cdfc2751ac34331005da45733`,
identical to the working tree and to `f951f28:tools/tsukuroi-census.sh`. Counter:
`tools/score-selftest-literals-r40.py` sha256 `8b06de18ca7eec1d928a0dfac8ca6930bf808bfd1f4250374ec300640f2f0159`
(matches the declaration). Receipts: `.ufo/waves/round-40/w1/C1CritAxis/{variants.txt,fixture-mount-lines.txt,
host-fstype-case.txt,base-counter-53b294a.json}`.

## 1. What I re-ran, and what I did not

| Run | Command (abridged) | Observed |
|---|---|---|
| before, own run | `python3 tools/score-selftest-literals-r40.py --revision 53b294a27... --scratch <S>/counter/base --jobs 2` | exit 1, `baseline_pass 1`, `neutral_pass 3`, `mutants_applied 9`, **`survivors 9`**, `selfref 5`, baseline `TSUKUROI_CENSUS_SELFTEST: PASS (119 cases, 119 passed, 0 failed)` (`base-counter-53b294a.json`) |
| after, author receipt | `.ufo/waves/round-40/after/c1-after-c707e35.jsonl` | `survivors 0`, baseline `PASS (124 cases, 124 passed, 0 failed)`, 9/9 `killed`, 3/3 neutral pass, `selfref 5`, exit 0 |
| variants, own runs | 11 builds of the c707 census (9 mutant/neutral variants + 2 correction runs) + `bash <v>.sh --selftest` (cwd `/`, `PATH=/usr/bin:/bin`, `LC_ALL=C`, TMPDIR in scratch) | table in `variants.txt`; the two that matter here: an arm keyed on `,subvol=` **passes 124/124**, and M6's only kill is the uppercase-BTRFS case |

I did **not** re-run the full after receipt; I re-ran its baseline (124/124 PASS, matching the receipt) and
mutant M6 (killed, matching), and relied on the receipt and the frozen pre-data control rows
(`.ufo/waves/round-40/controls/controls.jsonl`) for M1–M5, M7–M9 and the K1/K2/K3 controls.

## 2. Axis fit — operability, supports, with the evidence type stated honestly

`AXES.md` ("The six axes" table): operability = "Runnable artifacts: checklists that are executable, commands
that exist, scripts that run"; signal = "A checklist item can be run and produces the stated outcome". The
artifact here is `run_selftest` (`tools/tsukuroi-census.sh:1928`), and the move is exactly: run it, it now
fails on wrong storage arms instead of passing them. That is operability's signal, not calibration's
(self-assessment honesty) and not depth's (cited technical detail). Lane precedent agrees: rounds 38 and 39
put the same instrument's hardening on operability (`SCORECARD.md:2220`, `:2249`).

Three qualifications belong in the row rather than in a footnote:

1. **The artifact's own output does not change.** Before `PASS (119 cases)`, after `PASS (124 cases)`
   (`base-counter-53b294a.json`; author receipt). The before→after is visible only under mutation, so the
   claim is *instrument sensitivity*, not a new host reading.
2. Operability is saturated at 9 (`SCORECARD.md:2270`), so this claim can move no ordinal; the declaration
   correctly claims none (`SCORECARD.md:2303`). As a defect repair it is legitimate; as an axis move it is
   a repair of the lane's own measuring rig.
3. The evidence type is a mutant-kill rate over nine hand-selected mutants (the round-39 survivors). That is
   a test-quality measure whose value is bounded by the sample; §5 shows the sample is not fair.

Verdict: **axis fit = operability, no other axis harmed** (the commit is 36 insertions, 0 deletions, all
inside `run_selftest`; `probe_storage_arm` at `:1906-1921` is byte-identical, so no live datum changes).
The defect is in how much the nine kills prove, not in which axis was chosen.

## 3. Is the before (9 survivors) reachable by a do-nothing control only? — Yes, and that is its limit

The before is *exactly* the do-nothing measurement: control `C1-K0-do-nothing-base`
(`controls/controls.jsonl`, revision `53b294a27...`) scores `survivors 9` with all nine names, and my own run
reproduced `survivors 9`, exit 1. Nothing else is needed to reach the number.

That makes it a valid before and an uninformative one. At base the selftest carries exactly one btrfs table
line (`tsukuroi-census.sh:2978`) and the arm is unchanged, so every mutant either keys on a literal of that
one line (M1, M2, M3, M4, M8) or exercises a guard no base case reaches (M5 grep-count passes because
`btrfs` appears only in the fstype field of the one line; M6 folds case on an input never supplied; M7's
`blocked -eq 0` conjunct never has a btrfs mount behind it; M9's `tail -1` is right when the btrfs line is
the only line). The nine survivors are therefore *forced by the fixture monoculture*, not discovered: the
before number is a ceiling ("everything is masked") and carries no information about which fault a real
observation had previously caught. The counter cannot separate "fixtures are monocultural" from "the arm is
broken" at base — which is what the claim says the defect was, so no overreach, but also no measurement.

## 4. Could the target be met without the selftest discriminating any new real host state? — Yes, 1 of 9 kills

M6 (`fstype-casefold`, the round-39 MutParse (b) survivor) is killed **only** by the fixture added at
`tsukuroi-census.sh:3032-3035`, whose btrfs line is `/dev/fx0 / BTRFS rw,relatime 0 0` — an uppercase
fstype. Measured:

- `m6` (frozen M6 text) → exit 1, `FAIL (124 cases, 123 passed, 1 failed)`, and the single failing case is
  `healthy: the fstype match is exact, so BTRFS is not btrfs (R40-C1)` (`variants.txt`).
- `m6-nocase` (M6 with that one case block removed) → exit 0, `PASS (123 cases, 123 passed, 0 failed)`;
  `nocase-base` → exit 0 as well. So M6 has no other killer.

A `BTRFS` fstype is not a host state for btrfs. Field 3 of `/proc/self/mounts` is the registered fs name;
`/proc/filesystems` lists `btrfs` in lower case and holds 0 upper-case names (35 entries), and this host's
four btrfs mounts all read `btrfs` (`host-fstype-case.txt`). The one upper-case fstype in the host's table is
`fuse.Grok_Bot_0.70.2.AppImage` — a FUSE type that embeds a binary name, i.e. case is a real hazard for
FUSE, not for btrfs. [INFERENCE] The kernel name is a fixed string in `btrfs.ko`, so nothing short of a
patched module prints `BTRFS`.

Consequence: M6 is equivalent on every host-producible input, and its kill is a *spec pin* (the fixture
comment says so: "the fstype match is exact, so BTRFS is not btrfs"). The counter's own equivalence policy
excludes the `$fsn → $devn` guard mutant for equivalence (docstring; declaration under "Equivalent mutant")
while counting M6, which is equivalent over the reachable domain. That is an inconsistency in the tally's
meaning, not a false statement: the declaration says "vary ... fstype case", which is accurate. But "guard
arms of the round-39 STORAGE cross-check fail it" should not be read as "nine host-reachable faults are now
caught"; it is eight, plus one documented limitation.

The other eight kills do map to host-reachable classes: M1 (device literal) needs only a btrfs line with a
different device (`:3013` `/dev/nvme0n1p3`, `:3021` `/dev/sda2`); M2 (root mountpoint) is beaten by the real
`/home` and `/var/log` mounts this host already has; M3 (`grep -c btrfs`) is beaten by `btrfs` in a device or
mountpoint name at `:3028` (`/dev/disk/by-label/btrfs-old /mnt/btrfs-backup` — a real naming pattern; the
`comment=btrfs` option on the same line is synthetic but redundant); M4/M8 by any other subvolid or subvol;
M5/M7/M9 as above. Note `:3028` is the only fixture whose *negative* direction is exercised by a
`btrfs`-looking option, and that option (`comment=btrfs`) is not a real ext4 mount option.

## 5. QUALITY 87 (b) — met on the letter, unmet on the dimension the criterion names

`corpus/QUALITY.md:171` requires: fixtures "share one literal shape (one device string, one option set)"
→ vary that shape across fixtures; and, frozen before scoring, "an arm keyed on a literal common to every
fixture" must fail.

- Varying: device (5 values), mountpoint (`/`, `/home`, `/var/lib/machines`, `/data`, `…/btrfs-backup`),
  option values, subvolume ids (256, 5, 263), position (btrfs line not last at `:3013`, third of four at
  `:3021`), fstype case, plus the unlistable root with btrfs mounted (`:3037`). ✓
- Frozen one-literal control: `C1-K1-one-literal-fixtures` (base census + five copies of the round-39
  literal) scores `survivors 9`, FAIL, pre-data (`controls.jsonl`). ✓
- **Option set: still one shape per class.** Enumerated in `fixture-mount-lines.txt` (14 distinct table
  lines): all **4** btrfs lines carry a `subvol=` selector (`:2978`, `:3013`, `:3021`, `:3039`; `:2978` is
  reused by three cases, so six case instances mount btrfs), and **none of the 10** lines that are not
  btrfs does (9 other fstypes plus the upper-case `BTRFS` line at `:3033`). `QUALITY.md:171` names "one
  option set" as the very shape to vary; here the option set is varied in its values but not in this
  property.
- Measured consequence: an arm keyed on that literal passes the whole round-40 selftest. `subvol-comma-key`
  (`case $mtab in *',subvol='*`) → exit 0, **PASS (124 cases, 124 passed, 0 failed)**; `subvol-eq-key`
  (`*'subvol='*`) → exit 0, PASS 124/124 (`variants.txt`). This is the same class as round 39
  (R39-FIXTURE-MONOCULTURE: "an arm keyed on the literal `subvolid=256` passed 11/11"), one level down: the
  literal is no longer one device string but one option property shared by every btrfs fixture.
- [INFERENCE] It is not a harmless synonym on a real host: a btrfs mounted at the top-level subvolume reports
  no `subvol`/`subvolid` option, so a `,subvol=`-keyed arm returns the round-39 false `HEALTHY 0/0/0` for an
  ordinary btrfs mount. No fixture in the selftest has a btrfs line without a subvolume selector, so the
  selftest cannot see that arm.

So 87(b) is satisfied at its stated test and not for the option-set dimension it names. The claim's wording
("vary ... options, subvolume") is true for the values; the missing variation is the *presence* of a
subvolume option.

## 6. Is nine mutants a fair sample of the arm? — No; list of kinds none of M1–M9 represents

Measured (my runs) — kinds the c707 fixture set does not discriminate:

- **Option-set-keyed arms** (`*',subvol='*`, `*'subvol='*`): survive 124/124. The whole class "key on a
  literal that every btrfs fixture happens to carry" is still open.

Measured — kinds the fixtures *do* kill but no frozen mutant represents (so nothing in the receipt shows it):

- `fieldswap-mp` (`[ "${_mp:-}" = btrfs ]`, mountpoint field): killed, FAIL 120/124 (4 cases).
- `head-1` (`head -n 1` partial read from the front; M9 covers only `tail`): killed, FAIL 121/124 (3 cases).
- `block-always` (drop the fstype test and set `blocked=1` unconditionally): killed, FAIL 121/124 (3 cases).

Not represented and not measured (reasoned only):

- **Table-open guard mutants**: `[ -f "$PROC_MOUNTS" ]` → `[ -e` (would hang on the `:2999` FIFO fixture —
  killed only by the counter's 900 s timeout, never by a verdict), dropping `[ -n "$mtab" ]` (`:1910`), and
  inverting the `mounts:unreadable` else branch. The fixtures exist; no mutant exercises them.
- **Detail-token mutant** (any edit to `mounts:btrfs-without-sysfs`): the case regexes would kill it, but no
  mutant demonstrates it.
- **Kill attribution**: the counter reads stdout only (`score-selftest-literals-r40.py:104-108`) while the
  selftest writes FAIL lines to stderr (`tsukuroi-census.sh:2019`), so `first_fails` is structurally always
  `[]` — visible in the author receipt for all nine mutants and in the control rows. A "kill" therefore
  means "the whole 124-case selftest failed somewhere", not "a storage fixture failed it". For M6 I
  isolated the case by hand; for the other eight the receipt cannot.

So the sample is nine mutants chosen to match the round-39 observed survivors, plus two variants of one
round-39 member, and it omits the one dimension the fixtures still fix. It is a fair sample of *the round-39
list* and not of the arm.

## 7. Two smaller items

- **Brittleness (fail-closed, acceptable).** Mutant applicability is bound to exact arm bytes; control
  `C1-K3-arm-rewritten` shows a semantics-preserving rename makes `mutants_applied 2/9` and FAIL
  (`controls.jsonl`). The counter is a round gate, not a lasting one.
- **Downstream case-count obligation.** `tools/check-self-assessment.py:649-655` (K13) compares the
  operability row's stated `N cases` with the census selftest at the revision. The round-40 outcome row must
  restate **124** cases for the measured revision (base 119 at `:2270`), or K13 fails. Nothing has been
  written yet; flagging it before the outcome lands.

## 8. Smallest safe correction

1. **Fixture (measured, 20 s per run).** Add one blocking case whose btrfs line has no subvolume selector —
   `printf 'proc /proc proc rw 0 0\n/dev/sdc1 /mnt/plain btrfs rw,relatime 0 0\n'`, empty sysfs root,
   expecting `state=BLOCKED … detail=mounts:btrfs-without-sysfs`. Measured: `fix-base` → exit 0,
   `PASS (125 cases, 125 passed, 0 failed)`; `fix-subvolkey` (fix + `,subvol=`-keyed arm) → exit 1,
   `FAIL (125 cases, 124 passed, 1 failed)`, failing case `a plain btrfs mount with no subvolume option is
   BLOCKED`. That closes the measured survivor without touching any existing case.
2. **Optional companion fixture**: one *negative* line carrying a subvol-like option on a non-btrfs fstype,
   so the reverse direction is also pinned (e.g. an ext4 line with `subvol=/x`), which kills the keyed arm
   from the other side.
3. **Frozen counter**: M1–M9 and the predicate are frozen at sha `8b06de18…`; a `,subvol=`-keyed mutant cannot
   be added to this round's tally without a new frozen revision. The honest in-round move is to name the
   residual as a known limit (§9) and hand the mutant to the next round's freeze.

## 9. Proposed text (optional, for the C1 claim/row)

> Known limit (C1CritAxis, round 40): the five mount-table fixtures vary device, mountpoint, option values,
> subvolume id, line position and fstype case, and every btrfs line they add carries a subvolume selector
> while no non-btrfs line does. An arm keyed on `,subvol=` (or on `subvol=`) therefore passes the selftest
> 124/124 (`.ufo/waves/round-40/w1/C1CritAxis/variants.txt`, `subvol-comma-key`/`subvol-eq-key`), so the
> literal-keyed class is closed only for the round-39 arms M1–M9; the option-set dimension named in
> QUALITY 87 (b) is not fully varied. The `fstype-case` fixture asserts exact fstype matching on an
> upper-case `BTRFS` line, which no btrfs host produces (`/proc/filesystems` lists `btrfs`), so M6's kill is
> a spec pin, not a second-reading of a host-reachable fault.

If the operator prefers only the fixture repair, items 1–2 satisfy it; if the wording is to stay as it is,
the paragraph above is the smallest honest disclosure.

## 10. Impacted axes

- **operability** — supports (artifact runnable, now fails on eight host-reachable mis-arms); the claim's
  ordinal cannot move (saturated at 9), and one ninth of the tally is a non-host spec pin.
- **calibration** — the before number is a do-nothing ceiling (§3) and the kill count is unattributed (§6);
  naming both keeps the row honest. No overreach found in the declaration itself.
- **freshness** — the operability row's `119 cases` (`SCORECARD.md:2270`) must become 124 at the measured
  revision or K13 fails (§7).
- **depth, coverage, adjacency** — untouched; the commit changes no live path and no knowledge row.

## 11. Scope notes

- No tool was installed or upgraded (system `bash`, `python3`, `git show`, `man` only).
- My reads bind the bytes named in §1: `git status --porcelain -- tools/tsukuroi-census.sh
  tools/score-selftest-literals-r40.py .ufo/waves/round-40/controls .ufo/waves/round-40/after` was empty at
  report time. The working tree meanwhile shows other round-40 wave files (`make-w1-spec.py` modified,
  `corpus/lessons/round-40.md` and `w1-spec.json` untracked) written by the wave harness, not by this seat;
  none of them is content I judged.
- Scratch `/fast/scratch/hyaku/tsukuroi-r40/C1CritAxis/` removed after the four receipts were copied; no
  census copy or `corpus/SOURCES.md` was copied into the seat dir.
- Read-only on all lane content: the only lane writes are `.ufo/waves/round-40/w1/C1CritAxis.md` and the
  four files in `.ufo/waves/round-40/w1/C1CritAxis/`.
