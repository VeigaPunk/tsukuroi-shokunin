ROW SC2 VERDICT: holds

Seat C2RevSC2, tsukuroi lane round-42 w2 (hyaku run 9), item V-2a (counted verdict). I did not write this row. My item names no wave-1 report to read; I additionally consulted w1/C2DraftRevSC2.md for context only (it reached "holds" on the draft at f50c28d8; the w1 integration commit 78abb8b5 corrected SC1/SC3/SC4/scope/triage but not SC2, per its commit message).

## Scope and method

- Row text: SC2 of `corpus/knowledge/btrfs-scrub-record-r42.md` at 78abb8b5cdc9da511b4fc523e661517a68dd33d3, extracted with `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 78abb8b5…:corpus/knowledge/btrfs-scrub-record-r42.md` (receipt `record-at-pin.md`; the SC2 section is lines 42-63, `## SC3` starts at 64). The working tree is clean for this file (`git status --porcelain -- corpus/knowledge/btrfs-scrub-record-r42.md` → empty) and 78abb8b5 is the last commit touching it (`git log --oneline -3 -- <file>` → 78abb8b5, f50c28d8), so the integrated text is the pin text. No `Corrections` section exists anywhere in the file (grep over the extracted text: no hit) and nothing is appended inside the SC2 section.
- Snapshot integrity: `cd .ufo/waves/round-42/frozen/src && sha256sum -c SHA256SUMS` → observed `scrub.c: OK`, `CHANGES: OK` (2026-10-26).
- Capture integrity: `sha256sum .ufo/waves/round-42/frozen/hostcap/capture.txt` → observed `942edc91a6b8fcda3ef29e88c3d54e7a9a48ec4cce302b8c1edcc89c8710643c`, equal to the digest pinned in the record header (record-at-pin.md:2).
- Every Quote line located by `grep -n` on the pinned scrub.c (receipt `quotes-verified.txt`). No tools were installed for this seat.

## Quote checks — all five occur on the cited line

1. scrub.c:69 — observed `#define SCRUB_FILE_VERSION_PREFIX "scrub status"` (grep -n: `69:#define SCRUB_FILE_VERSION_PREFIX "scrub status"`). Exact.
2. scrub.c:856 — observed `ret = scrub_write_buf(fd, SCRUB_FILE_VERSION_PREFIX ":"` (grep -n: `856:	ret = scrub_write_buf(fd, SCRUB_FILE_VERSION_PREFIX ":"`; leading tab in source). Exact; the literal continues at :857 with `SCRUB_FILE_VERSION "\n",`.
3. scrub.c:840 — observed `return scrub_writev(fd, buf, max, "|%s:%lld", key, val);`. Exact.
4. scrub.c:870 — observed `		    _SCRUB_KVWRITE(fd, buf, data_extents_scrubbed, use) ||` (leading whitespace in source). Exact.
5. scrub.c:888 — observed `		    _SCRUB_KVWRITE_STATS(fd, buf, finished, use) ||`. Exact.

## Statement, sentence by sentence

S1 "The record is text." — TRUE. The record's only writer is `scrub_write_file` (scrub.c:843), reached for the record file only via `scrub_write_progress` (opens the `_tmp` fd at :917, calls scrub_write_file at :922, renames over the record at :925; further scrub_write_progress calls at :1123, :1503, :1702; the other scrub_write_file call at :1112 writes to the progress-socket `peer_fd`, not the record). Every byte emitted is character data: `scrub_write_buf` is a bare `write(fd, data, len)` wrapper returning `ret - len` (scrub.c:772-776), `scrub_writev` formats with vsnprintf then writes the buffer (scrub.c:778-793), and scrub_write_file emits only string literals and formatted text (:856-859, :865-868, :840, :889). No binary encoding on the path.

S2 "Its first line is `scrub status:1` (format prefix and version 1)." — TRUE. The first write to the record is the version line: scrub.c:856-859 writes `SCRUB_FILE_VERSION_PREFIX ":" SCRUB_FILE_VERSION "\n"`, i.e. "scrub status" ":" "1" "\n" (defines at scrub.c:69 and :70), before the per-device loop that starts at :863. The `_tmp` fd is opened `O_WRONLY|O_CREAT` (scrub.c:517, via `scrub_open_file_w` at :917) and each update is renamed over the record (:925), so the write starts at offset 0 and the record's first line is this version line. The reader independently requires it: state 0 parses SCRUB_FILE_VERSION_PREFIX and rejects `version != atoll(SCRUB_FILE_VERSION)` with -ENOTSUP (scrub.c:627-632). The parenthetical is accurate: the prefix is the format prefix, "1" is the version.

S3 "Each further line belongs to one device: the filesystem UUID, a colon, the device id, then one `|key:value` pair per field, in this order — <the 14 progress counters>, then the run fields <t_start, t_resumed, duration, canceled, finished>." — TRUE.
- One line per device: the loop `for (i = 0; i < n; ++i)` (scrub.c:863) writes per iteration exactly fsid (:865), ":" (:866), devid (:867-868), the kv pairs (:870-888), "\n" (:889); nothing is written between the version line and the device lines or after the loop (`return 0` at :894).
- Filesystem UUID: the `fsid` argument is the unparsed UUID string — `char fsid[BTRFS_UUID_UNPARSED_SIZE]` (scrub.c:999) filled by `uuid_unparse(spc->fi->fsid, fsid)` (:1025; same pattern at :1360, :1915); the reader requires exactly 36 chars before the ':' and parses them with `uuid_parse` into a `BTRFS_FSID_SIZE` uuid (scrub.c:676-690).
- Colon and device id: ":" literal (scrub.c:866); devid written as `"%lld"` of `use->scrub_args.devid` (scrub.c:867-868). Writer/reader round-trip corroborates the devid is in the record: reader case 4 "read dev id" parses the digits after the colon into `p[curr]->devid` (scrub.c:692-699). Source-level nuance (does not affect the row): the devid reaches the fd through `scrub_writev` itself, which formats into buf and then writes buf (scrub.c:778-793); the next chain element `scrub_write_buf(fd, buf, ret)` (:869) is a no-op because `ret` is 0 — the version-line write returns `written - len` = 0 on success and `if (ret) return -EOVERFLOW;` (:860-861) guarantees ret == 0, and nothing reassigns `ret` inside the loop.
- `|key:value` per field: `scrub_kvwrite` formats `"|%s:%lld"` (scrub.c:840).
- Order: source order at scrub.c:870-888 is exactly the row's list — data_extents_scrubbed (:870), tree_extents_scrubbed (:871), data_bytes_scrubbed (:872), tree_bytes_scrubbed (:873), read_errors (:874), csum_errors (:875), verify_errors (:876), no_csum (:877), csum_discards (:878), super_errors (:879), malloc_errors (:880), uncorrectable_errors (:881), corrected_errors (:882), last_physical (:883), then t_start (:884), t_resumed (:885), duration (:886), canceled (:887), finished (:888). The row's "progress counters"/"run fields" split matches the two macro groups field for field: `_SCRUB_KVWRITE` reads `use->scrub_args.progress.<name>` (:830-832), `_SCRUB_KVWRITE_STATS` reads `use->stats.<name>` (:834-836). The reader does not contradict this order: `_SCRUB_KVREAD` is guarded by `if (ret == 0)` so only the first matching key consumes per pair (scrub.c:538, :700-741) — it matches order-independently, and state 6 re-enters per `|` (scrub.c:742-749).

S4 "A record therefore carries per-device error sums and a per-device finished flag, not one filesystem verdict." — TRUE. Each device line carries its own error counters (read_errors, csum_errors, verify_errors, super_errors, malloc_errors, uncorrectable_errors, corrected_errors — scrub.c:874-881) and its own `finished` (:888); "sums" is literal for a resumed run, where `scrub_resumed_stats` adds the resumed run's counters into the current one before writing (`_SCRUB_SUM`, scrub.c:794-818). The record contains no filesystem-level line: the write path emits only the version line plus per-device lines (:856-892), and the reader stores one per-device entry per line (allocation at scrub.c:645-664, fsid at :676-690, devid at :692-699). The filesystem verdict is computed by the status command from the records, not stored in the record.

## Host reading

"Not observable on this host: there is no record to parse (capture.txt:6)." — TRUE. capture.txt:6 is `var_lib_btrfs absent`; with `/var/lib/btrfs` absent there is no record file, so the row claims nothing it did not observe. The capture digest matches the pinned one (see Method). The row makes no other host claim.

## Overreach scan

No sentence overreaches: the row claims only the record's format (text; first line; per-device line shape and field order; per-device error sums and finished flag) and the host absence of a record. It makes no claim about who writes the record or when recording is disabled (SC3's ground), nor about how the status command aggregates devices into a verdict (SC4's ground, cross-referenced by the entry's triage section at record-at-pin.md:147).

## Not done

- No scrub was run and no record was created or parsed live (operator actions, forbidden for this seat); the format claims rest on the pinned v7.1 source, which the entry's Limits section pins to the installed binary (Arch btrfs-progs 7.1-1, no packaging patch — record-at-pin.md:152-155, citing wave-1 C2ExecLiveSources).
- The upstream URLs were not re-fetched by this seat (recheck-on-release item); wave-1 C2DraftRevSC2.md reports the pinned scrub.c byte-identical to the live v7.1 raw GitHub file on 2026-10-26 (both sha256 48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801) — their observation, not re-run here.
- CHANGES (S238) was digest-verified but not otherwise consulted: SC2 cites only S237 and S239, and no SC2 sentence rests on CHANGES.

## Verdict basis

Every sentence of the SC2 Statement and Host reading is true of the pinned source and the capture; all five quotes occur on their cited lines; nothing is incomplete or overreaching. No replacement text required.

Receipts (this dir): `record-at-pin.md`, `quotes-verified.txt`, `capture-digest.txt`. Scratch `/fast/scratch/hyaku/tsukuroi-r42/C2RevSC2` removed after copying.
