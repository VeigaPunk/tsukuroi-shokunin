# C1CritParams receipts (scratch /fast/scratch/hyaku/tsukuroi-r41/C1CritParams, removed)

## variant baseline selftest
TSUKUROI_CENSUS_SELFTEST: PASS (128 cases, 128 passed, 0 failed)
rc from run: 0

## direct mutant runs on the variant (mut.py, frozen MUTANTS texts applied to the variant file)
H5-mountpoint-absolute: rc=0 TSUKUROI_CENSUS_SELFTEST: PASS (128 cases, 128 passed, 0 failed)
H6-source-devonly: rc=0 TSUKUROI_CENSUS_SELFTEST: PASS (128 cases, 128 passed, 0 failed)
H9-subvolkey-option: rc=0 TSUKUROI_CENSUS_SELFTEST: PASS (128 cases, 128 passed, 0 failed)
H10-count-exactly-one: rc=0 TSUKUROI_CENSUS_SELFTEST: PASS (128 cases, 128 passed, 0 failed)
M1-VA-device-literal: rc=1 TSUKUROI_CENSUS_SELFTEST: FAIL (128 cases, 126 passed, 2 failed)
  (H5 run re-executed manually: rc=0, 131 stdout lines, 0 stderr)

## capture-line differential (plain vs injected, original census at 71851d63)
plain:    rc=0 TSUKUROI_CENSUS_SELFTEST: PASS (128 cases, 128 passed, 0 failed) pass-labels=128 fail-labels=0
injected: rc=0 TSUKUROI_CENSUS_SELFTEST: PASS (128 cases, 128 passed, 0 failed) pass-labels=128 fail-labels=0
SAME (ordered PASS label lists and FAIL sets identical)
capture files: 125 .args / 123 .mounts (125 check() calls; FIFO and removed-mounts cases have no .mounts)

## FIFO probe
[ -f fifo ] -> F-FALSE ; { [ -f fifo ] && cp -- fifo out.mounts; } 2>/dev/null || true -> group-continued rc=0

## params_from_capture unit probe (label-only and ABSENT-only mentions)
P1 credited from the LABEL text alone (no regex): 'healthy: sysfs root present, detail=mounts:btrfs-without-sysfs never asserted'
P2 credited from an ABSENT (must-not-match) pattern: 'ABSENT:detail=mounts:btrfs-without-sysfs'

## counter score of the variant (fc74df4)
revision fc74df417e009dfea1b45dccad9c976596ddd7d7
baseline TSUKUROI_CENSUS_SELFTEST: PASS (128 cases, 128 passed, 0 failed)
capture_pass 1
neutral_pass 3
decoy_pass 1
mutants_applied 13
survivors 4 ['H10-count-exactly-one', 'H5-mountpoint-absolute', 'H6-source-devonly', 'H9-subvolkey-option']
params 4
result FAIL exit 1
param_cases {"P1-mountpoint-not-absolute": ["healthy: a populated sysfs root is read and the mount table adds nothing (variant P1 table)"], "P2-source-not-dev": ["healthy: a populated sysfs root is read and the mount table adds nothing (variant P2 table)"], "P3-no-subvol-option": ["healthy: a populated sysfs root is read and the mount table adds nothing (variant P3 table)"], "P4-two-btrfs-lines": ["healthy: a populated sysfs root is read and the mount table adds nothing (variant P4 table)"]}
mutant killed flags {'M1-VA-device-literal': True, 'M2-VB-root-mountpoint': True, 'M3-VC-substring-btrfs': True, 'M4-VG-subvolid-256': True, 'M5-a-grep-count': True, 'M6-b-fstype-casefold': True, 'M7-e-guard-drops-blocked': True, 'M8-subvol-at-literal': True, 'M9-last-line-only': True, 'H5-mountpoint-absolute': False, 'H6-source-devonly': False, 'H9-subvolkey-option': False, 'H10-count-exactly-one': False}

## detail-free genuine-kill direction
detailfree baseline: rc=0 TSUKUROI_CENSUS_SELFTEST: PASS (128 cases, 128 passed, 0 failed)
detailfree + H5:     rc=1 TSUKUROI_CENSUS_SELFTEST: FAIL (128 cases, 127 passed, 1 failed); FAIL label = the mp-relative case
params_from_capture on that case's .args/.mounts: mount_props P1=True; credited P1=[] (no WANT_BLOCK outside the label)

## nounset caveat
bash -c 'set -euo pipefail; { printf "%s\n" "$UNDEF" > /dev/null; } 2>/dev/null || true; echo continued' -> outer=1 (no 'continued'): an unset R41_CAP aborts the suite
