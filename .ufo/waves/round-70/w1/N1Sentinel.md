# N1Sentinel — boundary, secret and side-effect sweep (round 70, w1)

Seat: N1Sentinel, round 70 w1. Read-only; no remediation. Base: lane tip `84e013a7` (declaration
`1710bd74` + the L1 health.c snapshot repair). Witness of every number below:
`.ufo/waves/round-70/probes/N1Sentinel/boundary-witness.txt` (generated 2026-11-04T00:12:54Z).

Scope audited: everything under `.ufo/waves/round-70/` present at audit time (`before/`, `after/`,
`w1/`, `probes/`, plus the orchestrator control files `w1-dispatch.json`, `w1-spec.json`,
`w1.ready*`, `w1-run.stderr`, `w1/swarm-registry.json`), the committed declaration and instruments,
and the two repositories' git state. No seat artifact was executed; the only command run against the
lane was the frozen counter itself (below).

## Findings

| # | severity | finding | evidence |
|---|---|---|---|
| F1 | **HIGH** | C1 draft row **XS5** states the `error/` subtree "holds **7** regular files" while its own sentence enumerates **9** (`fail_at_unmount` = 1 + `default`/`EIO`/`ENOSPC`/`ENODEV` × {`max_retries`, `retry_timeout_seconds`}); the host holds **9 per filesystem, 18 total**. A wrong, self-contradictory host fact can land as a rule row: the frozen counter tests token overlap, quote location, source binding and digests — it never tests numeracy (its statement clause needs 3 non-stopword tokens shared with the snapshot, which "error", "files", "metadata" satisfy). | `w1/SC1Entry-note.md:53-58`; `.ufo/waves/round-70/before/host.txt` "error subtree" section (9 lines per fs); live `find /sys/fs/xfs/<dev>/error -type f` = 9 per fs; `probes/E2Capture/host-enum.txt:72-95` (`count_recursive=9`, `sum_recursive=18`) |
| F2 | **MED** | The frozen declaration's host-fact prose §(b) repeats the same wrong count: "error subtree **7** regular files per filesystem". Its own committed capture (`before/host.txt`, committed at `1710bd74`) prints 9 lines per filesystem. This is unlike F1 a *frozen premise* defect: it cannot be amended this round and must be recorded as an erratum while the note states the true 9. It does not falsify the C2 predicate (the predicate binds `error`/`log` to the live enumeration, target 18/8), but a reader who binds "7" mis-audits. | `SCORECARD.md` at `1710bd74`, Round 70 declaration §(b); `before/host.txt`; independent seat flag `w1/E2Capture.md:47-53` |
| F3 | **LOW** | `after/gates.sh` runs `bash tools/tsukuroi-census.sh --selftest` **without `TMPDIR`**; the tool's selftest resolver then falls back to `mktemp`'s default `/tmp` (`tools/tsukuroi-census.sh:2402,2443`) and removes the tree on EXIT (`:2446`). A transient `/tmp/tsukuroi-r3-2-selftest.oyq4RW` was observed at 21:12 and was gone 60 s later, so this is a real path exercised this wave, but nothing was left behind and no evidence path points at `/tmp`. Smallest remediation: export `TMPDIR=/fast/scratch/hyaku/tsukuroi-r70/l1/tmp` in `gates.sh`. | `after/gates.sh:1-24` (no TMPDIR); `tools/tsukuroi-census.sh:2363-2448`; observed dir names in the shell transcript, absent on re-stat |
| F4 | none (verified) | **Arm patch write surface — clean, re-read at its final bytes.** The patch was revised mid-wave (first reading 21:14, sha `cb147b10…`; final reading 21:16, sha **`99a1c8d2…5caecbf`**, 18 612 B, companion `.sha256` matches, `APPLY_CHECK_OK`, applied file sha `8ad56c22…`). Both readings agree on the write surface. Live `probe_xfs_arm` reads only: `cat -- "$PROC_MOUNTS"` guarded by `-f`/non-empty (a FIFO mount table is never opened), `-d`/`-r`/`-x` tri-state on `/sys/fs/xfs/<basename>`, `IFS= read -r first < stats/stats` (first line only), and two `globstar` `-f`/`-r` counts that **never open** `error/`/`log/` entries; `stats_clear` is never read or written. The emission sits exactly between `printf '%s\n' "$KERNEL_LINE"` and the rollup composition; no rollup term and no exit path is touched (A/B neutrality case PASS). All 8 `chmod` (000/600/755) and both `mkfifo` calls (the must-not-block case, preceded by `rm -f`) act on selftest fixture paths under `$FX/...`, never on `/sys`, `/proc`, `/dev` or `/etc`; there is **no** `mknod`, no `tee`, no redirection to a host path (patch host-path redirections = 0), no `sudo`/`pacman`/`systemctl`. Final selftest receipt: `PASS (212 cases, 212 passed, 0 failed)`, rc 0, 16 `R70-C2` labels; the live line `mounts=2 present=2 absent=0 unreadable=0 stats=2 error=18 log=8 detail=none` equals E2's independent enumeration and my own counts. | `probes/E1XfsArm/r70-xfs-arm.diff` (hunk `@@ -4380,6 +4639,10 @@ main()`; `probe_xfs_arm`), `probes/E1XfsArm/{apply-check.txt,r70-xfs-arm.diff.sha256,live-xfs-line.txt,selftest-full.txt,neutrality-and-fields.txt}` |
| F5 | **LOW** | Scratch footprint: every sandbox is a `--shared` clone (`.git` 3.0 M with `objects/info/alternates` → the lane, so no duplicated object store) and every one lives under `/fast/scratch/hyaku/tsukuroi-r70/`; no fixture exists outside `/fast/scratch` and no clone exists anywhere else. Size is the checked-out worktree, not objects: first reading `E1XfsArm` 431 M, `R2Reviewer` 431 M, `K1Critic` 429 M (E1's and K1's later removed by their own `trap`); final reading `E1XfsArm` 861 M (clone + applytest), `M1Mutation` 431 M, `R2Reviewer` 431 M, `K1Critic` 429 M — i.e. **no single multi-GB tree**, but ≈ 2.1 G in aggregate while four seats ran concurrently. Cleanup is each seat's `trap`; E1's and K1's first trees did disappear and E1's re-created one was live at yield, so a post-wave agent should re-check `du -sh /fast/scratch/hyaku/tsukuroi-r70` is empty. | witness §7 and §9 (final `du`); `git -C <clone> remote -v` → lane; alternates file present |
| F6 | none | **No host write of any class.** An arrow-safe scan of every round artifact (reports, probes, committed capture, the arm patch) for `> /sys`, `> /proc`, `> /etc`, `> /boot`, `tee /sys`, `stats_clear` writes, `max_retries`/`fail_at_unmount` stores, `xfs_scrub`/`xfs_repair`/`btrfs`/`snapper` invocations, `mknod`, `chown`, `pacman -S/-Sy/-Syu/-U/-R`, `systemctl start|stop|restart|enable|disable|mask` yields **0** host invocations. Non-zero hits, all explained: one quoted historical `pacman -Syu` line (`before/novelty-sweep.txt:12`), two of this report's own quoted pattern strings, and eight `chmod` lines plus two `mkfifo` lines in the arm patch — every one of them on a selftest fixture path under `$FX/...` (F4); `grep '> */\(sys\|proc\|etc\|boot\)/'` over the patch = **0**. `xfs_spaceman` appears only as `-c 'health'` and as source text. | final scan (3 files: patch, this report, one quote); witness §8 |
| F7 | none | **No privilege escalation.** The artifacts contain no `sudo` at all — not even `sudo -n`. Observed verbs are `findmnt`, `stat`, `find`, `cat`/`head`, `wc`, `grep`, `awk`, `git show`, `xfs_spaceman -V`/`-c health`, `date`, `uname`. | `grep -rIn '\bsudo\b'` over `before/ after/ w1/ probes/` → 0 (dispatch/spec text excluded as orchestrator prompt) |
| F8 | none | **No secret, credential, key path, token, serial or WWID.** No `op://`, private-key block, `ghp_`/`sk-`/`xoxb-`/`AKIA` token, `~/.ssh`, `id_rsa`, `.gnupg`, `.aws`, `.netrc`, `machine-id`, `/dev/disk/by-id`, `nvme id-ctrl`, or serial/WWID value. One host-name occurrence exists: `before/census-live-base.txt:1` header (`host=<name>`), the pre-data L1 capture on this fixture host, which the brief allows; no seat report copies it. `w1/swarm-registry.json` is mode 600. | witness; `grep -rIl <fixture-host-name>` → 1 file |
| F9 | none | **Host not mutated.** `stats_clear` is `0200 root root` on both filesystems **and** the global dir (identical to `before/host.txt`); `fail_at_unmount` `0644` value 1 on both; `metadata/default/max_retries` `0644` value -1 on both; `metadata/ENODEV/max_retries` = 0; `error/` 9, `log/` 4, `stats/stats` 34 lines per filesystem; `/proc/fs/xfs/stat` still the symlink to `/sys/fs/xfs/stats/stats`; `findmnt -t xfs` still the same two mounts. The global stats counters **increased** between the pre-data capture and audit (`extent_alloc` first field 50 993 491 → 54 336 997), which a `stats_clear` write would have reset — direct evidence no clear occurred. `/etc` and `/boot` have **0** files modified since wave start (20:59); `/var/lib/pacman/db.lck` absent and `/var/lib/pacman/local` mtime `2026-11-02 15:30`, i.e. no package transaction. | witness §§4-5 |
| F10 | none | **Validator / JJ boundary.** Lane tree: HEAD `84e013a7`, tracked diff **0** lines, index **0** staged lines, so no seat modified a tracked file; `.git/HEAD`, `refs/heads/master` and `logs/HEAD` were last written at `21:08:15` by the L1's jj export (`reflog: export from jj`) with content still `84e013a7`. Untracked: 37 paths at the witness reading and 53 at the final reading, all under `.ufo/waves/round-70/` except two inherited markers (`.ufo/waves/round-66/w1.ready.dispatched` 18:11, `.ufo/waves/round-67/w1.ready.dispatched` 18:48 — prior rounds, not this wave). Fleet repo dirt is not this lane's: `M .scratch/goal-20261103-hyaku-run15.md`, `M .scratch/run15-state.json`, `?? .scratch/run13-state.json`, `?? .scratch/run15-kernel.py`, `?? after` (20:05) are L1/orchestrator run state predating the wave, and `?? .ufo/reports/round-70/kama.md` (21:10) is the **kama** sibling lane's own report (`/home/vgpnk/Projects/shokunin/kama-shokunin`, 0 occurrences of "tsukuroi"). Structurally, the lane dir is gitignored in the fleet (`.gitignore:1  *-shokunin/`), so no lane-tree file can dirty the fleet repo. | witness §§1-3 |
| F11 | none | **Instrument write surface (counter).** `tools/count-xs-rows-r70.py` opens no file for writing: its only IO is `Path.read_text/read_bytes` (fixture mode) and `subprocess.run(["git","-C",lane,"show",...])` (revision mode); no `tempfile`, `mkstemp`, `mkdir`, `shutil`, `remove`, `rename`. Empirically run at the declaration revision from a scratch cwd with `TMPDIR` inside that cwd: printed `XS_NOTE absent`, rc **128**, and created **0** files in the cwd and **0** in `/tmp`. Its sha256 is `65065d9d18cea52027619697264de430780e65ff13ab6da2a790c3d2054f6f5c` both in the worktree and at `1710bd74`, matching the frozen value. The four snapshots pass `sha256sum -c` and match `SOURCES.json`. | `tools/count-xs-rows-r70.py:21,53-71`; witness §6; `sha256sum -c SHA256SUMS` → 4× OK |

Split: 1 HIGH (F1), 1 MED (F2), 2 LOW (F3, F5), 8 none (F4, F6-F11). F1/F2 are the same wrong
number seen from two sides (a frozen premise and the draft that inherits it); F3/F5 are scratch
hygiene; F4 was the one open verification gap and it closed clean when the patch landed at 21:14.

## Item answers

1. **Host / package / service writes, sudo, secrets.** None of the four classes fired (F6-F8). Every
   host-facing command in the round's artifacts is a read: `findmnt`, `stat`, `find`, `cat`, `wc`,
   `grep`, `xfs_info`, `xfs_spaceman -c health`, `uname`, `pacman -Q*`. No stats_clear, no
   `error/*/max_retries` or `fail_at_unmount` store, no `xfs_scrub`/`xfs_repair`/`btrfs`/`snapper`, no
   package transaction, no service action, no `mknod`/`chmod`/`chown`.
2. **Scratch discipline.** No `/tmp` path is cited as evidence (the one `/tmp/` string in
   `before/novelty-sweep.txt` is a quoted round-40 lesson about `<root>/tmp/alpm_XXXXXX`), and no
   report/build script hardcodes `/tmp` — `before/control/build_battery.py:128` defaults its fixture
   root to `/fast/scratch/.../l1/battery`, E2's and E1's recipes use `/fast/scratch`. The one live
   `/tmp` use is the pre-existing census selftest fallback reached by `after/gates.sh` (F3), transient
   and self-cleaning. No fixture repo exists outside `/fast/scratch`; no multi-GB tree (F5).
3. **Validator / JJ boundary.** Clean (F10): tracked tree untouched, index empty, all new files in
   the wave's own write scope, and the fleet-repo dirt attributable to orchestrator/sibling work.
4. **Instrument write surface.** Counter verified by code and by an empirical run (F11). Arm patch
   delivered at 21:14 and read in full (F4): live arm reads only, the emission sits exactly between
   the KERNEL line and the rollup, no rollup/exit term changes, and the only `chmod`/`mkfifo` calls
   act on selftest fixture paths — no host redirection, no device node, no sysfs write.
5. **Host not mutated.** Verified against `before/host.txt` for every non-time-varying field and by
   the monotonic stats counters for the one time-varying proof that matters (no clear) (F9).

## What I could not check

- Seat artifacts that land after this audit window: at yield time `R2Reviewer`, `K1Critic` and
  `M1Mutation` had produced no report under `w1/` or `probes/` (their sandbox clones were live; E1's
  and K1's scratch was already removed by its `trap`). The same scan — host redirection, `sudo`,
  tokens/serials, `/tmp` evidence, out-of-scope lane or fleet writes — must be re-run on their
  outputs. Of the reports that did land, `w1/SC3Lesson-gate.md` (21:20) was scanned after the table
  was written and is clean; `R1Reviewer.md`, `E3Repairs.md`, `S1Scout.md`, `C1Connector.md`,
  `SC1Entry*.md`, `SC2Sources.md`, `E2Capture.md`, `E1XfsArm`'s probes and `after/gates.sh` are
  covered above.
- Service state (`systemctl`) was not probed: no artifact invokes it, so a host restart could only be
  visible as an uptime discontinuity, which is outside this seat's read budget; no such invocation
  exists in any artifact.
- Scratch cleanup is each seat's own `trap`; my own scratch
  `/fast/scratch/hyaku/tsukuroi-r70/N1Sentinel` was removed before yield (its only file was the
  `.marker` used by the counter write-surface test).
- I did not re-derive C1's rows, C2's predicate, or any host count as a claim; the counts above are
  audit evidence only and bind no claim. F1/F2 report what the artifacts and the host say; the
  correction of `7` → `9` is the L1's and the scribe's call, not this seat's.

Metric definitions: **WRITES** host-mutating commands found in round artifacts; **SECRETS**
secret/credential/serial items; **SUDO_NONREADONLY** `sudo` invocations neither `-n` nor read-only;
**TMP_EVIDENCE** artifacts citing a `/tmp` path as evidence; **LANE_DIRTY** seat-authored paths
outside `.ufo/waves/round-70/{w1,probes}` (0 — the 53 untracked wave paths are inside that scope, and
the tracked tree and index are clean); **STATS_CLEAR_MODE_UNCHANGED** 1 iff all `stats_clear` modes are
still 0200; **FINDINGS** rows in the table above.

WRITES=0 SECRETS=0 SUDO_NONREADONLY=0 TMP_EVIDENCE=0 LANE_DIRTY=0 STATS_CLEAR_MODE_UNCHANGED=1 FINDINGS=11
