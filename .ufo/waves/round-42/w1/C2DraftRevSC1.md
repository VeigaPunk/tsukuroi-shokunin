ROW SC1 FIRST-READ: holds

Seat: C2DraftRevSC1 (wave-1 first falsifier, not a counted verdict). Item C2-SC1, row SC1 of
`corpus/knowledge/btrfs-scrub-record-r42.md`, read at dispatch tip f50c28d83e1832ecd7eba765caace531f45d6b27.
No tool installs were made this session (nothing to record under the 2026-10-19 tooling authorization).

## Provenance checks (all run, all passed)

- `cd .ufo/waves/round-42/frozen/src && sha256sum -c SHA256SUMS` → `scrub.c: OK`, `CHANGES: OK`
  (scrub.c `48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801`, CHANGES
  `bd881ab899ba4f4fba820207c4cb671eacbb34843db4cf95fd7d90aaff2a0d22`).
- Live source fetched 2026-10-26: `curl -fsSL https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/cmds/scrub.c`
  → sha256 `48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801` — **byte-identical to the snapshot**.
  FETCH.txt records the same tag resolution (v7.1 = 0a919c7d…, peeled 4ab0e80be9e3bb1db2e6038e6d4316d35fb7ba8b),
  matching the row header's peeled commit.
- Host capture digest: `sha256sum .ufo/waves/round-42/frozen/hostcap/capture.txt` →
  `942edc91a6b8fcda3ef29e88c3d54e7a9a48ec4cce302b8c1edcc89c8710643c`, equal to the digest named in the row header.
- Row content at the dispatch revision: `git show f50c28d8…:corpus/knowledge/btrfs-scrub-record-r42.md | sha256sum`
  → `9038ea7a4b8d8c6ac88f7feca3dfdbfc8c7822faa6ce0c0f8207c7eed077ca36`, equal to the working-tree file I read.

## Quote check — 6/6 exact (number and text), grep -n on the snapshot

- scrub.c:67 `#define SCRUB_DATA_FILE "/var/lib/btrfs/scrub.status"` — exact.
- scrub.c:459 `datafile[ret] = '.';` — exact.
- scrub.c:467 `datafile[ret] = '_';` — exact.
- scrub.c:483 `fd = open(datafile, m, 0600);` — exact.
- scrub.c:487 `ret = flock(fd, LOCK_EX|LOCK_NB);` — exact.
- scrub.c:534 `ret = rename(datafile_old, datafile_new);` — exact.

## Statement check — claim by claim

1. **Record name `/var/lib/btrfs/scrub.status.<fsid>`** — holds. Base path scrub.c:67; `scrub_datafile()`
   builds `fn_base` + `.` + `fn_local` (:459 dot, :460 strncpy) and, when `fn_tmp` is given, appends `_` + tmp
   (:467-:468). `fn_local` is the unparsed filesystem UUID at every call site: the only writer passes `fsid`
   filled by `uuid_unparse(spc->fi->fsid, fsid)` (:1025, buffer :999) into `scrub_open_file_w(SCRUB_DATA_FILE,
   fsid, "tmp")` (:917); both readers `uuid_unparse(fi_args.fsid, fsid)` (:1360, :1915) into
   `scrub_open_file_r(SCRUB_DATA_FILE, fsid)` (:1361, :1930).
2. **Every update written to sibling `scrub.status.<fsid>_tmp`, then renamed over the record** — holds. The
   only `open(` in the file is scrub.c:483 (grep for `= open(|open64(|fopen(`: single hit), so every record/tmp
   open routes through `scrub_open_file`. The only record writer is `scrub_write_progress` (:897): open tmp
   (:917) → write full file `scrub_write_file` (:918) → `scrub_rename_file(SCRUB_DATA_FILE, fsid, "tmp")`
   (:925), which renames tmp→record (:534; old name built with `fn_tmp`, new with NULL, :526-:535). The
   all-zero start record goes through the same function (:1502-:1504), as does the later update (:1702). The
   tmp name is exactly `scrub.status.<fsid>_tmp` (base + `.` + fsid + `_` + `tmp`, :459/:467 with `fn_tmp="tmp"`).
   Write completes before rename in the same thread under one mutex (:917-:925), so rename(2) publishes a whole
   file: "a reader sees either the old or the new record, never a half-written one" holds for concurrent readers.
3. **Mode 0600 on create** — holds for the record/tmp create path. `open(datafile, m, 0600)` (:483) with
   `O_WRONLY|O_CREAT` from `scrub_open_file_w` (:517); the reader passes `O_RDONLY` (:505) and creates nothing.
   Precision note N1 below on the sentence's scope.
4. **Every open takes non-blocking exclusive flock; second writer / lock-held reader fails at once** — holds.
   Single open site :483 feeds both readers (:505) and writers (:517); :487 `flock(fd, LOCK_EX|LOCK_NB)`, and on
   failure the fd is closed and `-errno` returned (:488-:493) — no waiting, no retry. Two writers of the same
   filesystem contend on the *same* `_tmp` path (:917), so the second fails the flock at once.

## Host reading check — holds, reproduced live

- capture.txt:5 `root_fsid 1d02a454-c549-4a35-b567-89d60902af8e`, capture.txt:6 `var_lib_btrfs absent` — exactly
  as the row cites; line numbers correct.
- Re-ran the read-only capture 2026-10-26: `bash .ufo/waves/round-42/frozen/hostcap/capture.sh
  /fast/scratch/hyaku/tsukuroi-r42/C2DraftRevSC1/capture.recheck.txt` (receipt copied to my seat dir) — all ten
  fields byte-identical to the frozen capture except `captured_utc` (19:45:01Z vs 19:13:44Z). `var_lib_btrfs
  absent` and the root fsid reproduce, so "no record exists" stands on this host today.

## Precision notes (non-failing; proposed text for the L1 to adopt or reject)

- **N1 — scope of "a file the CLI creates gets mode 0600".** As written, "a file" could be read to cover any
  file the CLI creates under /var/lib/btrfs; the progress socket `/var/lib/btrfs/scrub.progress`
  (SCRUB_PROGRESS_SOCKET_PATH, scrub.c:68) is created by `bind(2)` with a umask-derived mode, not 0600, and is
  not the record. Also 0600 is the `open` mode argument, applied subject to the umask. The row's referent is
  clearly the record/tmp files, so this is a tightening, not an error. Exact replacement:
  - Old: "A file the CLI creates gets mode 0600, and every open, for reading or writing, must take a
    non-blocking exclusive `flock` (`LOCK_EX`), so a second writer or a reader that finds the lock held fails
    at once instead of waiting."
  - New: "A record or `_tmp` file the CLI creates gets mode 0600 (the `open` mode argument, subject to the
    umask), and every open of either, for reading or writing, must take a non-blocking exclusive `flock`
    (`LOCK_EX`), so a second writer or a reader that finds the lock held fails at once instead of waiting."

## Residual observations (upstream code facts, not row defects; no replacement text proposed)

- **Stale-tmp tail.** The tmp open is `O_WRONLY|O_CREAT` without `O_TRUNC` (:483/:517) and there is no
  `ftruncate`/`truncate` call in the file (grep: only `unlink` hits, all on the progress socket path :1485,
  :1497, :1721). A `_tmp` left behind by a write that crashed between :917 and :925 would be reused from
  offset 0, and a shorter new record would leave a stale tail inside the renamed file. This does not contradict
  any SC1 sentence (the row claims atomic visibility, not truncation semantics), but wave-2 should not extend
  the atomicity sentence to post-crash tmp reuse.
- **No fsync before rename.** Nothing forces the tmp to disk before :534; the row's claim is about what a
  concurrent reader sees, which rename(2) guarantees without fsync. Durability across power loss is outside the
  row's claim.
- **Region pointer.** The item's review region "scrub.c:446-535" is a hint, not a row citation; the actual
  function block (`scrub_datafile` … `scrub_rename_file`) is scrub.c:448-:538. The row's own citations are all
  exact, so nothing to correct in the row.

## What I did not do

- Did not compile or run `btrfs scrub` (operator action; also unnecessary for SC1 — every claim is decided by
  the pinned source).
- Did not compare the Arch packaging patches of btrfs-progs 7.1-1 against upstream (out of SC1 scope; the
  entry's own Limits already flags this for a wave item).
- Did not verify rows SC2-SC5 (other seats' items).

## Verdict

Every sentence of the SC1 Statement is supported by the pinned, digest-verified snapshot whose bytes equal the
live v7.1 source; all six quotes are exact; the Host reading matches capture.txt:5-:6 and reproduces live.
ROW SC1 FIRST-READ: **holds**, with optional tightening N1.
