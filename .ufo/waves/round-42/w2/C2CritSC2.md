ROW SC2 VERDICT: holds

Seat C2CritSC2, tsukuroi lane round 42 w2 (hyaku run 9), item V-2b (counted verdict, adversarial).
Row judged: `## SC2` of `corpus/knowledge/btrfs-scrub-record-r42.md` at `78abb8b5cdc9da511b4fc523e661517a68dd33d3`
(entry:42-62). The file is unchanged at lane HEAD `a968393c` (`git diff 78abb8b5..HEAD -- <file>` empty), and SC2's
text is unchanged since the w1 entry commit `f50c28d8` (that diff changes the preamble, SC1, SC3, SC4, one triage
bullet and one Limits bullet; no changed line falls in entry:42-62). All line numbers below are the merged text as it
stands.

## Basis (identity first, before any reading)

- `cd .ufo/waves/round-42/frozen/src && sha256sum -c SHA256SUMS` → `scrub.c: OK`, `CHANGES: OK` (exit 0).
- Fresh clone `git clone --depth 1 --branch v7.1 https://github.com/kdave/btrfs-progs` resolves to peeled commit
  `4ab0e80be9e3bb1db2e6038e6d4316d35fb7ba8b`, exactly the commit `frozen/src/FETCH.txt` records. Its
  `cmds/scrub.c` = `48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801` and `CHANGES` =
  `bd881ab899ba4f4fba820207c4cb671eacbb34843db4cf95fd7d90aaff2a0d22` — the pinned digests (receipts
  `C2CritSC2/identity.txt`). Every line cite below is therefore simultaneously true of the snapshot and of the
  upstream v7.1 tag.
- Whole-tree grep of that clone for `SCRUB_DATA_FILE|SCRUB_FILE_VERSION|scrub\.status` outside `cmds/scrub.c`:
  no hits (`identity.txt`). `scrub_write_file` is the only place in v7.1 that defines the record's bytes, so a
  single writer's literal sequence is a complete basis for a format claim.
- Empirical side used the installed binary `btrfs-progs v7.1` (`btrfs --version`, also capture.txt:3) as the real
  reader, against crafted records mounted only inside private `unshare -rm` namespaces (`C2CritSC2/probes.txt`).

## Per-sentence check

Statement at entry:44-50; Host reading at entry:62.

1. entry:44 "The record is text." — the write path emits only literals and printf-formatted numbers/strings:
   `scrub_write_buf` is a bare `write(2)` wrapper (scrub.c:773-778), `scrub_writev` formats with `vsnprintf`
   (scrub.c:780-796), keys are `#name` stringifications (scrub.c:830-836), and the only other writes in
   `scrub_write_file` are the literal `":"` and `"\n"` (scrub.c:866, :889). No binary encoding anywhere in
   :843-895. Empirically the shipped reader consumed our ASCII record and rendered every field (`probes.txt`
   `rec_ok`). **Supported.**
2. entry:44 "Its first line is `scrub status:1` (format prefix and version 1)." — `SCRUB_FILE_VERSION_PREFIX
   "scrub status"` at scrub.c:69, `SCRUB_FILE_VERSION "1"` at scrub.c:70, written once before the device loop as
   prefix `":"` version `"\n"` with `+2` for the two separators (scrub.c:856-859); the `for (i = 0; i < n; ++i)`
   loop opens at scrub.c:863, so nothing can precede it. Prediction tested against the real binary: a record whose
   first line is `scrub status:2` is refused — `WARNING: failed to read status: Operation not supported`, then
   "no stats available" (`probes.txt` `rec_v2`) — while `scrub status:1` parses fully (`rec_ok`). The first line's
   `prefix:version` is load-bearing exactly as stated. **Supported.**
3. entry:44-46 "…the filesystem UUID, a colon, the device id, then one `|key:value` pair per field" — fsid at
   scrub.c:865, `":"` at :866, devid as `"%lld"` at :867-868, then pairs through `scrub_kvwrite`'s `"|%s:%lld"`
   (scrub.c:838-841), line closed by `"\n"` at :889. The reader agrees on every element: 36-char UUID then `':'`
   (scrub.c:676-690, length enforced at :683), digits then one separator skipped (:692-698), key:value pairs
   (:701-740), `'|'` continues / `'\n'` ends (:745-753). `probes.txt` `rec_ok` renders the line. **Supported.**
4. entry:46-49 the 14 progress counters then the 5 run fields — `_SCRUB_KVWRITE` calls at scrub.c:870-883
   (data_extents_scrubbed, tree_extents_scrubbed, data_bytes_scrubbed, tree_bytes_scrubbed, read_errors,
   csum_errors, verify_errors, no_csum, csum_discards, super_errors, malloc_errors, uncorrectable_errors,
   corrected_errors, last_physical) and `_SCRUB_KVWRITE_STATS` calls at scrub.c:884-888 (t_start, t_resumed,
   duration, canceled, finished). A mechanical comparison of the row's 19 names against the 19 writer arguments is
   19/19 identical and in order (`C2CritSC2/quote-order.txt`). Empirically `btrfs scrub status -d -R` printed
   precisely those 19 fields from our record (`probes.txt` `rec_ok`). **Supported.**
5. entry:49-50 "A record therefore carries per-device error sums and a per-device finished flag, not one filesystem
   verdict." — every statistic is written inside the per-device loop (scrub.c:863-891); the error fields are
   scrub.c:874-882 and `finished` is :888; `scrub_write_file` writes nothing but the version header (:856-859) and
   n device lines, so no aggregate line exists (:843-895). "Sums" is literal, not loose: `_SCRUB_SUM` at
   scrub.c:795-796 assigns `data->resumed->p.name + data->scrub_args.progress.name`, applied per device at
   scrub.c:806-820. Empirically the per-device history block is printed from that single record line, and the device
   status it shows (`Status: finished`) comes from the written `finished:1` with `canceled:0` (`probes.txt`
   `rec_ok`). **Supported.**
6. entry:62 "Not observable on this host: there is no record to parse (capture.txt:6)." — capture.txt:6 is
   `var_lib_btrfs absent`, emitted by `capture.sh` in the `[ -e /var/lib/btrfs ]` else-branch; the record path is
   `SCRUB_DATA_FILE "/var/lib/btrfs/scrub.status"` (scrub.c:67) under that directory, so no record can exist.
   Independently re-checked today rather than trusting the capture: `ls -d /var/lib/btrfs` → "No such file or
   directory", and the real command `btrfs scrub status /` → "\tno stats available" (`probes.txt`). The wording is
   the modest one ("not observable", not "never written"), consistent with SC3. **Supported.**

## Attacks tried, and why none lands

- **A1 — "in this order" as a reader requirement (the strongest overreach candidate).** The reader does not
  require the writer's order: `_SCRUB_KVREAD` matches at the current offset and the chain stops at the first hit
  (scrub.c:538-540, :701-740), so all 19 names are tried at every position. Tested: a record with the field order
  fully reversed parsed to identical output (`probes.txt` `rec_reorder`). This does not touch the row: the row
  states the order the record's pairs *are written in*, and the writer's order is fixed (attack A-source:
  scrub.c:870-888). Informational only.
- **A2 — universal "each further line belongs to one device" against the un-truncated tmp file.** `scrub_open_file`
  calls `open(datafile, m, 0600)` (scrub.c:483) and the writer opens `O_WRONLY|O_CREAT` with no `O_TRUNC`
  (scrub.c:517). A write that fails before the rename can leave a longer `scrub.status.<fsid>_tmp`; a later,
  shorter record renamed over it would keep stale bytes after the new last newline. Tested the consequence: such a
  trailing fragment produces `WARNING: invalid data on line … state 5` while the complete device line still parses
  into the correct values (`probes.txt` `rec_tail`). The fragment is not a line the writer emitted, and the row
  describes the writer's output, so the sentence is not false; the residue is SC1's rename territory and the
  reader's skip path (scrub.c:569-576, :754-764) contains it. Recorded as a limit, not a falsification.
- **A3 — "version 1" as a universal across tool versions.** `rec_v2` shows v7.1 refuses any other version
  (scrub.c:631-632 `version != atoll(SCRUB_FILE_VERSION)` → `-ENOTSUP`). So the first line is guaranteed
  `scrub status:1` only for records v7.1 writes — which is exactly the entry's stated scope at entry:13-14 ("Rows
  SC1-SC5 state upstream behaviour of btrfs-progs v7.1"). Not an overreach of the row.
- **A4 — wrong lines.** All five Quote lines are byte-exact at scrub.c:69, :856, :840, :870, :888
  (`quote-order.txt`: `exact=True` for each, count 5).
- **A5 — false provenance / duplicate authority.** Pinned files equal upstream v7.1 tag commit (identity.txt), and
  no other file in the tree writes or names the record; there is no second format authority to contradict.
- **A6 — "the filesystem UUID".** The value written is `uuid_unparse(spc->fi->fsid, fsid)` (scrub.c:1025, buffer
  scrub.c:999), and the reader `uuid_parse`s a 36-char field (scrub.c:683-686): a filesystem UUID, not a devid and
  not a human string.
- **A7 — "error sums" as an inference stated as fact.** It is the code: `_SCRUB_SUM` (scrub.c:795-796) writes
  resumed-total + current for each error counter, per device (scrub.c:806-820).

## Optional strengthening (no defect; no replacement text)

The literal value `"1"` lives at scrub.c:70, which no SC2 Quote line names; :856 shows the concatenation and :69
the prefix. No sentence is false or overreaching, so nothing needs replacing. If wanted, the cheap strengthening is
a prose cite of `scrub.c:70 SCRUB_FILE_VERSION "1"` — a Quote there would fall outside SC2's counter window
(826-895), so prose is the lower-risk form.

## Adjacent observation (not part of this row's verdict; SC4/triage territory)

With no record at all, this host's `btrfs scrub status /` prints `Error summary:    no errors found` (`probes.txt`):
`add_to_fs_stat` sums per-device statistics (scrub.c:282-300) and the summary prints " no errors found" when the
counts are zero (scrub.c:238-249). An absent record therefore reads as zero errors on that line. That bears on the
triage bullet at entry:148-149, not on SC2.

## What I did not do

- Did not produce a record with the real writer (that needs `btrfs scrub start`, forbidden by the host guard); the
  format is proven from the write path and exercised through the shipped reader.
- Did not run `tools/check-scrub-record-r42.py` (it judges the tree, costs minutes, and belongs to other seats) and
  did not read SC1/SC3/SC4/SC5 for verdicts.
- Did not test a multi-device record (this filesystem has one device), so "per-device" is demonstrated for device
  id 1 plus the loop structure that writes one line per `n` devices.
- No tool installed or upgraded. `btrfs scrub status` on the host was read-only; crafted records were read inside
  private `unshare -rm` namespaces; no host path, lane file or index was written.
- Receipts: `.ufo/waves/round-42/w2/C2CritSC2/` — `identity.txt`, `quote-order.txt`, `probes.txt`, `rec_ok`,
  `rec_reorder`, `rec_v2`, `rec_tail`. Scratch `/fast/scratch/hyaku/tsukuroi-r42/C2CritSC2` removed after the
  receipts were copied.
