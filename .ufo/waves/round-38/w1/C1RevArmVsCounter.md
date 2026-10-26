VERDICT: defect-found

# C1-1 — probe_storage_arm (bash) vs expected_from_sysfs (python model): parity audit

Seat: C1RevArmVsCounter · lane round 38 w1 · item C1-1 (coverage, C1, "C1 contract parity").
All bytes measured at the pinned implementation commit 52ffd65f868431f021b8615ab281efd87195eac6;
lane HEAD 5edb6c2e0d0e47b731fb0cb50e5d2df5abb7aacf has byte-identical files:

    $ git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin diff --stat 52ffd65..HEAD -- tools/tsukuroi-census.sh tools/score-storage-arm-r38.py
    (empty output — no changes)
    $ sha256sum tools/score-storage-arm-r38.py   -> e649bfb33ed99161dc3affdacd7fa86fa8d96e2c5bb60b2d22d6fc12a7f82218  (matches declared e649bfb3…)
    $ sha256sum tools/tsukuroi-census.sh         -> 8e0084f67ad4783a980d5c2eaba453f51f1fc5d75408a1c9021a7249ac9aba1c (same at 52ffd65 and HEAD)

Method: for each fixture I built a fake sysfs tree under
/fast/scratch/hyaku/tsukuroi-r38/C1RevArmVsCounter/fx/<case>, ran
`env -i PATH=/usr/bin:/bin LC_ALL=C HOME=<scratch>/home TMPDIR=<scratch>/tmp TSUKUROI_BTRFS_SYSFS=<tree> bash /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/tsukuroi-census.sh | grep '^STORAGE'`
(the counter's own child-env shape, score-storage-arm-r38.py:154-160), and ran the python model
`expected_from_sysfs(<tree>)` loaded from the pinned bytes (importlib on a scratch copy of
score@52ffd65.py; sha256 re-verified e649bfb3…). Both outputs pasted verbatim below. uid=1000 (non-root).
No tool installs were made (nothing to record under the 2026-10-19 tooling authorization).

## The two readers, semantics side by side

bash `probe_storage_arm` — tools/tsukuroi-census.sh:1848-1886 (contract paragraph :350-369):
- fs entries: glob `$root/*`, kept if `[ -e ]` (:1854) and basename matches lowercase-UUID ERE (:1855). Any entry type counts (dir, regular file, symlink-to-something-existing); a broken symlink fails `-e` and is silently skipped.
- devices: glob `$fsd/devinfo/*`, kept if `[ -e ]` (:1858); missing/unsearchable devinfo ⇒ glob literal ⇒ `nd=0` ⇒ BLOCKED `no-devinfo` (:1879).
- error_stats: must be `-f` and `-r` (:1860), else BLOCKED `unreadable`.
- parse: `IFS=' ' read -r k v extra` (:1866) — space is the only delimiter (tab/CR stay inside the token); key must be one of the five, `extra` empty, value `^[0-9]+$` (ASCII only), key unseen (:1867-1869); exactly 5 lines (:1874); a blank line anywhere (including trailing) enters the body with empty key ⇒ malformed.
- nonzero: value not all-zeros (`! [[ $v =~ ^0+$ ]]`), string-compared, no arithmetic on values.

python `expected_from_sysfs` — tools/score-storage-arm-r38.py:112-150:
- fs entries: `sorted(os.listdir(root))` (:118), lowercase-UUID `re.match` (:116); any entry type counts, including broken symlinks.
- devices: `os.listdir(devinfo) if os.path.isdir(devinfo) else []` (:123) — every listed name counts as a device (:129), including broken symlinks.
- error_stats: `open(f).read()` (:131), any `OSError` ⇒ BLOCKED (:132-133).
- parse: `text.splitlines()` (:137) — splits on `\r\n`, lone `\r`, `\v`, `\f`, `\x85`, U+2028/9 as well as `\n`; `line.split()` — any whitespace run, tabs included; value `.isdigit()` (:139) — True for non-ASCII digits ('٥', '²') — then `int(parts[1])` (:142) — accepts '+5' never (isdigit gate), accepts '٥' (=5), raises ValueError on '²'.
- nonzero: `int(v) > 0` (:146).

Structural fact that bounds the impact: the counter's fixture leg compares the census line against
hardcoded per-fixture expectations (`ok = got == exp`, score-storage-arm-r38.py:214, expectations from
FIXTURES :71-92), NOT against expected_from_sysfs; the model is used only for the live leg against
/sys/fs/btrfs (:223,227). So a census↔model disagreement cannot flip `fixtures_matched`; it can only
matter if such an input appeared in the live sysfs.

## Fixture matrix — both outputs verbatim (receipts: .ufo/waves/round-38/w1/C1RevArmVsCounter/out/<case>.txt)

| # | case | census STORAGE line (grep '^STORAGE') | model expected_from_sysfs | verdict |
|---|------|---------------------------------------|---------------------------|---------|
| fx01 | non-directory devinfo entry (`devinfo/1` regular file) | `STORAGE btrfs-device-stats state=BLOCKED filesystems=1 devices=1 nonzero=0 detail=11111111:1:unreadable` | `["BLOCKED", 1, 1, 0]` | MATCH |
| fx02 | UUID-named regular file as fs entry | `STORAGE btrfs-device-stats state=BLOCKED filesystems=1 devices=0 nonzero=0 detail=11111111:-:no-devinfo` | `["BLOCKED", 1, 0, 0]` | MATCH |
| fx03 | CRLF line endings, five zero counters | `STORAGE btrfs-device-stats state=BLOCKED filesystems=1 devices=1 nonzero=0 detail=11111111:1:malformed` | `["HEALTHY", 1, 1, 0]` | **DIVERGE** |
| fx04 | blank trailing line | `STORAGE btrfs-device-stats state=BLOCKED filesystems=1 devices=1 nonzero=0 detail=11111111:1:malformed` | `["BLOCKED", 1, 1, 0]` | MATCH |
| fx05 | value with '+' (`write_errs +5`) | `STORAGE btrfs-device-stats state=BLOCKED filesystems=1 devices=1 nonzero=0 detail=11111111:1:malformed` | `["BLOCKED", 1, 1, 0]` | MATCH |
| fx06 | huge value (generation_errs=18446744073709551616 = 2^64) | `STORAGE btrfs-device-stats state=DEGRADED filesystems=1 devices=1 nonzero=1 detail=11111111:1:generation_errs=18446744073709551616` | `["DEGRADED", 1, 1, 1]` | MATCH |
| fx07 | symlinked device → valid dir with error_stats | `STORAGE btrfs-device-stats state=HEALTHY filesystems=1 devices=1 nonzero=0` | `["HEALTHY", 1, 1, 0]` | MATCH |
| fx08 | symlinked device → broken target | `STORAGE btrfs-device-stats state=BLOCKED filesystems=1 devices=0 nonzero=0 detail=11111111:-:no-devinfo` | `["BLOCKED", 1, 1, 0]` | **DIVERGE** (devices 0 vs 1) |
| fx09 | tab-separated counters (`write_errs\t0` …) | `STORAGE btrfs-device-stats state=BLOCKED filesystems=1 devices=1 nonzero=0 detail=11111111:1:malformed` | `["HEALTHY", 1, 1, 0]` | **DIVERGE** |
| fx10 | non-ASCII digit value (`read_errs ٥` = Arabic-Indic 5) | `STORAGE btrfs-device-stats state=BLOCKED filesystems=1 devices=1 nonzero=0 detail=11111111:1:malformed` | `["DEGRADED", 1, 1, 1]` | **DIVERGE** |
| fx11 | value '²' (isdigit-true, int()-invalid) | `STORAGE btrfs-device-stats state=BLOCKED filesystems=1 devices=1 nonzero=0 detail=11111111:1:malformed` | **model crashes**: `ValueError: invalid literal for int() with base 10: '²'` (uncaught, score-storage-arm-r38.py:142) | **DIVERGE** (model crash) |
| fx12 | UUID-named broken symlink as fs entry | `STORAGE btrfs-device-stats state=HEALTHY filesystems=0 devices=0 nonzero=0` | `["BLOCKED", 1, 0, 0]` | **DIVERGE** |
| fx13 | sysfs root mode 000 (uid 1000) | `STORAGE btrfs-device-stats state=HEALTHY filesystems=0 devices=0 nonzero=0` | **model crashes**: `PermissionError: [Errno 13] Permission denied: '…/fx13-root-unreadable'` (uncaught os.listdir, :118) | **DIVERGE** (model crash) |
| fx14 | lone CR as line separator | `STORAGE btrfs-device-stats state=BLOCKED filesystems=1 devices=1 nonzero=0 detail=11111111:1:malformed` | `["HEALTHY", 1, 1, 0]` | **DIVERGE** |
| fx15 | error_stats is a FIFO | `STORAGE btrfs-device-stats state=BLOCKED filesystems=1 devices=1 nonzero=0 detail=11111111:1:unreadable` | **model hangs**: no output, killed by `timeout 10` (blocks in `open(f)`, :131) | **DIVERGE** (model hang) |
| fx16 | no trailing newline on last line | `STORAGE btrfs-device-stats state=HEALTHY filesystems=1 devices=1 nonzero=0` | `["HEALTHY", 1, 1, 0]` | MATCH |
| fx17 | fs dir named `<UUID>\n` (trailing newline in name) | `STORAGE btrfs-device-stats state=HEALTHY filesystems=0 devices=0 nonzero=0` | `["BLOCKED", 1, 0, 0]` | **DIVERGE** (python `$` matches before a trailing newline; bash ERE `$` does not) |
| fx18 | empty error_stats file | `STORAGE btrfs-device-stats state=BLOCKED filesystems=1 devices=1 nonzero=0 detail=11111111:1:malformed` | `["BLOCKED", 1, 1, 0]` | MATCH |
| fx19 | error_stats is a directory | `STORAGE btrfs-device-stats state=BLOCKED filesystems=1 devices=1 nonzero=0 detail=11111111:1:unreadable` | `["BLOCKED", 1, 1, 0]` | MATCH |
| fx20 | uppercase UUID fs name | `STORAGE btrfs-device-stats state=HEALTHY filesystems=0 devices=0 nonzero=0` | `["HEALTHY", 0, 0, 0]` | MATCH |

Runner output shape (every case): `{"model": […], "census_fields": […], "verdict": "MATCH|DIVERGE"}`;
crash cases print `{"model": null, "model_error": …}`; fx15 printed nothing (killed). Raw per-case
transcripts kept as receipts.

## The disagreement list (10 classes)

1. **CRLF endings** (fx03): census BLOCKED (value token `0\r` fails `^[0-9]+$`, :1867-1869) vs model HEALTHY (`splitlines` strips `\r\n`, :137). Direction: census stricter.
2. **Tab-separated counters** (fx09): census BLOCKED (tab not in `IFS=' '`, key token becomes `write_errs\t0`) vs model HEALTHY (`split()` splits on tabs). Census stricter.
3. **Lone CR separator** (fx14): census BLOCKED (whole file one line, `extra` non-empty) vs model HEALTHY (`splitlines` splits on `\r`). Census stricter.
4. **Non-ASCII digit value** (fx10): census BLOCKED (`[0-9]` ASCII-only under LC_ALL=C) vs model DEGRADED nonzero=1 (`'٥'.isdigit()` True, `int('٥')=5`). Census stricter.
5. **Value '²'** (fx11): census BLOCKED; model **crashes** — `'²'.isdigit()` True but `int('²')` raises ValueError, uncaught at score-storage-arm-r38.py:142. Strongest defect: the counter's live leg would die (traceback, no JSON verdict) instead of evaluating.
6. **Broken-symlink device entry** (fx08): census devices=0 (`[ -e ]` false ⇒ device skipped ⇒ `no-devinfo`, :1858/:1879) vs model devices=1 (listdir name counted, :123/:129, then open fails ⇒ BLOCKED). Both BLOCKED, `devices` field differs.
7. **UUID-named broken symlink as fs entry** (fx12): census ignores it entirely (`[ -e ]` false, :1854 ⇒ HEALTHY 0/0/0) vs model BLOCKED 1/0/0 (listdir + UUID match, :118/:116). Direction: census lenient, model strict — opposite of 1-4.
8. **fs name with trailing newline** (fx17): census ignores (bash ERE `$` = end of string) vs model counts + BLOCKED (python `$` matches before a final `\n`). Census lenient, model strict.
9. **Unreadable sysfs root** (fx13): census HEALTHY 0/0/0 (`[ -d ]` true, glob fails silently ⇒ no fs counted) vs model **crashes** (uncaught PermissionError from `os.listdir`, :118). On the live leg this means: census prints a line, model dies ⇒ `live_match` cannot be computed.
10. **FIFO error_stats** (fx15): census BLOCKED `unreadable` (`[ -f ]` false, :1860) vs model **hangs forever** in `open()` (:131) — the counter would stall to its 300s subprocess timeout (score-storage-arm-r38.py:160) and then raise TimeoutExpired, uncaught in main's live leg.

Parity confirmed (no divergence) on: non-directory devinfo entry, UUID-named regular file, blank
trailing line, '+' values, huge values (2^64 — string-vs-bignum both count nonzero=1, no octal trap:
'010' handled, selftest tools/tsukuroi-census.sh:2902-2903), valid symlinked device, no-final-newline,
empty stats file, directory-as-error_stats, uppercase UUID ignored.

## Impact on the declared C1 claim

- The fixture leg cannot be flipped by any of the above: it compares against hardcoded expectations (score-storage-arm-r38.py:214), and the 10 FIXTURES (F01-F10, :71-92) contain none of the 10 divergence shapes.
- The live leg reads the real /sys/fs/btrfs, where none of the 10 shapes occurs (kernel-generated ASCII files, `\n` endings, no symlinks/FIFOs, world-readable root) — so `live_match == 1` stands on this host.
- Corroboration (frozen counter re-run by this seat at the pinned revision, scratch copy, observed 2026-10-26): `python3 tools/score-storage-arm-r38.py --repo <lane> --revision 52ffd65f868431f021b8615ab281efd87195eac6 --scratch <scratch>/counter-run` → `exit=0`, `{'result': 'PASS', 'exit': 0, 'fixtures_matched': 10, 'fixtures_expected': 10, 'live_match': 1, 'six_planes_all': 1}`, live leg model `['HEALTHY', 1, 1, 0]` == census `['HEALTHY', 1, 1, 0]` (host has one btrfs fs, one device, all counters zero). Receipt: counter-run/result.json.
- So the declared PASS is not falsified on this host. What IS falsified is total parity of the two readers: on adversarial or corrupted sysfs shapes they disagree in both directions, and the python model has three failure modes the bash arm does not (ValueError crash, PermissionError crash, FIFO hang). If the model is ever promoted to judge non-live trees (as QUALITY 82's production-path counter does for namespace views), these become live defects.

## What I did not do

- Did not run the q82 counter (tools/score-storage-arm-r38-q82.py) — outside this item.
- Did not test error_stats sizes, exotic key spellings beyond the listed classes, or devinfo-symlinked directories ( reasoned parity, unrun).
- Did not verify the counter's behavior as root (uid 1000 only; F10 root caveat is the counter's own, score-storage-arm-r38.py:216-217).

## Receipts

- Per-case transcripts: .ufo/waves/round-38/w1/C1RevArmVsCounter/out/fx01…fx20.txt
- Census stderr per case: .ufo/waves/round-38/w1/C1RevArmVsCounter/err/ (checked empty unless noted)
- Frozen counter re-run: .ufo/waves/round-38/w1/C1RevArmVsCounter/counter-run/result.json
- Scratch /fast/scratch/hyaku/tsukuroi-r38/C1RevArmVsCounter removed at seat end (receipts copied first).
