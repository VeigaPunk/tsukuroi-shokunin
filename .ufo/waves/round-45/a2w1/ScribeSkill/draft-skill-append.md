## Census first-line readers — round 45

Appended 2026-10-27 (round-45 C1; drafted by wave seat ScribeSkill, integrated by the L1). Base `5bbd5ff5`;
implementation `18389f44` — five site conversions plus six `(R45-C1)` selftest cases (148 → 154), census sha256
`237b21c9d757e339943c29b0f005faf569ff997deca46dd5bce16bc631b5fcdc`. Evidence: `.ufo/waves/round-45/` (`before/`,
`controls/`, `a2w1/`).

Surface: five production readers in `tools/tsukuroi-census.sh` that keep only the first line of a captured output —
`probe_systemd` `state` (`:965`) and the timer `Result` `r` (`:1003`), `probe_drivers` `driver` (`:1085`),
`probe_journal` `t_word` (`:1460`) and the timer `ActiveState` `r` (`:1535`). At the base each read
`X=$(printf '%s\n' "$CAP_OUT" | head -n1 | …)`; each now takes its first line by parameter expansion
(`X=${CAP_OUT%%$'\n'*}`) and does the CR removal and trailing-blank strip in the same expansion — no `head` inside
an assignment.

Why it mattered: the census runs under `set -euo pipefail` (`:451`). `head -n1` exits after its one line, so a
captured output larger than the pipe buffer (65536 bytes on this host) leaves the `printf` producer writing into a
closed pipe; it dies of SIGPIPE, the pipeline reports 141, `pipefail` hands that status to the assignment and
`set -e` ends the census — exit 141, no PLANE line, no verdict (R41-CENSUS-PIPEFAIL-692, routed since round 42).
Measured on a 20000-line variable under `set -euo pipefail`: the base form exits 141 and prints nothing, the
parameter-expansion form prints the first line and exits 0. On this host the readers were latent — real probe
outputs sit far below the buffer — so the conversion changes no PLANE line here; the leg that shows the difference
uses stub commands padded to ~200 KB (`a2w1/C1ExecFullLarge.md`: base exit 141 with 0 PLANE lines, `18389f44` exit
2 with six plane lines matching an unpadded run).

| Observation | Reading | Action |
|---|---|---|
| the census exits 141 and prints no `TSUKUROI_CENSUS:` line | a first-line reader emptied its producer: `head` closed the pipe on a capture past the buffer, `printf` died of SIGPIPE, `pipefail` + `set -e` made 141 the census's own status, which is outside the gate's documented 0/1/2 arms | read the capture's size before trusting the run; the repair is parameter expansion, never `\|\| true` on the pipe — the `\| head -1` evasion (control K1) fails the counter |
| `TSUKUROI_CENSUS_SELFTEST: PASS (154 cases, …)` with six PASS lines ending `(R45-C1)` | each case puts the deciding first line in front of ~150 KB of padding (162000 bytes), so a `\| head` reader would die before the assertion; the sixth drives the foreign-baseline lookup (`probe_packages` `bn`, a full read since round 42) past the buffer with the deciding row last | `bash tools/tsukuroi-census.sh --selftest` in any copy: a FAIL on an `(R45-C1)` label means a reader, or the round-42 full read, regressed |
| `printf '%s\n' "$CAP_OUT" \| head` still present at `:707`, `:832`, `:997`, `:1196`, `:1517`, `:1531`, `:1817` | each sits in a process substitution or behind `\|\| true`, so its status is not the assignment's and cannot kill the census; unclaimed by C1 and recorded as a limit | leave them; claiming one needs its own case and revert mutant, as the five claimed sites have |
| the `PLANE` lines at `18389f44` on a drawn capture | equal to the base's on eight draws per site (at least three with a 70-300 KB tail) | check a rewrite of one of these readers with the counter's equivalence leg, not a hand diff |

Counter: `python3 tools/score-census-readers-r45.py --revision <REV> --scratch <DIR> [--lane <repo>]` (sha256
`fe0e31e25c5b3c92cc5aace48acc56bc6dab39b4b3c09b49708a715a3250bd50`) — PASS iff `lexical_hits == 0 and sites_found ==
5 and equiv_ok == 5 and selftest_pass == 1 and selftest_r45 >= 6 and revert_killed == 6 and adjacency_ok == 1`.
Legs: lexical (no `"$CAP_OUT"` followed by `| head` before `run_selftest() {`); per-site equivalence for S1-S5
against the BASE statement on eight drawn captures each; the census selftest carrying at least six `(R45-C1)`
labels; six revert mutants — S1-S5 back to their base lines and the foreign-baseline `bn` back to the round-41
`| head` form — each killed by a non-zero selftest printing an `(R45-C1)` `FAIL`; and the adjacency kill rule
(`tools/check-adjacency-anchors.py` at REV, run from the lane copy whose bytes equal the base — the round-44 harm,
R44C-ADJ-IN109). Base FAIL (control K0: `lexical_hits` 5, `equiv_ok` 0, `selftest_r45` 0, `revert_killed` 0,
`adjacency_ok` 0); pre-data controls K0-K7 and K10 FAIL, K8 (candidate) and K9 (`sed -n 1p` full read) PASS,
`control_accepted` 1 (`.ufo/waves/round-45/controls/battery-summary-c1.jsonl`). Kill rule for the round: any
PLANE/HANDOFF/DRIFT/STORAGE/SCRUB/`TSUKUROI_CENSUS` line shape or live exit code that differs from the base (other
than live drift recurring between two runs of one revision), a predecessor census counter going PASS → FAIL, or a
live run that writes a file, fails C1.

Recorded limits (wave `a2w1`): the equivalence leg scores each site's first physical line only, so a conversion
split over two lines is scored on its first line; the seven masked or process-substitution `| head` readers listed
above are not claimed; the six cases and the draws are fixture captures, not this host's own
`systemctl`/`nvidia-smi` output, and the readers were latent here; `driver` still passes its single-line value
through `printf '%s\n' "$driver" | awk …`, which the lexical leg allows because it is not `"$CAP_OUT" | head`; the
live-mode no-write kill rule was checked by strace in `a2w1/C1ExecLiveRead.md`; the scored outcome of the counter
at `18389f44` is the receipt line under `.ufo/waves/round-45/`, not this section.

## Scrub grounding — round 45 rows

Appended 2026-10-27 (round-45 C2; drafted by wave seat ScribeSkill, integrated by the L1). Entry
`corpus/knowledge/btrfs-scrub-grounding-r45.md` rows GR1, GR2, GR3 on S246 (Linux v7.2.11 `lib/cmdline.c`,
`lib/vsprintf.c`, `lib/kstrtox.c`), S247 (`fs/btrfs/dev-replace.c`) and S248 (systemd v262 `man/systemd.kill.xml`),
with S242 and S243 (round-44 `fs/btrfs/scrub.c`, `sysfs.c`), S237 (round-42 btrfs-progs `scrub.c`) and the own-work
host capture S249 (`.ufo/waves/round-45/frozen/hostcap/capture.txt`). The three rows ground the three `[inference]`
marks the round-44 entry carried: SR8's `memparse` suffixes, SR7's replace caller of `btrfs_scrub_dev`, and SR9's
`KillSignal=` as the stop signal. Nothing here writes sysfs, starts, stops or enables a unit, runs a scrub or a
replace, or calls a privileged ioctl.

| Observation | Reading | Action |
|---|---|---|
| `devinfo/<devid>/scrub_speed_max` reads a value the operator did not type — `010` reads 8, `100m` reads 104857600 — or a write is refused with `EINVAL` | the write is parsed by `memparse` (S243 sysfs.c:2040) over `simple_strtoull` with base 0 (S246 cmdline.c:156), so a leading `0x` plus a hex digit is hexadecimal and any other leading `0` octal (S246 kstrtox.c:29-33, vsprintf.c:86); at most one suffix `K`/`M`/`G`/`T`/`P`/`E`, either case, each a factor of 1024, counted only when a digit precedes it (cmdline.c:189), overflow to `ULLONG_MAX` (:191-192); trailing whitespace is skipped (S243 sysfs.c:2042) and any text after that is `EINVAL` (:2043-2044); 0 = no limit, in-memory only, and a bare newline parses 0 and clears the limit | any user reads it, only root writes it; recompute 1024^n and the radix before calling the value wrong; the census reports `limited=` and never writes (SR8) |
| `btrfs scrub start` answers `EINPROGRESS` on a filesystem where no scrub was started, or a privileged `scrub status` shows the source device of a replace as running | a device replace copies through the scrub code: `btrfs_scrub_dev(fs_info, src_device->devid, …, false, true)` at start (S247 dev-replace.c:701-703) and on continuation (:1265-1268); inside `btrfs_scrub_dev` a call with `is_dev_replace` false is refused `-EINPROGRESS` while `btrfs_dev_replace_is_ongoing` (S242 scrub.c:3148-3153), and any call is refused while the device carries a scrub context (SR7) — so a progress query for the source devid answers 0 during the copy | check the replace first (`btrfs replace status`, read-only): `EINPROGRESS` says the replace holds the scrub machinery, not that a scrub runs; how btrfs-progs prints these two answers is `[inference]` |
| `systemctl stop btrfs-scrub@<instance>.service` returns but the record shows no `canceled` mark, or counters that look frozen | the unit sets `KillSignal=SIGINT` (S244 btrfs-scrub@.service:9) and no `KillMode=`, so the default `control-group` applies (S248 systemd.kill.xml:68,101) — every remaining process, not only the main one; SIGCONT follows the signal (:114), and after `TimeoutStopSec=` the request repeats with SIGKILL unless `SendSIGKILL=no` (:91,96); on this host the effective timeout is 5 s from `/etc/systemd/system.conf.d/10-faster-shutdown.conf` (capture.txt:4), a drop-in no installed package owns (:5), with `systemctl show` reporting `KillSignal=2 KillMode=control-group TimeoutStopUSec=5s FinalKillSignal=9 SendSIGKILL=yes` (:3) under systemd 262-1-arch (:2); SIGINT reaches the foreground start's handler, which issues `BTRFS_IOC_SCRUB_CANCEL` (S237 scrub.c:421) | read the record's timestamps before treating the run as finished: a start killed inside the 5 s may leave the record as last written, without `canceled` (`[inference]`); stop, start and enable stay operator-owned |

Counter: `python3 tools/check-scrub-grounding-r45.py --revision <REV> [--lane <repo>]` (sha256
`a1eb402dffae97fcefd9bd539529f1cacc5034419b6de06e1f8ac1c08d011331`; the attempt-2 rebinding `057c1804` changed only
the two wave-name literals `w1`/`r1` → `a2w1`/`a2r1`) — PASS iff `rows == 3 and quotes_ok == 3 and props_ok == 3 and
host_ok == 3 and sources_ok == 1 and verdicts_ok == 3 and novelty_base_hits == 0 and pointer_ok == 1`. A quote
counts only when its (id, file) is a digest-checked snapshot, its text occurs on the named line and is substantial
(at least half of the stripped line, and at least 10 characters), and one quote lies in the row's frozen window;
`props_ok` is the frozen proposition tokens, `host_ok` names existing non-empty `capture.txt` lines, and
`verdicts_ok` binds the counted seats `C2RevGR<n>` (reviewer) and `C2CritGR<n>` (critic) of wave `a2w1` through
`a2w1-dispatch.json`/`a2w1-results.json` and the report's first line `ROW GR<n> VERDICT: <holds|partly|fails>`; a
`partly` is answered by a residual `C2ResGR<n>` reading `holds` in wave `a2r1`, and an unbound counted seat makes
its row not ok. Controls `.ufo/waves/round-45/controls-a2/`: 30 controls, `should_fail_accepted` 0, K3 (forged
records), K19 (`partly` plus a bound residual) and K26 (JSON-string output) PASS (`battery-summary-c2.jsonl`).

Limits (entry Limits): kernel behaviour is pinned at Linux v7.2.11 lines (the Arch kernel 7.2.11-arch1-1 patch
touches no `fs/` file, carried from round 43 and not re-checked for `lib/` this round); GR1's examples follow from
the quoted code, not from a write — the capture's caller is uid 1000 with `CapEff` 0 (capture.txt:1) and this host's
devid 1 reads 0 (capture.txt:8); GR3 pins systemd's documented order and the host's effective values, not a trace of
a stop and nothing was started or stopped; GR2's btrfs-progs printing and GR3's record after SIGKILL stay
`[inference]`; the verdicts are seat verdicts of this lane, not outside review; committed bytes cannot tell forged
orchestrator records from real ones (control K3 is the standing limit).

### Correction — the round-44 SR8 `memparse` parenthetical (routed defect D2; append-only)

The `scrub_speed_max` row of "Scrub record — round 44 rows" (`SKILL.md:4225` at this append) states "writes parse
with `memparse` (K/M/G suffixes, trailing whitespace skipped, else `-EINVAL`)" as fact on S243 alone. That was
ahead of its source: the entry the row summarizes carried the suffix claim as `[inference]` —
`corpus/knowledge/btrfs-scrub-record-r44.md:63`, "is [inference: its definition in `lib/cmdline.c` is not pinned]".
GR1 now grounds it on S246 (`cmdline.c:147,156,189-192`, `vsprintf.c:86`, `kstrtox.c:29-33`) and S243
(`sysfs.c:2040,2043`). Read the row as grounded, and as understated: the radix is base 0, so a leading `0` is octal
and `0x10` is hexadecimal; each suffix is a power of 1024, not 1000; the suffix letter may be lower case; overflow
becomes `ULLONG_MAX`; and a bare newline parses 0 and clears the limit. The row's other statements (mode 0644,
`0` = no limit, in-memory only) are unchanged; this note corrects the source standing, not the row's text.
