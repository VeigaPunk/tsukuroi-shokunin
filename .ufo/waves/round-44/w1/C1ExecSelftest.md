VERDICT: supports

# C1ExecSelftest — C1-2: census selftest 132 → 141 and the scrub arm's locale invariance

All commands below ran in /fast/scratch/hyaku/tsukuroi-r44/C1ExecSelftest with
`TMPDIR=/fast/scratch/hyaku/tsukuroi-r44/C1ExecSelftest/tmp`; lane reads only. Receipts:
`.ufo/waves/round-44/w1/C1ExecSelftest/`.

## 1. Inputs and identity

```
git -C <lane> show 7e081698d4fc3c4ea944884fd093058de9909de1:tools/tsukuroi-census.sh > impl.sh   # 3396 lines
git -C <lane> show 98020ece0674e0b569ee23aed10ffbee355b248e:tools/tsukuroi-census.sh > base.sh   # 3220 lines
fca419b4714f7d24314b8d5877f0992c7f326aa8ff80045743990d058e8eaa1c  impl.sh
7c9f79036782de951a69325fe6f5cc742d8acac4de389626026bc33d8f7877f9  base.sh
```
Receipt: `sha256-inputs.txt`. Drift check: `git -C <lane> diff --stat 7e0816 HEAD -- tools/tsukuroi-census.sh`
prints nothing (rc 0), so the file is unchanged from the declared implementation commit to the
current lane tip `ff2c264a` — the numbers below hold at tip as well.

## 2. Selftest at both revisions (the 132 → 141 claim)

| script | command | exit | tail line |
|---|---|---|---|
| impl (7e0816) | `bash impl.sh --selftest` | 0 | `TSUKUROI_CENSUS_SELFTEST: PASS (141 cases, 141 passed, 0 failed)` |
| base (98020e) | `bash base.sh --selftest` | 0 | `TSUKUROI_CENSUS_SELFTEST: PASS (132 cases, 132 passed, 0 failed)` |

`grep -c '^PASS ' impl-selftest.log` = 141, `^FAIL ` = 0; `base-selftest.log` = 132 PASS / 0 FAIL.
Delta is exactly the nine R44-C1 cases (141 − 132 = 9). Cross-checks:
`grep -c R44-C1 impl.sh` = 9, `grep -c R44-C1 base.sh` = 0,
`grep -c probe_scrub_record base.sh` = 0, and base contains no `SCRUB_LINE`/`SCRUB ` arm at all.

## 3. The nine `(R44-C1)` labels, with line numbers

Line numbers are in the exported `impl.sh` (7e0816); log lines are from `impl-selftest.log`. Each
label sits on its `check '<label>' <want_rc> <want_verdict> '<SCRUB regex>' [extra regex…]` line
(the regex is on the following line, `r44-labels-impl.txt` has all nine).

| # | impl.sh:line | log line | label (case assertion in brief) |
|---|---|---|---|
| 1 | 3229 | 132 | no record dir, no sysfs root, no wants dir → `state=NONE dir=absent … records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0` |
| 2 | 3236 | 133 | one readable record of a mounted fsid → `RECORDED`, `records=1`; `notes.txt` and `scrub.status.NOT-A-UUID` ignored |
| 3 | 3244 | 134 | 000 record unreadable + record of unmounted fsid orphan + `_tmp` counted apart → `RECORDED records=2 tmp=1 unreadable=1 orphan=1` |
| 4 | 3251 | 135 | nonzero `scrub_speed_max` → `limited=1` and `detail=11111111:2:speed_max=104857600`; `0` is no limit |
| 5 | 3257 | 136 | non-decimal limit BLOCKED + missing limit file unreadable (never no-limit) → `detail=11111111:1:speed-malformed,11111111:3:speed-unreadable` **and** rollup `^TSUKUROI_CENSUS: HEALTHY ` |
| 6 | 3263 | 137 | unlistable record dir → `BLOCKED dir=unreadable detail=dir:unreadable` |
| 7 | 3271 | 138 | timer instances count by link name (`btrfs-scrub@-.timer`, `btrfs-scrub@home.timer` → `timers=2`); bare template and `fstrim.timer` not counted |
| 8 | 3278 | 139 | symlinked record + directory record + non-socket progress → `BLOCKED … detail=progress:not-socket,record:not-regular,record:not-regular`, and a newline-in-filename forgery of `TSUKUROI_CENSUS: HEALTHY (forged)` must be **ABSENT** from output |
| 9 | 3285 | 140 | record with no sysfs root → `BLOCKED dir=present records=1 … detail=sysfs:absent` |

Placement in the emitted report (live fixture run `loc-C.log`): `STORAGE …` at line 11,
`SCRUB …` at line 12, `TSUKUROI_CENSUS: …` at line 13 — after STORAGE, before the rollup, as declared.
Code sites: construction `impl.sh:2036`, call `impl.sh:3375`, print `impl.sh:3376` — i.e. after
`printf '%s\n' "$STORAGE_LINE"` (`impl.sh:3372`) and before the rollup `printf` (`impl.sh:3386`);
contract paragraph "Round-44 addition (C1)" spans `impl.sh:384–409`.

## 4. Locale invariance of the selftest

Five full runs of the same exported file, identical PASS/FAIL case lines (byte-identical after
`grep '^\(PASS\|FAIL\)'`, diffed pairwise):

| env | exit | wall | result |
|---|---|---|---|
| ambient (`LANG=en_US.UTF-8`, `LC_ALL` unset) | 0 | 27.932 s | `PASS (141 cases, 141 passed, 0 failed)` |
| `LANG=LC_ALL=en_US.utf8` | 0 | 27.229 s | 141/141 |
| `LANG=LC_ALL=en_US.UTF-8` | 0 | 30.517 s | 141/141 |
| `LANG=LC_ALL=C` | 0 | 27.743 s | 141/141 |
| `LANG=LC_ALL=C.utf8` | 0 | 31.819 s | 141/141 |

Base for comparison: 33.006 s (`real`, user 2m07.5s, sys 56.1s) — the impl run is not slower per
case; the spread across the five impl runs (27.2–31.8 s) is host load, not locale (same case set,
same PASS lines). `locale -a` here offers only `C C.utf8 en_US.utf8 POSIX`; `en_US.UTF-8` and
`C.UTF-8` resolve to the same charmaps (`LC_ALL=<x> locale charmap` → `UTF-8` for all three
spellings), and I used both spellings of en_US to cover the seat's literal string.

## 5. Detail order does not change with locale — shown, not asserted

The arm pins the locale itself: `impl.sh:1968` `local LC_ALL=C` (first line of `probe_scrub_record`,
declared at `impl.sh:407`: "Globs run under LC_ALL=C, so the detail order is bytewise").

Real census, one fixture with **five** detail entries in two ordering groups
(`mklocfx.sh`: devinfo 1 malformed / 3 unreadable, then `progress:not-socket`, `record:not-regular`,
then the `limited` info group), run under four locale settings:

```
SCRUB btrfs-scrub-record state=BLOCKED dir=present records=2 tmp=1 sockets=0 unreadable=1 orphan=1 limited=1 timers=2 detail=11111111:1:speed-malformed,11111111:3:speed-unreadable,progress:not-socket,record:not-regular,11111111:2:speed_max=104857600
```
Identical, byte for byte, for `LC_ALL=C`, `C.utf8`, `en_US.utf8` **and** `en_US.UTF-8`
(`md5sum` of the SCRUB line = `a858bc22b95b48f102a160c498f6bdb5` in all four; `scrub-lines-by-locale.txt`).
Two-sided control that the locale is really in play: a bare glob in scratch reorders under these
locales — `LC_ALL=C` → `1 10 2 20 Zz az`, `LC_ALL=en_US.utf8` → `1 10 2 20 az Zz` — so bash glob
order does follow `LC_ALL`; the SCRUB line stayed put because the arm's names are
locale-invariant by construction (lowercase-hex UUIDs from the `uuid` regex, decimal devids,
and timer instance names that are only counted, `impl.sh:2027–2031`, never listed).

Pin-removal mutant (`sed '1968d' impl.sh > impl-nopin.sh`, i.e. no `local LC_ALL=C`):
`LC_ALL=C` and `LC_ALL=en_US.utf8` both still emit the *same* SCRUB line as the pinned file
(`diff` empty, receipts `nopin-C.log`, `nopin-en_US.utf8.log`). Read honestly: the pin is
defensive, not load-bearing for the current name space — the fixture cannot make it bite because
no accepted name differs in collation between C and en_US.UTF-8.

Adversarial-locale fixture (`mklocadv.sh`): `scrub_speed_max` containing Arabic-Indic `١٢٣`,
fullwidth `１２３`, mixed `12٣`, and ASCII `4096`; record dir names with multibyte suffixes
(`scrub.status.<uuid>ü`, `scrub.status.Ü<uuid>`, `scrub.énotes`). Under `C`, `C.utf8`, `en_US.utf8`
all three emit, identically (`md5 fea5d1a298d1e45f8a06fd42c9843bf2`):

```
SCRUB btrfs-scrub-record state=BLOCKED dir=present records=1 tmp=0 sockets=0 unreadable=0 orphan=0 limited=1 timers=0 detail=11111111:1:speed-malformed,11111111:2:speed-malformed,11111111:3:speed-malformed,11111111:4:speed_max=4096
```
So `[[ $v =~ ^[0-9]+$ ]]` (impl.sh:1989) does not admit Unicode digits under a UTF-8 locale, and the
multibyte names are neither counted nor echoed (records=1). No `SCRUB`-line or rollup text differs.

## 6. What I did not do

- No shellcheck/bash -n beyond the selftest's own parse; no review of the other twelve planes.
- No legacy non-UTF-8 locale beyond `C`/`POSIX` was installed, so a stateful multibyte locale
  (e.g. `ja_JP.eucJP`) is untested; the arm's inputs are ASCII by regex, and the adversarial
  fixture is the closest available probe.
- Every locale run set both `LANG` and `LC_ALL`; `LANG` alone was not isolated.
- The arm-level runs let all non-scrub planes read the live host read-only (they printed
  `BLOCKED`/`DEGRADED` from real host state); only the three scrub overrides were synthetic, and
  those runs wrote no file — the census's live mode created nothing in `/var/lib/btrfs` or `/etc`.
- No mutation of the nine cases themselves (e.g. deleting one to confirm the counter notices); the
  base-vs-impl delta and the case-by-case PASS lines are the evidence offered.
- Timings are bash wall-clock arithmetic for the locale matrix and `/usr/bin/time`-style `time`
  for the first two runs; treat them as ±10 ms.
- No tool was installed or upgraded for this seat.

Scratch `/fast/scratch/hyaku/tsukuroi-r44/C1ExecSelftest` was removed after the receipts were
copied; no lane tracked file, fleet-root file, PATH directory or host state was touched.
