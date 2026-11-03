2026-11-03T18:46:50Z

# SC1Host — C2-RECON (round 64 / w1, scout, read-only)

Seat: `SC1Host`. Item **C2-RECON**. Host `plazir27`, kernel `7.2.11-arch1-1`, systemd
`262.1-1-arch`. All probes read-only; no `sudo`, no service actions, no pacman transaction.

Output artifact (this seat's one write):
`.ufo/waves/round-64/after/scout-host-recon.md` (793 lines, 9 sections: probe receipts §1,
findings §2–§6, traps §7, register-ready values §8, unknowns §9).

## Failed-unit identities

Two, both **app-level transients (rembg-class), not system-unit failures**:

| unit | result | cap | peak | window |
|---|---|---|---|---|
| `run-p1157862-i1164315.scope` | `oom-kill` | `MemoryMax=3221225472`, `MemorySwapMax=0` | 3221225472 (exactly at cap) | 2026-11-02 16:49:19 → 16:49:24 |
| `run-p1159104-i1145275.scope` | `oom-kill` | `MemoryMax=8589934592`, `MemorySwapMax=0` | 8589934592 (exactly at cap) | 2026-11-02 16:49:33 → 16:49:45 |

Both are `[systemd-run] /home/vgpnk/.local/bin/rembg i -m birefnet-general …`, loaded from
`/run/user/1000/systemd/transient/` with `Transient=yes`, and killed by the **cgroup** OOM killer
(`Memory cgroup out of memory: Killed process 1157862 (rembg) … oom_score_adj:200`). No unit file
exists for either (`list-unit-files --state=bad` → 0). System scope is clean: `running`,
`NFailedUnits=0`, `--failed` empty, `graphical.target` active.

The user manager's `degraded` (rc=1) is caused entirely by these two leftovers, so the stored
`running` + `0 failed` is a genuine `drift`.

## Top-3 err identifiers with counts (`journalctl -b -p err -o json | …count by SYSLOG_IDENTIFIER`)

```
total 5276
5230 systemd-socket-proxyd
  40 kernel
   4 systemd-coredump
```
(complete list: `+1 sddm-helper`, `+1 systemd`)

1. **`systemd-socket-proxyd` 5230** — one PID (442437), one cgroup (`comfyui.service`), one
   message (`Failed to connect to remote host: Connection refused`), one 330.6 s window
   2026-11-02 16:04:19→16:09:50 at ≈15.8/s. The ComfyUI backend died at 16:04:19 (24.1 G peak) and
   the on-demand proxy logged every refused connect at err priority until its 20-min idle exit.
2. **`kernel` 40** — `sr0` 35 (20 `critical target error` + 15 `Buffer I/O error`, all in 2.6 s at
   boot on a USB optical drive labelled `MB_Support_CD`), cgroup-OOM 2, `virt/tdx` unsupported 1,
   new `overlayfs: failed to resolve '/upper': -2` 1, one empty-MESSAGE entry 1.
3. **`systemd-coredump` 4** — 2 chromium SIGSEGV crit entries at 16:47:00/01 (earlyoom SIGKILL'd
   renderers) and 2 python3 `terminated abnormally without generating a coredump` at
   22:53:23/23:05:12 (the two `shokunin-r67-*` probes exiting 134).

Residual after removing the one-process storm: **46** entries — today's real noise floor is
*below* the stored 238; the 22× headline growth is a single application log loop, not a system
regression.

## Other quantities for the register

| item | stored 2026-10-14 | live |
|---|---|---|
| err entries | 238 | 5276 |
| err classes | coredump 198 / kernel 38 / sddm 1 | proxyd 5230 / kernel 40 / coredump 4 / sddm 1 / systemd 1 |
| `sddm-helper` | 1 `gkr-pam: couldn't unlock the login keyring.` | 1, identical → **match** |
| coredumps | 198 entries / 764 files / 3.8 G | 252 rows / 10 files / 704 M (737406945 B) |
| retained boots | 13 (census) / 9 (later) | 3 (−2 2026-10-26, −1 2026-10-31, 0 2026-11-02) |
| timers | only `ai-usage.timer` active | 2 listed: `ai-usage.timer` (5 min, 327 runs this boot) + `cursor-shim-healthcheck.timer` |

## OS-level observations (detection only)

* **`sr0` boot read failures are chronic**: 65 / 60 / 35 kernel err lines in boots −2 / −1 / 0,
  every boot, all inside 2.6 s at enumeration, device never mounted. Largest kernel err class in
  every retained boot; hardware/media class.
* **New `overlayfs` err burst during wave hours**: `failed to resolve '/upper': -2` (prio 3) at
  15:39:19 plus 5 warning-priority `failed to set xattr on upper` batches at 15:38:04, 15:39:33,
  15:41:07, 15:41:23, 15:41:30, 15:43:11. No overlay mount exists at probe time, `/upper` absent,
  no `_PID`/`_COMM` attached. Non-fatal (kernel falls back to `userxattr`/reduced features);
  inference: ephemeral sandbox mounts, correlated with agent activity, not with a boot or kernel path.
* **`cursor-shim-healthcheck.timer` is a dead watchdog**: enabled, active/elapsed,
  `OnUnitActiveUSec=1min`, `next_elapse=0`, `LastTriggerUSec=Mon 2026-10-19 00:33:15 -03`, and its
  service has **zero** journal entries across all retained boots. Silent, never in `--failed`.
* **Memory cluster** (the real operability event this boot): 176 SIGKILL + 144 SIGTERM by
  `earlyoom` on 2026-11-02 16:04–16:48 (boots −1/−2: 0 and 0); `mem avail 409 of 26184 MiB`,
  `swap free 0 of 30979 MiB` at 16:47:00; 12 shim/agent services failed `signal`, `ai-usage`
  SIGTERM'd, and the two rembg scopes cgroup-OOM'd. `systemd-oomd` is disabled and inactive, so it
  is not the killer. Current PSI `some/full avg300=0.03` — no ongoing pressure.

## Traps recorded (so no seat re-derives them)

1. `coredumpctl` has **no** `--boot`/`-b` here: `unrecognized option '-b'`, rc=1. Per-boot counts
   must use `--since/--until` windows from `journalctl --list-boots`.
2. `systemctl --user show -p State` prints nothing (rc=0); use `is-system-running` or `NFailedUnits`.
3. `-p err` line count (6213) ≠ entry count (5276) in the same window — coredump stack traces.
4. `dmesg` blocked (`dmesg_restrict=1`, `Operation not permitted`); kernel evidence via `journalctl -k`.
5. `btrfs subvolume list /` and `/sys/kernel/debug/zswap/*` blocked unprivileged.
6. `ps --sort=-etimes` unsupported; `-btrfs`/`zswap` limits noted; `--sort=-rss` works.

## Scratch

No clone or work tree was created; no `/fast/scratch/**` dir exists for this seat. Probe
transcripts were staged in `/tmp/sc1-{a,b,c,d}.txt` (< 50 MB) and their content is reproduced
verbatim in the artifact; they are being deleted before yield.
