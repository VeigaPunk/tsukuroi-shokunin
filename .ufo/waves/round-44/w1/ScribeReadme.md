VERDICT: draft

# Seat ScribeReadme — F-5: round-44 promotion notes (PROVINCE.md, corpus/README.md)

Item: draft the append-only promotion notes for `PROVINCE.md` (after the round-43 note) and
`corpus/README.md` (coverage map / Frontier; the scrub-record line), stating what moves Frontier → Core (the
unprivileged scrub-record view the `SCRUB` line reads), what stays Frontier (record content, running state per
SR6/SR7, NVMe SMART), what stays operator-owned, and the counting command — in the round-38/round-39 register.

This is a **draft**: the lane files were read only. No lane file was created, edited or deleted by this seat; the
only writes are this report and `w1/ScribeReadme/receipts.jsonl`. No counter and no census was run for this item
(the pre-wave C1 receipt is cited as the record of the measurement, and no measurement is claimed here).

## 1. Ground read (all read-only)

| Artifact | What was read | Line anchor |
|---|---|---|
| `PROVINCE.md` | round-38 promotion section (the register to copy), round-39 limit closure, round-42 and round-43 notes; file ends at line 254, last bytes `…is unchanged.\n` | `PROVINCE.md:199-224`, `:225-238`, `:239-245`, `:246-254` |
| `corpus/README.md` | coverage map, `## Frontier`, the round-26 Frontier bullets, rounds 38–43 notices; file is 425 lines | `corpus/README.md:3-22`, `:28-43`, `:241-244`, `:293-301`, `:313-317`, `:406-425` |
| `tools/tsukuroi-census.sh` | the arm's contract paragraph, `probe_scrub_record`, its print site, the rollup, the env defaults, the nine selftest cases | `:384-410` (header "Round-44 addition (C1)"), `:1967-2040` (function), `:3374-3376` (print after `STORAGE`), `:3378-3391` (rollup + `TSUKUROI_CENSUS`), `:492-495` (defaults), `:3229-3286` (cases) |
| `corpus/knowledge/btrfs-scrub-record-r44.md` | SR7, SR8, SR9 statements (the three rows the arm leans on) | `:13-40` (SR7), `:55-63` (SR8), `:86-96` (SR9) |
| `.ufo/waves/round-44/frozen/hostcap/capture.txt` | S245 host capture: `var_lib_btrfs absent`, one device `devid 1` limit `value=0` `mode=644 owner=root`, `wants_btrfs_scrub_instances 0`, `btrfs-scrub@-.timer disabled`, units owned by `btrfs-progs 7.1-1` | `capture.txt:1-10` |
| `.ufo/waves/round-44/after/c1-after-ab8aae1.jsonl` | the pre-wave C1 receipt: `verdict PASS`, `cases 16`, `correct 16`, `identity_ok 1`, `wired_ok 1`, `live_agree 1`, `selftest_pass 1`, `selftest_r44 9`, `selftest_line "TSUKUROI_CENSUS_SELFTEST: PASS (141 cases, 141 passed, 0 failed)"`, `revision ab8aae16…`, `tool_revision 1d2afffe…`, `live.got "SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0"` | receipt line 2 |

Where the scrub-record line lives in README: the Frontier bullet at **`corpus/README.md:243`** ("Storage
integrity is a frontier area, not Core: it becomes Core only after a read-only census arm reads it…"), restated in
the round-38/39/40/41 notices at `:296`, `:315`, `:335`, `:384` and in the round-42/43 coverage notes at `:410-414`,
`:420`, `:424`. The register for a promotion is an appended note at the end of the file (rounds 38–43 all append),
so the draft below appends after line 425 and **references** line 243 without editing it.

## 2. Draft A — `PROVINCE.md`, append after line 254 (end of file)

One blank line, then exactly:

```markdown
## Round-44 promotion — R44-SCRUB-VIEW: the unprivileged scrub-record view moves Frontier → Core

Append-only; the round-38 promotion, the round-39 limit closure and the round-42 and round-43 notes above stay as
written. The condition those sections set — "it becomes Core only after a read-only census arm reads it"
(`corpus/README.md:243`) — is met for the part of the scrub record an unprivileged reader can see.

**Core now:** the census's verdict-neutral `SCRUB btrfs-scrub-record state=NONE|RECORDED|BLOCKED
dir=absent|present|unreadable records=N tmp=N sockets=N unreadable=N orphan=N limited=N timers=N [detail=...]`
line (`probe_scrub_record` in `tools/tsukuroi-census.sh`, printed after the `STORAGE` line and before
`TSUKUROI_CENSUS`; contract in that file's header paragraph "Round-44 addition (C1)"). It reads the record
directory by name and stat only: the record `scrub.status.<fsid>`, its `_tmp` staging file and the
`scrub.progress.<fsid>` socket under `/var/lib/btrfs` (override `TSUKUROI_SCRUB_DIR`), with an `unreadable` count
(records and `_tmp` files the caller cannot read, a root-written record being 0600) and an `orphan` count (a record
whose fsid has no entry under `/sys/fs/btrfs`, override `TSUKUROI_BTRFS_SYSFS`, so that filesystem is not mounted
now); each fsid's `devinfo/<devid>/scrub_speed_max` (a nonzero decimal is a limit and is listed in `detail`; SR8);
and the enabled instances `btrfs-scrub@<instance>.timer` under `/etc/systemd/system/timers.target.wants` (override
`TSUKUROI_TIMER_WANTS`; the bare template name is not an instance and is not counted; SR9). The arm reads no
record content, makes no ioctl, calls neither `btrfs` nor `systemctl`, needs no privilege and creates no file; the
line is never a rollup term and never an exit-code input.

**Still Frontier:** the record's content — a root-written record is mode 0600 and every open takes
`flock(LOCK_EX|LOCK_NB)` (SR1, round-43 note above), so the arm counts and stats it rather than parsing it; the
running state — `BTRFS_IOC_SCRUB_PROGRESS` needs `CAP_SYS_ADMIN` (SR6) and returns 0 only while `dev->scrub_ctx`
is attached, `-ENOTCONN` for an idle device (SR7), so a leftover progress socket is counted as `sockets=N` and is
not the running state; and NVMe SMART/Health (`smartctl -H -A`, `nvme smart-log`; SH5/SH6). The second NVMe device
(xfs on `/tmp`, `/fast`) still has no btrfs counters and stays unread.
**Operator-owned:** running, canceling, resuming or limiting a scrub, enabling its timer, resetting the error
counters (`btrfs device stats -z`), profile changes, firmware, LUKS and any repair. **Mori's, unchanged:**
disk-space runway as fleet capacity, under the round-26 wave-2 split. **Known limit:** an absent sysfs root with no
record reads `limited=0`, and the `STORAGE` line's mount-table guard is what flags a hidden sysfs
(`corpus/README.md:315`); a record's readability is counted, never its content; and the arm's namespace legs leave
the mount-table, `uid_map` and script-path channels open (QUALITY 90 "named open"; control C1-K7 holds the arm to
the real path only when `/proc/self/mountinfo` shows tmpfs on `/var/lib`), while this host's live answer is
constant (`NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0`), so a census that
behaves honestly only there cannot be told apart here; no host-side injection is authorized (read-only lane).

Counted by `python3 tools/score-scrub-arm-r44.py --revision <REV> --scratch <DIR>` (frozen; sha256
`1409a5fd75adaa4c0a238a7f9ad31621dd34a52ad1a40483e4a18d27c9536388`; predicate `cases == 16 and correct == 16 and
identity_ok == 1 and wired_ok == 1 and live_agree == 1 and selftest_pass == 1 and selftest_r44 >= 6`) at the
round-44 measured revision (`SCORECARD.md` "Round 44 — measured outcome"). The census selftest it runs reports 141
cases, nine of them labelled `(R44-C1)`. No package, service, mount, scrub, timer, counter-reset, firmware or
configuration action is authorized by this section.
```

## 3. Draft B — `corpus/README.md`, append after line 425 (end of file)

One blank line, then exactly:

```markdown
## Round-44 coverage note (appended 2026-10-26)

Append-only; the coverage map, the Frontier bullets and the round-38 to round-43 notes above stay as written.

| Note | Holds | Sources |
|---|---|---|
| `../tools/tsukuroi-census.sh` (`probe_scrub_record`, round-44 C1) | The verdict-neutral scrub-record arm: one `SCRUB btrfs-scrub-record state=NONE\|RECORDED\|BLOCKED dir=absent\|present\|unreadable records=N tmp=N sockets=N unreadable=N orphan=N limited=N timers=N [detail=…]` line from names and stat only under `/var/lib/btrfs` (the `scrub.status.<fsid>` records, their `_tmp` staging files, the `scrub.progress.<fsid>` sockets; the `unreadable` and `orphan` counts), each fsid's `devinfo/<devid>/scrub_speed_max` (nonzero = limited, listed in `detail`) and the enabled `btrfs-scrub@<instance>.timer` links under `timers.target.wants` (the bare template is not an instance); BLOCKED when a reading is unavailable, RECORDED when record, `_tmp` or socket names exist, NONE otherwise; never content, never an ioctl, never a rollup term | S237, S242, S243, S244; `knowledge/btrfs-scrub-record-r44.md` SR7–SR9; receipt `.ufo/waves/round-44/after/c1-after-ab8aae1.jsonl` |
| `knowledge/btrfs-scrub-record-r44.md` | Storage-integrity frontier, scrub record, the three rows the arm relies on: SR7 the scrub-progress success direction (`btrfs_scrub_progress` returns 0 only while `dev->scrub_ctx` is attached, `-ENOTCONN` for an idle device, `-ENODEV` for an unknown devid; the ioctl handler copies back only on 0; device replace runs through the same `btrfs_scrub_dev`); SR8 `scrub_speed_max` (`BTRFS_ATTR_RW` mode 0644, `%llu` read, `memparse` write, `-EINVAL` on trailing text, 0 = no limit); SR9 the Arch-packaged `btrfs-scrub@.timer`/`.service` (monthly, `RandomizedDelaySec=1w`, `Persistent=true`, `WantedBy=timers.target`, `btrfs scrub start -B %f`, `KillSignal=SIGINT` → the foreground handler's `BTRFS_IOC_SCRUB_CANCEL`, a canceled record) | S237, S240, S242, S243, S244; S245 host capture `.ufo/waves/round-44/frozen/hostcap/capture.txt`; counter `tools/check-scrub-record-r44.py` |

### Frontier notice — round 44

The round-26 condition at `corpus/README.md:243` is met for the unprivileged scrub-record view only: the census now
reads the record directory by name and stat, the per-device limit and the enabled timer instances, so that part of
the storage-integrity frontier moves Frontier → Core (`../PROVINCE.md` "Round-44 promotion — R44-SCRUB-VIEW"). The
record's content (SR1, a 0600 root-written file opened under `flock(LOCK_EX|LOCK_NB)`), the running state (SR6
`CAP_SYS_ADMIN`; SR7 0 only while a scrub context is attached, so a progress socket is a reading, not the running
state) and NVMe SMART/Health (SH5/SH6) stay Frontier, as they have since round 26; running, canceling, resuming or
limiting a scrub, enabling its timer, resetting the error counters, profile changes, firmware, LUKS and any repair
stay operator-owned. Measured with `../tools/score-scrub-arm-r44.py --revision <REV> --scratch <DIR>` at the
revision named in `../SCORECARD.md` "Round 44 — measured outcome"; the depth entry is counted by
`tools/check-scrub-record-r44.py --revision <REV>` (predicate `rows == 3 and quotes_ok == 3 and props_ok == 3
and host_ok == 3 and sources_ok == 1 and verdicts_ok == 3 and novelty_base_hits == 0 and pointer_ok == 1`, its
three row verdicts binding only from the round-44 wave-2 reviewer and critic seats). Known limit: an absent sysfs
root with no record reads `limited=0` (the `STORAGE` mount-table guard, `corpus/README.md:315`, flags a hidden
sysfs), a record's readability is counted and its content never read, and the arm's namespace legs leave the
mount-table, `uid_map` and script-path channels open (control C1-K7). Host at lane revision `ab8aae16`:
`NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0` (receipt
`.ufo/waves/round-44/after/c1-after-ab8aae1.jsonl:2`), consistent with S245 (no `/var/lib/btrfs`, one device at
`scrub_speed_max` 0 mode 644 root, 0 enabled scrub timer instances).
```

## 4. Coverage of the item's four required elements

| Required | Draft A (PROVINCE) | Draft B (README) |
|---|---|---|
| what moves Frontier → Core | "**Core now:**" paragraph — the `SCRUB` line, names/stat only, the speed limit, the timer instances, no privilege/ioctl/rollup | round-44 row 1 + "Frontier notice — round 44" first sentence, anchored to `:243` |
| what stays Frontier (record content, running state SR6/SR7, NVMe SMART) | "**Still Frontier:**" paragraph — SR1 content, SR6/SR7 running state, SH5/SH6 SMART, the xfs NVMe | "Frontier notice" second sentence |
| what stays operator-owned | "**Operator-owned:**" + "**Mori's, unchanged:**" | "Frontier notice", operator clause |
| the counting command | "Counted by `python3 tools/score-scrub-arm-r44.py --revision <REV> --scratch <DIR>` …" + predicate + sha256 + 141 cases / nine `(R44-C1)` | "Measured with `../tools/score-scrub-arm-r44.py --revision <REV> --scratch <DIR>` …" + the depth counter with its predicate |

## 5. Facts the drafts assert, and their evidence

| Assertion in the drafts | Evidence |
|---|---|
| the line is printed after `STORAGE` and before the rollup, and is never a rollup term | `tools/tsukuroi-census.sh:3374-3376` (arm call + `printf`), `:3378-3391` (`roll` built from the six plane verdicts only; `TSUKUROI_CENSUS` prints six terms) |
| the arm reads names and stat only, never record content | `tools/tsukuroi-census.sh:1996-2021` (record directory) and `:2022-2033` (timer links): `-e`/`-L`/`-f`/`-S`/`-r`/`-d` tests and the name regexes only; the only file content read is `devinfo/<devid>/scrub_speed_max` (`:1985-1992`, one line, `^[0-9]+$`) |
| record, `_tmp`, socket names, `unreadable`, `orphan`, `limited`, `timers` | `tools/tsukuroi-census.sh:387-399` (contract), `:2002-2036` (implementation) |
| defaults `/var/lib/btrfs`, `/sys/fs/btrfs`, `/etc/systemd/system/timers.target.wants` and their overrides | `tools/tsukuroi-census.sh:492-495` (`BTRFS_SYSFS`, `SCRUB_DIR`, `TIMER_WANTS`), `:435-438` (documented overrides) |
| nine selftest cases labelled `(R44-C1)`; 132 → 141 | `grep -c '(R44-C1)' tools/tsukuroi-census.sh` → `9`; `grep -c "^  check '"` → `129` at `98020ece` and `138` at HEAD, plus 3 `check_cli '` at both → `132` and `141` (receipt `selftest_line` prints `141 cases`) |
| C1 counter sha256 and predicate | `sha256sum tools/score-scrub-arm-r44.py` → `1409a5fd…6388`; `tools/score-scrub-arm-r44.py --help` shows `--revision REVISION --scratch SCRATCH [--lane LANE]`; predicate quoted from receipt line 2 field `predicate` |
| C2 counter predicate and wave-2-only verdicts | `tools/check-scrub-record-r44.py:109-110` (`PREDICATE = 'rows == 3 and quotes_ok == 3 and props_ok == 3 and host_ok == 3 and sources_ok == 1 and verdicts_ok == 3 and novelty_base_hits == 0 and pointer_ok == 1'`), `:108` `VERDICT_RE = 'ROW (SR\d) VERDICT: (holds|partly|fails)'` |
| the host's live `SCRUB` answer and the receipt revision | `.ufo/waves/round-44/after/c1-after-ab8aae1.jsonl:2` (`live.got`, `revision ab8aae16…`) |
| S245 host values named in draft B | `.ufo/waves/round-44/frozen/hostcap/capture.txt:3-8` (`var_lib_btrfs absent`; `scrub_speed_max … /devinfo/1/scrub_speed_max mode=644 owner=root value=0`; `wants_btrfs_scrub_instances 0`) |
| SR7/SR8/SR9 content as summarised | `corpus/knowledge/btrfs-scrub-record-r44.md:13-40`, `:55-63`, `:86-96` |

## 6. Gates, placeholders and limits (for the integrator)

1. **Placeholders to fill at append time.** `<REV>`, `<DIR>`, and the forward reference to `SCORECARD.md`
   "Round 44 — measured outcome". These notes are promotion text and are appended **after** the round's
   measurement; wave 1 has no measured revision, so no measured outcome is claimed here.
2. **Heading id `R44-SCRUB-VIEW` is my proposal** (the register uses ids such as `R38-STORAGE-CORE` and
   `R38-ABSENT-ROOT`). Draft B's cross-reference `../PROVINCE.md` "Round-44 promotion — R44-SCRUB-VIEW" must be
   kept identical if the id is renamed.
3. **Census bytes at HEAD are the measured bytes**: `git diff --stat ab8aae16..HEAD -- tools/tsukuroi-census.sh`
   prints nothing (commits `7e081698` and `ff2c264a` touch the C2 entry / receipts / dispatch, not the census), so
   the draft cites the receipt's `ab8aae16` line as the arm's host reading.
4. **No `SKILL.md` citation.** Rounds 38 and 42 cited `../SKILL.md` sections for their arms; at HEAD `ff2c264a`
   `grep -n 'R44\|round 44\|round-44' SKILL.md` returns 0 matches, so neither draft cites SKILL.md. If the
   integrator adds a "scrub-record arm — round 44" SKILL section, add it to draft B's row-1 Sources cell.
5. **No counted verdicts in wave 1** — draft B therefore cites the C2 counter and its predicate, not a pass, and
   says its row verdicts bind only from the wave-2 reviewer/critic seats.
6. **Known limits restated, not closed**: the namespace channels (mount table, `uid_map`, script path; control
   C1-K7) and the constant live answer mean the host cannot distinguish a census that behaves honestly only in a
   namespace; the drafts keep that as a Known limit, as round-39 did.
7. **What I did not do**: did not edit `PROVINCE.md` or `corpus/README.md`; did not run
   `tools/score-scrub-arm-r44.py`, `tools/check-scrub-record-r44.py` or `tools/tsukuroi-census.sh` (live or
   `--selftest`); ran no package, service, sysfs, scrub or mount action; installed no tool; left the lane git/jj
   state untouched. Every statement above is either a file line or a command output in `receipts.jsonl`.

## 7. Receipts

- `.ufo/waves/round-44/w1/ScribeReadme/receipts.jsonl` — 17 rows, each `{fact, cmd, rc, observed}`: counter
  sha256s, the extracted C1 receipt fields and live line, selftest and `check_cli` counts at base and HEAD, the nine
  `(R44-C1)` labels, the empty `ab8aae16..HEAD` census diff, the arm print site, `probe_scrub_record` bounds, the
  arm defaults, `corpus/README.md:243`, the file lengths, the S245 capture head and the SKILL.md grep counts.
- Scratch `/fast/scratch/hyaku/tsukuroi-r44/ScribeReadme/` is removed after the receipt copy.
