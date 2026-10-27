VERDICT: supports

# C1ExecFinalSelftest — C1-2 final selftest (round 44 / hyaku run 9, wave w2)

Seat item: export `tools/tsukuroi-census.sh` at measured tip
`8eee79db608b5815c325a5af7cbfdeac50eda9f4` and base
`98020ece0674e0b569ee23aed10ffbee355b248e`; run `--selftest` three times at tip
(expect 148/148), once at base (expect 132); list the R44-C1 labels; check
`LC_ALL=C` vs `en_US.UTF-8` identical. Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.
Scratch: `/fast/scratch/hyaku/tsukuroi-r44/C1ExecFinalSelftest` (`TMPDIR` inside it).
No lane mutation, no git/jj operation in the lane, no service/mount/sysfs write, no
`btrfs scrub`, no pacman/sudo. Only the two assigned paths were written.

## Exports (all runs executed from the exported files, not the worktree)

Exported with `git show <commit>:tools/tsukuroi-census.sh` inside a scratch clone whose
toplevel was asserted (`git rev-parse --show-toplevel` == the scratch clone); the clone's
own HEAD (`0f8c07a5`) was never used as a content source.

| rev | blob | mode | sha256 | lines |
|---|---|---|---|---|
| tip `8eee79db…` | `8a2a665c8c9ac1795ea52819ee565ae4f0b65b00` | 100755 | `2ef86357c14aec3f4346f7ac9013cdda3b399d38bae67f4ca2e286e5a37c4639` | 3441 |
| base `98020ece…` | `18a1db6448358d7ecf4634570fcd2bf075eccb1b` | 100755 | `7c9f79036782de951a69325fe6f5cc742d8acac4de389626026bc33d8f7877f9` | 3220 |

Receipt: `w2/C1ExecFinalSelftest/exports.txt`.

## Results

Tip, three required runs plus one extra, all `TMPDIR=/fast/scratch/.../tmp`, `chmod +x`
exports, cwd in scratch:

| run | rc | final line |
|---|---|---|
| tip-1 | 0 | `TSUKUROI_CENSUS_SELFTEST: PASS (148 cases, 148 passed, 0 failed)` |
| tip-2 | 0 | `… PASS (148 cases, 148 passed, 0 failed)` |
| tip-3 | 0 | `… PASS (148 cases, 148 passed, 0 failed)` |
| tip-4 | 0 | `… PASS (148 cases, 148 passed, 0 failed)` |
| base-1 (`98020ece…`) | 0 | `… PASS (132 cases, 132 passed, 0 failed)` |

- No `FAIL`/`ERROR` line in any run (`grep -nE '^(FAIL|ERROR)'` → empty across all six logs).
- Run-to-run determinism: `cmp` shows `tip-2/3/4` byte-identical to `tip-1`.
- Case totals by independent count: `grep -c '^PASS '` = 148 (tip), 132 (base) — matches the
  reported totals and the declared `132 -> 148`.
- Zero leftover fixture dirs in `$TMPDIR` after every run (`ls -d tmp/tsukuroi-r3-2-selftest.*`
  → 0); the script mints its fixture tree at
  `mktemp -d "${TMPDIR:-/tmp}/tsukuroi-r3-2-selftest.XXXXXX"` (line 2048) and the per-run
  `fx_no_mutation` sweep (line 2241, invoked 2324) asserts the fixture tree is byte-unchanged.
  Nothing was written under `/tmp` (no evidence taken from there).

Receipts: `w2/C1ExecFinalSelftest/run-tip-{1,2,3,4}.txt`, `run-base-98020ece.txt`.

## R44-C1 label list (16 cases; identical set in all four tip runs)

Derived from `grep '^PASS ' … | sed -E 's/^PASS //; s/ \(exit [0-9]+.*$//'` under `LC_ALL=C`:

```
 1 healthy rollup: a non-decimal limit is BLOCKED and a missing limit file is unreadable, never no-limit (R44-C1)
 2 healthy rollup: a symlinked or directory record and a non-socket progress name are BLOCKED; a newline name is never echoed (R44-C1)
 3 healthy rollup: a sysfs root that exists but is not a directory is BLOCKED, never a silent no-orphan scan (R44-C1)
 4 healthy rollup: an empty scrub_speed_max line is malformed, never a silent no-limit (R44-C1)
 5 healthy rollup: an unlistable record directory is BLOCKED, never an absent record (R44-C1)
 6 healthy rollup: detail evidence precedes limit info in the detail join (R44-C1)
 7 healthy rollup: records with no sysfs root to judge orphans by are BLOCKED (R44-C1)
 8 healthy: a 000 record is unreadable, a record of an unmounted fsid is an orphan, a _tmp counts apart (R44-C1)
 9 healthy: a directory named like a scrub timer is not an enabled instance (R44-C1)
10 healthy: a nonzero scrub_speed_max counts as limited and is listed; 0 is no limit (R44-C1)
11 healthy: a zero-padded scrub_speed_max is still no limit (R44-C1)
12 healthy: an in-progress _tmp record alone reads RECORDED with zero finished records (R44-C1)
13 healthy: enabled scrub timer instances count by link name; the bare template and other timers do not (R44-C1)
14 healthy: no record directory, no sysfs root, no wants directory reads NONE with zero counts (R44-C1)
15 healthy: one readable record of a mounted fsid reads RECORDED; other names are ignored (R44-C1)
16 healthy: the probe pins LC_ALL=C so a collation-inflated name is never a uuid (R44-C1)
```

Set arithmetic (`LC_ALL=C comm`, receipts `labels-tip.txt`, `labels-base.txt`,
`labels-added-at-tip.txt`, `labels-removed-at-tip.txt`):

- base-only (removed at tip): **0**
- tip-only (added): **16**, all `(R44-C1)`
- `148 = 132 + 16`; all 148 tip labels and all 132 base labels are unique
  (`sort -u | wc -l` equals the count, 0 duplicates), so no case was renamed into a
  duplicate to inflate the total.
- Base output contains **0** occurrences of `SCRUB` and 0 `(R44…)` labels; the base script
  itself has 0 `SCRUB` / 0 `probe_scrub_record` tokens vs 26 / 2 at tip.

Judging axis coverage: the 16 cases cover absent/present dirs, records, `_tmp`, progress
sockets, unreadable (000) records, orphan fsid, `scrub_speed_max` (nonzero / 0 / zero-padded
/ empty / non-decimal / missing), unlistable dir, non-directory sysfs root, absent sysfs with
records, wrong-name file types, symlinked/directory records, timer wants (link-name instances
vs bare template, other timers, directory named like a timer), name-never-echoed (a forged
`TSUKUROI_CENSUS: HEALTHY` injected through a newline filename is asserted ABSENT), and the
`LC_ALL=C` collation pin. Cases assert exit code + final verdict + the exact
`^SCRUB btrfs-scrub-record …$` line, so they are not vacuous substring matches.

## Locale check: `LC_ALL=C` vs `en_US.UTF-8` — identical

- `LC_ALL=C ./census-tip.sh --selftest` → rc 0, 148/148, log `run-tip-LC_ALL=C.txt`
- `LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8 ./census-tip.sh --selftest` → rc 0, 148/148, log
  `run-tip-LC-en_US.UTF-8.txt`
- `cmp tip-LC_C.txt tip-LC_enUS.txt` → **byte-identical** (no output). Both are also
  byte-identical to the ambient-locale `tip-1` log.
- `locale -a` on the host provides `C`, `C.utf8`, `en_US.utf8`; `en_US.UTF-8` resolves to
  `en_US.utf8`, so the non-C branch was genuinely exercised (the same environment the R44
  collation case 16 uses via `EXTRA_ENV=(LC_ALL=en_US.UTF-8)`).

## Verdict-neutrality / contract spot-checks (static, against the exported tip file)

- One line, printed `probe_scrub_record; printf '%s\n' "$SCRUB_LINE"` (3419-3421), positioned
  **after** the storage arm's `printf '%s\n' "$STORAGE_LINE"` and **before** the rollup
  `local roll=HEALTHY` / `worse` chain and before `TSUKUROI_CENSUS:` — as the header contract
  states (`tools/tsukuroi-census.sh`) header "Round-44 addition (C1)", lines 384-406.
- `SCRUB_LINE` has exactly three references: the two assignments (2039, 2041) and the print
  (3421). It never reaches `worse`; `roll` is computed only from `PKG_V SYS_V DRV_V JRN_V
  UPD_V OOM_V` (3424-3429), so the arm cannot move the rollup term or the exit code.
- `probe_scrub_record` (1965-2043) is read-only: names + `stat`-style tests only, no redirect
  that writes, `return 0`; `local LC_ALL=C` at 1966 pins collation for the arm, matching the
  header's bytewise-detail-order claim. Defaults `SCRUB_DIR=${TSUKUROI_SCRUB_DIR:-/var/lib/btrfs}`
  and `TIMER_WANTS=${TSUKUROI_TIMER_WANTS:-/etc/systemd/system/timers.target.wants}` (492-493)
  match the header.
- Cross-check against w1's live receipt (read-only, not my measurement):
  `.ufo/waves/round-44/after/c1-after-8eee79db.jsonl` carries three `SCRUB btrfs-scrub-record`
  lines whose state/dir/counts/detail fields fit the same grammar. Live-mode behaviour,
  PLANE-line identity and live exit codes are other w2 seats' items; this seat measured the
  hermetic selftest only.

## Kill-rule exposure from this seat

None triggered: no PLANE/rollup/exit-code claim is touched by the new line (static proof
above), the predecessor 132-case suite still passes in full at tip (0 removed labels), and the
selftest asserts fixture byte-identity plus creates no files in live mode by construction
(`find`-into-variables only; no `mktemp` outside the selftest path).

## Limits

- Only the selftest surface was exercised; host live state was not sampled here (deliberate —
  other w2 seats hold the live receipt and kill-rule measurements).
- The 148/132 counts were measured on this host's bash/`find`/`stat` (unprivileged, no
  `unshare` needed); a root-only environment could differ, as the header documents for
  0600 records.

## Proposed text (C1 scorecard / report line)

> C1-2 final selftest (C1ExecFinalSelftest, w2): `tools/tsukuroi-census.sh` exported at
> `8eee79db` (blob `8a2a665c`, sha256 `2ef86357…`) and base `98020ece` (blob `18a1db64`,
> sha256 `7c9f7903…`). Tip `--selftest` ran three times plus one repeat: 148/148 PASS each,
> byte-identical logs; base: 132/132 PASS. Label delta is exactly 16 added `(R44-C1)` cases
> and 0 removed (148 = 132 + 16), all labels unique. `LC_ALL=C` and `LC_ALL=en_US.UTF-8` runs
> are byte-identical (148/148 each). The `SCRUB btrfs-scrub-record` line prints once, after
> STORAGE and before the rollup, never feeds `worse`, and the probe is read-only.
> Verdict: supports C1.
