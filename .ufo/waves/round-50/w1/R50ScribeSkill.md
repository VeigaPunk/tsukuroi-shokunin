VERDICT: draft

# R50ScribeSkill — D-1: draft body for `## Scrub grounding — round 50 admission`

Item D-1 (prose). Execution class EXEC-AUTHORIZED: the commands this seat ran are read-only
`git -C … show 8029cdba:<path>` reads of the frozen bytes, plus one read of the frozen counter to
learn the exact marker strings the L1 must write. Nothing was executed against the counter, the
census or any fixture; no scratch was created (the seat wrote no fixture, clone or mutant, so
`/fast/scratch/hyaku/tsukuroi-r50/R50ScribeSkill/` was never populated and needs no removal).

## What the L1 must supply around this draft

1. The heading line, exactly (the frozen counter compares the stripped line to `MARK_SKILL`):
   `## Scrub grounding — round 50 admission`
   — `tools/check-scrub-admission-r50.py:97` (`MARK_SKILL`), consumed at `:362`
   (`any(ln.strip() == MARK_SKILL for ln in skill.split('\n'))`). My draft below deliberately
   starts *after* that line.
2. The entry heading `## Gate status — round 50 (GR1-GR3 admitted)` replaces the current
   `## Gate status — round 50 (pending; the round-50 cohort has not settled)`
   (`MARK_ENTRY`, `:96`) — L1's edit, outside every row extent per `FROZEN.md` §"Frozen row hashes".
3. The README sentence naming `btrfs-scrub-grounding-r45.md` and `admitted round 50` in one
   sentence that no negation word governs (`MARK_README` `:98`, `NEGATE_RE` `:99`:
   `unadmitted|not admitted|never admitted|stay pending|stays pending`).
4. Append point: `SKILL.md` ends at the round-49 selftest section
   (`8029cdba:SKILL.md:4563`, last line `… current: 167 cases, PASS.`), so this section appends at
   end of file.

**Draft is conditional on admission.** The prose is written for the admitted state. If the cohort
settles a bound `partly`/`fails`, do not integrate it; the round-49 section
(`8029cdba:SKILL.md:4548-4561`) is the precedent for what is written instead.

## Axes named (Godspeed)

- **depth** (C1's axis, lowest tied 8): does the section say *what* each row decides, at the
  precision the entry pins it, without adding a proposition the entry does not carry.
- **docs/operability**: can a reader who never opens the entry act on the three surfaces from this
  section alone — the parse, the `EINPROGRESS` question, the stop signal — and know which actions
  are not theirs.
- **calibration**: the two `[inference]` marks that survive are stated as surviving, in the same
  words the counter requires (`CORR49_REQ[0]`, `tools/check-scrub-admission-r50.py:107`), so the
  section cannot drift into claiming more than the entry.
- **adjacency**: the census surface is named by the fields the census actually prints, so the
  section does not send a reader to a line the census does not emit.

Moves kept: one move per axis, all improving, none harming — the three-row "what is pinned" block
(depth), the triage table (operability), the explicit two-limits paragraph (calibration), the
census-lines paragraph including the *negative* ("the census does not report replace state")
(adjacency).

## Sources read (all read-only, frozen bytes)

| What | Where |
|---|---|
| SKILL house style, tail and round-49 section | `8029cdba:SKILL.md:4548-4572` |
| round-45 scrub grounding section (the direct precedent, same entry) | `8029cdba:SKILL.md:4286-4328` |
| round-44 scrub-record census arm + rows (table + counter + limits form) | `8029cdba:SKILL.md:4184-4214` |
| round-46 census identity section (Surface/Counter/Recorded limits form) | `8029cdba:SKILL.md:4426-4456` |
| entry `source:` line, GR1, GR2, GR3, triage, Limits, QUALITY, gate status r50 | `8029cdba:corpus/knowledge/btrfs-scrub-grounding-r45.md:1-8, 18-…, 229-240, 295-306` |
| frozen claims, row hashes, cohort shape, controls | `8029cdba:.ufo/waves/round-50/frozen/FROZEN.md` |
| census SCRUB line contract | `8029cdba:tools/tsukuroi-census.sh:386-406` |
| census `probe_scrub_record` (fields, `detail`, `state`) | `8029cdba:tools/tsukuroi-census.sh:1976-2050` |
| census SCRUB selftest expectations (16 `(R44-C1)` labels) | `8029cdba:tools/tsukuroi-census.sh:3334-3432` |
| counter legs and marker strings | `8029cdba:tools/check-scrub-admission-r50.py:22-40, 96-113, 340-400` |

Facts I relied on and how they were checked (not re-derived beyond the read):

- `grep -c 'exclusive_operation\|replace_target'` over the frozen census → `0`. So "the census does
  not report replace state" is a read, not an inference.
- `grep -c '(R44-C1)'` over the frozen census → `16`. So "sixteen `(R44-C1)` cases" is exact.
- The SCRUB line is emitted by exactly one `printf` (`tools/tsukuroi-census.sh:3804`), built at
  `:2048-2050`; no second scrub-shaped line exists.
- Row hashes in the draft are the `FROZEN.md` values (`GR1 3a2ba180…fee1`, `GR2 a2e955ce…f3f`,
  `GR3 43430a14…c32c`). I did **not** recompute them: `--section-hash` is outside this seat's
  command set.

## Proposed text (exact; insert directly after the `## Scrub grounding — round 50 admission` line)

```markdown

Appended 2026-10-28 (round-50 C1; drafted by wave seat R50ScribeSkill, integrated by the L1). Base
`b866a1d3`; freeze `8029cdba`; row hashes GR1 `3a2ba1807a7f2308acb11b2f928f85dba5156c6eb9fe865216a06ba2a843fee1`,
GR2 `a2e955cefbd110ced928407c79b2cedb3cc431734487aa29e74682b23aeb7f3f`, GR3
`43430a14069598947d225c1f8ae897d9baea1c0e268cb88c2b5ad9e247bbc32c` (`.ufo/waves/round-50/frozen/FROZEN.md`).
Entry `corpus/knowledge/btrfs-scrub-grounding-r45.md`, rows GR1-GR3 on S246 (Linux v7.2.11 `lib/cmdline.c`,
`lib/vsprintf.c`, `lib/kstrtox.c`), S247 (`fs/btrfs/dev-replace.c`) and S248 (systemd v262
`man/systemd.kill.xml`), with S242 and S243 (`fs/btrfs/scrub.c`, `sysfs.c`), S240 (`fs/btrfs/ioctl.c`),
S237 (btrfs-progs `scrub.c`), S244 (the packaged units) and the own-work capture S249. A fresh counted
cohort of one wave (18 seats, three reviewers and three critics per row) read the three rows `holds` on
the frozen row bytes, after the four corrections the round-49 counted critic named (`R49CritGR2b`) landed
before the freeze: the `[inference]` mark narrowed to the btrfs-progs printing, S240 named in the
`source:` line and QUALITY item 7, the `dev-replace.c:1128` quote exact, and the S247/S240 range gaps
declared in Limits. Nothing here writes sysfs, starts, stops or enables a unit, runs a scrub or a replace,
or calls a privileged ioctl.

**What the three rows now pin.**

- **GR1 — the speed limit's parse.** A write to `devinfo/<devid>/scrub_speed_max` goes `memparse` →
  `simple_strtoull(…, 0)` → `_parse_integer_fixup_radix`: hexadecimal for a leading `0x` or `0X` with a hex
  digit after it, octal for any other leading `0`, decimal otherwise. At most one suffix `K`/`M`/`G`/`T`/`P`/`E`
  in either case, each step a further 1024, counted only when a digit came before it, with overflow to
  `ULLONG_MAX`; the store then skips whitespace and returns `-EINVAL` on any text left over. So `010` is 8,
  `0x10` is 16, `100M` and `100m` are both 104857600, `10MB`, `10 M` and `-1` are `EINVAL`, and a bare
  newline parses 0 and clears the limit.
- **GR2 — a replace copies through the scrub code, and what refuses a scrub start.** Both the replace start
  and the path that continues an interrupted replace call `btrfs_scrub_dev` on the source device's devid with
  `readonly` false and `is_dev_replace` true. Inside, after the filesystem-closing `-EAGAIN` and the
  context/worker allocations, three device checks answer first — unknown devid, or a missing device on a
  non-replace call, `-ENODEV`; a non-writeable device on a non-replace writing call, `-EROFS`; a device
  outside the filesystem metadata or the replace's own target, `-EIO` — and only then is a non-replace call
  refused `-EINPROGRESS` while `btrfs_dev_replace_is_ongoing` holds (valid replace data, state started or
  suspended, an unmount-suspended replace included), and any call refused while the device already carries a
  scrub context. Cancelling a started replace stops its scrub, and the suspended state calls
  `btrfs_scrub_cancel` too although the pinned code says the replace scrub is not running there; the progress
  query answers `-ENOTCONN` for a devid that exists without a context and `-ENODEV` for an unknown devid. The
  scrub-start ioctl returns the `btrfs_scrub_dev` value (S240 `ioctl.c:3093-3095`) unless the argument copy
  fails, when it returns `-EFAULT` (`ioctl.c:3109-3110`, `:3115`), and the progress ioctl gates on
  `CAP_SYS_ADMIN` (`ioctl.c:3132-3133`).
- **GR3 — what a stop sends.** The packaged unit sets `KillSignal=SIGINT` and no `KillMode=`, so the default
  `control-group` reaches every remaining process in the unit; SIGCONT follows that signal immediately, and
  the request repeats with SIGKILL once `TimeoutStopSec=` has passed unless `SendSIGKILL=no`. On this host the
  effective stop timeout is 5 s, from a `10-faster-shutdown.conf` drop-in no installed package owns, with
  `systemctl show` reporting `KillSignal=2 KillMode=control-group TimeoutStopUSec=5s FinalKillSignal=9
  SendSIGKILL=yes`. `-B` keeps the start in the foreground and installs its SIGINT handler on the mount's
  descriptor, so SIGINT reaches the handler that issues `BTRFS_IOC_SCRUB_CANCEL`.

| Observation | Reading | Action |
|---|---|---|
| `devinfo/<devid>/scrub_speed_max` reads a value the operator did not type (`010` reads 8, `100m` reads 104857600), or a write is refused `EINVAL` | the write is parsed by `memparse` with base 0 (GR1), so a leading zero is octal and each `K`/`M`/`G` step is 1024; 0 means no limit | read the attribute before blaming the device; setting it is root's and a mutation — the census only reports it (`limited=`) |
| a scrub start answers `EINPROGRESS` on a filesystem where no scrub was started, or a privileged `scrub status` shows the replace's source device as running | a device replace copies through the scrub code, so the source device carries a scrub context; and while a replace is started or suspended a non-replace scrub is refused `EINPROGRESS` (GR2) | read the unprivileged `exclusive_operation` and `replace_target` sysfs files first; starting or cancelling either operation stays operator-owned |
| `systemctl stop btrfs-scrub@<instance>.service` returns but the record shows no `canceled` mark, or counters look frozen | the stop sends SIGINT to the whole control group, then SIGCONT, and SIGKILL only if a process remains after the 5 s timeout (GR3); whether the start writes its canceled record in that window is not established | read the record's timestamps before treating the run as finished; `systemctl enable`/start/stop are operator action |

**The census lines that report this surface.** The arm prints one verdict-neutral
`SCRUB btrfs-scrub-record state=NONE|RECORDED|BLOCKED dir=absent|present|unreadable records=N tmp=N sockets=N
unreadable=N orphan=N limited=N timers=N [detail=…]` line after the STORAGE line and before the rollup
(contract: the `tools/tsukuroi-census.sh` header paragraph "Round-44 addition (C1)"; sixteen `(R44-C1)`
selftest cases pin it). GR1's limit is reported, never set: `limited=N` counts devices whose
`scrub_speed_max` reads a nonzero decimal, each listed in `detail` as `<fsid8>:<devid>:speed_max=<v>`, while a
value that is not exactly one decimal line is `speed-malformed` and a value the caller cannot read is
`speed-unreadable` — either makes the line `BLOCKED`, an unknown rather than an absence. The census does
**not** report replace state: it reads no `exclusive_operation` and no `replace_target`, so GR2's two
unprivileged reads are hand reads, not census fields. Record content is never read and no ioctl is called, so
the record's own state (GR3's `canceled` mark) and any running state stay outside the census; `sockets=N`
counts `scrub.progress.<fsid>` sockets by name and stat — never the socket's content — and a name of the
wrong type is `progress:not-socket`. The arm's known limit carries: an absent sysfs root with no record
reads `limited=0`, and the STORAGE line's mount-table guard is what flags a hidden sysfs.

Counter: `python3 tools/check-scrub-admission-r50.py --revision <REV>` — PASS iff `structural_ok == 1 and
corr_ok == 1 and quotes_ok == 3 and verdicts_ok == 3 and seats_ok == 18 and marks_ok == 3`. `structural_ok`
bounds each row from its `## GR<n>` heading to the next `## ` heading, one header, no inner heading; `corr_ok`
requires the round-48 and round-49 corrections in the bytes and the defect strings gone; `quotes_ok` resolves
every `**Quote.**` line on its digest-pinned snapshot at the cited line; `verdicts_ok` needs, per row, three
credited seats of the wave universe (at least one reviewer, one critic), pairwise distinct bodies, every
verdict `holds` and no bound-format negative anywhere; `seats_ok` needs each of the 18 expected seats to be
exactly one completed `w1-results.json` entry and one dispatch task with the declared role; `marks_ok` needs
the three admission marks. Pre-data controls:
`.ufo/waves/round-50/controls/battery-summary-r50-c1.jsonl`. The counter is a shape-and-quote gate, not a
forgery gate (the round-49 receipt `.ufo/waves/round-49/w1/R49CritCounter/`), so admission credit rests on the
orchestrator's real dispatch and results file, never on a hand-written report set.

Limits. Two consequences the pinned code does not decide stay `[inference]`: how `btrfs scrub start` and
`btrfs scrub status` print the `btrfs_scrub_dev` returns (GR2), and whether the start writes its canceled
record within the 5 s before SIGKILL (GR3) — a record without a `canceled` mark after a stop is therefore
possible. GR1's examples follow from the quoted code, not from a write on this host (the capture's caller is
uid 1000 with `CapEff` 0, and this host's devid 1 reads 0); GR3 pins systemd's documented order and the host's
effective values, not a trace of a stop, and nothing was started or stopped. Kernel behaviour is pinned at
Linux v7.2.11 lines (the Arch 7.2.11-arch1-1 patch touches no `fs/` file, carried from round 43; `lib/` not
re-checked), and the S247 and S240 declared ranges still do not list the lines GR2 cites
(`dev-replace.c:1111`, `:1126-1142`, `:1171-1195`, `:1184-1188`; `ioctl.c:3093-3095`, `:3109-3110`, `:3115`,
`:3190`) — declared in the entry's Limits, the snapshots digest-pinned whole-file. The verdicts are this
lane's seat verdicts, not outside review, and committed bytes cannot tell forged orchestrator records from
real ones.
```

## What this draft does and does not do

- **Does**: states what GR1/GR2/GR3 pin, at the entry's precision; names the two surviving `[inference]`
  marks in the words the frozen counter requires (`[inference]` on the btrfs-progs printing, the record after
  SIGKILL); names the operator-owned actions (setting `scrub_speed_max`, starting/cancelling a scrub or a
  replace, `systemctl enable`/start/stop, creating `/var/lib/btrfs`); names the census surface line and its
  fields, including the negative (no replace state in the census).
- **Does not**: add a proposition the entry does not carry (no new kernel, systemd or btrfs-progs claim; the
  `-EAGAIN`/`-ENODEV`/`-EROFS`/`-EIO` ordering, the cancel/suspend path, the 5 s timeout and the `-B` handler
  are all in the entry's GR rows); quote a line the entry does not quote; state a counter digest or a measured
  predicate value (not this seat's to measure — `--section-hash` and the counter run are outside the
  EXEC-AUTHORIZED command set); mention the C2 or C3 surfaces beyond the census's scrub arm.
- One house-style deviation to flag for the L1: every earlier scrub section opens with a **gate-status**
  sentence ("the depth gate FAILED", "pending"). This section is the admission, so that sentence is replaced
  by the cohort sentence in the opening paragraph. The precedent for an admitted-shaped section is the
  round-44 census-arm section (`8029cdba:SKILL.md:4184-4186`), which likewise opens with "Surface: …".

## Not run (declared)

- `python3 tools/check-scrub-admission-r50.py --revision 8029cdba…` — not run (not in this seat's command
  set, and the cohort has not settled; a FAIL now would measure the pre-admission state, not the draft).
- `--section-hash` — not run; the hashes in the draft are copied from `FROZEN.md`.
- No census `--selftest`, no fixture, no scratch dir. Free space under `/fast/scratch` was not needed and
  not measured.
