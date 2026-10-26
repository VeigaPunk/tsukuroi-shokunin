VERDICT: draft

# P-3 — `## Storage integrity arm — round 38` and the storage-arm gate rows

Seat `DraftSkillStorage` (scribe, leaf), round 38 wave 1, axes operability/C1. Deliverable: the
exact SKILL.md markdown in §4 (section) and §5 (gate-registry rows), grounded on the frozen
counters and the round-26 sourcing. No lane file was edited; the only lane writes are this report
and the receipts in `.ufo/waves/round-38/w1/DraftSkillStorage/`.

## 1. Grounding — what the section must describe (read at the lane tip `5edb6c2`)

- Contract: `tools/tsukuroi-census.sh:350-370` — one line after the DRIFT line and before the
  rollup; fields `state`, `filesystems`, `devices`, `nonzero`, optional `detail`; BLOCKED when a
  filesystem has no devinfo entry or an `error_stats` file is unreadable/malformed, else DEGRADED
  when `nonzero > 0`, else HEALTHY; absent sysfs root = HEALTHY 0/0/0; counters never reset
  (`btrfs device stats -z` operator-owned); NVMe SMART (SH5/SH6) not read.
- Probe: `tools/tsukuroi-census.sh:1848-1887` — UUID-only filesystem dirs (`:1850,:1855`), five
  keys (`:1851`), `unreadable` (`:1860-1862`), `malformed` on any unknown/duplicate/missing key,
  non-integer value or extra token (`:1863-1876`), `no-devinfo` (`:1879`), state precedence
  `BLOCKED` then `DEGRADED` then `HEALTHY` (`:1882-1884`), detail appended without trailing comma
  (`:1885`). Emitted at `:3007-3008`; the rollup starts at `:3010`.
- Selftest: six R38-C1 cases at `:2889-2922` — absent root (`:2889-2891`), zero (`:2893-2897`),
  nonzero + `010` is ten (`:2899-2904`), missing counter with a healthy sibling count
  (`:2906-2911`), duplicate/extra line (`:2913-2917`), no-devinfo (`:2919-2922`). Each asserts
  `exit 0, HEALTHY` rollup beside the STORAGE line, i.e. verdict neutrality.
- `journalctl --grep` exits 1 on no-match, not failure: `tools/tsukuroi-census.sh:192`.
- Vocabulary the draft must respect: `SKILL.md:34-36` — `DEGRADED` is not an outage, `BLOCKED`
  is not "the hardware/package is corrupt".
- Sourcing: `corpus/knowledge/storage-health-r26.md:13-25` (SH1, five counters and names;
  "never add -z"), `:27-39` (SH2, persistent totals; error-level `errs:` line dates an incident,
  info-level mount line reprints the total; reset is operator-owned), `:114` ("No census arm
  reads these signals yet" — historical for these counters only). `corpus/SOURCES.md:134` (S128,
  `btrfs device stats` / `error_stats` mirror) and `:139` (S133, sysfs emission — including
  "or the word invalid when the stats were not loaded").
- Declaration and amendment: `SCORECARD.md:2117` (C1 predicate `fixtures_matched ==
  FIXTURES_EXPECTED and live_match == 1 and six_planes_all == 1`) and `:2133-2152` (QUALITY 82
  conjunct, `ns_views_matched == VIEWS and ns_available == 1`, tool sha256
  `a183ff58…`); after receipt `.ufo/waves/round-38/after/c1-after-52ffd65.json` = PASS (10/10,
  live 1, six_planes 1).
- Registry format: operative table `SKILL.md:3050` ("round36 superseding current rows"), columns
  `Name | Kind | Entry command | Verdict map | Self-test | Pinned values | Write scope | Owner`;
  round-37 precedent at `:3111`; the two round-38 rows already at `:3113-3114`.

## 2. Independent read-only runs (my own; `--shared` clone under scratch)

Clone: `git clone -q --shared …/tsukuroi-shokunin /fast/scratch/hyaku/tsukuroi-r38/DraftSkillStorage/lane`,
`remote remove origin`, tip `5edb6c2`; `sha256sum tools/tsukuroi-census.sh` =
`8e0084f67ad4783a980d5c2eaba453f51f1fc5d75408a1c9021a7249ac9aba1c`, and
`git diff 52ffd65f868431f021b8615ab281efd87195eac6..HEAD -- tools/tsukuroi-census.sh` is empty, so
the arm bytes at tip are the implementation commit's.

| Run | Command (scratch `S` = `/fast/scratch/hyaku/tsukuroi-r38/DraftSkillStorage`) | Observed |
|---|---|---|
| v1 counter | `TMPDIR=$S python3 tools/score-storage-arm-r38.py --revision 52ffd65f868431f021b8615ab281efd87195eac6 --repo $S/lane --scratch $S/v1` | exit 0; `fixtures_matched` 10/10, `live_match` 1, `six_planes_all` 1; live line `STORAGE btrfs-device-stats state=HEALTHY filesystems=1 devices=1 nonzero=0` |
| q82 counter | `TMPDIR=$S python3 tools/score-storage-arm-r38-q82.py --revision 52ffd65f868431f021b8615ab281efd87195eac6 --repo $S/lane --scratch $S/q82` | exit 0; `ns_views_matched` 3/3, `ns_available` 1 |
| census selftest | `TMPDIR=$S bash tools/tsukuroi-census.sh --selftest` | exit 0; `TSUKUROI_CENSUS_SELFTEST: PASS (111 cases, 111 passed, 0 failed)`; all six `R38-C1` cases PASS |
| census live | `TMPDIR=$S bash tools/tsukuroi-census.sh` | exit 1 (rollup DEGRADED); six `PLANE` lines at output lines 2-7, `DRIFT` at 10, `STORAGE btrfs-device-stats state=HEALTHY filesystems=1 devices=1 nonzero=0` at 11, rollup at 12 |
| direct sysfs | `stat -c '%a %U:%G %n' /sys/fs/btrfs/*/devinfo/*/error_stats; cat …` | `444 root:root`, one fs `1d02a454-…`, devid 1, five counters `0` |
| journal dating command | `journalctl --no-pager -o short-iso -p err _TRANSPORT=kernel --grep 'BTRFS.*errs: wr'` | rc 1 with `-- No entries --` (no error-level `errs:` line on the retained boots) |

Receipts: `v1-counter.json`, `q82-counter.json`, `selftest-storage-cases.txt`,
`census-live-lines.txt`, `sysfs-live.txt`, `journal-grep.txt`, `digests.txt` in
`.ufo/waves/round-38/w1/DraftSkillStorage/`. Scratch removed after copying; no `/tmp` path is
cited as evidence.

## 3. Findings that shape the draft

- **F1 — the registry rows already exist (item is stale by one pre-dispatch commit).** Commit
  `5edb6c2` (01:33:02 -0300, "round-38: registry rows for storage-arm-r38, storage-arm-r38-q82,
  hook-order-r38 (QUALITY 70)") added them at `SKILL.md:3113-3114`; the w1 spec was written
  01:32:34 and the earliest wave-1 seat artifact is 02:06. A landing must **not** insert them a
  second time; §5 is a verified restatement that adds the predicate field names and the observed
  control scores.
- **F2 — `invalid` is a second legal kernel emission, labelled `malformed`.** S133
  (`corpus/SOURCES.md:139`) records the single word `invalid` when stats were never loaded;
  `probe_storage_arm` rejects it as `malformed` (`tools/tsukuroi-census.sh:1866-1876`), and none
  of the six fixtures covers it. Confirmed independently in the wave by `.ufo/waves/round-38/w1/
  C1RevKernelFormat.md` §2-§3 (fail-closed, transient, no wrong-HEALTHY path). The draft's
  `malformed` row names both causes and sends the operator to re-read, not to conclude corruption.
  I proposed no census change (not my item); my text does not contradict the code as landed.
- **F3 — `BLOCKED` outranks `DEGRADED`, and counted pairs still print.** `:1883` gives BLOCKED
  precedence, but `nonzero`/`detail` are filled from readable devices first; selftest `:2906-2911`
  reads `state=BLOCKED … nonzero=1 detail=11111111:1:malformed,11111111:2:read_errs=2`. The
  draft has a row for this so `BLOCKED` is not misread as "no errors".
- **F4 — verdict neutrality is observable, not just declared.** Selftest `:2902-2904` asserts
  `TSUKUROI_CENSUS: HEALTHY` with `STORAGE … DEGRADED`; my live run shows the converse (rollup
  DEGRADED, `STORAGE … HEALTHY`). The draft tells the operator to read the line itself.
- **F5 — `--grep` rc 1 is a no-match.** Documented at `tools/tsukuroi-census.sh:192` and observed
  in my journal run; the draft says so, so the dating command cannot be mistaken for a failed probe.
- **F6 — `detail` is unvalidated diagnostic text.** The `<devid>` token is the raw `devinfo`
  basename (`:1861`, `:1872`, `:1875`); `.ufo/waves/round-38/w1/C1SentGrammar.md` §2 shows an
  injection through it. The draft says treat `detail` as data, never paste into a shell.
- **F7 — `HEALTHY` on this line is not storage-integrity clearance.** The arm reads the five
  counters only; the scrub record (SH3/SH4) and NVMe SMART (SH5/SH6) stay unread, and
  `storage-health-r26.md:114` remains true for them. The draft says this explicitly (consistent
  with the sibling draft `.ufo/waves/round-38/w1/DraftProvince/province-append-r38.md`).

## 4. Exact markdown — the section

Append as a new section (placement in §6):

<!-- BEGIN exact SKILL.md section -->

## Storage integrity arm — round 38

The census reads the five per-device btrfs error counters and prints one **verdict-neutral** line
after `DRIFT pacnew-plane` and before the rollup (`tools/tsukuroi-census.sh:350-370` contract,
`:1848-1887` probe, `:3007-3008` emitted). It adds no `PLANE`, no rollup term and no exit-code
change: the selftest keeps `TSUKUROI_CENSUS: HEALTHY` while the line reads `state=DEGRADED`
(`tools/tsukuroi-census.sh:2902-2904`), and the round-38 live run read five `PLANE` lines
`DEGRADED` beside `STORAGE … HEALTHY` at exit 1. **Read the line itself; the rollup never carries
it.** Normative detail: `corpus/knowledge/storage-health-r26.md` SH1 (`:13-25`) and SH2
(`:27-39`); sources S128 (`corpus/SOURCES.md:134`) and S133 (`corpus/SOURCES.md:139`).

Grammar — exactly one line per run:

    STORAGE btrfs-device-stats state=HEALTHY|DEGRADED|BLOCKED filesystems=N devices=N nonzero=N [detail=<fsid8>:<devid>:<key>=<value>|...]

`filesystems` and `devices` count sysfs directories — UUID-named filesystems and their
`devinfo/<devid>` entries; `features` and non-UUID names are ignored (`:2895-2897`). `nonzero`
counts (device, counter) **pairs** above zero, not errors. `detail` carries only the non-zero
pairs and/or one reason token per device: `unreadable`, `malformed`, `no-devinfo`.

| `STORAGE` line | Operator reading | Action — read-only unless marked operator |
|---|---|---|
| `state=HEALTHY filesystems=0 devices=0 nonzero=0` | The sysfs root is absent: no btrfs filesystem is mounted. This is the arm's declared pass value for "none present", not a reading of storage. | Confirm the root filesystem (`findmnt -no FSTYPE,TARGET /`). If a btrfs mount is expected, record `0/0/0` as a mount finding; it is not clearance. |
| `state=HEALTHY filesystems=N devices=N nonzero=0`, N ≥ 1 | All five counters on every enumerated device read 0 at this instant (SH1). The line covers the counters only — no scrub record (SH4), no NVMe SMART (SH5, SH6). | None for the counters. Do not read `HEALTHY` as storage-integrity clearance; SH4/SH5/SH6 stay separate and `UNVERIFIED`/operator-owned. |
| `state=DEGRADED nonzero=N detail=<fsid8>:<devid>:<key>=<value>,...` | A stored lifetime total, not a dated event (SH2). `key` names the class: `write_errs`, `read_errs`, `flush_errs` = failed IO; `corruption_errs` = checksum mismatch or corrupt metadata header; `generation_errs` = block generation mismatch (SH1; S128). `nonzero` N is the pair count, so read `detail` for the values. | Date the errors from error-level kernel lines, every retained boot: `sudo -n journalctl --no-pager -o short-iso -p err _TRANSPORT=kernel --grep 'BTRFS.*errs: wr'`; rc 1 with `-- No entries --` is a no-match, never a failed probe (`tools/tsukuroi-census.sh:192`). The same text at info level at mount reprints the stored total (SH2), and an operator-run scrub can also increment the counters (SH2 wave-2 correction). Record the `errs:` line with its boot. **Never reset while dating**: `btrfs device stats -z` is operator-owned and destroys the history (SH1/SH2; `tools/tsukuroi-census.sh:364-366`). |
| `state=BLOCKED detail=<fsid8>:<devid>:unreadable` | The `error_stats` file exists but was not readable (`[ ! -f ] \|\| [ ! -r ]`, `:1860-1862`). | Check sysfs readability: `ls -l /sys/fs/btrfs/<fsid>/devinfo/<devid>/error_stats` (mode `444` on this host, unprivileged read) and `cat` it. Still unreadable: record the line verbatim, check the mount and the kernel module. `BLOCKED` means "cannot be assessed read-only", never "the disk is corrupt" (`SKILL.md:36`). |
| `state=BLOCKED detail=<fsid8>:<devid>:malformed` | The file did not carry exactly the five counters once each as non-negative integers (`:1863-1876`). Causes: a truncated, duplicated or renamed counter, or the kernel's single word `invalid` when device stats were never loaded (S133, `corpus/SOURCES.md:139`; transient while `dev_stats_valid` is 0). | Re-read once with `cat` and record the bytes verbatim; never infer a counter from a partial read and never reset. For `invalid`, re-read after the mount settles — an uninitialised reading, not corruption. |
| `state=BLOCKED detail=<fsid8>:-:no-devinfo` | A mounted filesystem exposed no `devinfo` entries (`:1879`), so no device was assessed. | Re-run the census once, then `ls /sys/fs/btrfs/<fsid>/devinfo`; record both runs. Not a counter reading and not evidence of errors. |
| `state=BLOCKED` with `nonzero=N`, N > 0 | `BLOCKED` outranks `DEGRADED` in the state word, but counted pairs still print: one malformed device beside a sibling at `read_errs=2` reads `state=BLOCKED … nonzero=1 detail=11111111:1:malformed,11111111:2:read_errs=2` (selftest `:2906-2911`). | Handle the `BLOCKED` reason first, then date the counted pairs exactly as in the `DEGRADED` row. A `BLOCKED` line is not "no errors"; a `DEGRADED` line is not an outage (`SKILL.md:35`). |

`detail` is data: the `<devid>` token is the raw `devinfo` entry basename, printed without
validation (`:1861`, `:1872`, `:1875`); quote it and never paste a `detail` field into a shell.
A green example is not a clearance: the round-38 freeze read `STORAGE btrfs-device-stats
state=HEALTHY filesystems=1 devices=1 nonzero=0` (one device, five counters zero) — re-measure,
never quote as current state.

Not covered by this line, unchanged: the scrub record (SH3, SH4), NVMe SMART/Health (SH5, SH6) and
disk-space runway (mori). `corpus/knowledge/storage-health-r26.md:114` still says "No census arm
reads these signals yet" — true for SH3-SH6, historical for the SH1/SH2 counters from this round.

Counting: `python3 tools/score-storage-arm-r38.py --revision <REV>` (ten fixtures, the live leg,
six `PLANE` lines per run) and `python3 tools/score-storage-arm-r38-q82.py --revision <REV>`
(census with no override inside `unshare -rm`, a per-run random tree over `/sys/fs/btrfs`). The
second is required: a fixture-gated arm passes the first (QUALITY 82,
`.ufo/waves/round-38/controls/controls-q82.jsonl`).

<!-- END exact SKILL.md section -->

## 5. Exact markdown — gate-registry rows

Both rows belong to the operative table at `SKILL.md:3050`; row 1 is the item's row, row 2 is the
amendment conjunct without which C1 is not verified (`SCORECARD.md:2142-2152`). They are already
present at `:3113-3114` (F1) — this is the verified text, not a second insertion.

<!-- BEGIN exact registry rows -->

| storage-arm-r38 | gate | `python3 tools/score-storage-arm-r38.py --revision <REV> [--repo <PATH>] [--scratch <DIR>]` | 0 `fixtures_matched` 10/10 and `live_match` 1 and `six_planes_all` 1;1 any fixture, the live leg or the six-`PLANE` count differs;2 revision, git or bash could-not-evaluate | none: the ten built-in fixtures F01-F10 and the live leg are the measurement; controls `.ufo/waves/round-38/controls/controls.jsonl` (do-nothing 0/10, constant emitter 2/10, naive emitter 6/10 with five planes) | R38 C1 frozen at `7cbaeb63`; tool sha256 `e649bfb33ed99161dc3affdacd7fa86fa8d96e2c5bb60b2d22d6fc12a7f82218`; never sufficient alone — a fixture-gated arm passes it (QUALITY 82, `controls-q82.jsonl`), so C1 also needs `storage-arm-r38-q82` | private mkdtemp under `--scratch`/`TMPDIR`; reads the census at REV through git; no host write | tsukuroi |
| storage-arm-r38-q82 | gate | `python3 tools/score-storage-arm-r38-q82.py --revision <REV> [--repo <PATH>] [--scratch <DIR>]` | 0 `ns_views_matched` 3/3 and `ns_available` 1;1 a view differs;2 revision, `unshare` or v1-model digest could-not-evaluate | none: three per-run random views are the measurement; controls `.ufo/waves/round-38/controls/controls-q82.jsonl` (fixture-gated 0/3 FAIL, cached-live 1/3 FAIL, real arm 3/3 PASS) | R38 pre-seat amendment `9c9bb647`; tool sha256 `a183ff580cb92cdd276a5720adb54336e7e247c9bd7c81058065e706d62d99e3`; loads the v1 model from `7cbaeb63` by digest | `unshare -rm` child namespace with a bind mount over `/sys/fs/btrfs` that never leaves it; scratch under `--scratch`/`TMPDIR` | tsukuroi |

<!-- END exact registry rows -->

## 6. Placement

- Rows: end of the operative table `## Gate and probe registry — round36 superseding current rows`
  (`SKILL.md:3050`), after `hook-order-r38` (`:3115`). At the tip rows 1-2 already sit at
  `:3113-3114`; land only the missing text, never a duplicate row.
- Section: append after the table (after `:3115`, end of file), so the table stays contiguous and
  the reading section follows it — the same order round 35 used (its section at `:3007` follows
  its registry at `:2945`). Do not insert the section between the table header and its rows.

## 7. What I did not do

- Did not edit, create or delete any tracked lane file; no git/jj write; no lane or host mutation;
  no sudo; no package, service, sysfs, counter-reset or boot change; no tool install or upgrade.
- Did not run `python3 tools/check-storage-health.py` (the SH1/SH2 evidence gate) or
  `check-hook-order-r38.py`; neither is my item.
- Did not test a live BLOCKED or DEGRADED host state (that would require mutating sysfs); those
  rows rest on the six selftest cases and the pinned code, not on a live fault.
- Did not verify SH3-SH6 (scrub record, NVMe SMART) — the draft deliberately leaves them outside
  this line.
- Did not re-measure the host beyond the read-only runs listed in §2; the section's green example
  is labelled a freeze-time snapshot, not current state.

## 8. Tooling

No installs or upgrades. Used the preinstalled `git`, `bash`, `python3`, `journalctl`,
`sha256sum`, `stat`, `findmnt` (proposed command only, not run).
