VERDICT: defect-found

Seat C2CritNovelty, item C2-9 (round 42 / hyaku run 9, wave 1), milestone "depth or restatement".
Read-only on lane content. Scratch `/fast/scratch/hyaku/tsukuroi-r42/C2CritNovelty/` (removed after the receipts
were copied). Bytes under test: `corpus/knowledge/btrfs-scrub-record-r42.md` at HEAD `87c4f7c6` (sha256
`9038ea7a4b8d8c6ac88f7feca3dfdbfc8c7822faa6ce0c0f8207c7eed077ca36`; unchanged since the entry commit `f50c28d8`,
`git diff --quiet f50c28d8 HEAD -- <entry> corpus/SOURCES.md` empty), counter `tools/check-scrub-record-r42.py`
sha256 `dbe933ec8c2cca491346da76bbc104aba8ff9e5486f4dcaf572e59df3680503f`, matching the declaration.
Comparison ground: base `c8efaa3f`. `corpus/knowledge/storage-health-r26.md`, `SKILL.md`, `corpus/README.md`,
`PROVINCE.md` and `storage-health-r26.json` are all **identical base..HEAD** (`git diff --quiet c8efaa3f HEAD -- <f>`
rc 0 for each), so every base line below is also its HEAD line.
Receipts: `.ufo/waves/round-42/w1/C2CritNovelty/{novelty-tokens.txt,quotes.txt,base-ground.txt,gate-and-preamble.txt}`.

**Answer in one line:** C2 is depth — five rows of file/line-bound upstream mechanism, 28/28 quotes resolving at
their cited lines in the digest-pinned snapshots, all five frozen tokens absent at the base — but the entry's
**novelty accounting is over-broad in one clause**, **SC3's triage conclusion is a restatement of ground the base
already held**, and that restatement arrives wearing a **fifth verdict token outside the lane's frozen
`verdict_vocabulary`**. The row *count* is honest (no padded row, no row that is a pure restatement).

## 1. Per-row novelty against the base (the item's table)

Legend: **new** = proposition absent from base-held text; **partly held** = some conjunct already stated at the
base; **restated** = no new proposition. "Base ground" cites `corpus/knowledge/storage-health-r26.md` (=SH3/SH4 at
`c8efaa3f`), `SKILL.md` and the frozen tokens' own base-absence check (`novelty-tokens.txt`).

| Row | Frozen token, base hits | Base ground that already says part of it | Novelty verdict |
|---|---|---|---|
| SC1 (entry:18) | `LOCK_EX` 0 | `r26.md:57` "btrfs-progs keeps scrub.status.<UUID> files"; `r26.md:65` S139 line 71 quote "textual files named"; `SKILL.md:2368` "No `scrub.status.<UUID>` under `/var/lib/btrfs`" | **partly held** — the *name* is held; `_tmp`-then-`rename`, mode 0600, `LOCK_EX|LOCK_NB` on every open (incl. the read open, `scrub_open_file_r` → `scrub_open_file` at `scrub.c:497-505`) are new and quote-bound |
| SC2 (entry:41) | `scrub status:1` 0 | `r26.md:63` already names "csum, verify, read and super errors and the corrected versus uncorrectable split"; `r26.md:65` "textual files" | **new** — first-line version prefix, the `<fsid>:<devid>` + `|key:value` line shape, the exact 14+5 field order (`scrub.c:856-890`, verified) and the "per-device, not one filesystem verdict" reading are all absent at base |
| SC3 (entry:63) | `status recording disabled` 0 | `r26.md:133` "older scrubs, or scrubs run with **recording disabled**, cannot be excluded" **and** the same line's closing "SKILL SE4's 'no scrub has run' means no scrub status is recorded"; `SKILL.md:2368` "mean no scrub record, not a clean scrub" | **partly held** — the conclusion ("no record ≠ no scrub ran") is *restated*, twice over, at base; new is the mechanism: the writer is the userspace `scrub start` process, the all-zero write at start, the two disable conditions and their exact warning (`scrub.c:1502-1510`, `1330-1338`), and the kernel ioctl being independent of the file (`scrub.c:1190-1205`) |
| SC4 (entry:87) | `_SCRUB_FS_STAT_MIN` 0 | `r26.md:59`/`SKILL.md:2368` "`no stats available` mean no scrub record"; `r26.md:133` "no scrub status is recorded" | **partly held** — "missing record = no history" is held; new is the fold (`_SCRUB_FS_STAT_ZMIN` t_start/t_resumed, `_SCRUB_FS_STAT_ZMAX` canceled/duration, `_SCRUB_FS_STAT_MIN` finished with `init_fs_stat` seeding 1, `scrub.c:283-312`), the `running→aborted→finished→interrupted` status word (`scrub.c:341-343`), and ENOENT-vs-other open failure (`scrub.c:1931`) |
| SC5 (entry:116) | `scrub_speed_max` 0 | none | **new** — whole proposition (sysfs path, 0 = no limit, three consumers, 6.6.3 arrival, unreadable-reads-as-0). Verified against `scrub.c:1208-1222` and `CHANGES:467-469` |

Recap for the wave-2 seats and the integrator: **SC1 partly held · SC2 new · SC3 partly held · SC4 partly held ·
SC5 new · zero rows restated**. Three of five rows carry a held clause, so the honest label for the entry is "two
wholly new propositions (SC2, SC5), three rows that extend ground the base already stated (SC1, SC3, SC4)", not
"five wholly new rows".

Token check run exactly as the item prescribes, e.g.
`git -C <lane> grep -c -F -- 'LOCK_EX' c8efaa3f… -- corpus/knowledge SKILL.md` → no output, rc 1; same rc 1 for
the other four (`novelty-tokens.txt`). Tip counts are 2/1/3/2/5 hits, all inside the new entry — so the tokens are
honest shape gates.

## 2. Counterexample to the entry's novelty framing (the defect)

The entry's scope paragraph, `btrfs-scrub-record-r42.md:8-10`, contradicts itself in adjacent sentences:

> The lane already holds what scrub verifies and repairs **and that `btrfs scrub status` reads a file under
> `/var/lib/btrfs`** (… SH3, SH4; S129, S139). It held no statement of the record itself: **how the file is
> named** and replaced, its line format, …

The base does not merely hold "a file under `/var/lib/btrfs`": it holds the **name formula**.
`r26.md:57` (base = HEAD) says "btrfs-progs keeps **scrub.status.\<UUID\>** files"; `r26.md:65` already quotes S139
line 71 "…in textual files **named**"; `SKILL.md:2368` says "No **`scrub.status.<UUID>`** under `/var/lib/btrfs`".
So "how the file is named" is held ground, and SC1's naming clause (entry:18, "the base path plus a dot plus the
filesystem UUID") is a restatement of it. What is new in SC1 is the *replacement* (`_tmp` + `rename`,
`scrub.c:466-475`, `917`, `925`, `534`), the mode and the lock (`scrub.c:483-491`) — the sentence's own second
half.

This matters because the counter cannot see it: the novelty gate is one token per row
(`check-scrub-record-r42.py:55-61` sets `'SC1': {'token': 'LOCK_EX', …}`, `:206` `n_ok = spec['token'] in text`,
`:167-171` sums base hits over `corpus/knowledge` + `SKILL.md`). `LOCK_EX` is genuinely new, so `novelty_ok` for SC1
is 1 even though one of its two sentences is held ground. QUALITY 87 in the entry concedes the gates are "shape
gates only" — which is exactly why the *prose* novelty claim must be exact, and here it is not.

Strongest available counterexample, same shape: **SC3**. Its frozen token is `status recording disabled` (new:
0 base hits), but its conclusion — "a scrub whose recording was disabled … leaves none", entry:67-68 — is stated at
base `r26.md:133` ("older scrubs, or scrubs run with recording disabled, cannot be excluded") and again in that
line's closing sentence ("SKILL SE4's 'no scrub has run' means no scrub status is recorded"). Token novelty 1,
proposition novelty 0 for the row's last sentence. The row is still depth — its three mechanism quotes are real and
new — but one third of the row is restatement presented as new.

**Impacted axes:** depth (not reduced — the mechanism is quote-bound and verified), novelty accounting (over-broad
by one clause and one row's conclusion), identity (see §3).

## 3. The restated conclusion arrives as a new verdict token (`UNRECORDED`)

`btrfs-scrub-record-r42.md:136` reads the state as `` `UNRECORDED` `` and then, in the same sentence, says "the
lane's SH4 verdict `UNVERIFIED` for stored data stands". Two labels now name one state. The lane's authority for
that state is a frozen vocabulary, not a new word:

- `corpus/knowledge/storage-health-r26.json` `verdict_vocabulary` has exactly four tokens — `HEALTHY`, `DEGRADED`,
  `BLOCKED`, `UNVERIFIED` ("the evidence needed to judge this signal does not exist on the host").
- `SKILL.md:2419` binds the storage verdicts to that object: "The entry's `UNVERIFIED` verdict and its `DEGRADED`
  meaning are defined in `corpus/knowledge/storage-health-r26.json` (`verdict_vocabulary`)".
- `corpus/README.md:239` registers SH4 as "no scrub record exists on this host (`UNVERIFIED`)".
- `UNRECORDED` has **1** occurrence in the lane, the entry line above; base grep rc 1.

The state itself ("evidence absent, not a clean reading") is byte-for-byte what `UNVERIFIED` already means, so
`UNRECORDED` is a rename of held ground rather than a new distinction. Under the `verdict_vocabulary` definition,
"no record exists" *is* "the evidence needed to judge this signal does not exist on the host" — no fifth token is
earned. Smallest safe correction: keep SH4's token and drop the new one (§5, C2).

## 4. Inference is not separated from observation (lane rule, `SKILL.md:17`)

`SKILL.md:17`: "Every claim: measured anchor (path:line, command output, evidence id). Observation / inference /
unknown stay separate." The entry carries **zero** `[inference]` tags (`grep -n 'inference' <entry>` rc 1), while
the neighbouring knowledge entries use them (`storage-health-r26.md:121-122`; `degraded-triage-r4.md:122,171,202`
which pairs `[observed]` with `[inference]`; `pacman-exec-environment-r40.md:63`; `host-health-report-r3.md:128,
278,456`). Two of its sentences are inferences from code shape, not from a quoted line:

1. entry:67-68 "or one driven by another tool through the ioctl, leaves none" — no quoted line says the record is
   written *only* by this CLI; it follows from the write path being solely `scrub_write_progress` (called at
   `scrub.c:1123`, `1503`, `1702`). Plausible, unquoted.
2. entry:92-94 "An `interrupted` status therefore means an unfinished record with nothing running now (for example a
   start process that ended before the scrub did)" — the parenthetical cause is a story about a process exit; the
   quotes support only the predicate (`finished` from the record, `in_progress` from the ioctl).

Both are correct-looking and both belong in the entry; they need the tag the lane uses, not deletion.

## 5. Row-set sizing, and the exact proposed text

**Sizing is honest in count.** Five rows, five distinct questions (name/replacement · format · writer and
recording-off · reader fold and status word · throughput limit), no row is a subset of another and no row is pure
restatement (SC5 is wholly new; SC2/SC4 majority new). Nothing is padded to reach five. One caveat on framing:
SC5's object is the per-device sysfs limit, not the record, and the scope paragraph (entry:9-12) enumerates only
four items, none of which SC5 answers; `PROVINCE.md:212` names the Frontier object as "the scrub record (`btrfs
scrub status`, `/var/lib/btrfs/scrub.status.*`, `btrfs-scrub@.timer`)". SC5 is defensible because it is what the
status command *reports*, but the paragraph should say so rather than leave a fifth row outside its own list.

Proposed text (exact replacements; all are prose inside existing paragraphs — no quote line, no frozen token, no
row count and no counter window is touched, so `rows == 5 and quotes_ok == 5 and novelty_ok == 5 … and
novelty_base_hits == 0` is unaffected):

**C1 — entry:9-10, the false clause.** Replace
`It held no statement of the record`
`itself: how the file is named and replaced, its line format, which process writes it and when recording is`
`switched off, and how the status command turns per-device lines into one filesystem verdict.`
with
`It held the record's name pattern (SH4, and S139's "textual files named") but no statement of the record`
`itself: how the file is replaced, its line format, which process writes it and when recording is switched off, how`
`the status command turns per-device lines into one filesystem verdict, and the per-device throughput limit that`
`same command reports (SC5).`

**C2 — entry:136-137, the verdict token.** Replace
`- Read "no scrub record" as `UNRECORDED`, not `NEVER SCRUBBED` (SC3); the lane's SH4 verdict `UNVERIFIED` for stored`
`  data stands.`
with
`- Read "no scrub record" as a gap in evidence (`UNVERIFIED`, SH4), not as `NEVER SCRUBBED` (SC3): a`
`  recording-disabled scrub is already unexcluded at the base (`storage-health-r26.md:133`), and what SC3 adds is`
`  the mechanism, not the verdict; SH4's `UNVERIFIED` for stored data stands.`

**C3 — entry:66-68, mark what SC3 restates.** After
`scrub ran: a scrub whose recording was disabled, or one driven by another tool through the ioctl, leaves none.`
insert
`The conclusion was already held (SH4's note, `storage-health-r26.md:133`); new here is the mechanism and the two`
`disable conditions, and the "another tool" clause is `[inference]` from the write path.`

**C4 — entry:67-68 inference tag (if C3 is not taken verbatim):** append `[inference]` to the "one driven by
another tool through the ioctl" clause.

**C5 — entry:92-94 inference tag.** In the line `that ended before the scrub did), not a device error.` insert the
tag after the closing parenthesis, i.e. the line becomes
`that ended before the scrub did) [inference], not a device error.`

**C6 — entry:18-19, mark SC1's held clause (optional, belt-and-braces for C1).** After
`(the base path plus a dot plus the filesystem UUID)`
insert
` — the name pattern is already held (SH4, `storage-health-r26.md:57`) —`

## 6. Evidence index

| Claim | Command / path | Observed |
|---|---|---|
| all 28 quotes resolve at their cited lines in the pinned snapshots | `python3 qcheck.py` over `.ufo/waves/round-42/frozen/src/{scrub.c,CHANGES}` | `quotes good=28 bad=0` (`quotes.txt`) |
| the five frozen tokens are absent at the base | `git -C <lane> grep -c -F -- '<token>' c8efaa3f… -- corpus/knowledge SKILL.md` ×5 | rc 1, no output, for all five (`novelty-tokens.txt`) |
| snapshots are the declared bytes | `sha256sum` vs `frozen/src/SHA256SUMS`, capture vs declaration | `48df2e2f…` scrub.c, `bd881ab8…` CHANGES, `942edc91…` capture.txt — all match |
| the base holds the record's name | `git show c8efaa3f:corpus/knowledge/storage-health-r26.md` :57, :65; `SKILL.md:2368` | `base-ground.txt` §SH4 statement / Sources / SKILL row |
| the base holds SC3's conclusion | same file :133 | "older scrubs, or scrubs run with recording disabled, cannot be excluded" … "SKILL SE4's 'no scrub has run' means no scrub status is recorded" |
| four-token verdict vocabulary | `python3 -c` over `storage-health-r26.json` | `HEALTHY, DEGRADED, BLOCKED, UNVERIFIED` |
| `UNRECORDED` is new and unregistered | `git grep -n -F UNRECORDED HEAD`; base grep | 1 hit, entry:136; base rc 1 |
| novelty gate is per-row single-token | `tools/check-scrub-record-r42.py:55-61,167-171,206` | `gate-and-preamble.txt` |
| SC2 field order matches the writer | `frozen/src/scrub.c:856-890` | 14 `_SCRUB_KVWRITE` counters then 5 `_SCRUB_KVWRITE_STATS` in the stated order |
| SC4 fold matches the reader | `frozen/src/scrub.c:282-312,341-343,1931` | ZMIN t_start/t_resumed, ZMAX canceled, MIN finished, `init_fs_stat` seeds 1, ENOENT exempt |
| SC5 limit read swallows failure | `frozen/src/scrub.c:1213-1220`; `CHANGES:467-469` | `if (ret < 0) limit = 0;`; 6.6.3 entries for status, limit, start |
| SC1 read open also takes the exclusive lock | `frozen/src/scrub.c:497-505` | `scrub_open_file_r` → `scrub_open_file(datafile, O_RDONLY)` → `flock(fd, LOCK_EX|LOCK_NB)` |

Minor, outside my item but visible while checking: SC5's "scrub start … report[s] a set limit" rests on
`CHANGES:469` ("* scrub start: report the limit if set"), which is inside SC5's frozen CHANGES window 460-470 but is
not quoted; adding `S238 CHANGES:469` to SC5's quotes would bind that clause without changing the window.

## 7. What I did not do

- I did not run `tools/check-scrub-record-r42.py`: its predicate needs the wave-2 `C2RevSC<n>`/`C2CritSC<n>`
  verdicts, which do not exist yet, and other seats hold the host for counter runs. I reproduced its novelty leg
  exactly (same `git grep -c -F … BASE -- corpus/knowledge SKILL.md` command, `novelty-tokens.txt`).
- I did not judge quote-window adequacy or the host readings beyond confirming digests and that every host line
  number exists and is non-blank in `capture.txt`; those are the reviewer seats' items.
- I did not read the Arch packaging patches against `cmds/scrub.c` (the entry's own wave item), and I ran no scrub,
  wrote nothing under `/var/lib/btrfs`, and touched no lane file.
