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
