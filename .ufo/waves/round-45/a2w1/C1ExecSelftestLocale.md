VERDICT: supports

# Item C1-2 — census selftest count (148 -> 154) and locale invariance

Seat: C1ExecSelftestLocale (L2, wave a2w1). Judged axis: operability, C1.
Everything below was measured in this seat; no counter (C1/C2) was run, only the census script's own
`--selftest`. Receipts: `.ufo/waves/round-45/a2w1/C1ExecSelftestLocale/` (same directory basename as this
report, per the wave rule). Scratch: `/fast/scratch/hyaku/tsukuroi-r45/C1ExecSelftestLocale/` (removed at exit).

## 1. Revisions exported

```
$ git -C <lane> show 18389f44cf6ce414d7be205998b29c79fb0b490c:tools/tsukuroi-census.sh > impl/tsukuroi-census.sh
$ git -C <lane> show 5bbd5ff588120fd8e7c744695351a6978b4241c1:tools/tsukuroi-census.sh > base/tsukuroi-census.sh
237b21c9d757e339943c29b0f005faf569ff997deca46dd5bce16bc631b5fcdc  impl/tsukuroi-census.sh   (3485 lines)
17c82406fe7a7d06261b1fb2ac4be56e7d5498c6712ae90fe8233d2bb0e81a35  base/tsukuroi-census.sh   (3441 lines)
```

Lane workspace HEAD at seat start: `git -C <lane> rev-parse --short HEAD` -> `3c42f556` (the lane tip has
moved past the frozen implementation commit; the file was still exported from the frozen revisions, not from
the worktree).

## 2. Selftest counts — measured

| revision | command (TMPDIR inside scratch) | result | rc | wall |
|---|---|---|---|---|
| `18389f44` | `TMPDIR=<scratch>/run2/tmpimpl bash impl/tsukuroi-census.sh --selftest` | `TSUKUROI_CENSUS_SELFTEST: PASS (154 cases, 154 passed, 0 failed)` | 0 | 32.4 s |
| `5bbd5ff5` | `TMPDIR=<scratch>/run2/tmpbase bash base/tsukuroi-census.sh --selftest` | `TSUKUROI_CENSUS_SELFTEST: PASS (148 cases, 148 passed, 0 failed)` | 0 | 31.7 s |

`grep -c '^PASS'` / `grep -c '^FAIL'` on the two logs: 154 / 0 and 148 / 0. Both expectations in the claim
(154 at impl, 148 at base) hold, and both runs are clean (no FAIL line in either).

Case-set delta is exactly the six new cases and nothing else — `diff -u base-cases.txt impl-cases.txt`
(`sed 's/ (exit .*)//'` applied to the PASS lines so only the label text is compared) yields one hunk of six
added lines at base position 143-148, with all 148 base labels byte-identical:

```
@@ -143,6 +143,12 @@
 PASS healthy: a directory named like a scrub timer is not an enabled instance (R44-C1)
+PASS degraded: a large is-system-running output keeps its first line (R45-C1)
+PASS degraded: a large timer Result output keeps its first line (R45-C1)
+PASS healthy: a large nvidia-smi output keeps the first GPU line (R45-C1)
+PASS blocked: a large is-active output keeps its first word, trailing blanks and CR dropped (R45-C1)
+PASS degraded: a large timer ActiveState output keeps its first line (R45-C1)
+PASS degraded: a foreign baseline past the pipe buffer still finds its last row (R45-C1)
 PASS cli: unknown argument exits 2 with usage (S10-2)
```

`grep -c 'R45-C1'` = 6 at impl, 0 at base — the six cases exist only in the implementation revision.

## 3. The six `(R45-C1)` labels with line numbers

`tools/tsukuroi-census.sh` @ `18389f44` (`grep -n "check '.*(R45-C1)'"`):

| line | label | expected rc / verdict |
|---|---|---|
| 3342 | `degraded: a large is-system-running output keeps its first line (R45-C1)` | 1 / DEGRADED |
| 3347 | `degraded: a large timer Result output keeps its first line (R45-C1)` | 1 / DEGRADED |
| 3355 | `healthy: a large nvidia-smi output keeps the first GPU line (R45-C1)` | 0 / HEALTHY |
| 3360 | `blocked: a large is-active output keeps its first word, trailing blanks and CR dropped (R45-C1)` | 2 / BLOCKED |
| 3365 | `degraded: a large timer ActiveState output keeps its first line (R45-C1)` | 1 / DEGRADED |
| 3374 | `degraded: a foreign baseline past the pipe buffer still finds its last row (R45-C1)` | 1 / DEGRADED |

All six PASS with that verdict and exit code in every run listed in section 4.

The five production readers the claim names are at the claimed places, and the base's pipe form is gone:

* `state` — `impl:965`, inside `probe_systemd()` (`impl:955`); base `:965` `state=$(printf '%s\n' "$CAP_OUT" | head -n1 | tr -d '\r' | sed -E 's/[[:space:]]+$//')` -> impl `state=${CAP_OUT%%$'\n'*}; state=${state//$'\r'/}; state=${state%"${state##*[![:space:]]}"}`.
* timer `Result` `r` — `impl:1003`, `probe_systemd()`; `r=${CAP_OUT%%$'\n'*}; r=${r//$'\r'/}` (base piped `head -n1 | tr -d '\r'`).
* `driver` — `impl:1085`, `probe_drivers()` (`impl:1021`); first line now by parameter expansion, the `awk -F', *' '{print $NF}'` still runs on the already-extracted single line (not on `$CAP_OUT`).
* `t_word` — `impl:1460`, `probe_journal()` (`impl:1428`).
* timer `ActiveState` `r` — `impl:1535`, `probe_journal()`.

Live occurrences of the old form in the implementation: `grep -F "printf '%s\n' \"\$CAP_OUT\" | head -n1" impl/tsukuroi-census.sh`
matches **one** line, `impl:3334`, which is the explanatory comment ("output through `` `printf '%s\n' "$CAP_OUT" | head -n1` `` in an assignment. Under `set -euo pipefail` ..."). Zero executable occurrences; base has 5 (`base:965,1003,1085,1460,1535`). Other `head -n1` uses in impl (`:669` file-first-line, `:832` pacman.conf HoldPkg, `:1025` dmesg_restrict, `:2292/:2302` selftest assertions, `:3414` hostname file) are not the five readers and are outside this item.

Payload sizes that make the cases bite, and why the sizes are enough (measured):
`awk` re-run of the case pad generators (`r45pad` at `impl:3338`, 2000 lines each): `sysrunning` pad
**162,000 bytes**, `result` pad **154,000**, nvidia-smi pad **210,000**, `active` pads **154,000** each (used
twice, cases at `impl:3360` and `impl:3365`), and the foreign-baseline pads (`impl:3370`/`impl:3373`)
**88,000 bytes** for 2000 rows. Every pad exceeds the host's default pipe capacity, read here as **65,536
bytes** (`python3 -c "fcntl.fcntl(w,1032)"` on a
fresh `os.pipe()`), with `/proc/sys/fs/pipe-max-size` = 1,048,576. So the deciding first line sits in front of
more than one pipe buffer of padding, as the claim states.

## 4. Locale runs (implementation revision only)

`locale -a` on this host offers `C`, `C.utf8`, `en_US.utf8`, `POSIX`; ambient locale is `LANG=en_US.UTF-8`
with `LC_ALL=` unset (verified with `locale`). bash is 5.3.20(1)-release.

| setting | result | rc | wall | receipt |
|---|---|---|---|---|
| ambient (`LANG=en_US.UTF-8`, `LC_ALL` unset) | PASS 154/154 | 0 | 32.4 s | `impl-selftest.txt` |
| `LC_ALL=C` | PASS 154/154 | 0 | 53.7 s | `loc-C.txt` |
| `LC_ALL=C.UTF-8` | PASS 154/154 | 0 | 57.6 s | `loc-CUTF8.txt` |
| `LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8` | PASS 154/154 | 0 | 54.5 s | `loc-US.txt` |
| `LC_ALL=C` (paired re-run) | PASS 154/154 | 0 | 44.9 s @ load 21.7->23.2 | `loc-C-run4.txt` |
| `LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8` (paired re-run) | PASS 154/154 | 0 | 60.7 s @ load 23.2->35.5 | `loc-US-run4.txt` |

**No case changes outcome by locale.** Three independent checks:

1. Full outcome sets are identical: after stripping the `(exit N, VERDICT)` suffix, the 154-line case list of
   each locale run is byte-identical to the ambient-locale run (`diff -q` empty for `loc-C`, `loc-CUTF8`,
   `loc-US`; outputs: "identical 154-case outcome set to default-locale run" x3).
2. The six `(R45-C1)` PASS lines are byte-identical across all four locale runs:
   `grep 'R45-C1' <log> | sha256sum | cut -c1-16` = `dcb085d9f5ae8d17` for `impl-selftest.txt`, `loc-C.txt`,
   `loc-CUTF8.txt`, `loc-US.txt` (6 R45-C1 PASS, 0 FAIL in each).
3. FAIL counts are 0 in every run; the per-run summary line is `PASS (154 cases, 154 passed, 0 failed)`.

The selftest propagates the caller's locale into the census it re-invokes: it calls
`env <TSUKUROI_* overrides> "${EXTRA_ENV[@]}" "$BASH" "$SELF"` (`impl:2258`-`impl:2288`, with
`EXTRA_ENV=()` reset at `impl:2247`), which neither sets nor
clears `LC_ALL`/`LANG`, so the three runs above really exercised the five readers under each locale rather
than only the driver.

### Why the conversions are (largely) locale-invariant — and where they are not

Probe `probe_cp.py` (receipt) runs the exact conversion
`s=${s//$'\r'/}; s=${s%"${s##*[![:space:]]}"}` on `val<CP><CP>` for 24 codepoints under each locale:

```
C            stripped: U+0020 U+0009 U+000B U+000C U+000D
C.UTF-8      stripped: U+0020 U+0009 U+000B U+000C U+000D U+1680 U+2000 U+2001 U+2002 U+2003 U+2004 U+2005 U+2006 U+2008 U+2009 U+200A U+2028 U+2029 U+205F U+3000
en_US.UTF-8  stripped: (same 20 as C.UTF-8)
C            kept:     U+0085 U+00A0 U+1680 U+2000 ... U+205F U+3000
C.UTF-8      kept:     U+0085 U+00A0 U+2007 U+202F
```

* `${x//$'\r'/}` removes a literal CR byte and `${CAP_OUT%%$'\n'*}` cuts at a literal newline: no multibyte
  encoding used by the host's installed locales can hide `0x0D`/`0x0A` inside a character, so first-line and
  CR handling are locale-invariant (`firstline-utf8=[first line pad]`, `cr-strip` keeps `©`/`à` intact in all
  three locales — probe output).
* The trailing-blank strip `[![:space:]]` **is** locale-sensitive for Unicode space *separators*. Under
  `C`/`POSIX` it matches only ASCII whitespace and leaves 15 codepoints intact; under every UTF-8 locale here
  it also strips `U+1680, U+2000-U+2006, U+2008-U+200A, U+2028, U+2029, U+205F, U+3000`. `U+0085` (NEL),
  `U+00A0` (NBSP), `U+2007` (figure space) and `U+202F` (narrow NBSP) are kept in all three locales.
* Consequence for the base statement: GNU sed's `[[:space:]]` does **not** strip those 15 codepoints in any
  locale on this host (`printf 'val\xe2\x80\x83' | LC_ALL=en_US.UTF-8 sed -E 's/[[:space:]]+$//'` -> hex
  `76616ce28083`, EM SPACE retained, same under `C`; sed is multibyte-aware, `printf '\xc3\xa4' | sed 's/./X/'`
  -> `580a`). So on a *UTF-8* locale the new parameter expansion strips a trailing EM/IDEOGRAPHIC SPACE that
  the base's sed kept. This is a real, narrow semantic difference between the two statements, but it is
  invisible to this item's cases (all six fixtures are pure ASCII: `r45pad` pads with spaces and `.`, the
  foreign-baseline pad is ASCII package names) and it does not affect the counted verdict: the counter pins
  `LC_ALL=C` for its statement evaluation (`tools/score-census-readers-r45.py:108`, `e['LC_ALL'] = 'C'`),
  where both forms keep those bytes. Direction of the difference: the new form agrees with the C-pinned
  counter, and the production outputs (systemd state/Result/ActiveState, nvidia-smi driver field, journal
  word) are ASCII.

### Timing, with the caveat that the host was loaded

Whole-suite wall times above are **not** a clean locale comparison: the fleet was running many peers
(`/proc/loadavg` 1-min value observed at 19.06, 21.68, 23.19, 35.46 during these runs), the suite spawns the
whole census process tree 154 times, and the paired re-runs drifted in load in the wrong direction for the
UTF-8 arm. The isolated measurement is `bench_locale.sh` (receipt): 2000 iterations of the exact five-site
conversion on a 140,011-byte captured string, per locale —

```
C            2000 iters on 140011 bytes: 317209 us total, 158 us/iter, result=[degraded]
C.UTF-8      2000 iters on 140011 bytes: 985568 us total, 492 us/iter, result=[degraded]
en_US.UTF-8  2000 iters on 140011 bytes: 951156 us total, 475 us/iter, result=[degraded]
```

So one first-line extraction costs ~0.16 ms in `C` and ~0.48 ms in a UTF-8 locale (bash pattern matching is
multibyte-aware there) — ~0.3 ms extra per reader, at most ~1.5 ms per census run, i.e. below the noise of the
suite and irrelevant to the 141-exit defect this change removes. The extracted value is identical
(`result=[degraded]`) in all three locales.

## 5. What I did not do

* Did not run either counter (`score-census-readers-r45.py`, `check-scrub-grounding-r45.py`); the six revert
  mutants, the per-site equivalence leg on drawn outputs and the adjacency leg are other seats' items and the
  claim's `revert_killed == 6` / `equiv_ok == 5` are therefore unverified by this seat.
* Did not run the base revision's selftest under `LC_ALL=C` (only at ambient locale); the item asks for the
  locale sweep at the implementation revision only.
* Did not exercise a non-ASCII live capture (would need host mutation or a fixture run outside the selftest);
  the UTF-8-space difference in section 4 is inferred from the isolated probe on the same two statements, not
  from a census run.
* Did not verify the live census's exit-141 behaviour end-to-end; the six cases passing at 162,000-byte
  payloads is the only evidence here that the defect class is closed.

## 6. Risks / notes

* Host contention (load 19-35) makes any wall-time claim from this seat +/- 50 %; only the micro-benchmark is
  comparable. No check was run in parallel with another C1 counter in this seat.
* The trailing-strip locale difference (section 4) is a behavioural difference between base and impl for a
  first line ending in a Unicode space separator under a UTF-8 locale; if the counter's equivalence leg is
  ever re-pinned to a UTF-8 locale, that leg would flag the five conversion sites. As frozen (`LC_ALL=C` at
  `tools/score-census-readers-r45.py:108`) it does not.
* Attempt-1 remnants exist in this seat's scratch path (`/fast/scratch/hyaku/tsukuroi-r45/C1ExecSelftestLocale/`
  held `base.selftest.log`, `impl.selftest.log`, `selftest.LC_ALL=C.log` dated 23:52-23:55 before I started).
  None of them is cited: every number above comes from the runs listed here, in `run2/`, `run3/`, `run4/`,
  whose logs are copied into this seat's receipt directory.
* Tooling: nothing installed or upgraded; no pacman, no PATH writes. Timing used bash's `TIMEFORMAT` (the
  `~/.local/bin/time` on PATH was not used), the pipe-capacity probe used `python3` + `fcntl` only.
