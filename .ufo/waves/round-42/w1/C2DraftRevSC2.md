ROW SC2 FIRST-READ: holds

Seat C2DraftRevSC2, tsukuroi lane round-42 w1 (hyaku run 9), item C2-SC2: the `scrub status:1` first
line and the per-device `<fsid>:<devid>|key:value` line with its field order, against scrub.c:826-895
and :67-70. Basis: the corpus row read at the pinned entry commit f50c28d83e1832ecd7eba765caace531f45d6b27
via `git show f50c28d8…:corpus/knowledge/btrfs-scrub-record-r42.md` (dumped to scratch; NOT read from the
working tree, whose HEAD had already advanced to 87c4f7c627e377e5f6d361498e8db9b3886d7953).

## 1. Snapshot integrity and live-source identity
- Command: `cd …/round-42/frozen/src && sha256sum -c SHA256SUMS` → observed `scrub.c: OK`, `CHANGES: OK`, exit 0.
- Command (2026-10-26): `curl -fsSL https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/cmds/scrub.c -o scrub.c.live && sha256sum scrub.c.live …/frozen/src/scrub.c`
  → observed both `48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801`. The pinned snapshot is
  byte-identical to the live v7.1 file today, so every line cite below is simultaneously true of both.
- frozen/src/FETCH.txt records the same URL and tag (v7.1 = 0a919c7d6e389c07920675b7fad3f793b92aa78b), consistent.

## 2. Quote checks — all five hold exactly (S237 = pinned/live scrub.c)
- scrub.c:69 — observed `#define SCRUB_FILE_VERSION_PREFIX "scrub status"` — quote text exact. ✅
- scrub.c:856 — observed `ret = scrub_write_buf(fd, SCRUB_FILE_VERSION_PREFIX ":"` (continues :857 `SCRUB_FILE_VERSION "\n",`) — exact. ✅
- scrub.c:840 — observed `return scrub_writev(fd, buf, max, "|%s:%lld", key, val);` — exact. ✅
- scrub.c:870 — observed `		    _SCRUB_KVWRITE(fd, buf, data_extents_scrubbed, use) ||` — exact modulo leading tab. ✅
- scrub.c:888 — observed `		    _SCRUB_KVWRITE_STATS(fd, buf, finished, use) ||` — exact modulo leading tab. ✅
Supporting pins: SCRUB_FILE_VERSION "1" at :70; SCRUB_DATA_FILE "/var/lib/btrfs/scrub.status" at :67.

## 3. Statement checks — every sentence holds
1. "The record is text." Holds. The writer emits only literal strings and vsnprintf-formatted buffers:
   scrub_write_buf is a bare write(2) wrapper (scrub.c:773-779); scrub_writev formats via vsnprintf with
   `__attribute__ ((format (printf, 4, 5)))` (scrub.c:778-796); keys are C identifiers stringified by
   `#name` in the macros at scrub.c:830-836. No binary encoding anywhere in scrub_write_file (scrub.c:843-893).
2. "Its first line is `scrub status:1` (format prefix and version 1)." Holds. scrub.c:856-859 writes
   `SCRUB_FILE_VERSION_PREFIX ":" SCRUB_FILE_VERSION "\n"` = "scrub status" ":" "1" "\n", with the defines at
   scrub.c:69-70; this header is written exactly once, before the per-device loop that starts at scrub.c:863.
3. "Each further line belongs to one device: the filesystem UUID, a colon, the device id, then one
   `|key:value` pair per field". Holds. Loop `for (i = 0; i < n; ++i)` at scrub.c:863 writes, per device:
   fsid (scrub.c:865) — an unparsed filesystem UUID from `uuid_unparse(fi_args.fsid, fsid)` (scrub.c:1025,
   buffer scrub.c:999, passed by the record thread at scrub.c:1123) — then the literal ":" (scrub.c:866),
   then the devid as "%lld" of `use->scrub_args.devid` (scrub.c:867-868), then `|key:value` pairs via
   scrub.c:840, terminated by "\n" at scrub.c:889.
4. Field order. Holds exactly. scrub.c:870-883 progress counters in the stated order:
   data_extents_scrubbed(870), tree_extents_scrubbed(871), data_bytes_scrubbed(872), tree_bytes_scrubbed(873),
   read_errors(874), csum_errors(875), verify_errors(876), no_csum(877), csum_discards(878), super_errors(879),
   malloc_errors(880), uncorrectable_errors(881), corrected_errors(882), last_physical(883); then scrub.c:884-888
   run fields: t_start(884), t_resumed(885), duration(886), canceled(887), finished(888). 14 + 5, no
   reorderings, omissions or extras; keys equal the identifiers as written in the Statement.
5. "A record therefore carries per-device error sums and a per-device finished flag, not one filesystem
   verdict." Holds. Every error counter and the `finished` flag sit inside the per-device loop
   (scrub.c:870-888); scrub_write_file writes only the version header plus n device lines and returns
   (scrub.c:843-893); no aggregate/verdict line exists. The read side corroborates: it parses the version
   prefix then `atoll(SCRUB_FILE_VERSION)` (scrub.c:626-632) and the fsid via `uuid_parse` (scrub.c:683-686).

## 4. Host reading holds
Row sentence: "Not observable on this host: there is no record to parse (capture.txt:6)."
- frozen/hostcap/capture.txt:6 observed: `var_lib_btrfs absent`. capture.sh emits that line only when
  `[ -e /var/lib/btrfs ]` is false (frozen/hostcap/capture.sh, the `if [ -e /var/lib/btrfs ]` branch).
- SCRUB_DATA_FILE is "/var/lib/btrfs/scrub.status" (scrub.c:67), so with /var/lib/btrfs absent there is no
  record to parse — the sentence is correct and appropriately modest ("not observable", not "never written").
- Corroboration: capture.txt:3 shows `btrfs-progs btrfs-progs 7.1-1` installed, i.e. the pinned v7.1 source
  is the running tool's version, and capture.txt:5 `root_fsid 1d02a454-…` is a btrfs root (capture.txt:4)
  that has never left a record on this host.

## 5. Proposed replacement text
None. No sentence of the SC2 Statement, no Quote line number or text, and the Host reading is wrong or
overreaching; nothing to replace.

## 6. Observations (non-defects, for the L1's information)
- The values written per device are the resume-folded view: `use = scrub_resumed_stats(&data[i], &local)`
  (scrub.c:864; sums via _SCRUB_SUM, scrub.c:798-808). SC2 makes no claim about which values are written,
  so this is consistent; the folding itself is SC4's subject.
- The version define SCRUB_FILE_VERSION "1" lives at scrub.c:70 and is not separately quoted in the row;
  the :856 quote concatenates prefix ":" version, so the citation is implicit, not missing.

## 7. What I did not do
- Did not and could not observe a real record: none exists on this host (that absence is the row's own
  Host reading) and running `btrfs scrub start` is forbidden by the host guard. All verification is static
  source analysis plus the host capture, on a snapshot proven byte-identical to live v7.1 on 2026-10-26.
- Did not check rows SC1/SC3/SC4/SC5 or the doc sections outside row SC2 (out of item scope).
- Receipts: frozen/hostcap parity and fetch artifacts under .ufo/waves/round-42/w1/C2DraftRevSC2/
  (receipts.txt, scrub.c.live, record-at-f50c28d.md). Scratch /fast/scratch/hyaku/tsukuroi-r42/C2DraftRevSC2
  removed after copying.
