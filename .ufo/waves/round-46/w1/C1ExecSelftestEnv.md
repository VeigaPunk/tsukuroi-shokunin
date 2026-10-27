VERDICT: defect-found

## Item C1-19 — the census selftest across six environments, and its cost delta base vs impl

Seat: C1ExecSelftestEnv (leaf). Lane: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin.
Scratch: /fast/scratch/hyaku/tsukuroi-r46/C1ExecSelftestEnv (exported copies, removed at the end;
receipts copied to this seat dir first). Nothing in the lane, the fleet repo, a sibling lane or the
host was written. No tool was installed or upgraded (none was needed).

### The two censuses under test

Both were exported with `git show <rev>:tools/tsukuroi-census.sh` from the lane, never from the work
tree, so the byte identity is the commit's:

| rev | role | sha256 | lines | bytes |
|---|---|---|---|---|
| 2042117cfb724170772f4c128cc2ddba0b61d817 | base (lane tip at round start) | `237b21c9d757e339943c29b0f005faf569ff997deca46dd5bce16bc631b5fcdc` | 3485 | 202665 |
| a44770491eb5ca15ce9f8b3207309d1af683ffaf | impl (C1 census-identity) | `d925839cde9737fbd624ad2302671671c7ecc4e9a9331a1ff5a2ad1839112cfa` | 3598 | 209208 |

Cross-check of the new line against an independent recomputation over the exported file (command with
its output, both below):

```
$ bash impl/tsukuroi-census.sh --identity
TSUKUROI_CENSUS_IDENTITY: version=census-v2 sha256=d925839cde9737fbd624ad2302671671c7ecc4e9a9331a1ff5a2ad1839112cfa md5=db08a606ce128da3839457372e91e220 bytes=209208 lines=3598 planes=packages,systemd,drivers,journal,update-safety,oom exit_map=0:HEALTHY,1:DEGRADED,2:BLOCKED verified=yes
$ printf 'sha256=%s md5=%s bytes=%s lines=%s\n' "$(sha256sum < impl/tsukuroi-census.sh | cut -d' ' -f1)" ...
sha256=d925839c...9112cfa md5=db08a606ce128da3839457372e91e220 bytes=209208 lines=3598
```

The same line came out byte-identical through a symlinked directory (`bash impl-link/tsukuroi-census.sh
--identity`, where `impl-link -> impl`) and from a relative path (`cd impl && bash ./tsukuroi-census.sh
--identity`): the descriptor-based read is stable under both invocation shapes. That is extra evidence
for C1 outside this item's remit; the item's measurements follow.

### The six environments (impl a4477049)

Driver: `<seat dir>/drive.sh`, run from the scratch root; one census selftest at a time. Receipts are
`<env>.out` / `<env>.meta` in `<seat dir>/`; elapsed is per-run wall time on a host carrying ~100
other seats, so it is not the cost comparison (see the interleaved timing below).

| # | environment | rc | summary line | FAIL lines | elapsed |
|---|---|---|---|---|---|
| 1 | `LC_ALL=C` | 0 | `TSUKUROI_CENSUS_SELFTEST: PASS (160 cases, 160 passed, 0 failed)` | 0 | 53305 ms |
| 2 | `LC_ALL=C.UTF-8` | 0 | `TSUKUROI_CENSUS_SELFTEST: PASS (160 cases, 160 passed, 0 failed)` | 0 | 55642 ms |
| 3 | default locale (`LANG=en_US.UTF-8`, `LC_ALL` unset) | 0 | `TSUKUROI_CENSUS_SELFTEST: PASS (160 cases, 160 passed, 0 failed)` | 0 | 55485 ms |
| 4 | `TMPDIR=/fast/…/C1ExecSelftestEnv/tmp space` | 1 | `TSUKUROI_CENSUS_SELFTEST: FAIL (160 cases, 11 passed, 149 failed)` | 149 | 51330 ms |
| 5 | relative path from the census's own dir (`cd impl && ./tsukuroi-census.sh --selftest`) | 0 | `TSUKUROI_CENSUS_SELFTEST: PASS (160 cases, 160 passed, 0 failed)` | 0 | 43168 ms |
| 6 | absolute path through a symlinked dir (`bash impl-link/tsukuroi-census.sh --selftest`) | 0 | `TSUKUROI_CENSUS_SELFTEST: PASS (160 cases, 160 passed, 0 failed)` | 0 | 41325 ms |

`LC_ALL=C` was run twice (a first pass and a timed rerun); both are 160/160 PASS, receipts
`impl-lc_C.out` and `impl-lc_C_timed.out`. No run in any environment emitted a `setlocale` warning
(`grep -cE 'warning: setlocale|cannot change'` = 0 in all eight receipts).

The six `(R46-C1)` lines, identical byte for byte in **all seven** impl receipts — including the spaced
`TMPDIR` run, where they pass unchanged while every fixture-plane case fails:

```
PASS identity: one line naming this file, digests recomputed here, verified=yes (R46-C1) (exit 0)
PASS identity: a copy with one appended line reports its own bytes, not a constant (R46-C1) (exit 0)
PASS identity: a symlink invocation reports the target file (R46-C1) (exit 0)
PASS identity: a script read from stdin prints unverifiable, never a decoy file named bash (R46-C1) (exit 0)
PASS identity: a file replaced after bash opened it prints unverifiable, never the new bytes (R46-C1) (exit 0)
PASS cli: --identity with another flag exits 2 (R46-C1) (exit 2)
```

(`grep -E '\(R46-C1\)' <receipt> | md5sum` = `b6ba0ba6f2dde716434460a9a4d23111` for every impl run.)

### Environment 4 fails, and the failure is not round 46's

The full verbatim list of the 149 FAIL lines is appended below and is also a receipt:
`impl-tmpdir-space.FAIL-lines.txt` (149 lines), with the run's complete output in
`impl-tmpdir-space.out`. Three shapes, and only three:

| shape | count |
|---|---|
| `<label>: configured root not asserted at a field boundary (wanted root_dir=/fast/…/tmp space/…; possible live-root read)` | 34 |
| `<label>: exit 2 wanted 0; output: … TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED …)` | 76 |
| `<label>: exit 2 wanted 1; output: … TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED …)` | 39 |

The 11 that pass are exactly the 5 cases that never touch the root arm (the two `(R12-C1)` unsafe/empty
override cases and the three CLI cases) plus the six `(R46-C1)` cases.

Mechanism, demonstrated on the live census with one command each:

```
$ TSUKUROI_ROOT_DIR="/fast/…/C1ExecSelftestEnv/tmp space/rootA" bash impl/tsukuroi-census.sh
  … root_status=unavailable(override=unsafe) … root_dir=unsafe
$ TSUKUROI_ROOT_DIR="/fast/…/C1ExecSelftestEnv/tmpdefault" bash impl/tsukuroi-census.sh
  … root_status=ok root_mode=0755 … root_dir=/fast/…/C1ExecSelftestEnv/tmpdefault
```

`root_locator_class` (tools/tsukuroi-census.sh:848-863, the rejection at :857) admits only
`[A-Za-z0-9._/+-]` after the leading `/`, by design (:849-851: "`=` and whitespace are rejected so a path
like `/x root_mode=0755` can neither forge a token nor reach stat"), so the fixture root the selftest
builds under a spaced `TMPDIR` (`work=$(mktemp -d "${TMPDIR:-/tmp}/tsukuroi-r3-2-selftest.XXXXXX")`,
:2048) is classified `unsafe`, `probe_root_meta` returns `BLOCKED` (:881-885), and every `check()` case
fails at its rc (:2293-2294) or at its `root_dir=` boundary assertion (:2299-2300).

Attribution — this is pre-existing, not a round-46 regression. The same run on the base census:

```
$ env "TMPDIR=…/tmp space" bash base/tsukuroi-census.sh --selftest
TSUKUROI_CENSUS_SELFTEST: FAIL (154 cases, 5 passed, 149 failed)
```

and the two FAIL label sets are identical (`diff` of the label-only extracts: `IDENTICAL FAIL LABELS
base vs impl`), with the impl adding exactly the six identity PASS lines and nothing else. The
whitespace rejection predates the identity work; round 46's six cases are space-robust because they
hash through the descriptor and never consult the root arm.

### The consequence that matters for the frozen instrument

`tools/score-census-identity-r46.py` runs the selftest with `TMPDIR` **inside `--scratch`**
(:134, :145,:148: `tmp_d = top/tmp`, `env = {… 'TMPDIR': tmp_d}`) and gates on
`selftest_pass == 1` (:34,:39). Scored twice on the same correct revision, only the scratch path
differing:

| `--scratch` | verdict | identity_ok | tracks/symlink/unverifiable/cli/nowrite | selftest_pass | selftest_r46 | selftest last line |
|---|---|---|---|---|---|---|
| `/fast/…/C1ExecSelftestEnv/cnt-nospace` | **PASS** | 1 | 1/1/1/1/1 | 1 | 6 | `TSUKUROI_CENSUS_SELFTEST: PASS (160 cases, 160 passed, 0 failed)` |
| `/fast/…/C1ExecSelftestEnv/cnt space` | **FAIL** | 1 | 1/1/1/1/1 | 0 | 6 | `TSUKUROI_CENSUS_SELFTEST: FAIL (160 cases, 11 passed, 149 failed)` |

Receipts: `counter-nospace.json`, `counter-space.json` (both runs `rc=0`/`rc=1`; the counters' own
stderr empty). So a grader whose scratch directory has a space in its path scores a byte-correct
implementation **FAIL** on `selftest_pass`, while all seven identity legs and all six `(R46-C1)` labels
pass. The older counters share the pattern (e.g. `score-census-readers-r45.py:29,:107`: "TMPDIR in
scratch", `e['TMPDIR'] = tmp`), so this is a property of the shared harness, not of C1's code — but
round 46 is where it can flip a declared predicate, and no counter in `tools/` guards for it
(`grep -l 'space' score-*.py` matches only `[[:space:]]` regexes).

Nothing in the census documents the requirement: the `--selftest` help text
(tools/tsukuroi-census.sh:594-601) and the override header (:411-430) say only that it writes under
`${TMPDIR:-/tmp}`, with no space-free (safe-charset) note.

### Cost delta, base vs impl (interleaved, default locale, space-free TMPDIR)

`time.sh`, three pairs, base and impl alternating so the host load hits both:

| pair | base 2042117c | impl a4477049 |
|---|---|---|
| 1 | 36578 ms (154 cases) | 38378 ms (160 cases) |
| 2 | 36292 ms (154 cases) | 39468 ms (160 cases) |
| 3 | 40238 ms (154 cases) | 37926 ms (160 cases) |
| median | **36578 ms** | **38378 ms** |

Delta: **+1800 ms median (+4.9 %)**, which is inside the base's own spread (36.3–40.2 s) and inside the
impl's (37.9–39.5 s); per case 237.5 ms → 239.9 ms (+2.4 ms). Six extra cases cost about 1.8 s of the
~37 s run; the run is dominated by the 154 pre-existing fixture cases, not by the identity block. All
six runs are `PASS`, receipts `tm-{base,impl}-{1,2,3}.out`, `timing.tsv`. The higher single-shot numbers
in the table above (41–56 s) are load, not revision, and must not be read as the delta.

### What I did and did not run

Ran: 11 impl selftest passes (the seven environment runs — `LC_ALL=C` twice — plus `impl-timed` and the
three interleaved timing passes) and 5 base passes (`base-timed`, `base-tmpdir-space` and the three
interleaved), plus 2 frozen-counter runs and the identity cross-checks above.
Not run: any other locale (no `tr_TR`/non-UTF-8 collation beyond the three named), a `TMPDIR` that is
relative, read-only, on tmpfs, or contains `=`; the base census under environments 2, 3, 5, 6 (base was
measured only where a delta was needed); anything that mutates the host, the lane or a fixture outside
my scratch. The selftest's own cleanup was observed to work — no `tsukuroi-r3-2-selftest.*` directory
survived in either TMPDIR (`ls -d tmpdefault/* "tmp space"/*` shows only my own `bin/` and `rootA/`).

### Proposal (not applied — this seat is read-only on lane content)

One of, in the L1's call order of preference:

1. In `run_selftest`, refuse early with a named skip instead of 149 spurious failures, e.g. after the
   `mktemp -d`: `if [ "$(root_locator_class "$work")" != absolute ]; then printf 'SKIP selftest: TMPDIR must be an absolute path from [A-Za-z0-9._/+-] (fixture root override would read unsafe)\n'; exit 0; fi` — but note the counter treats a non-`PASS` last line as `selftest_pass=0`, so a `SKIP` exit 0 would still fail the predicate; it only makes the cause legible.
2. Make the harness space-safe: have `run_selftest` place the fixture root under a space-free child of
   `$work` (the fixture paths, not `$work` itself, are what reach `TSUKUROI_ROOT_DIR`), so `TMPDIR` may
   be anything.
3. Independently of either: have the round-46 counter reject a `--scratch` whose path is not
   `root_locator_class`-safe, with a named error rather than a silent `selftest_pass=0`.

Note for the L1: option 2 is the only one that makes environment 4 pass, and it is a selftest-internal
change to a line outside the C1 identity block (`run_selftest`'s fixture builder), so it needs its own
scored revision if taken; this seat has not touched it.

### Appendix — every FAIL line of environment 4 (TMPDIR containing a space), verbatim

Run: `impl-tmpdir-space.out`, ledger below is `impl-tmpdir-space.FAIL-lines.txt` (149 lines). The census is
`a4477049`; the base census at the same `TMPDIR` produces the same 149 labels (`base-tmpdir-space.FAIL-lines.txt`).

```
FAIL healthy: all planes pass: exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL healthy: nvidia present and answering: exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL healthy: unrestricted dmesg ring preferred: exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL healthy: rc=1 backup-only sample is not a defect: exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL degraded: Qkk sample drift: exit 2 wanted 1; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL degraded: foreign packages: exit 2 wanted 1; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=DEGRADED oom=HEALTHY)
FAIL healthy: foreign set equals the accepted baseline (16 rows, hit): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL healthy: embedded r6 snapshot is the default source: exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL degraded: new foreign arrival is named: exit 2 wanted 1; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=DEGRADED oom=HEALTHY)
FAIL degraded: baseline version change shows both versions: exit 2 wanted 1; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL degraded: baseline row no longer installed is never silent: exit 2 wanted 1; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL degraded: absent baseline never reads HEALTHY: exit 2 wanted 1; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=DEGRADED oom=HEALTHY)
FAIL degraded: declared hold (IgnorePkg): exit 2 wanted 1; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL degraded: failed unit: exit 2 wanted 1; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=DEGRADED drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL degraded: timer last run failed: exit 2 wanted 1; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=DEGRADED drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL degraded: kernel error ring: exit 2 wanted 1; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=DEGRADED journal=DEGRADED update-safety=HEALTHY oom=HEALTHY)
FAIL blocked: pacman db.lck: configured root not asserted at a field boundary (wanted root_dir=/fast/scratch/hyaku/tsukuroi-r46/C1ExecSelftestEnv/tmp space/tsukuroi-r3-2-selftest.XPZD1W/fx/blocked-lck/root; possible live-root read)
FAIL blocked: pacman binary missing: configured root not asserted at a field boundary (wanted root_dir=/fast/scratch/hyaku/tsukuroi-r46/C1ExecSelftestEnv/tmp space/tsukuroi-r3-2-selftest.XPZD1W/fx/blocked-pacman-missing/root; possible live-root read)
FAIL blocked: sample probe error: configured root not asserted at a field boundary (wanted root_dir=/fast/scratch/hyaku/tsukuroi-r46/C1ExecSelftestEnv/tmp space/tsukuroi-r3-2-selftest.XPZD1W/fx/blocked-sample-error/root; possible live-root read)
FAIL blocked: a sample error ahead of a large -Qkk output still blocks (R42-C1): configured root not asserted at a field boundary (wanted root_dir=/fast/scratch/hyaku/tsukuroi-r46/C1ExecSelftestEnv/tmp space/tsukuroi-r3-2-selftest.XPZD1W/fx/blocked-sample-error-large/root; possible live-root read)
FAIL blocked: systemd user bus unreachable: configured root not asserted at a field boundary (wanted root_dir=/fast/scratch/hyaku/tsukuroi-r46/C1ExecSelftestEnv/tmp space/tsukuroi-r3-2-selftest.XPZD1W/fx/blocked-bus/root; possible live-root read)
FAIL blocked: nvidia hardware, driver offline: configured root not asserted at a field boundary (wanted root_dir=/fast/scratch/hyaku/tsukuroi-r46/C1ExecSelftestEnv/tmp space/tsukuroi-r3-2-selftest.XPZD1W/fx/blocked-gpu/root; possible live-root read)
FAIL blocked: both kernel rings unusable: configured root not asserted at a field boundary (wanted root_dir=/fast/scratch/hyaku/tsukuroi-r46/C1ExecSelftestEnv/tmp space/tsukuroi-r3-2-selftest.XPZD1W/fx/blocked-rings/root; possible live-root read)
FAIL blocked: empty ring is not a clean bill: configured root not asserted at a field boundary (wanted root_dir=/fast/scratch/hyaku/tsukuroi-r46/C1ExecSelftestEnv/tmp space/tsukuroi-r3-2-selftest.XPZD1W/fx/blocked-empty-ring/root; possible live-root read)
FAIL healthy: journal/boot plane in the rollup: exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL degraded: journal boot errors at entry level: exit 2 wanted 1; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=DEGRADED journal=DEGRADED update-safety=HEALTHY oom=HEALTHY)
FAIL degraded: failed services history from journal: exit 2 wanted 1; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=DEGRADED journal=DEGRADED update-safety=HEALTHY oom=HEALTHY)
FAIL degraded: enabled timer not armed (drift): exit 2 wanted 1; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=DEGRADED update-safety=HEALTHY oom=HEALTHY)
FAIL blocked: journalctl missing (fails closed): configured root not asserted at a field boundary (wanted root_dir=/fast/scratch/hyaku/tsukuroi-r46/C1ExecSelftestEnv/tmp space/tsukuroi-r3-2-selftest.XPZD1W/fx/blocked-journal-missing/root; possible live-root read)
FAIL blocked: boot record missing: configured root not asserted at a field boundary (wanted root_dir=/fast/scratch/hyaku/tsukuroi-r46/C1ExecSelftestEnv/tmp space/tsukuroi-r3-2-selftest.XPZD1W/fx/blocked-boot-record/root; possible live-root read)
FAIL blocked: boot target not reached: configured root not asserted at a field boundary (wanted root_dir=/fast/scratch/hyaku/tsukuroi-r46/C1ExecSelftestEnv/tmp space/tsukuroi-r3-2-selftest.XPZD1W/fx/blocked-boot-target/root; possible live-root read)
FAIL blocked: empty journal is not a clean bill: configured root not asserted at a field boundary (wanted root_dir=/fast/scratch/hyaku/tsukuroi-r46/C1ExecSelftestEnv/tmp space/tsukuroi-r3-2-selftest.XPZD1W/fx/blocked-journal-empty/root; possible live-root read)
FAIL blocked: journal err stream unreadable: configured root not asserted at a field boundary (wanted root_dir=/fast/scratch/hyaku/tsukuroi-r46/C1ExecSelftestEnv/tmp space/tsukuroi-r3-2-selftest.XPZD1W/fx/blocked-journal-err/root; possible live-root read)
FAIL blocked: empty local db is not a pass (D02): configured root not asserted at a field boundary (wanted root_dir=/fast/scratch/hyaku/tsukuroi-r46/C1ExecSelftestEnv/tmp space/tsukuroi-r3-2-selftest.XPZD1W/fx/blocked-empty-pkgdb/root; possible live-root read)
FAIL healthy: privilege artifacts counted, not drift (D05): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL healthy: bounded -Qkk sample honors its size (D06): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL degraded: empty timer Result is an unknown, not a failure (D09): exit 2 wanted 1; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=DEGRADED drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL degraded: user scope state degraded (D10): exit 2 wanted 1; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=DEGRADED drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL blocked: nvidia module loaded but no /dev node (D12): configured root not asserted at a field boundary (wanted root_dir=/fast/scratch/hyaku/tsukuroi-r46/C1ExecSelftestEnv/tmp space/tsukuroi-r3-2-selftest.XPZD1W/fx/blocked-no-node/root; possible live-root read)
FAIL degraded: kernel ring class counts are evidence (D14/D15): exit 2 wanted 1; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=DEGRADED journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL blocked: unreadable PCI inventory is not a pass (D19): configured root not asserted at a field boundary (wanted root_dir=/fast/scratch/hyaku/tsukuroi-r46/C1ExecSelftestEnv/tmp space/tsukuroi-r3-2-selftest.XPZD1W/fx/blocked-pci-unreadable/root; possible live-root read)
FAIL degraded: journal timer plane unreadable, drift unknown (D20): configured root not asserted at a field boundary (wanted root_dir=/fast/scratch/hyaku/tsukuroi-r46/C1ExecSelftestEnv/tmp space/tsukuroi-r3-2-selftest.XPZD1W/fx/degraded-jrn-timer-plane/root; possible live-root read)
FAIL healthy: memory-pressure arm quiet (S7-2): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL degraded: memory arm — oom_kill is a presence flag, not a count (S7-2): exit 2 wanted 1; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=DEGRADED journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL degraded: memory arm — ring oom class and C1/C2/C3 reported together (S7-2): exit 2 wanted 1; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=DEGRADED journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL degraded: memory arm — swap-pressure anchors C5 (S7-2): exit 2 wanted 1; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=DEGRADED journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL degraded: memory arm — memory.events.local flag reported separately (S7-2): exit 2 wanted 1; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=DEGRADED journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL degraded: memory arm — unreadable PSI is a named unknown, not a pass (S7-2): exit 2 wanted 1; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=DEGRADED journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL degraded: memory arm — unreadable slice anchors are a named unknown (S7-2): exit 2 wanted 1; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=DEGRADED journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL blocked: memory arm — no cgroup and no journal: no class readable (S7-2): configured root not asserted at a field boundary (wanted root_dir=/fast/scratch/hyaku/tsukuroi-r46/C1ExecSelftestEnv/tmp space/tsukuroi-r3-2-selftest.XPZD1W/fx/blocked-mem-unreadable/root; possible live-root read)
FAIL healthy: update-safety INERT over a fresh channel (R9): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL degraded: update candidates are REQUIRES-PREP with names (R9): exit 2 wanted 1; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=DEGRADED oom=HEALTHY)
FAIL degraded: 4002 update candidates keep the names and the trap row (R42-C1): exit 2 wanted 1; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=DEGRADED oom=HEALTHY)
FAIL degraded: -Qu empty against a large -Sup keeps the disagree names (R42-C1): exit 2 wanted 1; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=DEGRADED oom=HEALTHY)
FAIL degraded: -Qu/-Sup count mismatch against a large -Sup keeps the disagree names (R42-C1): exit 2 wanted 1; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=DEGRADED oom=HEALTHY)
FAIL blocked: an empty -Qu at rc=0 is unreadable, never INERT (R9): configured root not asserted at a field boundary (wanted root_dir=/fast/scratch/hyaku/tsukuroi-r46/C1ExecSelftestEnv/tmp space/tsukuroi-r3-2-selftest.XPZD1W/fx/blocked-update-qu/root; possible live-root read)
FAIL blocked: empty over no channel is not an up-to-date reading (R9): configured root not asserted at a field boundary (wanted root_dir=/fast/scratch/hyaku/tsukuroi-r46/C1ExecSelftestEnv/tmp space/tsukuroi-r3-2-selftest.XPZD1W/fx/blocked-update-nochannel/root; possible live-root read)
FAIL degraded: a stale content stamp is UNKNOWN-UPSTREAM, never INERT (R9): exit 2 wanted 1; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=DEGRADED oom=HEALTHY)
FAIL healthy: the channel-freshness threshold is honoured, not decorative (R9): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL degraded: the fold names unknown-provenance arrivals and can only worsen (R9): exit 2 wanted 1; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=DEGRADED oom=HEALTHY)
FAIL degraded: the fold never reads off a missing baseline (R9): exit 2 wanted 1; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=DEGRADED oom=HEALTHY)
FAIL healthy: the joined class split is the register AUR-local pair (R9): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL healthy: the -Suu trap row is printed and verdict-neutral (R9): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL healthy: a log window miss prints cmd=unknown (R9): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL degraded: a repo-side behind row joins the candidate class (R9): exit 2 wanted 1; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=DEGRADED oom=HEALTHY)
FAIL healthy: absent expac prints its absence, never a silent pass (R9): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL healthy: an unreadable join is printed, never silent (R9): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL healthy: oom watch clean over the retained window (S9-2): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL healthy: oom watch — embedded r8 baseline, both declared waves known (S9-2): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL healthy: oom watch — external baseline file, both waves known (S9-2): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL degraded: oom watch — a cluster not in the baseline is new and named (S9-2): exit 2 wanted 1; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=DEGRADED)
FAIL degraded: oom watch — a declared wave missing inside the window (S9-2): exit 2 wanted 1; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=DEGRADED)
FAIL healthy: oom watch — declared wave older than the window (retention loss only) (S9-2): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL degraded: oom watch — absent baseline never reads HEALTHY (S9-2): exit 2 wanted 1; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=DEGRADED)
FAIL degraded: oom watch — unreadable kernel-kill ledger is a named unknown (S9-2): exit 2 wanted 1; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=DEGRADED)
FAIL blocked: oom watch — window unreadable (S9-2): configured root not asserted at a field boundary (wanted root_dir=/fast/scratch/hyaku/tsukuroi-r46/C1ExecSelftestEnv/tmp space/tsukuroi-r3-2-selftest.XPZD1W/fx/blocked-oom-window/root; possible live-root read)
FAIL blocked: oom watch — no boot measured is not a clean window (S9-2): configured root not asserted at a field boundary (wanted root_dir=/fast/scratch/hyaku/tsukuroi-r46/C1ExecSelftestEnv/tmp space/tsukuroi-r3-2-selftest.XPZD1W/fx/blocked-oom-window-empty/root; possible live-root read)
FAIL blocked: oom watch — a window scan unreadable fails closed (S9-2): configured root not asserted at a field boundary (wanted root_dir=/fast/scratch/hyaku/tsukuroi-r46/C1ExecSelftestEnv/tmp space/tsukuroi-r3-2-selftest.XPZD1W/fx/blocked-oom-scan/root; possible live-root read)
FAIL healthy: the default -Qkk sample cap bounds the sample (S10-2): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL blocked: the rollup line names every plane field in order (S10-2): configured root not asserted at a field boundary (wanted root_dir=/fast/scratch/hyaku/tsukuroi-r46/C1ExecSelftestEnv/tmp space/tsukuroi-r3-2-selftest.XPZD1W/fx/blocked-rollup-mixed/root; possible live-root read)
FAIL blocked: update-safety -Sup unreadable fails closed (S10-2): configured root not asserted at a field boundary (wanted root_dir=/fast/scratch/hyaku/tsukuroi-r46/C1ExecSelftestEnv/tmp space/tsukuroi-r3-2-selftest.XPZD1W/fx/blocked-upd-sup-unreadable/root; possible live-root read)
FAIL healthy: C1 root arm — 0755 owner bits present (R12-C1): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL healthy: C1 root arm — 0555 owner-write absent is report-only (R12-C1): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL healthy: C1 root arm — owner-search absent independently (R12-C1): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL healthy: C1 root arm — both owner bits absent, both named (R12-C1): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL healthy: C1 root arm — 1777 sticky parses as octal, bits present (R12-C1): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL healthy: C1 root arm — 2755 setgid does not disturb owner bits (R12-C1): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL healthy: C1 root arm — 1555 sticky with owner-write absent, report-only (R12-C1): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL blocked: C1 root arm — missing metadata BLOCKED with explicit unknowns (R12-C1): configured root not asserted at a field boundary (wanted root_dir=/fast/scratch/hyaku/tsukuroi-r46/C1ExecSelftestEnv/tmp space/tsukuroi-r3-2-selftest.XPZD1W/fx/blocked-root-missing/no-such-root; possible live-root read)
FAIL blocked: C1 root arm — regular file is a non-directory (R12-C1): configured root not asserted at a field boundary (wanted root_dir=/fast/scratch/hyaku/tsukuroi-r46/C1ExecSelftestEnv/tmp space/tsukuroi-r3-2-selftest.XPZD1W/fx/blocked-root-regular-file/root-file; possible live-root read)
FAIL blocked: C1 root arm — dangling symlink is unavailable, not a pass (R12-C1): configured root not asserted at a field boundary (wanted root_dir=/fast/scratch/hyaku/tsukuroi-r46/C1ExecSelftestEnv/tmp space/tsukuroi-r3-2-selftest.XPZD1W/fx/blocked-root-dangling/root-link; possible live-root read)
FAIL blocked: C1 root arm — symlink loop is unavailable, never a pass (R12-C1): configured root not asserted at a field boundary (wanted root_dir=/fast/scratch/hyaku/tsukuroi-r46/C1ExecSelftestEnv/tmp space/tsukuroi-r3-2-selftest.XPZD1W/fx/blocked-root-loop/loop-a; possible live-root read)
FAIL blocked: C1 root arm survives pacman=missing early return (R12-C1): configured root not asserted at a field boundary (wanted root_dir=/fast/scratch/hyaku/tsukuroi-r46/C1ExecSelftestEnv/tmp space/tsukuroi-r3-2-selftest.XPZD1W/fx/blocked-root-early-pacman-missing/root; possible live-root read)
FAIL blocked: C1 root arm survives db.lck early return (R12-C1): configured root not asserted at a field boundary (wanted root_dir=/fast/scratch/hyaku/tsukuroi-r46/C1ExecSelftestEnv/tmp space/tsukuroi-r3-2-selftest.XPZD1W/fx/blocked-root-early-lck/root; possible live-root read)
FAIL blocked: C1 root arm survives empty-db early return (R12-C1): configured root not asserted at a field boundary (wanted root_dir=/fast/scratch/hyaku/tsukuroi-r46/C1ExecSelftestEnv/tmp space/tsukuroi-r3-2-selftest.XPZD1W/fx/blocked-root-early-empty-db/root; possible live-root read)
FAIL blocked: C1 root arm survives sample-rc early return (R12-C1): configured root not asserted at a field boundary (wanted root_dir=/fast/scratch/hyaku/tsukuroi-r46/C1ExecSelftestEnv/tmp space/tsukuroi-r3-2-selftest.XPZD1W/fx/blocked-root-early-qkk-rc/root; possible live-root read)
FAIL healthy: no ADJ-04 handoff line without a dated event (R32-C1): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL healthy: a dated kill event routes one kill-events handoff, value = the cluster count (R32-C1): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL degraded: boot-0 coredumps route one coredumps handoff, value = the boot-0 count (R32-C1): exit 2 wanted 1; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=DEGRADED journal=DEGRADED update-safety=HEALTHY oom=HEALTHY)
FAIL healthy: a cumulative vmstat oom_kill counter never routes a kill-events handoff (R32-C1): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL healthy: the drift arm counts pacdiff names and symlinks, never directories or near-names (R35-C1): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL healthy: the drift arm pairs /etc warnings by full path; unlogged and gone (R35-C1): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL healthy: an unreadable directory is reported, and its logged target is neither present nor gone (R35-C1): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL healthy: an absent log prints log=unreadable and zero log counts, never a pass on pairing (R35-C1): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL healthy: no btrfs sysfs root reads as no btrfs filesystem, 0/0/0 (R38-C1): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL healthy: five zero counters on one device; features and non-fsid names ignored (R38-C1): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=BLOCKED dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0 detail=11111111:1:speed-unreadable|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL healthy rollup: nonzero lifetime counters read DEGRADED on the STORAGE line only; 010 is ten, not octal (R38-C1): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=BLOCKED dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0 detail=11111111:1:speed-unreadable,aaaaaaaa:2:speed-unreadable|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL healthy rollup: a missing counter is BLOCKED; the healthy sibling device still counts (R38-C1): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=BLOCKED dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0 detail=11111111:1:speed-unreadable,11111111:2:speed-unreadable|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL healthy rollup: a repeated counter or extra line is malformed, never a pass (R38-C1): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=BLOCKED dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0 detail=11111111:1:speed-unreadable|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL healthy rollup: a mounted filesystem with no readable devinfo is BLOCKED (R38-C1): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL healthy rollup: a non-integer devid is BLOCKED and its name is never echoed (R38-W1 hardening): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=BLOCKED dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0 detail=11111111:?:bad-devid|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL healthy rollup: an unlistable btrfs sysfs root is BLOCKED, never a silent 0/0/0 (R38-W1 hardening): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=BLOCKED dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0 detail=sysfs:unreadable|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL healthy rollup: btrfs mounted with no sysfs root is BLOCKED, never 0/0/0 (R39-C1): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL healthy rollup: btrfs mounted with a root holding no fsid is BLOCKED (R39-C1): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL healthy rollup: an unreadable mount table with no sysfs root is BLOCKED (R39-C1): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL healthy: a root with an fsid entry is read and the mount table adds nothing (R39-C1): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=BLOCKED dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0 detail=11111111:1:speed-unreadable|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL healthy rollup: a FIFO as the mount table is BLOCKED and never read, so it cannot hang (R39-W1 hardening): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL healthy rollup: an empty mount table is no table, BLOCKED not 0/0/0 (R39-W1 hardening): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL healthy rollup: a btrfs /home on another device and options, not last, is BLOCKED (R40-C1): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL healthy rollup: one read-only btrfs mount among four lines, empty root, is BLOCKED (R40-C1): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL healthy: btrfs in the device, mountpoint or options of an ext4 line is no btrfs mount (R40-C1): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL healthy: the fstype match is exact, so BTRFS is not btrfs (R40-C1): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL healthy rollup: a btrfs line whose mountpoint is not absolute still counts, BLOCKED (R41-C1 H5): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL healthy rollup: a btrfs line whose source is not under /dev still counts, BLOCKED (R41-C1 H6): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL healthy rollup: a btrfs line with no subvol= option still counts, BLOCKED (R41-C1 H9): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL healthy rollup: two btrfs lines are still btrfs without sysfs, BLOCKED (R41-C1 H10): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL healthy rollup: an unlistable root keeps its one reason; the mount table is never added (R40-C1): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=BLOCKED dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0 detail=sysfs:unreadable|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL healthy: no record directory, no sysfs root, no wants directory reads NONE with zero counts (R44-C1): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL healthy: one readable record of a mounted fsid reads RECORDED; other names are ignored (R44-C1): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=RECORDED dir=present records=1 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL healthy: a 000 record is unreadable, a record of an unmounted fsid is an orphan, a _tmp counts apart (R44-C1): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=RECORDED dir=present records=2 tmp=1 sockets=0 unreadable=1 orphan=1 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL healthy: a nonzero scrub_speed_max counts as limited and is listed; 0 is no limit (R44-C1): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=1 timers=0 detail=11111111:2:speed_max=104857600|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL healthy rollup: a non-decimal limit is BLOCKED and a missing limit file is unreadable, never no-limit (R44-C1): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=BLOCKED dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0 detail=11111111:1:speed-malformed,11111111:3:speed-unreadable|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL healthy rollup: an unlistable record directory is BLOCKED, never an absent record (R44-C1): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=BLOCKED dir=unreadable records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0 detail=dir:unreadable|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL healthy: enabled scrub timer instances count by link name; the bare template and other timers do not (R44-C1): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=2|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL healthy rollup: a symlinked or directory record and a non-socket progress name are BLOCKED; a newline name is never echoed (R44-C1): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=BLOCKED dir=present records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0 detail=progress:not-socket,record:not-regular,record:not-regular|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL healthy rollup: records with no sysfs root to judge orphans by are BLOCKED (R44-C1): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=BLOCKED dir=present records=1 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0 detail=sysfs:absent|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL healthy: the probe pins LC_ALL=C so a collation-inflated name is never a uuid (R44-C1): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=NONE dir=present records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL healthy rollup: an empty scrub_speed_max line is malformed, never a silent no-limit (R44-C1): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=BLOCKED dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0 detail=11111111:1:speed-malformed|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL healthy: a zero-padded scrub_speed_max is still no limit (R44-C1): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL healthy: an in-progress _tmp record alone reads RECORDED with zero finished records (R44-C1): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=RECORDED dir=present records=0 tmp=1 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL healthy rollup: detail evidence precedes limit info in the detail join (R44-C1): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=BLOCKED dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=1 timers=0 detail=11111111:1:speed-malformed,11111111:2:speed_max=104857600|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL healthy rollup: a sysfs root that exists but is not a directory is BLOCKED, never a silent no-orphan scan (R44-C1): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=BLOCKED dir=present records=1 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0 detail=sysfs:not-directory|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL healthy: a directory named like a scrub timer is not an enabled instance (R44-C1): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL degraded: a large is-system-running output keeps its first line (R45-C1): exit 2 wanted 1; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=DEGRADED drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL degraded: a large timer Result output keeps its first line (R45-C1): exit 2 wanted 1; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=DEGRADED drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL healthy: a large nvidia-smi output keeps the first GPU line (R45-C1): exit 2 wanted 0; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)
FAIL blocked: a large is-active output keeps its first word, trailing blanks and CR dropped (R45-C1): configured root not asserted at a field boundary (wanted root_dir=/fast/scratch/hyaku/tsukuroi-r46/C1ExecSelftestEnv/tmp space/tsukuroi-r3-2-selftest.XPZD1W/fx/r45-boottarget-large/root; possible live-root read)
FAIL degraded: a large timer ActiveState output keeps its first line (R45-C1): exit 2 wanted 1; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=DEGRADED update-safety=HEALTHY oom=HEALTHY)
FAIL degraded: a foreign baseline past the pipe buffer still finds its last row (R45-C1): exit 2 wanted 1; output: SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0|TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=DEGRADED oom=HEALTHY)
```
