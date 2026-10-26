VERDICT: supports (the L1 reject of F1 is right: the device id IS emitted, so "resume never engages for self-written records" is false)

Seat C2CritRejectF1 (item C2-F6) — attack on the integrator's rejection of wave-1 F1
(`w1/C2DraftCritSR3.md` F1) at `corpus/lessons/round-43.md:58-62`. Source of truth: S237 =
`.ufo/waves/round-42/frozen/src/scrub.c` (sha256 `48df2e2f…0801`, verified before compiling). The
reject stands. F1's operative claim and both of its consequential claims are false; only incidental
code-mechanics sentences in F1 are true, and none of them is a defect.

## 1. The reject is correct

F1's key sentence: "`scrub_writev` (782-793) formats the devid into `buf` and returns
`scrub_write_buf(fd, buf, len)` … so the chain proceeds and `scrub_write_buf(fd, buf, 0)` writes 0
bytes. The device id is never emitted". That reads `scrub_writev` as format-only. It is not:
`scrub_writev` performs the write itself and returns its result (scrub.c:788-792):

```
	        ret = vsnprintf(buf, max, fmt, args);
	        …
	        if (ret >= max)
	                return ret - max;
	        return scrub_write_buf(fd, buf, ret);
```

So in `scrub_write_file`'s chain (scrub.c:865-869)

```
	        if (scrub_write_buf(fd, fsid, strlen(fsid)) ||
	            scrub_write_buf(fd, ":", 1) ||
	            scrub_writev(fd, buf, sizeof(buf), "%lld",
	                        use->scrub_args.devid) ||
	            scrub_write_buf(fd, buf, ret) ||
```

the `scrub_writev` call writes the devid digits into the file and returns 0 on success; the trailing
`scrub_write_buf(fd, buf, ret)` then writes 0 bytes — `ret` is 0 (initialised at :846; the header
write at :856-859 succeeded), so it is a harmless no-op, exactly as the L1 stated. The record line is
`<fsid>:<devid>|data_extents_scrubbed:…|…`, not `<fsid>:|…`.

## 2. Independent round-trip from the frozen file (stubs only)

Built in scratch (`/fast/scratch/hyaku/tsukuroi-r43/C2CritRejectF1/`, removed after copying
receipts): `gen.py` slices the verbatim line-ranges 67-70, 72-110, 402-410, 538-567, 569-576,
578-771, 773-793, 795-841, 843-895 out of S237 (verified: all chunks byte-identical; generated
`harness.c` reproduces byte-identical from `gen.py`), then compiles with stub-only preamble
(`__u64`/`u64` typedefs, UAPI structs, `warning`/`error`, `fallthrough`, `libuuid`). Driver writes
two single-device records through the verbatim `scrub_write_file` — one fresh (`resumed=NULL`), one
resumed (`sp.resumed` set, `skip=0`, so `scrub_resumed_stats` returns the local `dest`) — then reads
the file back through the verbatim `scrub_read_file` (report_errors=1) and runs the resume-selection
predicate verbatim from `scrub_start` (scrub.c:1427-1438). fsid `1d02a454-c549-4a35-b567-89d60902af8e`
(root fsid, S241 capture.txt:5), devid 1 (root devid, capture.txt:6).

Observed (`run.log`):

```
RAW RECORD (744 bytes):
scrub status:1
1d02a454-c549-4a35-b567-89d60902af8e:1|data_extents_scrubbed:11|…|last_physical:44|t_start:1000|t_resumed:1001|duration:5|canceled:0|finished:0
scrub status:1
1d02a454-c549-4a35-b567-89d60902af8e:1|data_extents_scrubbed:177|…|last_physical:1234|t_start:1500|t_resumed:2000|duration:10|canceled:0|finished:0
PARSED record[0]: … devid=1 … data_extents=11 … last_physical=44 t_start=1000 t_resumed=1001 duration=5 canceled=0 finished=0
PARSED record[1]: … devid=1 … data_extents=177 … last_physical=1234 t_start=1500 t_resumed=2000 duration=10 canceled=0 finished=0
records=2 warnings=1 errors=0
RESUME-SELECT: device devid=1 selected, resumed start=last_physical=44
n_resume=1
```

- Both written lines carry the devid digits after the colon (`:1|`) — fresh path and resumed path
  alike (the resumed path's devid is the copy at scrub.c:826).
- The reader parses `devid=1` from both; neither record line produced a warning. The single
  `invalid data on line 2 pos 370 state 3` warning is an artifact of MY harness appending a second
  `scrub status:1` header line (two `scrub_write_file` calls into one file); the real writer emits
  one header per file. So the "warnings occur for every self-written record" claim is false for
  clean records (and matches C2ExecTailRepro's clean controls: 0 warnings).
- The resumed record parses as `data_extents=177 (100+77)`, `t_start=1500` (old record),
  `t_resumed=2000` (= new run's `t_start`), `duration=10 (3+7)`, `last_physical=1234` (new run) —
  exactly what SR3's standing sentence describes; the resume-selection predicate on the parsed
  self-written record selects the device and sets `start=last_physical`. SR3's resume sentences are
  reachable with self-written records.

## 3. What in F1 is still right

- `ret` is 0 at the no-op `scrub_write_buf(fd, buf, ret)` (scrub.c:869) — true, and harmless.
- The reader state machine demands ≥1 digit after the fsid colon: `if (j == 0 || i + j + 1 >= avail)
  _SCRUB_INVALID;` (scrub.c:695-696) — true as a parser property; if a devid were missing the line
  would be dropped. But the writer never produces such a line.
- `last_dev_scrub` matches `past_scrubs[i]->devid == devid` exactly (scrub.c:1144-1146) and real
  btrfs devids are ≥1 (S241 capture.txt:6) — true; the premise "parsed records all carry devid 0"
  is false for self-written records.
- `nothing_to_resume` → exit 2 (scrub.c:1452-1457, 1727-1728) — exists, but is not reached by
  self-written records in the normal case.
- F1's upstream-provenance section (frozen sha256 = upstream v7.1, fetched 2026-10-26) is not part
  of the rejected claim and remains valid as provenance.

## 4. What in F1 is false

- "The device id is never emitted" — false (verified above).
- "every line written is `<fsid>:|data_extents_scrubbed:<n>|…` (no devid digits after the colon)" —
  false; the observed lines contain `:1|`.
- "parsed records all carry devid 0 while real device ids are >=1" — false; parsed devid=1.
- "`last_scrub` is NULL for every device … resume never engages for self-written records" — false;
  the selection predicate engages on the parsed record.
- "This also narrows SR1's tail explanation: `invalid data on line` warnings occur for every
  self-written record even with no trailing bytes" — false; clean self-written record lines produce 0
  warnings (this run; C2ExecTailRepro controls).

## 5. Minor note (not a defect)

The lesson's rejection note cites the no-op as `:868`; in S237 it is line 869
(`scrub_write_buf(fd, buf, ret) ||`; :867-868 are the `scrub_writev` call). Cosmetic only; the
substance of the reject is exact.

## 6. Method, limits, housekeeping

- No host mutation: no `btrfs` command, no ioctl, no `/var/lib/btrfs`, `/etc`, service, package,
  sysfs or mount change; no `git`/`jj` mutation; no installs (`gcc`, `libuuid`, `python3` were
  present). No counter runs. No subagents (leaf seat).
- Scratch used `/fast/scratch/hyaku/tsukuroi-r43/C2CritRejectF1/`; receipts copied to
  `.ufo/waves/round-43/w2/C2CritRejectF1/` (`harness.c`, `driver.c`, `gen.py`, `record.bin`,
  `run.log`, `build.log`); scratch removed before finishing.
- Not done: I did not run `btrfs scrub start/resume` on a real host (privileged; forbidden), so the
  end-to-end kernel+userspace resume of a real scrub remains unobserved here; the round-trip covers
  the frozen writer+reader+selection code, which is the exact locus of F1.
