ROW SC3 VERDICT: fails

# C2CritSC3 — row SC3, adversarial read (round 42, w2, item V-3b)

Lane tip read: `a968393c678171f8a5a2907da5015735396da4cc`. Row text = `corpus/knowledge/btrfs-scrub-record-r42.md:64-89`;
`git diff 78abb8b5 HEAD -- corpus/knowledge/btrfs-scrub-record-r42.md` is empty, and the file carries no
`Corrections` section, so this is the integrated text with nothing appended.

Frozen evidence, verified first:
- `sha256sum -c SHA256SUMS` in `.ufo/waves/round-42/frozen/src` → `scrub.c: OK`, `CHANGES: OK`
  (`.ufo/waves/round-42/w2/C2CritSC3/probes.txt` §1).
- `capture.txt` sha256 `942edc91…10643c` = the digest in the doc header (receipt §2).
- All five SC3 quote lines resolve as exact substrings on the named lines (`scrub.c:1502,1336,1507,1121,1200`;
  receipt §3). No quote is misattributed.
- Host probes re-run read-only; the capture reproduces (receipt §4).

Two defects. F1 is a false sentence; F2 is a universal the code does not support. F1 alone decides the verdict.

---

## F1 (false) — "all-zero record … (or is resumed)" is wrong for the resume branch

Row text, `btrfs-scrub-record-r42.md:66-67`:

> The record is written by the userspace `btrfs scrub start` process, not by the kernel: it writes an
> all-zero record when the scrub starts (or is resumed) and progress records while it runs.

The "when the scrub starts" leg is true: `sp` is `calloc`ed (`scrub.c:1402`); on a start the setup loop fills
only `scrub_args.devid/start/end/flags` (`:1428`, `:1441`, `:1445-1446`) plus the limit/ioprio fields, none of
which the record's counters or run fields read, and `stats.t_start` is written only later (`:1558`); the first
write at `:1501-1504` therefore serialises zero counters and zero run fields (only the fsid and device ids are
content). The **"(or is resumed)"** leg is false.

Trace, all in `.ufo/waves/round-42/frozen/src/scrub.c`:

1. `btrfs scrub resume` runs the same body: `:1831-1834` `return scrub_start(cmd, argc, argv, true);`.
2. On resume the previous record is attached to the device before the write: `:1427`
   `last_scrub = last_dev_scrub(past_scrubs, devid);` (past_scrubs read from the record file at
   `:1361-1366`), then `:1430-1434` `sp[i].resumed = last_scrub;` for a device whose prior record is
   canceled-or-unfinished.
3. The first write passes those structs: `:1501-1504` `scrub_write_progress(&spc_write_mutex, fsid, sp, fi_args.num_devices)`
   → `:922` `scrub_write_file(fd, fsid, data, n)`.
4. The writer *applies the resumed sums itself*: `:864` `use = scrub_resumed_stats(&data[i], &local);`,
   `:803-804` returns the summed struct when `resumed && !skip`, and `:795-796`
   `_SCRUB_SUM(dest, data, name)` is `dest->scrub_args.progress.name = data->resumed->p.name + data->scrub_args.progress.name`.
   Run fields come from the old record too: `:823` `dest->stats.t_start = data->resumed->stats.t_start;`,
   `:824` duration = old + new.

So the record written at the start of a resume carries the interrupted run's counters, its original `t_start`
and its accumulated duration — a continuation, not zeros. Only device lines with `skip == 1` (devices with no
unfinished record, `:1435-1438`) serialise as zeros, and on a single-device filesystem (this host, capture
`root_fsid 1d02a454…`, one btrfs filesystem per `findmnt`) a resume that proceeds cannot have one.

Why it is not cosmetic: the row's own triage bullet says to read the error sums in the per-device lines. Under
the row's text a reader would treat the counters after a resume as reset and undercount `read_errors` /
`corrected_errors` / `uncorrectable_errors` accumulated before the interruption; `t_start` in a resumed record
is the original start, not the resume moment.

Origin (not the seat's business to fix, but the lane should know): w1 `C2DraftRevSC3.md:15` and `:52` read
`scrub.c:1549-1553` as restoring the resumed stats before the write. That block is the `if (sp[i].skip)` branch
(`:1548-1555`) and *copies into `sp[i]`* for the final write; the resumed sums that matter for the record are
applied inside `scrub_write_file` at `:864`, which both reviewers missed.

**Exact replacement** for `:66-67`, first sentence:

> The record is written by the userspace `btrfs scrub start` process (the same code serves `btrfs scrub
> resume`), not by the kernel: on a start it writes an all-zero record, on a resume the first record it writes
> already carries the interrupted record's counters, original start time and accumulated duration (the resumed
> sums applied in `scrub_write_file`, scrub.c:795-796 and :823 at :864), and while the scrub runs it writes
> progress records.

---

## F2 (universal the code does not support) — "only the final write reports a failure"

Row text, `btrfs-scrub-record-r42.md:70-72`:

> A record-write failure later in the run ends the progress writes without that warning; only the final write
> reports a failure ("failed to record the result").

The first clause is true: a failing progress write exits the thread (`:1123-1126` `if (ret) goto out;`) and
`:1133` returns `ERR_PTR(ret)`, so no further progress records are written; `do_record` stays true, so the
final write is still attempted (`:1701-1703`). The second clause is false in two ways.

1. There is a second report of exactly that failure. The main path joins the progress thread
   (`:1685-1687`) and prints its error: `:1696-1698`
   `if (do_print && terr && terr != PTHREAD_CANCELED) { … error("recording progress failed: %m"); }`.
   `terr` is the `ERR_PTR` the thread returned from the failed record write, so a mid-run record-write failure
   is reported — under a different message, not silently.
2. The final write's own message is conditional, not general: `:1704` `if (ret && do_print)`. `do_print` is
   false by default (`:1249`) and set only for foreground `-B` (`:1295`; suppressed again by quiet at
   `:1332-1333`). In the default background mode (`scrub.c:1512-1529`) the child inherits `do_print == false`,
   so *neither* of those two messages is printed; the first-write warning at `:1507` is not gated on
   `do_print` and does reach stderr, but what follows from it — the final write being skipped at `:1701` — is
   never reported in that mode.

Also worth fixing in the same sentence: neither report changes the exit status — `:1701-1707` sets no error
flag, and the command returns 0 at `:1725-1736` when the record write is the only failure. A scrub that lost
its record looks successful to a script.

**Exact replacement** for `:70-72`:

> A record-write failure later in the run ends the progress writes without that "status recording disabled"
> warning: the progress thread returns the error and the start process reports it as "recording progress
> failed" (scrub.c:1696-1698), while the final write, if it also fails, is reported as "failed to record the
> result" (scrub.c:1704-1706). Both messages print only in foreground mode (-B; `do_print` is false by default
> at scrub.c:1249 and set at :1295), and neither changes the exit status (scrub.c:1701-1707, :1725), so a
> scrub whose recording failed exits 0.

---

## F3 (scope overreach in the Host reading; the inferred fact is one this seat verified, so not a defect of truth)

Row text, `:86-89`:

> No scrub timer is enabled (`btrfs-scrub@.timer disabled`, capture.txt:8; no `btrfs-scrub@*` timer listed,
> capture.txt:7) and the current boot's kernel log holds no `scrub: started` or `scrub: finished` line
> (capture.txt:10); together with the absent directory (capture.txt:6) nothing on this host records a scrub,
> which is weaker than "no scrub ran" (this row).

- The conclusion is true on this host, and I checked it harder than the row did: `journalctl --list-boots`
  shows five retained boots (-4…0, the journal is persistent — `/var/log/journal` exists); across **all** of
  them the only line matching `scrub` is an XFS feature line
  (`SGI XFS with ACLs, security attributes, realtime, scrub, repair, quota…`), and
  `scrub: (started|finished)` matches 0 lines in every boot. `journalctl` is readable as this user
  (stderr empty on every query, and the all-boot `scrub` query returned a real kernel line), so the 0 is a
  real absence, not a permission artifact (receipt §4).
- But the capture proves the claim for the current boot only; "nothing on this host records a scrub" is a
  host-wide universal drawn from `-b 0` plus an absent directory. Held only because no earlier retained boot
  has a scrub line and the journal has not rotated those boots away — evidence the row does not carry.
- `capture.txt:8` is the *template* unit's own state (`btrfs-scrub@.timer disabled disabled`); a template's
  state says nothing about instances (compare `user@.service static -` with an active `user@1000.service`,
  receipt §5). The direct instance evidence exists and is stronger: `systemctl is-enabled
  'btrfs-scrub@-.timer' 'btrfs-scrub@1d02a454-c549-4a35-b567-89d60902af8e.timer'` → `disabled`, `disabled`,
  and `systemctl list-timers --all 'btrfs-scrub@*'` → 0 lines. The row's conclusion stands; the citation order
  invites a reader to over-trust a non-probative line.

**Exact replacement** for `:86-89`:

> No scrub timer exists or is enabled (no `btrfs-scrub@*` timer listed, capture.txt:7; the checked instances
> `btrfs-scrub@-.timer` and `btrfs-scrub@<fsid>.timer` report `disabled`, and capture.txt:8 is the template's
> own state, which says nothing about instances), and the current boot's kernel log holds no `scrub: started`
> or `scrub: finished` line (capture.txt:10); together with the absent directory (capture.txt:6) nothing
> retained on this host records a scrub — weaker than "no scrub ran" (this row).

---

## Per-sentence disposition (Statement `:66-74`, Host reading `:86-89`)

| # | Sentence (paraphrase) | Support | Contradiction |
|---|---|---|---|
| S1a | record written by userspace `btrfs scrub start`, not the kernel | `:1501-1504`, `:1701-1703`; the only record writers are those two `scrub_write_progress` calls, which open the `_tmp` sibling at `:917` and rename it at `:925` | — |
| S1b | all-zero record **on start** | `:1402` calloc, `:1441` start=0, `:1558` t_start set after the write, `:1502` upstream comment | — |
| S1c | all-zero record **on resume** | — | **F1**: `:1831-1834`, `:1427`, `:1430-1434`, `:864`, `:803-804`, `:795-796`, `:823-824` |
| S1d | progress records while it runs | `:1042-1127` (thread, 5 s poll at `:1043`), `:1123-1124`, `:1585` | — |
| S2 | recording off + "status recording disabled" on mkdir fail / first-write fail; scrub still runs | `:1151-1167` (mkdir_p creates every component up to `/var/lib/btrfs`), `:1335-1339`, `:1501-1509`, `:1581`; no `goto out` on either path | — |
| S3 | running asked from kernel via `BTRFS_IOC_SCRUB_PROGRESS`, per device, independent of the file | `:1190-1205`, `:1946` (status), `:1378` (start) | none; `:1392` consults the file only for the "already running" message and only when `force` is unset (`:1378-1379`, kernel result decides) |
| S4a | later failure ends progress writes | `:1121-1126`, `:1131-1133` | — |
| S4b | only the final write reports a failure | `:1704-1706` | **F2**: `:1696-1698` (second report), `:1249`/`:1295` (`do_print`), `:1701-1707`/`:1725` (exit status) |
| S5 | missing record does not prove no scrub ran; ioctl-driven scrub leaves none; labelled `[inference from the write path]` | `:917-925`, `:1503`, `:1701-1703` (only this path writes); the clause is marked as inference, not asserted | — |
| H1 | no scrub timer enabled | `capture.txt:7` (0 timers), `capture.txt:8`; direct instance check in F3 | — |
| H2 | current boot's kernel log has no `scrub: started/finished` | `capture.txt:10`; re-run: 0, exit 0, empty stderr | — |
| H3 | nothing on this host records a scrub | `capture.txt:6`; all-boot scan: 0 btrfs scrub lines | scope: capture is `-b 0` only (F3) |

## Impacted axes

- C2 depth / SC3 row verdict: the row's resume mechanism is wrong in the direction that matters for reading an
  interrupted-then-resumed record's counters and start time.
- The entry's "How this changes OS triage" bullet on reading per-device error sums inherits F1.
- Counter bookkeeping: `tools/check-scrub-record-r42.py:20-22` — "any bound `fails` makes the row not ok" — so
  SC3 cannot pass the w2 predicate until the row text is corrected. Integration and any rewrite belong to the
  L1; this seat wrote no lane content.

## What I did not do

- No scrub was run (`start`/`resume`/`cancel`/`limit -l` untouched, as required), in or out of a namespace; no
  btrfs filesystem was created or mounted; the resume behaviour is established from the pinned source path
  only, not from a live reproduction.
- The binary was not rebuilt; the packaging claim (no patch) is not re-litigated here — it belongs to the
  Limits section, not SC3.
- I did not re-verify SC1, SC2, SC4, SC5, or the counter's other gates.
- No tools installed or upgraded; scratch `/fast/scratch/hyaku/tsukuroi-r42/C2CritSC3` removed at exit.
