VERDICT: supports

Item C1-r — non-author structural read of the C1 implementation (`568c397da11339aed65181be598414f268835555`,
census re-read at `20c327b3f1cf96ad1828792c2ae5db71b5fd9ef7`) against base `0e5805a1f149bd2ed9fe0db2e0a832afb034a835`.
All three questions resolve in the claim's favor. This seat does not re-run the counter; the wave finding
(`.ufo/waves/round-41/w1/C1CritDecoy.md`: the frozen predicate is satisfiable by a self-reading selftest) stands —
but the *actual implementation* contains none of the self-reading machinery that makes that counterexample possible.

Method note: read-only lane access only (`git cat-file`/`git show`/`git log`/`git ls-tree`); census blobs extracted to
scratch and compared by sha256/cmp; no selftest or counter execution by this seat. Receipts:
`.ufo/waves/round-41/residual/C1RevDiffRead/` (`receipts.txt` R1–R8, `impl.diff`, `rs.diff`). Scratch
`/fast/scratch/hyaku/tsukuroi-r41/C1RevDiffRead/` removed after copying.

# 1. The added lines are exactly four fixture cases; no new self-reading construct (Q1 — holds)

The commit touches only `tools/tsukuroi-census.sh`, +27/−0 (`git show 568c397d --stat` → `27 insertions(+)`), with a
single hunk `@@ -3034,6 +3034,33 @@`. `run_selftest()` starts at line 1928 in both blobs and ends at 3055 (base) /
3082 (impl); the hunk (base 3034–3039 → impl 3034–3066) lies inside both spans. Extracting the function body with
`awk '/^run_selftest\(\) \{/{f=1} f{print} f&&/^\}$/{exit}'` at both revisions and diffing (receipt `rs.diff`):
**0 deleted lines, 27 added lines** (23 non-blank + 4 blank).

The 27 lines are exactly: 2 comment lines; 4 blocks, each one `case_home='<fixture>'; FX=…; mkdir -p "$FX";
fx_default "$FX"` line, one `printf '%s\n' … > "$FX/mounts"` fixture mount table (2 lines for H5/H6/H9, 3 for H10),
and a 2-line `check '<label>' 0 HEALTHY '^STORAGE btrfs-device-stats state=BLOCKED … detail=mounts:btrfs-without-sysfs$'`
call. Mechanical counts over the added lines: `check` calls = 4 (labels `R41-C1 H5`, `H6`, `H9`, `H10`); `case_home=`
lines = 4 (`storage-mounts-mp-relative`, `-src-uuid`, `-no-subvol-opt`, `-two-btrfs`). Each table carries a non-btrfs
`proc /proc proc …` line alongside the held-out shape (relative mountpoint `relative/mnt`; `UUID=…` source; no
`subvol=`; two btrfs lines), so each case is discriminating against the count-any-btrfs-row blind spot, and each
expectation is a behavioral census output regex, not a source-text assertion.

Self-reading construct scan over the extracted `run_selftest` bodies (grep -cE, base vs impl): `declare -f/-F` 0/0;
`$0` 0/0; `${0}` 0/0; `BASH_SOURCE` 0/0; `BASH_ARGV0` 0/0; `caller` 0/0; `eval` 0/0; `/dev/fd` 0/0; `<<` 1/1 (the
pre-existing fixture here-doc `cat > "$bin/.dispatch" <<'STUB'`, base extraction line 10 — it *writes* a fixture
stub, present at base, zero deletions); `type` 1/1 (`find "$1" -type f`, line 192); `/proc` 6→10, the four new hits
being exactly the four new fixture mount-table strings; `source` 0→1, prose inside the H6 check label ("…whose
source is not under /dev…"). Running the full construct set over the 27 added lines alone gives **0 hits**
(`grep '^+' rs.diff | grep -cE 'declare |compgen |trap |fc |history|local -n|BASH_|caller|\$\{?0\}?|<<|/dev/fd|eval |\. "\$|/\$0'` → 0).

# 2. The after receipt attributes every kill to a real case (Q2 — holds)

`.ufo/waves/round-41/after/c1-after-568c397.jsonl` (receipt 1, revision `568c397d…`, tool_revision `e479fdc5…`,
result PASS/exit 0, baseline `PASS (128 cases, 128 passed, 0 failed)`):

- **H mutants — each names its own R41-C1 case.** `mutants.H5-mountpoint-absolute.confirm_labels` =
  `["healthy rollup: a btrfs line whose mountpoint is not absolute still counts, BLOCKED (R41-C1 H5)"]` (sole
  label); `H6-source-devonly` → the `(R41-C1 H6)` label; `H9-subvolkey-option` → the `(R41-C1 H9)` label;
  `H10-count-exactly-one` → the `(R41-C1 H10)` label. All four: exit 1, `confirmed: true`, `killed: true`, and the
  FAIL line's fixture `root_dir` is the matching new case dir (`…/fx/storage-mounts-mp-relative/root`,
  `-src-uuid`, `-no-subvol-opt`, `-two-btrfs`).
- **M mutants — each names fixture-backed cases.** M1-VA-device-literal (6 labels: varied-home, H5, H6, H9,
  varied-multi, H10), M2-VB-root-mountpoint (5: varied-home, H5, H6, H9, varied-multi), M3-VC-substring-btrfs (1:
  "…ext4 line is no btrfs mount (R40-C1)"), M4-VG-subvolid-256 (5), M5-a-grep-count (1: btrfs-in-path case),
  M6-b-fstype-casefold (1: fstype-case case), M7-e-guard-drops-blocked (1: root-unreadable case),
  M8-subvol-at-literal (5), M9-last-line-only (2: varied-home, varied-multi). Mapping every distinct confirm label
  to its nearest preceding `case_home` in the impl census (awk, receipts R8): all resolve to fixture dirs —
  `storage-mounts-varied-home`, `storage-mounts-varied-multi`, `storage-mounts-btrfs-in-path`,
  `storage-mounts-fstype-case`, `storage-root-unreadable-mounted` (round 40) plus the four new round-41 dirs.
- Consistency: `param_cases` ties each of P1–P4 to exactly one distinct R41-C1 label; baseline case count 128 =
  124 (base census run, per `C1CritDecoy.md` §6) + 4 new `check` calls. Flaky `hostname override not honoured —
  possible host read` FAILs (R32-C1/R12-C1/D05/Qkk labels) appear in some `first_fails` but in **no**
  `confirm_labels` — attribution excluded them.

# 3. probe_storage_arm is byte-identical at base and 20c327b3 (Q3 — holds)

Blob identities (`git cat-file blob <rev>:tools/tsukuroi-census.sh`): base `0e5805a1` = sha256
`032faa8f1c914dd63a1de673aa9ed6767c4bd19cdfc2751ac34331005da45733` (3149 lines); `568c397d` and `20c327b3` = both
`646c84fcdc166dd4f5321a467e60036d785c106f061dd4fa7849424696f9eb95` (3176 lines) — so the census is byte-identical
at the implementation commit and the read revision, and the base→read diff is exactly the hunk in §1. Extracting
`probe_storage_arm` (lines 1865 onward, 61 lines) at base and impl: both sha256
`71e6007e566e1af32feb495e04e4f291c75fdddb2b521d9822b7363fcdf34d56`; `cmp` → ARM-IDENTICAL. This matches
`C1CritDecoy.md`'s independently computed sed-extraction sha256 (`71e6007e…` at `0e5805a1`, `568c397d`, and both of
its variants) — two independent extraction methods, same digest.

# Residual risk / what this seat did not do

- I did not execute the census `--selftest` or the frozen counter; the behavioral claims (four cases pass at
  `568c397d` and fail under each mutant) rest on the frozen after-receipt, which I read and cross-checked
  structurally but did not reproduce. If the receipt itself were fabricated, this read would not catch it; the
  receipt's internal consistency (case counts, fixture root_dirs, param_cases) is what I verified.
- Confirm labels are stderr strings attributed by the counter; the counter's inability to distinguish a fixture
  case from an inline assertion (the C1CritDecoy finding) remains a counter property. This seat's question was
  whether the *implementation* exploits it: it does not — every new case is fixture-driven, and the params in this
  receipt come from four distinct fixture labels (the exact shortcut C1CritDecoy §2 used on its variant is absent
  here).
- `git ls-tree 20c327b3` names blob `dda066f4…` for the census, equal to the impl blob id — one more identity
  cross-check on Q3.
- No lane file modified; no host mutation; no pacman transactions; no tools installed (nothing to record under the
  tooling directive).
