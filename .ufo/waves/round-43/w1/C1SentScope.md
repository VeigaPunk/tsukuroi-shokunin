VERDICT: defect-found

Scope of the verdict: the mount/host-safety questions about the C1 counter are answered
**supports** (no mount can reach the host, no residue, no writes outside `--scratch`, SIGINT/SIGTERM
clean up, the real `/etc` and `/usr/lib/modules` are never touched by the fixture legs, and the
whole run fails closed). The defect is in the *controls battery* `run_controls_c1.py`: it has no
signal cleanup (a SIGTERM leaves a 297 MB clone) and it writes its receipts into the git-tracked
lane directory instead of `--scratch`. Both are Low severity and neither touches the host.

Seat: C1SentScope (item C1-15), round 43 (hyaku run 9), w1. Counter under review
`tools/score-bootinputs-r43.py` sha256 886f92c8cd58e52e4e74f4df81708f243b77e9d33de567b47371f21419b3e10f
(matches the frozen hash in the declaration), scored revision
717b716a8943151ace8657e0ca23d7d9b8434f26, battery
`.ufo/waves/round-43/controls/run_controls_c1.py` sha256 8eb691711eefda48c3e557c06ac4b156299e2829e2688a893b84ad7b4a131493,
candidate `candidate-boot-chain-audit.sh` sha256 3e5c876389985aa5168c7116db5ea808fa0d7d697a1d66b7fcf850efd60dfd74
(receipt `C1SentScope/00-shas.txt`). Host: linux 7.2.11-arch1-1, strace present, `unshare` from
util-linux 2.42.4, `/proc/sys/kernel/unprivileged_userns_clone` = 1.

Baseline before I touched anything: the counter PASSes on this host in 907 ms —
`{"btime": 1793027300, "cases": 16, "correct": 16, "identity": ["1000","1000","1000"], "identity_ok": 1,
"live": {"expect":"0","got":"0","rc":0}, "live_agree": 1, "selftest_line": "TSUKUROI_BOOTCHAIN_SELFTEST:
PASS total=48 failed=0", "selftest_pass": 1, "selftest_r43": 3, "verdict": "PASS"}` (receipt
`C1SentScope/01-baseline-pass.jsonl`). Scratch dir empty afterwards; `/etc` fingerprint unchanged.

# 1. Can a mount reach the host mount namespace? No — three independent reasons.

(a) The host root *is* shared (`33 2 0:30 /@ / rw,noatime shared:1 - btrfs /dev/mapper/root …`,
`awk '$5=="/"' /proc/self/mountinfo`), so propagation is the thing that matters, not the namespace.
`unshare -m` itself breaks the peer group before the payload runs; straced on this host:
`mount("none", "/", NULL, MS_REC|MS_PRIVATE, NULL) = 0` (`trace-unshare`, receipt
`C1SentScope/03-propagation.txt`). The counter's own namespace child does the same call — first
mount-family line of the full trace, `trace-full:241
2415082 mount("none", "/", NULL, MS_REC|MS_PRIVATE, NULL) = 0` (receipt `C1SentScope/04-trace-mounts.txt`).
The propagation setting is produced by `unshare(1)` independent of the `--map-users/--map-groups`
options the counter passes (`score-bootinputs-r43.py:292-293`), so the production invocation is
covered by the same evidence.

(b) Empirical leak probe with the same option family: inside `unshare -U -m --map-root-user`, the
ns root line has *no* `shared:`/`master:` tag (private), a tmpfs mounted over `/etc` holds the marker
`/etc/R43-LEAK-PROBE`, and after the namespace exits the host cannot see it:
`ls: cannot access '/etc/R43-LEAK-PROBE': No such file or directory`; host `/etc` fingerprint
`060e9d5490a3002c383fbfdc5e7698d69e909d2cf9c10b299f4129239d124ba1` (184 entries) identical before and
after. Same result for the counter's own `/mnt` tmpfs: host `/mnt` still lists `snap101 snaps`.

(c) The mounts are tmpfs created by a process in an unprivileged user namespace, i.e. they are owned
by that namespace and die with it; after every run `grep -cE 'r43view|r43lib' /proc/self/mountinfo`
= 0. The four mounts are `score-bootinputs-r43.py:75` (`/mnt`) and `:80-81`
(`/usr/lib/initcpio`, `/usr/lib/modules`, `/etc`), traced as
`fsopen("tmpfs") … fsconfig … fsmount … move_mount(… , "/etc", MOVE_MOUNT_F_EMPTY_PATH) = 0`
(`trace-full:422-427`).

# 2. Can a failure leave tmpfs or files on the host? No. Fail-closed, verified by injection.

Ordering in INNER: all four mounts (`:75`, `:80-81`) precede `roots = [...]` (`:82`) and the wipe loop
(`:84+`), and `sh()` is `subprocess.run(..., check=True)` (INNER, `:73-74`), so *any* failed mount
aborts the namespace leg before a single file is removed. Traced order in the good run: `move_mount
… "/etc"` at `trace-full:427`, first `unlink("/etc/limine-snapper-sync.conf")` at `trace-full:498`
(receipt `C1SentScope/05-trace-order.txt`).

Injection (scratch copy, `/etc` mount target changed to `/etc/.__r43_missing__` so the covering tmpfs
cannot be mounted): the counter prints `{"error": "namespace leg failed: … CalledProcessError: Command
'['mount', '-t', 'tmpfs', '-o', 'mode=755', 'r43view', '/etc/.__r43_missing__']' returned non-zero exit
status 32", "verdict": "ERROR"}` and exits 2 (rc=2). In that trace there are **zero**
`unlink`/`unlinkat` calls naming `/etc` or `/usr/lib` (the wipe never ran), the scratch dir is cleaned,
and the host `/etc` fingerprint and the `/usr/lib/initcpio` (9 entries) and `/usr/lib/modules`
(`6.18.57-2-lts`, `7.2.11-arch1-1`) listings are unchanged (receipt `C1SentScope/11-inject-mount-failure.txt`).
The same fail-closed path is what the production artifact takes when the namespace cannot start at all:
under strace, `newuidmap` (setuid) cannot be traced, and the counter reports
`{"error": "namespace leg failed: newuidmap: Could not set caps", "verdict": "ERROR"}` exit 2 with no
mount executed and an empty scratch dir (receipt `C1SentScope/02-strace-production-error.txt`).

Residue after signals: 0 bytes of scratch after SIGTERM and SIGINT (below); only SIGKILL (uncatchable)
leaves `106866` bytes / 3 entries inside `--scratch` (`S16/bootinputs-r43.*/bca.sh`, `bca-lib.sh`).

# 3. Does anything write outside `--scratch`?

**Counter: no.** Every `openat` with `O_WRONLY|O_RDWR|O_CREAT|O_TRUNC` in the 26 209-line trace is
classified (receipt `06-writes-outside-scratch.txt`): 206 literal `--scratch` paths, 45 dirfd-relative
writes whose dirfd is a directory under `--scratch` (`trace-full:22277` opens
`<scratch>/S3/bootinputs-r43._d8vm9uz/st/tsukuroi-bootchain-selftest.WuzguW/work/tree.RvvsxM/` as
`O_PATH|O_DIRECTORY` = fd 3; `:22280` then writes `openat(3, "./VERSION", O_WRONLY|O_CREAT|O_EXCL)`),
3 `/proc/self/{uid_map,setgroups,gid_map}` writes made by `unshare`, 43 `/dev/null`-`/dev/tty`, and 152
absolute paths under `/etc` + `/usr/lib` that resolve **inside the namespace** after the tmpfs mounts
(see §1; host verified unchanged). Nothing else. `git` is only read (`rev-parse`, `show`): no
`.git` write appears in the trace.

**Controls battery: yes, by construction.** `run_controls_c1.py:118` and `:132` write
`C1-K*.jsonl` and `battery-summary-c1.jsonl` to `HERE` (`:35` = the script's own directory), not to
`--scratch`. In production that directory is the lane's tracked
`.ufo/waves/round-43/controls/` — `git -C <lane> ls-files .ufo/waves/round-43/controls/` lists
`C1-K0.jsonl … C1-K10.jsonl` (the same directory also holds the C2 battery's `C2-K*.jsonl`, which this script does not write), i.e. the 11 `C1-K*.jsonl` receipts and `battery-summary-c1.jsonl` (12 files) are overwritten by every run
(receipt `09-controls-write-path.txt`). Reproduction without touching the lane: an unmodified copy of
the script placed in scratch wrote all 11 `C1-K*.jsonl` receipts plus `battery-summary-c1.jsonl` beside itself and left `--scratch` empty (`S9` = 0 entries); that run's summary
reproduces the declared values (`counter_sha256` 886f92c8…, `candidate_sha256` 3e5c8763…,
`control_accepted: 1`, K0 correct 8, K1 9, K2 13, K10 15 — all FAIL as expected). Consequence: a
read-only seat cannot run the battery at all, and a killed run can truncate a tracked receipt (open
`'w'`, no tmp+rename).

# 4. SIGINT / SIGTERM

Counter (`score-bootinputs-r43.py:247-255`, handlers raise `SystemExit`, `finally:
shutil.rmtree(work, ignore_errors=True)`): SIGTERM at 0.45 s (namespace leg) → exit **143**, scratch
0 bytes; SIGINT at 0.25 s → exit **130**, scratch 0 bytes; no orphan (`ps -eo args | grep -c
'[u]nshare -m'` = 0, `[s]core-bootinputs` = 0) — receipt `08-signals.txt`. (The `orphans=1` line in
that log is `grep` matching itself; re-measured with the bracket pattern = 0.) The docstring claim at
`:46` ("everything the counter writes lives under it and is removed on exit, SIGINT and SIGTERM") is
therefore accurate.

Controls battery: **no handler** — the only cleanup is `finally: shutil.rmtree(work)` (`:137-138`),
which Python does not run for SIGTERM. Measured: `[controls TERM] exit=143 scratch_left=17435
bytes=296670369 receipts=0` — a 296.7 MB interrupted clone under `--scratch`, no orphan. Each repeat
of that costs another 297 MB.

# 5. Can it touch the real `/etc` or `/usr/lib/modules`?

Fixture legs (N): no — tmpfs covers all three roots before any write (§1, §2), and the code that runs
there holds no host write permission anyway: the namespace maps host uid 1000 → ns 0 and the
`/etc/subuid` range (`vgpnk:100000:65536`) from ns 1, so `setpriv --reuid=1000` lands on **host uid
100999**, not the caller. Measured: `id -u` inside = 1000, while the file that process created in a
1777 directory is owned by `100999:100999` on the host (receipt `07-uidprobe.txt`); writing into the
caller's own 0755 scratch dir was denied. Note this makes the docstring phrase "the caller's uid"
(`:13-16`) and `identity_ok` (`:305`, compares `id -u` output) *namespace-local* — accurate as a
channel check, but not a statement about host credentials (finding F4).

Live and selftest legs (L at `:310-315`, S at `:321-326`): these run the revision's code **with no
namespace at all**, at the caller's real identity, cwd = the scratch work dir, with the caller's
environment minus `TSUKUROI_*`/`BOOTCHAIN_*`/`UFO_*`/`TMPDIR` (`DROP`, `:68`; `clean_env`, `:150-151`).
For the frozen revision that is read-only (`boot_inputs_newer` → `btime_epoch` + one `find`; the
selftest writes only under `TMPDIR`, which is `<scratch>/work/st`), and the trace shows no write by
those legs. It is nevertheless a trust boundary the docstring does not state (finding F3), and the
"override environment (none set)" wording at `:35` overstates it: `HOME`, `USER`, `PATH`, `PWD`,
`SHLVL`, `BASH_ENV` survive, so a revision gated on e.g. `[ -n "$HOME" ]` would pass all legs (the K4
control only tests the three dropped prefixes). Untested by me as a scored variant (that would be the
K4 control's job); code evidence only.

# 6. Audit-method caveat (affects any future mount review of this counter)

The syscall set named in the assignment — `mount,umount2,unlink,rename,openat` — **cannot see these
mounts**: util-linux 2.42.4 `mount(8)` uses the new mount API, so `-e trace=mount` shows only
`unshare`'s own `MS_PRIVATE` call while the tmpfs appears as
`fsopen("tmpfs")`/`fsconfig`/`fsmount`/`move_mount` (receipt `10-trace-filter-gap.txt`). Second
limitation: the production artifact cannot be traced end-to-end, because `unshare(1)` spawns the
setuid helper `newuidmap`, which ptrace cannot follow — the run then ends `ERROR` (fail-closed, §2).
To get mount evidence I used a scratch copy of the counter with the two `--map-users`/`--map-groups`
arguments replaced by `--map-root-user` and `spec['uid'/'gid'] = 0`; the INNER mount sequence is
byte-identical, and the run reports `correct: 0` for that copy because `setpriv --clear-groups`
cannot run where `/proc/self/setgroups` is `deny` — an artefact of the copy, not of the frozen
counter, whose own run is the PASS in §0.

# Findings (severity / exploit path / evidence / impact / smallest remediation)

- **F1 (Low) — controls battery has no SIGINT/SIGTERM cleanup.** Exploit/failure path: operator or CI
  kills `run_controls_c1.py` mid-clone → `finally` never runs → `--scratch` holds a 296,670,369-byte
  clone (`S17`, 17 435 entries) for ever; repeat on a filled scratch FS and the next run fails with
  ENOSPC. Evidence: `:137-138` (only a `finally`), measured `[controls TERM] exit=143
  scratch_left=17435 bytes=296670369` (`08-signals.txt`). Impact: scratch leak only, nothing on the
  host and nothing in the lane. Remediation: install the same two handlers the counter already uses
  (`score-bootinputs-r43.py:247-251` pattern) before the `try` in `main()`.
- **F2 (Low) — the battery writes tracked lane files, non-atomically, from `--scratch` runs.**
  Path: `:118`, `:132` → `HERE` = `.ufo/waves/round-43/controls/` in production. Impact: those 12 tracked
  files are overwritten by any run (a read-only seat cannot run it; a concurrent or killed run can
  truncate one), i.e. the battery is not reproducible without mutating the lane. Evidence: `git
  ls-files` output + the relocation reproduction in `09-controls-write-path.txt`. Remediation: take
  `--out <dir>` (default `HERE`), write `tmp + os.replace`, and refuse to write when `os.environ`
  marks the seat read-only.
- **F3 (Low, statement-only) — unsandboxed execution of revision code in the L and S legs.**
  `:313`, `:324`. Impact: a mis-authored or adversarial revision runs as the caller against the real
  filesystem in those two legs; the N legs' isolation does not extend to them. Smallest remediation:
  one sentence in the docstring stating the trust model (the scored tree is lane-authored and already
  reviewed), so no reader assumes `--scratch` bounds all execution.
- **F4 (Info) — `identity_ok` is namespace-local.** `:305` compares `id -u`/`id -g` *inside* the
  namespace; host credentials are subuid 100999 (`07-uidprobe.txt`). Remediation: either say so at
  `:16`, or additionally assert the host uid (INNER creates a file in a 1777 dir under `--scratch`;
  the parent lstats it).
- **F5 (Info) — channel wording at `:35`.** "override environment (none set)" is true for the three
  dropped prefixes only (`:68`, `:150-151`); `HOME`/`USER`/`PATH`/`BASH_ENV` survive. A one-line
  precision fix (or dropping `HOME`, `USER`, `BASH_ENV`, `ENV` in `clean_env`) closes it.

Not findings: mounts reaching the host (ruled out, §1), tmpfs/files left on the host (§1, §2), writes
by the counter outside `--scratch` (§3), `/etc` or `/usr/lib/modules` touched (§2, §5), SIGINT/SIGTERM
residue in the counter (§4).

# What I did not do

- Did not run the controls battery in place (it would overwrite the lane's tracked receipts) — I ran
  an unmodified copy in scratch, which changes only `HERE`.
- Did not evaluate the correctness of the 16 cases or the controls' verdict table (not this item);
  the copied battery reproduced the declared summary, nothing more.
- Did not strace the frozen artifact to completion (impossible under ptrace because of setuid
  `newuidmap`); mount evidence comes from the `--map-root-user` copy plus the independent
  `unshare`-only probe.
- No tool was installed or upgraded for this seat.

Receipts: `.ufo/waves/round-43/w1/C1SentScope/` (13 files, 68 KB). Scratch
`/fast/scratch/hyaku/tsukuroi-r43/C1SentScope/` was removed after copying them.
