VERDICT: draft

Item C1-13 — append-only `SKILL.md` section `## Storage arm selftest literal variation — round 40`. Drafted, **not applied**: no lane file was edited, no git/jj mutation, no host mutation. Report + two receipts only.

## Evidence (all runs read-only; scratch `/fast/scratch/hyaku/tsukuroi-r40/C1ScribeSkill`, removed at end)

| Claim in the draft | Evidence | Observed |
|---|---|---|
| implementation commit changes only `run_selftest` | `git diff --stat 53b294a274656be6479aadf2ec2fee890ded77ce c707e356c2911646f7304d706eb77d118e510610 -- tools/tsukuroi-census.sh` | `1 file changed, 36 insertions(+)`; single hunk `@@ -3008,0 +3009,36 @@`; zero deletions → `probe_storage_arm` (`tools/tsukuroi-census.sh:1865-1925` at that revision) untouched |
| census blob has not moved since | `git rev-parse c707e35:tools/tsukuroi-census.sh HEAD:tools/tsukuroi-census.sh` | both `16438ee189cc359b6d4dc7e7ce171eea371c25e3` (HEAD = `f951f288483c1af0cef4afd458488b84cf7a2165`) |
| selftest 119 → 124 cases | before receipt `.ufo/waves/round-40/before/c1-before.jsonl` record 3; after `.ufo/waves/round-40/after/c1-after-c707e35.jsonl` record 1 | base `53b294a2`: `PASS (119 cases, 119 passed, 0 failed)`; `c707e35`: `PASS (124 cases, 124 passed, 0 failed)` |
| counter PASS at `c707e35` | own run, `python3 tools/score-selftest-literals-r40.py --revision c707e356c2911646f7304d706eb77d118e510610 --scratch /fast/scratch/hyaku/tsukuroi-r40/C1ScribeSkill/counter --jobs 2` | `EXIT=0`, `c707e35 … PASS (124 cases, 124 passed, 0 failed) | bp 1 neu 3 appl 9 surv 0 selfref 5 | PASS exit 0` (receipt `C1ScribeSkill/counter-mine.json`) |
| before = FAIL with 9 survivors | `.ufo/waves/round-40/before/c1-before.jsonl` | `baseline_pass 1, neutral_pass 3, mutants_applied 9, survivors 9, selfref 5`, all nine `killed: false`, `FAIL exit 1` |
| five fixtures, block anchors, mount tables, expected lines | `git show c707e35:tools/tsukuroi-census.sh` read at `:3009-3044` | blocks `:3011-3016`, `:3018-3024`, `:3026-3030`, `:3032-3035`, `:3037-3043`; labels and `check` expectations quoted verbatim in the draft |
| fixtures are wired through the override | `tools/tsukuroi-census.sh:2166` in `check()` | `TSUKUROI_PROC_MOUNTS="$FX/mounts" \` |
| per-case kill attribution | own harness: counter's frozen `MUTANTS`/`NEUTRAL` tables loaded from `tools/score-selftest-literals-r40.py` (import, tables `:68-89`), each `old` applied once to `git show c707e35:…`, `bash copy --selftest` with `TMPDIR` in scratch and cwd `/`, stderr `^FAIL ` captured | M1→{varied-home, varied-multi}; M2→{same two}; M3→{btrfs-in-path}; M4→{varied-home, varied-multi}; M5→{btrfs-in-path}; M6→{fstype-case}; M7→{root-unreadable-mounted}; M8→{varied-home, varied-multi}; M9→{varied-home, varied-multi}; per-mutant failed-case counts 2,2,1,2,1,1,1,2,2 = the receipt's |
| equivalent mutant survives, as expected | same harness, `$fsn`→`$devn` in the guard | `E1-guard-fsn-to-devn: exit=0 … PASS (124 cases, 124 passed, 0 failed)`; neutral rewrites N1–N3 also `PASS 124/124` |
| why the receipt has no labels | `tools/score-selftest-literals-r40.py:106` scans **stdout** for `^FAIL `; `tools/tsukuroi-census.sh:2019` `bad()` writes `FAIL %s` to **stderr** | every `first_fails` in both receipts is `[]` — counts only |
| bash used | `bash --version` | `GNU bash, version 5.3.20(1)-release` |

Finding (recorded, not a defect against the claim): the frozen counter cannot attribute a kill to a case — `first_fails` is structurally empty. The claim's predicate only needs counts, so the section states this limit rather than implying the receipt carries labels.

Gates run by this seat: the frozen C1 counter at `c707e35` (exit 0) and the ten-variant mapping harness. Nothing else was run; no live census, no lane gate. Tooling: no installs, no upgrades, no pacman transaction.

Touched surfaces: `SKILL.md` **not** touched; `.ufo/waves/round-40/w1/C1ScribeSkill/.md` (this report), `.ufo/waves/round-40/w1/C1ScribeSkill/counter-mine.json`, `.ufo/waves/round-40/w1/C1ScribeSkill/mutant-case-map.json`. Out of scope and untouched: the census, the counter, SCORECARD/LOG, knowledge entries, git/jj state, host.

## Exact proposed text (append after `SKILL.md:3324`; file blob unchanged since the declaration commit `758a4b08` — `git diff --stat 758a4b08 HEAD -- SKILL.md` is empty; 74 lines, sha256 of the block (`blk+"\n"`) `c90102d004b9ef52960ee4fe4805f6ba0de7c8353612308a65f0b855495a4837`, one new `##` heading, no earlier line moved; the block contains no triple-backtick fence)

````markdown
## Storage arm selftest literal variation — round 40

Appended 2026-10-26 (round-40 C1, commit `c707e356c2911646f7304d706eb77d118e510610`). Append-only: the round-38
and round-39 storage-arm sections above stay as written, and the arm itself — `probe_storage_arm`,
`tools/tsukuroi-census.sh:1865-1925` — is untouched. The commit is `1 file changed, 36 insertions(+)` in
`run_selftest` only (`git diff --stat 53b294a2 c707e35 -- tools/tsukuroi-census.sh`), so no earlier label or expected
line moved and the selftest count goes 119 → 124 (`PASS (124 cases, 124 passed, 0 failed)`).

Round 39 closed R38-ABSENT-ROOT but left R39-FIXTURE-MONOCULTURE: every "btrfs mounted" fixture in that selftest was
the one string `/dev/mapper/root / btrfs rw,noatime,subvolid=256,subvol=/@ 0 0`, so any arm keyed on a literal of it
passed 117/117 (`.ufo/waves/round-39/w1/C1CritControl.md` VA, VB, VC, VG; `C1MutParse.md` (a), (b);
`C1MutCrossCheck.md` (e)). The five cases below vary the btrfs line itself — device, mountpoint, options, subvolume,
its position in the table and the case of the fstype field — and add one unlistable root with btrfs mounted. Each
fixture writes its own `$FX/mounts`; `check()` exports it as `TSUKUROI_PROC_MOUNTS="$FX/mounts"`
(`tools/tsukuroi-census.sh:2166`), so the arm's mount-table cross-check reads the fixture, never the host's table.

| Case (`tools/tsukuroi-census.sh`) | Mount table (`$FX/mounts`, one line each) | Expected `STORAGE` line | Frozen mutants it kills |
|---|---|---|---|
| `storage-mounts-varied-home` (`:3011-3016`)<br>"a btrfs /home on another device and options, not last, is BLOCKED (R40-C1)"<br>*pins: device, mountpoint, option order, `subvolid=5`/`subvol=/`, middle position* | `proc /proc proc rw,nosuid,nodev,noexec,relatime 0 0`<br>`/dev/nvme0n1p3 /home btrfs rw,relatime,ssd,discard=async,space_cache=v2,subvolid=5,subvol=/ 0 0`<br>`tmpfs /tmp tmpfs rw,nosuid,nodev 0 0` | `STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs` | M1, M2, M4, M8, M9 |
| `storage-mounts-varied-multi` (`:3018-3024`)<br>"one read-only btrfs mount among four lines, empty root, is BLOCKED (R40-C1)"<br>*pins: `ro`, `compress=zstd:3`, named subvolume `/machines`, 4-line table, not root; root holds only `features`* | `sysfs /sys sysfs rw,nosuid,nodev,noexec,relatime 0 0`<br>`UUID=0b1c /boot vfat rw,relatime 0 0`<br>`/dev/sda2 /var/lib/machines btrfs ro,noatime,compress=zstd:3,subvolid=263,subvol=/machines 0 0`<br>`/dev/sdb1 /srv ext4 rw,relatime 0 0` | `STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs` | M1, M2, M4, M8, M9 |
| `storage-mounts-btrfs-in-path` (`:3026-3030`)<br>"btrfs in the device, mountpoint or options of an ext4 line is no btrfs mount (R40-C1)"<br>*pins: only the fstype field decides* | `proc /proc proc rw 0 0`<br>`/dev/disk/by-label/btrfs-old /mnt/btrfs-backup ext4 rw,relatime,comment=btrfs 0 0` | `STORAGE btrfs-device-stats state=HEALTHY filesystems=0 devices=0 nonzero=0` (no `detail`) | M3, M5 |
| `storage-mounts-fstype-case` (`:3032-3035`)<br>"the fstype match is exact, so BTRFS is not btrfs (R40-C1)"<br>*pins: case-sensitive field equality* | `proc /proc proc rw 0 0`<br>`/dev/fx0 / BTRFS rw,relatime 0 0` | `STORAGE btrfs-device-stats state=HEALTHY filesystems=0 devices=0 nonzero=0` (no `detail`) | M6 |
| `storage-root-unreadable-mounted` (`:3037-3043`)<br>"an unlistable root keeps its one reason; the mount table is never added (R40-C1)"<br>*pins: guard order — an already-BLOCKED root never consults the table, one reason only* | `proc /proc proc rw 0 0`<br>`/dev/vdb /data btrfs rw,relatime,subvolid=5,subvol=/ 0 0`<br>root `$FX/btrfs` holds one device `devinfo/1/error_stats` of five zero counters, then `chmod 000 "$FX/btrfs"` | `STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=root:unreadable` | M7 |

Mutant ids are the counter's own frozen names (`tools/score-selftest-literals-r40.py:68-81`): M1
`M1-VA-device-literal` (`*'/dev/mapper/root'*`), M2 `M2-VB-root-mountpoint` (`*' / btrfs '*`), M3
`M3-VC-substring-btrfs` (`*btrfs*`), M4 `M4-VG-subvolid-256`, M5 `M5-a-grep-count` (`grep -c btrfs`), M6
`M6-b-fstype-casefold` (`${fst,,}`), M7 `M7-e-guard-drops-blocked` (the guard loses `&& [ "$blocked" -eq 0 ]`), M8
`M8-subvol-at-literal` (`subvol=/@`), M9 `M9-last-line-only` (`tail -n 1`). The Kills column's union is all nine; three
cases are each the only killer of something — `btrfs-in-path` kills M3 and M5, `fstype-case` kills M6,
`root-unreadable-mounted` kills M7 — while the two varied cases kill five each, because both put btrfs on a non-root
mountpoint of a device other than `/dev/mapper/root` with `subvol=/` or a named subvolume.

Counting: `python3 tools/score-selftest-literals-r40.py --revision <REV> --scratch <DIR> --jobs 2` — 0 when
`baseline_pass == 1 and neutral_pass == 3 and mutants_applied == 9 and survivors == 0 and selfref == 5`
(`tools/score-selftest-literals-r40.py:28-29`; the same sentence is in the round-40 declaration and in the receipt);
1 otherwise; 2 on revision, git or scratch failure. A mutant is applied only when its exact `old` substring occurs
once, the three neutral rewrites N1–N3 must PASS inside the same run (so a selftest keyed on the arm's own text fails
them), and `selfref` must stay 5. Measured at `c707e35`: baseline `PASS (124 cases, 124 passed, 0 failed)`, neutral
3/3, mutants applied 9/9, survivors 0, selfref 5, exit 0 (`.ufo/waves/round-40/after/c1-after-c707e35.jsonl`; per-mutant
failed-case counts 2,2,1,2,1,1,1,2,2). At the base `53b294a2`: baseline `PASS (119 cases, 119 passed, 0 failed)`,
survivors 9, exit 1 (`.ufo/waves/round-40/before/c1-before.jsonl`).

Equivalent mutant, excluded and named in the counter (`:23-25`): the guard `$fsn` → `$devn`
(`if [ "$devn" -eq 0 ] && [ "$blocked" -eq 0 ]`, round-39 `C1MutCrossCheck` (d)). `devn > 0` implies `fsn > 0`, since a
device is counted only inside an fsid directory, and `fsn > 0` with `devn == 0` sets `blocked=1` (`no-devinfo`) before
the guard — so no fixture can kill it. Applied anyway at `c707e35` it still prints `PASS (124 cases, 124 passed,
0 failed)`: the expected result for an equivalent mutant, not a survivor.

### Limits of these five cases

- **Mutant sample, not proof of immunity.** All nine mutants rewrite one thing, the mount-table cross-check of the
  round-39 rule. The sysfs walk, the five-counter parser, `bad-devid`, `no-devinfo` and the `root:unreadable` paths
  carry no mutant here, and a literal the fixtures happen to share (`ssd`, `space_cache=v2`, `rw,relatime`) is
  unprobed. `survivors == 0` means 0 of these nine, never "no literal-keyed arm can pass".
- **Fixtures and mutants were written in the same round.** A mutant the author did not imagine stays invisible; the
  sample is nine arms carried from round 39, three neutral rewrites and one excluded equivalent.
- **`BTRFS` is a forged input, not a host shape.** Linux reports this field lower-case, so `storage-mounts-fstype-case`
  pins exact-match semantics against a table the kernel will not produce; the `comment=btrfs` option and the
  `/dev/disk/by-label/btrfs-old` device name in `btrfs-in-path` are forged too. These cases prove that only the third
  field decides — not that a real host ever shows such a line, and not what the arm would do with another spelling.
- **One line shape per case.** No fixture holds two btrfs mounts, a mountpoint with an escaped space (`\040`), a field
  count other than the six `mount` prints, or a btrfs line in a table whose root already has fsid entries. Position is
  varied only within 3–4 line tables.
- **Fixtures only.** All five tables are override files; no run reads the host's table, so this section says nothing
  new about the live host (round 39's live reading stands).
- **The receipt carries counts, not labels.** The counter scans stdout for `^FAIL `
  (`tools/score-selftest-literals-r40.py:106`) while the selftest's `bad()` writes `FAIL <label>` to stderr
  (`tools/tsukuroi-census.sh:2019`), so every `first_fails` is empty. The Kills column was measured by applying the
  counter's own frozen `MUTANTS`/`NEUTRAL` tables to `git show c707e35:tools/tsukuroi-census.sh`, running each variant
  `--selftest` and capturing stderr; the per-mutant failing-case counts reproduce the receipt's. Re-derive a row the
  same way, or delete one case block on a scratch clone and watch which mutants survive.
- **bash only.** The selftest runs under GNU bash (`5.3.20` here); `[[ ]]`, `${fst,,}` and `case` globbing are bash
  semantics, so N2 and M6 are bash-specific.
````

Artifacts: `.ufo/waves/round-40/w1/C1ScribeSkill.md` (this report),
`.ufo/waves/round-40/w1/C1ScribeSkill/counter-mine.json` (own counter run at `c707e35`),
`.ufo/waves/round-40/w1/C1ScribeSkill/mutant-case-map.json` (per-mutant exit, last line, killed case labels for all 9 mutants, 3 neutrals and E1). Scratch removed after the copies.
