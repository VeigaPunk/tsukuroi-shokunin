VERDICT: draft

# ScribeSkill — F-4: SKILL.md round-45 append draft, and the D2 correction line

Seat `ScribeSkill`, wave `a2w1` (round 45, hyaku run 9). Item F-4: draft the two appended `SKILL.md` sections in the
register of `SKILL.md` "Scrub-record census arm — round 44" (`SKILL.md:4184-4212`), and the appended correction line
for routed defect D2. I wrote no tracked file: `SKILL.md` is untouched, the lane has no edit from this seat, no
counter was modified, and nothing was installed. The exact append-ready text is in
`.ufo/waves/round-45/a2w1/ScribeSkill/draft-skill-append.md` and repeated verbatim below.

## What I did

Read-only reads of the lane at `HEAD` `3c42f556` (whose `tools/tsukuroi-census.sh` is byte-identical to the
implementation revision `18389f44`, sha256 `237b21c9…fcdc`), the two frozen counters, the round-44 and round-45
knowledge entries, the before/controls receipts, and this wave's C1 receipts; plus two cheap measurements of my own
in scratch: the census selftest at `18389f44` (~50 s) and a two-line reproduction of the exit-141 mechanism. I did
**not** run the full C1 counter (7 min, 6 CPUs — the declared cost, and other seats hold that leg) and did **not**
run any host-mutating command.

## Evidence for the draft's load-bearing statements

| Statement in the draft | Evidence (observed) |
|---|---|
| five base sites at `:965`, `:1003`, `:1085`, `:1460`, `:1535` read `X=$(printf '%s\n' "$CAP_OUT" \| head -n1 …)` | `git show 5bbd5ff…:tools/tsukuroi-census.sh \| grep -n 'printf …\| head -n1'` → exactly those five lines (`ScribeSkill/census-sites-and-masked.txt`) |
| the five now use parameter expansion at the same five line numbers | `git show 18389f44…:tools/tsukuroi-census.sh \| grep -n R45-C1` → `:965,:1003,:1085,:1460,:1535`, each `X=${CAP_OUT%%$'\n'*}` (`ScribeSkill/census-sites-and-masked.txt`) |
| census runs under `set -euo pipefail` | `tools/tsukuroi-census.sh:451` |
| the old form dies with 141 and prints nothing; the new form prints the first line and exits 0 | scratch scripts `r141.sh` / `r141b.sh` on a 20000-line variable: rc=141 with 0 bytes of stdout / rc=0 with the first line (`ScribeSkill/r141-observed.txt`, `o1.txt`, `o2.txt`) |
| the pipe buffer is 65536 bytes on this host | `fcntl` `F_GETPIPE_SZ` on a fresh pipe → 65536 (`ScribeSkill/r141-observed.txt`) |
| the selftest is `PASS (154 cases, 154 passed, 0 failed)` with six PASS lines ending `(R45-C1)`; base was 148 | my run at `18389f44` in a `--shared` clone: `TSUKUROI_CENSUS_SELFTEST: PASS (154 cases, 154 passed, 0 failed)`, `grep -c '^PASS .*(R45-C1)'` → 6 (`ScribeSkill/selftest-impl.txt`); base 148 in `.ufo/waves/round-45/before/census-selftest-base.txt` |
| six `(R45-C1)` case labels, one per reader plus the foreign baseline | `tools/tsukuroi-census.sh:3342,3347,3355,3360,3365,3374` |
| padding is ~150 KB | `r45pad` output measured at 162000 bytes for the first case's pad text |
| the seven unclaimed masked readers are at `:707`, `:832`, `:997`, `:1196`, `:1517`, `:1531`, `:1817` | `git show 18389f44…:tools/tsukuroi-census.sh \| grep -n '\| head'` → those seven plus the selftest's own `\| head` lines at `:2292,:2302`; contexts read at `:704-710` (mapfile process substitution), `:829-834` (`\|\| true`), `:1190-1200` (`done < <(find … \| head -n 4000)`), `:1513-1520` and `:1814-1820` (`\|\| true`); identical list to `SCORECARD.md` "Recorded limits" |
| the whole-census leg: base exit 141 and no PLANE line, implementation exit 2 with six plane lines | `.ufo/waves/round-45/a2w1/C1ExecFullLarge/{base-large.rc,impl-large.out,base-large.out}` → `141`, 6 `PLANE` lines, 0 `PLANE` lines; the "equal to an unpadded run" comparison is that seat's, cited to `a2w1/C1ExecFullLarge.md` (first line `VERDICT: supports`) |
| base FAIL and the pre-data controls | `.ufo/waves/round-45/controls/battery-summary-c1.jsonl`: K0 `lexical_hits` 5, `equiv_ok` 0, `selftest_r45` 0, `revert_killed` 0, `adjacency_ok` 0, FAIL; K0-K7, K10 FAIL; K8, K9 PASS; `control_accepted` 1 |
| C2 counter predicate, seats and rebinding | `tools/check-scrub-grounding-r45.py:84-85` (`VERDICT_WAVE = 'a2w1'`, `RESIDUAL_WAVE = 'a2r1'`), `:130` (predicate), `:29-47` (binding); sha256 `a1eb402d…1331` (my `sha256sum`) |
| C2 controls | `.ufo/waves/round-45/controls-a2/battery-summary-c2.jsonl`: 30 results, K3/K19/K26 PASS, K0/K1 FAIL, `should_fail_accepted` 0, `control_accepted` 1 |
| the GR citations I added beyond the entry (sysfs.c:2042 `skip_spaces`, :2044 `return -EINVAL`; dev-replace.c:701-703, :1265-1268; kstrtox.c radix) | read in `.ufo/waves/round-45/frozen/src/{cmdline.c,kstrtox.c,vsprintf.c,dev-replace.c}` and `.ufo/waves/round-44/frozen/src/{sysfs.c,scrub.c}` at the named lines; all match the entry's quotes |

## Findings (reported, including what falsifies nothing and what constrains the draft)

1. **The D2 defect is real and is a SKILL-only overreach, not an entry error.** `SKILL.md:4225` states the
   `memparse` suffix semantics as fact and cites S243 only; the entry it summarizes carried them as `[inference]` at
   `corpus/knowledge/btrfs-scrub-record-r44.md:63` ("is [inference: its definition in `lib/cmdline.c` is not
   pinned]"). GR1 grounds the claim on S246, and the round-44 entry already carries the append-only grounding pointer
   at `corpus/knowledge/btrfs-scrub-record-r44.md:157-161`. The correction is drafted as an appended note; the row
   text is not edited.
2. **The round-44 SR8 row is not merely ungrounded at its old round, it is understated.** It omits the base-0 radix
   (leading `0` octal, `0x` hex — `S246 kstrtox.c:29-33`), the lower-case suffix and the 1024 factor
   (`S246 cmdline.c:189-192`), the `ULLONG_MAX` overflow, and the bare newline that clears the limit. The draft's D2
   note says so, so a reader is not left with the impression that the old parenthetical is complete.
3. **The C2 counter at `18389f44` has every entry leg true and `verdicts_ok` 0** — my run: `rows` 3, `quotes_ok` 3,
   `props_ok` 3, `host_ok` 3, `sources_ok` 1, `novelty_base_hits` 0, `pointer_ok` 1, `verdict_ok` false per row,
   overall `FAIL` (`ScribeSkill/c2legs.json`). That is the expected state while the six counted seats run; my draft
   therefore makes no gate-outcome claim for C2, and none for C1 either (the C1 rerun receipts under
   `a2w1/C1ExecRerun/` are provenance envelopes only — `argv`, `tool_sha256`, branch list — with no predicate fields
   in them).
4. **No round-45 registry row exists in `SKILL.md` at `HEAD`** (`grep -n 'census-readers-r45\|scrub-grounding-r45'
   SKILL.md` → no hit). The registry table is another seat's item (peer `RegistryDraft` produced
   `a2w1/RegistryDraft/round45-table.md`); my two sections cite the counters by path and sha256 and do not depend on
   their registry rows, but the L1 must not append these sections without that table's row pair.
5. **The archived `SKILL.md` line numbers the draft cites are stable under appending**: `:4225` (SR8 row) and
   `:4184-4212` (round-44 section) are above the append point, so an append at the file end does not shift them.

## Exact proposed text

The block below is the exact Markdown to append to `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SKILL.md` (also at
`.ufo/waves/round-45/a2w1/ScribeSkill/draft-skill-append.md`). The L1 owns the "drafted by … integrated by the L1"
sentence and any outcome line it adds from the wave receipts; every clause here is a statement I either read in the
lane's own files or measured, with the row's source named.

---

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

---

## Out of scope / deliberately not done

- No edit to `SKILL.md`, the entries, the counters, `corpus/SOURCES.md`, `SCORECARD.md` or any tracked lane file; no
  git or jj command that mutates the lane (I used `git show`, `git log`, `git merge-base`, `git status`, and one
  `git clone --shared` into scratch).
- No gate outcome claimed: the C1 counter was not run by me (declared 6-7 min / 6 CPU), and the C1 wave receipts at
  `a2w1/C1ExecRerun/` carry provenance only. The L1 should add the outcome sentence after `after/` or the rerun
  receipt exists; my draft's "the scored outcome … is the receipt line under `.ufo/waves/round-45/`" is the
  placeholder-free form that stays true either way.
- The round-45 registry table is not mine (peer `RegistryDraft`); my sections cite both counters by path and sha256
  so the L1 can append the table and the sections in either order, but a section without its registry row would
  leave the gate undiscoverable.
- No host query beyond `git`/file reads (`systemctl show` was already frozen in the capture at
  `.ufo/waves/round-45/frozen/hostcap/capture.txt`); no tool installed, no package transaction, no unit touched.

## Artifact paths

- Report: `.ufo/waves/round-45/a2w1/ScribeSkill.md`
- Append-ready draft: `.ufo/waves/round-45/a2w1/ScribeSkill/draft-skill-append.md`
- Receipts: `.ufo/waves/round-45/a2w1/ScribeSkill/{selftest-impl.txt, r141-observed.txt, r141.sh, r141b.sh, o1.txt, o2.txt, c2legs.json, census-sites-and-masked.txt}`
- Scratch `/fast/scratch/hyaku/tsukuroi-r45/ScribeSkill` removed before this report was written.
