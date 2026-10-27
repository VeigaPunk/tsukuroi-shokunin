VERDICT: draft

Item F-5 (seat `ScribeReadme`, wave `tsukuroi-r45-a2w1`). Drafted, not landed: no lane file was written. The D3
omission it marks is real in committed bytes at `18389f44cf6ce414d7be205998b29c79fb0b490c` (evidence below). The
`corpus/README.md` draft appends after the file's last line, so no existing line, including every Frontier/Core
line, moves.

## 1. Where the text goes (line numbers at `18389f44`)

`corpus/README.md` at `18389f44cf6ce414d7be205998b29c79fb0b490c` is 452 lines and ends with a single newline
(`git show 18389f44:corpus/README.md | wc -l` → 452; `corpus/README.md` and `SKILL.md` are byte-identical at
`18389f44` and at the lane tip `3c42f556`, `git diff --stat 18389f44 HEAD -- corpus/ SKILL.md` → empty, so these
numbers also hold at the tip). The draft is appended at end of file; with the file's trailing newline preserved the
block lands as:

| Line | Content |
|---|---|
| 452 (unchanged) | `NONE dir=absent records=0 … timers=0`, consistent with S245.` — the last line of the round-44 Frontier notice |
| 453 | blank |
| 454 | `## Round-45 coverage note (appended 2026-10-27)` |
| 456 | append-only sentence |
| 458-459 | table header `\| Note \| Holds \| Sources \|` |
| 460 | C1 census row (additive; see §4) |
| 461 | `knowledge/btrfs-scrub-grounding-r45.md` row (the named deliverable) |
| 463 | `### Correction to the round-44 entry's index row — SR7-SR9 are pending, not admitted (routed defect D3)` |
| 465-475 | D3 body |
| 477 | `### Frontier notice — round 45` |
| 479-490 | Frontier notice body (promotes nothing) |

Verified mechanically: `(base + block).split('\n')[:453] == base.split('\n')` → PASS, i.e. all 452 base lines keep
their number and bytes; new content lines 490. A patch with the exact hunk is in the seat dir (`apply.diff`);
`git apply --check -p1` reads OK in a scratch clone at the tip, the applied file is byte-identical to the simulated
file (`cmp`), and `git apply -R --check` reads OK.

## 2. D3 is real in committed bytes (so the mark is warranted)

| Claim | Evidence at `18389f44` |
|---|---|
| The round-44 README row lists SR7-SR9 | `corpus/README.md:434` — "SR7 the scrub-progress success direction … SR8 `scrub_speed_max` … SR9 the Arch-packaged `btrfs-scrub@.timer`/`.service` …" |
| It does not say the depth gate failed | The round-44 notice (`:436-452`) names the predicate at `:447-448` ("… `verdicts_ok == 3` …") but nowhere states the result |
| The gate receipt returns `verdicts_ok 0` | `.ufo/waves/round-44/after/c2-final-fbfef071.jsonl` line 2: `rows 3, quotes_ok 3, props_ok 3, host_ok 3, sources_ok 1, novelty_base_hits 0, pointer_ok 1, verdicts_ok 0, verdict FAIL`; line 3 `exit_code 1` |
| The predicate requires 3 | `tools/check-scrub-record-r44.py:50-51` — "PASS iff rows == 3 … and verdicts_ok == 3 and novelty_base_hits == 0 and pointer_ok == 1." |
| The SR8/SR9 narrowings are unjudged | `corpus/lessons/round-44-verifier-spotcheck.md:81-99` (§2 C2; `:99` routes D2/D3) |
| The SKILL section carries the same omission | `SKILL.md:4214-4230`, "Scrub record — round 44 rows"; the SR8 row at `:4225` still states "`memparse` (K/M/G suffixes …)" as fact (D2) and no row records the gate result (D3) |
| The entry itself now records the status | `corpus/knowledge/btrfs-scrub-record-r44.md:153-161`, "## Round-45 grounding and gate status" — gate FAILED, `verdicts_ok 0`, narrowings unjudged, SR7-SR9 pending, grounding pointed at the r45 rows GR2/GR1/GR3 |
| The routed wording | `corpus/lessons/round-44-verifier-spotcheck.md:184-186` (D3 `R44C-C2-UNADMITTED-MARK`) |

The draft therefore says the gate FAILED (`verdicts_ok 0`), says the narrowings were judged by no counted seat, and
points at the entry's new `## Round-45 grounding and gate status` section (`btrfs-scrub-record-r44.md:153-161`).
It does not edit the round-44 row, the round-44 notice or the SKILL section, and it moves no Frontier/Core line.

## 3. Exact proposed Markdown

Append these bytes to `corpus/README.md` (the block starts with one blank line; receipt
`.ufo/waves/round-45/a2w1/ScribeReadme/readme-append.md` holds it byte-for-byte):

```markdown

## Round-45 coverage note (appended 2026-10-27)

Append-only; the coverage map, the Frontier bullets and the round-38 to round-44 notes above stay as written.

| Note | Holds | Sources |
|---|---|---|
| `../tools/tsukuroi-census.sh` (five first-line readers, round-45 C1) | The operability repair: the five production readers that keep the first line of a captured output (`probe_systemd` `state` and the timer `Result` `r`, `probe_drivers` `driver`, `probe_journal` `t_word` and the timer `ActiveState` `r`) take it by parameter expansion — `${CAP_OUT%%$'\n'*}` at all five, with a CR strip at four and a trailing-blank strip at three, and the driver reader keeping its last comma field — instead of `printf '%s\n' "$CAP_OUT" \| head -n1` inside an assignment, which under `set -euo pipefail` exits 141 once an output passes the pipe buffer; six `(R45-C1)` selftest cases put the deciding first line before ~150 KB of padding (2,000 generator lines, `tools/tsukuroi-census.sh:3338`), the sixth driving the foreign-baseline lookup past the pipe buffer | contract `tools/tsukuroi-census.sh:965,1003,1085,1460,1535` and cases `:3342-3374`; counter `tools/score-census-readers-r45.py` |
| `knowledge/btrfs-scrub-grounding-r45.md` | GR1 `memparse` is the `scrub_speed_max` write parser: `simple_strtoull` with base 0 (hex for `0x` and a hex digit, octal for any other leading `0`), at most one `K`/`M`/`G`/`T`/`P`/`E` suffix in either case with each step multiplying by 1024, the suffix counted only after at least one digit, overflow to `ULLONG_MAX`, trailing text `-EINVAL`, and a bare newline parses 0 and clears the limit; GR2 a device replace copies the source device through `btrfs_scrub_dev` (`readonly` false, `is_dev_replace` true) at start and on resume, so a non-replace scrub of that filesystem is refused `-EINPROGRESS` while `btrfs_dev_replace_is_ongoing`, and any call is refused while the device already carries a scrub context; GR3 `systemctl stop` of the Arch-packaged `btrfs-scrub@.service` under systemd v262 sends the unit's `KillSignal=SIGINT` to the whole control group (`KillMode=control-group` default), then SIGCONT, then SIGKILL at `TimeoutStopSec=` — 5 s on this host from an unowned drop-in — and the foreground start's handler issues `BTRFS_IOC_SCRUB_CANCEL` | S246 (Linux v7.2.11 `lib/cmdline.c`, `lib/vsprintf.c`, `lib/kstrtox.c`), S247 (`fs/btrfs/dev-replace.c`), S248 (systemd v262 `man/systemd.kill.xml`), S249 (own-work capture); S242/S243/S244 and S237 (round-44 and round-42 snapshots); counter `tools/check-scrub-grounding-r45.py` |

### Correction to the round-44 entry's index row — SR7-SR9 are pending, not admitted (routed defect D3)

The round-44 row above (`corpus/README.md:434`) and the `SKILL.md` section "Scrub record — round 44 rows"
(`SKILL.md:4214-4230`) present SR7-SR9 as that entry's holdings without recording that the round-44 depth gate
FAILED: `tools/check-scrub-record-r44.py` at `fbfef071` reports `verdicts_ok 0` with `rows 3, quotes_ok 3, props_ok
3, host_ok 3, sources_ok 1, novelty_base_hits 0, pointer_ok 1`, verdict `FAIL`, exit 1
(`.ufo/waves/round-44/after/c2-final-fbfef071.jsonl`), against a predicate that requires `verdicts_ok == 3`
(`tools/check-scrub-record-r44.py:50-51`). The SR8/SR9 narrowings made after the counted reads (`8eee79db` →
`fbfef071`) were judged by no counted seat (`corpus/lessons/round-44-verifier-spotcheck.md:81-99`, its §2 C2). Read
SR7-SR9 as pending, not admitted: the entry now records the gate status and the round-45 grounding at its
`## Round-45 grounding and gate status` section (`corpus/knowledge/btrfs-scrub-record-r44.md:153-161`), and the
`SKILL.md` section carries the same omission until the round-45 SKILL append sweeps it (routed defects D2 and D3,
`corpus/lessons/round-44-verifier-spotcheck.md:181-186`).

### Frontier notice — round 45

Nothing moves. C1 is an operability repair inside `tools/tsukuroi-census.sh` (five first-line readers and six
`(R45-C1)` selftest cases), not a new coverage surface, and C2 deepens the held scrub-record surface from source: it
adds no census arm, so the round-26 condition at `corpus/README.md:243` is untouched and the storage-integrity split
stays as round 44 left it — the unprivileged scrub-record view Core (`../PROVINCE.md` "Round-44 promotion —
R44-SCRUB-VIEW"), the record's content, the running state and NVMe SMART/Health Frontier, and running, canceling,
resuming or limiting a scrub, enabling its timer, resetting the error counters, profile changes, firmware, LUKS and
any repair operator-owned. Recorded limits: the five readers are latent here (host outputs stay far below the pipe
buffer), the C1 equivalence leg scores each site's first physical line only, and the seven masked or
process-substitution `| head` readers in the same file are not claimed; the C2 row makes no claim beyond its quoted
source lines. The GR1-GR3 row verdicts bind only from this wave's counted seats, reviewers `C2RevGR1`-`3` and critics
`C2CritGR1`-`3` in wave `a2w1`, with a residual `C2ResGR<n>` seat in `a2r1` for any row a counted seat reads
`partly`; until a gate receipt shows `verdicts_ok 3`, no read of the entry is a pass.
```

## 4. Judgement calls the L1 should know

1. **The C1 census row (line 460) is additive.** F-5 names only the `btrfs-scrub-grounding-r45.md` row, but every
   census-touching round since 36 indexed the census change (round-44's own table opens with the
   `probe_scrub_record` row). Its facts are checked against committed bytes (`tools/tsukuroi-census.sh:965,1003,
   1085,1460,1535` at `18389f44`: prefix removal at all five, CR strip at `:965,:1003,:1460,:1535`, trailing-blank
   strip at `:965,:1460,:1535`, `:1085` keeping its last comma field via `awk -F', *' '{print $NF}'`; the six case
   labels at `:3342,:3347,:3355,:3360,:3365,:3374`; `r45pad` at `:3338` writes 2,000 padding lines). It is one line
   and can be dropped without touching the entry row or the D3 note; dropping it leaves the round's C1 change
   unindexed in `corpus/README.md`.
2. **Sources cell shape.** The round-44 row's Sources cell reads "entry header and rows at the measured revision",
   which names no fetched source and no counter. The draft cites the source ids and the counter — the shape of the
   round-42 and round-43 rows in the same file. If the L1 wants the literal round-44 phrasing, replace that cell with
   `entry header and rows at the measured revision` (no other text changes).
3. **Nothing is claimed about the round-45 gate.** The wave's counted seats (`C2RevGR1-3`, `C2CritGR1-3`, wave
   `a2w1`; residuals `C2ResGR<n>`, wave `a2r1`) have not all reported, so the notice says only how the verdicts
   bind, and that no read is a pass until a receipt shows `verdicts_ok 3` (predicate at
   `tools/check-scrub-grounding-r45.py:65-66`; wave literals `:84-85` at the tip).
4. **The SKILL half of D3 cannot be closed by a README note.** The note says so and names the round-45 SKILL append
   (D2 + D3) as the place it is swept, without asserting that it has been.
5. **No Frontier/Core line is moved or re-worded**, including the round-44 promotion sentence inside the old notice;
   the new notice restates the split as unchanged and cites `PROVINCE.md:256` ("Round-44 promotion —
   R44-SCRUB-VIEW") rather than creating a round-45 promotion token.

## 5. Findings (even where they do not favour the lane)

- The D3 defect reproduces exactly as routed: the index row `corpus/README.md:434` presents SR7-SR9 with no gate
  result, while the committed receipt for `fbfef071` reads `verdicts_ok 0` / `FAIL` / exit 1 against a predicate
  requiring 3 (`tools/check-scrub-record-r44.py:50-51`). The round-44 notice's phrase "binding only from the
  round-44 wave-2 reviewer and critic seats" does not say the gate failed; a reader who does not run the counter
  cannot tell admitted from pending.
- The round-44 row's Sources cell (`:434`) is not a source citation; the same file's r42/r43 rows cite ids. Left as
  written (append-only), flagged for the next index row.
- `SKILL.md:4225` still states the `memparse` suffix behaviour as fact (D2) — after this round it is grounded by GR1,
  but the SKILL sweep is F-4's item, not this one; the draft only names the omission so the index is not read as an
  admission.
- The r45 entry has no gate-status mark of its own; the draft's notice deliberately makes no admission claim.

## 6. Not done

- No counter, census selftest or host probe was run (evidence here is committed bytes, `git show`/`grep` reads, and
  one python read of the committed receipt JSONL). Reading the r44 receipt is not a re-run and is not treated as one.
- No lane file was created, edited or deleted; no `git add/commit/stash/checkout/reset/push` and no jj command ran in
  the lane. The only git writes were in throwaway scratch clones under
  `/fast/scratch/hyaku/tsukuroi-r45/ScribeReadme/` (each `git -C "$D" rev-parse --show-toplevel` printed the clone
  path before any use), and those were removed with the scratch dir.
- No host query beyond read-only file/git reads; no package, service, unit, sysfs, mount or namespace action; no tool
  installed or upgraded, so there is no install line to report.

Receipts (seat dir `.ufo/waves/round-45/a2w1/ScribeReadme/`): `readme-append.md` (exact appended bytes),
`line-map.txt` (line numbers), `apply.diff` (the hunk, applies `-p1` at the tip and reverses), `evidence.txt`
(commands and observed outputs).
