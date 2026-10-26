VERDICT: supports

Seat: SrcReopenS241 (w2 falsify, item C2-F4: S241 re-open).

## 1. Rerun of capture.sh vs frozen capture.txt (timestamps excepted)

Command (unprivileged, uid 1000, rc 0):
```
bash /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-43/frozen/hostcap/capture.sh \
  /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-43/w2/SrcReopenS241/capture-rerun.txt
```
Receipt: `.ufo/waves/round-43/w2/SrcReopenS241/capture-rerun.txt` (13 lines; sha256
295e93d9a26ed20b4a3b5beb59dcae0c5017bcff12e88994c772a6308c60c428).

`diff` frozen capture.txt vs rerun: exactly two lines differ.
- Line 1 (timestamp, excepted): `captured_utc 2026-10-26T21:51:26Z` → `captured_utc 2026-10-26T22:55:47Z`.
- Line 11: `scrub_status| Total to scrub: 309.39GiB` → `scrub_status| Total to scrub: 309.76GiB`.

The line-11 delta is environmental, not a probe change: in `cmd_scrub_status` (no `-d`), the summary's `bytes_total`
is the filesystem used-bytes sum, `total_bytes_used += sp->used_bytes * factor` (scrub.c:1988-1995), passed to
`print_fs_stat` → `print_scrub_summary`, which prints it as "Total to scrub" (scrub.c:205-206; per-device comment
"we use device's used bytes instead" at scrub.c:369-373). Used bytes grew ~0.37 GiB between the two runs; it is not a
quoted cell and does not change any adopted sentence. All other 11 lines byte-identical.

## 2. S241 Gate quotes (lessons round-43.md:20) located in both captures

`grep -n -F` over both files, each quote located at the named capture.txt line:
- `scrub_progress_ioctl devid=1 errno=EPERM (1)` → frozen:6, rerun:6 (full line equals quote).
- `uid 1000 euid_caps 0000000000000000` → frozen:2, rerun:2 (full line equals quote).
- `no stats available` → frozen:10, rerun:10 (substring of `scrub_status| \tno stats available`).
All three ≤25 words, verbatim, and stable across the re-open.

## 3. SOURCES.md S241 row (line 250, header line 5) — verdict per cell

| cell | value | verdict |
|---|---|---|
| id | S241 | holds |
| source | Round-43 host scrub-ioctl capture — `.ufo/waves/round-43/frozen/hostcap/` (own-work) | holds (capture.sh, capture.txt present) |
| kind | own-work | holds (produced by lane's own capture script) |
| tier | A | holds (admitted at entry; lessons:34 "new rows"; SR6 admit per lessons:131) |
| scope | What an unprivileged scrub-progress ioctl and scrub status return on this host at capture time | holds (capture records exactly this; time-bound wording correct) |
| anchor | capture.sh and capture.txt (sha256 f7ecbe7c990e68d7b0dbdbd8bfe65f3acd1cbbdabe33d47e71a6f1ae1242c556), captured 2026-10-26T21:51:26Z, uid 1000 | holds (computed sha256 of frozen capture.txt equals the full digest; `captured_utc` line 1 and uid line 2 match) |
| teaches | For uid 1000 the scrub-progress ioctl on the root filesystem fails with EPERM and scrub status prints no stats available | holds (capture.txt:6 EPERM, :10 no stats available, :8 exit 0; reproduced in rerun) |
| status | mined | holds (consistent with lessons:34 and counter `sources_ok`) |
| opened | 2026-10-26 | holds |
| recheck | 30d | holds (matches sibling own-work rows S218/S225/S236/S239; record's recheck line prescribes the exact rerun performed) |
| used-by | corpus/knowledge/btrfs-scrub-record-r43.md | holds (record `source:` line names S237 S240 S241; SR6 Host reading cites capture.txt:2,:6,:7,:8,:10; SR1/SR3 host readings cite :7) |

Frozen counter `tools/check-scrub-record-r43.py --revision 8acf0b022586a0f3164c77659fb96ba5f90949b6 --lane <lane>`
(exit 1, "Writes nothing" per its docstring): `rows 3, quotes_ok 3, props_ok 3, host_ok 3, sources_ok 1,
novelty_base_hits 0, pointer_ok 1, snapshots_ok true, capture_ok true, sources {S237,S240,S241,source_line} all true,
verdicts_ok 0` (all six C2RevSR<n>/C2CritSR<n> votes unbound — this wave's counted seats; sole FAIL cause).
`transcripts_bound 0` is host-local, reported outside the predicate.

## 4. capture.sh review (does it do exactly what its header says and nothing else?)

Read: `.ufo/waves/round-43/frozen/hostcap/capture.sh` (sha256 77ffeecb4955a36324efa45d8c07b03d7879ed232cf3cd4d20aea9cb36d2a1a9, claim 77ffeecb…a1a9 ✓).
- State: `set -u`; `out=${1:?…}`; the whole payload is one `{ … } >"$out"` block. Nothing is written outside `$out`
  — no mkdir, no /var/lib/btrfs touch, no /etc, no services, no sudo, no pacman transactions (`pacman -Q` is a
  read-only query). Header promise "Nothing is written outside <out-file>" holds.
- The two behaviors the header names are present and correct: (a) the kernel scrub-progress ioctl probe on `/`
  (`O_RDONLY|O_DIRECTORY`, `BTRFS_IOC_SCRUB_PROGRESS`, devid 1, records errno) — REQ `0xC400941D` matches
  `_IOWR(0x94, 29, struct btrfs_ioctl_scrub_args)` with sizeof 1024; header cite "scrub.c is_scrub_running_in_kernel,
  :1189-1205" matches the frozen function extent (scrub.c:1190-1206; ioctl loop 1197-1203); (b) `btrfs scrub status /`
  2>&1 with its exit code and piped lines.
- Under-described extras (read-only metadata, not side effects): `captured_utc`, `uid … euid_caps` (/proc/self/status
  read), `kernel` uname, `btrfs_progs` pacman query, `root_fs` findmnt, and a `var_lib_btrfs` presence stat. These
  are not named in the header prose; they are all unprivileged and read-only, and two of them (capture.txt:2, :7) are
  themselves adopted cells. Observation, not a defect: the header could list them, but no claim depends on their absence.
- Unprivileged/read-only confirmed: probe is the host-guard-sanctioned read-only ioctl; no other btrfs ioctl used.

## 5. Boundaries / not done

Did not run any `btrfs scrub start/cancel/resume/limit -l`, `btrfs device stats -z`, or any other btrfs ioctl; no
sudo; no lane/fleet mutations (only the seat's own report and capture-rerun.txt receipt were written); no tools
installed (none needed); no subagents. Scratch `/fast/scratch/hyaku/tsukuroi-r43/SrcReopenS241/` removed on finish.
