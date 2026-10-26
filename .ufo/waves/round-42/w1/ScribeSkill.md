VERDICT: draft

# ScribeSkill — round 42 / w1, item D-1 (two append-only SKILL.md sections)

Drafted 2026-10-26 by wave seat `ScribeSkill` (scribe, axes operability + depth). Lane tip at dispatch
`f50c28d83e1832ecd7eba765caace531f45d6b27`; implementation commit `447662088dfd3155e31aed239179a79c1d1046c7`;
base `c8efaa3f120834541f8de1e5e0367e8d1593bae6`. Nothing below is a product edit: the two sections are proposals
for the L1 to append to `SKILL.md`, and every cell I wrote from a lane file names that file.

## What I did (and did not do)

- Read the style of the last four appended sections of `SKILL.md` (`SKILL.md:-260` = `:3588-3847` of 3847):
  `Appended <date> (round-N <item>; drafted by wave seat <seat>, integrated by the L1).` opening, prose, tables,
  a `Counting:` paragraph with the counter command, predicate sentence and frozen sha256, then a `Limits` bullet
  list. Both drafts copy that shape.
- Read the C1 evidence: the diff of `44766208` (`git show 447662088dfd3155e31aed239179a79c1d1046c7 -- tools/tsukuroi-census.sh`),
  the base and tip census text, `.ufo/waves/round-42/before/c1-before.jsonl`, `.ufo/waves/round-42/impl/c1-able-to-fail.txt`,
  `.ufo/waves/round-42/controls/battery-summary-c1.jsonl` + `C1-K0.jsonl`/`C1-K6.jsonl`, the frozen counter
  `tools/score-size-invariance-r42.py:1-70`, and the wave-1 executor receipt
  `.ufo/waves/round-42/w1/C1ExecRerun/c1-after-4476620.jsonl` (peer seat, not mine).
- Read the C2 evidence: `corpus/knowledge/btrfs-scrub-record-r42.md` (whole, 159 lines), the frozen counter
  `tools/check-scrub-record-r42.py:1-90`, `.ufo/waves/round-42/before/c2-before.jsonl`,
  `.ufo/waves/round-42/frozen/hostcap/capture.txt` (10 lines), and the declaration rows (`SCORECARD.md:2573-2574`).
- **Did not run** either counter or the census selftest. Wave-1 peer seats already hold those receipts and this
  item is a draft; the host is loaded and counters must not overlap. The receipt pointers in the drafts are the
  files that exist, plus a marked place for the round-close `after/` receipt, which is empty at dispatch.
- Did not touch product code, the census, the counters, any tracked lane file besides this report and this seat
  dir, or the host. No tool was installed or upgraded. Scratch `/fast/scratch/hyaku/tsukuroi-r42/ScribeSkill` held
  no fixture and is removed.

## Evidence spine

| Claim | Evidence |
|---|---|
| base census reads wrong on the `-Qkk` error shape: large twin rc 0 where small twin rc 2 (P1, P3, P6) | `.ufo/waves/round-42/before/c1-before.jsonl` result line `per_case` `{"P1":{"small_rc":2,"large_rc":0}, "P3":(2,0), "P6":(2,0)}`, `invariant 3`, `non_invariant ["P1","P3","P6","U1","U2","U3","U4"]` |
| base census dies 141 on the update lists (U1-U3 rc 141 vs small 1; U4 141 vs 0) | same receipt, `per_case` U1-U4 `large_rc 141`, `ns_cases N1/N3/N6 invariant false`, `ns_invariant 0`, `verdict FAIL`, `exit_code 1`, 19:29:20Z→19:29:59Z |
| base selftest is 128 cases | same receipt `selftest_pass 1`, `selftest_label "PASS (128 cases, 128 passed, 0 failed)"` |
| fix reaches the predicate at `4476620` | `.ufo/waves/round-42/w1/C1ExecRerun/c1-after-4476620.jsonl` result: `cases 10, invariant 10, ns_invariant 3, selftest_pass 1, default_equal 1, verdict PASS`, `exit_code 0`, selftest label `PASS (130 cases, 130 passed, 0 failed)`, 19:41:06Z→19:41:50Z — **wave-1 executor's rerun receipt**, not the frozen `after/` receipt (`.ufo/waves/round-42/after/` is empty) |
| fix is able to fail | `.ufo/waves/round-42/impl/c1-able-to-fail.txt` — hybrid (base plane bodies + implementation selftest) prints `FAIL blocked: … exit 0 wanted 2; output: … TSUKUROI_CENSUS: HEALTHY (packages=HEALTHY …)` and `FAIL degraded: … exit 141 wanted 1; output: tsukuroi-census census-v2 — host=fixture-host — … read-only` |
| pre-data controls: every mutant rejected, candidate accepted | `.ufo/waves/round-42/controls/battery-summary-c1.jsonl` `{"control_accepted":1,"controls":{"K0":"FAIL",…,"K6":"PASS","K7":"FAIL","K8":"FAIL"},"should_fail_accepted":0}`; `C1-K6.jsonl` result `cases 10, invariant 10, ns_invariant 3, verdict PASS` |
| fixed sites, base→tip lines | base text via `git show c8efaa3f:tools/tsukuroi-census.sh` (`:692,:694,:1621,:1635,:1641,:1652`); tip text `grep -n` → `:695,:697,:1624,:1639,:1645,:1655` |
| the two new cases and their labels | `tools/tsukuroi-census.sh:2357` (blocked large `-Qkk`) and `:2564` (4002 candidates); fixtures at `:2352-2356`, `:2558-2563` |
| counter predicate + 64 KiB buffer + 1 MiB padding | `tools/score-size-invariance-r42.py:43`, `:61`, `:62`, `:369`; sha256 `c511104a…53e03` (`sha256sum`); buffer measured read-only this session: `python3 -c "import os,fcntl; r,w=os.pipe(); print(fcntl.fcntl(w,1032))"` → `65536`; shell `bash --version` → `GNU bash, version 5.3.20(1)-release` |
| C2 before: entry absent | `.ufo/waves/round-42/before/c2-before.jsonl` `rows 0, quotes_ok 0, verdicts_ok 0, verdict FAIL, exit_code 1` |
| C2 counter predicate + row tokens/windows + binding | `tools/check-scrub-record-r42.py:30`, `:240`, `:244`, `ROWS` (`:54-62`), `OPENED` (`:63`), verdict regex (`:66`); sha256 `dbe933ec…0503f` |
| entry rows SC1-SC5, S237/S238/S239, host readings | `corpus/knowledge/btrfs-scrub-record-r42.md:16-132`, host lines `capture.txt:5-10` |
| host capture values used in draft (b) | `.ufo/waves/round-42/frozen/hostcap/capture.txt:6` `var_lib_btrfs absent`, `:7` `scrub_timers_listed 0`, `:8` `btrfs-scrub@.timer disabled disabled`, `:9` `… scrub_speed_max … 1 0`, `:10` `journal_scrub_lines 0` |

## Proposed text (a) — append verbatim after the current tail of `SKILL.md`

```markdown
## Census early readers under pipefail — round 42

Appended 2026-10-26 (round-42 C1; drafted by wave seat ScribeSkill, integrated by the L1). Defect
R41-CENSUS-PIPEFAIL-692; implementation commit `447662088dfd3155e31aed239179a79c1d1046c7`, base
`c8efaa3f120834541f8de1e5e0367e8d1593bae6`; counter `tools/score-size-invariance-r42.py` (sha256
`c511104a8e69fe6a90bb849847fe9c4635642f70ff0cb01fb62c38c098553e03`).

### The rule

`tools/tsukuroi-census.sh` is bash (`#!/usr/bin/env bash`, `:1`) under `set -euo pipefail` (`:423`). A probe
buffer handed down a pipe is read by a reader that exits early — `grep -q` and `grep -m1` at the first match,
`head -n` after n lines. The writer (`printf '%s\n' "$CAP_OUT"`) is then killed by `SIGPIPE`, and `pipefail`
makes that 141 the pipeline's status whatever the reader returned. Two signatures follow from where the pipeline
sits:

- **In a condition** (`if printf … | grep -q …`) the 141 makes the test false: the error branch is skipped and
  the plane reports a clean verdict — a **wrong verdict**, census exit 0 (`HEALTHY`/`DEGRADED` where `BLOCKED`
  is due).
- **In a `$( … )` assignment** the 141 is the assignment's status, so `set -e` kills the census — **exit 141,
  nothing printed after the header line**.

Never pipe a probe buffer into an early-exiting reader in this file. Either read it with a here-string, which no
reader can truncate (`grep -q '^error:' <<<"$s_out"`), or with a reader that consumes the whole input
(`awk 'NR <= 3 {print $1}'` instead of `head -n3 | awk`). The size that decides is the kernel pipe buffer,
64 KiB; the counter's padding is 1 MiB, 16x it (`tools/score-size-invariance-r42.py:61`).

### The sites fixed (base line → tip line)

| Base | Tip | Base (early reader) | Tip (here-string / full-consume) |
|---|---|---|---|
| `:692` | `:695` | `if printf '%s\n' "$s_out" \| grep -q '^error:'; then` | `if grep -q '^error:' <<<"$s_out"; then` |
| `:694` | `:697` | `$(printf '%s\n' "$s_out" \| grep -m1 '^error:')` | `$(grep -m1 '^error:' <<<"$s_out")` |
| `:1621` | `:1624` | `$(printf '%s\n' "$CAP_OUT" \| head -n3 \| awk '{print $1}' \| paste -sd, -)` | `$(printf '%s\n' "$CAP_OUT" \| awk 'NR <= 3 {print $1}' \| paste -sd, -)` |
| `:1635` | `:1639` | `$(printf … \| head -n3 \| awk '{n=$1; sub(/^[^/]+\//, "", n); print n}' …)` | `$(printf … \| awk 'NR <= 3 {n=$1; sub(/^[^/]+\//, "", n); print n}' …)` |
| `:1641` | `:1645` | same as `:1635`, in the `disagree[qu … sup …]` branch | same as `:1639` |
| `:1652` | `:1655` | `$(printf '%s\n' "$CAP_OUT" \| head -n1 \| tr -d '\r')` | `$(printf '%s\n' "$CAP_OUT" \| awk 'NR == 1' \| tr -d '\r')` |

`:692/:694` guard the packages plane's merged `pacman -Qkk` sample (`cap … -Qkk "${names[@]}"` at `:684`, merged
into `s_out` at `:686`): an `error:`
line anywhere in it must make the plane `BLOCKED`. `:1621/:1635/:1641/:1652` extract candidate names and the
`-Suu` trap row in the update-safety plane. The diff of `44766208` is six hunks whose enclosing text is
`probe_packages() {` (`:689`), `probe_update_safety() {` (`:1618`, `:1632`, `:1649`) and `STUB` (`:2344`, `:2540`,
inside `run_selftest`) — the C1 kill rule's scope condition.

### Failure signatures, measured

| Variant | Fixture | Observed |
|---|---|---|
| base `c8efaa3f` | P1, P3, P6 — a `-Qkk` error line before, inside and after 1 MiB of padding | large twin rc **0** where the small twin exits 2; the hybrid run below prints `packages=HEALTHY` on the same shape (`.ufo/waves/round-42/before/c1-before.jsonl` `per_case`; `.ufo/waves/round-42/impl/c1-able-to-fail.txt`) |
| base `c8efaa3f` | U1-U4 — `-Qu`/`-Sup`/`-Suu` lists past the buffer | large twin rc **141** where the small twin exits 1 (U4: 0) — census dead, header line only (same receipt) |
| hybrid: implementation selftest + base plane bodies | the two new selftest cases | `FAIL blocked: … exit 0 wanted 2; output: … TSUKUROI_CENSUS: HEALTHY (packages=HEALTHY …)` and `FAIL degraded: … exit 141 wanted 1` (`impl/c1-able-to-fail.txt`) |

A live census that ends at exit 141 with only its header line should be read as this defect first, not as a probe
failure: the plane whose buffer outgrew 64 KiB is the one that was about to answer.

### Selftest cases added (128 → 130)

| Case (`tools/tsukuroi-census.sh`) | Line | Fixture |
|---|---|---|
| `blocked: a sample error ahead of a large -Qkk output still blocks (R42-C1)` | `:2357` | one error line, then 4000 warning lines (~300 KB) |
| `degraded: 4002 update candidates keep the names and the trap row (R42-C1)` | `:2564` | 4002 candidates on `-Qu`, `-Sup`, `-Suu`; expects `names=[alpha,beta,pad00000]` and `trap=-Suu:4002[fixture/alpha 1.1-1]` |

### Counting

`python3 tools/score-size-invariance-r42.py --revision <REV> --scratch <DIR>` — a metamorphic oracle that holds
no expected verdict: ten fixture twins (P1-P6 `-Qkk`, U1-U4 update lists) differing only by verdict-neutral
padding, signal before, inside and after it, large twin first, a per-run error token, and every compared `PLANE `
line plus the `TSUKUROI_CENSUS:` line and the exit code byte-identical between twins (U pairs with integers
normalised to `N`); three production-path legs N1/N3/N6 inside `unshare -rm` with a stub bind-mounted over
`/usr/bin/pacman` and no `TSUKUROI_*` override; the selftest; default-fixture equality with the base. Fixtures are
built from the base census's own dispatcher and `fx_default`, so a fixture-side change in the tested revision is
not scored. **PASS iff `cases == 10 and invariant == 10 and ns_invariant == 3 and selftest_pass == 1 and
default_equal == 1`**; exit 0 on PASS, 1 on FAIL, 2 on usage or read errors. Frozen sha256
`c511104a8e69fe6a90bb849847fe9c4635642f70ff0cb01fb62c38c098553e03`.

Measured at the base `c8efaa3f`: `cases 10`, `invariant 3` (P2, P4, P5), `ns_invariant 0`, `selftest_pass 1`
(`PASS (128 cases, 128 passed, 0 failed)`), `default_equal 1`, FAIL, exit 1, 39 s (19:29:20Z-19:29:59Z).
Measured at the implementation commit `4476620`: `cases 10`, `invariant 10`, `ns_invariant 3`, `selftest_pass 1`
(`PASS (130 cases, 130 passed, 0 failed)`), `default_equal 1`, PASS, exit 0, 44 s (19:41:06Z-19:41:50Z) — a wave-1
executor receipt, not the round-close receipt.

Receipts:

| Stage | Path |
|---|---|
| before, at the base | `.ufo/waves/round-42/before/c1-before.jsonl` (three lines: header, result, `receipt_end`) |
| pre-data controls | `.ufo/waves/round-42/controls/battery-summary-c1.jsonl` and `C1-K0.jsonl`-`C1-K8.jsonl`; K6 (candidate) PASS, K0-K5/K7/K8 FAIL, `should_fail_accepted 0`, `control_accepted 1` |
| able to fail | `.ufo/waves/round-42/impl/c1-able-to-fail.txt` |
| at the implementation commit (wave 1) | `.ufo/waves/round-42/w1/C1ExecRerun/c1-after-4476620.jsonl` |
| round close | `.ufo/waves/round-42/after/` — the L1 writes the after receipt there (round-41 name form: `.ufo/waves/round-41/after/c1-after-568c397.jsonl`) |

### Limits of this section

- **Six pipelines, not a class sweep.** The same shape survives at `:798`, `:931`, `:969`, `:1051`, `:1426`,
  `:1483`, `:1501` (all `$(printf … | head -n1 …)` or `| head -n6` over a single-value probe such as
  `systemctl show -p … --value`, `is-active`, or a journal grep), at `:2175`, `:2178`, `:2180`, `:2184`, `:2185`, `:2190`, `:2195`, `:2226` (the selftest's own
  `$out`/`$pkgline` readers), inside process substitution whose status the parent never checks at `:676`, `:963`,
  `:1162`, `:1497`, and behind `|| true` at `:1783`. No round-42 fixture drives any of those buffers past the pipe
  buffer — the two new fixtures' census lines stay at three names (`:2565`) — but none of them was
  measured for size here: the fix is scoped to the two declared surfaces, and this list is the exposure it leaves.
- **The `-Suu` fix is safe only because `awk` reads its whole input.** `awk 'NR == 1'` prints one line but does
  not stop reading, so the writer is never killed; a replacement built on `head -n1` or an `awk` with `exit`
  would reproduce the 141. The two `-Qu`/`-Sup` sites are the same trick (`NR <= 3` guards the print, not the
  read).
- **bash only.** Here-strings, `pipefail` and exit 141 are bash semantics (GNU bash `5.3.20` here); a `/bin/sh`
  census would not have this defect, and would not have these fixes either.
- **The 64 KiB threshold is the Linux default pipe buffer.** A host configured otherwise moves the twin sizes;
  the counter's 1 MiB padding is a margin, not a measurement of this host's buffer.
- **Fixture twins, plus three namespaced production legs.** Pairs are built by the base census's dispatcher, and
  only N1/N3/N6 read anything live, inside `unshare -rm` with the real `pacman` copied in and a stub bound over
  it. Nothing here reads or writes `/var/lib/pacman` on the host.
- **The counter scores size invariance, not the verdict's correctness.** A census that answers wrongly and
  identically on both twins passes; P5 (clean) and U4 (rc 0) are the pairs that refuse an always-`BLOCKED`
  answer, and the controls K1-K5/K7/K8 are the refusal evidence, not the predicate.
```

## Proposed text (b) — append after draft (a)

```markdown
## Scrub status record — round 42

Appended 2026-10-26 (round-42 C2; drafted by wave seat ScribeSkill, integrated by the L1). Entry
`corpus/knowledge/btrfs-scrub-record-r42.md` rows SC1-SC5, commit
`f50c28d83e1832ecd7eba765caace531f45d6b27`; sources S237 (btrfs-progs v7.1 `cmds/scrub.c`, tag peeled commit
`4ab0e80be9e3bb1db2e6038e6d4316d35fb7ba8b`), S238 (v7.1 `CHANGES`), S239 (own-work host capture); snapshots
pinned in `.ufo/waves/round-42/frozen/src/` with digests in its `SHA256SUMS`, capture
`.ufo/waves/round-42/frozen/hostcap/capture.txt` sha256
`942edc91a6b8fcda3ef29e88c3d54e7a9a48ec4cce302b8c1edcc89c8710643c` (2026-10-26T19:13:44Z, host btrfs-progs
`7.1-1`, kernel `7.2.11-arch1-1`). `btrfs scrub status` reads a file; this section is what that file can and
cannot say. Nothing here runs a scrub, writes `/var/lib/btrfs` or sets a scrub limit — those are operator actions.

### Observation → reading → action

| Observation | Reading | Action |
|---|---|---|
| `btrfs scrub status` prints `no stats available` | No device line carries a start time, so the summary has none (SC4; `S237` scrub.c:321 `pr_default("\tno stats available\n");`) | Read it as "no record of a run", not "never scrubbed": check for the record file and the recording state (rows below) before concluding anything about the data |
| No `/var/lib/btrfs/scrub.status.<fsid>` on disk (host: `/var/lib/btrfs` absent, capture.txt:6) | The record is that one file, and only the userspace `btrfs scrub start` process writes it (SC1, SC3) | `UNRECORDED`. Not evidence that no scrub ran: a run whose recording was disabled, or one driven through the kernel ioctl, leaves no file (SC3) |
| Opening the record fails with `ENOENT` and the status command still answers | A missing record is "no history", not an error (SC4; scrub.c:1931 `if (fdres < 0 && fdres != -ENOENT) {`) | Treat as the row above: absence is a normal answer, not a failed probe |
| Opening the record fails with any other errno, and a warning appears | The status command warns on a real open failure; the file exists but is unreadable, and a record the CLI creates is mode 0600 (SC1; scrub.c:483 `fd = open(datafile, m, 0600);`) | Unreadable is not "no history": the last run may be recorded. Re-read with the owner's privileges before writing "no record" |
| A `scrub.status.<fsid>_tmp` file sits beside the record | That is the staging file: every update is written to `_tmp` and `rename`d over the record (SC1; scrub.c:467 `datafile[ret] = '_';`, :534 `rename(datafile_old, datafile_new)`) | It is neither a second record nor evidence of damage, and a `_tmp` left by a killed start is not the record |
| The record read fails immediately instead of waiting | Every open, reading or writing, takes a non-blocking exclusive lock (SC1; scrub.c:487 `ret = flock(fd, LOCK_EX\|LOCK_NB);`), so a reader that finds it held fails at once | Do not retry in a loop expecting a wait; come back after the start process exits, or read through `btrfs scrub status` |
| The file's first line is not `scrub status:1` | Not a version-1 record written by this tool, or a format this reader does not know (SC2; scrub.c:69 `#define SCRUB_FILE_VERSION_PREFIX "scrub status"`, :856 writes prefix, `:`, version) | Do not parse by column: per-device fields are `\|key:value` pairs after `<uuid>:<devid>` (scrub.c:840) |
| A `scrub start` warning ends "status recording disabled" | `/var/lib/btrfs` could not be created, or the first record could not be written; the scrub itself still runs (SC3; scrub.c:1336, :1507) | Expect no record for that run: do not wait for a file, and do not read its later absence as "no scrub" |
| Status word `running` | The kernel reports a scrub in progress through `BTRFS_IOC_SCRUB_PROGRESS` per device — not through the file (SC3; scrub.c:1200) | Ask the ioctl/`status`; a fresh mtime or a `_tmp` does not make a run "running" |
| Status word `aborted` | The summary marks canceled if any device's record is canceled (SC4; scrub.c:303 `_SCRUB_FS_STAT_ZMAX(ss, canceled, fs_stat);`) | One canceled device makes the whole run `aborted`: separate the devices before judging the rest |
| Status word `finished`, but a device line reads `finished:0` | The summary's finished flag starts at 1 and takes the minimum across devices (SC4; scrub.c:310 `fs_stat->s.finished = 1;`, :304 `_SCRUB_FS_STAT_MIN(ss, finished, fs_stat);`) | A `finished` filesystem verdict is not a finished scrub of every device; read `btrfs scrub status -d` |
| Status word `interrupted` | The record is unfinished and nothing is running now — e.g. the start process ended before the scrub did (SC4; scrub.c:342 `(ss->canceled ? "aborted" :`) | A process outcome, not a media fault: read the per-device error sums (`-d`, raw `-R`) before calling the device |
| You want "how many errors did the scrub find?" | The record holds per-device sums — `read_errors`, `csum_errors`, `verify_errors`, `uncorrectable_errors`, `corrected_errors`, … — and a per-device finished flag; there is no filesystem verdict in it (SC2; scrub.c:870, :888) | Read the device lines; the status word is a fold of them, never a total to cite alone |
| A scrub looks slow | Each device has a byte-per-second limit in `/sys/fs/btrfs/<fsid>/devinfo/<devid>/scrub_speed_max`, 0 meaning none, read by `status` and `start` and set by `scrub limit`, all since btrfs-progs 6.6.3 (SC5; scrub.c:1215 `snprintf(path, sizeof(path), "devinfo/%llu/scrub_speed_max", devid);`, :1218 `limit = 0;`; `S238` CHANGES:460, :467, :468) | Read the file before the device is blamed; a failed read is reported as 0, so "no limit" and "limit unreadable" print the same 0, and a kernel without the file silently reads as none |
| You want "did a scrub run?" and the record is all you have | The start process writes an all-zero record when the scrub starts and progress records while it runs (SC3; scrub.c:1502 `/* write all-zero progress file for a start */`) | The file answers "what the start process recorded", not "what the kernel did". On this host today: no record, no `btrfs-scrub@*` timer enabled, no `scrub:` line in the journal (capture.txt:6, 7, 8, 10) — `UNRECORDED`, weaker than "no scrub ran" (S239) |

### What this changes in triage

- Read "no scrub record" as `UNRECORDED`, not `NEVER SCRUBBED` (SC3); the lane's SH4 verdict `UNVERIFIED` for
  stored data stands (`corpus/knowledge/storage-health-r26.md:55-61`).
- A record is per device: a filesystem `finished` needs every device finished, and one canceled device makes the
  whole run `aborted` (SC2, SC4).
- `interrupted` is a process outcome — an unfinished record with nothing running — not a media fault. Read the
  error sums in the per-device lines (`btrfs scrub status -d`, raw `-R`) before calling the device (SC4).
- Before reading a slow scrub as a device problem, read `scrub_speed_max` (SC5).

### Counting

`python3 tools/check-scrub-record-r42.py --revision <REV>` — per row a quote that resolves on its named line of a
digest-pinned snapshot and lies inside the row's frozen source window, the row's frozen token (absent at the
base), a host line naming an existing line of the pinned capture, and registry rows new, `mined`, opened
2026-10-26 and used-by the entry; verdicts count only through `w2-dispatch.json` + `w2-results.json` + the
committed report, two seats per row (`C2RevSC<n>` reviewer, `C2CritSC<n>` critic; a `partly` needs a bound residual
`C2RevSC<n>c` reading `holds`). **PASS iff `rows == 5 and quotes_ok == 5 and novelty_ok == 5 and host_ok >= 3 and
sources_ok == 1 and verdicts_ok == 5 and novelty_base_hits == 0`**; exit 0 on PASS, 1 on FAIL, 2 on
usage/read failure. Frozen sha256 `dbe933ec8c2cca491346da76bbc104aba8ff9e5486f4dcaf572e59df3680503f`. Measured at the
base: `rows 0`, `quotes_ok 0`, `verdicts_ok 0`, FAIL, exit 1 (`.ufo/waves/round-42/before/c2-before.jsonl`). The
wave-1 C2 reviews are first falsifiers, not counted verdicts: only the wave-2 seats bound through the two
orchestrator records and their committed reports enter `verdicts_ok`.

### Limits of this section

- **Upstream is pinned, the host build is not compared.** All rows state btrfs-progs v7.1 source lines; the host
  runs the Arch build `7.1-1`, whose packaging patches were not compared with `cmds/scrub.c` (entry, Limits).
- **The host readings show absence, not history.** No record and no timer, and no `scrub:` line in this boot's
  kernel log, cannot show that no scrub ever ran (SC3); the record's directory is reported absent, not read
  (capture.txt:6).
- **No census arm reads the record.** This section stays on Frontier ground; `PROVINCE.md`'s promotion condition
  for the scrub record is unchanged, and a census plane reading `no stats available` would still be reading
  absence.
- **The lexical half of the counter is a shape gate.** Quote, token and host-line checks can be written to the
  windows mechanically; only the two bound verdicts per row read the statements (QUALITY 87, entry).
- **The 6.6.3 boundary is a version fact, not a probe.** On an older btrfs-progs a missing `scrub_speed_max`
  report means the command predates the field, not that the device has no limit (S238 CHANGES:460, :467, :468).
```

## Findings for the L1 (outside the drafts)

1. **The C1 fix is scoped, and the same shape survives elsewhere in the census** — `tools/tsukuroi-census.sh`
   at `:798`, `:931`, `:969`, `:1051`, `:1426`, `:1483`, `:1501`, `:1783`, `:2175`, `:2178`, `:2180`, `:2184`,
   `:2185`, `:2190`, `:2195`, `:2226`, and inside unchecked process substitution at `:676`, `:963`, `:1162`,
   `:1497`. (`:1483` is the one of these whose writer can be large in principle — a `grep … | sort -u | head -n 6`
   over journal output inside `$( … )` — and it is unmeasured here.)
   The item's target was the two declared surfaces and the frozen counter's ten pairs, so this is not a defect
   against the declaration; it is the exposure the declaration's scope leaves, and it belongs in the section's
   Limits (draft (a) says so). No size was measured for those buffers by this seat.
2. **The after receipt does not exist yet** (`.ufo/waves/round-42/after/` empty). Draft (a) therefore cites the
   wave-1 executor rerun receipt at `4476620` for the tip measurement and marks the round-close path as the L1's.
   Do not let the section's `Counting` paragraph stand as a claim about an `after/` file until one exists.
3. **The tip measurement I cite is a peer's, not a frozen receipt** — `.ufo/waves/round-42/w1/C1ExecRerun/` is a
   wave-1 executor's seat receipt; the L1 should re-point or re-measure at the tip if the wave-2 tip moves past
   `4476620`.
4. **The census selftest's own readers use the same shape** (`:2178`, `:2180`, `:2184` `printf … | grep -q` under
   the script's `set -euo pipefail`) and are fed by a census output that the round-42 fixtures keep small. If a
   later round grows a fixture's `PLANE ` line past 64 KiB, those checks can flip from `PASS` to "missing" — the
   same defect, one level up, inside the harness rather than the plane.
5. **Draft (b) deliberately carries no wave-1 verdict line** — `ROW SC<n> VERDICT:` lines are the wave-2 seats'
   format and are bound through `w2-dispatch.json`/`w2-results.json`; a wave-1 scribe emitting one would be a
   planted verdict.
6. **Nothing in either draft asserts a host measurement beyond `capture.txt`** — draft (b)'s only host cells are
   `capture.txt:6,7,8,9,10`, matching the entry's own host readings. No `btrfs` command was run by this seat.

## Files written

- `.ufo/waves/round-42/w1/ScribeSkill.md` (this report)
- `.ufo/waves/round-42/w1/ScribeSkill/` (seat directory, created; no separate receipt — every evidence path is an
  existing lane file, cited above)
- Scratch `/fast/scratch/hyaku/tsukuroi-r42/ScribeSkill` created and removed; no fixture, no clone, no commit.
