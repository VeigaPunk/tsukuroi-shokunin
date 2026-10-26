ROW SC1 VERDICT: fails

Seat: `C2CritSC1` — tsukuroi lane round 42, wave w2, item V-1b (counted row verdict, adversarial).
Row judged: SC1 of `corpus/knowledge/btrfs-scrub-record-r42.md` at dispatch tip
`78abb8b5cdc9da511b4fc523e661517a68dd33d3` (168 lines, sha256 `536846f6cb49c2c41cc48228bb03945da0d232dff28c89b35164dc88ee445ef8`,
byte-identical to the lane working tree today: `sha256sum corpus/knowledge/btrfs-scrub-record-r42.md` → same digest;
`git diff 78abb8b5..HEAD -- corpus/knowledge/btrfs-scrub-record-r42.md` → empty, `git log 78abb8b5..HEAD -- <path>` → no commits,
`grep -n Corrections <file>` → no match, so there is no later correction block to fold in). I did not write this row.
No tool installs were needed or made; nothing changed on the host, nothing written outside my seat dir and scratch.

## 1. Provenance (all run, all passed)

- `cd .ufo/waves/round-42/frozen/src && sha256sum -c SHA256SUMS` → `scrub.c: OK`, `CHANGES: OK`
  (scrub.c `48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801`,
  CHANGES `bd881ab899ba4f4fba820207c4cb671eacbb34843db4cf95fd7d90aaff2a0d22`; re-hashed independently in `check-sc1.out`).
- `.ufo/waves/round-42/frozen/hostcap/capture.txt` sha256
  `942edc91a6b8fcda3ef29e88c3d54e7a9a48ec4cce302b8c1edcc89c8710643c`, equal to the digest in the row's header line 1.
- Live read-only re-check of the one host fact SC1 rests on: `stat -c '%F %n' /var/lib/btrfs` →
  `cannot stat '/var/lib/btrfs': No such file or directory (os error 2)`; `ls -ld /var/lib/btrfs` → same. The
  capture's line 6 label `var_lib_btrfs absent` is produced by `capture.sh:11`
  `if [ -e /var/lib/btrfs ]; then … else echo "var_lib_btrfs absent"; fi`, i.e. "the path does not exist", which is
  what the row's Host reading says (not merely "not a directory").
- Quote check, automated per cited line (`check-sc1.py`, receipt `check-sc1.out`): **6/6 exact**.

| row line | cite | verdict | snapshot line as stored |
|---|---|---|---|
| 11 | scrub.c:67 | exact | `#define SCRUB_DATA_FILE "/var/lib/btrfs/scrub.status"` |
| 13 | scrub.c:459 | exact | `\tdatafile[ret] = '.';` |
| 15 | scrub.c:467 | exact | `\t\tdatafile[ret] = '_';` |
| 17 | scrub.c:483 | exact | `\tfd = open(datafile, m, 0600);` |
| 19 | scrub.c:487 | exact | `\tret = flock(fd, LOCK_EX|LOCK_NB);` |
| 21 | scrub.c:534 | exact | `\tret = rename(datafile_old, datafile_new);` |

## 2. Sentence-by-sentence (Statement, then Host reading)

**S1 — "The record for one filesystem is the file `/var/lib/btrfs/scrub.status.<fsid>` (the base path plus a dot plus
the filesystem UUID; the name pattern is already held, SH4)." — holds.**
`SCRUB_DATA_FILE` scrub.c:67; `scrub_datafile()` appends `.` (:459) then `fn_local` (:460), and `_`+`fn_tmp` when a
tmp name is given (:467-468). `fn_local` is the unparsed filesystem UUID at every call site: writer
`uuid_unparse(spc->fi->fsid, fsid)` :1025 → `scrub_open_file_w(SCRUB_DATA_FILE, fsid, "tmp")` :917; readers
`uuid_unparse(fi_args.fsid, fsid)` :1360 / :1915 → `scrub_open_file_r(SCRUB_DATA_FILE, fsid)` :1361 / :1930. SH4
(`corpus/knowledge/storage-health-r26.md:57`) does state the `scrub.status.<UUID>` pattern, so the cross-reference is
sound. One record per filesystem (not per device) is consistent with the per-device *lines* of SC2.

**S2 — sentence 1 "Every update is written to a sibling file `scrub.status.<fsid>_tmp` and then moved over the record
with `rename`" — holds; sentence 2 "so a reader sees either the old or the new record, never a half-written one" —
FALSE on the pinned source.** This clause is the falsifying sentence (section 3). Sentence 1's support: the only
record writer is `scrub_write_progress` :897 — open `_tmp` :917 (`fn_tmp="tmp"`), write the whole file :922 →
`scrub_write_file` :843 which starts with the version line :856 and rewrites every device line from the beginning
:863-889, then `scrub_rename_file` :925 → :520-535, new name built with `fn_tmp=NULL` :530. The start (all-zero)
write takes the same path :1501-1504, and so does the final write :1702.

**S3 — "A record or `_tmp` file the CLI creates gets mode 0600 (the `open` mode argument, subject to the umask), and
every open of either, for reading or writing, must take a non-blocking exclusive `flock` (`LOCK_EX`), so a second
writer or a reader that finds the lock held fails at once instead of waiting." — holds**, with two precision notes.
There is exactly one `open(` in the file (:483, mode `0600`, effective only with `O_CREAT`) and both helpers route
through it: `O_RDONLY` for reads :505, `O_WRONLY|O_CREAT` for writes :517. `flock(fd, LOCK_EX|LOCK_NB)` :487, and on
failure the fd is closed and `-errno` returned :488-492 — no wait, no retry. Notes (non-falsifying):
- **N1 (mode source).** The *record* is never created by `open`: it appears only through `rename` of the `_tmp`
  (:534), so it inherits the `_tmp`'s mode rather than an `open` mode argument of its own; and a pre-existing `_tmp`
  is opened without `O_CREAT` semantics (mode ignored). Parenthetical is loose, effect is 0600 & ~umask. Exact
  tightening in section 5 (N1).
- **N2 (which pair the lock excludes).** The writer locks the `_tmp` *inode* and the reader locks the *record* inode,
  so a reader never contends with a writer that is mid-update; the only reader/writer contention is the window
  between `rename` :925 and `close` :931, where the writer still holds `LOCK_EX` on the now-record inode. Measured
  (`stale-tmp-demo.out`, last section): reader `flock(LOCK_EX|LOCK_NB)` while the writer's fd is open →
  `EWOULDBLOCK (Resource temporarily unavailable)`; after close → acquired. In that window `btrfs scrub status`
  prints `failed to open status file: %m` and exits 1 (:1931-1935), i.e. the reader sees **neither** record. S3 states
  this ("a reader that finds the lock held fails at once"); S2's "sees either" does not, which is the second reason
  S2 overreaches (section 4).

**S4 — "(The progress socket `/var/lib/btrfs/scrub.progress.<fsid>` is a different file, created by `bind`, not
covered here.)" — holds.** `SCRUB_PROGRESS_SOCKET_PATH` :68; the name is built with the same helper
`scrub_datafile(SCRUB_PROGRESS_SOCKET_PATH, fsid, NULL, sock_path, …)` :1461-1462 and the file is created by
`bind(prg_fd, …)` :1466 (reader side rebuilds the same sun_path :1923-1926). It is created by `bind`, not by
`scrub_open_file`, and carries no flush of the record.

**Host reading — "No record exists: `/var/lib/btrfs` is absent (capture.txt:6) for the root filesystem
`1d02a454-c549-4a35-b567-89d60902af8e` (capture.txt:5)." — holds.** capture.txt:5
`root_fsid 1d02a454-c549-4a35-b567-89d60902af8e`; capture.txt:6 `var_lib_btrfs absent` (both lines non-empty, so the
counter's `host_ok` pointer is satisfied); reproduced live today (`stat /var/lib/btrfs` → ENOENT). Since the record's
directory itself is absent, no `scrub.status.<root fsid>` can exist; the row states only that, not "never scrubbed".

## 3. The counterexample (the falsifying branch, run)

The universal "never a half-written one" is not supported, and the record a reader gets can be a mixture of two
different publications — neither the old nor the new record. Chain, all from the pinned snapshot:

1. The `_tmp` open is `O_WRONLY|O_CREAT` and **not** `O_TRUNC` (`scrub.c:517`; `grep -n 'O_TRUNC\|O_EXCL' scrub.c` →
   no hit), and nothing truncates afterwards (`grep -n 'truncate\|ftruncate' scrub.c` → no hit).
2. The `_tmp` path is deterministic (`base + '.' + fsid + "_tmp"`, :459/:467/:513), and nothing removes it:
   `grep -n 'unlink(' scrub.c` → only `:1485`, `:1497`, `:1721`, all on `sock_path` (the progress socket).
3. A write that fails leaves it: `:922` `err = scrub_write_file(...)`; `:923-924` `if (err) goto out1;` → `:929-934`
   close without `rename`. A failed `rename` (:925-927) and a killed process leave it too. The row's own SC3 says
   record-write failures occur ("a record-write failure later in the run ends the progress writes").
4. The next run opens that same path from offset 0 and writes a **shorter** record: the all-zero start record
   (:1501-1504) is the shortest record for a given device count, and any leftover from a run that made progress is
   longer (a 174.40 GiB scrub gives `data_bytes_scrubbed` ≈ 1.9e11 = 12 digits where the start record has `0`;
   +~50 bytes on this host's field set). `rename` :534 then publishes the union.

Model with the exact flags, byte-for-byte record format (`stale-tmp-demo.py`, receipt `stale-tmp-demo.out`; the
leftover `_tmp` is `fsync`ed before the "kill", so this does not depend on unflushed data):

```
leftover tmp exists: True size: 410
new record bytes: 360  stale _tmp bytes: 410  -> new is shorter: True
record size: 410  == len(new)? False
record == new? False | record == old? False
head equals the all-zero record: True         appended bytes: 50
  line 1: b'scrub status:1'
  line 2: b'1d02a454-…-89d60902af8e:1|data_extents_scrubbed:0|…|finished:0'
  line 3: b'1|t_resumed:0|duration:4213|canceled:0|finished:0'
tail is a verbatim suffix of the killed run's record: True
```

What the reader then does (parser `scrub_read_file` :578-771): line 3 fails the fsid check at :679-689
(`j != BTRFS_UUID_UNPARSED_SIZE - 1`) → `_SCRUB_INVALID` :569-576 → `warning("invalid data on line %d pos %d state %d
(near \"%.*s\") …")` and skip the line; both call sites pass `report_errors = 1` (:1366, :1940). So `btrfs scrub
status` reads a file that is 50 bytes longer than the record its writer wrote and prints an invalid-data warning for
it, on that read and on every later read until a longer record overwrites the tail. The reader does not see "the old
record" (the old record is a different file content), and does not see "the new record" (50 bytes of it were never
written by that update). The word "never" is therefore false of the pinned code, not merely unproven — the row's
first-line verdict word is `fails` under the seat definition ("a sentence is false") — while S1, S3, S4, the
Host reading and S2's first clause hold.

A second, smaller overreach in the same clause, independent of any failure: in the :925→:931 window a reader's open
of the finished record fails `EWOULDBLOCK` (measured above) and `btrfs scrub status` exits 1 with
`failed to open status file: Resource temporarily unavailable` (:1931-1935), so "a reader sees either the old or the
new record" has a third outcome; S3 states it, S2's universal does not admit it.

## 4. Impacted axes

- **SC1 (this row's verdict):** fails as written; the failing unit is exactly S2's last clause. S1, S3, S4 and the
  Host reading stand, so the correction is bounded to one sentence (plus one quote) and does not touch the row's
  proposition token.
- **C2 (frozen counter, `tools/check-scrub-record-r42.py`, sha256 `dbe933ec…0503f`):** the counter's SC1 gate is
  `token: 'LOCK_EX'` and window `scrub.c 446-535` (:55) — S3 keeps `LOCK_EX` and adds no out-of-window citation, and
  a new quote at :517 lies inside the same window (`good >= 1 and in_window >= 1 and bad == 0`, counter :210-215), so
  the correction keeps the counter's lexical gates intact. The predicate itself needs no change; `verdicts_ok`
  will read FAIL until the w2 pair plus a residual seat bind a corrected row (counter :232-236), which is the
  expected cost of a falsified claim, not a counter defect.
- **C1:** untouched; I ran no census command and no C1 counter.
- **No axis widened:** I did not read the record's durability across power loss as established (no `fsync` before
  :534, `grep -n 'fsync\|fdatasync' scrub.c` → no hit), so I did not use it as evidence for the verdict; it is only a
  reason the corrected text must not claim durability.

## 5. Smallest safe correction (exact text)

**R1 — replace S2's second clause (the false universal).**
Old: "Every update is written to a sibling file `scrub.status.<fsid>_tmp` and then moved over the record with
`rename`, so a reader sees either the old or the new record, never a half-written one."
New: "Every update is written in full to a sibling file `scrub.status.<fsid>_tmp` and, only when that write succeeds,
moved over the record with `rename`, so a reader never catches an update that is still being written: it opens the
record before or after the swap (in the moment between `rename` and `close` the still-held lock makes the open fail,
S3). The `_tmp` is opened `O_WRONLY|O_CREAT` without `O_TRUNC` (scrub.c:517) and is never deleted, so a `_tmp` left
by a failed write, a failed `rename` or a killed process is reused from offset 0: a later, shorter record — notably
the all-zero start record (:1502) — then leaves the tail of the older record inside the renamed file, and
`btrfs scrub status` reports it as `invalid data on line …` (:569-576, `report_errors` 1 at :1366 and :1940) until a
longer record is written."

**R2 — add the missing quote for the branch, in the same window** (keeps the row's quote-bound rule; token and
window unchanged):
`**Quote.** `S237` scrub.c:517: "return scrub_open_file(datafile, O_WRONLY|O_CREAT);"`

**N1 (precision, adopt or reject) — mode source.** Old: "gets mode 0600 (the `open` mode argument, subject to the
umask)". New: "gets mode 0600 on creation (the `open` mode argument, subject to the umask; the record itself appears
only through `rename` of the `_tmp`, scrub.c:534, so it inherits that mode)".

**N2 (precision, adopt or reject) — which opens exclude which.** After "every open of either, for reading or
writing, must take a non-blocking exclusive `flock` (`LOCK_EX`)", add: "the writer's lock is on the `_tmp` inode and
the reader's on the record inode (scrub.c:917, :1930), so the two exclude each other only between `rename` :925 and
`close` :931".

Nothing else in SC1 needs changing; S1, S3, S4 and the Host reading are already exact at the lines cited.

## 6. What I did not do / limits

- Did not run `btrfs scrub status|start|limit`, touch `/var/lib/btrfs`, or write anywhere outside my seat dir and
  `/fast/scratch/hyaku/tsukuroi-r42/C2CritSC1` (removed at the end after copying receipts). No `unshare`, no sudo,
  no pacman, no service, no git/jj mutation in the lane; only `git show/rev-parse/log/diff/grep` read-only calls.
- Did not run the frozen C2 counter `tools/check-scrub-record-r42.py` (binding/aggregation is the integrator's step)
  and did not run the C1 counter (other claim, host is loaded).
- Did not test the power-loss branch (no `fsync` before `rename`); it is marked as unproven above and not used.
- Did not verify rows SC2-SC5 (other seats' items), and did not look at the paired w2 reviewer's verdict.
- The demo models the write path on an ordinary filesystem, not on btrfs; it uses the exact flags, mode and sequence
  from :483/:517/:922/:925 and the exact record byte format from :856-889. The claim it supports (no `O_TRUNC` ⇒ a
  shorter rewrite keeps the old tail) is POSIX `open(2)`/`write(2)` semantics, not a filesystem-specific behaviour;
  the only btrfs-dependent part would be the durability branch, which I did not use.
