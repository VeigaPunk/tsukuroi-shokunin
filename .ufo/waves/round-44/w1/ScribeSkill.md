VERDICT: draft

# Seat ScribeSkill — item F-4: two `SKILL.md` sections for round 44

Draft only. Wave 1 produces no counted verdict; the arm and the rows are judged by
`tools/score-scrub-arm-r44.py` and `tools/check-scrub-record-r44.py`, whose C2 verdict conjuncts bind only from
wave-2 seats (`tools/check-scrub-record-r44.py:21-31`). Nothing below claims that either counter PASSes: I ran
neither (see §7).

Lane reads only. No lane file created, edited or deleted; no git/jj mutation; no host mutation (no sysctl, sysfs
write, unit, timer, package, scrub or limit command); no `sudo`. Scratch
`/fast/scratch/hyaku/tsukuroi-r44/ScribeSkill/` removed on exit after the two receipts were copied to
`.ufo/waves/round-44/w1/ScribeSkill/` (§7).

## 1. What the draft is grounded on

| Read | Identity / anchor |
|---|---|
| Census contract for the arm | `tools/tsukuroi-census.sh:384-410` (header paragraph "Round-44 addition (C1)"), probe `:1967-2040`, print site `:3374-3376`; 9 `(R44-C1)` selftest cases at `:3229-3285` |
| Census selftest, first-hand | `bash tools/tsukuroi-census.sh --selftest` → exit 0, `TSUKUROI_CENSUS_SELFTEST: PASS (141 cases, 141 passed, 0 failed)`, 0 stderr lines, 9 case labels matching `(R44-C1)`, 41.9 s wall (receipt `w1/ScribeSkill/selftest.out:144`, `selftest.err` empty) |
| Live host shape, first-hand | `uid=1000`; `/var/lib/btrfs` absent; `timers.target.wants` exists with no `btrfs-scrub@*` entry; `/sys/fs/btrfs/1d02a454-c549-4a35-b567-89d60902af8e/devinfo/1/scrub_speed_max` mode 644 root value 0; `/sys/fs/btrfs` also holds a non-UUID `features` entry (receipt `w1/ScribeSkill/host-shape.txt`) |
| Frozen sources re-read this seat | `.ufo/waves/round-42/frozen/src/scrub.c` (S237) `:67,421,917-925,969,1293,1295,1335-1336,1430-1431`; `.ufo/waves/round-43/frozen/src/ioctl.c` (S240) `:3132-3133,3139,3141`; `.ufo/waves/round-44/frozen/src/scrub.c` (S242) `:1380-1381,3321,3331,3336`; `sysfs.c` (S243) `:72,74,2028,2040,2044,2048`; `btrfs-scrub@.timer` `:5,7,8,11`; `btrfs-scrub@.service` `:9,10`; `PKGBUILD` `:100-101` |
| Entry rows to point at | `corpus/knowledge/btrfs-scrub-record-r44.md` SR7 `:15-53`, SR8 `:55-85`, SR9 `:86-126`, triage `:128-136`, Limits `:138-145` |
| Declaration | `SCORECARD.md:2746` (round-44 declaration), `:2760` (C1 row), `:2761` (C2 row); promotion condition `PROVINCE.md:212-214` and `corpus/README.md:243`, re-asserted `corpus/README.md:424`; operator-owned list `PROVINCE.md:215` |
| Wave-1 falsifiers already on disk (cited, not re-run) | `w1/C1ExecEdgeNames.md` (65 edge fixtures, 5 gaps), `w1/C1CritChannels.md` (open channels), `w1/C1ExecLiveRead.md` (no-file live mode, live line), `w1/C1ExecSelftest.md` (132 → 141), `w1/C1CritAxis.md` (sub-surface narrowing), `w1/C2DraftCritSR7.md` (the "exactly while" overreach), `w1/C2DraftCritSR9.md` (units are packaging-side) |

Both drafts are appendable as written: no earlier `SKILL.md` text changes, no row of the operative registry table
is touched (see §5, item 1 for the one integration gap this raises).

## 2. Proposed text — section one (append verbatim)

```markdown
## Scrub-record census arm — round 44

Appended 2026-10-26 (round-44 C1; drafted by wave-1 seat ScribeSkill, pending L1 integration).
Surface: `probe_scrub_record` (`tools/tsukuroi-census.sh:1967-2040`) prints one verdict-neutral line after the
STORAGE line and before the rollup (`:3374-3376`); the contract is the census header paragraph "Round-44 addition
(C1)" (`:384-410`). What the arm reads: entry **names and stat** under `/var/lib/btrfs`, the per-device sysfs
`scrub_speed_max` value, and `btrfs-scrub@*.timer` entry names under `timers.target.wants` — never a record's
content, never an ioctl, never the kernel's running state (round-43 SR6,
`corpus/knowledge/btrfs-scrub-record-r43.md:98-117`). Read the Frontier condition (`PROVINCE.md:212-214`,
`corpus/README.md:243`) as met for this sub-surface only: the artifact set around the record, not the record's data
and not running state (`w1/C1CritAxis.md` §2-3). Live shape at the declaration: `state=NONE dir=absent records=0
tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0` (`w1/C1ExecLiveRead/live-run-a.txt:12`), which is the
record directory absent, no enabled instance and devid 1 unlimited (S245 `capture.txt:3-6`).

| Observation | Reading | Action |
|---|---|---|
| `state=NONE\|RECORDED\|BLOCKED` — BLOCKED if any block reason, else RECORDED when records+tmp+sockets > 0, else NONE (`tools/tsukuroi-census.sh:2034-2035`; header `:406-407`) | `NONE`: no record, tmp or progress artifact exists (the directory may still be present and empty). `RECORDED`: at least one artifact exists, so something is worth reading. `BLOCKED`: a reading failed (`:400-406`) | `BLOCKED` is an unknown, not an absence — hand it to the operator, who re-reads as root (`btrfs scrub status <path>`); the census creates nothing |
| `dir=absent\|present\|unreadable` — no entry / a listable directory / an entry that is not a listable directory (`:1997-2001`) | `absent` on a btrfs host means no record write has created the directory yet: btrfs-progs' path is `/var/lib/btrfs/scrub.status` (S237 `scrub.c:67`) and its `mkdir_p` warns `status recording disabled` when it cannot create it (`scrub.c:1335-1336`); `unreadable` is BLOCKED `dir:unreadable` | read-only: `absent` is a finding, not a to-do — never `mkdir` the directory (a host write) |
| `records=N` — regular files named `scrub.status.<fsid>` (lowercase UUID); a symlink or non-regular file of that name is BLOCKED `record:not-regular` (`:2005-2007`; header `:390-392`) | one record per filesystem that has been scrubbed; names are read, content never is (`:1996`) | the operator reads a record as root (`btrfs scrub status <path>`); no lane process opens it |
| `tmp=N` — `scrub.status.<fsid>_tmp`; a wrong type is BLOCKED `tmp:not-regular` (`:2010-2012`) | round-43 SR1: every update opens it without `O_TRUNC`, writes from the start and renames it over the record only after a successful write (S237 `scrub.c:917-925`); a leftover means an update failed or its writer died before the rename, and a later, shorter record can carry its tail [inference, reproduced in a harness] | note it and leave it — deleting is a write; a stale `_tmp` is an operator-visible artifact, not a lane action |
| `sockets=N` — sockets named `scrub.progress.<fsid>`; anything else of that name is BLOCKED `progress:not-socket` (`:2014-2016`) | a `btrfs scrub start` progress socket; a killed start can leave one, so presence is **not** the running state (`:391-394`) — running needs `CAP_SYS_ADMIN` (round-43 SR6) | never infer a running scrub from a socket; the only running reading is a privileged `btrfs scrub status`, which the operator runs |
| `unreadable=N` — records and tmp files the caller cannot read (`:2008`, `:2013`; header `:394-396`) | a root scrub writes mode-0600 files, so a nonzero count is the normal shape after a root scrub, not integrity evidence (`:394-396`) | re-read as root if the record matters; never `chmod` (a write) |
| `orphan=N` — records whose fsid has no entry under `TSUKUROI_BTRFS_SYSFS` (`:2009`; header `:394-396`) | the record belongs to a filesystem that is not mounted now; computed only when the sysfs root is listable | read-only: confirm the filesystem with `lsblk`/`btrfs filesystem show`; never mount to reach the record |
| `limited=N` plus `detail=<fsid8>:<devid>:speed_max=<v>` — devices whose `devinfo/<devid>/scrub_speed_max` reads one decimal line other than 0 (`:1985-1992`; header `:396-398`) | the only file content the arm reads: 0 = no limit, nonzero = the throttle in bytes/s (round-44 SR8; S243 `sysfs.c:2028`) | compare `limited` with an observed slow scrub (`corpus/knowledge/btrfs-scrub-record-r44.md:132-133`); the value is root's to set — the census never writes the attribute |
| `timers=N` — `btrfs-scrub@<instance>.timer` entries under `TSUKUROI_TIMER_WANTS`; the bare template is not counted (`:2027-2030`; header `:398-400`) | an enabled instance of the packaged monthly scrub (round-44 SR9; S244 `btrfs-scrub@.timer:5,8,11`); 0 = no scheduled scrub on this host | `systemctl enable` is operator-owned and outside the census; the arm only counts links |
| `detail=…` — block reasons in traversal order, then the speed pairs; bytewise under `LC_ALL=C` (`:1968`, `:2037-2038`; header `:407`) | the first token says why the line is BLOCKED; speed pairs are informational and come after every block reason; no name is ever echoed (`:394`) | read the first token; a name carrying a newline still prints one line (selftest `:3278`) |

| BLOCKED reason | Produced when (locus) | Reading / action |
|---|---|---|
| `dir:unreadable` | the record directory exists but is not a listable directory (`tools/tsukuroi-census.sh:1998-1999`) | the record set is unknown, not empty; the operator re-reads as root — never `chmod` or `mkdir` |
| `sysfs:unreadable` | the sysfs root exists but is not listable (`:1974-1975`) | mounted set and limits unknown; operator reads `/sys/fs/btrfs` directly |
| `sysfs:absent` | at least one record present, no sysfs root to judge orphans by (`:2019`) | orphan-ness unknown; operator confirms which filesystems are mounted |
| `record:not-regular` | a symlink or non-regular file at a record name (`:2006`) | not a btrfs-progs record; read-only inspection, never replace the entry |
| `tmp:not-regular` | same class at a `_tmp` name (`:2011`) | as above; SR1 leaves good `_tmp` files regular |
| `progress:not-socket` | a non-socket at a progress name (`:2015`) | not a live start socket; nothing may be inferred from it |
| `<fsid8>:<devid>:speed-unreadable` | the attribute is missing or unreadable (`:1986`) | the device's limit is unknown, never "no limit"; operator reads sysfs as root |
| `<fsid8>:<devid>:speed-malformed` | not exactly one decimal line (`:1989-1991`) | the attribute is not the kernel's `%llu\n` shape (S243 `sysfs.c:2028`); record it as unknown |
| `<fsid8>:?:bad-devid` | a `devinfo` entry whose name is not decimal (`:1984`) | not a kernel devinfo name (S243 `sysfs.c:2048` `BTRFS_ATTR_RW(devid, …)`); unknown device, no limit claim |
| `timers:unreadable` | the wants directory exists but is not listable (`:2024-2025`) | enabled-instance count unknown, not 0; operator reads `systemctl list-timers` |

Counter: `python3 tools/score-scrub-arm-r44.py --revision <REV> --scratch <DIR> [--lane <repo>]` (sha256
`1409a5fd75adaa4c0a238a7f9ad31621dd34a52ad1a40483e4a18d27c9536388`) — PASS iff `cases == 16 and correct == 16 and
identity_ok == 1 and wired_ok == 1 and live_agree == 1 and selftest_pass == 1 and selftest_r44 >= 6`
(`tools/score-scrub-arm-r44.py:52-54`): 16 drawn production-path cases in a private user+mount namespace, the wired
full-census leg (one SCRUB line, equal to the oracle, between STORAGE and the rollup), the live leg against an
independent walk of the three paths, and the census selftest (`:29-45`). One heavy counter — run it alone, it mounts
namespaces, runs the full census and the selftest. The selftest it scores is 132 → 141 cases with nine `(R44-C1)`
labels (`tools/tsukuroi-census.sh:3229-3285`); observed 2026-10-27 in a seat scratch: `TSUKUROI_CENSUS_SELFTEST:
PASS (141 cases, 141 passed, 0 failed)`, exit 0. After receipt: `.ufo/waves/round-44/after/c1-after-ab8aae1.jsonl`
(arm revision `ab8aae16`, same census blob as the declared implementation `7e081698`).

Recorded limits (wave-1 findings, not claimed as fixed): the header's own — an absent sysfs root with no record
reads `limited=0`, and the STORAGE line's mount-table guard is what flags a hidden sysfs (`tools/tsukuroi-census.sh:407-408`);
five uncontracted shapes, none reachable on this host's live shape (`w1/C1ExecEdgeNames.md` §5) — a sysfs root that
exists but is not a directory reads `RECORDED orphan=0` with no reason (locus `:2019`), timer entries are counted with
no link-type check (`:2027-2031`), a symlink at `scrub_speed_max` is followed and its target read (`:1986`), a mounted
fsid with no `devinfo` reads `limited=0` unflagged (`:1982`), and the attribute read is unbounded (`:1987-1990`;
live risk nil, the kernel emits one page, S243 `sysfs.c:2028`); orphan counting rescans the mounted-fsid list per
record, so cost is quadratic in fsid count (`:2009`; 4000 records + 4000 fsids = 1525 ms, `w1/C1ExecEdgeNames.md`
§1); the counter's namespace legs differ from production in supplementary groups, cwd, stdin, `statfs` and process
ancestry, and control K7 (mount-table gate) fires in the legs only (`w1/C1CritChannels.md` §1,
`controls/battery-summary-c1.jsonl`); live mode creates no file — 29 read-only syscalls in the arm window and a
write-class profile identical to base (`w1/C1ExecLiveRead.md` §B-C).
```

## 3. Proposed text — section two (append verbatim, after section one)

```markdown
## Scrub record — round 44 rows

Appended 2026-10-26 (round-44 C2; drafted by wave-1 seat ScribeSkill, pending L1 integration).
Entry `corpus/knowledge/btrfs-scrub-record-r44.md` rows SR7, SR8, SR9 on S242 (Linux v7.2.11 `fs/btrfs/scrub.c`),
S243 (`fs/btrfs/sysfs.c`) and S244 (Arch btrfs-progs 7.1-1 `btrfs-scrub@.timer`, `btrfs-scrub@.service`,
`PKGBUILD`), with S237 (btrfs-progs v7.1 `cmds/scrub.c`), S240 (`fs/btrfs/ioctl.c`) and the own-work host capture
S245. Row status: judged by the counted wave-2 reads (`tools/check-scrub-record-r44.py`); wave-1 reads are drafts and
bind no verdict (`w1/C2DraftCritSR7.md`, `w1/C2DraftCritSR9.md`). Supersession: SR7 fills the success direction that
round-43 SR6 left open (`corpus/knowledge/btrfs-scrub-record-r43.md:98-117`); SR8 carries the mode and parse detail
round-42 SC5 did not state; SR9 grounds the packaged unit round 43 cited only by name.

| Observation | Reading | Action |
|---|---|---|
| A device carries a scrub context only inside the run's attached window: `btrfs_scrub_dev` refuses a second run with `-EINPROGRESS` while `dev->scrub_ctx` is set, attaches its context before any scrub work and detaches it when the work ends; every return path leaves the field as it found it (S242 `scrub.c:3147,3153,3159,3222`; r44 SR7 `:17-21`; the "exactly while it runs" phrasing is narrowed to the attached window by `w1/C2DraftCritSR7.md` §1) | a non-NULL context means a scrub, or a device replace, is running on that device at that moment (S242 `scrub.c:3081,3120-3121`; replace call sites `dev-replace.c:701-703,1265-1267`, unpinned in the entry) | read it only through a privileged `btrfs scrub status`; the census never calls the ioctl |
| `btrfs_scrub_progress` returns 0 only when the devid exists and carries a context, `-ENOTCONN` for an idle device, `-ENODEV` for an unknown devid (S242 `scrub.c:3331,3336`; r44 SR7 `:22-24`) | 0 = running now; `ENOTCONN` = idle, never 0; `ENODEV` = not a device of that filesystem — a momentary per-device answer, not a record of past scrubs (r44 `:25-28,130-131`) | "running" says nothing about when a scrub last ran or how it ended; the record files are where history lives |
| The progress ioctl handler copies the arguments back only when the return is 0, and only after its `CAP_SYS_ADMIN` gate (S240 `ioctl.c:3132-3133,3139,3141`; r44 SR7 `:24-25`; the gate itself round-43 SR6) | an unprivileged caller gets `-EPERM` and no arguments, so an unprivileged `btrfs scrub status` never prints `running` | a missing `running` is a privilege gate, not "no scrub ran"; stored-data integrity stays `UNVERIFIED` unprivileged (SH4) |
| Each device's limit is the sysfs attribute `devinfo/<devid>/scrub_speed_max`, declared `BTRFS_ATTR_RW` and built with `__INIT_KOBJ_ATTR(_name, 0644, …)` (S243 `sysfs.c:72,74,2048`; r44 SR8 `:57-59`) | any user reads it; only root writes it (host: mode 644 root, S245 `capture.txt:4`) | the census reports `limited=` and never writes the attribute |
| Reading prints the in-memory limit as one decimal number and a newline (S243 `sysfs.c:2028`; r44 SR8 `:59-60,62-63`) | one line, no suffix; 0 means no limit, because the scrub throttle returns at once on 0 (S242 `scrub.c:1380-1381`) | a slow scrub with a nonzero `limited` is the configured cap at work (r44 `:132-133`) |
| Writing parses with `memparse`, so `K`/`M`/`G` suffixes are accepted, trailing whitespace is skipped, and trailing text is rejected with `-EINVAL` (S243 `sysfs.c:2040,2044`; r44 SR8 `:58-62`) | a nonzero value is a configured cap in bytes per second; the value is root's to set | setting or clearing the limit is operator action on sysfs; no lane path does it |
| Arch's btrfs-progs package, not upstream, ships the scrub units: `PKGBUILD` installs `btrfs-scrub@.service` and `btrfs-scrub@.timer` into `/usr/lib/systemd/system` (S244 `PKGBUILD:100-101`; r44 SR9 `:88-90`; upstream v7.1 has no units, `w1/C2DraftCritSR9.md` S1) | a host whose installed units hash to the pinned files runs the packaged shape (S245 `capture.txt:7-9`) | installing, upgrading or removing the package is operator-owned; the census reads only the installed names |
| The timer is `OnCalendar=monthly`, `RandomizedDelaySec=1w`, `Persistent=true`, `WantedBy=timers.target` (S244 `btrfs-scrub@.timer:5,7,8,11`; r44 SR9 `:90-92`) | a monthly scrub exists only when an instance is enabled, which creates a `timers.target.wants/btrfs-scrub@<instance>.timer` link; this host has none and `btrfs-scrub@-.timer` is `disabled` (S245 `capture.txt:5-6`) | the census counts links (`timers=`); `systemctl enable` is operator action, outside the census |
| The service runs `btrfs scrub start -B %f` with `KillSignal=SIGINT` (S244 `btrfs-scrub@.service:9,10`; r44 SR9 `:92-95`) | `-B` keeps the start in the foreground and sets `do_print`, so the recording failures of round-43 SR3 print into the service log (S237 `scrub.c:1293,1295`); the foreground handler issues `BTRFS_IOC_SCRUB_CANCEL` on SIGINT (S237 `scrub.c:421,1546`) | stopping a running scrub service is operator action; when they do, expect a canceled record |
| A device whose scrub ioctl returns nonzero is recorded with `canceled` set, and `btrfs scrub resume` takes up a canceled or unfinished record, summing its counted fields and keeping its `t_start` (S237 `scrub.c:969,1430-1431`; r44 SR9 `:94-96`; round-43 SR3) | counters and start time are cumulative over the interrupted run and the resume; `canceled` in a record is not a defect | read, do not add a previous reading; starting, cancelling or resuming a scrub is operator-owned (`PROVINCE.md:215`) |

Limits carried from the entry (r44 `:138-145`): kernel behaviour is pinned at Linux v7.2.11 source lines and the Arch
patch touches no file under `fs/`, so the booted kernel's `fs/btrfs/scrub.c` and `sysfs.c` are the pinned ones
[inference carried from round 43, not re-measured]; SR7 is read from source only, no privileged ioctl is run on this
host; SR9's systemd half (that `KillSignal=` is the signal `systemctl stop` sends) is systemd.kill(5) behaviour and
stays inference — the pinned part is the unit text and the btrfs-progs handler.
```

## 4. Coverage map (what each row discharges)

Arm section — every field token of the line (`tools/tsukuroi-census.sh:2036`) and every reason token of the BLOCKED
list (`:400-406`) has exactly one row:

| Token | Row |
|---|---|
| `state` / `dir` / `records` / `tmp` / `sockets` / `unreadable` / `orphan` / `limited` / `timers` / `detail` | field table, rows 1-10 |
| `dir:unreadable` / `sysfs:unreadable` / `sysfs:absent` / `record:not-regular` / `tmp:not-regular` / `progress:not-socket` / `speed-unreadable` / `speed-malformed` / `bad-devid` / `timers:unreadable` | reason table, ten rows |

Rows section — SR7 (3 rows: context lifetime, errno direction, privilege gate) covers `r44:15-53`; SR8 (3 rows:
mode/path, read shape, write parse) covers `r44:55-85`; SR9 (4 rows: packaging provenance, timer shape and wants
link, service shape and cancel path, canceled record and resume) covers `r44:86-126`. Every action in both sections
is a read or an operator handoff: no scrub start/cancel/resume/limit, no sysfs write, no `systemctl enable`.

## 5. Findings for the integrator (not part of the draft)

1. **The two round-44 counters have no row in the operative registry table.** `grep -n 'scrub-arm-r44|scrub-record-r44' SKILL.md`
   returns nothing; the highest complete table ends with the round-43 rows (`SKILL.md:4111-4112`, which carry
   `bootinputs-r43` and `scrub-record-r43`). The round-43 section records that `check-registry-coverage.py` read 66 of
   68 tools registered when two counters were missing, so the round-44 table must add `scrub-arm-r44` (gate,
   `python3 tools/score-scrub-arm-r44.py --revision <REV> --scratch <DIR> [--lane <repo>]`, predicate §2) and
   `scrub-record-r44` (gate, `python3 tools/check-scrub-record-r44.py --revision <REV>`, predicate
   `rows == 3 and quotes_ok == 3 and props_ok == 3 and host_ok == 3 and sources_ok == 1 and verdicts_ok == 3 and
   novelty_base_hits == 0 and pointer_ok == 1`, `tools/check-scrub-record-r44.py:109-110`). I did not add rows: the
   table is not mine to edit and a gate row is a claim, not a draft.
2. **The promotion wording is a separate item (C1-13).** My section one states the sub-surface in its opening
   paragraph so the entry cannot be read as "the record's content is now Core"; `w1/C1CritAxis.md` §6 owns the
   `corpus/README.md`/`PROVINCE.md` wording. The two must agree — if the L1 keeps the promotion prose wider than my
   opening paragraph, the paragraph should be amended, not the claim.
3. **Entry-row line spans will move if the L1 edits the r44 entry.** I cite `r44:15-53,55-85,86-126,132-133,138-145`;
   the two wave-1 critics propose replacement Statement sentences (`w1/C2DraftCritSR7.md` §1 for SR7,
   `w1/C2DraftCritSR9.md` for SR9) that add lines. The spans, not the row names, would then need re-reading.
4. **The nine `(R44-C1)` count is a floor, not the case list.** The counter requires `selftest_r44 >= 6`
   (`tools/score-scrub-arm-r44.py:53-54`) while the census carries nine labels (`:3229-3285`; observed 9 by regex on
   the tool text). If a later edit drops to six, the predicate still passes — a narrowing the registry row should not
   present as "nine cases asserted".

## 6. Citation audit (every line I quote in the drafts, re-read this seat)

| Cited | Observed content |
|---|---|
| `S240 ioctl.c:3132-3133` | `if (!capable(CAP_SYS_ADMIN))` / `return -EPERM;` |
| `S240 ioctl.c:3139,3141` | `ret = btrfs_scrub_progress(fs_info, sa->devid, &sa->progress);` / `if (ret == 0 && copy_to_user(arg, sa, sizeof(*sa)))` |
| `S242 scrub.c:3331,3336` | `sctx = dev->scrub_ctx;` / `return dev ? (sctx ? 0 : -ENOTCONN) : -ENODEV;` |
| `S242 scrub.c:1380-1381` | `bwlimit = READ_ONCE(device->scrub_speed_max);` / `if (bwlimit == 0)` |
| `S243 sysfs.c:72,74` | `#define BTRFS_ATTR_RW(_prefix, _name, _show, _store)` / `__INIT_KOBJ_ATTR(_name, 0644, _show, _store)` |
| `S243 sysfs.c:2028,2040,2044,2048` | `return sysfs_emit(buf, "%llu\n", READ_ONCE(device->scrub_speed_max));` / `limit = memparse(buf, &endptr);` / `return -EINVAL;` / `BTRFS_ATTR_RW(devid, scrub_speed_max, btrfs_devinfo_scrub_speed_max_show,` |
| `S244 PKGBUILD:100-101` | two `install -Dm644 … "${pkgdir}/usr/lib/systemd/system/…"` lines |
| `S244 timer:5,7,8,11` | `OnCalendar=monthly` / `RandomizedDelaySec=1w` / `Persistent=true` / `WantedBy=timers.target` |
| `S244 service:9,10` | `KillSignal=SIGINT` / `ExecStart=/usr/bin/btrfs scrub start -B %f` |
| `S237 scrub.c:67` | `#define SCRUB_DATA_FILE "/var/lib/btrfs/scrub.status"` |
| `S237 scrub.c:917-925` | open of the `.tmp` name, write, then `scrub_rename_file(SCRUB_DATA_FILE, fsid, "tmp")` |
| `S237 scrub.c:969,1293,1295` | `sp->stats.canceled = !!ret;` / `do_background = false;` / `do_print = true;` |
| `S237 scrub.c:1335-1336` | `if (mkdir_p(datafile)) {` / `warning("cannot create scrub data file, mkdir %s failed: %m, status recording disabled",` |
| `S237 scrub.c:1430-1431` | `if (resume && last_scrub && (last_scrub->stats.canceled ||` / `!last_scrub->stats.finished)) {` |
| `tools/tsukuroi-census.sh` loci | printed with the draft above; each was read numbered (probe `:1967-2040` whole, print site `:3374-3376`, nine checks at `:3229-3285`) |
| `corpus/knowledge/btrfs-scrub-record-r44.md` | SR7 heading `:15`, statement `:17`, host reading `:52`; SR8 `:55,57,83`; SR9 `:86,88,124`; triage `:128-136`; Limits `:138-145` |
| `PROVINCE.md:212-214,215` | Frontier bundle text and "**Operator-owned:** running a scrub, enabling its timer, resetting a counter …" |
| `corpus/README.md:243,424` | the promotion condition and the round-43 re-assertion "the scrub record stays Frontier (no census arm reads it)" |
| Host capture S245 `capture.txt:3-6` | `var_lib_btrfs absent`; devid 1 attribute `mode=644 owner=root value=0`; wants instances 0; `btrfs-scrub@-.timer` `disabled` |

## 7. Not done

- Did not run `score-scrub-arm-r44.py` (C1 counter) or `check-scrub-record-r44.py` (C2 counter). The C2 counter would
  FAIL by construction in wave 1 (`verdicts_ok` needs wave-2 seats); the C1 counter is another seat's item and a
  heavy run I did not need for a draft. Neither counter's result is claimed here.
- Did not run the live census; the live SCRUB line and the rollup are cited from `w1/C1ExecLiveRead/live-run-a.txt`
  (line 12 and the `TSUKUROI_CENSUS: BLOCKED (…)` line above it), not re-observed.
- Did not re-run the wave-1 fixtures whose numbers I cite (`C1ExecEdgeNames` 65 cases, `C1CritChannels` channels,
  `C1ExecSelftest` 132 → 141); each is cited by report path. The selftest PASS line I do state is first-hand (§1,
  receipt `w1/ScribeSkill/selftest.out:144`).
- Did not edit the lane: no `SKILL.md`, `corpus/`, `SCORECARD.md` or tool change; no registry row; no commit.
- Did not exercise any host write: no sysfs write, no unit/timer, no package, no scrub/limit command, no `sudo`.
- Tool installs: none.

## 8. Receipts

- `.ufo/waves/round-44/w1/ScribeSkill.md` (this report)
- `.ufo/waves/round-44/w1/ScribeSkill/selftest.out` (144 lines, 141 PASS + the summary line; sha256 below)
- `.ufo/waves/round-44/w1/ScribeSkill/selftest.err` (0 bytes)
- `.ufo/waves/round-44/w1/ScribeSkill/host-shape.txt` (live read-only shape, 2026-10-27T00:23:09Z)
- `.ufo/waves/round-44/w1/ScribeSkill/sha256.txt` (digests of the three receipts above)
