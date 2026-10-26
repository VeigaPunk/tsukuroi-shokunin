VERDICT: draft

# C1ScribeSkill — item C1-14: `SKILL.md` storage-arm held-out tables section (draft, not applied)

Draft only. No tracked lane file was edited, `SKILL.md` was not touched, the counter was not re-run (the C1 executor
holds that once-per-item run), and no tool was installed. Scratch `/fast/scratch/hyaku/tsukuroi-r41/C1ScribeSkill/`
was removed after the draft was copied out.

Insertion point: **end of `SKILL.md`** (3561 lines; last section is the counter-lineage round-40 wave note), appended as
a new section so no earlier text moves. The exact bytes are also at
`.ufo/waves/round-41/w1/C1ScribeSkill/draft-skill-storage-heldout-r41.md` and are reproduced verbatim below.

## Evidence

**Scope of the change.**
- `git -C … show --stat 568c397` → `tools/tsukuroi-census.sh | 27 +++…`, `1 file changed, 27 insertions(+)`;
  `git diff --stat 0e5805a1 568c397 -- tools/tsukuroi-census.sh` → the same single line; removed lines
  `git diff c707e356 568c397 -- tools/tsukuroi-census.sh | grep -c '^-[^-]'` → `0`.
- `probe_storage_arm` is unchanged: `diff` of `git show 0e5805a1:tools/tsukuroi-census.sh | sed -n
  '/^probe_storage_arm()/,/^}/p'` against the `568c397` slice → empty (`ARM_IDENTICAL`); the function spans
  `tools/tsukuroi-census.sh:1865-1925`.
- `git rev-parse 568c397:tools/tsukuroi-census.sh HEAD:tools/tsukuroi-census.sh` → `dda066f48fdc…` twice, so the
  line numbers cited in the draft are valid at the implementation commit and at the round tip `71851d63`.
- Case count: before receipt baseline `PASS (124 cases, 124 passed, 0 failed)`
  (`.ufo/waves/round-41/before/c1-before.jsonl`), after receipt baseline `PASS (128 cases, 128 passed, 0 failed)`
  (`.ufo/waves/round-41/after/c1-after-568c397.jsonl`).

**The four cases and their labels** (`git show 568c397:tools/tsukuroi-census.sh | sed -n '3039-3062p'`):

| `case_home` | lines | `check` label | table |
|---|---|---|---|
| `storage-mounts-mp-relative` | 3039-3043 | `healthy rollup: a btrfs line whose mountpoint is not absolute still counts, BLOCKED (R41-C1 H5)` | `/dev/vdc1 relative/mnt btrfs rw,relatime,subvolid=5,subvol=/ 0 0` |
| `storage-mounts-src-uuid` | 3045-3049 | `healthy rollup: a btrfs line whose source is not under /dev still counts, BLOCKED (R41-C1 H6)` | `UUID=0b1c2d3e-4d5e-6f70-8192-a3b4c5d6e7f8 /data btrfs rw,relatime,subvolid=5,subvol=/ 0 0` |
| `storage-mounts-no-subvol-opt` | 3051-3055 | `healthy rollup: a btrfs line with no subvol= option still counts, BLOCKED (R41-C1 H9)` | `/dev/sdc1 /mnt/plain btrfs rw,commit=60 0 0` |
| `storage-mounts-two-btrfs` | 3057-3062 | `healthy rollup: two btrfs lines are still btrfs without sysfs, BLOCKED (R41-C1 H10)` | `/dev/nvme0n1p2 / btrfs … subvolid=256,subvol=/@` + `proc /proc …` + `/dev/nvme0n1p2 /home btrfs … subvolid=257,subvol=/@home` |

All four expect `^STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0
detail=mounts:btrfs-without-sysfs$` (lines 3043, 3049, 3055, 3062). The fixture seam is
`TSUKUROI_PROC_MOUNTS="$FX/mounts"` at `tools/tsukuroi-census.sh:2166`, read by the arm at `:463`.

**Kills, per case** (`.ufo/waves/round-41/after/c1-after-568c397.jsonl` `mutants.<id>.confirm_labels`, i.e. stderr
`FAIL <label>` lines reproduced in a second run):
`storage-mounts-mp-relative` → H5-mountpoint-absolute, M1-VA-device-literal, M2-VB-root-mountpoint,
M4-VG-subvolid-256, M8-subvol-at-literal; `storage-mounts-src-uuid` → H6-source-devonly + the same M1, M2, M4, M8;
`storage-mounts-no-subvol-opt` → H9-subvolkey-option + M1, M2, M4, M8; `storage-mounts-two-btrfs` →
H10-count-exactly-one, M1-VA-device-literal. Union 8 of 13; the four H mutants each have a one-label confirm set
(their own case); M3/M5 (confirm set: `storage-mounts-btrfs-in-path`), M6 (`storage-mounts-fstype-case`), M7
(`storage-root-unreadable-mounted`) and M9 (`storage-mounts-varied-home`, `…-varied-multi`) are killed by round-40
cases only.

**Predicate and receipts.** `.ufo/waves/round-41/after/c1-after-568c397.jsonl`: `baseline_pass 1`, `capture_pass 1`,
`neutral_pass 3`, `decoy_pass 1`, `mutants_applied 13`, `survivors 0`, `params 4`, `result PASS`, `exit 0`; run at
`--jobs 6`, started `2026-10-26T17:17:35Z`, finished `17:23:56Z` (6 m 21 s). Before at `0e5805a1`: baseline
`PASS (124 cases…)`, `survivors 4` (H10, H5, H6, H9), `params 0`, `exit 1`. Counter digest `sha256sum
tools/score-selftest-mounts-r41.py` → `8306d9990b156ceb625eabbe942910fc0d09b20f350a7e8af1ff2237fd07355c`;
`git show e479fdc5:tools/score-selftest-mounts-r41.py | sha256sum` → the same. The executor's independent rerun
(`.ufo/waves/round-41/w1/C1ExecRerun/c1-rerun-568c397.jsonl`, with `field-compare.json`) reproduces every top-level
predicate field and every per-mutant `confirm_labels` set: `equal: true` on all compared fields, `survivors 0`,
`params 4`, `result PASS`.

**Decoy mechanism.** `tools/score-selftest-mounts-r41.py:114-127`: `DECOY_DELIM='R41DECOY'`, `decoy()` wraps every
mutant's replacement text in `: <<'R41DECOY' … R41DECOY` and inserts it in front of the count loop, i.e. inside
`probe_storage_arm` in the counter's private copy. Receipt `decoys.D-all-mutant-texts` → `exit 0`, `PASS (128 cases,
128 passed, 0 failed)`. Pre-data controls: K1 (`declare -f` prologue on the base) and K3 (the same on the candidate)
both FAIL with `decoy_pass 0` (`SCORECARD.md:2486-2491`).

**Kill attribution.** `tools/score-selftest-mounts-r41.py:190-202` (`failed_base_labels`, `killed`) and `:255-271`
(confirmation run, `confirm_labels`, `confirmed`). The receipt's `first_fails` now carry raw stderr `FAIL …` lines
(`:159`, first three per run), e.g. `FAIL healthy rollup: a btrfs /home … (R40-C1): plane evidence missing: …`; the
same field also shows unrelated flakes (`hostname override not honoured — possible host read`) in the first runs of
M2, M4, M5, M9 and H9, none of which reached the confirmed intersection.

**`params`.** `:115-117` injects a `cp` of `$FX/mounts` beside the label and wanted patterns in `check()`; `:162-188`
requires a PASSing baseline case per declared table property whose wanted patterns include
`detail=mounts:btrfs-without-sysfs`. Receipt `param_cases` maps P1→H5 label, P2→H6, P3→H9, P4→H10. Control K2
(candidate with the H9 case removed), `.ufo/waves/round-41/controls/C1-K2-candidate-without-H9-case.jsonl`:
`params 3`, `survivors 1` (`H9-subvolkey-option`), `exit 1`.

**Kernel shape of the mount table** (measured 2026-10-26, `unshare -rm`, tmpfs, ctypes `mount(2)`):
`mount(b"relative-source", b"tgt1", b"tmpfs", 0, None)` → rc 0, and `/proc/self/mounts` then reads
`relative-source /fast/scratch/hyaku/tsukuroi-r41/C1ScribeSkill/tgt1 tmpfs rw,relatime,uid=1000,gid=1000,inode64,huge=advise 0 0`;
`mount(b"UUID=0b1c2d3e-4d5e-6f70-8192-a3b4c5d6e7f8", <absolute target>, b"tmpfs", …)` → the source prints verbatim. So
the mountpoint is canonicalised to absolute, the source is opaque text. `proc_pid_mounts(5)` points the format at
`fstab(5)`. Host table: `awk '$3=="btrfs"' /proc/self/mounts | wc -l` → `4`, all `/dev/mapper/root`, all absolute
mountpoints, all carrying `subvol=`.

**Runtime note carried from the item.** 19 selftests per run (baseline, capture, 13 mutants, 3 neutrals, decoy) plus
one confirmation run per attributed kill and one serial retry for a failed non-mutant run; 6 m 21 s at `--jobs 6` on
this loaded host. The draft says run it at most once per item at `--jobs 4`.

## Findings

1. **The new cases' union is 8 of 13 mutants, not all 13.** M3, M5, M6, M7 and M9 stay killed only by round-40 cases,
   and no new case is the sole killer of any M1-M9 mutant. The draft says this; the per-row Kills column is complete.
2. **Operability value is uneven across the four.** H10 is the only case whose property the live table has today (four
   btrfs lines, so `mt -eq 1` answers false on it — a live bug class whenever the sysfs root is absent or hidden, the
   only branch that reads the table). H5 pins a shape `/proc/self/mounts` cannot print (measured: a
   relative mount target is stored absolute). H6's non-`/dev` source is representable in the format (source prints
   verbatim) but no btrfs line with one was observed; no btrfs mount was attempted here. H9's "btrfs with no `subvol=`
   option" is a normal kernel shape this host does not show [inference, not mounted]. Three of four are therefore
   contract pinning over the overridable `TSUKUROI_PROC_MOUNTS` file, not live-host exposure — the draft's limits say
   exactly that instead of crediting host coverage.
3. **Kill attribution over-attributes in principle.** A mutant is killed when any baseline label fails twice; an
   unrelated reproducible flake counts as a kill. The receipt's own first runs carry such labels (`hostname override
   not honoured — possible host read` on M2, M4, M5, M9, H9), but they did not survive the confirmed intersection, so
   the 13 attributions here are not carried by flakes that reproduced.
4. **`params` is a shape gate, not a behaviour test.** It proves a passing case handed `check()` a table with the
   declared property and wanted a `detail=mounts:btrfs-without-sysfs` line; it cannot refuse a selftest that hands
   those tables and hardcodes the answers elsewhere. It does catch a missing case (K2: `params 3`, `survivors 1`).
5. **The decoy refuses text-grep self-readers only.** A reader that strips here-documents before matching, or keys on
   the fixture tables, the four new labels or the expected regexes, is untouched — the limit the round-41 declaration
   records and wave item C1CritDecoy attacks.
6. **Round-40 §6.2's receipt gap is closed for this counter**: `first_fails` is stderr text now, not a count, but only
   the first three lines per run are kept.

## What this seat did not do

- Did not run the counter (at most once per item). The draft rests on `after/c1-after-568c397.jsonl` and on the
  executor's independent rerun in `w1/C1ExecRerun/` (landed 18:12Z): every predicate field and every per-mutant
  `confirm_labels` set compares equal; no kill was re-derived by applying mutants.
- Did not apply the draft; `SKILL.md` and every other tracked lane file are untouched; no git/jj mutation, no index
  touch.
- Did not mount btrfs anywhere (host read-only; the measurement namespace held no block device).
- No host mutation, no sudo, no pacman transaction (paused), no service action; the only mount was an `unshare -rm`
  tmpfs that died with its namespace.

## Exact proposed text

Appended at the end of `SKILL.md`; identical to
`.ufo/waves/round-41/w1/C1ScribeSkill/draft-skill-storage-heldout-r41.md`.

````markdown
## Storage arm selftest held-out tables — round 41

Appended 2026-10-26 (round-41 C1, commit `568c397da11339aed65181be598414f268835555`). Append-only: the round-38,
round-39 and round-40 storage-arm sections above stay as written, and the arm itself — `probe_storage_arm`,
`tools/tsukuroi-census.sh:1865-1925` — is unchanged: its text at `568c397` is byte-identical to the base `0e5805a1`
(empty `diff` of the two `sed -n '/^probe_storage_arm()/,/^}/p'` slices), the census file at `568c397` and at the
round tip `71851d63` is the same blob (`dda066f4`), and the commit is `1 file changed, 27 insertions(+)` in
`run_selftest` only, with zero removed lines (`git diff --stat 0e5805a1 568c397 -- tools/tsukuroi-census.sh`). No
earlier label or expected line moved, and the selftest count goes 124 → 128 (`PASS (128 cases, 128 passed,
0 failed)`).

Round 40 varied the btrfs line but left four shapes shared by every must-block table: mountpoints absolute, sources
`/dev/*`, a `subvol=` key on every btrfs line, exactly one btrfs line per table — the residual monoculture it named
(`.ufo/waves/round-40/w1/C1HeldOutMutants.md:194-196`). Three held-out mutants of that class survived its 124 cases
(H5, H6, H9), and a fourth, count direction, was frozen this round (H10). Each table below varies exactly **one** of
those four shapes and keeps the other three, so the case that kills H5 is not the case that kills H6. Each fixture
writes its own `$FX/mounts`; `check()` exports it as `TSUKUROI_PROC_MOUNTS="$FX/mounts"`
(`tools/tsukuroi-census.sh:2166`), so the arm reads the fixture and never the host's table.

| Case (`tools/tsukuroi-census.sh` at `568c397`) | Mount table (`$FX/mounts`, one line each) | Expected `STORAGE` line | Frozen mutants it kills |
|---|---|---|---|
| `storage-mounts-mp-relative` (`:3039-3043`)<br>"healthy rollup: a btrfs line whose mountpoint is not absolute still counts, BLOCKED (R41-C1 H5)"<br>*pins: the mountpoint field decides nothing; `/dev` source, `subvolid=5`/`subvol=/` kept* | `proc /proc proc rw,nosuid,nodev,noexec,relatime 0 0`<br>`/dev/vdc1 relative/mnt btrfs rw,relatime,subvolid=5,subvol=/ 0 0` | `STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs` | `H5-mountpoint-absolute`, `M1-VA-device-literal`, `M2-VB-root-mountpoint`, `M4-VG-subvolid-256`, `M8-subvol-at-literal` |
| `storage-mounts-src-uuid` (`:3045-3049`)<br>"healthy rollup: a btrfs line whose source is not under /dev still counts, BLOCKED (R41-C1 H6)"<br>*pins: the source field decides nothing; absolute mountpoint, `subvol=` kept* | `proc /proc proc rw,nosuid,nodev,noexec,relatime 0 0`<br>`UUID=0b1c2d3e-4d5e-6f70-8192-a3b4c5d6e7f8 /data btrfs rw,relatime,subvolid=5,subvol=/ 0 0` | `STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs` | `H6-source-devonly`, `M1-VA-device-literal`, `M2-VB-root-mountpoint`, `M4-VG-subvolid-256`, `M8-subvol-at-literal` |
| `storage-mounts-no-subvol-opt` (`:3051-3055`)<br>"healthy rollup: a btrfs line with no subvol= option still counts, BLOCKED (R41-C1 H9)"<br>*pins: options decide nothing, not even the `subvol=` key* | `proc /proc proc rw,nosuid,nodev,noexec,relatime 0 0`<br>`/dev/sdc1 /mnt/plain btrfs rw,commit=60 0 0` | `STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs` | `H9-subvolkey-option`, `M1-VA-device-literal`, `M2-VB-root-mountpoint`, `M4-VG-subvolid-256`, `M8-subvol-at-literal` |
| `storage-mounts-two-btrfs` (`:3057-3062`)<br>"healthy rollup: two btrfs lines are still btrfs without sysfs, BLOCKED (R41-C1 H10)"<br>*pins: any count ≥ 1, not exactly 1; both lines carry `/dev` source, absolute mountpoints and `subvol=`* | `/dev/nvme0n1p2 / btrfs rw,relatime,ssd,subvolid=256,subvol=/@ 0 0`<br>`proc /proc proc rw,nosuid,nodev,noexec,relatime 0 0`<br>`/dev/nvme0n1p2 /home btrfs rw,relatime,ssd,subvolid=257,subvol=/@home 0 0` | `STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs` | `H10-count-exactly-one`, `M1-VA-device-literal` |

Mutant ids are the counter's own frozen names (`tools/score-selftest-mounts-r41.py:85-104`): H5
`H5-mountpoint-absolute` (counts only when `[[ ${_mp:-} == /* ]]`), H6 `H6-source-devonly` (only when
`[[ ${_src:-} == /dev/* ]]`), H9 `H9-subvolkey-option` (whole-table `*'subvol='*`), H10 `H10-count-exactly-one`
(`if [ "$mt" -eq 1 ]`), beside the round-40 M1-M9. Kills are the receipt's confirmed labels — a stderr `FAIL
<label>` that names a baseline `PASS <label>` and is reproduced in a second run —
`.ufo/waves/round-41/after/c1-after-568c397.jsonl` `mutants.<id>.confirm_labels`. The union of the four Kills cells
is eight of the 13 mutants (M1, M2, M4, M8, H5, H6, H9, H10); the other five are killed by round-40 cases only. No
new case is the only killer of a round-40 M1-M9 mutant: M3 and M5 still die only on
`storage-mounts-btrfs-in-path`, M6 on `storage-mounts-fstype-case`, M7 on `storage-root-unreadable-mounted`, and M9
only on the two round-40 varied tables, so those cases stay load-bearing. What the four add is separation — each
held-out mutant's confirmed FAIL set is exactly one label, its own case — so H5, H6, H9 and H10 are killed by the
table that varies their shape and not by the others.

Counting: `python3 tools/score-selftest-mounts-r41.py --revision <REV> --scratch <DIR> --jobs 4` — 0 when
`baseline_pass == 1 and neutral_pass == 3 and decoy_pass == 1 and mutants_applied == 13 and survivors == 0 and
params == 4` (`tools/score-selftest-mounts-r41.py:295-296`, the same sentence in the round-41 declaration, in the
counter's docstring and in the receipt); 1 otherwise; 2 on revision, git or scratch failure. The counter is frozen at
sha256 `8306d9990b156ceb625eabbe942910fc0d09b20f350a7e8af1ff2237fd07355c` (`sha256sum`; identical at the freeze commit
`e479fdc5`). Measured at `568c397`: baseline `PASS (128 cases, 128 passed, 0 failed)`, `capture_pass 1`, neutral 3/3,
decoy 1, mutants applied 13, survivors 0, params 4, exit 0 — 6 min 21 s at `--jobs 6` on a loaded host
(17:17:35Z–17:23:56Z). An independent rerun at the same revision (`.ufo/waves/round-41/w1/C1ExecRerun/`,
`field-compare.json`) reproduces every predicate field and every per-mutant confirmed label. At the base `0e5805a1`:
baseline `PASS (124 cases, 124 passed, 0 failed)`, survivors 4 (H5, H6, H9, H10), params 0, exit 1. One run is 19
selftests (baseline, capture, 13 mutants, 3 neutrals, decoy) plus one
confirmation run per attributed kill and one serial retry for any failed non-mutant run, so run it at most once per
item.

The `params` conjunct is a table-shape gate, not a behaviour test: the counter injects one `cp` into `check()` in its
private copy, captures each case's `$FX/mounts` beside its label and wanted patterns
(`tools/score-selftest-mounts-r41.py:115-117`), and requires a PASSing baseline case for each of the four declared
properties whose wanted patterns include `detail=mounts:btrfs-without-sysfs` (`:162-188`). The receipt records the
mapping (`param_cases`: P1→H5, P2→H6, P3→H9, P4→H10 labels). Dropping the H9 case from the candidate drops it to
`params 3` with `survivors 1` H9 (`.ufo/waves/round-41/controls/C1-K2-candidate-without-H9-case.jsonl`).

### What the decoy refuses, and what it does not

The one DECOY variant is the unmutated selftest with a dead here-document, `: <<'R41DECOY' … R41DECOY`, inserted in
front of the count loop **inside `probe_storage_arm`** in the counter's copy; the body carries every mutant's
replacement text verbatim (`tools/score-selftest-mounts-r41.py:114-127`). Its behaviour is the base arm's, so the
decoy must PASS (measured: 128/128). A selftest that reads its own text for any of those 13 strings — through
`declare -f probe_storage_arm`, `${0}`, `${BASH_ARGV0}` or `/proc/self/…` — fails it; that is the round-40
R40-ANSWER-KEY prologue, refused by construction (pre-data controls K1 and K3: `decoy_pass 0` on the base and on the
candidate). It does **not** refuse a self-reader that strips here-documents before matching (recorded limit; wave item
C1CritDecoy attacks it), nor one keyed on anything outside those 13 strings — the fixture tables, the four new case
labels and the expected regexes are not in the decoy body — nor a reader that keys on the census file's other text.

### What kill attribution refuses, and what it does not

A mutant counts as killed only when its run exits nonzero, prints the FAIL summary with the baseline's case count
(128), has at least one stderr `FAIL <label>` naming a label the baseline printed as `PASS <label>`, and a second run
fails at least one of the same labels (`tools/score-selftest-mounts-r41.py:190-202`, `:264-271`). Refused: a bare
nonzero exit, an early abort (no case count, or a different one — adding or losing a case invalidates every kill), a
summary-only failure, a FAIL label the baseline never passed, and a failure that does not reproduce. The receipt now
carries stderr labels, not counts (`first_fails`, the raw `FAIL …` lines, first three per run, `:159`), which closes the
round-40 "receipt carries counts, not labels" gap. It does **not** refuse an unrelated baseline label that fails
reproducibly twice: the receipt's first runs carry host-flake labels — `hostname override not honoured — possible host
read` on M2, M4, M5, M9 and H9 — which dropped out of the confirmed intersection here, but a flake confirmed twice
would be counted as a kill. Nor does it show causation: the rule proves the variant's run differs reproducibly at a
baseline case, not that the new table produced the difference.

### Limits of these four cases

- **H5's table is a shape the kernel does not print.** Measured in a private user namespace: `mount(2)` with a
  relative target stores the mountpoint absolute — `/proc/self/mounts` then reads
  `relative-source /fast/scratch/hyaku/tsukuroi-r41/C1ScribeSkill/tgt1 tmpfs rw,relatime,uid=1000,gid=1000,inode64,huge=advise 0 0`.
  So a relative mountpoint is forged input for any fstype, and H5 pins the arm's contract over an overridable file
  (`TSUKUROI_PROC_MOUNTS`, `tools/tsukuroi-census.sh:463`), not a live-host exposure.
- **H6's shape is representable but unobserved.** The same measurement shows the source field is stored verbatim
  (`UUID=0b1c2d3e-4d5e-6f70-8192-a3b4c5d6e7f8` prints as given), so a non-`/dev` source is not a field the format
  forbids; whether a real btrfs line ever carries one was not observed here — no btrfs mount was made (the host is
  read-only to this lane, and the measurement namespace held no block device). This host's table reads four btrfs lines, all
  `/dev/mapper/root`, all absolute mountpoints, all with `subvol=` (`awk '$3=="btrfs"' /proc/self/mounts`, 2026-10-26).
- **Live coverage is uneven.** H10's property is on this host today (four btrfs
  lines), so `mt -eq 1` answers false on this table — a live bug class whenever the sysfs root is absent or
  hidden, the only branch that reads the table; H9's — a btrfs mounted on its default subvolume, with no `subvol=`
  option — is a normal kernel shape this host does not show [inference: not mounted here].
- **Mutant sample, not proof of immunity.** The 13 mutants all rewrite the mount-table cross-check of the round-39
  rule. The sysfs walk, the five-counter parser, `bad-devid`, `no-devinfo` and the `root:unreadable` path carry no
  mutant here, and `survivors == 0` means 0 of these 13, never "no literal-keyed arm can pass".
- **`params` is a shape gate.** It checks that a passing case handed `check()` a table with the property and wanted a
  `detail=mounts:btrfs-without-sysfs` line; a selftest that hands those tables and hardcodes the answers elsewhere
  still scores 4. Removing a case is caught; faking a table is not.
- **One line shape per case.** No fixture holds a non-`/dev` source *and* two btrfs lines, a mountpoint with an
  escaped space (`\040`), a field count other than the six `mount` prints, or a btrfs line in a table whose sysfs root
  already has fsid entries (that guard is `storage-root-unreadable-mounted`).
- **Fixtures only.** All four tables are override files; no run reads the host's table, so this section says nothing
  new about the live host.
- **bash only.** `[[ ]]`, `${fst,,}` and `case` globbing are bash semantics (GNU bash `5.3.20` here).
````
