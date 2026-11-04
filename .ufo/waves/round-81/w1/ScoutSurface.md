# ScoutSurface — round 81, wave w1 — binding report

Seat: ScoutSurface (scout, leaf). Read-only reconnaissance of the live mount surface against
`corpus/knowledge/mount-unit-fstab-plane-r81.md` / `.json`. No production edit, no git/jj mutation,
no `systemctl` start/stop/reload/daemon-reload, no write outside this seat's directory.

## Axes

- depth — every generated mount, swap and device.d unit read; every mount unit systemd knows enumerated (22 generator files, 19 mount units listed, 13 surface sections).
- operability — each sentence of the entry checked against a command's output; the live `Options=`, `Requires=`, `Following=` and `JobRunningTimeoutUSec` values are the decisive legs.
- freshness — generator file mtimes vs `/etc/fstab` mtime vs boot time; generator output vs the captured `host/generator.txt`.

## Result

The live surface contradicts the entry in three places and mis-cites two measured legs. It does
not contradict the core mechanism rows (MT2 wanted-not-required, MT3–MT4, MT7–MT8 are not exercised
by this host's fstab).

| id | entry says | live surface shows | status |
|---|---|---|---|
| C1 | generated `Options=` "drops the `x-systemd.*` tokens" | `tmp.mount` `Options=…,nofail,x-systemd.before=local-fs.target` | contradicted for `/tmp` |
| C2 | "six local file systems; four are required and two are not" | five required + two `nofail` = seven; entry's own list has five | contradicted (count and "four") |
| C3 | `/tmp` boot cost "up to ten seconds" | 10s `JobRunningTimeoutUSec` sits on alias `dev-disk-by…1f8a5361…device` (`Following=…nvme1n1p1.device`); the unit `tmp.mount` `Requires=` (`dev-nvme1n1p1.device`) reports `1min 30s`, no drop-in | contradicted as a consequence; mechanism `[INFERENCE]`, not measured |
| C4 | measured legs "S332 :35-47 vs :95-107" for tmp/fast; MT5 leg `:99-100` | `:35-47` = fast.mount, `:95-107` = var-log.mount, tmp.mount = `:64-78` (Before at `:70`); `:99-100` = var-log.mount | citation defect (substance) |

Checked and clean: no `nofail` mount required by any target; no hand-written mount unit or mount
drop-in; the device.d drop-in headers match the fstab options; `/etc/fstab` mtime predates the
generated files; snapshot digests match. Full table: `ScoutSurface/contradictions.md`.

## Enumeration (surface.txt, 432 lines, §1–§13)

- `/etc/fstab`: 9 non-comment rows (5 required block mounts; swap; `/tmp` and `/fast` `nofail` with `x-systemd.device-timeout=10s`, `/tmp` also `x-systemd.before=local-fs.target`; `tmpfs /dev/shm`).
- `/run/systemd/generator/`: 22 files. Mount: `-.mount boot.mount fast.mount home.mount tmp.mount var-cache-pacman-pkg.mount var-log.mount`; swap: `swap-swapfile.swap`; device.d: two `50-device-timeout.conf`; target dirs: `local-fs.target.wants` (fast, tmp, systemd-remount-fs.service), `local-fs.target.requires` (-, boot, home, var-cache-pacman-pkg, var-log), `swap.target.requires`, `sockets.target.wants` (sshd, non-fstab).
- `systemctl show` for each generated mount: recorded in surface §7 with Before/After/WantedBy/RequiredBy/Wants/Requires/FragmentPath/SourcePath/Options/DropInPaths.
- Device units: `dev-disk-by…1f8a5361…device` and `…070be1ea…device` each carry `JobRunningTimeoutUSec=10s`, `Following=` the kernel device; `dev-nvme1n1p1/p2.device` carry `1min 30s`.
- Vendor `/usr/lib/systemd/system/tmp.mount` shadowed by generator `tmp.mount` (FragmentPath check).
- Runtime mount units (`SourcePath=/proc/self/mountinfo`): `tmp-.mount_alma.AFFvYd1.mount` (required-by `tmp.mount`), `run-user-1000*.mount`, vendor API mounts.
- Automount units: only the vendor `proc-sys-fs-binfmt_misc.automount`; none generated from fstab.

## Commands run (all read-only)

- `cat -n /etc/fstab`; `ls -la /run/systemd/generator/`; `ls` of `local-fs.target.wants/requires`.
- `cat` of every generator `*.mount`, `*.swap`, `*.device.d/*.conf`.
- `systemctl show -p … -- <unit>` for generated mounts, `local-fs.target`, `local-fs-pre.target`, device units, `-.mount` (with `--` after options).
- `systemctl list-units --type=mount --all`, `list-units --type=automount`, `list-dependencies --reverse`, `systemctl --version`.
- `grep -E ' /(tmp|fast|…)' /proc/self/mountinfo`; `stat`, `uptime -s`.
- Python byte-level comparison of live generator files vs `host/generator.txt` (receipts/).
- `sha256sum` of `before/src/*` vs `SHA256SUMS` and JSON.
- `git -C …/tsukuroi-shokunin log --oneline -4` and `git status --porcelain` (read-only).

Git observation (not mutated): HEAD `e8e5d5b3`, parent `80237118` (declaration commit message "pin controls and disclose predeclaration trials"), `96ad75b8` below it. Working tree has modified files and untracked `corpus/knowledge/mount-unit-fstab-plane-r81.{md,json}` (`??`), so the entry is not committed. The entry's "verified-at 2026-11-04" is self-asserted and not in history. The declaration commit is not characterised here beyond its message.

## Receipts (ScoutSurface/)

- `surface.txt` — full enumeration, exact command output.
- `contradictions.md` — C1–C4, sweep table, gaps G1–G6, not-evaluated list.
- `receipts/live-generator-dump.txt` — byte dump of every generator file.
- `receipts/gen-diff-vs-capture.txt` — diff of live dump against capture.

## Tooling

No tool installed or updated. `pacman` paused and not used. Used only pre-installed `systemctl`,
`python3`, coreutils, `grep`, `awk`, `git` (read-only), `sha256sum`. `RULES.md` read at
`/home/vgpnk/.omp/agent/RULES.md` (first path attempt used a mistyped home and failed; the read
succeeded on the corrected path). Nothing written to `~/.local/bin` or any PATH directory.

## Unknowns

- Real boot delay for a missing `/tmp` or `/fast` device: not measured (no removal test). C3 is a surface contradiction of the stated consequence, not a timing result.
- Whether systemd applies an alias unit's `JobRunningTimeoutUSec` to a job queued through the followed unit: not established from observation.
- Whether generator output at 17:34 came from a `daemon-reload` or another generator run: not established (no journal read).
- `mount_point_is_api` body (why `/dev/shm` gets no unit): not in the snapshot.
- Whether `generator_write_device_timeout` strips only `x-systemd.device-timeout`: its body is outside `fstab-generator.c`; inferred from C1 observation.
- Counter gate `tools/count-mount-rows-r81.py` not run; the milestone's round-80 counter repair and provenance-header closure were not evaluated by this seat.

## Verdict

Contradictions present: C1, C2 (clear), C3 (consequence; mechanism unmeasured), C4 (citation defect).
The entry should not be counted as grounded on the sentences above until corrected. No
fabricated verdict: the counter's `met` finding was not produced by this seat.

## Scratch

`/fast/scratch/hyaku/tsukuroi-r81/ScoutSurface/` held the live dump and diff; copied to
`ScoutSurface/receipts/` and removed before yield.
