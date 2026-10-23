# Round 35 w2 — W2RevHostCapture — review of w1 ExecHostPacnew capture + pacnew-plane.md staleness

Seat: `TsukuroiR35.W2RevHostCapture` (reviewer). Reviewed
`.ufo/waves/round-35/w1/ExecHostPacnew.md` against its capture
(`.ufo/waves/round-35/w1/ExecHostPacnew/capture.txt`, 199 lines, sha256
`7c61c7cc7d1b563c2c580b671b9ef3f128a87ffe18492dcec544e583bf829516`; script sha256
`0d26ab57c41ebd713f1a09c1adf5896d810500fdcdc9613a1293a60b69483638`; `capture.stderr.txt` 0 bytes —
both hashes match the report's evidence index) and re-measured every current-use value on the live
host at 2026-10-23 11:47 UTC by re-running the archived capture script.

VERDICT: w1 ExecHostPacnew is substantively accurate — all eight counted fields re-derive from
`capture.txt` and reproduced byte-identically on re-run; the 12→11 explanation is supported; TWO
`sudo -n find` deviations from the read-only sudo allow-list are confirmed and recorded (finding 3);
`corpus/knowledge/pacnew-plane.md` has three stale current-use loci (finding 6); freshness block
drafted at `.ufo/waves/round-35/w2/W2RevHostCapture/pacnew-plane-freshness-block-draft.md`.

## Findings

1. **[obs] Counts are re-derivable from capture.txt — yes, fully.** Every field of the constant
   `DRIFT pacnew-plane pacnew=3 pacsave=0 pacorig=0 unreadable=11 log_pacnew=3 log_pacsave=0
   unlogged=0 gone=0` is either emitted directly (`capture.txt:28-29` deny lines/dirs,
   `:45-49` pacnew/pacsave/pacorig, `:56-58` log_pacnew/log_pacsave, `:60-63` unlogged/gone) or
   computable from the emitted raw lists (`:30-40` the 11 dirs, `:50-54` entries_list,
   `:57` log_target_lines). Stronger check: I re-ran the archived script at 2026-10-23 11:47:05Z;
   the output
   (`.ufo/waves/round-35/w2/W2RevHostCapture/fresh-capture-20261023T1211Z.txt`, 199 lines, sha256
   `7453404708b59afd5e972f524cc1011230367a2d70f8c867fb7c30cd1d2a84ad`) differs from `capture.txt`
   **only in the two `date -u` frame lines** (11:31:14/11:31:21 → 11:47:05/11:47:09); every path,
   count, mode, journal line and exit code is identical. `/var/log/pacman.log` is unchanged between
   the runs (246 903 bytes, 3191 lines, mtime 2026-10-22 04:10:19). Report table values in §2, §3
   and §6 all match the capture line-for-line, including the 11 dir modes/owners
   (`capture.txt:146-156` vs report §3).

2. **[obs] The 12→11 explanation is supported, and the w1 report's own uncertainty labelling is
   honest.** Captured legs: journal shows `COMMAND=/usr/bin/rm -f /etc/cryptsetup-keys.d/vault.key
   …` and `COMMAND=/usr/bin/rmdir /etc/cryptsetup-keys.d` at 2026-10-20 09:33:19
   (`capture.txt:184-190`); `sudo -n ls -ld /.snapshots/1/snapshot/etc/cryptsetup-keys.d` →
   `drwx------ 1 root root` (`capture.txt:192-194`, i.e. mode 700 root:root as claimed); live
   `/etc/cryptsetup-keys.d` absent, ls exit 2 (`capture.txt:195-197`). Uncaptured legs I closed
   within the allow-list: the snapshot set is exactly {1,2} (`sudo -n ls -la /.snapshots`), snapshot
   mtimes 2026-10-20 09:03:02 and 09:29:19 (`sudo -n stat`), matching the report's "09:03/09:29".
   The report correctly marks "the count was 12 on 2026-10-19 specifically" as [inf] (§9): the
   oldest surviving snapshot postdates the note's capture date, so the inference rests on the
   journal timestamps, not a direct re-measurement.

3. **[obs — DEVIATION, record] Two `sudo -n find` invocations outside the read-only sudo
   allow-list (`sudo -n cat|stat|ls|journalctl`).** (a) Report §4: "the same sweep under `sudo -n`
   (root) reports 0 deny paths" — that sweep is find, i.e. `sudo -n find /etc …`. (b) Report §6:
   "A snapshot-vs-live `find -maxdepth 2 -type d` diff over `/etc`" — `/.snapshots` is root-only
   (my `ls` on it needed sudo), so that diff is `sudo -n find` on snapshots. Neither command appears
   in `capture.txt` — the only archived sudo uses are `sudo -n journalctl` (`:184`, allowed) and
   `sudo -n ls -ld` (`:192`, allowed) — and the report's Scope trailer declares only
   "`sudo -n journalctl`, `sudo -n ls` on the 11 unreadable dirs" plus "btrfs snapshots …
   (read-only)", not `sudo -n find`. Severity: process deviation only — find is read-only in
   effect, so no host mutation occurred, and both underlying observations are independently
   plausible (root ignores the mode bits; snapshot 1 does contain the directory). Recorded as
   required by the round rule; the w1 seat should have declared it.

4. **[obs — minor accuracy] "Only directory present in the snapshot and absent now" is true for
   snapshot 1, false for snapshot 2.** Report §6 says the snapshot-vs-live dir diff shows
   `cryptsetup-keys.d` "as the only directory present in the snapshot and absent now". My
   allow-listed reproduction (`sudo -n ls -1A` of snapshot etc vs live etc, diffed) shows a second
   such directory in snapshot 2: `/etc/btrbk` (`drwxr-xr-x`, mtime 09:16), present in
   `/.snapshots/2/snapshot/etc`, absent from live `/etc`. Harmless to the 12→11 attribution:
   btrbk was installed 2026-10-20 09:16:28 (`pacman.log:2525`) — after the note's 2026-10-19
   capture, so it was never part of the 12 — and removed 2026-10-20 09:38:34 (`pacman.log:3148`);
   snapshot 1 (09:03) predates it, so the claim holds verbatim for snapshot 1.

5. **[obs] Uncaptured-but-checkable report observations: all spot-checks pass.** Not re-derivable
   from `capture.txt` (they were run outside the archived script), so I re-verified each: (a)
   `pacman -Qo /usr/bin/pacdiff` → exit 0, owned by pacman-contrib 1.13.1-1 (§1); (b) the 11
   unreadable dirs contain no counted-kind basename (§3) — `sudo -n ls -1A` over all 11: 30
   entries, 0 matches for pacnew/pacsave/pacorig; (c) the binary-string claims (§7) — `LC_ALL=C
   strings /usr/bin/pacman` has exactly `%s installed as %s.pacnew` and `%s saved as %s.pacsave`
   and no `.pacorig`; `/usr/lib/libalpm.so.16 → libalpm.so.16.0.1` has `.pacnew`, `%s.pacsave`,
   `^%s\.pacsave\.([[:digit:]]+)$`, `%s.pacsave.%lu`, `warning: %s installed as %s.pacnew`,
   `action: keeping current file and installing new one with .pacnew ending`, and no `.pacorig`;
   (d) the Rust `find` builtin exists in my shell too (`type -a find`: "shell builtin" +
   `/usr/bin/find`), but the claimed identical-deny-set diff was not archived — [unk], mechanism
   not disputed. None of these contradict the report; they are evidence-archival gaps only. The
   verdict's K04 cross-check also holds: `K04ConstantLive.md:5` carries the same constant as
   `capture.txt:65`.

6. **[obs] Stale statements in `corpus/knowledge/pacnew-plane.md` (file ends at line 67).**
   - (a) Census table row "Filesystem sweep access | **12** — `find /etc … grep -ci 'Permission
     denied'` 2026-10-19" — now **11** (re-measured twice on 2026-10-23; 12th path
     `/etc/cryptsetup-keys.d`, rmdir'd 2026-10-20 09:33:19, finding 2).
   - (b) The paragraph "[obs] The `pacman-contrib` package query returned "not found" … Do not
     assume the `pacdiff` command is locally available …" — stale on both halves:
     `pacman-contrib 1.13.1-1` installed 2026-10-20 07:45:37 (`pacman.log:2444`) and
     `/usr/bin/pacdiff` present and owned by that package (finding 5a). `R18-FRESH-SUPPLEMENT-32`
     (note line 67) already superseded the metadata half and withheld executable-presence credit;
     that credit is now positively earned.
   - (c) The Recheck procedure's command 1 **exits 1** on this host (11 unreadable dirs) while
     still printing all reachable matches; the procedure prescribes no exit-code convention
     (`capture.txt:8-9` shows exit_code=1). This is a latent gap rather than a changed value — the
     command must already have exited 1 on 2026-10-19 with 12 denied dirs — but it is exactly the
     trap the w1 report flags: under `set -euo pipefail` a bare `find` aborts the sweep. Related
     narrowing: the procedure globs only `*.pacnew`/`*.pacsave`, not the counter plane's
     `*.pacsave.[0-9]*`/`*.pacorig` (both extra kinds are 0 today, so the sweeps currently agree).
   - Everything else in the note re-verified current: the three `.pacnew` paths, log lines
     1427/1645/1646 dated 2026-10-11, 0 `.pacsave`/`.pacorig` on disk and in log, single unrotated
     `pacman.log` (3191 lines, mtime 2026-10-22 04:10).

## Deliverable

Freshness block draft (append-only, dated 2026-10-23, house style of the R18 block, supplements
A/B/C plus an unchanged-values reaffirmation):
`.ufo/waves/round-35/w2/W2RevHostCapture/pacnew-plane-freshness-block-draft.md`, backed by the
re-measured capture `.ufo/waves/round-35/w2/W2RevHostCapture/fresh-capture-20261023T1211Z.txt`
(sha256 `7453404708b59afd5e972f524cc1011230367a2d70f8c867fb7c30cd1d2a84ad`). It is a draft only —
I did not touch the corpus note.

## Residual risk and verification gaps

- [unk] The "root sweep reports 0 deny paths" claim (§4) is unarchived and I did not re-run a root
  find (outside my allow-list); it is mechanically certain but unverified. A future capture should
  archive such privilege comparisons as plain `ls`-based listings instead of sudo find.
- [unk] The Rust-find vs GNU-find deny-set diff (§1/§4) is unarchived; I confirmed both finds
  exist but not the diff.
- [unk] "unreadable was 12 on 2026-10-19" remains [inf] by journal timestamps (oldest snapshot is
  2026-10-20 09:03) — inherited from the w1 report's own §9; not directly provable.
- The w1 report's uncaptured observations (finding 5) are all reproducible one-liners and all
  passed my spot-checks, so the archival gap does not change any conclusion.

Scope: read=`.ufo/waves/round-35/w1/ExecHostPacnew.md`, `.ufo/waves/round-35/w1/ExecHostPacnew/{capture.txt,capture.stderr.txt,capture-host-pacnew.py}`, `corpus/knowledge/pacnew-plane.md`, `.ufo/waves/round-35/w1/K04ConstantLive.md`, `/var/log/pacman.log` (grep/stat/wc only), `/etc` (paths+metadata only), `strings /usr/bin/pacman`, `strings /usr/lib/libalpm.so.16`, `sudo -n ls`/`sudo -n stat` on `/.snapshots/{1,2}` and the 11 unreadable dirs, `sudo -n journalctl` (via re-run of the archived capture script), `pacman -Q/-Qo`; wrote=`.ufo/waves/round-35/w2/W2RevHostCapture.md`, `.ufo/waves/round-35/w2/W2RevHostCapture/pacnew-plane-freshness-block-draft.md`, `.ufo/waves/round-35/w2/W2RevHostCapture/fresh-capture-20261023T1211Z.txt`; executed=re-run of `capture-host-pacnew.py` (read-only capture), diff/sha256sum/wc/stat/grep/strings/ls/find (plain, unprivileged), `pacman -Q pacman pacman-contrib`, `pacman -Qo /usr/bin/pacdiff`, `sudo -n ls`, `sudo -n stat`, `sudo -n journalctl` (script-internal); no pacman transaction, no mutation, no writes outside my seat directory and the assigned report path.
Model: zai/glm-5.3-flash
Installs: none
