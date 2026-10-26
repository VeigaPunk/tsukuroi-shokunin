ROW SC4 FIRST-READ: holds

Seat: C2DraftRevSC4 (wave-1 first falsifier, not a counted verdict)
Item: C2-SC4 — row SC4 of corpus/knowledge/btrfs-scrub-record-r42.md at f50c28d83e1832ecd7eba765caace531f45d6b27 vs pinned snapshot + live source + host capture.
Review date: 2026-10-26.

## Pinning verification (all passed)

- `cd .ufo/waves/round-42/frozen/src && sha256sum -c SHA256SUMS` → `scrub.c: OK`, `CHANGES: OK`
  (scrub.c 48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801, CHANGES bd881ab899ba4f4fba820207c4cb671eacbb34843db4cf95fd7d90aaff2a0d22).
- Live `https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/cmds/scrub.c` fetched 2026-10-26 (curl -sSfL):
  sha256 48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801, `cmp` with snapshot → IDENTICAL.
  Live CHANGES also fetched: bd881ab8… identical to snapshot. FETCH.txt's peeled-commit claim (4ab0e80b…) not
  re-derived; the raw-tag URLs are the pin and both match byte-for-byte.
- Host capture digest: `sha256sum .ufo/waves/round-42/frozen/hostcap/capture.txt` → 942edc91a6b8fcda3ef29e88c3d54e7a9a48ec4cce302b8c1edcc89c8710643c,
  equal to the digest in the entry header (entry.md:2).
- No drift: `git diff --stat f50c28d8..HEAD -- corpus/knowledge/btrfs-scrub-record-r42.md` is empty; the reviewed
  row is the current row.
- Counter context (frozen, unchanged): tools/check-scrub-record-r42.py sha256 dbe933ec8c2cca491346da76bbc104aba8ff9e5486f4dcaf572e59df3680503f
  (matches the declared digest); its SC4 check is token `_SCRUB_FS_STAT_MIN` over windows scrub.c 280–330 and
  1925–1945 (check-scrub-record-r42.py:60) — both windows fully inside what I reviewed.

## Quote verification (7/7 exact, line and text)

All against the snapshot .ufo/waves/round-42/frozen/src/scrub.c (= live v7.1, digest above):

| Entry quote | Snapshot line | Verdict |
|---|---|---|
| scrub.c:1931 `if (fdres < 0 && fdres != -ENOENT) {` | 1931 | exact (twin occurrence at 1362, in the start path) |
| scrub.c:300 `_SCRUB_FS_STAT_ZMIN(ss, t_start, fs_stat);` | 300 | exact |
| scrub.c:303 `_SCRUB_FS_STAT_ZMAX(ss, canceled, fs_stat);` | 303 | exact |
| scrub.c:304 `_SCRUB_FS_STAT_MIN(ss, finished, fs_stat);` | 304 | exact |
| scrub.c:310 `fs_stat->s.finished = 1;` | 310 | exact |
| scrub.c:321 `pr_default("\tno stats available\n");` | 321 | exact |
| scrub.c:342 `(ss->canceled ? "aborted" :` | 342 | exact |

All seven lines lie inside the item's stated ranges (280–345, 1920–2000). grep -n -F was the locator; every hit
above is the first and only occurrence at that line.

## Statement, sentence by sentence

1. "Missing record as no history; ENOENT not an error; any other open failure prints a warning." —
   Verified. cmd_scrub_status: socket connect fails → `scrub_open_file_r(SCRUB_DATA_FILE, fsid)` (scrub.c:1930);
   open failure other than -ENOENT → `warning("failed to open status file: %m")` and `err = 1` (1931–1936);
   ENOENT → fdres stays negative, `past_scrubs` stays NULL, both print modes degrade to `no stats available`
   (1955–1960 per device with ss=NULL; 1973–1996 summary folds nothing). `scrub_open_file_r` → `scrub_open_file`
   (497–505), so open and flock failures surface as one negative errno — the lock-held reader (EWOULDBLOCK) is a
   non-ENOENT failure and warns. Same ENOENT tolerance exists in the start path (1361–1370); the row attributes it
   to `status` and cites the `status` occurrence, which is correct and not exclusive.

2. Fold semantics — Verified. `add_to_fs_stat` (284–307): ZMIN t_start (300; macro 268–273 replaces whenever the
   accumulator is 0 or larger — "an unset value is always replaced" is exact); ZMAX canceled (303; macro 275–280,
   starts 0, so any canceled device sets it); MIN finished (304; macro 261–266) from `init_fs_stat`
   `fs_stat->s.finished = 1` (308–312) — so finished survives only if every folded device record has finished=1.
   The summary fold runs per device over `last_dev_scrub(past_scrubs, devid)` (1981–1986).

3. Status words and "no stats available" — Verified. The ternary at 340–345 is exactly
   `in_progress ? "running" : canceled ? "aborted" : finished ? "finished" : "interrupted"`, in both per-device
   (`print_scrub_dev` → `_print_scrub_ss`, 348–353) and summary mode (`print_fs_stat` calls
   `_print_scrub_ss(&fs_stat->s)`, 384–388), so "the summary prints no stats available instead" is right
   (`!ss || !ss->t_start` → 321, return). `in_progress` comes from `is_scrub_running_in_kernel` (1946, 1957),
   which issues `BTRFS_IOC_SCRUB_PROGRESS` per device and returns 1 on the first success (1190–1208) — "the
   kernel reports a scrub in progress" is a fair reading of that predicate.

4. "interrupted means unfinished record with nothing running now … not a device error." — Verified, and
   corroborated by upstream's own words: the start path calls the same state "stale information in the status
   file, ie. if it's canceled=0, finished=0 but no scrub is running" (1372–1378) and forces a re-check; the
   1379–1385 comment explains that an unchecked second start would otherwise produce "the state 'aborted' without
   the explanation that a scrub was already running" — i.e. `aborted` is a run-state word, not a fault verdict,
   exactly as the row reads it. The row's example (recorder process gone before the scrub ended) is the precise
   scenario of that stale-state comment.

Host reading — Verified as far as it claims. capture.txt:6 is `var_lib_btrfs absent`; from the code above a status
run on that root would take the ENOENT branch, fold nothing, init t_start=0, and print `no stats available`
(319–322, 308–312). The row honestly states the command itself was not run. The prediction is code-derived, not
executed — correct method, and it says so.

## Findings

No sentence of the Statement is false; no quote is misplaced. Three precision notes, none falsifying:

- F1 (minor, underreach). Statement sentence 1: "any other open failure prints a warning" — the command also
  fails (scrub.c:1935–1936: `err = 1; goto out;`, exit 1). True but incomplete; a triager should know the command
  errors out rather than degrading. Exact replacement:
  "any other open failure prints a warning and the command exits with an error".
- F2 (minor, quantifier). Statement sentence 2: "counts as finished only if every device's record is finished" —
  devices with no record in the file are skipped in the fold (scrub.c:1981–1986 `if (!last_scrub) continue;`), so
  the quantifier is over devices that have a record; a filesystem summary can print `finished` while a device
  added after the last scrub has no line at all. Exact replacement:
  "and it counts as finished only if every device that has a record in the file is finished (the flag starts at 1
  and takes the minimum, `_SCRUB_FS_STAT_MIN`; devices without a record are skipped)". The same tightening applies
  to the "How this changes OS triage" bullet "a filesystem `finished` needs every device finished" (entry.md:132)
  — it means every device with a record.
- F3 (note, no replacement demanded). "running" is keyed on the PROGRESS ioctl succeeding (1190–1208); userspace
  treats ENOTCONN/ENODEV as not-running (1050–1056). A paused scrub keeps its kernel context, so `scrub status`
  would print `running` for it [INFERENCE — kernel-side behaviour, not checked here; no kernel source is pinned in
  frozen/src]. If the L1 wants this nailed, pin the kernel's scrub ioctl behaviour or add "active (running or
  paused)" wording.

## Residual risk and what I did not do

- I did not compile or execute scrub.c, did not run `btrfs scrub status` (host guard: read-only, and the row says
  the same), and did not compare Arch's 7.1-1 packaging patches against upstream (that is the declared wave item
  in the entry's Limits, entry.md:146–147).
- F3 is left as marked inference, not verified against kernel source.
- FETCH.txt's `git ls-remote` peeled commit was not re-derived; verification is byte-level against the raw tag
  URLs, which is what the entry's recheck instructs.
- Scratch /fast/scratch/hyaku/tsukuroi-r42/C2DraftRevSC4 (fetched live copies, entry extract) removed after this
  report; no tool installs were needed.
