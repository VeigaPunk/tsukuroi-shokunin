ROW GR2 VERDICT: holds
SECTION SHA256: d4296085a574e29296fb9baba5a8722766a832a0b15809ccee72ea019ebd027f
Seat R49RevGR2c (reviewer). Row read only at `55c07cd3f8bff2e12117c34d57b4c618de74d85c`, extracted once with
`git -C …/tsukuroi-shokunin show <FREEZE>:corpus/knowledge/btrfs-scrub-grounding-r45.md`; I did not write it.

**Hash.** `python3 tools/check-scrub-admission-r49.py --revision 55c07cd3… --section-hash` printed
`GR2 d4296085…27f` (`problems: []`). I re-derived it in Python: lines 56–151 of the extracted file (from `## GR2`
up to, excluding, `## GR3`), joined with LF, **no trailing LF** =
`d4296085a574e29296fb9baba5a8722766a832a0b15809ccee72ea019ebd027f`. With a trailing LF the digest would be
`72d6f2b89055b8844380885780306dd54fd8401165a86dd2a0b10ed6b3327f25`, so the no-trailing-LF convention is the one
the counter uses; it matches.

**Pinned snapshots.** `sha256sum -c SHA256SUMS` in each `frozen/src` dir: round-45 `dev-replace.c` OK
(`f07ef0a0…` = S247), round-44 `scrub.c` OK (`f347931b…` = S242), round-44 `sysfs.c` OK (`ce146120…` = S243),
round-43 `ioctl.c` OK (`7b3488f2…` = S240). Round-45 `FETCH.txt` shows all four come from tag `v7.2.11` (peeled
`a2de78ee…`), so the row's "In Linux v7.2.11" is grounded. `hostcap/capture.txt` sha256 = `f5958a83…`, the digest
the row's front matter names (S249).

**Quotes.** A script parsed all 29 `**Quote.**` lines of the section and required each quoted text to be a substring
of the cited line of the cited snapshot: 29 checked, 0 mismatches (including `dev-replace.c:701`, `:703`, `:1128`,
`:1143`, `:1144`, `:1235`, `:1259`, `:1265`, `:1268`, `:1287`; `scrub.c:3081`, `:3094`, `:3095`, `:3109`, `:3114`,
`:3123`, `:3133`, `:3138`, `:3139`, `:3142`, `:3147`, `:3148`, `:3149`, `:3153`, `:3222`, `:3336`; `sysfs.c:1288`,
`:2015`).

**Clauses verified against the bytes.** (1) Both callers pass the source devid and `false, true` as the last two
parameters of the 7-parameter signature (`scrub.c:3079-3081`): start at `dev-replace.c:701-703` inside
`btrfs_dev_replace_start` (`:587`) under the reuse comment at `:700`; resume at `:1265-1268` inside
`btrfs_dev_replace_kthread` (`:1249`). (2) Inside `btrfs_scrub_dev` the stated order and errnos are exact:
`-EAGAIN` on `btrfs_fs_closing` (`scrub.c:3094-3095`), `scrub_setup_ctx` error returns directly (`:3109-3111`),
`scrub_workers_get` error goes to `out_free_ctx` (`:3114-3116`), then `-ENODEV` for `!dev || (MISSING &&
!is_dev_replace)` (`:3120-3123`), `-EROFS` for `!is_dev_replace && !readonly && !WRITEABLE` (`:3127-3133`), `-EIO`
for `!IN_FS_METADATA || REPLACE_TGT` (`:3138-3142`), only then `-EINPROGRESS` for `dev->scrub_ctx ||
(!is_dev_replace && is_ongoing)` (`:3146-3153`). (3) `btrfs_dev_replace_is_ongoing` requires `is_valid` first
(`dev-replace.c:1278-1279`; 0 on absent/bad item at `:120`, 1 after a good item at `:150`) and is true only for
STARTED/SUSPENDED (`:1286-1287`, comment `:1288-1297`) — the row states both gates. (4) Both `btrfs_scrub_cancel`
calls sit in `btrfs_dev_replace_cancel` (`:1085-1169`): STARTED at `:1111`, SUSPENDED at `:1144` after the "scrub
doing the replace isn't running" comment `:1127-1129` and the "must not be running" comment `:1143`; the row
attributes both to that one function and flags the comment's claim. (5) The unmount-suspend extent `:1171-1195` is
exactly `btrfs_dev_replace_suspend_for_unmount`, not one line past (`:1195` is its closing brace, `:1197` the next
function's comment); its only acting case is STARTED (`:1184-1186`) setting `time_stopped` (`:1187`) and
`item_needs_writeback` (`:1188`), and it contains no `btrfs_scrub_cancel` (grep: only `:1111`, `:1144`). (6) Context
attached at `scrub.c:3159`, cleared at `:3222`; progress query `dev ? (sctx ? 0 : -ENOTCONN) : -ENODEV`
(`:3321-3336`). (7) "no scrub is started": every EINPROGRESS path goes to `out` (`:3153-3154` → `:3248-3253`),
before `scrub_enumerate_chunks` (`:3208`) and before `atomic_inc(scrubs_running)` (`:3167`). (8) The scrub-start
ioctl does reach that code with `is_dev_replace` false (`ioctl.c:3093-3095`), so the conclusion's subject exists;
its "present, writeable, in metadata, not the target" qualifier is exactly the set that clears the earlier refusals,
and the qualifier is conservative, not overreaching. (9) Host reading: `capture.txt:9` `devids=1`, `:1`
`CapEff=0000000000000000`, `:2` kernel 7.2.11; the progress ioctl's `CAP_SYS_ADMIN` gate is `ioctl.c:3132` with
`-EPERM` at `:3133`; `exclusive_operation` prints `device replace` for `BTRFS_EXCLOP_DEV_REPLACE`
(`sysfs.c:1287-1288`, registered `:1302`) and is 0444 (`BTRFS_ATTR`, `:76-78`), `replace_target` is
`!!test_bit(REPLACE_TGT)` (`:2015`, registered `:2019`, same 0444 macro); the exclusive op is taken at the resume
path (`dev-replace.c:1235`) and around the ioctl start (`ioctl.c:3190`, finished `:3194`). The `[inference]` mark
covers exactly what no pinned file decides (ioctl hand-through and btrfs-progs printing); the sysfs readability
claim is not left unmarked as inference because the row cites the observed mode-444 reading in
`.ufo/waves/round-45/a2w1/C2ExecHostRecheck.md` §3, which I opened and found to contain those reads.

**Universal words.** "only" (the unmount path) is exact — the switch's other four cases just `break`
(`:1179-1183`). "any call" for the `dev->scrub_ctx` refusal is exact — that disjunct is not guarded by
`is_dev_replace` (`:3147`). "no scrub is started" is exact per (7) above.

**Defects.** None found. Every clause resolves to pinned lines; no range runs into a following function; no quote
is misplaced. Two non-defect observations (neither changes a truth value, so neither makes this `partly`): the
-ENOTCONN sentence calls the scrub context "the replace context", which is loose wording for the same field
(`scrub.c:3331/3336`), and it cites `scrub.c:3222` (the clear) alongside `:3336` (the return), which supports but
does not decide that sentence; the `SR7` token the row leans on resolves outside the row, at
`corpus/knowledge/btrfs-scrub-record-r44.md:15` (§SR7, which says a replace runs through the same
`btrfs_scrub_dev`) and is introduced at entry line 10.

**Verified but not re-derived.** The round-48 counted defects (R48CritGR2a 1–3, R48RevGR2a 1–4) are all in the
bytes as recommended — `is_valid` gate, rewritten cancel sentence citing both branches, range `1171-1195` with
`time_stopped`/writeback, `ioctl.c:3132` citation, `-ENOTCONN` narrowed to an existing devid with `-ENODEV`
separate — but I judged each clause against source, not against those reports. The host's live sysfs mode and
`none`/`0` values I read from the C2ExecHostRecheck receipt, not by re-running the reads.

**What I did not do.** No counter run except `--section-hash` (no `--selftest`, so no C1 predicate was measured by
me); no scrub, replace, privilege, sysfs write or unit action; no upstream re-fetch (digests only); no build/lint.
Scratch `/fast/scratch/hyaku/tsukuroi-r49/R49RevGR2c/` removed after writing this file.
