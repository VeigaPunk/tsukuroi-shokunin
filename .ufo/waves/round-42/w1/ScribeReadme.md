VERDICT: draft

# D-2 — append-only coverage notes for the round-42 scrub-record entry

Seat `ScribeReadme`, scribe, axis `coverage`, item D-2, lane `tsukuroi-shokunin`, round 42 wave `w1`, 2026-10-26.
Draft only: I wrote no `corpus/README.md`, `PROVINCE.md` or other lane file. The two blocks below are the exact
Markdown to append; the L1 places them.

## What was read (evidence)

| Claim | Evidence (command → observed) |
|---|---|
| The C2 entry exists at the tip with five rows SC1–SC5 | `grep -c '^## SC[1-5]$' corpus/knowledge/btrfs-scrub-record-r42.md` → `5`; entry commit `f50c28d8`, `git show --stat` → `corpus/knowledge/btrfs-scrub-record-r42.md \| 159 +` |
| Registry rows S237–S239 exist, `mined`, used-by this entry | `grep -n '^\| S23[789] ' corpus/SOURCES.md` → `246`, `247`, `248` (`corpus/SOURCES.md:246-248`) |
| The counter named in the draft is byte-identical to the freeze commit | `git diff --stat a84fc9de -- tools/check-scrub-record-r42.py` → empty; `sha256sum` → `dbe933ec8c2cca491346da76bbc104aba8ff9e5486f4dcaf572e59df3680503f` (matches the declared digest) |
| Snapshot digests cited in the row | `sha256sum` in `.ufo/waves/round-42/frozen/src/` → `scrub.c 48df2e2f…f0801`, `CHANGES bd881ab8…aaff2a0d22`, equal to `SHA256SUMS` |
| Host capture cited in the row and in the PROVINCE note | `sha256sum .ufo/waves/round-42/frozen/hostcap/capture.txt` → `942edc91…0643c`; file lines 1–10 read (fsid `:5`, `var_lib_btrfs absent` `:6`, 0 timers `:7`, unit `disabled` `:8`, limit 0 `:9`, 0 journal lines `:10`) |
| **The promotion condition is unchanged** — no census arm reads the scrub record | `grep -c scrub tools/tsukuroi-census.sh` → `0`; `grep -c var/lib/btrfs` → `0`; `grep -c btrfs-scrub` → `0` |
| C1 does not add a storage arm either | `git diff -U0 c8efaa3f 44766208 -- tools/tsukuroi-census.sh` → 8 hunks: 6 headers name `probe_packages()`/`probe_update_safety()`, the other two add lines at 2350 and 2556, inside `run_selftest` (span `1931`–`3109`, `grep -n '^run_selftest() {\|^main() {'`); `--stat` → `33 insertions(+), 8 deletions(-)`; no hunk in `probe_storage_arm` (`1868`) |
| The `PROVINCE.md` and `README.md` anchors the draft cites are the intended lines | `sed -n '169p' PROVINCE.md` → "This area becomes Core only after a census arm exists; until then it is"; `:212` → "**Still Frontier:** the scrub record (`btrfs scrub status`, `/var/lib/btrfs/scrub.status.*`"; `:234` → "**Still Frontier, unchanged:** the scrub record and NVMe SMART."; `corpus/README.md:243` → "- Storage integrity is a frontier area, not Core: it becomes Core only after a read-only census arm reads it"; `corpus/README.md:284` → "## Round 38 — storage arm in the census; effective ALPM hook order (2026-10-26)" |
| The wave-2-only verdict binding the draft says it relies on | `grep -n 'w2-dispatch\|C2RevSC\|C2CritSC' tools/check-scrub-record-r42.py` → lines `16-22` (`bound(a.lane, rev, 'w2', f'C2RevSC{n}', 'reviewer', …)` at `:211`, critic at `:212`) |
| The table is well-formed Markdown | `python3` split on unescaped `\|` over the proposal → header 3 cells, separator 3 cells, data row 3 cells; the only pipe inside the data row is `LOCK_EX\|LOCK_NB` |
| This seat changed nothing in the lane | `git status --porcelain corpus/README.md PROVINCE.md tools/tsukuroi-census.sh` → empty |

Receipt: `.ufo/waves/round-42/w1/ScribeReadme/checks.txt` (sections 1–9, commands and raw output).

## Placement

- `corpus/README.md` is 404 lines; the new `## Round 42 — …` section appends after line 404, matching the round-38 to
  round-41 pattern (round heading, one-sentence append-only preamble, one `| Note | Holds | Sources |` table, then the
  Frontier note as `### Frontier notice — round 42`). The item's "`## Frontier` note" is delivered that way because the
  top-level `## Frontier` bullet list (`corpus/README.md:28-42`) is frozen as written by every round since 12, and
  rounds 38–41 all carry their Frontier notes in the round section.
- `PROVINCE.md` is 237 lines and ends with the round-39 closure; the new `## Round-42 storage reading — …` section
  appends after line 237, i.e. under the storage Frontier line `PROVINCE.md:212` and the round-38/39 sections that
  keep the scrub record Frontier.

## Proposed text 1 — append to `corpus/README.md` (after line 404)

```markdown
## Round 42 — the scrub status record on the storage Frontier (2026-10-26)

Append-only (drafted by wave seat `ScribeReadme`, integrated by the L1); the coverage map and Frontier bullets above
stay as written. The C2 entry is the first statement of the storage Frontier's scrub record — the surface
`../PROVINCE.md:212` keeps Frontier — and it is not a promotion: no census arm reads the record. C1 is a census
operability repair inside `probe_packages` and `probe_update_safety` plus two `run_selftest` cases (8 hunks, 33
insertions and 8 deletions at commit `44766208`; `probe_storage_arm` untouched), not a coverage surface.

| Note | Holds | Sources |
|---|---|---|
| `knowledge/btrfs-scrub-record-r42.md` | The scrub status record of the storage-integrity Frontier at btrfs-progs v7.1 as built by Arch `7.1-1` (kernel `7.2.11-arch1-1`), deepening the plane whose counter reading is `knowledge/storage-health-r26.md` (SH1–SH6): the record for one filesystem is `/var/lib/btrfs/scrub.status.<fsid>`, every update written to a `_tmp` sibling and moved over it with `rename`, a file the CLI creates mode 0600, every open taking a non-blocking exclusive `flock` (`LOCK_EX\|LOCK_NB`), so a reader sees the old or the new record and a held lock fails at once (SC1); the text format — first line `scrub status:1`, then one line per device, the filesystem UUID and the device id followed by `key:value` fields in a fixed order, fourteen progress and error counters then the five run fields `t_start`, `t_resumed`, `duration`, `canceled`, `finished` — so a record carries per-device sums and a per-device finished flag, not one filesystem verdict (SC2); the userspace `btrfs scrub start` process writes it, an all-zero record when the scrub starts and progress records while it runs, recording is switched off with a warning ending "status recording disabled" when `/var/lib/btrfs` cannot be created or the first record written, and whether a scrub is running is asked from the kernel per device with `BTRFS_IOC_SCRUB_PROGRESS`, so a missing record does not prove no scrub ran (SC3); `btrfs scrub status` treats an `ENOENT` open as no history and any other open failure as a warning, folds the device lines (start time the smallest, canceled if any device was, finished only if all are, from a starting 1), words the status `running`/`aborted`/`finished`/`interrupted` and prints `no stats available` with no start time, so `interrupted` is a process outcome, not a device fault (SC4); each device's `devinfo/<devid>/scrub_speed_max` limit reads 0 on a failed read, so "no limit" and "unreadable" cannot be told apart, and the limit, its status report and `btrfs scrub limit` arrived in btrfs-progs 6.6.3 (SC5); the host column reads this host unprivileged — root filesystem `1d02a454-c549-4a35-b567-89d60902af8e`, `/var/lib/btrfs` absent, no `btrfs-scrub@*` timer listed and the unit file `disabled`, the single device's limit 0, no kernel scrub line in the current boot | S237–S239 in `../SOURCES.md` (btrfs-progs v7.1 `cmds/scrub.c` sha256 `48df2e2f…` and `CHANGES` sha256 `bd881ab8…`, pinned in `.ufo/waves/round-42/frozen/src/` with `SHA256SUMS` and `FETCH.txt`; own-work capture `.ufo/waves/round-42/frozen/hostcap/capture.txt` sha256 `942edc91…`, captured 2026-10-26T19:13:44Z); `lessons/round-42.md` Gate (rows S237–S239); counter `../tools/check-scrub-record-r42.py` (frozen at `a84fc9de`, sha256 `dbe933ec…`); `../SCORECARD.md` "Round 42 — declaration" |

### Frontier notice — round 42

Round 42 promotes nothing. The entry above states the storage Frontier's scrub record — its file and write discipline,
its format, its writer and the switch that disables recording, the status command's fold and the per-device
throughput limit — on S237/S238/S239, beside the Core part of the same area, the per-device btrfs error counters the
round-38 arm reads (`corpus/README.md:284`). The round-26 rule that a Frontier area becomes Core only after a
read-only census arm reads it (`corpus/README.md:243`) is not met: at this round's tip
`grep -c scrub tools/tsukuroi-census.sh` prints `0`, and neither `var/lib/btrfs` nor `btrfs-scrub` appears in the
census (both `grep -c` print `0`); C1's hunks stay inside `probe_packages`, `probe_update_safety` and `run_selftest`
(`git diff -U0 c8efaa3f 44766208 -- tools/tsukuroi-census.sh`: 8 hunks, none in `probe_storage_arm`). The storage items
are therefore unchanged — the scrub record and NVMe SMART stay Frontier (`../PROVINCE.md:212,234`).

What the reading changes is triage, not ownership: "no scrub record" reads `UNRECORDED`, not `NEVER SCRUBBED` (SC3),
while SH4's `UNVERIFIED` for stored data stands; a record is per device, so a filesystem `finished` needs every device
finished and one canceled device makes the run `aborted` (SC2, SC4); `interrupted` is a process outcome, not media,
and the per-device error sums are where a device is judged (SC4); a slow scrub is checked against `scrub_speed_max`
before the device is blamed, where a failed read reads 0 (SC5).

Limits, as the entry states them. This host has no record to parse (`capture.txt:6`), so the format row and the status
fold are source-only here, and SC4's host cell records that the status command was not run when the entry was written.
Upstream is pinned at btrfs-progs v7.1 and the Arch build's packaging patches were not compared with `cmds/scrub.c`.
No census arm reads the record, so this Frontier ground is read, not covered by a gate. Row credit is not claimed here:
the wave-1 C2 reviews are first falsifiers whose corrections the L1 integrates before wave 2, and the counter's
verdict conjunct counts only the wave-2 `C2RevSC<n>`/`C2CritSC<n>` seats bound through `w2-dispatch.json` and
`w2-results.json` (`../SCORECARD.md` "Round 42 — declaration"; `../tools/check-scrub-record-r42.py:16-22`).
```

## Proposed text 2 — append to `PROVINCE.md` (after line 237)

```markdown
## Round-42 storage reading — R42-SCRUB-RECORD: the record's shape is read; the promotion condition is unchanged

Append-only; the round-26 frontier section, the round-38 promotion (R38-STORAGE-CORE) and the round-39 closure
(R38-ABSENT-ROOT) above stay as written, and the **Still Frontier** sentence that names the scrub record is neither
closed nor narrowed here.

Round 42 read the record itself instead of the host's counters. `corpus/knowledge/btrfs-scrub-record-r42.md` states,
at btrfs-progs v7.1 as built by Arch `7.1-1` on kernel `7.2.11-arch1-1`, five rows: the file
`/var/lib/btrfs/scrub.status.<fsid>`, written to a `_tmp` sibling and moved over by `rename`, created 0600, every open
under a non-blocking exclusive `flock` (SC1); the `scrub status:1` first line and the per-device `key:value` line with
its fixed field order (SC2); that the userspace `btrfs scrub start` process writes it, that recording is disabled with a
warning when the directory cannot be created or the first record written, and that running state comes from
`BTRFS_IOC_SCRUB_PROGRESS` rather than the file (SC3); how `btrfs scrub status` folds device lines — start time
smallest, canceled if any device was, finished only if all are, `running`/`aborted`/`finished`/`interrupted`,
`no stats available` on no start time, `ENOENT` as no history (SC4); and the per-device `scrub_speed_max` limit, which
reads 0 on a failed read and arrived with `btrfs scrub limit` in btrfs-progs 6.6.3 (SC5). Sources S237 and S238 (the
pinned v7.1 `cmds/scrub.c` and `CHANGES`) and S239 (this host's unprivileged capture: `/var/lib/btrfs` absent, no
`btrfs-scrub@*` timer listed and the unit file `disabled`, the root device's limit 0, no kernel scrub line in the
current boot).

**The promotion condition is unchanged.** The round-26 rule — "This area becomes Core only after a census arm exists"
(`PROVINCE.md:169`; `corpus/README.md:243`) — is not met for the scrub record: at this round's tip
`grep -c scrub tools/tsukuroi-census.sh` prints `0`, and neither `var/lib/btrfs` nor `btrfs-scrub` appears in the
census, so no arm reads `/var/lib/btrfs/scrub.status.<fsid>`, `btrfs scrub status` or `btrfs-scrub@.timer`; round 42's
C1 change stays inside `probe_packages`, `probe_update_safety` and `run_selftest` (8 hunks, 33 insertions and 8
deletions at `44766208`, `probe_storage_arm` untouched). The scrub record and NVMe SMART therefore stay Frontier
exactly as the round-38 promotion left them (`PROVINCE.md:212`, `:234`), and the second NVMe device stays unread.

**Within Frontier, what the reading buys.** Absence of a record is `UNRECORDED`, not "never scrubbed" (SC3); a record
is per device and a filesystem `finished` needs every device (SC2, SC4); `interrupted` is a process outcome, not media,
so a device is judged from its per-device error sums (SC4); a slow scrub is checked against `scrub_speed_max` before
the device is blamed, and a limit that reads 0 may be a failed read (SC5). SH4's `UNVERIFIED` for stored data is
unchanged.

**Limits.** This host has no record to parse (`.ufo/waves/round-42/frozen/hostcap/capture.txt:6`), so SC2's format and
SC4's fold are source-only here, and SC4's host cell records that the status command was not run when the entry was
written. The Arch `7.1-1` packaging patches were not compared with `cmds/scrub.c`. Row credit belongs to the wave-2
bound verdicts, not this paragraph: `python3 tools/check-scrub-record-r42.py --revision <REV>` (frozen at
`a84fc9de`, sha256 `dbe933ec…`) counts a row only from its bound `C2RevSC<n>`/`C2CritSC<n>` seats.

Operator-owned actions are unchanged: running a scrub, enabling `btrfs-scrub@.timer`, setting a per-device limit
(`btrfs scrub limit`) and any repair. No package, service, mount, scrub, counter-reset or configuration action is
authorized by this section.
```

Same text on disk: `.ufo/waves/round-42/w1/ScribeReadme/proposed-readme-round42.md` and
`.ufo/waves/round-42/w1/ScribeReadme/proposed-province-round42.md`.

## Findings

1. **Interlock, not a defect (L1 action).** The README row's Sources cell points at `lessons/round-42.md` Gate (rows
   S237–S239). That file is present but untracked and its Gate table is still the placeholder
   `<!-- GATE-ROWS -->` (`corpus/lessons/round-42.md:14-18`), which item D-3 (`ScribeGate`) fills. If D-3 does not
   land, shorten the cell to the S237–S239 registry rows and the counter, or the README will cite a table that does
   not exist.
2. **Interlock with the wave-1 C2 corrections.** Both drafts state the entry as committed at `f50c28d8` and leave the
   row's content to SC1–SC5 as written there. If the L1 integrates a wave-1 row correction that changes a statement
   (SC2's field list or SC4's fold are the likely candidates), the corresponding clause in the README row must be
   updated at integration; the Frontier-notice sentences that depend on SC3/SC4 (`UNRECORDED`, `interrupted`,
   `aborted`) are the ones to re-read.
3. **The item's "`## Frontier` note" cannot be a new bullet in the top-level list.** `corpus/README.md:28-42` is frozen
   by every round since 12 (`## Round 12` onwards all say "the coverage map and Frontier bullets above stay as
   written"), so the note lands as `### Frontier notice — round 42` inside the new round section, the pattern of
   rounds 38–41 (`corpus/README.md:293`, `:313`, `:331`, `:371`). This is a format reading, reported for the L1.
4. **The promotion-condition claim is measured, not asserted.** `tools/tsukuroi-census.sh` at this round's tip has
   zero occurrences of `scrub`, `var/lib/btrfs` and `btrfs-scrub`, and C1's 8 hunks lie in `probe_packages`,
   `probe_update_safety` and `run_selftest`. So "the promotion condition is unchanged" holds by measurement, and the
   draft does not repeat round-41's pattern of citing a condition without re-checking it.
5. **Coverage-map placement is a new section, not a row in the near-top table.** The near-top `## Coverage map` table
   (`corpus/README.md:3-21`) was last extended in fleet round 1; rounds 12–41 each add a section with its own table. The
   draft follows the current practice, so the round-42 row is discoverable by `grep -n btrfs-scrub-record
   corpus/README.md` only after the L1 integrates it.

## Out of scope / not done

- No counter was run: `check-scrub-record-r42.py` (wave-1 C2 verdicts are first falsifiers and are other seats' work),
  no census `--selftest`, no live census. My numbers above are digests, greps and one `git diff`.
- No scrub command was run (`btrfs scrub status`/`limit`), no sudo, no package/service/mount change, no scratch dir
  created (no fixture needed): `/fast/scratch/hyaku/tsukuroi-r42/ScribeReadme/` was never created, so nothing to
  remove.
- No `corpus/README.md`, `PROVINCE.md`, `SKILL.md`, lesson or `SOURCES.md` edit; no git/jj mutation of any kind.
- I did not evaluate whether the round-42 row earns `expansion improved` (item G-4's question) and did not write the
  SCORECARD outcome; both drafts deliberately avoid a promotion or trend claim.

## Artifact paths

- Report: `.ufo/waves/round-42/w1/ScribeReadme.md`
- Receipts: `.ufo/waves/round-42/w1/ScribeReadme/checks.txt`,
  `.ufo/waves/round-42/w1/ScribeReadme/proposed-readme-round42.md`,
  `.ufo/waves/round-42/w1/ScribeReadme/proposed-province-round42.md`
