VERDICT: draft

# D-3 — `## Gate` "New SOURCES rows" (S237, S238, S239) for `corpus/lessons/round-42.md`

Inputs: rows as they stand at `f50c28d83e1832ecd7eba765caace531f45d6b27` (`git show
f50c28d8:corpus/SOURCES.md` lines 246-248), lesson placeholder `corpus/lessons/round-42.md:18`
(`<!-- GATE-ROWS -->`, working tree, untracked), format from `corpus/lessons/round-41.md:18-32`.
Lane HEAD when drafted: `87c4f7c6`; its `corpus/SOURCES.md` and
`corpus/knowledge/btrfs-scrub-record-r42.md` are byte-identical to `f50c28d8` (empty
`git diff --stat f50c28d8 HEAD` over both paths).

## Proposed text (exact Markdown; replaces `<!-- GATE-ROWS -->` at `corpus/lessons/round-42.md:18`)

| Row | URL (access 2026-10-26) | Located quote (≤25 words) | Location |
|---|---|---|---|
| S237 | https://github.com/kdave/btrfs-progs/blob/v7.1/cmds/scrub.c (tag v7.1, pinned raw `scrub.c`) | "/* write all-zero progress file for a start */" | `frozen/src/scrub.c:1502` |
| S238 | https://github.com/kdave/btrfs-progs/blob/v7.1/CHANGES (tag v7.1, pinned raw `CHANGES`) | "* scrub limit: new command to show or set the per-device scrub limits" | `frozen/src/CHANGES:468` |
| S239 | own-work capture `.ufo/waves/round-42/frozen/hostcap/` (`capture.sh`, run 2026-10-26T19:13:44Z, unprivileged) | "var_lib_btrfs absent"; "scrub_timer_unit_file btrfs-scrub@.timer disabled disabled"; "scrub_speed_max 1d02a454-c549-4a35-b567-89d60902af8e/devinfo/1 0"; "journal_scrub_lines 0" | `frozen/hostcap/capture.txt:6,8,9,10` |

Snapshot digests: `.ufo/waves/round-42/frozen/src/SHA256SUMS` (`scrub.c`
`48df2e2f468f…f0801`, `CHANGES` `bd881ab8…2a0d22`; both raw files re-fetched 2026-10-26 and
byte-identical with the pinned copies); fetch log `FETCH.txt` (tag v7.1 = `0a919c7d…`, peeled commit
`4ab0e80b…`, confirmed by `git ls-remote` 2026-10-26). Host capture: `capture.txt` sha256
`942edc91…643c` (the digest the S239 row pins), `capture.sh` sha256 `3ece27d0…077b`.

Rows touched old→new: S237-S239 only — `status` queued→mined and `used-by` —→
`corpus/knowledge/btrfs-scrub-record-r42.md`; `opened` (2026-10-26), `recheck` (`on-release` for
S237/S238, `30d` for S239) and every other row are unchanged (`git diff a84fc9de f50c28d8 --
corpus/SOURCES.md`: 3 insertions, 3 deletions, those three lines).

## Verification of each quote and location

`grep -n -F` run in `.../frozen/src` and `.../frozen/hostcap` (receipt
`w1/ScribeGate/gate-evidence.txt`):

| Row | `teaches` cell it must ground (`SOURCES.md:246-248` at f50c28d8) | `grep -n` hit | Tokens (whitespace) |
|---|---|---|---|
| S237 | "The status record is a userspace file the scrub start process writes and the status command reads; its format, its write discipline and the cases that leave no record" | `1502:		/* write all-zero progress file for a start */` | 9 |
| S238 | "The per-device scrub limit and its status report arrived in btrfs-progs 6.6.3" | `468:   * scrub limit: new command to show or set the per-device scrub limits` | 13 |
| S239 | "No /var/lib/btrfs directory, the scrub timer disabled, the root device limit 0 and no kernel scrub line in the current boot" | `6:var_lib_btrfs absent`, `8:scrub_timer_unit_file btrfs-scrub@.timer disabled disabled`, `9:scrub_speed_max 1d02a454-…/devinfo/1 0`, `10:journal_scrub_lines 0` | 11 |

Supporting lines, verified but deliberately not in the quote cell: `scrub.c:67`
`#define SCRUB_DATA_FILE "/var/lib/btrfs/scrub.status"`, `:487` `ret = flock(fd, LOCK_EX|LOCK_NB);`,
`:534` `ret = rename(datafile_old, datafile_new);` (all quoted in the entry's SC1); `CHANGES:460`
`btrfs-progs-6.6.3 (2023-12-14)` (the section header that carries the `:468` line and the
status-report line `:467` `* scrub status: report limit if set in sysfs/../scrub_speed_max`).

Digest and provenance checks (same receipt): `sha256sum` of the frozen copies reproduces
`SHA256SUMS` exactly (`48df2e2f…f0801` scrub.c, `bd881ab8…2a0d22` CHANGES); a fresh `curl -sSfL` of
both `raw.githubusercontent.com/.../v7.1/...` URLs on 2026-10-26 produced byte-identical files
(`cmp` clean); both HTML URLs and both raw URLs answered 200; `git ls-remote` returned
`0a919c7d… refs/tags/v7.1` and `4ab0e80b… refs/tags/v7.1^{}`.

## Rows-touched evidence

- old (`a84fc9de`): `| S237 … | queued | 2026-10-26 | on-release | — |`; S238 same shape; S239
  `| queued | 2026-10-26 | 30d | — |`.
- new (`f50c28d8`): all three `| mined | 2026-10-26 | <same recheck> | corpus/knowledge/btrfs-scrub-record-r42.md |`.
- `git diff --numstat a84fc9de f50c28d8 -- corpus/SOURCES.md` → `3	3	corpus/SOURCES.md`; the diff has
  exactly six `^[-+]|` lines (three removed, three added). Entry commit message: "S237-S239 queued ->
  mined, used-by the entry" (`git log -1 --oneline f50c28d8`).

## Findings and limits

1. **S239 location is `frozen/hostcap/`, not `frozen/src/`** — the row's source is the own-work
   capture, and `frozen/src/` holds only `scrub.c`, `CHANGES`, `SHA256SUMS`, `FETCH.txt`. The item's
   literal `frozen/src/<file>:<line>` cannot apply to S239; I followed the round-41 precedent for its
   own-work row S236 (`corpus/lessons/round-41.md:29`: two `frozen/hostcap/...` locations) and verified
   the lines with `grep -n` in `frozen/hostcap/`.
2. **Row-cell imprecision (source row, not my draft):** the S239 anchor cell reads "capture.sh and
   capture.txt (sha256 942edc…)" — one digest cannot cover two files; `942edc91…643c` is
   `capture.txt`'s (`sha256sum` above), and no manifest covers the pair (`ls` shows only the two
   files). My URL cell binds `capture.sh`'s own digest (`3ece27d0…077b`) in the digests sentence.
   The L1 may want to split the row's parenthetical the same way.
3. **Single-quote choice for S237:** `:1502` grounds the writer ("the scrub start process writes"),
   which is the triage pivot (a missing record does not prove no scrub ran, entry SC3); the file
   identity (`:67`) and write discipline (`:487`, `:534`) are quoted in SC1 and listed in the
   supporting-lines sentence rather than crammed into one cell. A merged two-fragment quote would also
   fit the 25-word budget if the L1 prefers it (`"/* write all-zero progress file for a start */";
   "ret = flock(fd, LOCK_EX|LOCK_NB);"` = 13 whitespace tokens).
4. **S238 covers one half per cell:** `:468` grounds the per-device limit; the "status report" half is
   `:467` and the "6.6.3" half is the header `:460`, both verified and named in the supporting
   sentence. `CHANGES` lines 467-468 sit inside the 6.6.3 entry, so the cell is not misattributed.
5. **Not run (and why):** the census, the census selftest, and both frozen counters — D-3 needs no
   counter verdict, and the C2 counter's conjunct counts only wave-2 `C2RevSC*`/`C2CritSC*` seats, so
   running it now would add no evidence. I did not re-open the ArchWiki/man pages; the two pinned
   upstream URLs were re-fetched (above).
6. **No writes outside my seat paths:** commands were read-only (`git show/diff/log/rev-parse/
   ls-remote`, `grep`, `sha256sum`, `curl`), no git/jj mutation, no sudo, no pacman, no service, no
   sysfs/mount change, no `btrfs scrub` verb. Scratch
   `/fast/scratch/hyaku/tsukuroi-r42/ScribeGate/` was removed after the receipts were copied. No tool
   installed or upgraded.

## Artifacts

- Report: `.ufo/waves/round-42/w1/ScribeGate.md` (this file).
- Receipts: `.ufo/waves/round-42/w1/ScribeGate/gate-evidence.txt` (all `grep -n`, `sha256sum`, re-fetch
  `cmp`, `ls-remote`, HTTP codes, old/new row cells, diff stats), `digests.txt`, `ls-remote.txt`,
  `http-check.txt`.
