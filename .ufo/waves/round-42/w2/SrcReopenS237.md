VERDICT: supports
# F-11 — re-open S237 (btrfs-progs v7.1 cmds/scrub.c)

Seat SrcReopenS237, tsukuroi round 42 wave w2 (falsify). Row under review: `corpus/SOURCES.md:246` at `78abb8b5cdc9da511b4fc523e661517a68dd33d3` (row byte-identical in the worktree; verified by `diff` of `sed -n '246p'` pinned vs worktree). All commands run 2026-10-26 from scratch `/fast/scratch/hyaku/tsukuroi-r42/SrcReopenS237`, removed after receipts were copied to `.ufo/waves/round-42/w2/SrcReopenS237/`. No tools installed or upgraded (none needed).

## 1. Fetch and sha256 vs the row anchor — reproduces
- `curl -fsSL https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/cmds/scrub.c` (2026-10-26) → sha256 `48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801`, 2231 lines, 57034 bytes (`sha256sum`, `wc -l -c`).
- Anchor cell (`SOURCES.md:246`): "raw bytes sha256 48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801" — exact match.
- `git ls-remote https://github.com/kdave/btrfs-progs "refs/tags/v7.1" "refs/tags/v7.1^{}"` → tag `0a919c7d6e389c07920675b7fad3f793b92aa78b`, peeled `4ab0e80be9e3bb1db2e6038e6d4316d35fb7ba8b` — matches the anchor's "tag v7.1 (peeled commit 4ab0e80be9e3bb1db2e6038e6d4316d35fb7ba8b)" and `frozen/src/FETCH.txt`.
- Bytes-at-commit identity: `git hash-object` of the fetched bytes = `2b256f9d08b074a8b9593a3081842d4442b967fb` = GitHub API blob sha for `cmds/scrub.c?ref=4ab0e80b…` (size 57034). The raw tag URL serves exactly the pinned peeled-commit content, so no tag-move drift is possible for this row.
- Lane frozen copy agrees: `.ufo/waves/round-42/frozen/src/scrub.c` sha256 = `48df2e2f…f0801`, equal to its `SHA256SUMS` line and to today's live fetch (receipts R1, R4).

## 2. Cited line ranges — all exist, content maps to the scope
Ranges claimed: 67-70, 280-330, 446-535, 826-895, 1110-1125, 1186-1220, 1330-1340, 1498-1512, 1925-1945. File has 2231 lines; every start ≤ end ≤ 2231; every range dumped with `nl -ba | sed -n` and read. Mapping:
- **67-70** names the record: `#define SCRUB_DATA_FILE "/var/lib/btrfs/scrub.status"` (67), `SCRUB_FILE_VERSION_PREFIX "scrub status"` (69), `SCRUB_FILE_VERSION "1"` (70).
- **280-330** stats aggregation and status print: `add_to_fs_stat` (282-305), `_print_scrub_ss` (313-330+).
- **446-535** name construction, lock, read/write open, atomic rename: `scrub_datafile` (446-476), `flock(fd, LOCK_EX|LOCK_NB)` (487), `scrub_open_file_r` (497-506), `scrub_open_file_w` (508-518), `scrub_rename_file` (520-536).
- **826-895** record write and wire format: `scrub_kvwrite` `|%s:%lld` (840), version header write (856-859), per-device key list (863-892).
- **1110-1125** recording gate in the background thread: `if (!spc->do_record)` / `continue;` (1121-1122).
- **1186-1220** kernel-running check and rate limit: `BTRFS_IOC_SCRUB_PROGRESS` ioctl (1200), `devinfo/%llu/scrub_speed_max` (1215).
- **1330-1340** disable on mkdir failure: warning "…status recording disabled" (1336), `do_record = false;` (1338).
- **1498-1512** disable on first write failure: `if (do_record)` → warning (1507), `do_record = false;` (1508).
- **1925-1945** status command reads the record: `scrub_open_file_r(SCRUB_DATA_FILE, fsid)` (1930), ENOENT tolerated (1931), `scrub_read_file(fdres, 1)` (1940).

## 3. `teaches` cell grounded — yes
teaches: "The status record is a userspace file the scrub start process writes and the status command reads; its format, its write discipline and the cases that leave no record."
- userspace file, named — `scrub.c:67`: `#define SCRUB_DATA_FILE "/var/lib/btrfs/scrub.status"`
- start writes it — `scrub.c:917`: `fd = scrub_open_file_w(SCRUB_DATA_FILE, fsid, "tmp");` then `scrub.c:925`: `err = scrub_rename_file(SCRUB_DATA_FILE, fsid, "tmp");`
- status reads it — `scrub.c:1930`: `fdres = scrub_open_file_r(SCRUB_DATA_FILE, fsid);` → `scrub.c:1940`: `past_scrubs = scrub_read_file(fdres, 1);`
- format — `scrub.c:840`: `return scrub_writev(fd, buf, max, "|%s:%lld", key, val);`; header `scrub.c:856`: `ret = scrub_write_buf(fd, SCRUB_FILE_VERSION_PREFIX ":"`
- write discipline — `scrub.c:487`: `ret = flock(fd, LOCK_EX|LOCK_NB);`; tmp-then-rename (917/925); gate `scrub.c:1121`: `if (!spc->do_record)`
- cases that leave no record — `scrub.c:1336`: `warning("cannot create scrub data file, mkdir %s failed: %m, status recording disabled",` → `do_record = false;` (1338); `scrub.c:1507`: `warning("failed to write the progress status file: %m, status recording disabled");` → `do_record = false;` (1508)

Machine cross-check: all 25 `S237` quotes in the used-by doc `corpus/knowledge/btrfs-scrub-record-r42.md` (lines 27-132 at 78abb8b5) prefix-match the fetched bytes: `verified=25 mismatch=0` (receipts R5, `quote-check.txt`).

## 4. Tier A / kind code honest — yes
- kind `code`: `cmds/scrub.c` is upstream C source — accurate.
- tier A: consistent with the registry's own usage for pinned upstream artifacts (S009, S016, S020, S021, S022 are all `code | A` with commit/tag pins). This row carries the strongest pin in the registry — tag + peeled commit + raw-bytes sha256 — and all three reproduced today. No prose tier glossary exists in SOURCES.md at this commit (sections: Registry/Paths/Search log/Leads only); QUALITY.md:11 points to SOURCES.md for tier definitions, so convention-by-usage is what exists. Not a defect of this row.
- `status mined`, `opened 2026-10-26`, `recheck on-release`, `used-by corpus/knowledge/btrfs-scrub-record-r42.md` (exists at the pinned commit) — coherent.

## Findings
1. **[minor, non-blocking] anchor coverage gap vs use.** `btrfs-scrub-record-r42.md:116` quotes `S237` `scrub.c:342`: `(ss->canceled ? "aborted" :` — byte-true upstream (verified), but 342 lies outside all nine anchor ranges; nearest range 280-330 ends 12 lines earlier and the quote sits in `_print_scrub_ss` (body 313-345). 24/25 doc quotes are inside anchor ranges. Fix option: extend the row anchor with 340-345 (or 313-345), or re-point the doc quote at 340-343. Does not affect the row's own four checks.
2. No other defect found; nothing falsified. All anchor elements (sha256, tag, peeled commit), all nine ranges, all 25 downstream quotes, and the teaches cell verify against today's live upstream bytes.

## Residual risk / not done
- Byte/line-level verification only: I did not compile or execute `scrub.c`; behavior claims rest on read code, not a run.
- Identity rest on HTTPS fetch + GitHub API blob sha + `git ls-remote`; no local clone, so no object-graph verification beyond blob-sha equality at the pinned ref.
- SC1-SC5 verdicts are the row-verdict seats' scope; I checked only that this row grounds them at the quote level.

## Receipts
`.ufo/waves/round-42/w2/SrcReopenS237/`: `receipts.txt` (R1-R6 command logs), `v7.1-scrub.c` (fetched copy, 57034 bytes), `check_quotes.py` + `quote-check.txt` + `quote-check-input-sha.txt`, `row246.txt`.
