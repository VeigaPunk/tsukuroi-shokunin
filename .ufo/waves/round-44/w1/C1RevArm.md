VERDICT: supports

Item C1-15 — review of `probe_scrub_record` and its 9 selftest cases, tools/tsukuroi-census.sh at
7e081698d4fc3c4ea944884fd093058de9909de1 (worktree verified byte-identical to that revision by
`cmp`; single commit ab8aae16 between base 98020ece and impl, +177/-1 lines). Line numbers below
are that revision's. No tool installs were made (none needed).

## Question-by-question findings

1. Every echoed token validated (QUALITY 84 — corpus/QUALITY.md:165)? YES.
   - The line grammar (1967-2040, output built at 2036-2038) echoes only: `state` from the fixed
     enum NONE|RECORDED|BLOCKED (2034-2035), `dir` from absent|present|unreadable (1971,1999,2001),
     nine arithmetic counters, and `detail=` tokens that are either fixed reason strings
     (`sysfs:unreadable` 1975, `dir:unreadable` 1999, `sysfs:absent` 2019, `timers:unreadable` 2025,
     `record:not-regular` 2006, `tmp:not-regular` 2011, `progress:not-socket` 2015) or carry
     name-derived parts only after a closed-pattern match: `fs8` is the first 8 chars of a basename
     that matched `^[0-9a-f]{8}-...-[0-9a-f]{12}$` (1970,1980-1981); every devid echoed was matched
     `^[0-9]+$` first (1984 guards the echoes at 1986,1990,1992); `speed_max=$v` echoes `v` only
     after `^[0-9]+$` (1989-1992). Host names, record names and timer instance names are never
     echoed — the wrong-type reasons are constant strings (2006,2011,2015) and timers are counted,
     not printed (2027-2030). The round-38 lesson (newline name forging a second rollup line) is
     both structurally excluded and asserted: fixture name `scrub.status.<uuid>\nTSUKUROI_CENSUS:
     HEALTHY (forged)` (3277) must be ignored, asserted `ABSENT:^TSUKUROI_CENSUS: HEALTHY \(forged`
     (3280). Hostile battery (receipt hostile-battery.txt): forged name ignored, uppercase-UUID
     record ignored, all detail tokens as above, run under `set -euo pipefail`, rc=0.

2. `set -e` / `set -u` hazards? None found; one narrow TOCTOU residual.
   - No `((i++))`-style pre-increment: the read loop uses `nl=$((nl + 1))` (1988), which cannot
     return nonzero. Verified `while false; do :; done` exits 0 under `set -euo pipefail` (observed
     rc=0), so the read loop's final false condition is harmless.
   - BASH_REMATCH: `${BASH_REMATCH[1]}` (2009) is expanded inside the branch whose regex
     `^scrub\.status\.(${uuid})$` (2005) had just matched, and word expansion precedes the `[[`
     that follows it in the same list — never unset. Battery ran with `set -u` active, rc=0.
   - Empty globs: nullglob is NOT set (no nullglob/failglob anywhere in the file); unmatched globs
     leave the literal pattern, and every loop guards it: 1979 (`[ -e "$fsd" ]`), 1983, 2003
     (`[ -e "$e" ] || [ -L "$e" ]`, which also keeps dangling symlinks), 2028. No unguarded
     expansion.
   - Read loop: `while IFS= read -r line || [ -n "$line" ] ... < "$f"` (1988) correctly counts a
     final line without trailing newline (battery: `104857600` with no newline read as limited=1;
     empty file and two-line file both speed-malformed).
   - RESIDUAL (low): TOCTOU between the `-f` test (1986) and the `< "$f"` redirect (1988). If the
     file disappears in between, the failed redirect fails the `while` compound under `set -e` and
     kills the whole census. Demonstrated on the construct: file checked, deleted, redirect → rc=1,
     `UNREACHED`. Live reachability requires a sysfs scrub_speed_max to vanish mid-run (kernel
     attribute removal ≈ module unload); fixtures are selftest-controlled. Not a defect claim; note
     for the record. Relatedly, `read -r line` is unbounded — a pathological one-line fixture file
     of any size is slurped; host sysfs files are kernel-bounded.

3. Blocking reads / FIFOs? None reachable.
   - The only content read in the arm is `scrub_speed_max` (1988), reached only after `-f` (1986);
     a FIFO fails `-f`, so it can never be redirected from. Battery: FIFO at
     devinfo/1/scrub_speed_max → `11111111:1:speed-unreadable`, returned in well under the 10 s
     timeout (rc=0, not 124). Progress entries are classified by `-S` (2015) — a FIFO progress name
     reads `progress:not-socket` without being opened (battery + selftest case 3276 plants a real
     mkfifo). Records are never opened at all: `[ -r "$e" ]` (2008,2013) is an access check, per
     the header's "by name and stat, never by content" (391-392).

4. Symlink escape? Entry-level symlinks are blocked before any content/type test follows them:
   record (2006), tmp (2011), progress (2015) all test `[ -L "$e" ]` first; dangling symlinks pass
   the 2003/2028 existence guard via `-L` and are classified not-regular. Timer links are symlinks
   by nature and are counted by name only (2027-2030), which is the contract (397-399).
   INFORMATIONAL: the configured roots themselves — TSUKUROI_SCRUB_DIR / TSUKUROI_BTRFS_SYSFS —
   are followed if they are symlinks (observed: scrub dir symlinked to another tree reads
   `dir=present records=1 orphan=1`; sysfs symlink likewise). That matches the other census dir
   overrides (an operator-configured path is authoritative) and no entry-symlink is ever followed,
   but the header's `dir=absent|present|unreadable` does not document symlink-following at dir
   level; one clause would close it if the C2/verdict seats care.

5. Locale dependence? Closed. `local LC_ALL=C` (1968) demonstrably governs the function's glob
   sort: with ambient `LC_ALL=en_US.UTF-8`, ambient expansion sorts `scrub.status.a~b` before
   `scrub.status.aXb`, while the same loop inside the function with `local LC_ALL=C` sorts bytewise
   (`aXb` before `a~b`) — receipt lc-all-glob-demo.txt. Battery output is byte-identical under
   LC_ALL=C and en_US.UTF-8. Everything else in the arm is numeric (`-eq/-gt/-ne`, `$(( ))`),
   regex with explicit `[0-9a-f]`/`[0-9]` classes, or fixed strings — no collation-dependent
   comparison remains.

6. Selftest hermeticity? YES. `check` sets TSUKUROI_SCRUB_DIR="$FX/scrub",
   TSUKUROI_TIMER_WANTS="$FX/wants" (2282-2283) and TSUKUROI_BTRFS_SYSFS="$FX/btrfs" (2280) on
   every case; `fx_default` (2137ff) creates none of these three, so case `scrub-absent`
   (3228-3230) genuinely exercises absent dirs and no case can fall through to /var/lib/btrfs or
   /etc/systemd/system/timers.target.wants. Every case re-asserts the hostname override
   (`host=fixture-host`) and hashes the fixture tree before/after (`fx_hash`, 2228, 2239-2244),
   so a surprise host read or any mutation would fail loudly. Observed: `bash
   tools/tsukuroi-census.sh --selftest` with TMPDIR pointed at my scratch → `PASS (141 cases, 141
   passed, 0 failed)`, rc=0 (receipt selftest-141.log). Count check: 138 `check '` + 3 `check_cli`
   = 141 total; 9 labels match `(R44-C1)` (grep count 9, lines 3229-3286) → 132 before, 141 after,
   as declared.

7. Does `check_cli` (no fixture env) reach the arm? NO. `check_cli` runs `"$BASH" "$SELF"` with no
   env (2338-2340) and its comment pins the invariant "only arms that exit before any probe"
   (2327). All three cases (3288-3293) exit inside the argument-parse loop at the top of `main`:
   `--bogus` → 3315, `--sample 0` → 3309/3311, `--help` → 3314; the arm is called only later, at
   3375. Observed live: `--bogus` rc=2 and `--sample 0` rc=2 with usage text only and no probe
   output, instantly; `--help` rc=0.

## Contract conformance extras

- Placement: STORAGE (3372) → SCRUB (3376) → rollup (3378-3385), matching the header's "ONE line
  after the STORAGE line and before the rollup" (386-388). Live run on this host (receipt
  live-census-7e081698.txt): `SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0
  sockets=0 unreadable=0 orphan=0 limited=0 timers=0` between the STORAGE line and
  `TSUKUROI_CENSUS: BLOCKED (...)`; consistent with the host state I stat'ed (/var/lib/btrfs
  absent; /sys/fs/btrfs 755 present; no btrfs-scrub@*.timer in timers.target.wants). Arm returns 0
  (2039) and nothing consumes its output for the verdict — the rollup at 3378-3385 reads only
  plane variables, so the line is verdict-neutral by construction.
- The base→impl diff is additive except one usage-text line (deleted `...DRIFT (pacnew) and
  STORAGE ... lines`, replaced at 600-601 with `...DRIFT (pacnew), STORAGE (btrfs error counters)
  and SCRUB (btrfs scrub record, unprivileged view) lines`) — no existing behavior line touched.
- Selftest case coverage maps 1:1 onto the header's token taxonomy: NONE/absent (3229), RECORDED +
  foreign names ignored (3236), unreadable/orphan/tmp split (3244), limited listing + 0=no-limit
  (3251), speed-malformed + speed-unreadable BLOCKED (3257), dir:unreadable BLOCKED (3263), timer
  counting with the bare template excluded (3271), wrong types + forged newline name (3278),
  sysfs:absent BLOCKED (3285). Note the fixture builds declare the wrong-type reason strings
  sorted bytewise (`progress:not-socket,record:not-regular,record:not-regular`, 3279), which
  double-pins the LC_ALL=C claim.

## Residual risk and verification gaps

- TOCTOU kill on `< "$f"` (1986-1988) and unbounded line read — see item 2; low, live-sysfs-only.
- Dir-level symlink following is undocumented in the header contract (informational, item 4).
- I did NOT run the frozen counters (score-scrub-arm-r44.py, check-scrub-record-r44.py) — those
  are the counter/C2 seats' predicates; I did NOT compare base-vs-impl live PLANE lines (the kill
  rule is integrator/counter scope); my live evidence is one impl-revision run. The census selftest
  was run with TMPDIR in my scratch; its own fixture writes stayed under mktemp there.
- Scratch /fast/scratch/hyaku/tsukuroi-r44/C1RevArm removed after receipt copy. Receipts:
  live-census-7e081698.txt, selftest-141.log, hostile-battery.txt, lc-all-glob-demo.txt in
  .ufo/waves/round-44/w1/C1RevArm/.
