VERDICT: supports

# C1-11 — the seven unclaimed `| head` readers at `18389f44` (masked status / process substitution)

Item: the declaration names seven `| head` production readers it does NOT claim; drive each past the pipe
buffer and show (a) the census exit status is unchanged and (b) the value read is still right. Any that can
kill the census or reads a wrong value would falsify the declaration's limit text.

Result: **none of the seven kills the census and none reads a wrong value**, at payloads 4.7x-9.6x the pipe
buffer, with the producer observably SIGPIPE'd in six of the seven. The declaration's limit text stands.

## 1. Limit text under test (quoted)

`SCORECARD.md:2881-2883` (lane root):
> "the seven masked or process-substitution `| head` readers (`:707`, `:832`, `:997`, `:1196`, `:1517`,
> `:1531`, `:1817`) cannot kill the census (their status is ignored or `|| true`) and are not claimed; the
> readers are latent defects on this host, whose outputs are far below the pipe buffer."

## 2. The set is exactly those seven, and the seven lines are untouched bytes

Command (lane root), on the census blob at the implementation commit:

```
$ git cat-file -p 18389f44cf6ce414d7be205998b29c79fb0b490c:tools/tsukuroi-census.sh | grep -n '| *head' | awk -F: '$1<2046'
707:  mapfile -t names < <(printf '%s\n' "$CAP_OUT" | grep -v '^[[:space:]]*$' | head -n "$SAMPLE_N")
723:  # Round 42 ... never `printf | grep -q` / `| grep -m1` / `| head` under pipefail ...      <- comment, not a reader
832:      | head -n1 | sed -E 's/^[[:space:]]*HoldPkg[[:space:]]*=[[:space:]]*//' || true)
997:  mapfile -t timers < <(printf '%s\n' "$CAP_OUT" | awk 'NF && $1 ~ /\.timer$/ {print $1}' | head -n "$TIMER_SCAN_MAX")
1196:             -print 2>/dev/null | LC_ALL=C sort | head -n 4000)
1517:      | sort -u | head -n 6 | paste -sd, - || true)
1531:  mapfile -t timers < <(printf '%s\n' "$CAP_OUT" | awk 'NF && $1 ~ /\.timer$/ {print $1}' | head -n "$TIMER_SCAN_MAX")
1817:      unk_names=$(printf '%s\n' "$cl_out" | grep '^?' | sed 's/^?//' | head -n6 | paste -sd, - || true)
```

Seven readers (723 is a comment line containing the token `| head` in prose), three forms:
process substitution `mapfile < <(...)` (:707, :997, :1531), process substitution `while ... done < <(...)`
(:1196), `x=$(... | head ... || true)` (:832, :1517, :1817). Matching the declaration exactly.

Untouched-bytes check — `sed -n '707p;832p;997p;1196p;1517p;1531p;1817p'` piped to sha256sum at base
`5bbd5ff5…` vs impl `18389f44…` prints the same digest `a04ddba8d0de28b36c56eefbbf3c62da4db183302b2c3db8d7ae9c05e49c342d`
for both, and `diff` is empty ("SEVEN READER LINES BYTE-IDENTICAL base vs impl"): these are unmodified latent
sites, not part of the C1 change.

Census blob provenance: `sha256sum census.sh` = `237b21c9d757e339943c29b0f005faf569ff997deca46dd5bce16bc631b5fcdc`,
identical to `git cat-file -p 18389f44:tools/tsukuroi-census.sh | sha256sum`
(`C1ExecMaskedSites/census-provenance.txt`).

## 3. Method (fixture harness at `18389f44`)

The census is fully path-override-able, so each site was driven **end to end through its real code path** by
running the census at `18389f44` against the revision's own selftest fixture mechanism:

- `C1ExecMaskedSites/bin/.dispatch` — the revision's selftest dispatcher, extracted verbatim from
  `census.sh:2056-2127` (answers `pacman -Qq`, `pacman -Qm`, `pacman-conf`, `systemctl`, `journalctl`, … from
  `$TSUKUROI_FIXTURE`).
- `C1ExecMaskedSites/fxfn.sh` — `fx_default()`, the revision's clean fixture tree, extracted verbatim from
  `census.sh:2140-2229`.
- `C1ExecMaskedSites/h.sh` — the census runner with the same environment override list the selftest's `check()`
  uses (`census.sh:2249-2327`, env block `2258-2289`), capturing stdout and the real exit code.
- For each site, **a SMALL and a PAD fixture pair with the same leading rows**, so the exit code and the read
  value are directly comparable: SMALL keeps the deciding content and totals below the pipe buffer, PAD keeps
  the same first rows and adds enough rows that the deciding pipeline's producer must be SIGPIPE'd.

Pipe buffer on this host, measured: `fcntl(F_GETPIPE_SZ)` on a fresh `os.pipe()` = **65536 bytes**
(`/proc/sys/fs/pipe-max-size` = 1048576). Every PAD payload is 96 KB - 638 KB of *pipeline* output, i.e.
1.5x - 9.7x the buffer.

`C1ExecMaskedSites/probe.sh` replays each exact pipeline text on the padded bytes and prints `PIPESTATUS`
immediately (the "is the producer actually SIGPIPE'd" leg); `C1ExecMaskedSites/pc.sh` is the positive control
(the same bytes through the unmasked shape); `C1ExecMaskedSites/cases.sh` builds and runs all fixtures.

## 4. Per-site result (pairs; `C1ExecMaskedSites/fields.txt`, `summary.txt`)

| site | form | padded payload | producer status (`probe.log`) | census rc small -> pad | value small -> pad | value right? |
|---|---|---|---|---|---|---|
| `:707` | `mapfile < <(printf\|grep -v\|head -n 8)` | `pq` 96,056 B | `PIPESTATUS=0 141 0` (grep SIGPIPE) | 0 -> **0** (HEALTHY) | `sample=8(pkg-01…pkg-08)` -> identical | yes: first 8 of 2008 rows |
| `:832` | `holds=$(grep -hE HoldPkg\|head -n1\|sed … \|\| true)` | `pacman.conf` 115,023 B, all matching | `PIPESTATUS=141 0 0` (grep SIGPIPE) | 0 -> **0** | `holds=pacman glibc;` -> identical | yes: first HoldPkg row |
| `:997` | `mapfile < <(printf\|awk\|head -n 12)` | `timerlist` 2001 rows | `PIPESTATUS=141 141 0` | 1 -> **1** (DEGRADED) | `timers_enabled` 1 -> 2001 (= exact row count), `timers_scanned` 1 -> 12 (= `TIMER_SCAN_MAX`), scanned names = first 12 rows in fixture order | yes |
| `:1196` | `while … done < <(find\|sort\|head -n 4000)` | 1505 / 4205 `memory.events` paths (227 KB / 638 KB) | `PIPESTATUS=0 0 0` on the sample runs; **1 in 20 repeats showed `… 141 0 0`** (sort SIGPIPE) | 0 -> **0** (both) | `C4_sweep` 5 -> **1505** (full sweep, cap not hit) and 5 -> **4000** (cap hit at 4205 candidates) | yes |
| `:1517` | `fh_names=$(…\|grep -E\|grep -oE\|sort -u\|head -n 6\|paste \|\| true)` | `journal-err.json` 3006 distinct units | `PIPESTATUS=0 0 0 141 0 0` (sort SIGPIPE) | 1 -> **1** | `failedhist=6[aa-fail-01…06]` -> `failedhist=3006[aa-fail-01…06]` | yes: same 6 names (first 6 sorted of 3006) |
| `:1531` | `mapfile < <(printf\|awk\|head -n 12)` | `timerlist` 2001 rows | `PIPESTATUS=141 141 0` | 1 -> **1** | `timer_drift` 1 -> 12, `armed=0`, `timers_scanned` 1 -> 12, names = first 12 rows | yes |
| `:1817` | `unk_names=$(printf\|grep '^?'\|sed\|head -n6\|paste \|\| true)` | `pm` 3006 unknown rows, `cl_out` 162,108 B | `PIPESTATUS=0 141 141 0 0` (grep, sed SIGPIPE) | 1 -> **1** | `unknown-provenance=[zz-unk-01…zz-unk-06]` -> identical | yes: first 6 in input order |

Exit codes are stable across three full runs of every PAD fixture (`C1ExecMaskedSites/repeats.log`: 2 extra
runs each, 7/7 identical rc and verdict; the run in `cases.sh` is the third). No run exited 141.

Two extra "deciding row is last" fixtures, i.e. the reader must reach the *end* of the padded stream
(`C1ExecMaskedSites/lastrow.log`):

```
x832-last  rc=0 verdict=HEALTHY  holds=pacman glibc;          # 2500 non-matching lines, then the one HoldPkg row
x1517-last rc=1 verdict=DEGRADED failedhist=1[zz-late-only.service]   # 3000 non-matching entries, then the one failure
```

And a single *over-buffer first line* (72,011 B), the sharpest truncation case for `head -n1` behind `|| true`
(`C1ExecMaskedSites/longline.log`): `masked rc=0 value_bytes=72000` — the whole first HoldPkg value is
captured (4000 tokens), nothing is cut at the 64 KiB boundary.

## 5. Positive control: the masking is what saves them

The same padded bytes through the *unmasked* shape, under `set -euo pipefail`, in a child shell
(`C1ExecMaskedSites/pc.log`):

```
PC :707 x=$(printf|head -n1) in assignment                        rc=141  [killed by SIGPIPE]
PC :707 x=$(printf|grep -v|head -n8) in assignment                rc=141  [killed by SIGPIPE]
PC :832 holds=$(grep|head -n1|sed) with || true REMOVED           rc=141  [killed by SIGPIPE]
PC :997 timers=$(printf|awk|head -n12) without process substitution rc=141  [killed by SIGPIPE]
PC :1531 same, journal timerlist                                   rc=141  [killed by SIGPIPE]
PC :1517 fh_names=$(...|sort -u|head -n6|paste) with || true REMOVED rc=141  [killed by SIGPIPE]
PC :1817 unk_names=$(printf|grep ^?|sed|head -n6|paste) with || true REMOVED rc=141  [killed by SIGPIPE]
PC :1196 sweep=$(find|sort|head -n4000) as an assignment (pad-b, 637 KB) rc=0
PC CONTROL :707 sub-buffer payload (56 B) as the same assignment   rc=0
```

So for six of the seven, the payload provably crosses the buffer (the claimed-defect shape dies 141 on it),
and the census survives only because the pipeline status is discarded. The masked forms on the same bytes,
under `set -euo pipefail`, keep the right value:

```
832 masked: rc=0 holds=[pacman glibc]
707 masked: rc=0 n=8 last=pkg-08
1517 masked: rc=0 fh=[aa-fail-01.service,…,aa-fail-06.service]
1817 masked (census fold shape): rc=0 unk=[zz-unk-01,…,zz-unk-06]
```

Process-substitution status cannot escape the substitution either, measured directly on a 200,000-line
producer (one SIGPIPE'd `head -n 3`, one `head -n 4000`):

```
process-substitution survivor rc=0 n=3 first=1 last=3
while-read survivor rc=0 n=4000
```

## 6. Observations recorded (they do NOT falsify the limit text; recorded so a later reader does not over-read it)

1. `:1196` is not "over the buffer therefore SIGPIPE'd": it is a **race**. 20 repetitions of the exact pipeline
   on the 638 KB candidate list gave `0 0 0` nineteen times and `0 141 0` once — `sort` sometimes still has
   data in flight when `head -n 4000` exits. Either way the enclosing `while` loop cannot see it (process
   substitution), which is exactly the declaration's "status is ignored".
2. `:1196`'s `head -n 4000` is a real truncation of *data*, by design (`census.sh:1179` "C4 — cgroup presence
   flags, bounded sweep over memory.events[.local]"): 4205 candidate files report `C4_sweep=4000`, and the
   note carries no signal that the cap was hit. On this host the live sweep is ~95 files, so nothing is lost
   today; this is a property of the bounded sweep, not of the pipe buffer, and the declaration does not claim
   otherwise.
3. Same class for `:997` / `:1531`: `TIMER_SCAN_MAX=12` (`census.sh:480`) caps the `show` loop while
   `timers_enabled` reports the full count; both numbers are printed in the note (`timers_enabled=2001
   timers_scanned=12`), so a drifting timer beyond the 12th is invisible to `timer_drift` but the gap is
   visible in the same line. Also by design and consistent with the limit text.

## 7. Evidence files (all relative to the lane root)

- `.ufo/waves/round-45/a2w1/C1ExecMaskedSites/fields.txt` — the table of §4, extracted from the run outputs
- `…/summary.txt`, `…/repeats.log` — per-case rc/verdict, three runs per PAD fixture
- `…/s707-*.out|.rc`, `s832-*`, `s997-*`, `s1531-*`, `s1196-*`, `s1517-*`, `s1817-*` — full census stdout + rc per case
- `…/probe.log` — exact pipeline text replayed on the padded bytes with `PIPESTATUS`
- `…/pc.log` — positive controls (unmasked shape => 141) and masked forms with values
- `…/lastrow.log`, `…/longline.log` — deciding-row-last and over-buffer-first-line truncation probes
- `…/census-provenance.txt` — blob sha256 of the census used vs the blob at `18389f44`
- `…/h.sh`, `…/cases.sh`, `…/probe.sh`, `…/pc.sh`, `…/fxfn.sh`, `…/r6classes.txt` — the harness as run

## 8. What I did not do

- No live-host run: the census was driven only through fixture stubs (the live path's shell-variable and
  pipeline semantics are identical, but the live host's own outputs are far below the pipe buffer, so no
  live run could exercise the class at all — this is also the declaration's own premise).
- Did not run `tools/score-census-readers-r45.py` (it scores the five *claimed* readers, not these seven) and
  did not run the census selftest.
- Did not test payloads above 638 KB per site (no behavioural difference expected: the 141 positive control
  already fires above 64 KiB).
- No tool installs or upgrades were needed; no host state was touched; scratch was under
  `/fast/scratch/hyaku/tsukuroi-r45/C1ExecMaskedSites/` and was removed at the end.
